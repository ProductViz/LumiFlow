# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Orbit Operations
Operators for orbital positioning and rotation of lights around targets.
"""

import bpy
from mathutils import Vector, Matrix
import math
from ...utils import lumi_is_addon_enabled, lumi_update_light_orientation
from ...utils.light import lumi_get_light_pivot
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

class LUMI_OT_orbit_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.orbit_positioning"
    bl_label = "Orbit Positioning"
    bl_description = "Alt + LMB drag: Orbit lights around pivot point"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _dragging = False
    _initial_positions = {}
    
    azimuth: bpy.props.FloatProperty(
        name="Azimuth",
        description="Azimuth angle in degrees (rotation around Z)",
        default=0.0,
        min=-180.0,
        max=180.0,
        subtype='ANGLE',
        update=lambda self, context: self.apply_popup_changes(context)
    )

    elevation: bpy.props.FloatProperty(
        name="Elevation", 
        description="Elevation angle in degrees (from horizontal)",
        default=0.0,
        min=-90.0,
        max=90.0,
        subtype='ANGLE',
        update=lambda self, context: self.apply_popup_changes(context)
    )

    @classmethod
    def poll(cls, context):
        # # Get selected objects in scene
        return lumi_is_addon_enabled() and any(obj.type == 'LIGHT' for obj in context.selected_objects)

    def validate_context(self, context):
        """Validate context for orbit positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal orbit operations"""
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=True, required_mode='ORBIT')

    def invoke(self, context, event):
        """Invoke method - starts modal operator for orbit positioning"""
        try:
            # Validate inputs
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for orbit positioning")
                return {'CANCELLED'}
            
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'ORBIT':
                self.report({'WARNING'}, f"Use {get_modifier_keys_for_mode('ORBIT')} + LMB drag for orbit positioning")
                return {'CANCELLED'}
            
            scene = context.scene
            
            lumi_disable_all_positioning_ops(scene)
            
            state = get_state()
            state.set_modal_state('rotate', True)
            scene.light_props.positioning_mode = 'ORBIT'
            
            context.window_manager.modal_handler_add(self)
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            
            # Enable overlay handler for positioning mode
            from ...overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            self._dragging = True
            self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
            self.store_original_positions(context)
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            return {'RUNNING_MODAL'}
                
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Orbit positioning")

    def apply_popup_changes(self, context):
        """Apply azimuth/elevation changes when popup values change"""
        try:
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if not selected_lights:
                return
                
            for light in selected_lights:
                try:
                    if "Lumi_pivot_world" in light:
                        pivot = lumi_get_light_pivot(light)
                    elif hasattr(context.scene, 'light_target') and context.scene.light_target:
                        pivot = context.scene.light_target.location
                    else:
                        pivot = Vector((0.0, 0.0, 0.0))

                    vec = light.location - pivot
                    r = vec.length
                    if r <= 0.0001:
                        r = 1.0

                    target_az = math.radians(self.azimuth)
                    target_el = math.radians(self.elevation)

                    x = r * math.cos(target_el) * math.cos(target_az)
                    y = r * math.cos(target_el) * math.sin(target_az)
                    z = r * math.sin(target_el)

                    light.location = pivot + Vector((x, y, z))

                    if "Lumi_pivot_world" in light:
                        lumi_update_light_orientation(light)
                    else:
                        direction = (pivot - light.location)
                        if direction.length > 0.001:
                            direction = direction.normalized()
                            light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
                except Exception:
                    continue
        except Exception:
            pass

    def show_popup(self, context, event):
        """Show popup with current azimuth/elevation values"""
        try:
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if selected_lights:
                first = selected_lights[0]
                try:
                    if "Lumi_pivot_world" in first:
                        pivot = lumi_get_light_pivot(first)
                    elif hasattr(context.scene, 'light_target') and context.scene.light_target:
                        pivot = context.scene.light_target.location
                    else:
                        pivot = Vector((0.0, 0.0, 0.0))
                except Exception:
                    pivot = Vector((0.0, 0.0, 0.0))

                vec = first.location - pivot
                if vec.length > 0.001:
                    az = math.degrees(math.atan2(vec.y, vec.x))
                    el = math.degrees(math.atan2(vec.z, math.sqrt(vec.x * vec.x + vec.y * vec.y)))
                else:
                    az = 0.0
                    el = 0.0

                az = max(-180.0, min(180.0, az))  # Clamp azimuth to [-180, 180]
                el = max(-90.0, min(90.0, el))    # Clamp elevation to [-90, 90]

                bpy.ops.lumi.orbit_angles('INVOKE_DEFAULT', azimuth=az, elevation=el)
                
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Orbit popup")
            
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        try:
            # Validate inputs
            if not self.validate_modal_context(context, event):
                self.cleanup(context)
                # # Cancel operation
                return {'CANCELLED'}

            scene = context.scene
            if not lumi_is_addon_enabled() or scene.light_props.positioning_mode != 'ORBIT':
                self.cleanup(context)
                # # Cancel operation
                return {'CANCELLED'}
            
            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.ctrl:
                return {'PASS_THROUGH'}
            
            if event.type == 'C' and event.value == 'PRESS' and event.ctrl and event.shift:
                return self.show_popup(context, event)
            
            if not (not event.ctrl and not event.shift and event.alt):
                self.cleanup(context)
                return {'CANCELLED'}
           
            if self.handle_undo(context, event):
                return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if not self._dragging:
                    self._dragging = True
                    self.store_original_positions(context)
                    self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
                return {'RUNNING_MODAL'}
        except Exception as e:
            self.cleanup(context)
            return lumi_handle_modal_error(self, context, e, "Rotate modal")

        if self._dragging and event.type == 'MOUSEMOVE' and event.alt:
            # # Try to execute code with error handling
            try:
                scene = context.scene
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                
                selected_objects = context.selected_objects
                selected_lights = [obj for obj in selected_objects if obj.type == 'LIGHT']
                
                if selected_lights:
                    delta_x = (event.mouse_x - event.mouse_prev_x) * 0.01
                    delta_y = (event.mouse_y - event.mouse_prev_y) * 0.01
                    scene_light_target = scene.light_target
                    z_vector = Vector((0, 0, 1))
                    
                    for light in selected_lights:
                        try:
                            if "Lumi_pivot_world" in light:
                                pivot = lumi_get_light_pivot(light)
                            elif scene_light_target:
                                pivot = scene_light_target.location
                            else:
                                pivot = Vector((0, 0, 0))
                            
                            offset = light.location - pivot
                            offset = Matrix.Rotation(delta_x, 4, 'Z') @ offset

                            # Handle Z-axis alignment issue when elevation = 0
                            right_vector = offset.cross(z_vector)
                            if right_vector.length > 0.001:
                                right_vector.normalize()
                                offset = Matrix.Rotation(delta_y, 4, right_vector) @ offset
                            else:
                                # When offset is parallel to Z-axis (elevation = Â±90Â°)
                                # or when offset is zero (light at pivot), use X-axis as fallback
                                # This prevents the "spinning in place" issue
                                if abs(offset.z) > 0.001:  # Nearly vertical
                                    # Use X-axis for elevation rotation when vertical
                                    right_vector = Vector((1, 0, 0))
                                    offset = Matrix.Rotation(delta_y, 4, right_vector) @ offset
                                else:  # Nearly zero offset or horizontal
                                    # For elevation = 0 case, use Y-axis for elevation rotation
                                    right_vector = Vector((0, 1, 0))
                                    offset = Matrix.Rotation(delta_y, 4, right_vector) @ offset

                            light.location = pivot + offset

                            if "Lumi_pivot_world" in light:
                                lumi_update_light_orientation(light)
                            else:
                                direction = (pivot - light.location)
                                if direction.length > 0.001:
                                    direction = direction.normalized()
                                    light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
                        except Exception as light_error:
                            lumi_handle_positioning_error(self, context, light_error, f"Light {light.name} rotation")
                            continue
                            
                return {'RUNNING_MODAL'}
            except Exception as e:
                return lumi_handle_modal_error(self, context, e, "Rotation")
        
        # Handle mouse release - finish modal operation
        if self._dragging and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self._dragging = False
            state = get_state()
            if state:
                state.set_modal_state('rotate', False)
            
            # Reset positioning mode for consistency with cancel
            if hasattr(context.scene, 'light_props'):
                context.scene.light_props.positioning_mode = 'DISABLE'
            
            self.cleanup(context)
            self.report({'INFO'}, 'Orbit positioning completed')
            return {'FINISHED'}

        # Check if Alt key is released - cancel positioning
        if event.type == 'LEFTALT' and event.value == 'RELEASE':
            return self.cancel(context)

        return {'PASS_THROUGH'}
    
    def store_original_positions(self, context):
        """Store original positions and rotations of lights for cancel restore"""
        self._initial_positions = {}
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        
        # Store initial positions, rotations, rotation modes, and pivots for all selected lights
        for light in selected_lights:
            self._initial_positions[light.name] = {
                'location': light.location.copy(),
                'rotation_euler': light.rotation_euler.copy(),
                'rotation_mode': light.rotation_mode,
                'pivot': None  # Initialize pivot storage
            }
            
            # Store initial pivot position if it exists
            if "Lumi_pivot_world" in light:
                try:
                    pivot = lumi_get_light_pivot(light)
                    self._initial_positions[light.name]['pivot'] = (pivot.x, pivot.y, pivot.z)
                except Exception as e:
                    print(f"âŒ Error storing pivot for {light.name}: {e}")
                    self._initial_positions[light.name]['pivot'] = None
    
    def cancel(self, context):
        """Cancel orbit positioning and restore initial positions"""
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
            state.set_modal_state('rotate', False)
            
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
                        
            self.report({'INFO'}, "Orbit positioning cancelled - positions restored")
            return {'CANCELLED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def execute(self, context):
        """Execute method - not used for modal positioning"""
        return {'CANCELLED'}

    def add_timer(self, context):
        if self._timer is None:
            # # Coba eksekusi kode dengan error handling
            try:
                self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            except Exception as e:
                lumi_handle_positioning_error(self, context, e, "Add timer")

    def cleanup(self, context):
        state = get_state()
        # # Coba eksekusi kode dengan error handling
        try:
            if self._timer is not None:
                context.window_manager.event_timer_remove(self._timer)
                self._timer = None
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Orbit cleanup")
        
        state.set_modal_state('rotate', False)
        self._dragging = False
        super().cleanup(context)


class LUMI_OT_orbit_angles(bpy.types.Operator):
    """Popup to set azimuth and elevation for selected lights around pivot"""
    bl_idname = "lumi.orbit_angles"
    bl_label = "Orbit: Azimuth / Elevation"
    bl_description = "Set azimuth and elevation (degrees) for selected lights around pivot"
    bl_options = {'REGISTER', 'UNDO'}

    def update_realtime(self, context):
        """Update light positions in real-time when slider values change"""
        try:
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if not selected_lights:
                return

            for light in selected_lights:
                try:
                    # Get pivot point
                    pivot = Vector((0.0, 0.0, 0.0))
                    try:
                        if "Lumi_pivot_world" in light:
                            from ...utils.light import lumi_get_light_pivot
                            pivot = lumi_get_light_pivot(light)
                        elif hasattr(context.scene, 'light_target') and context.scene.light_target:
                            pivot = context.scene.light_target.location.copy()
                    except Exception:
                        pass

                    # Calculate distance from pivot
                    vec = light.location - pivot
                    r = vec.length
                    if r <= 0.001:
                        r = 1.0

                    # Convert angles to radians and calculate new position
                    target_az_rad = math.radians(self.azimuth)
                    target_el_rad = math.radians(self.elevation)

                    # Calculate new position using spherical coordinates
                    x = r * math.cos(target_el_rad) * math.cos(target_az_rad)
                    y = r * math.cos(target_el_rad) * math.sin(target_az_rad)
                    z = r * math.sin(target_el_rad)

                    # Set new position
                    light.location = pivot + Vector((x, y, z))

                    # Update light orientation
                    try:
                        from ...utils import lumi_update_light_orientation
                        lumi_update_light_orientation(light)
                    except Exception:
                        # Fallback: manual orientation
                        direction = (pivot - light.location)
                        if direction.length > 0.001:
                            direction = direction.normalized()
                            light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

                    # Force update
                    light.update_tag()
                    
                except Exception:
                    continue

            # Force scene update
            context.view_layer.update()
            
            # Force viewport refresh
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
                        
        except Exception:
            pass

    azimuth: bpy.props.FloatProperty(
        name="Azimuth (Â°)",
        description="Azimuth angle in degrees (rotation around Z)",
        default=0.0,
        min=-180.0,
        max=180.0,
        soft_min=-180.0,  # Soft range for better slider control
        soft_max=180.0,
        step=10,  # Smaller step for more responsive dragging (0.1 degree)
        precision=1,  # 1 decimal precision
        update=update_realtime
    )

    elevation: bpy.props.FloatProperty(
        name="Elevation (Â°)",
        description="Elevation angle in degrees (from horizontal)",
        default=0.0,
        min=-90.0,
        max=90.0,
        soft_min=-90.0,  # Soft range for better slider control
        soft_max=90.0,
        step=10,  # Smaller step for more responsive dragging (0.1 degree)
        precision=1,  # 1 decimal precision
        update=update_realtime
    )

    def invoke(self, context, event):
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        if not selected_lights:
            return {'CANCELLED'}

        first = selected_lights[0]
        # determine pivot
        try:
            if "Lumi_pivot_world" in first:
                from ...utils.light import lumi_get_light_pivot
                pivot = lumi_get_light_pivot(first)
            elif hasattr(context.scene, 'light_target') and context.scene.light_target:
                pivot = context.scene.light_target.location
            else:
                pivot = Vector((0.0, 0.0, 0.0))
        except Exception:
            pivot = Vector((0.0, 0.0, 0.0))

        vec = first.location - pivot
        r = vec.length
        if r <= 0.0001:
            r = 1.0
            
        # Calculate azimuth and elevation with proper range clamping
        az = math.degrees(math.atan2(vec.y, vec.x))
        el = math.degrees(math.atan2(vec.z, math.sqrt(vec.x * vec.x + vec.y * vec.y)))
        
        # Clamp values to property ranges
        az = max(-180.0, min(180.0, az))  # Clamp azimuth to [-180, 180]
        el = max(-90.0, min(90.0, el))    # Clamp elevation to [-90, 90]
        
        self.azimuth = az
        self.elevation = el

        return context.window_manager.invoke_props_popup(self, event)

    def execute(self, context):
        """Execute azimuth/elevation changes with simplified approach"""
        try:
            selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
            if not selected_lights:
                return {'CANCELLED'}

            success_count = 0
            for light in selected_lights:
                try:
                    # Get pivot point
                    pivot = Vector((0.0, 0.0, 0.0))
                    try:
                        if "Lumi_pivot_world" in light:
                            from ...utils.light import lumi_get_light_pivot
                            pivot = lumi_get_light_pivot(light)
                        elif hasattr(context.scene, 'light_target') and context.scene.light_target:
                            pivot = context.scene.light_target.location.copy()
                    except Exception:
                        pass  # use default pivot

                    # Calculate distance from pivot
                    vec = light.location - pivot
                    r = vec.length
                    if r <= 0.001:
                        r = 1.0  # minimum distance

                    # Convert angles to radians and calculate new position
                    target_az_rad = math.radians(self.azimuth)
                    target_el_rad = math.radians(self.elevation)

                    # Calculate new position using spherical coordinates
                    x = r * math.cos(target_el_rad) * math.cos(target_az_rad)
                    y = r * math.cos(target_el_rad) * math.sin(target_az_rad)
                    z = r * math.sin(target_el_rad)

                    # Set new position
                    new_location = pivot + Vector((x, y, z))
                    light.location = new_location

                    # Update light orientation to point toward pivot
                    try:
                        from ...utils import lumi_update_light_orientation
                        lumi_update_light_orientation(light)
                    except Exception:
                        # Fallback: manual orientation
                        direction = (pivot - light.location)
                        if direction.length > 0.001:
                            direction = direction.normalized()
                            light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

                    # Force update
                    light.update_tag()
                    success_count += 1
                    
                except Exception:
                    continue

            # Force scene update
            context.view_layer.update()
            
            # Force viewport refresh
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

            if success_count > 0:
                return {'FINISHED'}
            else:
                return {'CANCELLED'}
                
        except Exception:
            return {'CANCELLED'}

