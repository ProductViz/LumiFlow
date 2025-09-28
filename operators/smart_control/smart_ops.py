"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
# # Import modul utama Blender
import bpy
from ...utils import (
    lumi_is_addon_enabled, lumi_reset_highlight,
    lumi_update_light_orientation, lumi_apply_kelvin_to_lights
)
from ...utils.light import lumi_get_light_pivot
from ...utils.properties import LightControlProperties
from ..positioning.utils import lumi_get_active_power_value
from mathutils import Vector
from ...core.state import get_state
from ...base_modal import BaseModalOperator
from ...overlay import lumi_enable_cursor_overlay_handler, lumi_disable_cursor_overlay_handler
from ...utils.mode_manager import ModeManager


# # Definisi class untuk Operator
class LUMI_OT_smart_control(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.smart_control"
    bl_label = "Light Smart Control"
    bl_description = "Toggle smart control or control light properties with mouse movement"
    bl_options = {'REGISTER'}

    # Property untuk preset mode dari keymap
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
    _mmb_active = False  # Tambahkan flag untuk drag MMB
    
    # Smart sensitivity tracking variables
    _last_mouse_x = 0
    _last_time = 0
    _total_drag_distance = 0
    _drag_start_time = 0
    
    # Mode-based sensitivity configuration
    _MODE_SENSITIVITY = {
        'DISTANCE': {
            'base': 0.015,      # Base sensitivity
            'speed_factor': 1.5, # Speed multiplier
            'accel_factor': 2.0  # Acceleration factor for long drags
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
            'base': 0.001,
            'speed_factor': 0.8,
            'accel_factor': 1.2
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
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        # # Periksa apakah objek adalah lampu
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

    # # Method dipanggil saat operator dimulai
    def invoke(self, context, event):
        # # Coba eksekusi kode dengan error handling
        try:
            # Validate inputs
            if not self.validate_modal_context(context):
                self.report({'ERROR'}, "Invalid context for modal operation")
                # # Batalkan operasi
                return {'CANCELLED'}

            # # Ambil objek yang dipilih dalam scene
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            
            if not selected_lights:
                self.report({'WARNING'}, 'No lights selected! Please select at least one light object.')
                # # Batalkan operasi
                return {'CANCELLED'}

            state = get_state()
            
            # Direct activation - always start modal control when keymap is pressed
            # If already enabled, disable first then restart
            if state.scroll_control_enabled:
                # Clean up existing session
                state.scroll_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                self._redraw_view3d()
            
            # Start modal control
            scene = context.scene
            
            # # Set modal state
            state.register_modal('scroll', self)
            scene.lumi_scroll_control_enabled = True
            state.scroll_control_enabled = True
            
            # # Set initial values
            self._start_mouse_x = event.mouse_x
            # Use preset mode from property if provided by keymap, otherwise use scene mode
            if hasattr(self, 'mode') and self.mode:
                # Keymap provided a specific mode
                current_mode = self.mode
                # Also update scene mode to keep in sync
                scene.lumi_smart_mode = current_mode
            else:
                # Use scene mode (default behavior)
                current_mode = getattr(scene, 'lumi_smart_mode', 'DISTANCE')
            
            # # Get initial value based on mode
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
            elif current_mode == 'SPOT_SIZE':
                self._start_value = getattr(scene, 'light_spot_size', 45.0)
            elif current_mode == 'SPREAD':
                self._start_value = getattr(scene, 'light_spread', 180.0)
            
            # # Enable overlay
            lumi_enable_cursor_overlay_handler()
            
            # # Add modal handler
            context.window_manager.modal_handler_add(self)
            
            # Auto-start drag mode when activated via keymap
            # This makes it work immediately when keymap is pressed
            self._mmb_active = True
            self._start_mouse_x = event.mouse_x
            
            # Update mouse position for overlay immediately
            scene.lumi_smart_mouse_x = event.mouse_region_x
            scene.lumi_smart_mouse_y = event.mouse_region_y
            
            return {'RUNNING_MODAL'}
            
        # # Tangani error jika terjadi
        except Exception as e:
            self.report({'ERROR'}, f"Modal operation failed: {str(e)}")
            # Log full error for debugging
            import traceback
            traceback.print_exc()
            # # Batalkan operasi
            return {'CANCELLED'}
    
    def calculate_smart_sensitivity(self, context, event, delta_x, mode):
        """Calculate smart sensitivity based on mode, speed, and acceleration"""
        import time
        
        # Get mode configuration
        mode_config = self._MODE_SENSITIVITY.get(mode, self._MODE_SENSITIVITY['DISTANCE'])
        base_sensitivity = mode_config['base']
        speed_factor = mode_config['speed_factor']
        accel_factor = mode_config['accel_factor']
        
        # Initialize tracking if first time
        if self._last_time == 0:
            self._last_mouse_x = event.mouse_x
            self._last_time = time.time()
            self._total_drag_distance = 0
            self._drag_start_time = time.time()
            return base_sensitivity * delta_x
        
        # Calculate speed-based sensitivity
        current_time = time.time()
        time_delta = current_time - self._last_time
        
        if time_delta > 0:
            # Calculate mouse speed (pixels per second)
            current_mouse_x = event.mouse_x
            mouse_delta = current_mouse_x - self._last_mouse_x
            mouse_speed = abs(mouse_delta) / time_delta
            
            # Speed-based adjustment
            if mouse_speed < 100:  # Slow movement - high precision
                speed_multiplier = 0.5
            elif mouse_speed > 1000:  # Fast movement - less precision
                speed_multiplier = 2.0
            else:  # Medium speed - balanced
                speed_multiplier = 1.0
            
            # Apply speed factor
            speed_sensitivity = base_sensitivity * (1.0 + (speed_multiplier - 1.0) * speed_factor)
        else:
            speed_sensitivity = base_sensitivity
        
        # Calculate acceleration-based sensitivity
        self._total_drag_distance += abs(delta_x)
        drag_duration = current_time - self._drag_start_time
        
        if drag_duration > 0:
            # Acceleration based on total distance and duration
            if self._total_drag_distance < 100:  # Short drag - high precision
                accel_multiplier = 0.7
            elif self._total_drag_distance > 500:  # Long drag - fast adjustment
                accel_multiplier = 1.5
            else:  # Medium drag - balanced
                accel_multiplier = 1.0
            
            # Apply acceleration factor
            accel_sensitivity = speed_sensitivity * (1.0 + (accel_multiplier - 1.0) * accel_factor)
        else:
            accel_sensitivity = speed_sensitivity
        
        # Update tracking variables
        self._last_mouse_x = current_mouse_x
        self._last_time = current_time
        
        # Calculate final amount with direction
        final_sensitivity = accel_sensitivity
        amount = delta_x * final_sensitivity
        
        # Debug logging (optional)
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

    # # Method utama untuk modal operator
    def modal(self, context, event):
        # # Coba eksekusi kode dengan error handling
        try:
            if not self.validate_modal_context(context):
                self.report({'ERROR'}, "Context became invalid during modal operation")
                # # Batalkan operasi
                return {'CANCELLED'}

            state = get_state()
            scene = context.scene

            # TAB key untuk membuka menu kontrol mode saat modal aktif
            if event.type == 'TAB' and event.value == 'PRESS':
                # Menu functionality removed for simplicity
                self.report({'INFO'}, "Use keyboard shortcuts: D for mode/axis/step cycling")
                return {'RUNNING_MODAL'}

            # KEY 'D' cycling - Handle D key press untuk mode cycling
            # # Periksa jenis event (mouse, keyboard, dll)
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
                    
                    # Force redraw untuk update overlay
                    for area in context.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
                    # # Tetap jalankan modal operator
                    return {'RUNNING_MODAL'}
                
                # Only SCALE mode has axis cycling, POWER mode cycling removed
                # # Tetap jalankan modal operator
                return {'RUNNING_MODAL'}
        
            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'RIGHTMOUSE':
                pass               

            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'RIGHTMOUSE' and event.value == 'PRESS' and event.alt:
                pass
                
            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'RIGHTMOUSE' and not event.ctrl and not event.shift and not event.alt:
                return {'PASS_THROUGH'}

            # Early exit conditions
            if not lumi_is_addon_enabled() or not state.scroll_control_enabled:
                state.unregister_modal('scroll')
                self.reset_sensitivity_tracking()  # Reset sensitivity tracking
                # # Batalkan operasi
                return {'CANCELLED'}

            # # Ambil objek yang dipilih dalam scene
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if not selected_lights:
                state.unregister_modal('scroll')
                self.reset_sensitivity_tracking()  # Reset sensitivity tracking
                # # Batalkan operasi
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
                self.reset_sensitivity_tracking()  # Reset sensitivity tracking
                self.report({'INFO'}, message)
                # # Batalkan operasi
                return {'CANCELLED'}

            # ESC untuk batal
            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'ESC' and event.value == 'PRESS':
                return cleanup_and_exit(undo_changes=True, message='Scroll changes undone')

            # Exit when all modifiers are released (for keymap activation)
            if not (event.ctrl or event.shift or event.alt):
                return cleanup_and_exit()
            
            # Handle MIDDLEMOUSE press (for manual activation)
            if event.type == 'MIDDLEMOUSE' and event.value in {'PRESS', 'CLICK_DRAG'}:
                self._mmb_active = True
                self._start_mouse_x = event.mouse_x  # Reset start posisi saat drag dimulai
                self.reset_sensitivity_tracking()  # Reset sensitivity tracking
                return {'RUNNING_MODAL'}

            # Handle MIDDLEMOUSE release
            if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                self._mmb_active = False
                # End modal operation when mouse is released
                state.unregister_modal('scroll')
                scene.lumi_scroll_control_enabled = False
                lumi_disable_cursor_overlay_handler()
                lumi_reset_highlight(scene)
                self.report({'INFO'}, 'Smart control completed')
                return {'FINISHED'}

            # Proses perubahan hanya saat drag MIDDLEMOUSE aktif
            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'MOUSEMOVE' and self._mmb_active:
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                delta_x = event.mouse_x - self._start_mouse_x
                # Get scroll mode before calculating sensitivity
                scroll_mode = getattr(scene, 'lumi_smart_mode', 'DISTANCE')
                # Use smart sensitivity calculation
                amount = self.calculate_smart_sensitivity(context, event, delta_x, scroll_mode)
                lumi_reset_highlight(scene)
                
                # Validasi mode availability untuk light yang dipilih
                if selected_lights:
                    first_light = selected_lights[0]
                    light_type = first_light.data.type
                    if not ModeManager.is_mode_available(scroll_mode, light_type):
                        # # Tetap jalankan modal operator
                        return {'RUNNING_MODAL'}  # Skip processing untuk mode yang tidak tersedia
                
                # (kode perubahan nilai lampu sesuai mode, sama seperti sebelumnya)
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
                    angle_delta = amount * 0.05
                    for light in selected_lights:
                        data = light.data
                        if data.type == 'SUN':
                            data.angle = max(0.0, data.angle + angle_delta)
                        elif data.type == 'SPOT':
                            data.spot_size = max(0.0, min(3.1415, data.spot_size + angle_delta))
                        elif data.type == 'AREA' and hasattr(data, 'spread'):
                            data.spread = max(0.0, min(1.0, data.spread + angle_delta))
                elif scroll_mode == 'TEMPERATURE':
                    scene.lumi_status_temperature_active = True
                    # Use smart sensitivity amount directly with reasonable temperature scaling
                    color_step = amount * 100.0  # Scale factor for temperature changes
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
                # # Tetap jalankan modal operator
                return {'RUNNING_MODAL'}

            return {'PASS_THROUGH'}
        # # Tangani error jika terjadi
        except Exception as e:
            self.report({'ERROR'}, f"Modal operation failed: {str(e)}")
            # Clean up and exit on error
            # # Coba eksekusi kode dengan error handling
            try:
                state = get_state()
                state.unregister_modal('scroll')
                lumi_disable_cursor_overlay_handler()
            except:
                pass  # Cleanup failed, but continue with error handling
            
            import traceback
            traceback.print_exc()
            # # Batalkan operasi
            return {'CANCELLED'}

    def cancel(self, context):
        """Cancel method for modal operator cleanup"""
        # # Coba eksekusi kode dengan error handling
        try:
            state = get_state()
            state.unregister_modal('scroll')
            context.scene.lumi_scroll_control_enabled = False
            lumi_disable_cursor_overlay_handler()
            lumi_reset_highlight(context.scene)
        # # Tangani error jika terjadi
        except Exception as e:
            print(f"Error in cancel cleanup: {str(e)}")
        return None
    
    def _redraw_view3d(self):
        """Redraw 3D viewport"""
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()


# Register / unregister helpers for this module


CLASSES = (
    LUMI_OT_smart_control,
)


def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            # ignore duplicates during reload
            pass


def unregister():
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

