# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Smart Light Addition Operator

Uses NeededLightRecommender to intelligently suggest and add
the next light based on current scene composition.
"""

import bpy
from bpy.props import BoolProperty, EnumProperty
from mathutils import Vector
from typing import Optional, List, Dict, Any

from ..utils.common import lumi_is_addon_enabled, lumi_get_light_collection, lumi_move_to_collection
from ..utils.light import lumi_set_light_pivot
from ..utils.scene_context import SceneAnalyzer
from ..utils.scene_context.light_role_analyzer import (
    LightRoleAnalyzer, LightRole, LightRoleResult
)
from ..utils.scene_context.composition_analyzer import (
    CompositionAnalyzer, CompositionAnalysisResult, LightingStyle
)
from ..utils.scene_context.needed_light_recommender import (
    NeededLightRecommender, LightRecommendation, RecommendationPriority
)
from ..utils.scene_context.product_category_detector import (
    ProductCategoryDetector, ProductCategoryResult
)
from ..utils.color import lumi_kelvin_to_rgb


class LUMI_OT_smart_add_light(bpy.types.Operator):
    """Intelligently add the next recommended light based on scene composition"""
    bl_idname = "lumiflow.smart_add_light"
    bl_label = "Smart Add Light"
    bl_description = "Add the next recommended light based on current lighting composition"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    auto_apply: BoolProperty(
        name="Auto Apply",
        description="Automatically add the recommended light without confirmation",
        default=True,
    )
    
    show_alternatives: BoolProperty(
        name="Show Alternatives",
        description="Show alternative light recommendations",
        default=False,
    )
    
    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)
    
    def execute(self, context):
        try:
            # Get target objects (products)
            target_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            
            if not target_objects:
                self.report({'WARNING'}, "No mesh objects selected")
                return {'CANCELLED'}
            
            # === 1. ANALYZE SCENE ===
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(
                target_objects,
                include_camera=True,
                include_materials=True
            )
            
            # === 2. DETECT PRODUCT CATEGORY ===
            category_result = None
            try:
                detector = ProductCategoryDetector()
                category_result = detector.detect(
                    target_objects,
                    scene_ctx.materials,
                    scene_ctx.bounds
                )
            except Exception as e:
                print(f"Category detection failed: {e}")
            
            # === 3. ANALYZE CURRENT LIGHT ROLES ===
            camera = context.scene.camera
            if not camera:
                self.report({'WARNING'}, "No active camera - using default parameters")
            
            light_roles = []
            if camera:
                try:
                    role_analyzer = LightRoleAnalyzer(context)
                    camera_data = type('CameraData', (), {
                        'location': camera.location,
                        'matrix': camera.matrix_world,
                    })()
                    
                    # Get all lights in scene
                    scene_lights = [obj for obj in context.scene.objects 
                                   if obj.type == 'LIGHT' and obj.visible_get()]
                    
                    for light in scene_lights:
                        role_result = role_analyzer.analyze_single_light(
                            light, camera_data, scene_ctx.bounds.center
                        )
                        if role_result:
                            light_roles.append(role_result)
                except Exception as e:
                    print(f"Role analysis failed: {e}")
            
            # === 4. ANALYZE COMPOSITION ===
            composition = None
            if light_roles:
                try:
                    comp_analyzer = CompositionAnalyzer()
                    composition = comp_analyzer.analyze(light_roles)
                except Exception as e:
                    print(f"Composition analysis failed: {e}")
            
            # === 5. GET RECOMMENDATION ===
            recommender = NeededLightRecommender()
            recommendation = recommender.recommend(composition, category_result)
            
            if not recommendation:
                self.report({'INFO'}, "No additional lights needed - composition is complete")
                return {'FINISHED'}
            
            # === 6. REPORT RECOMMENDATION ===
            role_name = recommendation.role.value if recommendation.role else "UNKNOWN"
            priority_name = recommendation.priority.value if recommendation.priority else "MEDIUM"
            
            self.report({'INFO'}, 
                f"Recommended: {role_name} light ({priority_name} priority) - {recommendation.reason}")
            
            # === 7. CREATE THE LIGHT ===
            if self.auto_apply:
                light = self._create_recommended_light(
                    context, recommendation, scene_ctx, category_result
                )
                
                if light:
                    self.report({'INFO'}, 
                        f"Added {role_name} light: {light.name}")
                    return {'FINISHED'}
                else:
                    self.report({'WARNING'}, "Failed to create recommended light")
                    return {'CANCELLED'}
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Smart add light failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def _create_recommended_light(
        self, 
        context, 
        recommendation: LightRecommendation,
        scene_ctx,
        category_result: Optional[ProductCategoryResult]
    ) -> Optional[bpy.types.Object]:
        """Create the recommended light."""
        
        try:
            # Determine light type based on role
            light_type = self._get_light_type_for_role(recommendation.role)
            
            # Create light data
            light_data = bpy.data.lights.new(
                name=f"Lumi_{recommendation.role.value}",
                type=light_type
            )
            
            # Apply recommended properties
            params = recommendation.suggested_params or {}
            
            # Energy
            energy = params.get('energy', 200)
            light_data.energy = energy
            
            # Color temperature
            color_temp = params.get('color_temp', 5500)
            if category_result and category_result.recommended_color_temp:
                color_temp = category_result.recommended_color_temp
            light_data.color = lumi_kelvin_to_rgb(color_temp)
            
            # Size for area lights
            if light_type == 'AREA':
                light_data.size = params.get('size', 1.0)
                light_data.shape = 'SQUARE'
            elif light_type == 'SPOT':
                light_data.spot_size = params.get('spot_size', 0.785)  # 45 degrees
                light_data.spot_blend = params.get('spot_blend', 0.15)
            
            # Create light object
            light_obj = bpy.data.objects.new(light_data.name, light_data)
            context.collection.objects.link(light_obj)
            
            # Calculate position
            position = self._calculate_light_position(
                recommendation, scene_ctx, context
            )
            light_obj.location = position
            
            # Orient toward subject
            direction = (scene_ctx.bounds.center - position).normalized()
            if direction.length > 0.001:
                rot_quat = direction.to_track_quat('-Z', 'Y')
                light_obj.rotation_euler = rot_quat.to_euler()
            
            # Set pivot
            lumi_set_light_pivot(light_obj, scene_ctx.bounds.center)
            
            # Move to LumiFlow collection
            light_collection = lumi_get_light_collection(context)
            if light_collection:
                lumi_move_to_collection(light_obj, light_collection)
            
            # Select the new light
            bpy.ops.object.select_all(action='DESELECT')
            light_obj.select_set(True)
            context.view_layer.objects.active = light_obj
            
            return light_obj
            
        except Exception as e:
            print(f"Error creating light: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_light_type_for_role(self, role: LightRole) -> str:
        """Get appropriate Blender light type for role."""
        role_to_type = {
            LightRole.KEY: 'AREA',
            LightRole.FILL: 'AREA',
            LightRole.BACK: 'AREA',
            LightRole.RIM: 'SPOT',
            LightRole.ACCENT: 'SPOT',
            LightRole.AMBIENT: 'AREA',
            LightRole.UNKNOWN: 'AREA',
        }
        return role_to_type.get(role, 'AREA')
    
    def _calculate_light_position(
        self,
        recommendation: LightRecommendation,
        scene_ctx,
        context
    ) -> Vector:
        """Calculate optimal position for recommended light."""
        
        center = scene_ctx.bounds.center
        radius = scene_ctx.bounds.radius * 2.0  # Distance based on subject size
        
        # Get suggested position from recommendation
        suggested_pos = recommendation.suggested_position
        
        if suggested_pos:
            azimuth = suggested_pos.get('azimuth', 45)
            elevation = suggested_pos.get('elevation', 45)
            distance_mult = suggested_pos.get('distance', 1.0)
        else:
            # Default positions based on role
            role_defaults = {
                LightRole.KEY: {'azimuth': 45, 'elevation': 45, 'distance': 1.0},
                LightRole.FILL: {'azimuth': -45, 'elevation': 30, 'distance': 1.2},
                LightRole.BACK: {'azimuth': 180, 'elevation': 30, 'distance': 1.0},
                LightRole.RIM: {'azimuth': 135, 'elevation': 60, 'distance': 1.0},
                LightRole.ACCENT: {'azimuth': 90, 'elevation': 20, 'distance': 1.5},
            }
            defaults = role_defaults.get(recommendation.role, 
                                        {'azimuth': 45, 'elevation': 45, 'distance': 1.0})
            azimuth = defaults['azimuth']
            elevation = defaults['elevation']
            distance_mult = defaults['distance']
        
        # Convert spherical to cartesian
        import math
        azimuth_rad = math.radians(azimuth)
        elevation_rad = math.radians(elevation)
        distance = radius * distance_mult
        
        # Calculate position
        x = center.x + distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
        y = center.y - distance * math.cos(elevation_rad) * math.cos(azimuth_rad)
        z = center.z + distance * math.sin(elevation_rad)
        
        # Adjust for camera if available
        camera = context.scene.camera
        if camera:
            # Rotate position to be camera-relative
            camera_forward = camera.matrix_world.to_3x3() @ Vector((0, 0, -1))
            camera_forward.z = 0
            if camera_forward.length > 0.001:
                camera_forward.normalize()
                # Apply camera-relative rotation here if needed
        
        return Vector((x, y, z))


class LUMI_OT_analyze_composition(bpy.types.Operator):
    """Analyze current lighting composition and show recommendations"""
    bl_idname = "lumiflow.analyze_composition"
    bl_label = "Analyze Lighting Composition"
    bl_description = "Analyze the current lighting setup and show composition info"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT')
    
    def execute(self, context):
        try:
            # Get target objects
            target_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            if not target_objects:
                target_objects = [obj for obj in context.scene.objects 
                                if obj.type == 'MESH' and obj.visible_get()]
            
            if not target_objects:
                self.report({'WARNING'}, "No mesh objects found")
                return {'CANCELLED'}
            
            # Analyze scene
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(target_objects, include_camera=True)
            
            # Get camera
            camera = context.scene.camera
            if not camera:
                self.report({'WARNING'}, "No active camera")
                return {'CANCELLED'}
            
            # Analyze light roles
            role_analyzer = LightRoleAnalyzer(context)
            camera_data = type('CameraData', (), {
                'location': camera.location,
                'matrix': camera.matrix_world,
            })()
            
            scene_lights = [obj for obj in context.scene.objects 
                          if obj.type == 'LIGHT' and obj.visible_get()]
            
            light_roles = []
            for light in scene_lights:
                role_result = role_analyzer.analyze_single_light(
                    light, camera_data, scene_ctx.bounds.center
                )
                if role_result:
                    light_roles.append(role_result)
            
            # Analyze composition
            if not light_roles:
                self.report({'INFO'}, "No lights found in scene")
                return {'FINISHED'}
            
            comp_analyzer = CompositionAnalyzer()
            composition = comp_analyzer.analyze(light_roles)
            
            # Report results
            self.report({'INFO'}, f"═══ Composition Analysis ═══")
            self.report({'INFO'}, f"Style: {composition.style.value}")
            self.report({'INFO'}, f"Quality: {composition.quality.value} ({composition.quality_score:.0%})")
            self.report({'INFO'}, f"Key:Fill Ratio: {composition.key_fill_ratio:.1f}:1")
            
            # Report light roles
            self.report({'INFO'}, f"═══ Light Roles ═══")
            for role_result in light_roles:
                self.report({'INFO'}, 
                    f"  {role_result.light.name}: {role_result.role.value} "
                    f"({role_result.confidence:.0%})")
            
            # Report suggestions
            if composition.suggestions:
                self.report({'INFO'}, f"═══ Suggestions ═══")
                for suggestion in composition.suggestions[:3]:
                    self.report({'INFO'}, f"  • {suggestion}")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


# Registration
classes = [
    LUMI_OT_smart_add_light,
    LUMI_OT_analyze_composition,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
