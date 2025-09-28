"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
# Import modul utama Blender
import bpy
import bgl
import gpu
from bpy_extras import view3d_utils
from bpy.types import Operator
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from ...utils import lumi_is_addon_enabled
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

# Definisi class untuk Operator - Refactored for Positioning Mode
class LUMI_OT_highlight_positioning(bpy.types.Operator, BaseModalOperator):
    bl_idname = "lumi.highlight_positioning"
    bl_label = "Highlight Positioning"
    bl_description = "Ctrl + LMB drag: Position light to create highlight based on surface normal"
    bl_options = {'REGISTER', 'UNDO'}

    _dragging = False
    _initial_distances = {}
    _initial_positions = {}  # Store initial light positions for cancel restore
    _mouse_x = 0
    _mouse_y = 0
    _start_mouse = None

    def __del__(self):
        """Clean up stored data when operator is destroyed"""
        try:
            # Only clean up if the object still exists
            if hasattr(self, '_initial_distances'):
                self._initial_distances.clear()
            if hasattr(self, '_initial_positions'):
                # Clear pivot data from each light's initial positions
                for light_name in self._initial_positions:
                    if 'pivot' in self._initial_positions[light_name]:
                        self._initial_positions[light_name]['pivot'] = None
                self._initial_positions.clear()
        except (ReferenceError, AttributeError):
            # Ignore errors when object is being destroyed
            pass

    @classmethod
    def poll(cls, context):
        """Check if operator can run"""
        return lumi_is_valid_positioning_context(context)

    def validate_context(self, context):
        """Validate context for highlight positioning operations"""
        return lumi_is_valid_positioning_context(context)

    def validate_modal_context(self, context, event):
        """Validate context for modal highlight operations"""
        # Event is already passed as parameter, no need to check context.event
        return lumi_is_valid_positioning_context(context, check_event=False, check_mode=False, required_mode=None)

    def invoke(self, context, event):
        """Invoke method - starts modal operator for highlight positioning"""
        try:
            # Reset state to ensure clean operation
            self._dragging = False
            self._initial_distances = {}
            self._initial_positions = {}  # Initialize positions storage
            self._mouse_x = 0
            self._mouse_y = 0
            self._start_mouse = None
            
            # Validate inputs
            if not self.validate_context(context):
                self.report({'ERROR'}, "Invalid context for highlight positioning")
                return {'CANCELLED'}
            
            # Check if this is the correct positioning mode
            detected_mode = detect_positioning_mode(event)
            if detected_mode != 'HIGHLIGHT':
                return {'PASS_THROUGH'}
            
            scene = context.scene
            
            # Disable other positioning operations
            lumi_disable_all_positioning_ops(scene)
            # Set modal state using new state management
            state = get_state()
            state.set_modal_state('highlight', True)
            
            # Keep old properties for backward compatibility
            scene.light_props.positioning_mode = 'HIGHLIGHT'
            scene.light_props.modal_state = 'highlight'
            self.positioning_mode = 'HIGHLIGHT'
            
            # Initialize dragging state IMMEDIATELY (like Orbit & Target modes)
            self._dragging = True
            self._start_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            # Set mouse position for ray cast calculation
            self._mouse_x = event.mouse_region_x
            self._mouse_y = event.mouse_region_y
            self.store_initial_positions(context)
            
            # Add modal handler
            context.window_manager.modal_handler_add(self)
            
            # Enable overlay handler untuk positioning mode
            from ...overlay import lumi_enable_cursor_overlay_handler
            lumi_enable_cursor_overlay_handler()
            
            # Redraw UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            return {'RUNNING_MODAL'}
                
        except Exception as e:
            import traceback
            error_msg = f"Error in highlight positioning operation: {str(e)}"
            self.report({'ERROR'}, error_msg)
            traceback.print_exc()
            return {'CANCELLED'}

    def update_highlight_position(self, context):
        """Update highlight position based on mouse movement"""
        try:
            from bpy_extras import view3d_utils
            from mathutils import Vector
            
            scene = context.scene
            scene_camera = scene.camera
            
            # Validasi kamera aktif
            if not scene_camera or scene_camera.type != 'CAMERA':
                self.report({'WARNING'}, "No active camera found. Using viewport as fallback.")
            
            region = context.region
            rv3d = context.region_data
            coord = Vector((self._mouse_x, self._mouse_y))

            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
            hit, location, normal, *_ = scene.ray_cast(
                context.view_layer.depsgraph, ray_origin, view_vector
            )

            if hit:
                scene_light_distance = scene.light_distance
                
                # Selalu gunakan kamera aktif, bukan viewport
                if scene_camera and scene_camera.type == 'CAMERA':
                    view_origin = scene_camera.location
                    # Gunakan matrix kamera untuk perhitungan yang akurat
                    camera_matrix = scene_camera.matrix_world
                    camera_direction = camera_matrix.to_3x3().col[2].normalized()
                else:
                    # Fallback ke viewport hanya jika tidak ada kamera aktif
                    view_origin = rv3d.view_matrix.inverted().translation
                    camera_direction = rv3d.view_matrix.to_3x3().col[2].normalized()
                
                # Hitung vektor dari lokasi hit ke kamera
                to_camera = (view_origin - location).normalized()
                
                # Hitung refleksi berdasarkan normal surface
                reflected = to_camera - 2 * to_camera.dot(normal) * normal

                # # Ambil objek yang dipilih dalam scene
                selected_lights = [l for l in context.selected_objects if l.type == 'LIGHT']
                
                for light in selected_lights:
                    lumi_set_light_pivot(light, location)
                    distance = self._initial_distances.get(light.name, scene_light_distance)
                    new_location = location - reflected * distance
                    
                    light.location = new_location

                    # Gunakan arah kamera aktif untuk rotasi yang akurat
                    pivot = lumi_get_light_pivot(light)
                    if pivot:
                        to_pivot = (pivot - light.location).normalized()
                        # Untuk highlight, arahkan cahaya ke pivot dengan mempertimbangkan orientasi kamera
                        if scene_camera and scene_camera.type == 'CAMERA':
                            # Gunakan matrix kamera untuk referensi rotasi
                            # to_track_quat hanya menerima string untuk axis kedua
                            rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                        else:
                            # Fallback ke viewport jika tidak ada kamera
                            rot_quat = to_pivot.to_track_quat('-Z', 'Y')
                        
                        light.rotation_mode = 'XYZ'
                        light.rotation_euler = rot_quat.to_euler('XYZ')
                    else:
                        pass
        except Exception as e:
            lumi_handle_positioning_error(self, context, e, "Highlight position update")

    def store_initial_positions(self, context):
        """Store initial positions and distances of lights for highlight positioning"""
        self._initial_distances = {}
        self._initial_positions = {}  # Initialize positions storage
        scene = context.scene
        scene_light_distance = scene.light_distance
        
        selected_lights = [l for l in context.selected_objects if l.type == 'LIGHT']
        
        # Store initial positions, rotations, and pivots for all selected lights
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
                    print(f"❌ Error storing pivot for {light.name}: {e}")
                    self._initial_positions[light.name]['pivot'] = None
        
        # Get initial ray cast from mouse position to calculate actual distances
        region = context.region
        rv3d = context.region_data
        coord = Vector((self._mouse_x, self._mouse_y))
        
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        hit, location, normal, *_ = scene.ray_cast(
            context.view_layer.depsgraph, ray_origin, view_vector
        )
        
        for light in selected_lights:
            if hit:
                # Calculate actual distance from light to pivot (hit location)
                actual_distance = (light.location - location).length
                self._initial_distances[light.name] = actual_distance
            else:
                # Fallback to scene light distance if no hit
                self._initial_distances[light.name] = scene_light_distance
        

    def modal(self, context, event):
        """Modal implementation for highlight positioning - Ctrl + LMB drag"""
        # Validate context first
        if not self.validate_modal_context(context, event):
            return {'CANCELLED'}
        
        try:
            # Check if we're still in the correct positioning mode
            detected_mode = detect_positioning_mode(event)
            
            # If we're already dragging, check if Ctrl is still held
            if self._dragging:
                # Check if Ctrl key is still held (required for highlight positioning)
                if not event.ctrl:
                    return self.cancel(context)
            elif detected_mode != 'HIGHLIGHT':
                return {'PASS_THROUGH'}
            
            # Main event handling logic
            if event.type == 'RIGHTMOUSE' or event.type == 'ESC':
                return self.cancel(context)

            # Allow wheel scrolling to pass through when Ctrl is held
            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'} and event.ctrl:
                return {'PASS_THROUGH'}

            # Handle mouse interactions for highlight positioning
            if event.ctrl and not event.shift and not event.alt:
                
                # Since dragging starts immediately in invoke(), just process mouse movement
                if self._dragging and event.type == 'MOUSEMOVE':
                    self._mouse_x = event.mouse_region_x
                    self._mouse_y = event.mouse_region_y
                    
                    # Update mouse position for overlay cursor
                    scene = context.scene
                    scene.lumi_smart_mouse_x = event.mouse_region_x
                    scene.lumi_smart_mouse_y = event.mouse_region_y
                    
                    self.update_highlight_position(context)
                    return {'RUNNING_MODAL'}

                # Handle mouse release - finish modal operation
                if self._dragging and event.type in {'LEFTMOUSE', 'LEFT_CTRL', 'RIGHT_CTRL'} and event.value == 'RELEASE':
                    self._dragging = False
                    # End modal operation when mouse is released
                    state = get_state()
                    if state:
                        state.set_modal_state('highlight', False)
                    
                    # Reset positioning mode untuk konsistensi dengan cancel
                    if hasattr(context.scene, 'light_props'):
                        context.scene.light_props.positioning_mode = 'DISABLE'
                    
                    self.cleanup(context)
                    self.report({'INFO'}, 'Highlight positioning completed')
                    return {'FINISHED'}

            return {'PASS_THROUGH'}
            
        except Exception as e:
            return lumi_handle_modal_error(self, context, e, "Highlight positioning")

    def cancel(self, context):
        """Cancel highlight positioning and restore initial positions"""
        try:
            self._dragging = False
            self._start_mouse = None
            
            # Restore initial positions, rotations, and pivots for all selected lights
            selected_lights = [l for l in context.selected_objects if l.type == 'LIGHT']
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
            
            # Clean up state
            state = get_state()
            state.set_modal_state('highlight', False)
            
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
                        
            self.report({'INFO'}, "Highlight positioning cancelled - positions restored")
            return {'CANCELLED'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}



