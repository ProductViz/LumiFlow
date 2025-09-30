# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Normal Operations
Operators for normal-based positioning and alignment of lights.
"""
import bpy
from bpy_extras import view3d_utils
from mathutils import Vector
from ...utils import lumi_is_addon_enabled, lumi_raycast_at_mouse
from ...utils.light import lumi_get_light_pivot, lumi_set_light_pivot
from .utils import (
    lumi_disable_all_positioning_ops, 
    lumi_is_valid_positioning_context, 
    lumi_handle_modal_error, 
    lumi_handle_positioning_error,
    detect_positioning_mode,
    get_modifier_keys_for_mode
)
from ...core.state import get_state
from ...base_modal import BaseModalOperator

class LUMI_OT_normal_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.normal_positioning"
    bl_label = "Normal Positioning"
    bl_description = "Shift + LMB drag: Align light to face normal"
    bl_options = {'REGISTER', 'UNDO'}

    _dragging = False
    _initial_distances = {}
    _initial_positions = {}

    def __del__(self):
        """Clean up stored data when operator is destroyed"""
        try:
            # Only clean up if the object still exists
            if hasattr(self, '_initial_distances'):
                self._initial_distances.clear()
            if hasattr(self, '_initial_positions'):
                for light_name in self._initial_positions:
                    if 'pivot' in self._initial_positions[light_name]:
                        self._initial_positions[light_name]['pivot'] = None
                self._initial_positions.clear()
        except (ReferenceError, AttributeError):
            pass

    @classmethod
    def poll(cls, context):
        """Check if operator can run"""
        return lumi_is_valid_positioning_context(context)

    def validate_context(self, context):
        """Validate context for normal positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal operations"""
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=False, required_mode=None)

    def store_original_positions(self, context):
        """Store original positions and distances for selected lights"""
        self._initial_distances = {}
        self._initial_positions = {}
        scene_light_distance = context.scene.light_distance
        
        # Get selected lights
        selected_lights = [l for l in context.selected_objects if l.type == 'LIGHT']
        for light in selected_lights:
            self._initial_positions[light.name] = {
                'location': light.location.copy(),
                'rotation_euler': light.rotation_euler.copy(),
                'rotation_mode': light.rotation_mode,
                'pivot': None
            }
            
            if "Lumi_pivot_world" in light:
                try:
                    pivot = lumi_get_light_pivot(light)
                    self._initial_positions[light.name]['pivot'] = (pivot.x, pivot.y, pivot.z)
                    self._initial_distances[light.name] = (light.location - pivot).length
                except Exception as e:
                    print(f"âŒ Error storing pivot for {light.name}: {e}")
                    self._initial_positions[light.name]['pivot'] = None
                    self._initial_distances[light.name] = scene_light_distance
            else:
                self._initial_distances[light.name] = scene_light_distance

    def invoke(self, context, event):
        """Invoke method - starts modal operator for normal positioning"""
        try:
            
            self._dragging = False
            self._initial_distances = {}
            
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for normal positioning")
                return {'CANCELLED'}
            
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'NORMAL':
                return {'PASS_THROUGH'}
            
            
            scene = context.scene
            
            lumi_disable_all_positioning_ops(scene)
            state = get_state()
            state.set_modal_state('align', True)
            scene.light_props.positioning_mode = 'NORMAL'
            
            self._dragging = True
            self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
            self.store_original_positions(context)
            
            context.window_manager.modal_handler_add(self)
            
            # Enable overlay handler for positioning mode
            from ...overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            return {'RUNNING_MODAL'}
                
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Normal positioning")

    def modal(self, context, event):
        """Modal implementation for normal positioning - Shift + LMB drag"""
        
        try:
            if not self.validate_modal_context(context, event):
                return {'CANCELLED'}
            
            detected_mode = detect_positioning_mode(event)
            
            if self._dragging:
                pass
            elif detected_mode != 'NORMAL':
                return {'PASS_THROUGH'}
            
            if event.type == 'RIGHTMOUSE' or event.type == 'ESC':
                return self.cancel(context)

            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.shift:
                return {'PASS_THROUGH'}

            if event.shift and not event.ctrl and not event.alt:
                
                if self._dragging and event.type == 'MOUSEMOVE' and event.shift:
                    mouse_pos = (event.mouse_region_x, event.mouse_region_y)
                    
                    scene = context.scene
                    scene.lumi_smart_mouse_x = event.mouse_region_x
                    scene.lumi_smart_mouse_y = event.mouse_region_y
                    
                    hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, mouse_pos)

                    if hit_obj and hit_obj.type == 'MESH':
                        scene = context.scene
                        scene.light_target = hit_obj
                        scene.light_target_face_location = (hit_location.x, hit_location.y, hit_location.z)
                        
                        direction = hit_normal.normalized()
                        scene_light_distance = scene.light_distance
                        hit_location_copy = hit_location[:]
                        hit_normal_copy = hit_normal[:]
                        hit_obj_name = hit_obj.name
                        
                        selected_lights = [l for l in context.selected_objects if l.type == 'LIGHT']
                        for light in selected_lights:
                            distance = self._initial_distances.get(light.name, scene_light_distance)
                            light.location = hit_location + direction * distance
                            rot_quat = direction.to_track_quat('Z', 'Y')
                            light.rotation_euler = rot_quat.to_euler()
                            lumi_set_light_pivot(light, hit_location)
                            light["target_face_index"] = hit_index
                            light["target_face_location"] = hit_location_copy
                            light["target_face_normal"] = hit_normal_copy
                            light["target_face_object"] = hit_obj_name
                        self.report({'INFO'}, 'Normal positioning active - face highlighting enabled')
                    else:
                        self.report({'INFO'}, 'Normal positioning active - no mesh surface detected')

                    return {'RUNNING_MODAL'}

                if self._dragging and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    self._dragging = False
                    state = get_state()
                    if state:
                        state.set_modal_state('align', False)
                    
                    # Reset positioning mode for consistency with cancel
                    if hasattr(context.scene, 'light_props'):
                        context.scene.light_props.positioning_mode = 'DISABLE'
                    
                    self.cleanup(context)
                    self.report({'INFO'}, 'Normal positioning completed')
                    return {'FINISHED'}

            return {'PASS_THROUGH'}
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Normal positioning")

    def cleanup(self, context):
        """Clean up normal positioning state"""
        try:
            self._dragging = False
            state = get_state()
            state.set_modal_state('align', False)
            
            # Reset positioning mode
            if hasattr(context.scene, 'light_props'):
                context.scene.light_props.positioning_mode = 'DISABLE'
            else:
                pass
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                        
            super().cleanup(context)
            
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Normal cleanup")

    def cancel(self, context):
        """Cancel normal positioning and restore initial positions"""
        try:
            self._dragging = False
            self._start_mouse = None
            
            # Restore initial positions, rotations, and pivots for all selected lights
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            for light in selected_lights:
                if light.name in self._initial_positions:
                    initial_data = self._initial_positions[light.name]
                    # Restore position
                    light.location = initial_data['location'].copy()
                    # Restore rotation
                    light.rotation_mode = initial_data['rotation_mode']
                    light.rotation_euler = initial_data['rotation_euler'].copy()
                    # Restore pivot if it was stored
                    if initial_data['pivot'] is not None:
                        light["Lumi_pivot_world"] = initial_data['pivot']
                    else:
                        # If no initial pivot stored, remove pivot
                        if "Lumi_pivot_world" in light:
                            del light["Lumi_pivot_world"]
            
            # Clean up state
            state = get_state()
            state.set_modal_state('align', False)
            
            # Disable overlay handler only if no smart control is active
            if not state.scroll_control_enabled:
                from ...overlay import lumi_disable_cursor_overlay_handler
                lumi_disable_cursor_overlay_handler()
            
            # Reset positioning mode
            if hasattr(context.scene, 'light_props'):
                context.scene.light_props.positioning_mode = 'DISABLE'
            else:
                pass
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                        
            self.report({'INFO'}, "Normal positioning cancelled - positions restored")
            return {'CANCELLED'}
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Normal cancel")
            return {'CANCELLED'}

