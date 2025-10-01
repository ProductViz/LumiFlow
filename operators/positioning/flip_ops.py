# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Light Flip Operations
Quick system for flipping light orientation based on various references.
"""

import bpy
import bmesh
import math
from typing import Optional, List
from mathutils import Vector, Matrix, Euler, Quaternion

from ...utils.common import lumi_is_addon_enabled
from ...utils.light import (
    lumi_get_light_pivot, 
    lumi_set_light_pivot, 
    lumi_update_light_orientation
)
from ...utils.operators import lumi_ray_cast_between_points
from ...core.state import get_state
from ...utils.scene_analysis import (
    classify_objects_by_background,
    get_objects_in_camera_view,
    get_object_thickness_analysis
)



class LUMI_OT_flip_to_camera_front(bpy.types.Operator):
    """Position light behind target facing camera"""
    bl_idname = "lumiflow.flip_to_camera_front"
    bl_label = "Flip to Camera Front"
    bl_description = "Position light behind target facing camera"
    bl_options = {'REGISTER', 'UNDO'}
   
    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))

    def execute(self, context):
        try:
            # Get active camera
            camera = context.scene.camera
            if not camera:
                self.report({'WARNING'}, "No active camera found")
                return {'CANCELLED'}

            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            flipped_count = 0
            for light in lights:
                # Get pivot/target point for this light menggunakan central system
                pivot_point = lumi_get_light_pivot(light)

                # Position light behind target facing camera
                # Method ini akan return early jika tidak ada target ditemukan
                old_location = light.location.copy()
                self.position_light_behind_target(light, camera, pivot_point, context)
                
                # Cek apakah light benar-benar dipindahkan
                if light.location != old_location:
                    flipped_count += 1

            if flipped_count > 0:
                self.report({'INFO'}, f"Positioned {flipped_count} lights behind target facing camera")
            else:
                self.report({'WARNING'}, "No lights positioned - no targets found on camera Z axis")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error in flip to camera front: {str(e)}")
            return {'CANCELLED'}

    def position_light_behind_target(self, light, camera, pivot_point, context):
        """Position light behind target facing camera (legacy method for flip_to_camera_front)"""
        # Use shared function with face_background=False (facing target)
        return position_light_on_camera_z_axis(light, camera, pivot_point, context, face_background=False)

# =============================================================================
# FUNGSI BERSAMA UNTUK FLIP OPERATIONS
# =============================================================================

def get_target_objects_for_light(context, light):
    """Get target objects for light filtering"""
    try:
        candidates = [obj for obj in context.selected_objects if obj.type != 'LIGHT']
        
        # If no selected objects, get objects in camera view or all scene objects
        if not candidates:
            candidates = _get_fallback_candidates(context)
            if not candidates:
                return []
        
        # SIMPLIFIED APPROACH: Use candidates directly with optional background filtering
        # Only try background classification if we have a reasonable number of objects
        if len(candidates) <= 20:  # Avoid expensive analysis on large scenes
            try:
                camera = context.scene.camera
                if camera:
                    camera_position = camera.location
                    camera_direction = (camera.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()
                    
                    classified_objects = classify_objects_by_background(
                        context, candidates, camera
                    )
                    
                    target_objects = classified_objects.target_objects
                    background_objects = classified_objects.background_objects
                    
                    # FALLBACK: If classification returned no targets, use all candidates
                    if not target_objects:
                        target_objects = candidates

                    return target_objects
                else:
                    # No camera found, use all candidates
                    return candidates

            except Exception as e:
                # Fallback: treat all candidates as targets
                return candidates
        else:
            # For large scenes, skip expensive analysis and use all candidates
            return candidates
            
    except Exception as e:
        # Final fallback: selected non-light objects
        return [obj for obj in context.selected_objects if obj.type != 'LIGHT']

def _get_fallback_candidates(context):
    """Get fallback candidate objects when none are selected"""
    # Try objects in camera view first
    try:
        view_objects = get_objects_in_camera_view(context)
        if view_objects:
            return view_objects
    except Exception as e:
        pass
    
    # Fallback to all non-light objects in scene
    return all_objects

def find_target_on_camera_z_axis(camera, camera_forward_normalized, context):
    """Find target object on camera Z axis"""
    if not isinstance(camera_forward_normalized, Vector):
        return None, None

    # Get target objects for background filter
    target_objects = get_target_objects_for_light(context, None)

    if not target_objects:
        return None, None

    # Raycast along camera Z axis with sufficient distance
    ray_start = camera.location
    ray_end = camera.location + camera_forward_normalized * 1000.0  # 1000 units is sufficient distance
    
    # Perform raycast to find objects on camera Z axis
    try:
        has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
            context, ray_start, ray_end, exclude_objects=[]
        )
    except Exception as e:
        return None, None
    
    # Iterative raycast to pass through background objects
    current_start = ray_start
    max_iterations = 10
    
    for iteration in range(max_iterations):
        if not has_obstruction or not hit_location:
            # No more objects blocking
            break

        # Validate hit_location
        if not isinstance(hit_location, Vector):
            break

        if hit_object in target_objects:
            # Found target object!
            return hit_location, hit_object
        else:
            # Hit background object, continue raycast from this point
            # Continue raycast from slightly after hit point
            offset = 0.01
            try:
                current_start = hit_location + camera_forward_normalized * offset
            except Exception as e:
                break

            # Perform raycast again
            try:
                has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
                    context, current_start, ray_end, exclude_objects=[]
                )
            except Exception as e:
                break
    
    # FALLBACK: If no target object found on camera Z axis, use first object from target_objects
    if target_objects:
        fallback_target = target_objects[0]
        fallback_location = fallback_target.location
        return fallback_location, fallback_target

    # FINAL FALLBACK: If no target_objects at all, find any visible object
    all_visible_objects = [obj for obj in context.scene.objects if obj.visible_get() and obj.type != 'LIGHT']
    if all_visible_objects:
        final_fallback = all_visible_objects[0]
        final_location = final_fallback.location
        return final_location, final_fallback

    # Really no objects at all
    return None, None

def adjust_pivot_with_raycast(light, context, light_position, original_pivot):
    """Adjust pivot with raycast for background lighting
    
    Args:
        light: Light object
        context: Blender context
        light_position: Current light position
        original_pivot: Original pivot point
    """
    # STEP 1: Determine raycast direction (toward background)
    light_direction = (light_position - original_pivot).normalized()
    ray_distance = (light_position - original_pivot).length
    ray_end = light_position + light_direction * (ray_distance * 2.0)

    # STEP 2: Perform raycast
    has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
        context, light_position, ray_end, exclude_objects=[light]
    )

    # STEP 3: Handle raycast result
    if has_obstruction and hit_location:
        # Update pivot to hit mesh location in background direction
        lumi_set_light_pivot(light, hit_location)

        # Re-orient light to face new pivot (consistent with system)
        direction_to_pivot = (hit_location - light_position).normalized()
        rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()
    else:
        # IF NO SURFACE FOUND, SET PIVOT TO DEFAULT VALUE
        # Place pivot in front of light in background direction with default distance
        default_distance = 2.0
        default_pivot_position = light_position + light_direction * default_distance
        lumi_set_light_pivot(light, default_pivot_position)

        # Re-orient light to face default pivot (consistent with system)
        direction_to_pivot = (default_pivot_position - light_position).normalized()
        rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()

def position_light_on_camera_z_axis(light, camera, pivot_point, context, face_background=False):
    """Shared function to position light on camera Z axis
    
    Args:
        light: Light object to position
        camera: Active camera as reference
        pivot_point: Initial pivot/target point
        context: Blender context
        face_background: If True, light faces background; if False, faces target
    
    Returns:
        bool: True if operation successful, False if failed
    """
    
    # STEP 1: Get camera forward direction (actual camera Z axis)
    try:
        camera_forward = camera.matrix_world.to_3x3() @ Vector((0, 0, -1))
        camera_forward_normalized = camera_forward.normalized()
    except Exception as e:
        return False
    
    # STEP 2: DETECT TARGET ON CAMERA Z AXIS
    # Raycast from camera along camera Z axis to find target
    target_location, target_object_from_ray = find_target_on_camera_z_axis(camera, camera_forward_normalized, context)
    
    if target_location is None:
        return False

    if not isinstance(target_location, Vector):
        return False
    
    # STEP 3: ANALISIS KETEBALAN OBJEK
    target_object = target_object_from_ray
    back_surface_location = None
    front_surface_location = None
    obj_thickness = 0
    
    if target_object:
        try:
            # Dapatkan data ketebalan (front & back surface)
            thickness_analysis = get_object_thickness_analysis(context, [target_object])

            if thickness_analysis['thickness_data'] and target_object.name in thickness_analysis['thickness_data']:
                thickness_data = thickness_analysis['thickness_data'][target_object.name]
                obj_thickness = thickness_data['average_thickness']
                back_surface_location = thickness_data.get('back_surface_location')
                front_surface_location = thickness_data.get('front_surface_location')

        except Exception as e:
            pass
    
    # STEP 4: TENTUKAN TITIK REFERENSI & POSISI LIGHT
    try:
        # Gunakan back surface sebagai titik referensi, fallback ke target location
        reference_point = back_surface_location if back_surface_location else target_location
        light_distance = 0.5  # 0.5m di belakang referensi

        # Hitung posisi light: reference_point + 0.5m menjauhi kamera
        light_position = reference_point + (camera_forward_normalized * light_distance)
    except Exception as e:
        return
    
    # STEP 5: Update posisi light
    light.location = light_position

    # STEP 6: Set pivot ke reference point (back surface)
    try:
        # Gunakan reference point yang sama dengan light placement
        pivot_location = reference_point

        lumi_set_light_pivot(light, pivot_location)
    except Exception as e:
        pass
    
    # STEP 7: Orientasikan light berdasarkan mode
    try:
        # Selalu hitung direction dari light ke pivot point untuk konsistensi
        direction_to_pivot = (pivot_location - light.location).normalized()
        if direction_to_pivot.length > 0.001:  # Avoid zero-length vectors
            rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
            light.rotation_euler = rot_quat.to_euler()
    except Exception as e:
        pass
    
    # STEP 8: Update scene agar matrix world ter-refresh
    context.view_layer.update()
    
    # STEP 9: Lakukan pivot adjustment dengan raycast (hanya untuk face_background=True)
    if face_background:
        try:
            pivot_location = adjust_pivot_with_raycast(light, context, light.location, pivot_location)
        except Exception as e:
            pass

    return True

class LUMI_OT_flip_to_camera_back(bpy.types.Operator):
    """Position light at same position and distance as camera"""
    bl_idname = "lumiflow.flip_to_camera_back"
    bl_label = "Flip to Camera Back"
    bl_description = "Position light at same position and distance as camera (co-located)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))

    def execute(self, context):
        try:
            # Get active camera
            camera = context.scene.camera
            if not camera:
                self.report({'WARNING'}, "No active camera found")
                return {'CANCELLED'}

            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            flipped_count = 0
            for light in lights:
                # Get pivot/target point for this light
                pivot_point = lumi_get_light_pivot(light)

                # Position light co-located with camera
                self.position_light_with_camera(light, camera, pivot_point, context)
                flipped_count += 1

            self.report({'INFO'}, f"Co-located {flipped_count} lights with camera")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error in flip to camera back: {str(e)}")
            return {'CANCELLED'}

    def position_light_with_camera(self, light, camera, pivot_point, context):
        """Position light at same position and distance as camera"""
        # Get camera distance from pivot
        camera_distance = (camera.location - pivot_point).length

        # Get camera direction from pivot
        camera_direction = (camera.location - pivot_point).normalized()

        # Position light at same distance and direction as camera
        light.location = pivot_point + (camera_direction * camera_distance)

        # Make light face the pivot (same direction as camera)
        direction_to_pivot = (pivot_point - light.location).normalized()
        rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()
        
        # TAHAP AKHIR: ATUR ULANG PIVOT KE PERMUKAAN PERTAMA YANG TERKENA RAYCAST
        # Cast ray dari light menuju pivot untuk mendeteksi permukaan pertama
        ray_end = light.location + direction_to_pivot * (camera_distance * 2.0)
        
        has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
            context, light.location, ray_end, exclude_objects=[light]
        )
        
        # Set pivot to first surface location hit by raycast
        if has_obstruction and hit_location:
            lumi_set_light_pivot(light, hit_location)
        
        # IMPORTANT: Don't re-orient light! Light must remain co-located with camera
        # Light continues to face the same direction as camera
        
        # Update scene
        context.view_layer.update()

class LUMI_OT_flip_to_camera_along(bpy.types.Operator):
    """Position light same as camera front but facing background (background lighting)"""
    bl_idname = "lumiflow.flip_to_camera_along"
    bl_label = "Flip to Camera Along"
    bl_description = "Position light between target and background but facing background for rim/background lighting"
    bl_options = {'REGISTER', 'UNDO'}

    # BACKGROUND INTEGRATION NOTE:
    # This operator positions light at the SAME POSITION as camera front
    # BUT light faces BACKGROUND (not target)
    # - Position: SAME as camera front (between target and background)
    # - Light faces: BACKGROUND (background/rim lighting)
    # - Integration point: Detect background to illuminate it from target side
    # - Use case: Rim lighting, background illumination, separation lighting

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))

    def execute(self, context):
        try:
            # Get active camera
            camera = context.scene.camera
            if not camera:
                self.report({'WARNING'}, "No active camera found")
                return {'CANCELLED'}

            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            flipped_count = 0
            for light in lights:
                # Get pivot/target point for this light menggunakan central system
                pivot_point = lumi_get_light_pivot(light)

                # Position light same as camera front but facing background
                # Use shared function with face_background=True (facing background)
                old_location = light.location.copy()
                
                success = position_light_on_camera_z_axis(light, camera, pivot_point, context, face_background=True)
                
                # Increment flipped_count if operation successful
                if success:
                    flipped_count += 1

            if flipped_count > 0:
                self.report({'INFO'}, f"Positioned {flipped_count} lights for background lighting")
            else:
                self.report({'WARNING'}, "No lights positioned - no targets found on camera Z axis")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error in flip to camera along: {str(e)}")
            return {'CANCELLED'}

    def position_light_for_background_lighting(self, light, camera, pivot_point, context):
        """Position light same as camera front but facing background for rim lighting (legacy method)"""
        # Gunakan fungsi bersama dengan face_background=True (menghadap ke background)
        return position_light_on_camera_z_axis(light, camera, pivot_point, context, face_background=True)

class LUMI_OT_flip_across_pivot(bpy.types.Operator):
    """Flip light across pivot/target object"""
    bl_idname = "lumiflow.flip_across_pivot"
    bl_label = "Flip Across Pivot"
    bl_description = "Flip light to opposite side relative to target object or scene center"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))

    def execute(self, context):
        try:
            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            # Find pivot point (target object or scene center)
            pivot_point = self.find_pivot_point(context)

            flipped_count = 0
            for light in lights:
                # Calculate vector from pivot to light
                to_light = light.location - pivot_point

                # Flip to opposite side (mirror across pivot)
                new_position = pivot_point - to_light
                light.location = new_position

                # Make light face the pivot
                direction_to_pivot = (pivot_point - new_position).normalized()
                light.rotation_euler = direction_to_pivot.to_track_quat('-Z', 'Y').to_euler()
                
                # FINAL STEP: RESET PIVOT TO HIT MESH
                # Cast ray from light toward pivot to detect hit mesh
                current_distance = (new_position - pivot_point).length
                ray_end = new_position + direction_to_pivot * (current_distance * 2.0)
                
                # Get target objects for background filter
                target_objects = self.get_target_objects_for_light(context, light)
                
                has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
                    context, new_position, ray_end, exclude_objects=[light]
                )
                
                if has_obstruction and hit_location and hit_object in target_objects:
                    # Update pivot to hit mesh location ONLY if object is target
                    lumi_set_light_pivot(light, hit_location)

                    # Re-orient light to face new pivot point
                    direction_to_pivot = (hit_location - new_position).normalized()
                    light.rotation_euler = direction_to_pivot.to_track_quat('-Z', 'Y').to_euler()
                
                # Update scene
                context.view_layer.update()

                flipped_count += 1

            self.report({'INFO'}, f"Flipped {flipped_count} lights across pivot")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error flipping across pivot: {str(e)}")
            return {'CANCELLED'}

    def find_pivot_point(self, context):
        """Find the best pivot point for flipping"""
        # Priority 1: Active object (if not a light)
        if context.active_object and context.active_object.type != 'LIGHT':
            return context.active_object.location.copy()

        # Priority 2: Non-light selected objects
        non_light_objects = [obj for obj in context.selected_objects if obj.type != 'LIGHT']
        if non_light_objects:
            # Filter untuk hanya objek target (bukan background)
            target_objects = self.get_target_objects_from_selection(context, non_light_objects)
            if target_objects:
                # Calculate center of target objects
                total_location = Vector((0, 0, 0))
                for obj in target_objects:
                    total_location += obj.location
                return total_location / len(target_objects)
            else:
                # Jika tidak ada target objects, gunakan semua non-light objects
                total_location = Vector((0, 0, 0))
                for obj in non_light_objects:
                    total_location += obj.location
                return total_location / len(non_light_objects)

        # Priority 3: 3D cursor
        return context.scene.cursor.location.copy()
    
    def get_target_objects_for_light(self, context, light):
        """Get target objects for a specific light using background detection"""
        try:
            # Dapatkan objek yang dipilih sebagai kandidat target
            selected_objects = [obj for obj in context.selected_objects if obj.type != 'LIGHT']
            
            if not selected_objects:
                # Jika tidak ada objek yang dipilih, gunakan semua objek dalam camera view
                view_objects = get_objects_in_camera_view(context)
                return view_objects
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, selected_objects)
            
            # Kembalikan target objects (objek yang bukan background)
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: gunakan semua objek yang dipilih (non-light)
            return [obj for obj in context.selected_objects if obj.type != 'LIGHT']
    
    def get_target_objects_from_selection(self, context, objects):
        """Filter objects to get only target objects (not background)"""
        try:
            if not objects:
                return []
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, objects)
            
            # Kembalikan target objects
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: kembalikan semua objek
            return objects

class LUMI_OT_flip_horizontal(bpy.types.Operator):
    """Flip light horizontally relative to camera view"""
    bl_idname = "lumiflow.flip_horizontal"
    bl_label = "Flip Horizontal"
    bl_description = "Flip light left ↔ right relative to camera view"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))
    
    def get_target_objects_for_light(self, context, light):
        """Get target objects for a specific light using background detection"""
        try:
            # Dapatkan objek yang dipilih sebagai kandidat target
            selected_objects = [obj for obj in context.selected_objects if obj.type != 'LIGHT']
            
            if not selected_objects:
                # Jika tidak ada objek yang dipilih, gunakan semua objek dalam camera view
                view_objects = get_objects_in_camera_view(context)
                return view_objects
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, selected_objects)
            
            # Kembalikan target objects (objek yang bukan background)
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: gunakan semua objek yang dipilih (non-light)
            return [obj for obj in context.selected_objects if obj.type != 'LIGHT']
    
    def get_target_objects_from_selection(self, context, objects):
        """Filter objects to get only target objects (not background)"""
        try:
            if not objects:
                return []
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, objects)
            
            # Kembalikan target objects
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: kembalikan semua objek
            return objects

    def execute(self, context):
        try:
            # Get camera orientation
            camera = context.scene.camera or self.get_view_camera(context)
            if not camera:
                self.report({'WARNING'}, "No camera reference available")
                return {'CANCELLED'}

            # Get camera right vector (X axis in world space)
            camera_matrix = camera.matrix_world
            camera_right = camera_matrix.to_3x3() @ Vector((1, 0, 0))
            camera_location = camera_matrix.translation

            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            flipped_count = 0
            for light in lights:
                # Get pivot/target point for this light (CONSISTENT dengan operator lain)
                pivot_point = lumi_get_light_pivot(light)

                # Perform horizontal flip relative to camera while maintaining pivot relationship
                self.flip_horizontal_around_pivot(light, camera, pivot_point, context)
                flipped_count += 1

            self.report({'INFO'}, f"Flipped {flipped_count} lights horizontally")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error flipping horizontally: {str(e)}")
            return {'CANCELLED'}

    def flip_horizontal_around_pivot(self, light, camera, pivot_point, context):
        """Flip light horizontally relative to camera while maintaining pivot relationship"""

        # STEP 1: Get camera matrix and right vector
        camera_matrix = camera.matrix_world
        camera_right = camera_matrix.to_3x3() @ Vector((1, 0, 0))
        camera_location = camera_matrix.translation

        # STEP 2: Calculate current light position relative to camera coordinate system
        camera_to_light = light.location - camera_location

        # STEP 3: Calculate horizontal component relative to camera
        horizontal_distance = camera_to_light.dot(camera_right)
        horizontal_component = camera_right * horizontal_distance

        # STEP 4: Flip horizontal component
        flipped_horizontal = camera_right * (-horizontal_distance)

        # STEP 5: Calculate other components (vertical + depth from camera perspective)
        other_components = camera_to_light - horizontal_component

        # STEP 6: Reconstruct new light position
        new_camera_to_light = other_components + flipped_horizontal
        new_light_position = camera_location + new_camera_to_light

        # STEP 7: Update light position
        light.location = new_light_position

        # STEP 8: CRITICAL - Make light face the pivot (maintain target relationship)
        direction_to_pivot = (pivot_point - light.location).normalized()
        rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()
        
        # Update scene
        context.view_layer.update()
        
        # TAHAP AKHIR: ATUR ULANG PIVOT KE PERMUKAAN PERTAMA YANG TERKENA RAYCAST
        # Cast ray dari light menuju pivot untuk mendeteksi permukaan pertama
        direction_to_pivot = (pivot_point - light.location).normalized()
        ray_distance = (light.location - pivot_point).length
        ray_end = light.location + direction_to_pivot * (ray_distance * 2.0)  # Perpanjang ray untuk memastikan menabrak
        
        has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
            context, light.location, ray_end, exclude_objects=[light]
        )

        # Set pivot to first surface location hit by raycast
        if has_obstruction and hit_location:
            lumi_set_light_pivot(light, hit_location)

            # Re-orient light to face new pivot (surface)
            new_direction_to_pivot = (hit_location - light.location).normalized()
            rot_quat = new_direction_to_pivot.to_track_quat('-Z', 'Y')
            light.rotation_euler = rot_quat.to_euler()
        
        # Final scene update
        context.view_layer.update()

        # Horizontal flip completed

    def get_view_camera(self, context):
        """Get camera from current view if no scene camera"""
        if context.region_data.view_perspective == 'CAMERA':
            return context.scene.camera
        # For non-camera views, create temporary camera-like reference
        return None

class LUMI_OT_flip_vertical(bpy.types.Operator):
    """Flip light vertically relative to camera view"""
    bl_idname = "lumiflow.flip_vertical"
    bl_label = "Flip Vertical"
    bl_description = "Flip light top ↔ bottom relative to camera view"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))
    
    def get_target_objects_for_light(self, context, light):
        """Get target objects for a specific light using background detection"""
        try:
            # Dapatkan objek yang dipilih sebagai kandidat target
            selected_objects = [obj for obj in context.selected_objects if obj.type != 'LIGHT']
            
            if not selected_objects:
                # Jika tidak ada objek yang dipilih, gunakan semua objek dalam camera view
                view_objects = get_objects_in_camera_view(context)
                return view_objects
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, selected_objects)
            
            # Kembalikan target objects (objek yang bukan background)
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: gunakan semua objek yang dipilih (non-light)
            return [obj for obj in context.selected_objects if obj.type != 'LIGHT']
    
    def get_target_objects_from_selection(self, context, objects):
        """Filter objects to get only target objects (not background)"""
        try:
            if not objects:
                return []
            
            # Klasifikasikan objek berdasarkan background
            analysis_result = classify_objects_by_background(context, objects)
            
            # Kembalikan target objects
            return analysis_result.target_objects
            
        except Exception as e:
            print(f"⚠️ Error in background detection: {e}")
            # Fallback: kembalikan semua objek
            return objects

    def execute(self, context):
        try:
            # Get camera orientation
            camera = context.scene.camera or self.get_view_camera(context)
            if not camera:
                self.report({'WARNING'}, "No camera reference available")
                return {'CANCELLED'}

            # Get selected lights
            lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

            if not lights:
                self.report({'WARNING'}, "No lights selected")
                return {'CANCELLED'}

            flipped_count = 0
            for light in lights:
                # Get pivot/target point for this light (CONSISTENT dengan operator lain)
                pivot_point = lumi_get_light_pivot(light)

                # Perform vertical flip relative to camera while maintaining pivot relationship
                self.flip_vertical_around_pivot(light, camera, pivot_point, context)
                flipped_count += 1

            self.report({'INFO'}, f"Flipped {flipped_count} lights vertically")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error flipping vertically: {str(e)}")
            return {'CANCELLED'}

    def flip_vertical_around_pivot(self, light, camera, pivot_point, context):
        """Flip light vertically relative to camera while maintaining pivot relationship"""

        # STEP 1: Get camera matrix and up vector
        camera_matrix = camera.matrix_world
        camera_up = camera_matrix.to_3x3() @ Vector((0, 1, 0))
        camera_location = camera_matrix.translation

        # STEP 2: Calculate current light position relative to camera coordinate system
        camera_to_light = light.location - camera_location

        # STEP 3: Calculate vertical component relative to camera
        vertical_distance = camera_to_light.dot(camera_up)
        vertical_component = camera_up * vertical_distance

        # STEP 4: Flip vertical component
        flipped_vertical = camera_up * (-vertical_distance)

        # STEP 5: Calculate other components (horizontal + depth from camera perspective)
        other_components = camera_to_light - vertical_component

        # STEP 6: Reconstruct new light position
        new_camera_to_light = other_components + flipped_vertical
        new_light_position = camera_location + new_camera_to_light

        # STEP 7: Update light position
        light.location = new_light_position

        # STEP 8: CRITICAL - Make light face the pivot (maintain target relationship)
        direction_to_pivot = (pivot_point - light.location).normalized()
        rot_quat = direction_to_pivot.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()
        
        # Update scene
        context.view_layer.update()
        
        # TAHAP AKHIR: ATUR ULANG PIVOT KE PERMUKAAN PERTAMA YANG TERKENA RAYCAST
        # Cast ray dari light menuju pivot untuk mendeteksi permukaan pertama
        direction_to_pivot = (pivot_point - light.location).normalized()
        ray_distance = (light.location - pivot_point).length
        ray_end = light.location + direction_to_pivot * (ray_distance * 2.0)  # Perpanjang ray untuk memastikan menabrak
        
        has_obstruction, hit_object, hit_location, distance = lumi_ray_cast_between_points(
            context, light.location, ray_end, exclude_objects=[light]
        )

        # Set pivot to first surface location hit by raycast
        if has_obstruction and hit_location:
            lumi_set_light_pivot(light, hit_location)

            # Re-orient light to face new pivot (surface)
            new_direction_to_pivot = (hit_location - light.location).normalized()
            rot_quat = new_direction_to_pivot.to_track_quat('-Z', 'Y')
            light.rotation_euler = rot_quat.to_euler()
        
        # Final scene update
        context.view_layer.update()

        # Vertical flip completed

    def get_view_camera(self, context):
        """Get camera from current view if no scene camera"""
        if context.region_data.view_perspective == 'CAMERA':
            return context.scene.camera
        # For non-camera views, create temporary camera-like reference
        return None

class LUMI_OT_flip_180_degrees(bpy.types.Operator):
    """Flip light 180° around world Z axis at pivot point"""
    bl_idname = "lumiflow.flip_180_degrees"
    bl_label = "Flip 180 Degrees"
    bl_description = "Rotate light 180° around world Z axis at pivot point"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if operator can run"""
        return (lumi_is_addon_enabled() and 
                context.active_object and 
                context.active_object.type == 'LIGHT')

    def execute(self, context):
        """Execute flip 180° operation"""
        try:
            light = context.active_object
            
            # Get current pivot point using LumiFlow system
            pivot_point = lumi_get_light_pivot(light)
            
            if pivot_point is None:
                self.report({'WARNING'}, "No pivot point found. Using scene center.")
                pivot_point = Vector((0, 0, 0))
            
            # Perform the 180° flip
            self.flip_180_around_pivot(light, pivot_point)
            
            # Pivot tetap di lokasi asli - tidak dipindahkan
            
            self.report({'INFO'}, "Light flipped 180° around pivot")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Flip 180° failed: {str(e)}")
            return {'CANCELLED'}

    def flip_180_around_pivot(self, light, pivot_point):
        """Flip light 180° around world Z axis at pivot point"""
        
        # STEP 1: Calculate vector from pivot to light
        pivot_to_light = light.location - pivot_point
        
        # STEP 2: Create rotation matrix for 180° around world Z axis
        # World Z axis rotation matrix (180 degrees)
        cos_180 = -1.0
        sin_180 = 0.0
        
        rotation_matrix = Matrix((
            (cos_180, -sin_180, 0.0),
            (sin_180, cos_180, 0.0),
            (0.0, 0.0, 1.0)
        ))
        
        # STEP 3: Apply rotation to the vector from pivot to light
        rotated_vector = rotation_matrix @ pivot_to_light
        
        # STEP 4: Calculate new position
        new_light_position = pivot_point + rotated_vector
        
        # STEP 5: Update light position
        light.location = new_light_position
        
        # STEP 6: Rotate light orientation 180° around world Z axis
        # Get current rotation as quaternion
        current_rot = light.rotation_euler.to_quaternion()
        
        # Create 180° rotation around world Z axis
        z_180_rot = Quaternion((0.0, 0.0, 1.0), 3.14159)  # 180 degrees in radians
        
        # Apply rotation
        new_rot = z_180_rot @ current_rot
        light.rotation_euler = new_rot.to_euler()
        
        # 180-degree flip completed

# Registration
def register():
    """Register flip operators"""
    bpy.utils.register_class(LUMI_OT_flip_to_camera_front)
    bpy.utils.register_class(LUMI_OT_flip_to_camera_back)
    bpy.utils.register_class(LUMI_OT_flip_to_camera_along)
    bpy.utils.register_class(LUMI_OT_flip_across_pivot)
    bpy.utils.register_class(LUMI_OT_flip_horizontal)
    bpy.utils.register_class(LUMI_OT_flip_vertical)
    bpy.utils.register_class(LUMI_OT_flip_180_degrees)

def unregister():
    """Unregister flip operators"""
    bpy.utils.unregister_class(LUMI_OT_flip_to_camera_front)
    bpy.utils.unregister_class(LUMI_OT_flip_to_camera_back)
    bpy.utils.unregister_class(LUMI_OT_flip_to_camera_along)
    bpy.utils.unregister_class(LUMI_OT_flip_across_pivot)
    bpy.utils.unregister_class(LUMI_OT_flip_horizontal)
    bpy.utils.unregister_class(LUMI_OT_flip_vertical)
    bpy.utils.unregister_class(LUMI_OT_flip_180_degrees)


if __name__ == "__main__":
    register()
