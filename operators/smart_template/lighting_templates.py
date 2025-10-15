"""
LumiFlow Lighting Templates Operator - Refactored
Orchestration only, delegates to core + utils.
"""

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from mathutils import Vector
from typing import List, Dict, Any

from ...utils.common import (
    lumi_is_addon_enabled, lumi_get_light_collection, lumi_move_to_collection
)
from ...utils.light import lumi_set_light_pivot
from ...utils.scene_context import SceneAnalyzer, SceneContext
from ...utils.positioning import (
    calculate_position_from_template, calculate_optimal_distance
)
from ...utils.material_adaptation import (
    generate_lighting_recommendations, apply_material_adjustments_to_light
)
from ...utils.obstruction_detector import get_enhanced_detector
from ...core.template_system import TemplateSystem, ValidationResult
from .template_library import get_template


class LUMI_OT_apply_lighting_template(bpy.types.Operator):
    """Apply photographic lighting template to selected objects"""
    bl_idname = "lumi.apply_lighting_template"
    bl_label = "Apply Lighting Template"
    bl_options = {'REGISTER', 'UNDO'}

    # === PROPERTIES (unchanged) ===
    template_id: StringProperty(name="Template ID", default="")
    auto_scale: BoolProperty(name="Auto Scale", default=True)
    manual_distance: FloatProperty(name="Manual Distance", default=0.0, min=0.0)
    use_camera_relative: BoolProperty(name="Camera Relative", default=False)
    enable_obstruction_detection: BoolProperty(name="Obstruction Detection", default=True)
    obstruction_fallback_strategy: EnumProperty(
        name="Fallback Strategy",
        items=[
            ('SKIP_LIGHT', "Skip Light", "Skip lights with obstructions"),
            ('ADJUST_POSITION', "Adjust Position", "Find clear position"),
            ('WARN_ONLY', "Warn Only", "Create anyway with warning"),
        ],
        default='ADJUST_POSITION'
    )
    show_obstruction_warnings: BoolProperty(name="Show Warnings", default=True)
    use_material_adaptation: BoolProperty(name="Material Adaptation", default=True)
    intensity_multiplier: FloatProperty(name="Intensity Multiplier", default=1.0, min=0.1)
    size_multiplier: FloatProperty(name="Size Multiplier", default=1.0, min=0.1)
    preserve_existing: BoolProperty(name="Preserve Existing", default=False)

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def invoke(self, context, event):
        """Invoke operator with dialog when called from UI"""
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        """Draw operator properties in dialog"""
        layout = self.layout
        
        # Template selection (display template name if set)
        layout.label(text="Template Settings:", icon='LIGHT')
        if self.template_id:
            # Get template info to display name
            try:
                template = get_template(self.template_id)
                if template:
                    template_name = template.get('name', self.template_id)
                    layout.label(text=f"Template: {template_name}")
            except:
                layout.label(text=f"Template: {self.template_id}")
        
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
        layout.prop(self, "use_material_adaptation")
        
        layout.separator()
        
        # Obstruction detection
        layout.label(text="Obstruction Detection:", icon='MODIFIER')
        layout.prop(self, "enable_obstruction_detection")
        
        if self.enable_obstruction_detection:
            layout.prop(self, "obstruction_fallback_strategy")
            layout.prop(self, "show_obstruction_warnings")

    def execute(self, context):
        """Main execution - orchestration only."""
        try:
            # === 1. VALIDATE ===
            template_system = TemplateSystem()

            # Validate template
            template_validation = template_system.validate_template(self.template_id)
            if not template_validation.valid:
                for error in template_validation.errors:
                    self.report({'ERROR'}, error)
                return {'CANCELLED'}

            # Validate scene
            scene_validation = template_system.validate_scene(context, context.selected_objects)
            if not scene_validation.valid:
                for error in scene_validation.errors:
                    self.report({'ERROR'}, error)
                return {'CANCELLED'}

            for warning in scene_validation.warnings:
                self.report({'WARNING'}, warning)

            template = template_system.current_template

            # === 2. ANALYZE SCENE ===
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(
                context.selected_objects,
                include_camera=True,
                include_classification=self.enable_obstruction_detection,
                include_materials=self.use_material_adaptation
            )

            # === 3. CLEAR EXISTING LIGHTS (if requested) ===
            if not self.preserve_existing:
                self._clear_existing_lights(context)

            # === 4. CALCULATE POSITIONS ===
            positions = self._calculate_light_positions(scene_ctx, template, context)

            # === 5. HANDLE OBSTRUCTIONS ===
            if self.enable_obstruction_detection and scene_ctx.classifications:
                positions = self._adjust_for_obstructions(positions, scene_ctx, context)

            # === 5. CREATE LIGHTS ===
            lights = self._create_lights(positions, template, context)

            if not lights:
                self.report({'WARNING'}, "No lights created")
                return {'CANCELLED'}

            # === 6. MATERIAL ADAPTATIONS ===
            if self.use_material_adaptation and scene_ctx.materials:
                recommendations = generate_lighting_recommendations(scene_ctx.materials)
                for light in lights:
                    apply_material_adjustments_to_light(light, recommendations)

            # === 7. ORGANIZE ===
            self._organize_lights(lights, context)

            # === 8. SELECT ===
            self._select_lights(lights, context)

            self.report({'INFO'}, f"Applied '{self.template_id}': {len(lights)} lights created")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply template: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def _calculate_light_positions(self, scene_ctx: SceneContext,
                                   template: Dict, context) -> List[Dict]:
        """Calculate initial light positions (no obstruction)."""
        positions = []

        # Calculate base distance
        if self.manual_distance > 0:
            base_distance = self.manual_distance
        else:
            template_distance = template.get('settings', {}).get('base_distance', 2.0)
            base_distance = calculate_optimal_distance(
                scene_ctx.bounds, template_distance, self.auto_scale
            )

        # Get camera matrix if needed
        camera_matrix = None
        if self.use_camera_relative and scene_ctx.camera:
            camera_matrix = scene_ctx.camera.matrix

        # Calculate each light position
        for light_template in template.get('lights', []):
            try:
                position = calculate_position_from_template(
                    light_template,
                    scene_ctx.bounds.center,
                    base_distance,
                    camera_matrix=camera_matrix,
                    use_camera_relative=self.use_camera_relative
                )

                positions.append({
                    'light_template': light_template,
                    'position': position,
                    'target': scene_ctx.bounds.center
                })
            except Exception as e:
                self.report({'WARNING'}, f"Failed to calculate position: {e}")
                continue

        return positions

    def _adjust_for_obstructions(self, positions: List[Dict],
                                 scene_ctx: SceneContext, context) -> List[Dict]:
        """Adjust positions for obstructions."""
        from ...utils.operators import lumi_ray_cast_between_points

        adjusted_positions = []
        background_objects = scene_ctx.get_background_objects()

        for pos_data in positions:
            has_obstruction, hit_location = self._check_obstruction(
                pos_data['position'], pos_data['target'],
                background_objects, context
            )

            if has_obstruction:
                if self.obstruction_fallback_strategy == 'SKIP_LIGHT':
                    if self.show_obstruction_warnings:
                        name = pos_data['light_template'].get('name', 'Light')
                        self.report({'WARNING'}, f"{name}: Skipped due to obstruction")
                    continue
                elif self.obstruction_fallback_strategy == 'ADJUST_POSITION':
                    # Find clear position
                    clear_pos = self._find_clear_position(
                        pos_data['position'], pos_data['target'],
                        background_objects, context
                    )
                    if clear_pos:
                        pos_data['position'] = clear_pos
                    else:
                        continue
                # WARN_ONLY: continue with warning
                elif self.show_obstruction_warnings:
                    name = pos_data['light_template'].get('name', 'Light')
                    self.report({'WARNING'}, f"{name}: Has obstruction")

            adjusted_positions.append(pos_data)

        # Update pivots for adjusted positions
        for pos_data in adjusted_positions:
            if 'light_obj' in pos_data:
                # Position was adjusted, update pivot to target
                lumi_set_light_pivot(pos_data['light_obj'], pos_data['target'])

        return adjusted_positions

    def _check_obstruction(self, from_pos: Vector, to_pos: Vector,
                           obstacles: List, context) -> tuple:
        """Check for obstruction using raycast."""
        from ...utils.operators import lumi_ray_cast_between_points

        hit, hit_obj, hit_location, distance = lumi_ray_cast_between_points(
            context, from_pos, to_pos
        )

        if hit and hit_obj in obstacles:
            return (True, hit_location)
        return (False, None)

    def _find_clear_position(self, original: Vector, target: Vector,
                            obstacles: List, context, max_attempts=10) -> Vector:
        """Find clear position near original."""
        import random

        direction = (original - target).normalized()
        distance = (original - target).length

        for i in range(max_attempts):
            # Try positions around original
            offset = Vector((
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-0.5, 1)
            )).normalized() * (distance * 0.2)

            test_pos = original + offset
            has_obstruction, _ = self._check_obstruction(test_pos, target, obstacles, context)

            if not has_obstruction:
                return test_pos

        return None

    def _create_lights(self, positions: List[Dict], template: Dict, context) -> List:
        """Create light objects from positions."""
        lights = []

        for pos_data in positions:
            try:
                light = self._create_single_light(pos_data, context)
                if light:
                    lights.append(light)
            except Exception as e:
                self.report({'WARNING'}, f"Failed to create light: {e}")
                continue

        return lights

    def _create_single_light(self, pos_data: Dict, context) -> bpy.types.Object:
        """Create single light object."""
        light_template = pos_data['light_template']

        # Create light data
        light_type = light_template.get('type', 'AREA')
        base_name = light_template.get('name', 'Light')
        
        # Add prefix based on assignment mode
        assignment_mode = getattr(context.scene, 'lumi_light_assignment_mode', 'SCENE')
        if assignment_mode == 'SCENE':
            light_name = f"G_{base_name}"
        else:  # CAMERA mode
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
                    import re
                    match = re.search(r'\d+', camera_name)
                    camera_num = match.group(0).zfill(2) if match else '00'
                    camera_prefix = f'C_{camera_num}'
                light_name = f"{camera_prefix}_{base_name}"
            else:
                light_name = f"C_00_{base_name}"
        
        light_data = bpy.data.lights.new(light_name, light_type)

        # Set properties
        power = light_template.get('power', 100.0) * self.intensity_multiplier
        light_data.energy = power
        light_data.color = light_template.get('color', (1.0, 1.0, 1.0))

        if light_type == 'AREA':
            size = light_template.get('size', 1.0) * self.size_multiplier
            light_data.size = size
            light_data.shape = light_template.get('shape', 'SQUARE')
        elif light_type == 'SPOT':
            light_data.spot_size = light_template.get('spot_size', 0.785398)  # 45 deg
            light_data.spot_blend = light_template.get('spot_blend', 0.15)

        # Create object
        light_obj = bpy.data.objects.new(light_name, light_data)
        light_obj.location = pos_data['position']

        # Orient to target
        direction = (pos_data['target'] - pos_data['position']).normalized()
        light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

        # Set pivot based on rotation method
        rotation_config = light_template.get('rotation', {})
        rotation_method = rotation_config.get('method', 'target')  # Default to target

        if rotation_method == 'euler':
            # Euler rotation: Set pivot 3 meters in front of light in facing direction
            pivot_position = pos_data['position'] + direction * 3.0
            lumi_set_light_pivot(light_obj, pivot_position)
        else:
            # Target rotation: Set pivot to target center
            lumi_set_light_pivot(light_obj, pos_data['target'])

        # Link to scene
        context.scene.collection.objects.link(light_obj)

        return light_obj

    def _organize_lights(self, lights: List, context):
        """Organize lights into collection."""
        collection = lumi_get_light_collection(context.scene)
        if collection:
            for light in lights:
                if light.name not in collection.objects:
                    lumi_move_to_collection(light, collection)

    def _select_lights(self, lights: List, context):
        """Select created lights."""
        bpy.ops.object.select_all(action='DESELECT')
        for light in lights:
            light.select_set(True)
        if lights:
            context.view_layer.objects.active = lights[0]

    def _clear_existing_lights(self, context):
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
                return False

            # Analyze subject
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(context.selected_objects)

            # Calculate positions
            positions = self._calculate_light_positions(scene_ctx, template, context)

            # Create preview lights
            for position_data in positions:
                light_template = position_data['light_template']
                world_pos = position_data['position']
                target_pos = position_data['target']

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

    def _calculate_light_positions(self, scene_ctx, template, context):
        """Calculate light positions using new scene context"""
        positions = []

        # Calculate base distance
        if template.get('settings', {}).get('base_distance'):
            base_distance = template['settings']['base_distance']
        else:
            base_distance = calculate_optimal_distance(scene_ctx.bounds, 2.0, True)

        # Get camera matrix if needed
        camera_matrix = None
        if scene_ctx.camera:
            camera_matrix = scene_ctx.camera.matrix

        # Calculate each light position
        for light_template in template.get('lights', []):
            try:
                position = calculate_position_from_template(
                    light_template,
                    scene_ctx.bounds.center,
                    base_distance,
                    camera_matrix=camera_matrix,
                    use_camera_relative=False
                )

                positions.append({
                    'light_template': light_template,
                    'position': position,
                    'target': scene_ctx.bounds.center
                })
            except Exception as e:
                continue

        return positions


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
                return {'CANCELLED'}

            light_count = len(template.get('lights', []))
            template_name = template.get('name', 'Unknown')
            category = template.get('category', 'unknown')

            self.report({'INFO'}, f"Template: {template_name} ({category}) - {light_count} lights")
            return {'FINISHED'}

        except Exception as e:
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
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                any(obj.type == 'LIGHT' for obj in context.scene.objects))

    def invoke(self, context, event):
        """Show popup dialog for template parameters"""
        # Set default template name based on scene
        if hasattr(context.scene, 'name') and context.scene.name:
            self.template_name = f"{context.scene.name}_lighting"

        # Show dialog
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        """Draw the popup dialog"""
        layout = self.layout

        # Template info
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
        lights_count = len([obj for obj in context.scene.objects if obj.type == 'LIGHT'])
        col.separator()
        col.label(text=f"Lights to save: {lights_count}", icon='LIGHT')

    def execute(self, context):
        """Execute the template saving"""
        try:
            # 1. Validate template name
            if not self.template_name.strip():
                self.report({'ERROR'}, "Template name cannot be empty")
                return {'CANCELLED'}

            # 2. Get all lights in scene
            lights = self.get_scene_lights(context)
            if not lights:
                self.report({'ERROR'}, "No lights found in scene to save")
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
                "lumiflow_version": "1.0.0",
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
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}

    def get_scene_lights(self, context):
        """Get all lights in LumiFlow collection and scene"""
        lights = []

        # Get lights from LumiFlow collection
        collection = lumi_get_light_collection(context.scene)

        if collection:
            for obj in collection.objects:
                if obj.type == 'LIGHT':
                    lights.append(obj)
        else:
            # Fallback: get all lights in scene
            for obj in context.scene.objects:
                if obj.type == 'LIGHT':
                    lights.append(obj)

        return lights

    def convert_to_template(self, lights, context):
        """Convert absolute light positions to relative template format"""
        # Calculate subject center for relative positioning
        subject_center = Vector((0, 0, 0))
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
                        pass
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

    def execute(self, context):
        """Execute template management action"""
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

            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}

    def delete_template(self, filepath):
        """Delete a template file"""
        import os
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
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
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(LUMI_OT_apply_lighting_template)
    bpy.utils.register_class(LUMI_OT_preview_template)
    bpy.utils.register_class(LUMI_OT_preview_lighting_template)
    bpy.utils.register_class(LUMI_OT_save_custom_template)
    bpy.utils.register_class(LUMI_OT_manage_custom_templates)
    bpy.utils.register_class(LUMI_OT_save_lighting_template)


def unregister():
    bpy.utils.unregister_class(LUMI_OT_apply_lighting_template)
    bpy.utils.unregister_class(LUMI_OT_preview_template)
    bpy.utils.unregister_class(LUMI_OT_preview_lighting_template)
    bpy.utils.unregister_class(LUMI_OT_save_custom_template)
    bpy.utils.unregister_class(LUMI_OT_manage_custom_templates)
    bpy.utils.unregister_class(LUMI_OT_save_lighting_template)