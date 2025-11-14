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
from ..ui.overlay import lumi_enable_cursor_overlay_handler, lumi_disable_cursor_overlay_handler
from ..utils.mode_manager import ModeManager


class LUMI_OT_smart_control(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.smart_control"
    bl_label = "Light Smart Control"
    bl_description = "Toggle smart control or control light properties with mouse movement"
    bl_options = {'REGISTER', 'UNDO'}

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
    
    # Mode-based sensitivity configuration (now percentage-based, only base sensitivity used)
    _MODE_SENSITIVITY = {
        'DISTANCE': {
            'base_percent': 0.5  # 0.5% per pixel
        },
        'POWER': {
            'base_percent': 1.0  # 1.0% per pixel
        },
        'SCALE': {
            'base_percent': 0.3  # 0.3% per pixel
        },
        'ANGLE': {
            'base_percent': 0.5  # 0.5% per pixel
        },
        'TEMPERATURE': {
            'base_percent': 0.5  # 5.0% per pixel
        },
        'BLEND': {
            'base_percent': 0.5  # 0.5% per pixel
        }
    }

    @classmethod
    def poll(cls, context):
        has_light = any(obj.type == 'LIGHT' for obj in getattr(context, 'selected_objects', []))
        smart_control_mode_enabled = getattr(context.scene, 'lumi_smart_control_mode_enabled', True)
        return lumi_is_addon_enabled() and smart_control_mode_enabled and has_light

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

            # Store initial values for undo on ESC
            self._initial_values = {}
            scene = context.scene
            self._initial_scene_temp = getattr(scene, 'lumi_color_temperature', 5500)
            
            # Reset warning flags for new modal session
            self._spread_warning_shown = False
            
            for light in selected_lights:
                self._initial_values[light.name] = {
                    'location': light.location.copy(),
                    'energy': light.data.energy,
                    'color': light.data.color[:],
                    'shadow_soft_size': getattr(light.data, 'shadow_soft_size', 0.0),
                    'size': getattr(light.data, 'size', 0.0),
                    'size_y': getattr(light.data, 'size_y', 0.0),
                    'spot_size': getattr(light.data, 'spot_size', 0.0),
                    'spot_blend': getattr(light.data, 'spot_blend', 0.0),
                    'angle': getattr(light.data, 'angle', 0.0),
                    'spread': getattr(light.data, 'spread', 0.0)
                }

            state = get_state()
            
            # Direct activation - start modal control when keymap is pressed
            if state.smart_control_enabled:
                state.smart_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                self._redraw_view3d()
            
            scene = context.scene
            
            state.register_modal('scroll', self)
            scene.lumi_smart_control_enabled = True
            state.smart_control_enabled = True
            
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
    
    def calculate_smart_sensitivity(self, context, event, delta_x, mode, current_value=1.0):
        """Calculate smart sensitivity based on base percentage only"""
        
        mode_config = self._MODE_SENSITIVITY.get(mode, self._MODE_SENSITIVITY['DISTANCE'])
        base_percent = mode_config['base_percent']
        
        # Return percentage change (as decimal, e.g., 0.05 for 5%)
        percentage_change = (base_percent / 100.0) * delta_x
        
        if hasattr(context.scene, 'lumi_debug_sensitivity') and context.scene.lumi_debug_sensitivity:
            print(f"Mode: {mode}, Base Percent: {base_percent:.2f}%, Delta X: {delta_x}, Change: {percentage_change:.4f}")
        
        return percentage_change
    
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
                    # Check if any selected light is Area with Rectangle or Ellipse shape
                    can_change_axis = False
                    for light in selected_lights:
                        if light.data.type == 'AREA':
                            shape = getattr(light.data, 'shape', 'SQUARE')
                            if shape in {'RECTANGLE', 'ELLIPSE'}:
                                can_change_axis = True
                                break
                    
                    if can_change_axis:
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
                    else:
                        self.report({'INFO'}, "Axis change only available for Area lights with Rectangle/Ellipse shape")
                    
                    return {'RUNNING_MODAL'}
                
                # Keep modal operator running
                return {'RUNNING_MODAL'}
        
            if event.type == 'RIGHTMOUSE':
                pass               
            if event.type == 'RIGHTMOUSE' and event.value == 'PRESS' and event.alt:
                pass
                
            if event.type == 'RIGHTMOUSE' and not event.ctrl and not event.shift and not event.alt:
                return {'PASS_THROUGH'}

            if not lumi_is_addon_enabled() or not state.smart_control_enabled:
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
                    # Restore all initial values
                    scene.lumi_color_temperature = self._initial_scene_temp
                    for light in selected_lights:
                        if light.name in self._initial_values:
                            initial = self._initial_values[light.name]
                            light.location = initial['location']
                            light.data.energy = initial['energy']
                            light.data.color = initial['color']
                            if hasattr(light.data, 'shadow_soft_size'):
                                light.data.shadow_soft_size = initial['shadow_soft_size']
                            if hasattr(light.data, 'size'):
                                light.data.size = initial['size']
                            if hasattr(light.data, 'size_y'):
                                light.data.size_y = initial['size_y']
                            if hasattr(light.data, 'spot_size'):
                                light.data.spot_size = initial['spot_size']
                            if hasattr(light.data, 'spot_blend'):
                                light.data.spot_blend = initial['spot_blend']
                            if hasattr(light.data, 'angle'):
                                light.data.angle = initial['angle']
                            if hasattr(light.data, 'spread'):
                                light.data.spread = initial['spread']
                state.unregister_modal('scroll')
                scene.lumi_smart_control_enabled = False
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
                scene.lumi_smart_control_enabled = False
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
                # Calculate amount - special handling for POWER, ANGLE, BLEND, TEMPERATURE modes with inverse relationship
                if scroll_mode in ['POWER', 'ANGLE', 'BLEND', 'TEMPERATURE']:
                    # These modes use inverse relationship, amount calculated per light/item in the mode block
                    amount = 0  # Placeholder, will be calculated per light/item
                else:
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
                    light_target = scene.light_target
                    for light in selected_lights:
                        if "Lumi_pivot_world" in light:
                            pivot = lumi_get_light_pivot(light)
                            light_to_pivot = light.location - pivot
                            current_distance = light_to_pivot.length
                            # Apply percentage change: new_distance = current_distance * (1 + amount)
                            new_distance = max(0.1, current_distance * (1.0 + amount))
                            direction_vec = light_to_pivot.normalized()
                            light.location = pivot + (direction_vec * new_distance)
                            lumi_update_light_orientation(light)
                        elif light_target:
                            target_pos = light_target.location
                            light_to_target = light.location - target_pos
                            current_distance = light_to_target.length
                            # Apply percentage change: new_distance = current_distance * (1 + amount)
                            new_distance = max(0.1, current_distance * (1.0 + amount))
                            direction_vec = light_to_target.normalized()
                            light.location = target_pos + (direction_vec * new_distance)
                elif scroll_mode == 'POWER':
                    scene.lumi_status_power_active = True
                    for light in selected_lights:
                        current_energy = light.data.energy
                        # Inverse relationship: sensitivitas berkurang dari 1% (nilai 1) ke 0.2% (nilai 100)
                        clamped_energy = max(1.0, min(100.0, current_energy))  # Clamp ke rentang 1-100
                        # Formula: sensitivitas = 1.0 - (0.8/99) * (clamped_energy - 1)
                        sensitivity_percent = 1.0 - (0.8 / 99.0) * (clamped_energy - 1.0)
                        # Hitung amount berdasarkan delta_x dan sensitivitas
                        amount = (sensitivity_percent / 100.0) * delta_x
                        # Apply percentage change: new_energy = current_energy * (1 + amount)
                        new_energy = max(0.001, current_energy * (1.0 + amount))
                        light.data.energy = new_energy
                elif scroll_mode == 'SCALE':
                    scene.lumi_status_scale_active = True
                    
                    # Check if any selected light can use non-XY axis
                    can_use_custom_axis = False
                    for light in selected_lights:
                        if light.data.type == 'AREA':
                            shape = getattr(light.data, 'shape', 'SQUARE')
                            if shape in {'RECTANGLE', 'ELLIPSE'}:
                                can_use_custom_axis = True
                                break
                    
                    # Force XY axis if no Area Rectangle/Ellipse light selected
                    if not can_use_custom_axis and scene.lumi_scale_axis != 'XY':
                        scene.lumi_scale_axis = 'XY'
                    
                    axis = scene.lumi_scale_axis
                    for light in selected_lights:
                        data = light.data
                        if data.type in {'POINT', 'SPOT'}:
                            current_size = data.shadow_soft_size
                            new_size = max(0.01, current_size * (1.0 + amount))
                            data.shadow_soft_size = new_size
                        elif data.type == 'AREA':
                            shape = getattr(data, 'shape', 'SQUARE')
                            if shape in {'SQUARE', 'DISK'}:
                                current_size = data.size
                                new_size = max(0.01, current_size * (1.0 + amount))
                                data.size = new_size
                            elif shape in {'RECTANGLE', 'ELLIPSE'}:
                                if axis == 'XY':
                                    current_size = data.size
                                    current_size_y = data.size_y
                                    new_size = max(0.01, current_size * (1.0 + amount))
                                    new_size_y = max(0.01, current_size_y * (1.0 + amount))
                                    data.size = new_size
                                    data.size_y = new_size_y
                                elif axis == 'X':
                                    current_size = data.size
                                    new_size = max(0.01, current_size * (1.0 + amount))
                                    data.size = new_size
                                elif axis == 'Y':
                                    current_size_y = data.size_y
                                    new_size_y = max(0.01, current_size_y * (1.0 + amount))
                                    data.size_y = new_size_y
                elif scroll_mode == 'ANGLE':
                    scene.lumi_status_angle_active = True
                    for light in selected_lights:
                        data = light.data
                        if data.type == 'SUN':
                            current_angle = data.angle
                            # Convert to degrees for sensitivity calculation (1-180 range)
                            current_angle_deg = math.degrees(current_angle)
                            clamped_angle = max(1.0, min(180.0, current_angle_deg))
                            # Inverse sensitivity: 0.5% at 1° to 0.1% at 180°
                            sensitivity_percent = 0.5 - (0.4 / 179.0) * (clamped_angle - 1.0)
                            # Calculate amount based on delta_x and sensitivity
                            amount = (sensitivity_percent / 100.0) * delta_x
                            # Apply percentage change: new_angle = current_angle * (1 + amount)
                            new_angle = max(0.0, min(math.pi, current_angle * (1.0 + amount)))
                            data.angle = new_angle
                        elif data.type == 'SPOT':
                            current_angle = data.spot_size
                            # Convert to degrees for sensitivity calculation (1-180 range)
                            current_angle_deg = math.degrees(current_angle)
                            clamped_angle = max(1.0, min(180.0, current_angle_deg))
                            # Inverse sensitivity: 0.5% at 1° to 0.1% at 180°
                            sensitivity_percent = 0.5 - (0.4 / 179.0) * (clamped_angle - 1.0)
                            # Calculate amount based on delta_x and sensitivity
                            amount = (sensitivity_percent / 100.0) * delta_x
                            # Apply percentage change: new_angle = current_angle * (1 + amount)
                            new_angle = max(0.0, min(math.pi, current_angle * (1.0 + amount)))
                            data.spot_size = new_angle
                        elif data.type == 'AREA' and hasattr(data, 'spread'):
                            # CRITICAL: Spread is only available in Cycles render engine
                            if scene.render.engine != 'CYCLES':
                                # Skip spread adjustment if not using Cycles
                                # Show warning only once per modal session
                                if not hasattr(self, '_spread_warning_shown'):
                                    self.report({'WARNING'}, f'Spread control requires Cycles render engine (current: {scene.render.engine})')
                                    self._spread_warning_shown = True
                                continue
                            
                            current_spread = data.spread
                            # Convert to degrees for sensitivity calculation (1-180 range)
                            current_spread_deg = math.degrees(current_spread)
                            clamped_spread = max(1.0, min(180.0, current_spread_deg))
                            # Inverse sensitivity: 0.5% at 1° to 0.1% at 180°
                            sensitivity_percent = 0.5 - (0.4 / 179.0) * (clamped_spread - 1.0)
                            # Calculate amount based on delta_x and sensitivity
                            amount = (sensitivity_percent / 100.0) * delta_x
                            # Apply percentage change: new_spread = current_spread * (1 + amount)
                            new_spread = max(0.0, min(math.pi, current_spread * (1.0 + amount)))
                            data.spread = new_spread
                            
                elif scroll_mode == 'TEMPERATURE':
                    scene.lumi_status_temperature_active = True  
                    current_temp = getattr(scene, 'lumi_color_temperature', 5500)
                    # Clamp temperature to range 1000-20000 for sensitivity calculation
                    clamped_temp = max(1000.0, min(20000.0, current_temp))
                    # Inverse sensitivity: 0.5% at 1000K to 0.1% at 20000K
                    sensitivity_percent = 0.5 - (0.4 / 19000.0) * (clamped_temp - 1000.0)
                    # Calculate amount based on delta_x and sensitivity
                    amount = (sensitivity_percent / 100.0) * delta_x
                    # Apply percentage change: new_temp = current_temp * (1 + amount)
                    new_temp = max(1000, min(20000, current_temp * (1.0 + amount)))
                    new_temp_int = int(new_temp)
                    scene.lumi_color_temperature = new_temp_int
                    lumi_apply_kelvin_to_lights(context, new_temp_int)
                elif scroll_mode == 'BLEND':
                    for light in selected_lights:
                        data = light.data
                        if data.type == 'SPOT':
                            current_blend = data.spot_blend
                            # Clamp blend to range 0.01-1 for sensitivity calculation
                            clamped_blend = max(0.01, min(1.0, current_blend))
                            # Inverse sensitivity: 0.5% at 0.01 to 0.1% at 1.0
                            sensitivity_percent = 0.5 - (0.4 / 0.99) * (clamped_blend - 0.01)
                            # Calculate amount based on delta_x and sensitivity
                            amount = (sensitivity_percent / 100.0) * delta_x
                            # Apply percentage change: new_blend = current_blend * (1 + amount)
                            new_blend = max(0.0, min(1.0, current_blend * (1.0 + amount)))
                            data.spot_blend = new_blend
                self._start_mouse_x = event.mouse_x
                return {'RUNNING_MODAL'}

            return {'PASS_THROUGH'}
        except Exception as e:
            # Clean up and exit on error
            try:
                state = get_state()
                state.unregister_modal('scroll')
                lumi_disable_cursor_overlay_handler()
            except Exception as cleanup_error:
                logger.error(f"Cleanup failed during modal error: {cleanup_error}")
            
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def cancel(self, context):
        """Cancel method for modal operator cleanup"""
        try:
            state = get_state()
            state.unregister_modal('scroll')
            context.scene.lumi_smart_control_enabled = False
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

