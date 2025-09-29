"""
Target Operations
Operators for target-based positioning and alignment of lights.
"""

import bpy
from mathutils import Vector
from bpy_extras import view3d_utils
from ...utils import lumi_is_addon_enabled
from ...utils.light import lumi_set_light_pivot, lumi_get_light_pivot
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

class LUMI_OT_target_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.target_positioning"
    bl_label = "Target Positioning"
    bl_description = "Ctrl+Alt + LMB drag: Position lights by targeting surface points"
    bl_options = {'REGISTER', 'UNDO'}

    _start_mouse = None
    _pivot_data = {}
    _timer = None
    _initial_positions = {}

    @classmethod    
    def poll(cls, context):
        """Check if the operator can be invoked"""
        return lumi_is_addon_enabled() and any(obj.type == 'LIGHT' for obj in context.selected_objects)

    def validate_context(self, context):
        """Validate context for target positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal target operations"""
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=True, required_mode='TARGET')

    def invoke(self, context, event):
        """Invoke for target positioning"""
        try:
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for target positioning")
                return {'CANCELLED'}
            
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'TARGET':
                self.report({'WARNING'}, f"Use {get_modifier_keys_for_mode('TARGET')} + LMB drag for target positioning")
                return {'CANCELLED'}
            
            scene = context.scene
            
            lumi_disable_all_positioning_ops(scene)
            
            state = get_state()
            scene.light_props.positioning_mode = 'TARGET'
            
            context.window_manager.modal_handler_add(self)
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            
            # Enable overlay handler for positioning mode
            from ...overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            self._dragging = True
            self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
            self.store_initial_positions(context)
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            return {'RUNNING_MODAL'}
                
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Target positioning")

    def modal(self, context, event):
        try:
            if not self.validate_modal_context(context, event):
                self._dragging = False
                self.cleanup(context)
                return {'CANCELLED'}

            scene = context.scene
            if not lumi_is_addon_enabled() or scene.light_props.positioning_mode != 'TARGET':
                self._dragging = False
                self.cleanup(context)
                return {'CANCELLED'}

            context.area.tag_redraw()

            if event.type == 'RIGHTMOUSE':
                return self.cancel(context)

            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.ctrl:
                return {'PASS_THROUGH'}
            
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if not self._dragging:
                    self._dragging = True
                return {'RUNNING_MODAL'}

            if self._dragging and event.type == 'MOUSEMOVE' and event.ctrl and event.alt:
                self._mouse_x = event.mouse_region_x
                self._mouse_y = event.mouse_region_y
                
                scene = context.scene
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                
                self.update_target_position(context)
                return {'RUNNING_MODAL'}

            if self._dragging and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self._dragging = False
                state = get_state()
                if state:
                    state.set_modal_state('target', False)
                
                # Reset positioning mode for consistency with cancel
                if hasattr(context.scene, 'light_props'):
                    context.scene.light_props.positioning_mode = 'DISABLE'
                
                self.cleanup(context)
                self.report({'INFO'}, 'Target positioning completed')
                return {'FINISHED'}

            if (event.type == 'LEFTCTRL' or event.type == 'RIGHTCTRL' or event.type == 'LEFTALT' or event.type == 'RIGHTALT') and event.value == 'RELEASE':
                if not (event.ctrl and event.alt):
                    return self.cancel(context)

            return {'PASS_THROUGH'}
        except Exception as e:
            self.report({'ERROR'}, f"Target modal error: {str(e)}")
            self.cleanup(context)
            return {'CANCELLED'}

    def cancel(self, context):
        """Cancel target positioning and restore initial positions"""
        try:
            self._dragging = False
            self._start_mouse = None
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            for light in selected_lights:
                if light.name in self._initial_positions:
                    initial_data = self._initial_positions[light.name]
                    light.location = initial_data['location'].copy()
                    light.rotation_mode = initial_data['rotation_mode']
                    light.rotation_euler = initial_data['rotation_euler'].copy()
                    if initial_data.get('pivot') is not None:
                        light["Lumi_pivot_world"] = initial_data['pivot']
            
            state = get_state()
            state.set_modal_state('target', False)
            
            # Disable overlay handler only if no smart control is active
            if not state.scroll_control_enabled:
                from ...overlay import lumi_disable_cursor_overlay_handler
                lumi_disable_cursor_overlay_handler()
            
            # Reset positioning mode
            if hasattr(context.scene, 'light_props'):
                context.scene.light_props.positioning_mode = 'DISABLE'
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                        
            self.report({'INFO'}, "Target positioning cancelled - positions restored")
            return {'CANCELLED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def update_target_position(self, context):
        # # Try to execute code with error handling
        try:
            region = context.region
            rv3d = context.region_data
            coord = Vector((self._mouse_x, self._mouse_y))

            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

            scene = context.scene
            depsgraph = context.view_layer.depsgraph
            hit, location, normal, *_ = scene.ray_cast(depsgraph, ray_origin, view_vector)

            if hit:
                # # Get selected objects in scene
                selected_objects = context.selected_objects
                for light in selected_objects:
                    if light.type != 'LIGHT':
                        continue

                    # # Try to execute code with error handling
                    try:
                        lumi_set_light_pivot(light, location)

                        direction_vector = location - light.location
                        if direction_vector.length > 0.001:
                            to_pivot = direction_vector.normalized()
                            rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                            light.rotation_mode = 'XYZ'
                            light.rotation_euler = rot_quat.to_euler('XYZ')
                    except Exception as light_error:
                        lumi_handle_positioning_error(self, context, light_error, f"Light {light.name} target")
                        continue
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Target position update")

    def cleanup(self, context):
        state = get_state()
        # # Try to execute code with error handling
        try:
            if self._timer is not None:
                context.window_manager.event_timer_remove(self._timer)
                self._timer = None
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Target cleanup")
        
        state.set_modal_state('target', False)
        self._dragging = False
        super().cleanup(context)
    
    def store_initial_positions(self, context):
        """Store initial positions, rotations, and rotation modes of lights for cancel restore"""
        self._initial_positions = {}
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
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
                except Exception as e:
                    print(f"âŒ Error storing pivot for {light.name}: {e}")
                    self._initial_positions[light.name]['pivot'] = None

