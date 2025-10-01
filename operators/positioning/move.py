# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Move Operations
Operators for moving and positioning lights.
"""
# Import main Blender modules
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

# Class definition for Operator - Refactored for Positioning Mode
class LUMI_OT_move_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.move_positioning"
    bl_label = "Move Positioning"
    bl_description = "Shift+Alt + LMB drag: Move light and pivot together"
    bl_options = {'REGISTER', 'UNDO'}

    _dragging = False
    _start_mouse = None
    _initial_positions = {}
    _timer = None

    @classmethod
    # # Method to determine when operator/panel is active
    def poll(cls, context):
        # # Get selected objects in scene
        return lumi_is_addon_enabled() and any(obj.type == 'LIGHT' for obj in context.selected_objects)

    def validate_context(self, context):
        """Validate context for move positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal move operations"""
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=True, required_mode='MOVE')

    def invoke(self, context, event):
        """Invoke method - starts modal operator for move positioning"""
        try:
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for move positioning")
                return {'CANCELLED'}
            
            # Check if this is the correct positioning mode (Shift+Alt + LMB drag)
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'MOVE':
                self.report({'WARNING'}, f"Use {get_modifier_keys_for_mode('MOVE')} + LMB drag for move positioning")
                return {'CANCELLED'}
            
            scene = context.scene
            
            # Disable any existing positioning operations
            lumi_disable_all_positioning_ops(scene)
            
            # Set up modal state
            state = get_state()
            state.set_modal_state('move', True)
            scene.light_props.positioning_mode = 'MOVE'
            
            # Setup modal operator
            context.window_manager.modal_handler_add(self)
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            
            # Enable overlay handler for positioning mode
            from ...ui.overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            # Initialize dragging state
            self._dragging = True
            self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
            self.store_initial_positions(context)
            
            # Set state for overlay detection
            if state:
                state.set_modal_state('move_pressing', True)
                # Force overlay redraw
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            return {'RUNNING_MODAL'}
                
        except Exception as e:
            import traceback
            error_msg = f"Error in move positioning operation: {str(e)}"
            self.report({'ERROR'}, error_msg)
            pass
            return {'CANCELLED'}

    # # Main method for modal operator
    def modal(self, context, event):
        """Modal implementation for move positioning"""
        # Validate context first
        if not self.validate_modal_context(context, event):
            return {'CANCELLED'}

        try:
            # Main event handling logic
            if event.type == 'RIGHTMOUSE':
                return self.cancel(context)

            # Allow wheel scrolling to pass through when Ctrl is held
            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.ctrl:
                return {'PASS_THROUGH'}

            # Check if Shift+Alt keys are still held (required for move positioning)
            if not (not event.ctrl and event.shift and event.alt):
                self._dragging = False
                self.cleanup(context)
                return {'CANCELLED'}

            # Handle mouse press for dragging (already started in invoke)
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if not self._dragging:
                    self._dragging = True
                    self._start_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
                    self.store_initial_positions(context)
                    # Set state for overlay detection
                    state = get_state()
                    if state:
                        state.set_modal_state('move_pressing', True)
                        # Force overlay redraw
                        for window in bpy.context.window_manager.windows:
                            for area in window.screen.areas:
                                if area.type == 'VIEW_3D':
                                    area.tag_redraw()
                return {'RUNNING_MODAL'}

            # Handle mouse movement for move positioning
            if self._dragging and event.type == 'MOUSEMOVE' and event.shift and event.alt:
                self._mouse_x = event.mouse_region_x
                self._mouse_y = event.mouse_region_y
                
                # Update mouse position for overlay cursor
                scene = context.scene
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                
                self.update_move_position(context)
                return {'RUNNING_MODAL'}

            # Handle mouse release - finish modal operation
            if self._dragging and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self._dragging = False
                # End modal operation when mouse is released
                state = get_state()
                if state:
                    state.set_modal_state('move_pressing', False)
                    state.set_modal_state('move', False)

                # Reset positioning mode for consistency with cancel
                if hasattr(context.scene, 'light_props'):
                    context.scene.light_props.positioning_mode = 'DISABLE'

                # Disable overlay handler only if no smart control is active
                if not state.scroll_control_enabled:
                    from ...ui.overlay import lumi_disable_cursor_overlay_handler
                    lumi_disable_cursor_overlay_handler()

                self.cleanup(context)
                self.report({'INFO'}, 'Move positioning completed')
                return {'FINISHED'}

            # Check if Shift+Alt keys are released - cancel positioning
            if (event.type == 'LEFTSHIFT' or event.type == 'RIGHTSHIFT' or event.type == 'LEFTALT' or event.type == 'RIGHTALT') and event.value == 'RELEASE':
                # Check if we still have the required modifier keys
                if not (event.shift and event.alt):
                    return self.cancel(context)

            return {'PASS_THROUGH'}
            
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Move positioning")

    def store_initial_positions(self, context):
        """Store initial positions and rotations of lights for cancel restore"""
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
                self._initial_positions[light.name]['pivot'] = tuple(light["Lumi_pivot_world"])

    def update_move_position(self, context):
        """Update light and pivot positions together based on 2D movement - natural movement like Free mode"""
        region = context.region
        rv3d = context.region_data
        coord = Vector((self._mouse_x, self._mouse_y))

        selected_objects = context.selected_objects
        
        for light in selected_objects:
            if light.type != 'LIGHT':
                continue

            try:
                # Get current pivot position
                current_pivot = lumi_get_light_pivot(light)
                if current_pivot is None:
                    # If no pivot exists, create one at a reasonable distance in front of the light
                    current_pivot = light.location + Vector((0, 0, -2))
                
                # Store initial light-to-pivot offset for maintaining relationship
                initial_light_to_pivot = current_pivot - light.location
                
                # Get viewport origin for distance calculation
                view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
                ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
                
                # Project current pivot to screen coordinates
                pivot_screen = view3d_utils.location_3d_to_region_2d(region, rv3d, current_pivot)
                
                if pivot_screen is not None:
                    # Calculate screen space movement from current pivot to cursor
                    screen_delta = coord - pivot_screen
                    
                    # Use perspective projection to calculate accurate world-space movement
                    # This method properly accounts for viewport depth and perspective
                    offset_coord = Vector((pivot_screen.x + screen_delta.x, pivot_screen.y + screen_delta.y))
                    
                    # Convert both positions from screen to world space at the same depth
                    pivot_world = view3d_utils.region_2d_to_location_3d(region, rv3d, pivot_screen, current_pivot)
                    offset_world = view3d_utils.region_2d_to_location_3d(region, rv3d, offset_coord, current_pivot)
                    
                    # Calculate actual world movement vector
                    world_movement = offset_world - pivot_world
                    
                    # Move pivot to new position (following cursor naturally)
                    new_pivot_location = current_pivot + world_movement
                    
                    # Move light to maintain the same relative offset from the new pivot
                    new_light_location = new_pivot_location - initial_light_to_pivot
                    
                    # Apply the new positions
                    light.location = new_light_location
                    lumi_set_light_pivot(light, new_pivot_location)
                    
                    # Make light face the pivot
                    direction_vector = new_pivot_location - new_light_location
                    if direction_vector.length > 0.001:
                        to_pivot = direction_vector.normalized()
                        rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                        light.rotation_mode = 'XYZ'
                        light.rotation_euler = rot_quat.to_euler('XYZ')
                else:
                    # Fallback: use ray casting at current depth if projection fails
                    camera_distance = (ray_origin - current_pivot).length
                    new_pivot_location = ray_origin + view_vector * camera_distance
                    
                    # Move light to maintain the same relative offset from the new pivot
                    new_light_location = new_pivot_location - initial_light_to_pivot
                    
                    # Apply the new positions
                    light.location = new_light_location
                    lumi_set_light_pivot(light, new_pivot_location)
                    
                    # Make light face the pivot
                    direction_vector = new_pivot_location - new_light_location
                    if direction_vector.length > 0.001:
                        to_pivot = direction_vector.normalized()
                        rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                        light.rotation_mode = 'XYZ'
                        light.rotation_euler = rot_quat.to_euler('XYZ')
                    
            except Exception as light_error:
                lumi_handle_positioning_error(self, context, light_error, f"Light {light.name} update")
                continue

    def cleanup(self, context):
        """Clean up move positioning state"""
        try:
            # Remove timer if it exists
            try:
                if self._timer is not None:
                    context.window_manager.event_timer_remove(self._timer)
                    self._timer = None
            except Exception as e:
                lumi_handle_positioning_error(self, context, e, "Move cleanup")

            self._dragging = False

            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

            super().cleanup(context)

        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Move cleanup")

    def cancel(self, context):
        """Cancel move positioning and restore initial positions"""
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
            scene = context.scene
            lumi_disable_all_positioning_ops(scene)
            state.set_modal_state('move', False)
            # Clear pressing state when cancel
            if state:
                state.set_modal_state('move_pressing', False)

            # Disable overlay handler only if no smart control is active
            if not state.scroll_control_enabled:
                from ...ui.overlay import lumi_disable_cursor_overlay_handler
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

            self._initial_positions = {}
            self.report({'INFO'}, "Move positioning cancelled - positions restored")
            return {'CANCELLED'}

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


