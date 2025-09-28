"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
"""
Scene Analysis
Menganalisis scene untuk deteksi objek, background, dan karakteristik lighting.
"""

import math
import bpy
from mathutils import Vector, Matrix, geometry
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass

# Import utility functions
from .light import lumi_get_viewport_camera_position
from .operators import lumi_ray_cast_between_points


@dataclass
class SceneAnalysisResult:
    """Hasil analisis scene."""
    target_objects: List[bpy.types.Object]
    background_objects: List[bpy.types.Object]
    occluded_objects: List[bpy.types.Object]
    camera_position: Vector
    camera_direction: Vector
    view_frustum_objects: List[bpy.types.Object]
    analysis_metadata: Dict[str, Any]


def get_camera_frustum_planes(context: bpy.types.Context, camera_obj: bpy.types.Object) -> List[Dict[str, Any]]:
    """
    Dapatkan plane-plane frustum kamera untuk deteksi objek dalam view.
    
    Args:
        context: Blender context
        camera_obj: Object kamera
    
    Returns:
        List of plane dictionaries dengan normal dan point
    """
    if not camera_obj or camera_obj.type != 'CAMERA':
        return []
    
    # Dapatkan camera data
    camera_data = camera_obj.data
    scene = context.scene
    
    # Hitung frustum berdasarkan camera type
    if camera_data.type == 'PERSP':
        # Perspective camera
        fov = camera_data.angle
        aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        
        # Camera transform
        cam_matrix = camera_obj.matrix_world
        cam_pos = cam_matrix.translation.to_3d()
        cam_forward = (-cam_matrix.col[2].normalized()).to_3d()
        cam_up = cam_matrix.col[1].normalized().to_3d()
        cam_right = cam_matrix.col[0].normalized().to_3d()
        
        # Hitung frustum planes
        planes = []
        
        # Near plane
        near_distance = camera_data.clip_start
        near_center = cam_pos + cam_forward * near_distance
        planes.append({
            'normal': cam_forward,
            'point': near_center,
            'type': 'near'
        })
        
        # Far plane
        far_distance = camera_data.clip_end
        far_center = cam_pos + cam_forward * far_distance
        planes.append({
            'normal': -cam_forward,
            'point': far_center,
            'type': 'far'
        })
        
        # Left, Right, Top, Bottom planes
        half_fov_h = fov / 2
        half_fov_v = math.atan(math.tan(half_fov_h) / aspect_ratio)
        
        # Left plane
        left_normal = (cam_forward.cross(cam_up)).normalized()
        left_rotation = Matrix.Rotation(half_fov_h, 4, cam_up)
        left_normal = (left_rotation @ left_normal).normalized()
        planes.append({
            'normal': left_normal,
            'point': cam_pos,
            'type': 'left'
        })
        
        # Right plane
        right_normal = (cam_up.cross(cam_forward)).normalized()
        right_rotation = Matrix.Rotation(-half_fov_h, 4, cam_up)
        right_normal = (right_rotation @ right_normal).normalized()
        planes.append({
            'normal': right_normal,
            'point': cam_pos,
            'type': 'right'
        })
        
        # Top plane
        top_normal = (cam_right.cross(cam_forward)).normalized()
        top_rotation = Matrix.Rotation(-half_fov_v, 4, cam_right)
        top_normal = (top_rotation @ top_normal).normalized()
        planes.append({
            'normal': top_normal,
            'point': cam_pos,
            'type': 'top'
        })
        
        # Bottom plane
        bottom_normal = (cam_forward.cross(cam_right)).normalized()
        bottom_rotation = Matrix.Rotation(half_fov_v, 4, cam_right)
        bottom_normal = (bottom_rotation @ bottom_normal).normalized()
        planes.append({
            'normal': bottom_normal,
            'point': cam_pos,
            'type': 'bottom'
        })
        
    else:
        # Orthographic camera
        cam_matrix = camera_obj.matrix_world
        cam_pos = cam_matrix.translation.to_3d()
        cam_forward = (-cam_matrix.col[2].normalized()).to_3d()
        cam_up = cam_matrix.col[1].normalized().to_3d()
        cam_right = cam_matrix.col[0].normalized().to_3d()
        
        ortho_scale = camera_data.ortho_scale
        
        planes = []
        
        # Near plane
        near_distance = camera_data.clip_start
        near_center = cam_pos + cam_forward * near_distance
        planes.append({
            'normal': cam_forward,
            'point': near_center,
            'type': 'near'
        })
        
        # Far plane
        far_distance = camera_data.clip_end
        far_center = cam_pos + cam_forward * far_distance
        planes.append({
            'normal': -cam_forward,
            'point': far_center,
            'type': 'far'
        })
        
        # Left, Right, Top, Bottom planes untuk orthographic
        half_scale = ortho_scale / 2
        
        # Left plane
        left_center = cam_pos - cam_right * half_scale
        planes.append({
            'normal': cam_right,
            'point': left_center,
            'type': 'left'
        })
        
        # Right plane
        right_center = cam_pos + cam_right * half_scale
        planes.append({
            'normal': -cam_right,
            'point': right_center,
            'type': 'right'
        })
        
        # Top plane
        top_center = cam_pos + cam_up * half_scale
        planes.append({
            'normal': -cam_up,
            'point': top_center,
            'type': 'top'
        })
        
        # Bottom plane
        bottom_center = cam_pos - cam_up * half_scale
        planes.append({
            'normal': cam_up,
            'point': bottom_center,
            'type': 'bottom'
        })
    
    return planes


def is_object_in_frustum(obj: bpy.types.Object, frustum_planes: List[Dict[str, Any]]) -> bool:
    """
    Periksa apakah objek berada dalam camera frustum.
    
    Args:
        obj: Object yang diperiksa
        frustum_planes: List of frustum planes
    
    Returns:
        True jika objek dalam frustum, False jika tidak
    """
    if obj.type == 'EMPTY' or obj.hide_get():
        return False
    
    # Dapatkan bounding box object dalam world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Periksa apakah semua corner berada di luar salah satu plane
    for plane in frustum_planes:
        normal = plane['normal']
        point = plane['point']
        
        # Periksa semua corner
        all_outside = True
        for corner in bbox_corners:
            # Hitung jarak dari corner ke plane
            distance = (corner - point).dot(normal)
            if distance >= 0:  # Corner di dalam atau pada plane
                all_outside = False
                break
        
        if all_outside:
            return False  # Objek di luar frustum
    
    return True  # Objek dalam frustum


def get_objects_in_camera_view(context: bpy.types.Context, camera_obj: bpy.types.Object = None) -> List[bpy.types.Object]:
    """
    Dapatkan semua objek yang terlihat dalam camera view.
    
    Args:
        context: Blender context
        camera_obj: Camera object (jika None, gunakan active camera)
    
    Returns:
        List of objects dalam camera view
    """
    if camera_obj is None:
        camera_obj = context.scene.camera
    
    if not camera_obj:
        print("🔍 get_objects_in_camera_view: No camera found")
        return []
    
    print(f"🔍 get_objects_in_camera_view: Using camera '{camera_obj.name}' (type: {camera_obj.data.type if camera_obj.data else 'NONE'})")
    
    # Dapatkan frustum planes
    frustum_planes = get_camera_frustum_planes(context, camera_obj)
    print(f"🔍 get_objects_in_camera_view: Got {len(frustum_planes)} frustum planes")
    
    if not frustum_planes:
        print("🔍 get_objects_in_camera_view: No frustum planes generated")
        return []
    
    # Kumpulkan semua objek dalam frustum
    objects_in_view = []
    total_objects_checked = 0
    
    for obj in context.scene.objects:
        if obj.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
            total_objects_checked += 1
            if is_object_in_frustum(obj, frustum_planes):
                objects_in_view.append(obj)
                print(f"🔍 get_objects_in_camera_view: Object '{obj.name}' is in view")
            else:
                print(f"🔍 get_objects_in_camera_view: Object '{obj.name}' is NOT in view")
    
    print(f"🔍 get_objects_in_camera_view: Checked {total_objects_checked} objects, found {len(objects_in_view)} in view")
    return objects_in_view


def is_object_occluded_from_camera(
    context: bpy.types.Context, 
    obj: bpy.types.Object, 
    camera_obj: bpy.types.Object,
    max_samples: int = 5
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Periksa apakah objek terhalang (occluded) dari view kamera.
    
    Args:
        context: Blender context
        obj: Object yang diperiksa
        camera_obj: Camera object
        max_samples: Jumlah maksimum sampling points
    
    Returns:
        Tuple (is_occluded, occlusion_data)
    """
    camera_pos = camera_obj.matrix_world.translation
    
    # Dapatkan beberapa titik pada objek untuk pengujian
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Pilih titik-titik representatif (kurangi sampling untuk performance)
    if len(bbox_corners) > max_samples:
        # Pilih titik-titik yang paling jauh dari center
        obj_center = obj.matrix_world.translation
        corners_with_distance = [
            (corner, (corner - obj_center).length_squared) 
            for corner in bbox_corners
        ]
        corners_with_distance.sort(key=lambda x: x[1], reverse=True)
        test_points = [corner for corner, _ in corners_with_distance[:max_samples]]
    else:
        test_points = bbox_corners
    
    occlusion_data = []
    occluded_count = 0
    
    for point in test_points:
        # Lakukan raycast dari kamera ke titik objek
        has_obstruction, hit_obj, hit_location, distance = lumi_ray_cast_between_points(
            context, camera_pos, point, exclude_objects=[obj]
        )
        
        occlusion_result = {
            'test_point': point,
            'is_occluded': has_obstruction,
            'hit_object': hit_obj,
            'hit_location': hit_location,
            'distance': distance
        }
        
        occlusion_data.append(occlusion_result)
        
        if has_obstruction:
            occluded_count += 1
    
    # Objek dianggap occluded jika lebih dari 50% test points terhalang
    is_occluded = occluded_count > len(test_points) * 0.5
    
    return is_occluded, occlusion_data


def classify_objects_by_background(
    context: bpy.types.Context, 
    target_objects: List[bpy.types.Object],
    camera_obj: bpy.types.Object = None
) -> SceneAnalysisResult:
    """
    Klasifikasikan objek menjadi target dan background berdasarkan view kamera.
    
    Args:
        context: Blender context
        target_objects: List of target objects yang dianggap sebagai subjek utama
        camera_obj: Camera object (jika None, gunakan active camera)
    
    Returns:
        SceneAnalysisResult dengan klasifikasi objek
    """
    try:
        if camera_obj is None:
            camera_obj = context.scene.camera
        
        if not camera_obj:
            return SceneAnalysisResult(
                target_objects=[],
                background_objects=[],
                occluded_objects=[],
                camera_position=Vector(),
                camera_direction=Vector(),
                view_frustum_objects=[],
                analysis_metadata={'error': 'No camera found'}
            )
        
        # Dapatkan posisi dan arah kamera
        camera_position = camera_obj.matrix_world.translation
        camera_direction = -camera_obj.matrix_world.col[2].normalized()
        
        # Validasi Vector
        if not isinstance(camera_position, Vector):
            print(f"❌ Error: camera_position is not Vector: {type(camera_position)}")
            camera_position = Vector()
            
        if not isinstance(camera_direction, Vector):
            print(f"❌ Error: camera_direction is not Vector: {type(camera_direction)}")
            camera_direction = Vector((0, 0, -1))
        
        # Dapatkan semua objek dalam camera view
        view_frustum_objects = get_objects_in_camera_view(context, camera_obj)
        
        # Klasifikasikan objek
        classified_targets = []
        classified_background = []
        occluded_objects = []
        
        for obj in view_frustum_objects:
            if obj in target_objects:
                # Periksa apakah target object terhalang
                try:
                    is_occluded, _ = is_object_occluded_from_camera(context, obj, camera_obj)
                    
                    if is_occluded:
                        occluded_objects.append(obj)
                    else:
                        classified_targets.append(obj)
                except Exception as e:
                    print(f"❌ Error checking occlusion for {obj.name}: {e}")
                    # Anggap tidak terhalang jika ada error
                    classified_targets.append(obj)
            else:
                # Objek lain dianggap background
                classified_background.append(obj)
        
        # Tambahkan target objects yang tidak dalam view ke occluded
        for obj in target_objects:
            if obj not in view_frustum_objects and obj not in occluded_objects:
                occluded_objects.append(obj)
        
        # Buat metadata analisis
        analysis_metadata = {
            'total_objects_in_view': len(view_frustum_objects),
            'target_objects_count': len(classified_targets),
            'background_objects_count': len(classified_background),
            'occluded_objects_count': len(occluded_objects),
            'camera_type': camera_obj.data.type if camera_obj.data else 'UNKNOWN',
            'analysis_timestamp': context.scene.frame_current
        }
        
        return SceneAnalysisResult(
            target_objects=classified_targets,
            background_objects=classified_background,
            occluded_objects=occluded_objects,
            camera_position=camera_position,
            camera_direction=camera_direction,
            view_frustum_objects=view_frustum_objects,
            analysis_metadata=analysis_metadata
        )
        
    except Exception as e:
        print(f"❌ Error in classify_objects_by_background: {e}")
        import traceback
        traceback.print_exc()
        # Return empty result on error
        return SceneAnalysisResult(
            target_objects=[],
            background_objects=[],
            occluded_objects=[],
            camera_position=Vector(),
            camera_direction=Vector(),
            view_frustum_objects=[],
            analysis_metadata={'error': str(e)}
        )


def get_background_distance_analysis(
    context: bpy.types.Context,
    background_objects: List[bpy.types.Object],
    camera_obj: bpy.types.Object = None
) -> Dict[str, Any]:
    """
    Analisis jarak background objects dari kamera.
    
    Args:
        context: Blender context
        background_objects: List of background objects
        camera_obj: Camera object
    
    Returns:
        Dictionary dengan analisis jarak background
    """
    if camera_obj is None:
        camera_obj = context.scene.camera
    
    if not camera_obj:
        return {}
    
    camera_pos = camera_obj.matrix_world.translation
    
    distance_analysis = {
        'nearest_background': None,
        'farthest_background': None,
        'average_distance': 0.0,
        'distance_groups': {
            'near': [],      # 0-10 units
            'medium': [],    # 10-50 units  
            'far': [],       # 50+ units
            'very_far': []   # 100+ units
        }
    }
    
    if not background_objects:
        return distance_analysis
    
    distances = []
    
    for obj in background_objects:
        obj_center = obj.matrix_world.translation
        distance = (obj_center - camera_pos).length
        distances.append(distance)
        
        # Klasifikasikan berdasarkan jarak
        if distance <= 10:
            distance_analysis['distance_groups']['near'].append(obj.name)
        elif distance <= 50:
            distance_analysis['distance_groups']['medium'].append(obj.name)
        elif distance <= 100:
            distance_analysis['distance_groups']['far'].append(obj.name)
        else:
            distance_analysis['distance_groups']['very_far'].append(obj.name)
    
    if distances:
        distance_analysis['nearest_background'] = min(distances)
        distance_analysis['farthest_background'] = max(distances)
        distance_analysis['average_distance'] = sum(distances) / len(distances)
    
    return distance_analysis


def create_background_selection_set(
    context: bpy.types.Context,
    background_objects: List[bpy.types.Object],
    set_name: str = "LumiFlow_Background_Objects"
) -> bpy.types.Collection:
    """
    Buat collection khusus untuk background objects.
    
    Args:
        context: Blender context
        background_objects: List of background objects
        set_name: Nama collection yang akan dibuat
    
    Returns:
        Collection yang berisi background objects
    """
    # Hapus collection jika sudah ada
    if set_name in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections[set_name])
    
    # Buat collection baru
    background_collection = bpy.data.collections.new(set_name)
    context.scene.collection.children.link(background_collection)
    
    # Tambahkan background objects ke collection
    for obj in background_objects:
        if obj not in background_collection.objects:
            background_collection.objects.link(obj)
    
    return background_collection


def analyze_background_for_lighting(
    context: bpy.types.Context,
    target_objects: List[bpy.types.Object],
    camera_obj: bpy.types.Object = None
) -> Dict[str, Any]:
    """
    Analisis background untuk keperluan lighting setup.
    
    Args:
        context: Blender context
        target_objects: List of target objects
        camera_obj: Camera object
    
    Returns:
        Dictionary lengkap dengan analisis background untuk lighting
    """
    # Klasifikasikan objek
    analysis_result = classify_objects_by_background(context, target_objects, camera_obj)
    
    # Analisis jarak background
    distance_analysis = get_background_distance_analysis(
        context, analysis_result.background_objects, camera_obj
    )
    
    # Buat lighting recommendations
    lighting_recommendations = {
        'background_lighting_needed': len(analysis_result.background_objects) > 0,
        'background_separation_good': False,
        'rim_lighting_recommended': False,
        'fill_lighting_recommended': False,
        'key_lighting_recommendations': []
    }
    
    # Analisis untuk lighting recommendations
    if analysis_result.background_objects:
        nearest_bg_distance = distance_analysis.get('nearest_background', float('inf'))
        
        # Rekomendasi berdasarkan jarak background
        if nearest_bg_distance > 20:
            lighting_recommendations['background_separation_good'] = True
            lighting_recommendations['rim_lighting_recommended'] = True
        elif nearest_bg_distance > 5:
            lighting_recommendations['fill_lighting_recommended'] = True
        else:
            # Background terlalu dekat, perlu careful lighting
            lighting_recommendations['key_lighting_recommendations'].append(
                "Gunakan lighting yang precise untuk memisahkan target dari background"
            )
    
    # Gabungkan semua hasil analisis
    complete_analysis = {
        'background_classification': analysis_result,
        'distance_analysis': distance_analysis,
        'lighting_recommendations': lighting_recommendations,
        'summary': {
            'total_objects_analyzed': len(analysis_result.view_frustum_objects),
            'visible_targets': len(analysis_result.target_objects),
            'visible_background': len(analysis_result.background_objects),
            'occluded_targets': len(analysis_result.occluded_objects)
        }
    }
    
    return complete_analysis


def get_object_thickness_analysis(
    context: bpy.types.Context,
    target_objects: List[bpy.types.Object],
    camera_obj: bpy.types.Object = None,
    sample_points: int = 2  # Dikurangi lagi karena fokus pada sumbu Z saja
) -> Dict[str, Any]:
    """
    Analisis ketebalan objek target menggunakan raycast sampling di sumbu Z kamera.
    Sampling fokus pada sumbu Z kamera karena light ditempatkan di posisi ini.
    
    Args:
        context: Blender context
        target_objects: List of target objects yang akan dianalisis
        camera_obj: Camera object (jika None, gunakan active camera)
        sample_points: Jumlah sampling points per objek di sepanjang sumbu Z kamera
    
    Returns:
        Dictionary dengan analisis ketebalan untuk setiap objek target
    """
    thickness_analysis = {
        'objects_analyzed': 0,
        'thickness_data': {},
        'average_thickness': 0.0,
        'max_thickness': 0.0,
        'min_thickness': float('inf'),
        'camera_position': None,
        'analysis_method': 'camera_z_axis_sampling'
    }
    
    try:
        # Dapatkan kamera
        if camera_obj is None:
            camera_obj = context.scene.camera
        
        if not camera_obj or camera_obj.type != 'CAMERA':
            # No valid camera found for thickness analysis
            return thickness_analysis
        
        camera_position = camera_obj.location
        thickness_analysis['camera_position'] = camera_position
        
        total_thickness = 0.0
        valid_objects = 0
        
        for obj in target_objects:
            if obj.type != 'MESH':
                # Skipping non-mesh object
                continue
            
            # Analyzing thickness for object
            
            # Dapatkan bounding box objek dalam world coordinates
            bbox_world = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            
            # Hitung center objek
            obj_center = sum(bbox_world, Vector()) / 8.0
            
            # Dapatkan dimensi bounding box
            bbox_dimensions = {
                'x': max(corner.x for corner in bbox_world) - min(corner.x for corner in bbox_world),
                'y': max(corner.y for corner in bbox_world) - min(corner.y for corner in bbox_world),
                'z': max(corner.z for corner in bbox_world) - min(corner.z for corner in bbox_world)
            }
            
            # Generate sampling points di sumbu Z kamera (karena light ditempatkan di sini)
            sampling_points = []
            directions = []
            
            # Karena light ditempatkan di sumbu Z kamera, kita hanya perlu sampling di sepanjang sumbu ini
            camera_to_obj = (obj_center - camera_position).normalized()
            
            # Generate sampling points yang lebih jauh dari objek untuk raycast yang lebih baik
            max_dimension = max(bbox_dimensions.values())
            sampling_distance = max_dimension * 0.8  # Sampling di 80% dari dimensi objek
            
            # Camera to object analysis completed
            
            # Generate sampling points di sepanjang sumbu Z kamera
            for i in range(sample_points):
                # Buat sampling points yang lebih jauh dari center objek
                # Ini memastikan raycast benar-benar menembus objek
                offset_distance = (i - (sample_points - 1) / 2) * sampling_distance
                
                # Hitung titik sampling di sepanjang sumbu kamera-objek
                sample_point = obj_center + camera_to_obj * offset_distance
                direction = camera_to_obj  # Gunakan arah kamera
                
                sampling_points.append(sample_point)
                directions.append(direction)
                
                # Sample point calculated
                
                # Tambahkan sampling dari arah berlawanan hanya untuk titik tengah
                # untuk validasi ketebalan dari kedua sisi
                if i == sample_points // 2:  # Titik tengah
                    opposite_direction = -camera_to_obj
                    sampling_points.append(sample_point)
                    directions.append(opposite_direction)
                    # Opposite sample point calculated
            
            # Lakukan raycast sampling untuk mengukur ketebalan
            thickness_measurements = []
            front_surface_locations = []  # Kumpulkan lokasi permukaan depan
            back_surface_locations = []   # Kumpulkan lokasi permukaan belakang
            
            for i, (start_point, direction) in enumerate(zip(sampling_points, directions)):
                try:
                    # Raycast dari luar objek menuju objek
                    # Gunakan jarak yang lebih besar untuk memastikan kita mulai dari luar
                    ray_start = start_point + direction * (max_dimension * 2 + 10.0)  # Mulai dari jauh di luar
                    ray_end = start_point - direction * (max_dimension * 2 + 10.0)   # Akhir di jauh di sisi lain
                    
                    # Ray cast initialized
                    
                    # Cari intersection points
                    has_hit1, hit_obj1, hit_loc1, dist1 = lumi_ray_cast_between_points(
                        context, ray_start, ray_end, exclude_objects=[]
                    )
                    
                    if has_hit1 and hit_obj1 == obj:
                        # Lanjutkan raycast dari titik pertama untuk mencari sisi lain
                        # Gunakan arah yang berlawanan untuk mencari sisi lain objek
                        opposite_direction = -direction
                        ray_start2 = hit_loc1 + opposite_direction * 0.01  # Offset dengan arah berlawanan
                        ray_end2 = hit_loc1 + opposite_direction * (max_dimension * 2 + 10.0)  # Raycast ke sisi lain
                        
                        # Second ray cast initialized
                        has_hit2, hit_obj2, hit_loc2, dist2 = lumi_ray_cast_between_points(
                            context, ray_start2, ray_end2, exclude_objects=[]
                        )
                        
                        if has_hit2 and hit_obj2 == obj:
                            # Validasi bahwa kedua titik berbeda secara signifikan
                            thickness = (hit_loc1 - hit_loc2).length
                            # Thickness measurement calculated
                            
                            # Tambahkan validasi tambahan untuk memastikan ketebalan masuk akal
                            if thickness > 0.001 and thickness < max_dimension * 3:  # Filter nilai terlalu kecil dan terlalu besar
                                thickness_measurements.append(thickness)
                                
                                # Tentukan mana front surface dan back surface berdasarkan jarak ke kamera
                                dist1_to_camera = (hit_loc1 - camera_position).length
                                dist2_to_camera = (hit_loc2 - camera_position).length
                                
                                if dist1_to_camera < dist2_to_camera:
                                    # hit_loc1 lebih dekat ke kamera = front surface
                                    front_surface_locations.append(hit_loc1)
                                    back_surface_locations.append(hit_loc2)
                                else:
                                    # hit_loc2 lebih dekat ke kamera = front surface
                                    front_surface_locations.append(hit_loc2)
                                    back_surface_locations.append(hit_loc1)
                                
                                # Valid thickness measurement
                            else:
                                # Invalid thickness measurement - filtered out
                                pass
                        else:
                            # No second intersection found
                            pass
                    else:
                        # No first intersection found
                        pass
                    
                except Exception as e:
                    # Error in thickness sampling - continuing
                    continue
            
            # Hitung statistik ketebalan untuk objek ini
            if thickness_measurements:
                avg_thickness = sum(thickness_measurements) / len(thickness_measurements)
                max_obj_thickness = max(thickness_measurements)
                min_obj_thickness = min(thickness_measurements)
                
                # Hitung rata-rata lokasi permukaan depan dan belakang
                avg_front_surface = None
                avg_back_surface = None
                
                if front_surface_locations:
                    avg_front_surface = sum(front_surface_locations, Vector((0, 0, 0))) / len(front_surface_locations)
                    # Average front surface calculated
                
                if back_surface_locations:
                    avg_back_surface = sum(back_surface_locations, Vector((0, 0, 0))) / len(back_surface_locations)
                    # Average back surface calculated
                
                thickness_data = {
                    'object_name': obj.name,
                    'average_thickness': avg_thickness,
                    'max_thickness': max_obj_thickness,
                    'min_thickness': min_obj_thickness,
                    'measurements': thickness_measurements,
                    'sample_count': len(thickness_measurements),
                    'total_samples': len(sampling_points),  # Tambahkan info total samples
                    'success_rate': len(thickness_measurements) / len(sampling_points),  # Tambahkan success rate
                    'bounding_box_dimensions': bbox_dimensions,
                    'object_center': obj_center,
                    'method': 'camera_z_axis_sampling',
                    'front_surface_location': avg_front_surface,  # Tambahkan lokasi permukaan depan
                    'back_surface_location': avg_back_surface    # Tambahkan lokasi permukaan belakang
                }
                
                thickness_analysis['thickness_data'][obj.name] = thickness_data
                
                # Update statistik keseluruhan
                total_thickness += avg_thickness
                thickness_analysis['max_thickness'] = max(thickness_analysis['max_thickness'], max_obj_thickness)
                thickness_analysis['min_thickness'] = min(thickness_analysis['min_thickness'], min_obj_thickness)
                valid_objects += 1
                
                # Thickness analysis completed successfully
            else:
                # No valid thickness measurements - using fallback
                
                # Fallback ke bounding box dimensions - gunakan dimensi terbesar sebagai ketebalan
                fallback_thickness = max(bbox_dimensions.values())
                thickness_data = {
                    'object_name': obj.name,
                    'average_thickness': fallback_thickness,
                    'max_thickness': fallback_thickness,
                    'min_thickness': fallback_thickness,
                    'measurements': [],
                    'sample_count': 0,
                    'bounding_box_dimensions': bbox_dimensions,
                    'object_center': obj_center,
                    'method': 'bounding_box_fallback'
                }
                
                thickness_analysis['thickness_data'][obj.name] = thickness_data
                total_thickness += fallback_thickness
                thickness_analysis['max_thickness'] = max(thickness_analysis['max_thickness'], fallback_thickness)
                thickness_analysis['min_thickness'] = min(thickness_analysis['min_thickness'], fallback_thickness)
                valid_objects += 1
                
                # Using bounding box fallback thickness
        
        # Hitung final statistics
        thickness_analysis['objects_analyzed'] = valid_objects
        if valid_objects > 0:
            thickness_analysis['average_thickness'] = total_thickness / valid_objects
        else:
            thickness_analysis['average_thickness'] = 0.0
            thickness_analysis['min_thickness'] = 0.0
        
        # Thickness analysis summary completed
        
    except Exception as e:
        # Error in thickness analysis - using defaults
        pass
    
    return thickness_analysis


# Export list untuk import control
__all__ = [
    'SceneAnalysisResult',
    'get_camera_frustum_planes',
    'is_object_in_frustum',
    'get_objects_in_camera_view',
    'is_object_occluded_from_camera',
    'classify_objects_by_background',
    'get_background_distance_analysis',
    'create_background_selection_set',
    'analyze_background_for_lighting',
    'get_object_thickness_analysis'
]
