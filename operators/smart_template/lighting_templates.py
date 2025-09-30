"""
Lighting Templates Module
Main operators for applying photographic lighting templates.
"""

# Import Blender modules
import bpy
import math
import re
from typing import Dict, List, Tuple, Optional, Any
from mathutils import Vector, Matrix
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty

# Import LumiFlow utilities
from ...utils.common import lumi_is_addon_enabled, lumi_get_light_collection, lumi_move_to_collection
from ...utils.light import lumi_calculate_light_intensity, lumi_calculate_light_size, lumi_set_light_pivot
from ...utils.operators import lumi_ray_cast_between_points, lumi_check_line_of_sight_with_sampling
from ...core.state import get_state
from .template_analyzer import analyze_subject, SubjectAnalysis, analyze_materials_advanced, apply_material_adjustments
from .template_library import get_template, list_templates

# Import error handling system
from .template_error_handling import (
    safe_template_operation, safe_template_context,
    validate_scene_for_template, validate_template_data,
    report_errors, report_exception,
    TemplateError, TemplateNotFoundError, InvalidTemplateError,
    SceneValidationError, TemplateOperationError
)


class LUMI_OT_apply_lighting_template(bpy.types.Operator):
    """Apply photographic lighting template to selected objects"""
    bl_idname = "lumi.apply_lighting_template"
    bl_label = "Apply Lighting Template"
    bl_description = "Apply professional lighting template to selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'OUTLINER_OB_LIGHT'

    # Template selection
    template_id: StringProperty(
        name="Template ID",
        description="Template to apply",
        default="portrait_rembrandt"
    )

    # Scaling options
    auto_scale: BoolProperty(
        name="Auto Scale",
        description="Automatically scale lights to subject size",
        default=True
    )

    intensity_multiplier: FloatProperty(
        name="Intensity Multiplier",
        description="Global intensity multiplier for all lights",
        default=1.0,
        min=0.1,
        max=10.0,
        step=10,
        precision=2
    )

    size_multiplier: FloatProperty(
        name="Size Multiplier", 
        description="Global size multiplier for area lights",
        default=1.0,
        min=0.1,
        max=5.0,
        step=10,
        precision=2
    )

    # Positioning options
    use_camera_relative: BoolProperty(
        name="Camera Relative",
        description="Position lights relative to camera view",
        default=True
    )

    preserve_existing: BoolProperty(
        name="Preserve Existing Lights",
        description="Keep existing lights in scene. If unchecked, removes lights based on current assignment mode: SCENE mode removes G_* lights, CAMERA mode removes C_XX_* lights for active camera",
        default=False
    )

    # Distance override
    manual_distance: FloatProperty(
        name="Manual Distance",
        description="Override automatic distance calculation",
        default=0.0,
        min=0.0,
        max=50.0,
        step=10,
        precision=2
    )

    # Material adaptation
    use_material_adaptation: BoolProperty(
        name="Material Adaptation",
        description="Adjust lighting based on material analysis",
        default=True
    )

    # Obstruction detection properties
    enable_obstruction_detection: BoolProperty(
        name="Enable Obstruction Detection",
        description="Detect and avoid obstructions between lights and targets",
        default=True
    )
    
    obstruction_fallback_strategy: bpy.props.EnumProperty(
        name="Fallback Strategy",
        description="How to handle detected obstructions",
        items=[
            ('ADJUST_POSITION', 'Adjust Position', 'Move light to clear line-of-sight'),
            ('SKIP_LIGHT', 'Skip Light', 'Skip creating obstructed lights'),
            ('WARN_ONLY', 'Warning Only', 'Create light but show warning'),
        ],
        default='ADJUST_POSITION'
    )
    
    show_obstruction_warnings: BoolProperty(
        name="Show Warnings",
        description="Show warnings when obstructions are detected",
        default=True
    )

    @classmethod
    def description(cls, context, properties):
        """Get dynamic description with template information"""
        return "Apply professional lighting template to selected objects"
    
    @classmethod
    def poll(cls, context):
        """Check if operator can be executed"""
        return (lumi_is_addon_enabled() and 
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def validate_context(self, context):
        """Validate context for template application"""
        try:
            if not context or not context.scene:
                return False
            if not lumi_is_addon_enabled():
                return False
            if not context.selected_objects:
                return False
            if not any(obj.type == 'MESH' for obj in context.selected_objects):
                return False
            return True
        except Exception:
            return False

    def execute(self, context):
        """Main execution method with comprehensive error handling"""
        return self._execute_with_error_handling(context)
    
    def _execute_with_error_handling(self, context):
        """Execution with full error handling and optimization"""
        try:
            with safe_template_context(self, "apply template") as operation_stack:
                # 1. Validate scene before starting
                template = get_template(self.template_id)
                if not template:
                    raise TemplateNotFoundError(self.template_id)
                
                # Validate template data
                template_valid, template_errors = validate_template_data(template)
                if not template_valid:
                    raise InvalidTemplateError(self.template_id, template_errors)
                
                # Validate scene
                errors, warnings = validate_scene_for_template(context, template)
                if not report_errors(self, errors, warnings):
                    return {'CANCELLED'}
                
                # 2. Get selected objects
                scene = context.scene
                # Check if we have stored selected object data (from template menu)
                if (hasattr(scene, 'lumi_temp_selected_obj') and 
                    scene.lumi_temp_selected_obj is not None and 
                    scene.lumi_temp_selected_obj.type == 'MESH'):
                    # Use stored selected object data
                    selected_objects = [scene.lumi_temp_selected_obj]
                else:
                    # Fallback to current selection
                    selected_objects = [obj for obj in context.selected_objects 
                                      if obj.type == 'MESH']
                
                # 3. Get/cache analysis and template
                analysis = self._get_cached_analysis(selected_objects, context)
                template = self._get_cached_template()
                
                # 4. Clear existing lights if requested
                if not self.preserve_existing:
                    self.clear_existing_lights(context)
                
                # 5. PLACE: Calculate initial positions (tanpa obstruction)
                # Calculating initial light positions...
                initial_positions = self.calculate_initial_light_positions(analysis, template, context)
                
                # 6. PLACE: Create lights di posisi awal
                # Creating lights...
                lights_created = self.create_lights_at_positions(initial_positions, context)
                
                # 7. CHECK → ADJUST: Cek dan adjust lights yang sudah ada
                if self.enable_obstruction_detection:
                    # Adjusting lights for obstructions...
                    self.adjust_lights_for_obstruction(lights_created, analysis, context)
                
                # Track created lights for recovery
                if lights_created:
                    # Created lights successfully
                    operation_stack.push_object_creation(lights_created)
                else:
                    # No lights to push to operation_stack
                    pass
                
                if not lights_created:
                    # lights_created is empty/None - raising TemplateOperationError
                    raise TemplateOperationError("light creation")
                else:
                    # SUCCESS: lights created successfully
                    pass
                
                # 8. Apply material adjustments
                if self.use_material_adaptation:
                    self.apply_material_adjustments(lights_created, analysis, selected_objects)
                
                # 9. Organize lights
                self._organize_created_lights(lights_created, context)
                
                # 10. Final setup
                self._finalize_template_application(lights_created, context)
                
                # Success message
                success_msg = f"Applied '{self.template_id}' template: {len(lights_created)} lights created"
                
                self.report({'INFO'}, success_msg)
                return {'FINISHED'}
                
        except (TemplateError, TemplateOperationError) as e:
            # Already handled by context manager
            return {'CANCELLED'}
        except Exception as e:
            report_exception(self, e, "apply template")
            return {'CANCELLED'}
    
    def _cleanup_failed_lights(self, lights_to_cleanup):
        """Clean up any lights that were created during a failed operation"""
        if not lights_to_cleanup:
            return
            
        try:
            for light_obj in lights_to_cleanup:
                try:
                    if light_obj and light_obj.name in bpy.data.objects:
                        # Remove from all collections
                        for collection in light_obj.users_collection:
                            collection.objects.unlink(light_obj)
                        
                        # Remove object and data
                        if light_obj.data:
                            bpy.data.lights.remove(light_obj.data, do_unlink=True)
                        else:
                            bpy.data.objects.remove(light_obj, do_unlink=True)
                            
                except Exception as cleanup_error:
                    pass
                    
        except Exception as e:
            pass
    
    def _get_cached_analysis(self, selected_objects, context):
        """Get analysis without complex caching"""
        # Simplified analysis - no caching for now
        self.report({'INFO'}, f"Analyzing {len(selected_objects)} objects...")
        analysis = analyze_subject(selected_objects, context)
        return analysis
    
    

    def _get_cached_template(self):
        """Get template with simplified caching"""
        # Use the new simplified template system
        template = get_template(self.template_id)
        
        # Cache custom templates if they're not built-in
        if template:
            try:
                from .template_library import ALL_TEMPLATES
                if self.template_id not in ALL_TEMPLATES:
                    cache_custom_template(self.template_id, template)
            except ImportError:
                pass  # Template library not available
        
        return template
    
    def _organize_created_lights(self, lights_created, context):
        """Organize created lights in collection"""
        collection = lumi_get_light_collection(context.scene)
        if collection:
            for light_obj in lights_created:
                if light_obj.name not in collection.objects:
                    lumi_move_to_collection(light_obj, collection)
    
    def _finalize_template_application(self, lights_created, context):
        """Final setup after template application"""
        try:
            # Select created lights
            bpy.ops.object.select_all(action='DESELECT')
            
            for light_obj in lights_created:
                light_obj.select_set(True)
            
            if lights_created:
                context.view_layer.objects.active = lights_created[0]
            
        except Exception as e:
            self.report({'ERROR'}, f"Template application failed: {str(e)}")
    
    def calculate_initial_light_positions(self, analysis: SubjectAnalysis, template: Dict[str, Any], context: bpy.types.Context) -> List[Dict[str, Any]]:
        """Calculate initial light positions WITHOUT obstruction logic"""
        positions = []
        
        # Safety check for subject center
        subject_center = analysis.bounds.get("center")
        if subject_center is None:
            # Fallback to origin if center is not available
            subject_center = Vector((0, 0, 0))
            self.report({'WARNING'}, "Subject center not found, using origin as fallback")
        
        # Calculate base distance
        if self.manual_distance > 0:
            base_distance = self.manual_distance
        else:
            base_distance = template.get('settings', {}).get('base_distance', 2.0)
            if self.auto_scale:
                # Scale based on subject size
                subject_radius = analysis.bounds["radius"]
                scale_factor = max(0.5, subject_radius)
                base_distance *= scale_factor
        
        # Get camera info if using camera relative positioning
        camera_matrix = Matrix()
        if self.use_camera_relative and context.scene.camera:
            camera_matrix = context.scene.camera.matrix_world.copy()

        # Process each light in template
        for light_index, light_template in enumerate(template.get('lights', [])):
            try:
                position_data = light_template.get('position', {})
                method = position_data.get('method', 'spherical')
                params = position_data.get('params', {})
                
                light_name = light_template.get('name', f'Light_{light_index}')
                
                world_position = None  # Initialize
                
                if method == 'spherical':
                    # Spherical coordinates (azimuth, elevation, distance)
                    azimuth = math.radians(params.get('azimuth', 0))
                    elevation = math.radians(params.get('elevation', 30))
                    
                    # Safety check for base_distance
                    if base_distance is None or base_distance <= 0:
                        base_distance = 2.0
                        print("WARNING: Invalid base_distance, using default value 2.0")
                    
                    distance = params.get('distance', 1.0) * base_distance
                    
                    # Convert to cartesian
                    x = distance * math.cos(elevation) * math.sin(azimuth)
                    y = -distance * math.cos(elevation) * math.cos(azimuth)  # Negative for front
                    z = distance * math.sin(elevation)
                    
                    print(f"Spherical: azimuth={azimuth}, elevation={elevation}, distance={distance}")
                    print(f"Cartesian: x={x}, y={y}, z={z}")
                    
                    world_position = subject_center + Vector((x, y, z))
                    print(f"World position (spherical): {world_position}")

                elif method == 'cartesian':
                    # Direct cartesian coordinates
                    x = params.get('x', 0)
                    y = params.get('y', 0)
                    z = params.get('z', 0)
                    
                    # Safety check for base_distance
                    if base_distance is None or base_distance <= 0:
                        base_distance = 2.0
                        print("WARNING: Invalid base_distance, using default value 2.0")
                    
                    x = x * base_distance
                    y = y * base_distance
                    z = z * base_distance
                    
                    if dimensions is None:
                        dimensions = Vector((1, 1, 1))
                        self.report({'WARNING'}, "Subject dimensions not found, using default dimensions")
                    
                    offset = Vector((
                        rel_x * dimensions.x,
                        rel_y * dimensions.y,
                        rel_z * dimensions.z
                    ))
                    
                    world_position = subject_center + offset

                elif method == 'direct':
                    # Direct world coordinates (absolute positioning)
                    location = params.get('location', (0, 0, 0))
                    
                    if isinstance(location, (list, tuple)) and len(location) >= 3 and all(loc is not None for loc in location):
                        world_position = Vector(location)
                    else:
                        world_position = subject_center + Vector((0, -base_distance, base_distance))

                else:
                    # Default to spherical with default values
                    world_position = subject_center + Vector((0, -base_distance, base_distance))
                
                # Final validation
                if world_position is None:
                    self.report({'ERROR'}, "world_position is None!")
                    raise ValueError("world_position is None")
                
                # Apply camera relative transformation if needed
                if self.use_camera_relative and context.scene.camera:
                    # Transform position relative to camera view
                    # Get camera basis vectors in world space
                    cam_matrix = camera_matrix.to_3x3()
                    cam_forward = cam_matrix @ Vector((0, 0, -1))  # Camera looks down -Z
                    cam_right = cam_matrix @ Vector((1, 0, 0))
                    cam_up = cam_matrix @ Vector((0, 1, 0))
                    
                    # Get original position relative to subject
                    local_offset = world_position - subject_center
                    
                    # Transform the offset using camera's coordinate system
                    # This maintains the relative positioning between lights
                    transformed_offset = (
                        local_offset.x * cam_right +
                        local_offset.y * cam_forward +
                        local_offset.z * cam_up
                    )
                    
                    final_position = subject_center + transformed_offset
                    world_position = final_position

                # Prepare position data WITHOUT obstruction information
                position_data = {
                    'light_template': light_template,
                    'world_position': world_position,
                    'target_position': subject_center,
                    'distance': base_distance
                }
                
                positions.append(position_data)
                
            except Exception as e:
                self.report({'ERROR'}, f"Error calculating position for light {light_index}: {str(e)}")
                continue

        return positions
    
    def _get_safe_target_position(self, target_obj: bpy.types.Object) -> Vector:
        """Get target position using the same method as calculate_bounds (bound_box center)"""
        try:
            # Use the same method as calculate_bounds - bound_box center
            if hasattr(target_obj, 'bound_box'):
                # Get world-space bounding box corners
                bbox_corners = [Vector(corner) @ target_obj.matrix_world for corner in target_obj.bound_box]
                
                # Calculate min/max coordinates
                min_coord = Vector(bbox_corners[0])
                max_coord = Vector(bbox_corners[0])
                
                for corner in bbox_corners:
                    for i in range(3):
                        min_coord[i] = min(min_coord[i], corner[i])
                        max_coord[i] = max(max_coord[i], corner[i])
                
                # Calculate center (same as calculate_bounds)
                center = (min_coord + max_coord) * 0.5
                return center
            else:
                # Fallback to object's world location
                return target_obj.matrix_world.translation
        except Exception as e:
            # Ultimate fallback to object's world location
            return target_obj.matrix_world.translation
    
    def _check_and_handle_obstruction(self, world_position: Vector, target_objects: List[bpy.types.Object], 
                                    context: bpy.types.Context, light_name: str) -> Dict[str, Any]:
        """Check if light has clear line-of-sight to target objects"""
        obstruction_result = {
            'has_obstruction': False,
            'hit_object': None,
            'hit_location': None,
            'distance': 0.0
        }
        
        try:
            # Check line-of-sight to each target object
            for target_obj in target_objects:
                # Use the object's center as target point with safe fallback
                target_position = self._get_safe_target_position(target_obj)
                
                # Perform raycast with multi-point sampling for robust detection
                has_clear_path, sample_results = lumi_check_line_of_sight_with_sampling(
                    context, world_position, target_position, 
                    exclude_objects=[target_obj],  # Exclude the target itself
                    sample_radius=0.1,
                    sample_count=5
                )
                
                if not has_clear_path:
                    obstruction_result['has_obstruction'] = True
                    # Find the closest obstruction from sample results
                    for sample in sample_results:
                        if sample['has_obstruction'] and sample['hit_object']:
                            obstruction_result['hit_object'] = sample['hit_object']
                            obstruction_result['hit_location'] = sample['hit_location']
                            obstruction_result['distance'] = sample['distance']
                            break
                    break  # Found obstruction, no need to check other targets
                    
        except Exception as e:
            # If raycast fails, assume no obstruction to avoid breaking the flow
            print(f"Obstruction detection failed for {light_name}: {str(e)}")
            
        return obstruction_result
    
    def _find_alternative_position(self, original_position: Vector, target_objects: List[bpy.types.Object], 
                                 context: bpy.types.Context) -> Optional[Vector]:
        """Find alternative position with clear line-of-sight to targets using new logic"""
        try:
            # Calculate average target position and bounds
            avg_target = Vector((0, 0, 0))
            max_z = float('-inf')
            min_z = float('inf')
            
            for target_obj in target_objects:
                target_pos = self._get_safe_target_position(target_obj)
                avg_target += target_pos
                max_z = max(max_z, target_pos.z)
                min_z = min(min_z, target_pos.z)
            
            avg_target /= len(target_objects)
            target_height = max_z - min_z
            target_top_z = max_z
            
            # Determine light position relative to target
            light_z = original_position.z
            
            # Strategy 1: Light is above or at same level as target
            if light_z >= target_top_z - 0.1:  # Allow small tolerance
                # Try moving closer to target (obstruction point + 1 unit)
                alternative_pos = self._try_closer_position_adjustment(
                    original_position, avg_target, target_objects, context
                )
                if alternative_pos:
                    return alternative_pos
            
            # Strategy 2: Light is below target
            else:
                # First: Lift light to target level
                lifted_position = original_position.copy()
                lifted_position.z = target_top_z + 0.5  # Lift slightly above target top
                
                # Check if lifted position has clear line-of-sight
                if self._has_clear_line_of_sight_to_all_targets(lifted_position, target_objects, context):
                    return lifted_position
                
                # If still obstructed, try moving closer
                alternative_pos = self._try_closer_position_adjustment(
                    lifted_position, avg_target, target_objects, context
                )
                if alternative_pos:
                    return alternative_pos
            
            # No fallback to old strategies - use new logic only
                    
        except Exception as e:
            print(f"Failed to find alternative position: {str(e)}")
            
        return None
    
    def _try_closer_position_adjustment(self, original_position: Vector, avg_target: Vector, 
                                      target_objects: List[bpy.types.Object], context: bpy.types.Context) -> Optional[Vector]:
        """Try moving closer to target using obstruction point + 1 unit logic"""
        try:
            # Type checking and validation
            if not isinstance(original_position, Vector):
                print(f"Error: original_position is not Vector: {type(original_position)}")
                return None
            if not isinstance(avg_target, Vector):
                print(f"Error: avg_target is not Vector: {type(avg_target)}")
                return None
            
            # Find the closest obstruction point
            closest_obstruction = None
            min_distance = float('inf')
            
            for target_obj in target_objects:
                target_pos = self._get_safe_target_position(target_obj)
                
                # Validate target_pos
                if not isinstance(target_pos, Vector):
                    print(f"Error: target_pos is not Vector: {type(target_pos)}")
                    continue
                
                # Cast ray to find obstruction point
                has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
                    context, original_position, target_pos, exclude_objects=[target_obj]
                )
                
                if has_obstruction and hit_location and distance < min_distance:
                    # Validate hit_location
                    if isinstance(hit_location, Vector):
                        closest_obstruction = hit_location
                        min_distance = distance
                    else:
                        print(f"Error: hit_location is not Vector: {type(hit_location)}")
            
            if closest_obstruction and isinstance(closest_obstruction, Vector):
                # Calculate direction from obstruction to target
                to_target = (avg_target - closest_obstruction).normalized()
                
                # Move 1 unit beyond obstruction point towards target
                new_position = closest_obstruction + to_target * 1.0
                
                # Check if this position has clear line-of-sight
                if self._has_clear_line_of_sight_to_all_targets(new_position, target_objects, context):
                    return new_position
                
                # Try multiple steps if single step doesn't work
                for step in [0.5, 1.5, 2.0]:
                    new_position = closest_obstruction + to_target * step
                    if self._has_clear_line_of_sight_to_all_targets(new_position, target_objects, context):
                        return new_position
            else:
                print(f"Error: closest_obstruction is not valid: {closest_obstruction}")
            
        except Exception as e:
            print(f"Closer position adjustment failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
        return None
    
    def _has_clear_line_of_sight_to_all_targets(self, position: Vector, target_objects: List[bpy.types.Object], 
                                             context: bpy.types.Context) -> bool:
        """Check if position has clear line-of-sight to all target objects"""
        try:
            for target_obj in target_objects:
                target_pos = self._get_safe_target_position(target_obj)
                
                # Use multi-point sampling for robust detection
                has_clear_path, _ = lumi_check_line_of_sight_with_sampling(
                    context, position, target_pos,
                    exclude_objects=[target_obj],
                    sample_radius=0.1,
                    sample_count=3  # Reduced for performance
                )
                
                if not has_clear_path:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Line-of-sight check failed: {str(e)}")
            return False
    
    def create_lights_at_positions(self, positions: List[Dict[str, Any]], context: bpy.types.Context) -> List[bpy.types.Object]:
        """Create lights at specified positions"""
        try:
            created_lights = []

            for position_data in positions:
                try:
                    light_template = position_data['light_template']
                    world_pos = position_data['world_position']
                    target_pos = position_data['target_position']
                    distance = position_data['distance']

                    # Get light properties
                    light_name = light_template.get('name', 'Template Light')
                    light_type = light_template.get('type', 'AREA')
                    properties = light_template.get('properties', {})

                    # Create light data
                    light_data = bpy.data.lights.new(name=light_name, type=light_type)
                    
                    # Get subject radius for adaptive calculations
                    subject_radius = 1.0  # Default value since analysis not available
                    
                    # Apply light properties with adaptive resolution
                    # Process shape first to ensure proper handling of size_y
                    if 'shape' in properties and light_data.type == 'AREA':
                        shape_value = self._resolve_adaptive_property(properties['shape'], subject_radius, 'shape')
                        light_data.shape = shape_value if shape_value in ['RECTANGLE', 'SQUARE', 'DISK', 'ELLIPSE'] else 'RECTANGLE'
                    
                    for prop_name, prop_value in properties.items():
                        # Skip shape as it's already processed
                        if prop_name == "shape" and light_data.type == 'AREA':
                            continue
                            
                        # Resolve adaptive properties
                        resolved_value = self._resolve_adaptive_property(prop_value, subject_radius, prop_name)
                        
                        if prop_name == "intensity":
                            light_data.energy = resolved_value * self.intensity_multiplier
                        elif prop_name == "color":
                            if len(resolved_value) >= 3:
                                light_data.color = resolved_value[:3]  # RGB only
                        elif prop_name == "size" and light_data.type == 'AREA':
                            final_size = resolved_value
                            # Auto-scale disabled since analysis not available
                            light_data.size = final_size * self.size_multiplier
                            # Set default size_y only if not explicitly defined and shape supports it
                            if hasattr(light_data, 'shape') and light_data.shape in ['RECTANGLE', 'ELLIPSE'] and 'size_y' not in properties:
                                light_data.size_y = light_data.size
                        elif prop_name == "size_y" and light_data.type == 'AREA':
                            final_size_y = resolved_value
                            # Auto-scale disabled since analysis not available
                            if hasattr(light_data, 'shape') and light_data.shape in ['RECTANGLE', 'ELLIPSE']:
                                light_data.size_y = final_size_y * self.size_multiplier
                        elif prop_name == "use_shadow":
                            light_data.use_shadow = resolved_value
                        elif prop_name == "shadow_soft_size":
                            light_data.shadow_soft_size = resolved_value
                        elif prop_name == "spot_angle" and light_data.type == 'SPOT':
                            light_data.spot_size = math.radians(resolved_value)
                        elif prop_name == "spot_blend" and light_data.type == 'SPOT':
                            light_data.spot_blend = resolved_value
                        elif prop_name == "spot_size" and light_data.type == 'SPOT':
                            light_data.spot_size = resolved_value
                        elif prop_name == "angle" and light_data.type == 'SUN':
                            light_data.angle = math.radians(resolved_value)
                    
                    # Set default values if not specified in properties
                    if not hasattr(light_data, 'energy') or light_data.energy == 0:
                        light_data.energy = 100 * self.intensity_multiplier
                    if light_data.type == 'AREA' and light_data.size == 0:
                        light_data.size = 1.0 * self.size_multiplier

                    # Create light object
                    light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
                    light_obj.location = world_pos

                    # Set up light orientation
                    rotation_data = light_template.get('rotation', {})
                    rotation_method = rotation_data.get('method', 'target')
                    
                    if rotation_method == 'euler':
                        # Direct euler angles - check both 'euler' and 'rotation' parameter names
                        euler_angles = (rotation_data.get('params', {}).get('euler') or 
                                      rotation_data.get('params', {}).get('rotation') or 
                                      (0, 0, 0))
                        
                        # Apply camera relative transformation to euler angles if enabled
                        if self.use_camera_relative and context.scene.camera:
                            # Convert euler to quaternion for transformation
                            from mathutils import Euler
                            base_euler = Euler(euler_angles, 'XYZ')
                            base_rotation = base_euler.to_quaternion()
                            
                            # Get camera rotation
                            camera_rotation = context.scene.camera.rotation_euler.to_quaternion()
                            
                            # Combine rotations: camera rotation + base euler rotation
                            final_rotation = camera_rotation @ base_rotation
                            
                            light_obj.rotation_euler = final_rotation.to_euler()
                        else:
                            light_obj.rotation_euler = euler_angles
                    elif target_pos and rotation_method in ['target_subject', 'target']:
                        # Point towards target
                        direction = (target_pos - world_pos).normalized()
                        if direction.length > 0.001:  # Avoid zero-length vectors
                            rot_quat = direction.to_track_quat('-Z', 'Y')
                            light_obj.rotation_euler = rot_quat.to_euler()
                    
                    # Set pivot point for LumiFlow positioning system (if target exists)
                    if target_pos:
                        lumi_set_light_pivot(light_obj, target_pos)

                    # Add to scene
                    context.collection.objects.link(light_obj)
                    created_lights.append(light_obj)
                    
                    # Automatic camera light assignment
                    try:
                        from ...core.camera_manager import assign_light_to_active_camera
                        assign_light_to_active_camera(light_obj)
                    except Exception:
                        pass

                except Exception as e:
                    self.report({'ERROR'}, f"Error creating light '{light_name}': {e}")
                    continue

            return created_lights

        except Exception as e:
            self.report({'ERROR'}, f"Error in create_lights_at_positions: {e}")
            return []

    def adjust_lights_for_obstruction(self, lights: List[bpy.types.Object], analysis: SubjectAnalysis, context: bpy.types.Context):
        """Check obstruction pada lights yang sudah ada dan adjust posisinya"""
        state = get_state()
        target_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        # If no selected objects, use the analysis subject (if available)
        if not target_objects and hasattr(analysis, 'subject_object') and analysis.subject_object:
            target_objects = [analysis.subject_object]
        
        # Make a copy of lights list since we might modify it
        lights_to_process = lights.copy()
        
        for light in lights_to_process:
            # Skip if light was already removed
            if light.name not in bpy.data.objects:
                continue
                
            light_name = light.name
            
            # Check obstruction
            obstruction_result = self._check_and_handle_obstruction_object_level(
                light, target_objects, context
            )
            
            if obstruction_result['has_obstruction']:
                # Record obstruction
                if obstruction_result['hit_object']:
                    state.add_detected_obstruction(
                        light_name, 
                        obstruction_result['hit_object'].name, 
                        obstruction_result['hit_location']
                    )
                
                # Handle berdasarkan strategy
                if self.obstruction_fallback_strategy == 'SKIP_LIGHT':
                    # Hapus light yang terhalang
                    bpy.data.objects.remove(light, do_unlink=True)
                    if light in lights:  # Remove dari original list
                        lights.remove(light)
                    state.add_skipped_light(light_name, "Obstruction detected, fallback strategy: SKIP_LIGHT")
                    
                elif self.obstruction_fallback_strategy == 'ADJUST_POSITION':
                    # Cari alternative position
                    alternative_pos = self._find_alternative_position(
                        light.location, target_objects, context
                    )
                    
                    if alternative_pos:
                        original_position = light.location.copy()
                        light.location = alternative_pos  # Adjust object langsung
                        
                        # Re-orient light to face target after position adjustment
                        if target_objects and len(target_objects) > 0:
                            # Calculate target position (center of target objects)
                            target_center = Vector((0, 0, 0))
                            for obj in target_objects:
                                target_center += obj.location
                            target_center /= len(target_objects)
                            
                            # Point light towards target
                            direction = (target_center - light.location).normalized()
                            if direction.length > 0.001:  # Avoid zero-length vectors
                                rot_quat = direction.to_track_quat('-Z', 'Y')
                                light.rotation_euler = rot_quat.to_euler()
                                
                                # Update pivot point for LumiFlow system
                                if hasattr(light, "Lumi_pivot_world"):
                                    lumi_set_light_pivot(light, target_center)
                        
                        state.add_adjusted_light(light_name, original_position, light.location)
                        
                        if self.show_obstruction_warnings:
                            self.report({'WARNING'}, f"Adjusted {light_name} position to avoid obstruction")
                            
                        # Store original position di custom properties
                        light["lumi_original_position"] = original_position
                        light["lumi_position_adjusted"] = True
                        light["lumi_adjustment_reason"] = "obstruction_detected"
                    else:
                        # Hapus jika tidak ada alternative
                        bpy.data.objects.remove(light, do_unlink=True)
                        if light in lights:  # Remove dari original list
                            lights.remove(light)
                        state.add_skipped_light(light_name, "No clear position found, fallback strategy: ADJUST_POSITION")
                        
                elif self.obstruction_fallback_strategy == 'WARN_ONLY':
                    if self.show_obstruction_warnings:
                        self.report({'WARNING'}, f"{light_name} has line-of-sight obstruction")
                        
                        # Store obstruction info in custom properties
                        light["lumi_obstruction_detected"] = True
                        light["lumi_obstruction_timestamp"] = context.scene.frame_current
                        if obstruction_result['hit_object']:
                            light["lumi_obstruction_object"] = obstruction_result['hit_object'].name

    def _check_and_handle_obstruction_object_level(self, light_object: bpy.types.Object, target_objects: List[bpy.types.Object], context: bpy.types.Context) -> Dict[str, Any]:
        """Check obstruction for an existing light object"""
        obstruction_result = {
            'has_obstruction': False,
            'hit_object': None,
            'hit_location': None,
            'distance': 0.0
        }
        
        if not target_objects:
            return obstruction_result
        
        light_pos = light_object.location
        
        # Check line-of-sight to all target objects
        for target_obj in target_objects:
            target_pos = self._get_safe_target_position(target_obj)
            
            # Cast ray from light to target
            has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
                context, light_pos, target_pos, exclude_objects=[target_obj]
            )
            
            if has_obstruction and hit_object:
                obstruction_result['has_obstruction'] = True
                obstruction_result['hit_object'] = hit_object
                obstruction_result['hit_location'] = hit_location
                obstruction_result['distance'] = distance
                break  # Found obstruction, no need to check other targets
        
        return obstruction_result

    def _get_safe_target_position(self, target_obj: bpy.types.Object) -> Vector:
        """Get safe target position for ray casting"""
        if hasattr(target_obj, 'matrix_world'):
            return target_obj.matrix_world.translation
        else:
            return Vector((0, 0, 0))

    def _resolve_adaptive_property(self, prop_value, subject_radius, property_name):
        """Resolve adaptive property values based on subject size"""
        if isinstance(prop_value, str):
            if prop_value == "adaptive":
                if property_name == "intensity":
                    return max(50, min(300, subject_radius * 80))
                elif property_name == "size":
                    return max(1.0, subject_radius * 1.5)
            elif prop_value == "adaptive_soft":
                if property_name == "intensity":
                    return max(30, min(150, subject_radius * 40))
            elif prop_value == "adaptive_large":
                if property_name == "size":
                    return max(5.0, subject_radius * 4.0)
                elif property_name == "intensity":
                    return max(80, min(400, subject_radius * 100))
            elif prop_value == "adaptive_small":
                if property_name == "size":
                    return max(0.5, subject_radius * 0.8)
        
        return prop_value

    def apply_material_adjustments(self, lights: List[bpy.types.Object], analysis: SubjectAnalysis, selected_objects: List[bpy.types.Object]):
        """Apply material-based light adjustments with advanced analysis"""
        try:
            # Use advanced material adaptation if enabled
            if self.use_material_adaptation:
                # Perform advanced material analysis
                advanced_analysis = analyze_materials_advanced(selected_objects)
                recommendations = advanced_analysis.get("recommendations", {})
                
                if recommendations:
                    self.report({'INFO'}, f"Applying advanced material adaptations for {len(advanced_analysis['types'])} material types")
                    
                    # Apply advanced recommendations to each light
                    for light_obj in lights:
                        try:
                            apply_material_adjustments(light_obj, recommendations)
                            
                            # Apply additional template-specific adjustments
                            self.apply_template_specific_adjustments(light_obj, advanced_analysis)
                            
                        except Exception as e:
                            pass
                            continue
                    
                    return
            
            # Fallback to basic material adjustments
            self.apply_basic_material_adjustments(lights, analysis)
            
        except Exception as e:
            pass
            # Fallback to basic adjustments
            self.apply_basic_material_adjustments(lights, analysis)
   
    def apply_basic_material_adjustments(self, lights: List[bpy.types.Object], analysis: SubjectAnalysis):
        """Apply basic material-based light adjustments (legacy method)"""
        try:
            material_type = analysis.materials.get("dominant_type", "dielectric")
            roughness = analysis.materials.get("average_roughness", 0.5)
            has_emission = analysis.materials.get("has_emission", False)

            for light_obj in lights:
                try:
                    light_data = light_obj.data
                    
                    # Adjust intensity based on material type
                    if material_type == "metallic":
                        # Metallic surfaces need more intensity
                        light_data.energy *= 1.3
                    elif material_type == "glass":
                        # Glass needs softer, more diffused lighting
                        light_data.energy *= 0.8
                        if light_data.type == 'AREA':
                            light_data.size *= 1.5  # Larger area for softer shadows

                    # Adjust for roughness
                    if roughness < 0.3:  # Very smooth surfaces
                        # Need more diffused lighting to avoid harsh reflections
                        if light_data.type == 'AREA':
                            light_data.size *= 1.2
                    elif roughness > 0.7:  # Very rough surfaces  
                        # Can handle more direct lighting
                        light_data.energy *= 1.1

                    # Reduce intensity if subject has emission
                    if has_emission:
                        light_data.energy *= 0.7

                except Exception as e:
                    pass
                    continue

        except Exception as e:
            pass

    def apply_template_specific_adjustments(self, light_obj: bpy.types.Object, advanced_analysis: Dict[str, Any]):
        """Apply template-specific adjustments based on advanced material analysis"""
        try:
            properties = advanced_analysis.get("properties", {})
            complexity = advanced_analysis.get("complexity_score", 1.0)
            
            # Additional adjustments based on material complexity
            if complexity > 2.0:
                # High complexity materials need more careful lighting
                if hasattr(light_obj.data, 'energy'):
                    light_obj.data.energy *= 0.95  # Slightly reduce intensity
            
            # Glass-specific enhancements
            if properties.get("has_glass", False):
                # Ensure area lights for glass materials
                if light_obj.data.type in ['SPOT', 'POINT']:
                    # Convert to area light for better glass rendering
                    # Note: In production, this might be too aggressive
                    pass
                
                # Adjust light positioning for glass (if possible)
                # This would require more sophisticated positioning logic
                pass
            
            # Metallic material enhancements
            if properties.get("has_metallic", False):
                # Ensure softer shadows for metallic reflections
                if light_obj.data.type == 'SUN' and hasattr(light_obj.data, 'angle'):
                    light_obj.data.angle = max(light_obj.data.angle, 0.05)  # Minimum softness
            
            # Emission material adjustments
            if properties.get("has_emission", False):
                # Reduce ambient contribution from all lights
                if hasattr(light_obj.data, 'energy'):
                    light_obj.data.energy *= 0.85
                
                # Enhance contrast by adjusting light color temperature
                if hasattr(light_obj.data, 'color'):
                    # Slightly cool the lights to contrast with warm emission
                    current_color = list(light_obj.data.color)
                    current_color[0] *= 0.95  # Reduce red slightly
                    current_color[2] *= 1.05  # Increase blue slightly
                    light_obj.data.color = current_color
            
            # SSS material adjustments
            if properties.get("has_sss", False):
                # Ensure area lights for SSS-friendly lighting
                if light_obj.data.type == 'AREA' and hasattr(light_obj.data, 'size'):
                    # Increase area light size for better SSS
                    light_obj.data.size *= 1.1
                
                # Warm up the color temperature slightly for skin tones
                if hasattr(light_obj.data, 'color'):
                    current_color = list(light_obj.data.color)
                    current_color[0] *= 1.02  # Slightly warmer
                    current_color[1] *= 1.01
                    light_obj.data.color = current_color
                    
        except Exception as e:
            pass

    def clear_existing_lights(self, context):
        """Remove existing lights from LumiFlow collection based on assignment mode"""
        try:
            collection = lumi_get_light_collection(context.scene)
            if not collection:
                return

            # Get current assignment mode
            assignment_mode = getattr(context.scene, 'lumi_light_assignment_mode', 'SCENE')
            
            all_lights = [obj for obj in collection.objects if obj.type == 'LIGHT']
            lights_to_remove = []
            
            if assignment_mode == 'SCENE':
                # In SCENE mode, only remove lights with G_ prefix (global lights)
                lights_to_remove = [light for light in all_lights if light.name.startswith('G_')]
            else:  # CAMERA mode
                # In CAMERA mode, only remove lights with C_XX prefix matching active camera
                active_camera = context.scene.camera
                if active_camera:
                    camera_name = active_camera.name
                    
                    # Determine camera prefix
                    if camera_name.endswith('.001'):
                        camera_prefix = 'C_01'
                    elif camera_name.endswith('.002'):
                        camera_prefix = 'C_02'
                    elif camera_name.endswith('.003'):
                        camera_prefix = 'C_03'
                    elif camera_name.endswith('.004'):
                        camera_prefix = 'C_04'
                    elif camera_name.endswith('.005'):
                        camera_prefix = 'C_05'
                    elif camera_name.endswith('.006'):
                        camera_prefix = 'C_06'
                    elif camera_name.endswith('.007'):
                        camera_prefix = 'C_07'
                    elif camera_name.endswith('.008'):
                        camera_prefix = 'C_08'
                    elif camera_name.endswith('.009'):
                        camera_prefix = 'C_09'
                    elif camera_name == 'Camera':
                        camera_prefix = 'C_00'
                    else:
                        # Extract number from camera name or use default
                        import re
                        match = re.search(r'\d+', camera_name)
                        camera_num = match.group(0).zfill(2) if match else '00'
                        camera_prefix = f'C_{camera_num}'
                    
                    # Remove lights with matching camera prefix
                    lights_to_remove = [light for light in all_lights if light.name.startswith(camera_prefix + '_')]
                else:
                    # No active camera, remove all C_00 lights (default)
                    lights_to_remove = [light for light in all_lights if light.name.startswith('C_00_')]
            
            # Remove the filtered lights
            for light_obj in lights_to_remove:
                try:
                    # Remove from collection
                    collection.objects.unlink(light_obj)
                    
                    # Remove from scene if not in other collections
                    if len(light_obj.users_collection) == 0:
                        bpy.data.objects.remove(light_obj, do_unlink=True)
                        
                except Exception as e:
                    pass

        except Exception as e:
            pass

    def invoke(self, context, event):
        """Invoke operator with dialog"""
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        """Draw operator properties in dialog"""
        layout = self.layout
        
        # Template selection
        layout.label(text="Template Settings:", icon='LIGHT')
        layout.prop(self, "template_id")
        
        layout.separator()
        
        # Scaling options
        layout.label(text="Scaling Options:", icon='TRANSFORM_ORIGINS')
        layout.prop(self, "auto_scale")
        layout.prop(self, "intensity_multiplier")
        layout.prop(self, "size_multiplier")
        
        layout.separator()
        
        # Positioning options
        layout.label(text="Positioning Options:", icon='OBJECT_ORIGIN')
        layout.prop(self, "use_camera_relative")
        row = layout.row()
        row.prop(self, "manual_distance")
        row.enabled = not self.auto_scale
        
        layout.separator()
        
        # Advanced options
        layout.label(text="Advanced Options:", icon='PREFERENCES')
        layout.prop(self, "preserve_existing")
        
        layout.separator()
        
        # Obstruction detection options
        layout.label(text="Obstruction Detection:", icon='MODIFIER')
        layout.prop(self, "enable_obstruction_detection")
        
        if self.enable_obstruction_detection:
                layout.prop(self, "obstruction_fallback_strategy")
                layout.prop(self, "show_obstruction_warnings")


class LUMI_OT_preview_template(bpy.types.Operator):
    bl_idname = "lumi.preview_template"
    bl_label = "Preview Template"
    bl_description = "Preview lighting template with real-time adjustments"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Template selection
    template_id: StringProperty(
        name="Template ID",
        description="Template to preview",
        default="portrait_rembrandt"
    )
    
    # Preview state
    _preview_lights = []
    _original_lights = []
    _preview_collection = None
    _intensity_multiplier = 1.0
    _rotation_offset = 0.0
    _current_template_index = 0
    _available_templates = []
    
    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and 
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)
    
    def invoke(self, context, event):
        """Initialize preview mode"""
        try:
            # 1. Create temporary collection for preview lights
            if "LumiFlow_Preview" in bpy.data.collections:
                bpy.data.collections.remove(bpy.data.collections["LumiFlow_Preview"])
            
            self._preview_collection = bpy.data.collections.new("LumiFlow_Preview")
            context.scene.collection.children.link(self._preview_collection)
            
            # 2. Store original lights state
            self._original_lights = []
            for obj in context.scene.objects:
                if obj.type == 'LIGHT':
                    self._original_lights.append({
                        'object': obj,
                        'visible': obj.visible_get(),
                        'energy': obj.data.energy if hasattr(obj.data, 'energy') else 1.0
                    })
                    # Dim original lights
                    obj.hide_viewport = True
            
            # 3. Get available templates for cycling
            self._available_templates = self._get_available_templates()
            if self.template_id in self._available_templates:
                self._current_template_index = self._available_templates.index(self.template_id)
            else:
                self._current_template_index = 0
                if self._available_templates:
                    self.template_id = self._available_templates[0]
            
            # 4. Create initial preview lights
            if not self.create_preview_lights(context):
                return self.cancel(context)
            
            # 5. Start modal
            context.window_manager.modal_handler_add(self)
            
            # Show instructions
            self.report({'INFO'}, "Preview Mode: Scroll=Intensity, R=Rotate, Tab=Next Template, Enter=Apply, Esc=Cancel")
            
            return {'RUNNING_MODAL'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to start preview: {str(e)}")
            return self.cancel(context)
    
    def modal(self, context, event):
        """Handle modal interactions"""
        if event.type == 'MOUSEMOVE':
            return {'PASS_THROUGH'}
        
        # Intensity adjustment with mouse wheel
        if event.type == 'WHEELUPMOUSE':
            self._intensity_multiplier = min(3.0, self._intensity_multiplier * 1.1)
            self.update_preview_intensity(context)
            self.report({'INFO'}, f"Intensity: {self._intensity_multiplier:.2f}")
            return {'RUNNING_MODAL'}
            
        elif event.type == 'WHEELDOWNMOUSE':
            self._intensity_multiplier = max(0.1, self._intensity_multiplier / 1.1)
            self.update_preview_intensity(context)
            self.report({'INFO'}, f"Intensity: {self._intensity_multiplier:.2f}")
            return {'RUNNING_MODAL'}
        
        # Rotate setup with R key
        elif event.type == 'R' and event.value == 'PRESS':
            self._rotation_offset += math.radians(15)  # 15 degrees
            self.update_preview_rotation(context)
            self.report({'INFO'}, f"Rotation: {math.degrees(self._rotation_offset):.0f}°")
            return {'RUNNING_MODAL'}
        
        # Cycle templates with Tab
        elif event.type == 'TAB' and event.value == 'PRESS':
            if self._available_templates:
                self._current_template_index = (self._current_template_index + 1) % len(self._available_templates)
                self.template_id = self._available_templates[self._current_template_index]
                self.recreate_preview_lights(context)
                template = get_template(self.template_id)
                template_name = template.get('name', self.template_id) if template else self.template_id
                self.report({'INFO'}, f"Template: {template_name}")
            return {'RUNNING_MODAL'}
        
        # Confirm and apply template
        elif event.type in {'LEFTMOUSE', 'RET'} and event.value == 'PRESS':
            return self.confirm_and_apply(context)
        
        # Cancel preview
        elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            return self.cancel(context)
        
        return {'PASS_THROUGH'}
    
    def create_preview_lights(self, context):
        """Create semi-transparent preview lights"""
        try:
            # Clear existing preview lights
            self.cleanup_preview_lights()
            
            # Get template
            template = get_template(self.template_id)
            if not template:
                self.report({'ERROR'}, f"Template '{self.template_id}' not found")
                return False
            
            # Analyze subject
            analysis = analyze_subject(context.selected_objects, context)
            
            # Calculate positions
            positions = self.calculate_initial_light_positions(analysis, template, context)
            
            # Create preview lights
            for position_data in positions:
                light_template = position_data['light_template']
                world_pos = position_data['world_position']
                target_pos = position_data['target_position']
                
                # Create light
                light_name = f"Preview_{light_template.get('name', 'Light')}"
                light_type = light_template.get('type', 'AREA')
                properties = light_template.get('properties', {})
                
                # Create light data with preview characteristics
                light_data = bpy.data.lights.new(name=light_name, type=light_type)
                light_data.energy = properties.get('intensity', 100) * 0.5  # 50% intensity for preview
                
                # Set preview color (slightly tinted for visibility)
                color = properties.get('color', (1.0, 1.0, 1.0))
                preview_color = (color[0] * 0.8 + 0.2, color[1] * 0.8 + 0.2, color[2] * 0.9 + 0.1)  # Slight cyan tint
                light_data.color = preview_color
                
                # Configure type-specific properties
                if light_type == 'AREA':
                    shape = properties.get('shape', 'RECTANGLE')
                    light_data.shape = shape if shape in ['RECTANGLE', 'SQUARE', 'DISK', 'ELLIPSE'] else 'RECTANGLE'
                    light_data.size = properties.get('size', 1.0)
                    # Set size_y properly for RECTANGLE and ELLIPSE
                    if light_data.shape in ['RECTANGLE', 'ELLIPSE']:
                        light_data.size_y = properties.get('size_y', light_data.size)
                    else:
                        light_data.size_y = light_data.size
                
                elif light_type == 'SPOT':
                    light_data.spot_size = math.radians(properties.get('spot_size', 45))
                    light_data.spot_blend = properties.get('spot_blend', 0.2)
                
                elif light_type == 'SUN':
                    light_data.angle = math.radians(properties.get('angle', 0.5))
                
                # Create object
                light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
                light_obj.location = world_pos
                
                # Point light at target
                direction = (target_pos - world_pos).normalized()
                light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
                
                # Add to preview collection
                self._preview_collection.objects.link(light_obj)
                self._preview_lights.append(light_obj)
                
                # Automatic camera light assignment for preview lights
                try:
                    from ...core.camera_manager import assign_light_to_active_camera
                    assign_light_to_active_camera(light_obj)
                except Exception:
                    pass
            
            return True
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create preview lights: {str(e)}")
            return False
    
    def update_preview_intensity(self, context):
        """Update intensity of all preview lights"""
        for light in self._preview_lights:
            if light.data and hasattr(light.data, 'energy'):
                # Get original intensity from template
                template = get_template(self.template_id)
                if template:
                    for light_template in template.get('lights', []):
                        if light_template.get('name', 'Light') in light.name:
                            base_intensity = light_template.get('properties', {}).get('intensity', 100)
                            light.data.energy = base_intensity * 0.5 * self._intensity_multiplier
                            break
    
    def update_preview_rotation(self, context):
        """Rotate entire lighting setup around subject"""
        if not context.selected_objects:
            return
        
        # Get subject center
        subject_center = sum((obj.location for obj in context.selected_objects), Vector()) / len(context.selected_objects)
        
        # Rotate each light around subject center
        for light in self._preview_lights:
            # Get original position relative to subject
            original_offset = light.location - subject_center
            
            # Apply rotation
            rotated_offset = original_offset.copy()
            rotated_offset.rotate(Matrix.Rotation(self._rotation_offset, 3, 'Z'))
            
            # Set new position
            light.location = subject_center + rotated_offset
            
            # Update light direction to still point at subject
            direction = (subject_center - light.location).normalized()
            light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    def recreate_preview_lights(self, context):
        """Recreate preview lights with new template"""
        self.cleanup_preview_lights()
        self._intensity_multiplier = 1.0
        self._rotation_offset = 0.0
        self.create_preview_lights(context)
    
    def cleanup_preview_lights(self):
        """Remove all preview lights"""
        for light in self._preview_lights:
            if light.data:
                bpy.data.lights.remove(light.data)
        self._preview_lights.clear()
    
    def cleanup_preview(self, context):
        """Remove all preview elements"""
        # Remove preview lights
        self.cleanup_preview_lights()
        
        # Remove preview collection
        if self._preview_collection and self._preview_collection.name in bpy.data.collections:
            bpy.data.collections.remove(self._preview_collection)
        
        # Restore original lights
        for light_data in self._original_lights:
            light_obj = light_data['object']
            if light_obj:
                light_obj.hide_viewport = not light_data['visible']
        
        self._preview_collection = None
        self._original_lights.clear()
    
    def confirm_and_apply(self, context):
        """Apply the current template and exit preview mode"""
        # # Coba eksekusi kode dengan error handling
        try:
            # Cleanup preview first
            self.cleanup_preview(context)
            
            # Apply the template using the existing operator
            bpy.ops.lumi.apply_lighting_template(
                template_id=self.template_id,
                intensity_multiplier=self._intensity_multiplier
            )
            
            self.report({'INFO'}, f"Applied template: {self.template_id}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply template: {str(e)}")
            return {'CANCELLED'}
    
    def cancel(self, context):
        """Cancel preview and restore original state"""
        self.cleanup_preview(context)
        self.report({'INFO'}, "Preview cancelled")
        return {'CANCELLED'}
    
    def _get_available_templates(self):
        """Get list of all available template IDs"""
        try:
            from .template_library import list_templates
            all_templates = list_templates()
            return [template['id'] for template in all_templates]
        except:
            return ['rembrandt', 'butterfly', 'split', 'loop']  # Fallback list
    
    def calculate_light_positions(self, template: Dict[str, Any], analysis: SubjectAnalysis, context: bpy.types.Context) -> List[Dict[str, Any]]:
        """Calculate world positions for template lights"""
        # Reuse the existing method from LUMI_OT_apply_lighting_template
        apply_op = LUMI_OT_apply_lighting_template()
        apply_op.template_id = self.template_id
        apply_op.auto_scale = True
        apply_op.intensity_multiplier = 1.0
        apply_op.use_camera_relative = True
        
        return apply_op.calculate_initial_light_positions(analysis, template, context)


class LUMI_OT_preview_lighting_template(bpy.types.Operator):
    """Preview lighting template without creating lights"""
    bl_idname = "lumi.preview_lighting_template"
    bl_label = "Preview Template"
    bl_description = "Preview lighting template positions"
    bl_options = {'REGISTER'}

    template_id: StringProperty(name="Template ID", default="portrait_rembrandt")

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and 
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def execute(self, context):
        try:
            # Get template info
            template = get_template(self.template_id)
            if not template:
                self.report({'ERROR'}, f"Template '{self.template_id}' not found")
                return {'CANCELLED'}

            light_count = len(template.get('lights', []))
            template_name = template.get('name', 'Unknown')
            category = template.get('category', 'unknown')

            self.report({'INFO'}, f"Template: {template_name} ({category}) - {light_count} lights")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Preview failed: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_save_custom_template(bpy.types.Operator):
    """Save current scene lighting as reusable template"""
    bl_idname = "lumi.save_custom_template"
    bl_label = "Save Custom Template"
    bl_description = "Save current scene lighting setup as a custom template"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties for template metadata
    template_name: StringProperty(
        name="Template Name",
        description="Name for the custom template",
        default="My Template",
        maxlen=64
    )
    
    template_category: EnumProperty(
        name="Category",
        description="Template category",
        items=[
            ('portrait', "Portrait", "Portrait lighting setup"),
            ('product', "Product", "Product photography lighting"),
            ('fashion', "Fashion", "Fashion photography lighting"),
            ('automotive', "Automotive", "Automotive photography lighting"),
            ('custom', "Custom", "Custom user-defined lighting")
        ],
        default='custom'
    )
    
    template_description: StringProperty(
        name="Description",
        description="Brief description of the template",
        default="",
        maxlen=256
    )
    
    include_world: BoolProperty(
        name="Include World Settings",
        description="Include world lighting settings in template",
        default=False
    )
    
    save_location: EnumProperty(
        name="Save Location",
        description="Where to save the template",
        items=[
            ('user', "User Presets", "Save to user preferences folder"),
            ('project', "Project Folder", "Save to current .blend file directory")
        ],
        default='user'
    )
    
    @classmethod
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                # # Periksa apakah objek adalah lampu
                any(obj.type == 'LIGHT' for obj in context.scene.objects))
    
    # # Method dipanggil saat operator dimulai
    def invoke(self, context, event):
        """Show popup dialog for template parameters"""
        # Set default template name based on scene
        if hasattr(context.scene, 'name') and context.scene.name:
            self.template_name = f"{context.scene.name}_lighting"
        
        # Show dialog
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    # # Method untuk menggambar UI
    def draw(self, context):
        """Draw the popup dialog"""
        layout = self.layout
        
        # Template info
        # # Buat kolom vertikal UI
        col = layout.column()
        col.label(text="Template Information:", icon='INFO')
        col.prop(self, "template_name")
        col.prop(self, "template_category")
        col.prop(self, "template_description")
        
        col.separator()
        
        # Options
        col.label(text="Options:", icon='PREFERENCES')
        col.prop(self, "include_world")
        col.prop(self, "save_location")
        
        # Info
        # # Periksa apakah objek adalah lampu
        lights_count = len([obj for obj in context.scene.objects if obj.type == 'LIGHT'])
        col.separator()
        col.label(text=f"Lights to save: {lights_count}", icon='LIGHT')
    
    # # Method utama eksekusi operator
    def execute(self, context):
        """Execute the template saving"""
        # # Coba eksekusi kode dengan error handling
        try:
            # 1. Validate template name
            if not self.template_name.strip():
                self.report({'ERROR'}, "Template name cannot be empty")
                # # Batalkan operasi
                return {'CANCELLED'}
            
            # 2. Get all lights in scene
            lights = self.get_scene_lights(context)
            if not lights:
                self.report({'ERROR'}, "No lights found in scene to save")
                # # Batalkan operasi
                return {'CANCELLED'}
            
            # 3. Convert to relative template format
            template_data = self.convert_to_template(lights, context)
            
            # 4. Add metadata
            import datetime
            template_data.update({
                "id": self.generate_template_id(),
                "name": self.template_name,
                "category": self.template_category,
                "description": self.template_description,
                "author": getattr(context.preferences.system, 'author', 'Unknown'),
                "date": datetime.datetime.now().isoformat(),
                "blender_version": bpy.app.version_string,
                "lumiflow_version": "1.0.0",  # TODO: Get from addon version
                "settings": {
                    "base_distance": 2.0,
                    "auto_scale": True,
                    "preserve_existing": False
                }
            })
            
            # 5. Include world settings if requested
            if self.include_world and context.scene.world:
                template_data["world"] = self.get_world_settings(context.scene.world)
            
            # 6. Save to file
            saved_path = self.save_template_to_file(template_data)
            
            self.report({'INFO'}, f"Template saved: {self.template_name} ({saved_path})")
            # # Selesaikan operasi dengan sukses
            return {'FINISHED'}
            
        # # Tangani error jika terjadi
        except Exception as e:
            self.report({'ERROR'}, f"Failed to save template: {str(e)}")
            # # Batalkan operasi
            return {'CANCELLED'}
    
    def get_scene_lights(self, context):
        """Get all lights in LumiFlow collection and scene"""
        lights = []
        
        # Get lights from LumiFlow collection
        from ...utils.common import lumi_get_light_collection
        collection = lumi_get_light_collection(context.scene)
        
        if collection:
            for obj in collection.objects:
                # # Periksa apakah objek adalah lampu
                if obj.type == 'LIGHT':
                    lights.append(obj)
        else:
            # Fallback: get all lights in scene
            for obj in context.scene.objects:
                # # Periksa apakah objek adalah lampu
                if obj.type == 'LIGHT':
                    lights.append(obj)
        
        return lights
    
    def convert_to_template(self, lights, context):
        """Convert absolute light positions to relative template format"""
        # Calculate subject center for relative positioning
        subject_center = Vector((0, 0, 0))
        # # Ambil objek yang dipilih dalam scene
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if selected_objects:
            # Use selected objects as subject reference
            total_pos = sum((obj.location for obj in selected_objects), Vector())
            subject_center = total_pos / len(selected_objects)
        
        # Calculate reference distance (largest dimension of all lights)
        all_positions = [light.location for light in lights]
        if all_positions:
            min_pos = Vector((min(pos.x for pos in all_positions),
                            min(pos.y for pos in all_positions),
                            min(pos.z for pos in all_positions)))
            max_pos = Vector((max(pos.x for pos in all_positions),
                            max(pos.y for pos in all_positions),
                            max(pos.z for pos in all_positions)))
            reference_distance = (max_pos - min_pos).length / 2
        else:
            reference_distance = 2.0
        
        # Convert each light to template format
        template_lights = []
        for light in lights:
            # Calculate relative position
            relative_pos = light.location - subject_center
            distance = relative_pos.length
            
            # Convert to spherical coordinates
            import math
            if distance > 0.001:  # Avoid division by zero
                azimuth = math.degrees(math.atan2(relative_pos.y, relative_pos.x))
                elevation = math.degrees(math.asin(relative_pos.z / distance))
            else:
                azimuth = 0
                elevation = 0
            
            # Get light properties
            light_data = {
                "name": light.name,
                "type": light.data.type,
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": azimuth,
                        "elevation": elevation,
                        "distance": distance / reference_distance if reference_distance > 0 else 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": tuple(light.rotation_euler)
                },
                "properties": {
                    "intensity": getattr(light.data, 'energy', 100),
                    "color": tuple(getattr(light.data, 'color', (1, 1, 1))),
                    "size": getattr(light.data, 'size', 1.0) if hasattr(light.data, 'size') else 1.0
                }
            }
            
            # Add type-specific properties
            if light.data.type == 'AREA':
                light_data["properties"]["shape"] = light.data.shape
                if hasattr(light.data, 'size_y'):
                    light_data["properties"]["size_y"] = light.data.size_y
            elif light.data.type == 'SPOT':
                light_data["properties"]["spot_size"] = math.degrees(light.data.spot_size)
                light_data["properties"]["spot_blend"] = light.data.spot_blend
            elif light.data.type == 'SUN':
                light_data["properties"]["angle"] = math.degrees(light.data.angle)
            
            template_lights.append(light_data)
        
        return {
            "lights": template_lights,
            "reference_distance": reference_distance,
            "subject_center": tuple(subject_center)
        }
    
    def get_world_settings(self, world):
        """Extract world lighting settings"""
        world_data = {
            "strength": 1.0,
            "color": (1, 1, 1)
        }
        
        if world.use_nodes and world.node_tree:
            # Find world output and background shader
            for node in world.node_tree.nodes:
                if node.type == 'BACKGROUND':
                    world_data["strength"] = node.inputs['Strength'].default_value
                    color_input = node.inputs['Color'].default_value
                    world_data["color"] = tuple(color_input[:3])
                    break
        
        return world_data
    
    def generate_template_id(self):
        """Generate unique template ID"""
        import re
        import time
        
        # Clean template name for ID
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', self.template_name.lower())
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        
        # Add timestamp for uniqueness
        timestamp = str(int(time.time()))[-6:]  # Last 6 digits
        
        return f"{self.template_category}_{clean_name}_{timestamp}"
    
    def save_template_to_file(self, template_data):
        """Save template as JSON file"""
        import json
        import os
        
        # Determine save path
        if self.save_location == 'user':
            # User presets folder
            import bpy.utils
            presets_path = bpy.utils.user_resource('SCRIPTS', path="presets")
            save_dir = os.path.join(presets_path, "lumiflow_templates")
        else:
            # Project folder
            if bpy.data.filepath:
                blend_dir = os.path.dirname(bpy.data.filepath)
                save_dir = os.path.join(blend_dir, "lumiflow_templates")
            else:
                # Fallback to temp directory
                import tempfile
                save_dir = os.path.join(tempfile.gettempdir(), "lumiflow_templates")
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', self.template_name)
        filename = f"{safe_name}.json"
        filepath = os.path.join(save_dir, filename)
        
        # Handle existing files
        counter = 1
        base_filepath = filepath
        while os.path.exists(filepath):
            name_part, ext = os.path.splitext(base_filepath)
            filepath = f"{name_part}_{counter}{ext}"
            counter += 1
        
        # Save JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def load_custom_templates():
        """Load all custom templates from user folders"""
        import json
        import os
        import bpy.utils
        
        templates = []
        
        # Check user presets folder
        presets_path = bpy.utils.user_resource('SCRIPTS', path="presets")
        if presets_path:
            templates_dir = os.path.join(presets_path, "lumiflow_templates")
            if os.path.exists(templates_dir):
                templates.extend(LUMI_OT_save_custom_template._load_templates_from_dir(templates_dir))
        
        # Check project folder if blend file is saved
        if bpy.data.filepath:
            blend_dir = os.path.dirname(bpy.data.filepath)
            project_templates_dir = os.path.join(blend_dir, "lumiflow_templates")
            if os.path.exists(project_templates_dir):
                templates.extend(LUMI_OT_save_custom_template._load_templates_from_dir(project_templates_dir))
        
        return templates
    
    @staticmethod
    def _load_templates_from_dir(directory):
        """Load templates from a specific directory"""
        import json
        import os
        
        templates = []
        
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)
                            template_data['_filepath'] = filepath  # Store file path for management
                            templates.append(template_data)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Failed to load template {filepath}: {e}")
        except OSError:
            pass
        
        return templates


class LUMI_OT_manage_custom_templates(bpy.types.Operator):
    """Manage custom templates (delete, export, etc.)"""
    bl_idname = "lumi.manage_custom_templates"
    bl_label = "Manage Custom Templates"
    bl_description = "Manage custom lighting templates"
    bl_options = {'REGISTER'}
    
    action: EnumProperty(
        name="Action",
        description="Action to perform",
        items=[
            ('list', "List", "List all custom templates"),
            ('delete', "Delete", "Delete a template"),
            ('export', "Export", "Export template to file"),
            ('import', "Import", "Import template from file")
        ],
        default='list'
    )
    
    template_to_delete: StringProperty(
        name="Template to Delete",
        description="Path to template file to delete"
    )
    
    # # Method utama eksekusi operator
    def execute(self, context):
        """Execute template management action"""
        # # Coba eksekusi kode dengan error handling
        try:
            if self.action == 'list':
                templates = LUMI_OT_save_custom_template.load_custom_templates()
                if templates:
                    template_names = [t.get('name', 'Unknown') for t in templates]
                    self.report({'INFO'}, f"Found {len(templates)} custom templates: {', '.join(template_names)}")
                else:
                    self.report({'INFO'}, "No custom templates found")
                    
            elif self.action == 'delete' and self.template_to_delete:
                if self.delete_template(self.template_to_delete):
                    self.report({'INFO'}, f"Template deleted: {self.template_to_delete}")
                else:
                    self.report({'ERROR'}, f"Failed to delete template: {self.template_to_delete}")
                    
            # # Selesaikan operasi dengan sukses
            return {'FINISHED'}
            
        # # Tangani error jika terjadi
        except Exception as e:
            self.report({'ERROR'}, f"Management action failed: {str(e)}")
            # # Batalkan operasi
            return {'CANCELLED'}
    
    def delete_template(self, filepath):
        """Delete a template file"""
        import os
        # # Coba eksekusi kode dengan error handling
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        # # Tangani error jika terjadi
        except OSError:
            pass
        return False


class LUMI_OT_save_lighting_template(bpy.types.Operator):
    """Save current lighting setup as template"""
    bl_idname = "lumi.save_lighting_template"
    bl_label = "Save Template"
    bl_description = "Save current lighting setup as custom template"
    bl_options = {'REGISTER', 'UNDO'}

    template_name: StringProperty(
        name="Template Name",
        description="Name for the new template",
        default="Custom Template"
    )

    template_id: StringProperty(
        name="Template ID", 
        description="Unique identifier for template",
        default="custom_template"
    )

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                any(obj.type == 'LIGHT' for obj in context.scene.objects))

    def execute(self, context):
        try:
            # TODO: Implement template saving functionality
            # This would analyze current lights and create template data
            self.report({'INFO'}, f"Template saving not yet implemented")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Save failed: {str(e)}")
            return {'CANCELLED'}


# Registration classes
CLASSES = [
    LUMI_OT_apply_lighting_template,
    LUMI_OT_preview_template,
    LUMI_OT_preview_lighting_template,
    LUMI_OT_save_custom_template,
    LUMI_OT_manage_custom_templates,
    LUMI_OT_save_lighting_template,
]


# # Fungsi untuk mendaftarkan class ke Blender
def register():
    """Register all operators"""
    for cls in CLASSES:
        # # Daftarkan class ke sistem Blender
        bpy.utils.register_class(cls)


# # Fungsi untuk membatalkan pendaftaran class
def unregister():
    """Unregister all operators"""
    for cls in reversed(CLASSES):
        # # Batalkan pendaftaran class
        bpy.utils.unregister_class(cls)


# Export classes for registration
__all__ = [
    'LUMI_OT_apply_lighting_template',
    'LUMI_OT_preview_template',
    'LUMI_OT_preview_lighting_template',
    'LUMI_OT_save_custom_template',
    'LUMI_OT_manage_custom_templates', 
    'LUMI_OT_save_lighting_template'
]
