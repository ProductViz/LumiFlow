"""
Smart Light Calculator
Calculates optimal lighting parameters based on scene analysis.
"""

import math
import bpy
from mathutils import Vector, Matrix
from typing import Dict, List, Tuple, Optional, Any

# Import utility functions
from .light import lumi_calculate_light_intensity, lumi_calculate_light_size
from .common import lumi_get_light_collection, lumi_move_to_collection
from .scene_analysis import get_object_thickness_analysis


def get_smart_light_parameters(
    context: bpy.types.Context,
    hit_obj: bpy.types.Object,
    hit_location: Vector,
    hit_normal: Vector,
    light_type: str
) -> Dict[str, Any]:
    """
    Calculate optimal lighting parameters using intelligent analysis.
    
    Args:
        context: Blender context
        hit_obj: Object hit by raycast
        hit_location: Hit point location
        hit_normal: Normal vector at hit point
        light_type: Light type ('POINT', 'SPOT', 'AREA', 'SUN')
    
    Returns:
        Dictionary with optimal lighting parameters
    """
    # Default parameters
    smart_params = {
        'position': hit_location + Vector((0, 0, 5)),  # Default 5 units above
        'distance': 5.0,
        'power': 1000.0,
        'scale': {}
    }
    
    try:
        # Analyze scene for optimal parameters
        scene_analysis = analyze_scene_for_lighting(context, hit_obj, hit_location)
        
        # Calculate position based on hit_normal
        position = calculate_optimal_light_position(context, hit_obj, hit_location, hit_normal, light_type)
        smart_params['position'] = position
        
        # Calculate distance
        distance = (position - hit_location).length
        smart_params['distance'] = distance
        
        # Calculate power/intensity
        power = calculate_optimal_power(light_type, distance, scene_analysis)
        smart_params['power'] = power
        
        # Calculate scale parameters
        scale_params = calculate_optimal_scale(light_type, distance, scene_analysis)
        smart_params['scale'] = scale_params
        
        
    except Exception as e:
        # Error in smart light calculation - using defaults
        return smart_params
    
    return smart_params



def analyze_scene_for_lighting(
    context: bpy.types.Context,
    hit_obj: bpy.types.Object,
    hit_location: Vector
) -> Dict[str, Any]:
    """
    Analyze scene for optimal lighting parameters.
    
    Args:
        context: Blender context
        hit_obj: Hit object
        hit_location: Hit point location
    
    Returns:
        Dictionary with scene analysis
    """
    scene_analysis = {
        'object_count': 0,
        'scene_size': 0.0,
        'ambient_light_level': 0.0,
        'object_thickness': 0.0,
        'nearby_objects': []
    }
    
    try:
        # Calculate number of objects in scene
        all_objects = [obj for obj in context.scene.objects if obj.type == 'MESH']
        scene_analysis['object_count'] = len(all_objects)
        
        # Calculate scene size
        if all_objects:
            bbox_min = Vector((float('inf'), float('inf'), float('inf')))
            bbox_max = Vector((float('-inf'), float('-inf'), float('-inf')))
            
            for obj in all_objects:
                bbox_world = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                for corner in bbox_world:
                    bbox_min.x = min(bbox_min.x, corner.x)
                    bbox_min.y = min(bbox_min.y, corner.y)
                    bbox_min.z = min(bbox_min.z, corner.z)
                    bbox_max.x = max(bbox_max.x, corner.x)
                    bbox_max.y = max(bbox_max.y, corner.y)
                    bbox_max.z = max(bbox_max.z, corner.z)
            
            scene_size = (bbox_max - bbox_min).length
            scene_analysis['scene_size'] = scene_size
        
        # Analyze target object thickness
        if hit_obj and hit_obj.type == 'MESH':
            thickness_result = get_object_thickness_analysis(
                context, [hit_obj], context.scene.camera, sample_points=3
            )
            if thickness_result['thickness_data']:
                obj_thickness = thickness_result['thickness_data'][hit_obj.name]['average_thickness']
                scene_analysis['object_thickness'] = obj_thickness
        
        # Get nearby objects
        nearby_objects = get_nearby_objects(context, hit_location, radius=5.0)
        scene_analysis['nearby_objects'] = nearby_objects
        
        
    except Exception as e:
        # Error in scene analysis - using defaults
        pass
    
    return scene_analysis


def calculate_optimal_light_position(
    context: bpy.types.Context,
    hit_obj: bpy.types.Object,
    hit_location: Vector,
    hit_normal: Vector,
    light_type: str
) -> Vector:
    """
    Calculate optimal light position based on hit_normal.
    
    Args:
        context: Blender context
        hit_obj: Hit object
        hit_location: Hit point location
        hit_normal: Normal vector at hit point
        light_type: Light type
    
    Returns:
        Vector with optimal position
    """
    try:
        # Validate hit_normal
        if not isinstance(hit_normal, Vector) or hit_normal.length == 0:
            # Invalid hit_normal - using fallback
            return hit_location + Vector((0, 0, 5))  # Default fallback
        
        # Normalize hit_normal
        normal = hit_normal.normalized()
        
        # Calculate default distance based on light type
        default_distances = {
            'SUN': 20.0,
            'POINT': 5.0,
            'SPOT': 8.0,
            'AREA': 6.0
        }
        distance = default_distances.get(light_type, 5.0)
        
        # Calculate light offset based on normal and distance
        light_offset = normal * distance
        
        # Calculate final position
        final_position = hit_location + light_offset
        
        return final_position
            
    except Exception as e:
        # Error in position calculation - using fallback
        return hit_location + Vector((0, 0, 5))  # Default fallback


def calculate_optimal_power(
    light_type: str,
    distance: float,
    scene_analysis: Dict[str, Any]
) -> float:
    """
    Calculate optimal power for light.
    
    Args:
        light_type: Light type
        distance: Distance to target
        scene_analysis: Scene analysis result
    
    Returns:
        Float with optimal power
    """
    try:
        # Base power based on light type
        base_power = {
            'POINT': 1000.0,
            'SPOT': 1500.0,
            'AREA': 2000.0,
            'SUN': 5000.0
        }.get(light_type, 1000.0)
        
        # Adjust power based on distance (inverse square law)
        distance_multiplier = max(0.1, (distance / 5.0) ** 2)
        
        # Adjust power based on scene size
        scene_size = scene_analysis.get('scene_size', 10.0)
        scene_multiplier = max(0.5, scene_size / 20.0)
        
        # Calculate final power
        optimal_power = base_power * distance_multiplier * scene_multiplier
        
        return optimal_power
        
    except Exception as e:
        # Error in power calculation - using defaults
        return 1000.0  # Default fallback


def calculate_optimal_scale(
    light_type: str,
    distance: float,
    scene_analysis: Dict[str, Any]
) -> Dict[str, float]:
    """
    Calculate optimal scale parameters for light.
    
    Args:
        light_type: Light type
        distance: Distance to target
        scene_analysis: Scene analysis result
    
    Returns:
        Dictionary with scale parameters
    """
    scale_params = {}
    
    try:
        if light_type == 'AREA':
            # Area light size based on distance and object thickness
            object_thickness = scene_analysis.get('object_thickness', 1.0)
            base_size = max(0.5, object_thickness * 0.8)
            
            scale_params = {
                'size': base_size * (distance / 5.0),
                'size_y': base_size * 1.2 * (distance / 5.0)
            }
            
        elif light_type == 'SPOT':
            # Spot light parameters
            scale_params = {
                'spot_size': math.radians(45),  # 45 degrees
                'spot_blend': 0.15,
                'radius': 0.1
            }
            
        elif light_type == 'POINT':
            # Point light radius
            scale_params = {
                'radius': 0.1
            }
            
        elif light_type == 'SUN':
            # Sun light angle
            scale_params = {
                'angle': math.radians(0.5)  # 0.5 degrees
            }
        
        
    except Exception as e:
        # Error in scale calculation - using defaults
        if light_type == 'AREA':
            scale_params = {'size': 1.0, 'size_y': 1.2}
        elif light_type == 'SPOT':
            scale_params = {'spot_size': math.radians(45), 'spot_blend': 0.15, 'radius': 0.1}
        else:
            scale_params = {'radius': 0.1}
    
    return scale_params


def get_nearby_objects(
    context: bpy.types.Context,
    location: Vector,
    radius: float = 5.0
) -> List[bpy.types.Object]:
    """
    Get objects within a certain radius from location.
    
    Args:
        context: Blender context
        location: Center location
        radius: Search radius
    
    Returns:
        List of nearby objects
    """
    nearby_objects = []
    
    try:
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                distance = (obj.location - location).length
                if distance <= radius:
                    nearby_objects.append(obj)
    except Exception as e:
        # Error in nearby objects detection
        pass
    
    return nearby_objects


# Export list for import control
__all__ = [
    'get_smart_light_parameters',
    'analyze_scene_for_lighting',
    'calculate_optimal_light_position',
    'calculate_optimal_power',
    'calculate_optimal_scale',
    'get_nearby_objects'
]

