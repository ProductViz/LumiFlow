# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

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
from .material_adaptation import generate_lighting_recommendations
from .scene_context import MaterialData


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
        'target_object_size': 0.0,
        'target_object_bounds': None,
        'ambient_light_level': 0.0,
        'object_thickness': 0.0,
        'nearby_objects': [],
        'material_data': None
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

        # Calculate target object size specifically
        if hit_obj and hit_obj.type == 'MESH':
            # Calculate bounding box for target object
            bbox_world = [hit_obj.matrix_world @ Vector(corner) for corner in hit_obj.bound_box]
            obj_bbox_min = Vector((float('inf'), float('inf'), float('inf')))
            obj_bbox_max = Vector((float('-inf'), float('-inf'), float('-inf')))

            for corner in bbox_world:
                obj_bbox_min.x = min(obj_bbox_min.x, corner.x)
                obj_bbox_min.y = min(obj_bbox_min.y, corner.y)
                obj_bbox_min.z = min(obj_bbox_min.z, corner.z)
                obj_bbox_max.x = max(obj_bbox_max.x, corner.x)
                obj_bbox_max.y = max(obj_bbox_max.y, corner.y)
                obj_bbox_max.z = max(obj_bbox_max.z, corner.z)

            target_size = (obj_bbox_max - obj_bbox_min).length
            scene_analysis['target_object_size'] = target_size
            scene_analysis['target_object_bounds'] = {
                'min': obj_bbox_min,
                'max': obj_bbox_max,
                'dimensions': obj_bbox_max - obj_bbox_min
            }

            # Analyze material properties
            try:
                from .scene_context import MaterialAnalyzer
                material_analyzer = MaterialAnalyzer(context)
                material_data = material_analyzer.analyze_object_materials(hit_obj)
                scene_analysis['material_data'] = material_data
            except Exception as mat_e:
                # Material analysis failed, continue without it
                pass

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
    Calculate optimal light position based on photometric principles and object size.

    Photometric principles applied:
    - Distance affects illuminance (inverse square law)
    - Object size determines optimal viewing distance
    - Normal vector ensures proper light direction

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

        # Calculate base distance based on light type and photometric principles
        base_distances = {
            'SUN': 20.0,    # Sun lights are distant sources
            'POINT': 5.0,   # Point lights follow inverse square law closely
            'SPOT': 8.0,    # Spot lights need distance for proper beam spread
            'AREA': 6.0     # Area lights need distance for soft shadows
        }
        base_distance = base_distances.get(light_type, 5.0)

        # Adjust distance based on target object size using photometric principles
        if hit_obj and hit_obj.type == 'MESH':
            # Calculate object bounding box dimensions
            bbox_world = [hit_obj.matrix_world @ Vector(corner) for corner in hit_obj.bound_box]
            obj_bbox_min = Vector((float('inf'), float('inf'), float('inf')))
            obj_bbox_max = Vector((float('-inf'), float('-inf'), float('-inf')))

            for corner in bbox_world:
                obj_bbox_min.x = min(obj_bbox_min.x, corner.x)
                obj_bbox_min.y = min(obj_bbox_min.y, corner.y)
                obj_bbox_min.z = min(obj_bbox_min.z, corner.z)
                obj_bbox_max.x = max(obj_bbox_max.x, corner.x)
                obj_bbox_max.y = max(obj_bbox_max.y, corner.y)
                obj_bbox_max.z = max(obj_bbox_max.z, corner.z)

            # Get object dimensions
            obj_dimensions = obj_bbox_max - obj_bbox_min
            object_size = obj_dimensions.length

            # Photometric distance calculation:
            # - For proper illuminance distribution, distance should be 1.5-2x object size
            # - This ensures even lighting and proper shadow definition
            # - Larger objects need proportionally larger distances to maintain illuminance
            optimal_distance_multiplier = max(1.0, object_size / 2.0)
            distance = base_distance * optimal_distance_multiplier

            # For very large objects, add extra distance to prevent over-illumination
            if object_size > 10.0:
                distance *= 1.2  # Additional 20% for large objects
        else:
            distance = base_distance

        # Calculate light offset based on normal and photometrically calculated distance
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
    Calculate optimal power for light based on photometric principles.

    Photometric principles applied:
    - Inverse Square Law: Illuminance decreases with square of distance (for point sources)
    - Target Illuminance: Maintain consistent brightness on target surface
    - Material Reflectance: Adjust power based on material properties
    - Light Source Characteristics: Different light types have different efficiencies
    - SUN Light: Directional source, no distance falloff, uses absolute intensity

    Args:
        light_type: Light type
        distance: Distance to target
        scene_analysis: Scene analysis result

    Returns:
        Float with optimal power
    """
    try:
        # Base power based on light type and their photometric characteristics
        base_power = {
            'POINT': 1000.0,  # Isotropic radiator, high intensity needed
            'SPOT': 1500.0,   # Directional beam, concentrated power
            'AREA': 2000.0,   # Diffuse source, needs higher power for even illumination
            'SUN': 15.0       # Directional source, uses absolute intensity (10x boost for brighter outdoor lighting)
        }.get(light_type, 1000.0)

        # SUN light uses absolute intensity, not inverse square law
        if light_type == 'SUN':
            # For SUN light, adjust based on material reflectance only
            material_multiplier = 1.0
            material_data = scene_analysis.get('material_data')
            if material_data:
                try:
                    recommendations = generate_lighting_recommendations(material_data)
                    material_multiplier = recommendations.get('intensity_multiplier', 1.0)

                    # Adjust for dark materials
                    if hasattr(material_data, 'average_reflectance'):
                        reflectance_factor = max(0.5, 1.0 / max(0.1, material_data.average_reflectance))
                        # Clamp to prevent extreme values for SUN light
                        material_multiplier = min(2.0, material_multiplier * reflectance_factor)
                except Exception as mat_e:
                    material_multiplier = 1.0

            optimal_power = base_power * material_multiplier
            # Clamp SUN power to reasonable range (0.5-40.0 for flexible outdoor lighting)
            return max(0.5, min(40.0, optimal_power))

        # For point sources (POINT, SPOT, AREA): Apply Inverse Square Law
        # Power must increase with square of distance to maintain constant illuminance on target surface
        distance_multiplier = max(0.1, (distance / 5.0) ** 2)

        # Adjust power based on target object size for proper illuminance distribution
        target_object_size = scene_analysis.get('target_object_size', 2.0)

        # Photometric calculation: Larger objects need more total light energy
        # but distributed over larger area. Use square relationship for area coverage.
        object_size_multiplier = max(0.3, (target_object_size / 2.0) ** 1.5)

        # Apply material-based adjustments using photometric principles
        material_multiplier = 1.0
        material_data = scene_analysis.get('material_data')
        if material_data:
            try:
                recommendations = generate_lighting_recommendations(material_data)
                material_multiplier = recommendations.get('intensity_multiplier', 1.0)

                # Additional photometric adjustment based on material reflectance
                # Dark materials need more light to achieve same perceived brightness
                if hasattr(material_data, 'average_reflectance'):
                    reflectance_factor = max(0.5, 1.0 / max(0.1, material_data.average_reflectance))
                    material_multiplier *= reflectance_factor
            except Exception as mat_e:
                # Material adjustment failed, use default
                material_multiplier = 1.0

        # Calculate final power using photometric principles
        optimal_power = base_power * distance_multiplier * object_size_multiplier * material_multiplier

        return optimal_power

    except Exception as e:
        # Error in power calculation - using defaults
        return 1.0 if light_type == 'SUN' else 1000.0  # Default fallback


def calculate_optimal_scale(
    light_type: str,
    distance: float,
    scene_analysis: Dict[str, Any]
) -> Dict[str, float]:
    """
    Calculate optimal scale parameters for light based on photometric principles.

    Photometric principles applied:
    - Solid Angle: Light size affects the solid angle subtended at target
    - Penumbra/Umbra: Light size controls shadow softness and transition zones
    - Beam Spread: Proper angular size for optimal illumination coverage
    - Distance Relationship: Light size scales with distance for consistent illumination

    Args:
        light_type: Light type
        distance: Distance to target
        scene_analysis: Scene analysis result

    Returns:
        Dictionary with scale parameters
    """
    scale_params = {}

    try:
        target_object_size = scene_analysis.get('target_object_size', 2.0)
        object_thickness = scene_analysis.get('object_thickness', 1.0)

        if light_type == 'AREA':
            # Photometric calculation for area lights:
            # - Light size should be proportional to object size for proper coverage
            # - Use direct relationship: light_size = object_size * coverage_factor
            # - This ensures larger objects get proportionally larger lights

            # Direct proportional scaling based on object size
            # Base coverage factor ensures proper illumination distribution
            coverage_factor = 0.8  # Light covers 80% of object size for optimal soft shadows
            base_size = target_object_size * coverage_factor

            # Adjust for distance - closer lights can be smaller, distant lights need larger
            # But keep the primary relationship with object size
            distance_factor = min(1.5, max(0.7, distance / 6.0))  # Moderate distance adjustment
            final_size = base_size * distance_factor

            # Ensure reasonable minimum and maximum sizes
            min_size = 0.3  # Minimum practical size
            max_size = 20.0  # Maximum reasonable size to avoid performance issues
            final_size = max(min_size, min(max_size, final_size))

            # Consider object thickness for very small/thin objects
            if object_thickness < 0.5:
                final_size = max(final_size, 0.5)  # Ensure minimum size for thin objects

            scale_params = {
                'size': final_size,
                'size_y': final_size * 1.2  # Rectangular aspect ratio
            }

        elif light_type == 'SPOT':
            # Photometric calculation for spot lights:
            # - Spot angle should cover object with some margin
            # - Beam spread affects illuminance distribution

            # Calculate optimal spot angle based on object size and distance
            # Use similar triangles principle: object size / distance = tan(spot_angle/2)
            half_angle_rad = math.atan(target_object_size / (2 * distance))
            optimal_spot_angle = half_angle_rad * 2 * 1.5  # 50% margin

            # Clamp to reasonable range
            optimal_spot_angle = max(math.radians(15), min(math.radians(120), optimal_spot_angle))

            scale_params = {
                'spot_size': optimal_spot_angle,
                'spot_blend': 0.15,  # Standard blend for natural falloff
                'radius': max(0.05, target_object_size * 0.02)  # Small radius for crisp edges
            }

        elif light_type == 'POINT':
            # Point lights have no physical size, but shadow softness can be controlled
            # Larger objects benefit from softer shadows (larger effective size)
            radius_multiplier = max(0.5, target_object_size / 2.0)
            scale_params = {
                'radius': 0.1 * radius_multiplier
            }

        elif light_type == 'SUN':
            # Sun lights simulate distant sources
            # Angular size affects shadow softness - smaller angle = harder shadows
            # For realistic sun simulation, keep angle small
            scale_params = {
                'angle': math.radians(0.5)  # Standard sun angular size
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

