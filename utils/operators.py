"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
"""
LumiFlow Operator Utilities
Contains specialized utility functions for operators: modal states, smart control, raycast, etc.
"""

# # Import modul utama Blender
import bpy
from mathutils import Vector
from bpy_extras import view3d_utils
from typing import Optional, Tuple, List

# Import common utilities
from .common import lumi_is_addon_enabled, lumi_reset_highlight, lumi_safe_context_override

# Import state management
from ..core.state import get_state


def lumi_start_smart_control_if_needed(context: bpy.types.Context):
    """Start smart control if needed."""
    state = get_state()
    state.scroll_control_enabled = True
    
    def start_operation():
        bpy.ops.lumi.smart_control('INVOKE_DEFAULT')
        pass
        return True
    
    lumi_safe_context_override(context, start_operation)


def lumi_stop_smart_control():
    """Stop smart control."""
    state = get_state()
    state.scroll_control_enabled = False
    pass


def lumi_raycast_at_mouse(context: bpy.types.Context, mouse_pos: tuple[int, int]) -> tuple[bpy.types.Object | None, Vector | None, Vector | None, int | None]:
    """Perform raycast at mouse position."""
    if not lumi_is_addon_enabled():
        return None, None, None, None
        
    # # Coba eksekusi kode dengan error handling
    try:
        region = context.region
        rv3d = context.region_data
        if region is None or rv3d is None:
            return None, None, None, None
            
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse_pos)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse_pos)
        
        result, location, normal, index, obj, matrix = context.scene.ray_cast(
            context.view_layer.depsgraph, ray_origin, view_vector
        )
        
        return (obj, location, normal, index) if result else (None, None, None, None)
    # # Tangani error jika terjadi
    except Exception as e:
        pass
        return None, None, None, None


def lumi_safe_context_override(context: bpy.types.Context, operation_func) -> bool:
    """Safely override context for operations."""
    # # Coba eksekusi kode dengan error handling
    try:
        # Blender 4.x: use temp_override if available
        if hasattr(context, 'temp_override'):
            if context.area and context.area.type == 'VIEW_3D':
                override_context = {
                    'area': context.area,
                    'region': context.region,
                    'space_data': context.space_data
                }
                with context.temp_override(**override_context):
                    return operation_func()
        # Blender 3.6: run directly
        return operation_func()
    # # Tangani error jika terjadi
    except Exception as e:
        pass
        # # Coba eksekusi kode dengan error handling
        try:
            return operation_func()
        # # Tangani error jika terjadi
        except Exception:
            return False


def lumi_disable_all_positioning_ops(scene: bpy.types.Scene):
    """Disable all positioning modal operators."""
    state = get_state()
    state.set_modal_state('highlight', False)
    state.set_modal_state('align', False)
    state.set_modal_state('rotate', False)
    state.set_modal_state('target', False)


def lumi_ray_cast_between_points(
    context: bpy.types.Context, 
    start_point: Vector, 
    end_point: Vector, 
    exclude_objects: Optional[List[bpy.types.Object]] = None
) -> Tuple[bool, Optional[bpy.types.Object], Optional[Vector], float]:
    """
    Lakukan raycast antara dua titik untuk mendeteksi obstruksi.
    
    Args:
        context: Blender context
        start_point: Titik awal raycast (posisi light)
        end_point: Titik akhir raycast (posisi target)
        exclude_objects: Daftar objek yang diabaikan dalam deteksi
    
    Returns:
        Tuple (has_obstruction, hit_object, hit_location, obstruction_distance)
    """
    # Validasi input
    if not isinstance(start_point, Vector):
        print(f"❌ Error: start_point is not Vector: {type(start_point)}")
        return False, None, None, 0.0
    
    if not isinstance(end_point, Vector):
        print(f"❌ Error: end_point is not Vector: {type(end_point)}")
        return False, None, None, 0.0
    
    if exclude_objects is None:
        exclude_objects = []
    
    try:
        # Hitung arah dan jarak
        direction = (end_point - start_point).normalized()
        distance = (end_point - start_point).length
        
        # Tambahkan toleransi kecil untuk menghindari self-intersection
        ray_start = start_point + direction * 0.001
        ray_distance = distance - 0.002
        
        if ray_distance <= 0:
            return False, None, None, 0.0
        
        # Lakukan raycast
        result, location, normal, index, obj, matrix = context.scene.ray_cast(
            context.view_layer.depsgraph, ray_start, direction
        )
        
        if result:
            # Validasi location dari raycast
            if not isinstance(location, Vector):
                print(f"❌ Error: raycast location is not Vector: {type(location)}")
                return False, None, None, 0.0
            
            # Hitung jarak ke obstruksi
            obstruction_distance = (location - ray_start).length
            
            # Periksa apakah obstruksi terjadi sebelum mencapai target
            if obstruction_distance < ray_distance:
                # Periksa apakah objek yang terkena bukan objek yang dikecualikan
                if obj not in exclude_objects:
                    return True, obj, location, obstruction_distance
        
        return False, None, None, 0.0
        
    except Exception as e:
        print(f"❌ Error in lumi_ray_cast_between_points: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None, 0.0


def lumi_check_line_of_sight_with_sampling(
    context: bpy.types.Context,
    light_position: Vector,
    target_position: Vector,
    exclude_objects: Optional[List[bpy.types.Object]] = None,
    sample_radius: float = 0.1,
    sample_count: int = 5
) -> Tuple[bool, List[dict]]:
    """
    Periksa line-of-sight dengan multi-point sampling di sekitar posisi light.
    
    Args:
        context: Blender context
        light_position: Posisi light yang diusulkan
        target_position: Posisi target object
        exclude_objects: Daftar objek yang diabaikan
        sample_radius: Radius sampling di sekitar posisi light
        sample_count: Jumlah titik sampling
    
    Returns:
        Tuple (has_clear_path, sample_results)
    """
    if exclude_objects is None:
        exclude_objects = []
    
    sample_results = []
    clear_paths = 0
    
    # Generate titik sampling dalam pola lingkaran
    import math
    for i in range(sample_count):
        angle = (2 * math.pi * i) / sample_count
        
        # Hitung offset sampling
        offset_x = sample_radius * math.cos(angle)
        offset_y = sample_radius * math.sin(angle)
        
        # Buat titik sampling (dalam bidang XY relatif terhadap arah ke target)
        direction_to_target = (target_position - light_position).normalized()
        
        # Buat basis vektor untuk sampling
        if abs(direction_to_target.z) < 0.9:
            right = direction_to_target.cross(Vector((0, 0, 1))).normalized()
        else:
            right = direction_to_target.cross(Vector((1, 0, 0))).normalized()
        
        up = right.cross(direction_to_target).normalized()
        
        # Hitung posisi sampling
        sample_offset = right * offset_x + up * offset_y
        sample_position = light_position + sample_offset
        
        # Lakukan raycast dari titik sampling
        has_obstruction, hit_obj, hit_loc, distance = lumi_ray_cast_between_points(
            context, sample_position, target_position, exclude_objects
        )
        
        sample_result = {
            'sample_position': sample_position,
            'has_obstruction': has_obstruction,
            'hit_object': hit_obj,
            'hit_location': hit_loc,
            'distance': distance
        }
        
        sample_results.append(sample_result)
        
        if not has_obstruction:
            clear_paths += 1
    
    # Pertimbangkan jalur yang jelas jika setengah atau lebih sampling tidak terhalangi
    has_clear_path = clear_paths >= max(1, sample_count // 2)
    
    return has_clear_path, sample_results


# Export operator-specific utilities (excluding common ones and moved ones)
__all__ = [
    'lumi_start_smart_control_if_needed',
    'lumi_stop_smart_control',
    'lumi_raycast_at_mouse',
    'lumi_ray_cast_between_points',
    'lumi_check_line_of_sight_with_sampling'
]

