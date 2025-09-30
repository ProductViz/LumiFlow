# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Smart Control Operations
Operators for smart control and manipulation of lights.
"""
import bpy
import math
from ..utils import (
    lumi_is_addon_enabled, lumi_reset_highlight,
    lumi_update_light_orientation, lumi_apply_kelvin_to_lights
)
from ..utils.light import lumi_get_light_pivot
from ..utils.properties import LightControlProperties
from .positioning.utils import lumi_get_active_power_value
from mathutils import Vector
from ..core.state import get_state
from ..base_modal import BaseModalOperator
from ..overlay import lumi_enable_cursor_overlay_handler, lumi_disable_cursor_overlay_handler
from ..utils.mode_manager import ModeManager


class LUMI_OT_smart_control(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.smart_control"
    bl_label = "Light Smart Control"
    bl_description = "Toggle smart control or control light properties with mouse movement"
    bl_options = {'REGISTER'}

    # Property for preset mode from keymap
    mode: bpy.props.EnumProperty(
        name="Mode",
        description="Preset control mode for keymap shortcuts",
        items=[
            ('DISTANCE', "Distance", "Control light distance"),
            ('POWER', "Power", "Control light power"),
            ('SCALE', "Scale", "Control light scale"),
            ('ANGLE', "Angle", "Control light angle/spot size/spread"),
            ('BLEND', "Blend", "Control light blend"),
            ('TEMPERATURE', "Temperature", "Control light temperature"),
        ],
        default='DISTANCE',
    )

    _start_mouse_x = 0
    _start_value = 0
    _mmb_active = False
    
    # Smart sensitivity tracking variables
    _last_mouse_x = 0
    _last_time = 0
    _total_drag_distance = 0
    _drag_start_time = 0
    
    # Mode-based sensitivity configuration
    _MODE_SENSITIVITY = {
        'DISTANCE': {
            'base': 0.015,
            'speed_factor': 1.5,
            'accel_factor': 2.0
        },
        'POWER': {
            'base': 0.008,
            'speed_factor': 1.2,
            'accel_factor': 1.8
        },
        'SCALE': {
            'base': 0.004,
            'speed_factor': 1.0,
            'accel_factor': 1.5
        },
        'ANGLE': {
            'base': 0.008,
            'speed_factor': 1.2,
            'accel_factor': 1.8
        },
        'TEMPERATURE': {
            'base': 0.006,
            'speed_factor': 1.3,
            'accel_factor': 1.6
        },
        'BLEND': {
            'base': 0.002,
            'speed_factor': 0.9,
            'accel_factor': 1.3
        }
    }

    @classmethod
    def poll(cls, context):
        has_light = any(obj.type == 'LIGHT' for obj in getattr(context, 'selected_objects', []))
        return lumi_is_addon_enabled() and has_light

    def validate_modal_context(self, context):
        """Validate context for modal operations"""
        if not context or not context.scene:
            return False
        if not lumi_is_addon_enabled():
            return False
        if not hasattr(context, 'selected_objects'):
            return False
        return True

    def invoke(self, context, event):
        try:
            if not self.validate_modal_context(context):
                self.report({'ERROR'}, "Invalid context for modal operation")
                return {'CANCELLED'}

            # Get selected objects in scene
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            
            if not selected_lights:
                self.report({'WARNING'}, 'No lights selected! Please select at least one light object.')
                return {'CANCELLED'}

            state = get_state()
            
            # Direct activation - start modal control when keymap is pressed
            if state.scroll_control_enabled:
                state.scroll_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                self._redraw_view3d()
            
            scene = context.scene
            
            state.register_modal('scroll', self)
            scene.lumi_scroll_control_enabled = True
            state.scroll_control_enabled = True
            
            self._start_mouse_x = event.mouse_x
            if hasattr(self, 'mode') and self.mode:
                current_mode = self.mode
                scene.lumi_smart_mode = current_mode
            else:
                current_mode = getattr(scene, 'lumi_smart_mode', 'DISTANCE')
            
            if current_mode == 'DISTANCE':
                self._start_value = getattr(scene, 'light_distance', 5.0)
            elif current_mode == 'POWER':
                self._start_value = getattr(scene, 'light_power', 100.0)
            elif current_mode == 'SCALE':
                self._start_value = getattr(scene, 'light_scale', 1.0)
            elif current_mode == 'ANGLE':
                self._start_value = getattr(scene, 'light_angle', 45.0)
            elif current_mode == 'TEMPERATURE':
                self._start_value = getattr(scene, 'light_temperature', 5500.0)
            elif current_mode == 'BLEND':
                self._start_value = getattr(scene, 'light_blend', 0.5)
            
            lumi_enable_cursor_overlay_handler()
            
            context.window_manager.modal_handler_add(self)
            
            # Auto-start drag mode when activated via keymap
            self._mmb_active = True
            self._start_mouse_x = event.mouse_x
            
            scene.lumi_smart_mouse_x = event.mouse_region_x
            scene.lumi_smart_mouse_y = event.mouse_region_y
            
            return {'RUNNING_MODAL'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Modal operation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def calculate_smart_sensitivity(self, context, event, delta_x, mode):
        """Calculate smart sensitivity based on mode, speed, and acceleration"""
        import time
        
        mode_config = self._MODE_SENSITIVITY.get(mode, self._MODE_SENSITIVITY['DISTANCE'])
        base_sensitivity = mode_config['base']
        speed_factor = mode_config['speed_factor']
        accel_factor = mode_config['accel_factor']
        
        if self._last_time == 0:
            self._last_mouse_x = event.mouse_x
            self._last_time = time.time()
            self._total_drag_distance = 0
            self._drag_start_time = time.time()
            return base_sensitivity * delta_x
        
        current_time = time.time()
        time_delta = current_time - self._last_time
        
        if time_delta > 0:
            current_mouse_x = event.mouse_x
            mouse_delta = current_mouse_x - self._last_mouse_x
            mouse_speed = abs(mouse_delta) / time_delta
            
            if mouse_speed < 100:
                speed_multiplier = 0.5
            elif mouse_speed > 1000:
                speed_multiplier = 2.0
            else:
                speed_multiplier = 1.0
            
            speed_sensitivity = base_sensitivity * (1.0 + (speed_multiplier - 1.0) * speed_factor)
        else:
            speed_sensitivity = base_sensitivity
        
        self._total_drag_distance += abs(delta_x)
        drag_duration = current_time - self._drag_start_time
        
        if drag_duration > 0:
            if self._total_drag_distance < 100:
                accel_multiplier = 0.7
            elif self._total_drag_distance > 500:
                accel_multiplier = 1.5
            else:
                accel_multiplier = 1.0
            
            accel_sensitivity = speed_sensitivity * (1.0 + (accel_multiplier - 1.0) * accel_factor)
        else:
            accel_sensitivity = speed_sensitivity
        
        self._last_mouse_x = current_mouse_x
        self._last_time = current_time
        
        final_sensitivity = accel_sensitivity
        amount = delta_x * final_sensitivity
        
        if hasattr(context.scene, 'lumi_debug_sensitivity') and context.scene.lumi_debug_sensitivity:
            if time_delta > 0:
                print(f"Mode: {mode}, Speed: {mouse_speed:.1f}px/s, Distance: {self._total_drag_distance:.1f}px, Sensitivity: {final_sensitivity:.4f}")
            else:
                print(f"Mode: {mode}, Distance: {self._total_drag_distance:.1f}px, Sensitivity: {final_sensitivity:.4f}")
        
        return amount
    
    def reset_sensitivity_tracking(self):
        """Reset sensitivity tracking variables"""
        self._last_mouse_x = 0
        self._last_time = 0
        self._total_drag_distance = 0
        self._drag_start_time = 0

    def modal(self, context, event):
        try:
            if not self.validate_modal_context(context):
                self.report({'ERROR'}, "Context became invalid during modal operation")
                return {'CANCELLED'}

            state = get_state()
            scene = context.scene

            if event.type == 'TAB' and event.value == 'PRESS':
                self.report({'INFO'}, "Use keyboard shortcuts: D for mode/axis/step cycling")
                return {'RUNNING_MODAL'}

            # Check event type (mouse, keyboard, etc.)
            if event.type == 'D' and event.value == 'PRESS':
                if scene.lumi_smart_mode == 'SCALE':
                    current_axis = scene.lumi_scale_axis
                    if current_axis == 'XY':
                        scene.lumi_scale_axis = 'X'
                        self.report({'INFO'}, "Scale axis: X only")
                    elif current_axis == 'X':
                        scene.lumi_scale_axis = 'Y'
                        self.report({'INFO'}, "Scale axis: Y only")
                    elif current_axis == 'Y':
                        scene.lumi_scale_axis = 'XY'
                        self.report({'INFO'}, "Scale axis: XY (Uniform)")
                    
                    for area in context.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
                    return {'RUNNING_MODAL'}
                
                # Keep modal operator running
                return {'RUNNING_MODAL'}
        
            if event.type == 'RIGHTMOUSE':
                pass               
            if event.type == 'RIGHTMOUSE' and event.value == 'PRESS' and event.alt:
                pass
                
            if event.type == 'RIGHTMOUSE' and not event.ctrl and not event.shift and not event.alt:
                return {'PASS_THROUGH'}

            if not lumi_is_addon_enabled() or not state.scroll_control_enabled:
                state.unregister_modal('scroll')
                self.reset_sensitivity_tracking()
                return {'CANCELLED'}

            # Get selected objects in scene
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if not selected_lights:
                state.unregister_modal('scroll')
                self.reset_sensitivity_tracking()
                return {'CANCELLED'}

            def cleanup_and_exit(undo_changes=False, message='Changes confirmed'):
                if undo_changes:
                    for obj in selected_lights:
                        if obj.name in self._initial_values:
                            obj.data.energy = self._initial_values[obj.name]
                state.unregister_modal('scroll')
                scene.lumi_scroll_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                if not undo_changes:
                    lumi_reset_highlight(scene)
                self.reset_sensitivity_tracking()
                self.report({'INFO'}, message)
                return {'CANCELLED'}

            if event.type == 'ESC' and event.value == 'PRESS':
                return cleanup_and_exit(undo_changes=True, message='Scroll changes undone')

            # Exit when all modifiers are released (for keymap activation)
            if not (event.ctrl or event.shift or event.alt):
                return cleanup_and_exit()
            
            # Handle MIDDLEMOUSE press (for manual activation)
            if event.type == 'MIDDLEMOUSE' and event.value in {'PRESS', 'CLICK_DRAG'}:
                self._mmb_active = True
                self._start_mouse_x = event.mouse_x
                self.reset_sensitivity_tracking()
                return {'RUNNING_MODAL'}

            # Handle MIDDLEMOUSE release
            if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                self._mmb_active = False
                state.unregister_modal('scroll')
                scene.lumi_scroll_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                lumi_reset_highlight(scene)
                self.report({'INFO'}, 'Smart control completed')
                return {'FINISHED'}

            # Process changes only when MIDDLEMOUSE drag is active
            if event.type == 'MOUSEMOVE' and self._mmb_active:
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                delta_x = event.mouse_x - self._start_mouse_x
                scroll_mode = getattr(scene, 'lumi_smart_mode', 'DISTANCE')
                amount = self.calculate_smart_sensitivity(context, event, delta_x, scroll_mode)
                lumi_reset_highlight(scene)
                
                # Validate mode availability for selected light
                if selected_lights:
                    first_light = selected_lights[0]
                    light_type = first_light.data.type
                    if not ModeManager.is_mode_available(scroll_mode, light_type):
                        return {'RUNNING_MODAL'}
                
                if scroll_mode == 'DISTANCE':
                    scene.lumi_status_distance_active = True
                    # Use smart sensitivity amount directly
                    distance_step = amount
                    light_target = scene.light_target
                    for light in selected_lights:
                        if "Lumi_pivot_world" in light:
                            pivot = lumi_get_light_pivot(light)
                            light_to_pivot = light.location - pivot
                            current_distance = light_to_pivot.length
                            new_distance = max(0.1, current_distance + distance_step)
                            direction_vec = light_to_pivot.normalized()
                            light.location = pivot + (direction_vec * new_distance)
                            lumi_update_light_orientation(light)
                        elif light_target:
                            target_pos = light_target.location
                            light_to_target = light.location - target_pos
                            current_distance = light_to_target.length
                            new_distance = max(0.1, current_distance + distance_step)
                            direction_vec = light_to_target.normalized()
                            light.location = target_pos + (direction_vec * new_distance)
                elif scroll_mode == 'POWER':
                    scene.lumi_status_power_active = True
                    power_value = lumi_get_active_power_value(context)
                    power_delta = amount * power_value
                    for light in selected_lights:
                        light.data.energy = max(0.001, light.data.energy + power_delta)
                elif scroll_mode == 'SCALE':
                    scene.lumi_status_scale_active = True
                    # Use smart sensitivity amount directly
                    scale_factor = amount
                    axis = scene.lumi_scale_axis
                    for light in selected_lights:
                        data = light.data
                        if data.type in {'POINT', 'SPOT'}:
                            data.shadow_soft_size = max(0.01, data.shadow_soft_size + scale_factor)
                        elif data.type == 'AREA':
                            shape = getattr(data, 'shape', 'SQUARE')
                            if shape in {'SQUARE', 'DISK'}:
                                data.size = max(0.01, data.size + scale_factor)
                            elif shape in {'RECTANGLE', 'ELLIPSE'}:
                                if axis == 'XY':
                                    data.size = max(0.01, data.size + scale_factor)
                                    data.size_y = max(0.01, data.size_y + scale_factor)
                                elif axis == 'X':
                                    data.size = max(0.01, data.size + scale_factor)
                                elif axis == 'Y':
                                    data.size_y = max(0.01, data.size_y + scale_factor)
                elif scroll_mode == 'ANGLE':
                    scene.lumi_status_angle_active = True
                    angle_delta = amount * 10
                    print(f"DEBUG ANGLE: amount={amount:.6f}, angle_delta={angle_delta:.6f}")
                    for light in selected_lights:
                        data = light.data
                        if data.type == 'SUN':
                            # Convert angle_delta from degrees to radians for SUN light
                            sun_delta = angle_delta * math.pi / 180.0
                            data.angle = max(0.0, min(math.pi, data.angle + sun_delta))
                        elif data.type == 'SPOT':
                            
                            spot_delta = angle_delta * math.pi / 180.0  
                            data.spot_size = max(0.0, min(math.pi, data.spot_size + spot_delta))
                        elif data.type == 'AREA' and hasattr(data, 'spread'):
                            if data.spread > 1.0:
                                data.spread = 0.5  
                            
                            spread_delta = angle_delta / 180.0  
                            data.spread = max(0.0, min(1.0, data.spread + spread_delta))
                            
                elif scroll_mode == 'TEMPERATURE':
                    scene.lumi_status_temperature_active = True  
                    color_step = amount * 100.0  
                    current_temp = getattr(scene, 'lumi_color_temperature', 5500)
                    new_temp = max(1000, min(20000, current_temp + color_step))
                    new_temp_int = int(new_temp)
                    scene.lumi_color_temperature = new_temp_int
                    lumi_apply_kelvin_to_lights(context, new_temp_int)
                elif scroll_mode == 'BLEND':
                    blend_delta = amount * 0.05
                    for light in selected_lights:
                        data = light.data
                        if data.type == 'SPOT':
                            data.spot_blend = max(0.0, min(1.0, data.spot_blend + blend_delta))
                self._start_mouse_x = event.mouse_x
                return {'RUNNING_MODAL'}

            return {'PASS_THROUGH'}
        except Exception as e:
            # Clean up and exit on error
            try:
                state = get_state()
                state.unregister_modal('scroll')
                lumi_disable_cursor_overlay_handler()
            except:
                pass
            
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def cancel(self, context):
        """Cancel method for modal operator cleanup"""
        try:
            state = get_state()
            state.unregister_modal('scroll')
            context.scene.lumi_scroll_control_enabled = False
            lumi_disable_cursor_overlay_handler()
            lumi_reset_highlight(context.scene)
        except Exception as e:
            print(f"Error in cancel cleanup: {str(e)}")
        return None
    
    def _redraw_view3d(self):
        """Redraw 3D viewport"""
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()


# Module exports and registration
__all__ = (
    'LUMI_OT_smart_control',
)

CLASSES = (
    LUMI_OT_smart_control,
)


def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass


def unregister():
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

