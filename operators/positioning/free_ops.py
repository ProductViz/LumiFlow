"""
Free Positioning Operations
Operators for free positioning and movement of lights.
"""

# Import modul utama Blender
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

# Simple state import - replaces complex core.state
# try:
#     from ... import get_state
# except ImportError:
#     def get_state(): return type('SimpleState', (), {'overlay_enabled': True, 'current_mode': 'POWER', 'last_light': None})()

# Definisi class untuk Operator - Refactored for Positioning Mode
class LUMI_OT_free_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.free_positioning"
    bl_label = "Free Positioning"
    bl_description = "Ctrl+Shift + LMB drag: Freely position pivot while light aims at it"
    bl_options = {'REGISTER', 'UNDO'}

    _dragging = False
    _start_mouse = None
    _pivot_data = {}
    _timer = None
    _initial_positions = {}  # Store initial positions for cancel restore

    @classmethod
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        # # Ambil objek yang dipilih dalam scene
        return lumi_is_addon_enabled() and any(obj.type == 'LIGHT' for obj in context.selected_objects)

    def validate_context(self, context):
        """Validate context for free positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal free operations"""
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=True, required_mode='FREE')

    def invoke(self, context, event):
        """Invoke method - starts modal operator for free positioning"""
        try:
            # Validate inputs
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for free positioning")
                return {'CANCELLED'}
            
            # Check if this is the correct positioning mode (Ctrl+Shift + LMB drag)
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'FREE':
                self.report({'WARNING'}, f"Use {get_modifier_keys_for_mode('FREE')} + LMB drag for free positioning")
                return {'CANCELLED'}
            
            scene = context.scene
            
            # Disable any existing positioning operations
            lumi_disable_all_positioning_ops(scene)
            
            # Set up modal state
            state = get_state()
            state.set_modal_state('free', True)
            scene.light_props.positioning_mode = 'FREE'
            
            # Setup modal operator
            context.window_manager.modal_handler_add(self)
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            
            # Enable overlay handler untuk positioning mode
            from ...overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            # Initialize dragging state
            self._dragging = True
            self._start_mouse = (event.mouse_region_x, event.mouse_region_y)
            self.store_initial_positions(context)
            
            # Set state for overlay detection
            if state:
                state.set_modal_state('free_pressing', True)
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
            error_msg = f"Error in free positioning operation: {str(e)}"
            self.report({'ERROR'}, error_msg)
            pass
            return {'CANCELLED'}

    # # Method utama untuk modal operator
    def modal(self, context, event):
        """Modal implementation for free positioning"""
        # # Coba eksekusi kode dengan error handling
        try:
            # Validate inputs
            if not self.validate_modal_context(context, event):
                self._dragging = False
                return {'CANCELLED'}

            scene = context.scene
            if not lumi_is_addon_enabled() or scene.light_props.positioning_mode != 'FREE':
                self._dragging = False
                return {'CANCELLED'}

            context.area.tag_redraw()

            # # Periksa jenis event (mouse, keyboard, dll)
            if event.type == 'RIGHTMOUSE':
                return self.cancel(context)

            # # Allow wheel scrolling to pass through when Ctrl is held
            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.ctrl:
                return {'PASS_THROUGH'}

            # Check if Ctrl+Shift keys are still held (required for free positioning)
            if not (event.ctrl and event.shift and not event.alt):
                self._dragging = False
                self.cleanup(context)
                return {'CANCELLED'}

            # Handle mouse press for dragging (already started in invoke)
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if not self._dragging:
                    self._dragging = True
                    # Set state for overlay detection
                    state = get_state()
                    if state:
                        state.set_modal_state('free_pressing', True)
                        # Force overlay redraw
                        for window in bpy.context.window_manager.windows:
                            for area in window.screen.areas:
                                if area.type == 'VIEW_3D':
                                    area.tag_redraw()
                return {'RUNNING_MODAL'}

            # Handle mouse movement for free positioning
            if self._dragging and event.type == 'MOUSEMOVE' and event.ctrl and event.shift:
                self._mouse_x = event.mouse_region_x
                self._mouse_y = event.mouse_region_y
                
                # Update mouse position for overlay cursor
                scene = context.scene
                scene.lumi_smart_mouse_x = event.mouse_region_x
                scene.lumi_smart_mouse_y = event.mouse_region_y
                
                self.update_free_position(context)
                # # Tetap jalankan modal operator
                return {'RUNNING_MODAL'}

            # Handle mouse release - finish modal operation
            if self._dragging and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self._dragging = False
                # End modal operation when mouse is released
                state = get_state()
                if state:
                    state.set_modal_state('free_pressing', False)
                    state.set_modal_state('free', False)
                
                # Reset positioning mode untuk konsistensi dengan cancel
                if hasattr(context.scene, 'light_props'):
                    context.scene.light_props.positioning_mode = 'DISABLE'
                
                self.cleanup(context)
                self.report({'INFO'}, 'Free positioning completed')
                return {'FINISHED'}

            # Check if Ctrl+Shift keys are released - cancel positioning
            if (event.type == 'LEFTCTRL' or event.type == 'RIGHTCTRL' or event.type == 'LEFTSHIFT' or event.type == 'RIGHTSHIFT') and event.value == 'RELEASE':
                # Check if we still have the required modifier keys
                if not (event.ctrl and event.shift):
                    return self.cancel(context)

            return {'PASS_THROUGH'}

        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Free positioning")

    def update_free_position(self, context):
        """Update light position based on free 2D positioning without depth"""
        region = context.region
        rv3d = context.region_data
        coord = Vector((self._mouse_x, self._mouse_y))

        # Get viewport direction and origin
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        
        selected_objects = context.selected_objects
        
        for light in selected_objects:
            if light.type != 'LIGHT':
                continue

            try:
                # Get current pivot position or create initial position
                current_pivot = lumi_get_light_pivot(light)
                if current_pivot is None:
                    # If no pivot exists, create one at a reasonable distance in front of the light
                    current_pivot = light.location + Vector((0, 0, -2))
                
                # Project current pivot to screen coordinates
                pivot_screen = view3d_utils.location_3d_to_region_2d(region, rv3d, current_pivot)
                
                if pivot_screen is not None:
                    # Calculate screen space movement
                    screen_delta = coord - pivot_screen
                    
                    # Convert screen movement to world movement
                    # Get right and up vectors of the viewport
                    view_right = view3d_utils.region_2d_to_vector_3d(region, rv3d, (coord.x + 1, coord.y)) - view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
                    view_up = view3d_utils.region_2d_to_vector_3d(region, rv3d, (coord.x, coord.y + 1)) - view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
                    
                    # Normalize vectors
                    if view_right.length > 0:
                        view_right.normalize()
                    if view_up.length > 0:
                        view_up.normalize()
                    
                    # Calculate world movement based on screen movement
                    # Scale factor to make movement feel natural
                    scale_factor = 0.01
                    world_movement = (view_right * screen_delta.x + view_up * screen_delta.y) * scale_factor
                    
                    # Apply movement to current pivot position
                    free_position = current_pivot + world_movement
                else:
                    # Fallback: use ray casting at fixed distance if projection fails
                    distance = 5.0
                    free_position = ray_origin + view_vector * distance

                # Set pivot to the free position (2D movement without depth)
                lumi_set_light_pivot(light, free_position)

                # Calculate direction from light to pivot and rotate light to face it
                direction_vector = free_position - light.location
                if direction_vector.length > 0.001:
                    to_pivot = direction_vector.normalized()
                    rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                    light.rotation_mode = 'XYZ'
                    light.rotation_euler = rot_quat.to_euler('XYZ')
                    
            except Exception as light_error:
                lumi_handle_positioning_error(self, context, light_error, f"Light {light.name} update")
                continue
    
    def store_initial_positions(self, context):
        """Store initial positions and rotations of lights for cancel restore"""
        self._initial_positions = {}
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        
        # Store initial positions, rotations, and rotation modes for all selected lights
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

    def cancel(self, context):
        """Cancel free positioning and restore initial positions"""
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
            state.set_modal_state('free', False)
            # Clear pressing state when cancel
            if state:
                state.set_modal_state('free_pressing', False)
            
            # Disable overlay handler hanya jika tidak ada smart control aktif
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
                        
            self.report({'INFO'}, "Free positioning cancelled - positions restored")
            super().cleanup(context)
            return {'CANCELLED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
