# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Light Utilities
Contains specialized light-related utility functions: positioning, creation, intensity calculations, and mode management.
"""

import math
import bpy
import logging
from mathutils import Vector
from bpy_extras import view3d_utils

# Import common utilities
from .common import lumi_get_light_collection, lumi_move_to_collection

logger = logging.getLogger(__name__)

# MODE MANAGEMENT FUNCTIONS moved to overlay/utils.py


def lumi_get_light_pivot(light_obj) -> Vector:
    """Get the pivot point of a light object."""
    try:
        if "Lumi_pivot_world" in light_obj:
            pivot = light_obj["Lumi_pivot_world"]
            # Validate that pivot is a list/tuple with 3 elements or bpy id property array
            if isinstance(pivot, (list, tuple)) and len(pivot) >= 3:
                return Vector((pivot[0], pivot[1], pivot[2]))
            elif hasattr(pivot, '__len__') and hasattr(pivot, '__getitem__') and len(pivot) >= 3:
                # Handle bpy id property array and similar objects
                try:
                    return Vector((pivot[0], pivot[1], pivot[2]))
                except (IndexError, TypeError) as e:
                    logger.debug(f"Cannot access pivot elements: {e}")
            else:
                logger.debug(f"Invalid pivot format: {type(pivot)}")
        return light_obj.location.copy()
    except Exception as e:
        logger.error(f"Error in lumi_get_light_pivot: {e}")
        return light_obj.location.copy()


def lumi_set_light_pivot(light_obj: bpy.types.Object, pivot_location: Vector):
    """Set the pivot point for a light object."""
    try:
        # Validate input
        if not isinstance(pivot_location, Vector):
            logger.warning(f"pivot_location is not Vector: {type(pivot_location)}")
            return

        relative_position = pivot_location - light_obj.location

        light_obj["Lumi_pivot_relative"] = (relative_position.x, relative_position.y, relative_position.z)
        light_obj["Lumi_pivot_world"] = (pivot_location.x, pivot_location.y, pivot_location.z)

    except Exception as e:
        logger.error(f"Error in lumi_set_light_pivot: {e}")


def lumi_initialize_pivot_for_existing_light(light_obj: bpy.types.Object, context: bpy.types.Context) -> bool:
    """Initialize pivot for existing light that doesn't have pivot data"""
    try:
        # Skip if light already has pivot data
        if "Lumi_pivot_world" in light_obj:
            return True

        # Get light facing direction based on type
        light_direction = lumi_get_light_facing_direction(light_obj)

        if light_direction is None:
            logger.warning(f"Could not determine facing direction for {light_obj.name}")
            return False

        # Perform raycast from light position in the direction the light is shining
        # For pivot placement, we want to raycast in the direction the light is facing/emitting
        ray_start = light_obj.location
        ray_end = ray_start + light_direction * 100.0  # Long ray to find surfaces

        # Use scene raycast to find intersection
        result, location, normal, index, obj, matrix = context.scene.ray_cast(
            context.view_layer.depsgraph, ray_start, light_direction
        )

        if result and obj and obj.type == 'MESH':
            # Found mesh surface - place pivot at hit location
            lumi_set_light_pivot(light_obj, location)
            return True
        else:
            # No mesh found - place pivot 5 meters in facing direction
            fallback_pivot = ray_start + light_direction * 5.0
            lumi_set_light_pivot(light_obj, fallback_pivot)
            return True

    except Exception as e:
        logger.error(f"Error initializing pivot for {light_obj.name}: {e}")
        return False


def lumi_get_light_facing_direction(light_obj: bpy.types.Object) -> Vector | None:
    """Get the direction a light is facing based on its type and rotation.

    Args:
        light_obj: The light object

    Returns:
        Vector: Direction vector the light is facing, or None if cannot determine
    """
    try:
        if light_obj.data.type == 'SUN':
            # Sun lights: direction sun is shining FROM (opposite to where it's pointing)
            # The sun's "forward" direction is actually the direction it's shining from
            forward_vec = Vector((0, 0, -1))  # Negative Z = direction light comes from
            transformed_vec = light_obj.matrix_world @ forward_vec
            return (transformed_vec - light_obj.matrix_world.translation).normalized()

        elif light_obj.data.type == 'SPOT':
            # Spot lights: direction the spot is pointing (where light goes)
            forward_vec = Vector((0, 0, -1))  # Negative Z = emission direction
            transformed_vec = light_obj.matrix_world @ forward_vec
            return (transformed_vec - light_obj.matrix_world.translation).normalized()

        elif light_obj.data.type == 'AREA':
            # Area lights: direction the area light is emitting
            forward_vec = Vector((0, 0, -1))  # Negative Z = emission direction
            transformed_vec = light_obj.matrix_world @ forward_vec
            return (transformed_vec - light_obj.matrix_world.translation).normalized()

        elif light_obj.data.type == 'POINT':
            # Point lights: omnidirectional, but for pivot we use negative Z as default
            forward_vec = Vector((0, 0, -1))  # Negative Z = emission direction
            transformed_vec = light_obj.matrix_world @ forward_vec
            return (transformed_vec - light_obj.matrix_world.translation).normalized()

        else:
            # Unknown light type - use negative Z as fallback
            return Vector((0, 0, -1))

    except Exception as e:
        logger.error(f"Error getting light facing direction: {e}")
        return None


def lumi_initialize_pivots_for_all_existing_lights(context: bpy.types.Context) -> int:
    """Initialize pivots for all existing lights in the scene that don't have pivot data.

    Args:
        context: Blender context (can be restricted context)

    Returns:
        int: Number of lights that had pivots initialized
    """
    initialized_count = 0

    try:
        # Check if context is restricted and get a proper context if needed
        if not hasattr(context, 'scene') or not hasattr(context, 'view_layer'):
            # Context is restricted, use bpy.context as fallback
            proper_context = bpy.context
            if not hasattr(proper_context, 'scene') or not hasattr(proper_context, 'view_layer'):
                logger.error("No valid Blender context available for pivot initialization")
                return 0
        else:
            proper_context = context

        # Find all light objects in the scene
        all_lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']

        for light_obj in all_lights:
            if lumi_initialize_pivot_for_existing_light(light_obj, proper_context):
                initialized_count += 1

        if initialized_count > 0:
            return initialized_count

    except Exception as e:
        logger.error(f"Error initializing pivots for existing lights: {e}")
        return 0


def lumi_update_light_orientation(light_obj: bpy.types.Object):
    """Update light orientation to point towards its pivot."""
    try:
        if "Lumi_pivot_world" in light_obj:
            pivot_data = light_obj["Lumi_pivot_world"]
            # Handle various pivot data formats
            if isinstance(pivot_data, (list, tuple)) and len(pivot_data) >= 3:
                pivot_world = Vector((pivot_data[0], pivot_data[1], pivot_data[2]))
            elif hasattr(pivot_data, '__len__') and hasattr(pivot_data, '__getitem__') and len(pivot_data) >= 3:
                # Handle bpy id property array and similar objects
                try:
                    pivot_world = Vector((pivot_data[0], pivot_data[1], pivot_data[2]))
                except (IndexError, TypeError) as e:
                    logger.debug(f"Cannot access pivot elements: {e}")
                    return
            else:
                logger.debug(f"Invalid pivot format: {type(pivot_data)}")
                return
                
            direction = (pivot_world - light_obj.location).normalized()
            rot_quat = direction.to_track_quat('-Z', 'Y')
            light_obj.rotation_euler = rot_quat.to_euler()
    except Exception as e:
        logger.error(f"Error in lumi_update_light_orientation: {e}", exc_info=True)


def lumi_calculate_light_intensity(light_type: str, distance: float) -> float:
    """Calculate appropriate light intensity based on type and distance."""
    intensities = {
        'AREA': max(10, distance * distance * 100), 
        'SUN': 3.0
    }
    return intensities.get(light_type, max(5, distance * distance * 25))


def lumi_calculate_light_size(light_type: str, distance: float) -> float:
    """Calculate appropriate light size based on type and distance."""
    base_size = distance * 0.2
    return max(0.1, min(base_size, 5.0))


def lumi_get_viewport_camera_position(rv3d: bpy.types.RegionView3D) -> Vector:
    """Get current viewport camera position."""
    if rv3d.view_perspective == 'CAMERA':
        camera = bpy.context.scene.camera
        if camera:
            return camera.location.copy()
    return rv3d.view_location.copy()


def create_smart_light(context: bpy.types.Context, light_type: str, hit_location: Vector, hit_normal: Vector, hit_obj: bpy.types.Object) -> bpy.types.Object:
    """Create a smart light with intelligent positioning and settings."""
    # Import smart calculator
    from .smart_calc import get_smart_light_parameters
    
    # Get smart parameters using intelligence system
    smart_params = get_smart_light_parameters(context, hit_obj, hit_location, hit_normal, light_type)
    
    # Use calculated position and distance
    light_position = smart_params['position']
    light_distance = smart_params['distance']
    
    # Create light data
    light_data = bpy.data.lights.new(name=f"Smart {light_type.title()}", type=light_type)
    light_data.energy = smart_params['power']  # Use intelligent power calculation

    # Configure light-specific settings using intelligent scale
    scale_params = smart_params['scale']
    if light_type == 'AREA':
        # Set default shape to RECTANGLE, but allow override by caller
        light_data.shape = 'RECTANGLE'
        light_data.size = scale_params.get('size', 1.0)
        light_data.size_y = scale_params.get('size_y', 1.2)
    elif light_type == 'SPOT':
        light_data.spot_size = scale_params.get('spot_size', math.radians(45))
        light_data.spot_blend = scale_params.get('spot_blend', 0.15)
        # Set radius if available
        if hasattr(light_data, 'shadow_soft_size'):
            light_data.shadow_soft_size = scale_params.get('radius', 0.1)
    elif light_type == 'POINT':
        # Set radius for point light
        if hasattr(light_data, 'shadow_soft_size'):
            light_data.shadow_soft_size = scale_params.get('radius', 0.1)
    elif light_type == 'SUN':
        light_data.angle = scale_params.get('angle', math.radians(0.5))
    
    # Create light object
    light_obj = bpy.data.objects.new(name=light_data.name, object_data=light_data)
    light_obj.location = light_position
    lumi_set_light_pivot(light_obj, hit_location)
    
    # Orient light towards target
    direction = (hit_location - light_position).normalized()
    rot_quat = direction.to_track_quat('-Z', 'Y')
    light_obj.rotation_euler = rot_quat.to_euler()
    
    # Add to collection and select
    collection = lumi_get_light_collection()
    lumi_move_to_collection(light_obj, collection)
    bpy.ops.object.select_all(action='DESELECT')
    light_obj.select_set(True)
    context.view_layer.objects.active = light_obj
    
    return light_obj


# get_mode_label_for_light_type() moved to overlay/utils.py


def lumi_get_selected_lights() -> list:
    """Get all selected light objects in the current scene."""
    return [obj for obj in bpy.context.selected_objects if obj.type == 'LIGHT']


def lumi_calculate_light_target_position(light_obj: bpy.types.Object, scene: bpy.types.Scene) -> Vector:
    """Calculate target position for light visualization.
    
    Args:
        light_obj: The light object to calculate target for
        scene: The current scene
        
    Returns:
        Vector: Target position for the light
    """
    try:
        # If light has a pivot, use that as target
        if "Lumi_pivot_world" in light_obj:
            pivot_data = light_obj["Lumi_pivot_world"]
            # Handle various pivot data formats
            if isinstance(pivot_data, (list, tuple)) and len(pivot_data) >= 3:
                return Vector((pivot_data[0], pivot_data[1], pivot_data[2]))
            elif hasattr(pivot_data, '__len__') and hasattr(pivot_data, '__getitem__') and len(pivot_data) >= 3:
                # Handle bpy id property array and similar objects
                try:
                    return Vector((pivot_data[0], pivot_data[1], pivot_data[2]))
                except (IndexError, TypeError) as e:
                    logger.debug(f"Cannot access pivot elements: {e}")
            else:
                logger.debug(f"Invalid pivot format: {type(pivot_data)}")
        
        # Fallback: calculate target based on light direction and distance
        light_location = light_obj.location
        
        # Get light direction based on type
        if light_obj.data.type == 'SUN':
            # For sun lights, use rotation to determine direction
            # Transform the forward vector by the world matrix and negate it
            forward_vec = Vector((0, 0, 1))
            transformed_vec = light_obj.matrix_world @ forward_vec
            direction = (transformed_vec - light_obj.matrix_world.translation).normalized()
            # Project far in the direction (sun lights shine from infinity)
            return light_location + direction * 100.0
        elif light_obj.data.type == 'SPOT':
            # For spot lights, use rotation to determine direction
            # Transform the forward vector by the world matrix and negate it
            forward_vec = Vector((0, 0, 1))
            transformed_vec = light_obj.matrix_world @ forward_vec
            direction = (transformed_vec - light_obj.matrix_world.translation).normalized()
            # Use spot size to estimate reasonable distance
            distance = max(5.0, light_obj.data.energy * 0.5)
            return light_location + direction * distance
        else:
            # For other lights (POINT, AREA), use default downward direction
            direction = Vector((0, 0, -1))
            # Estimate distance based on light energy
            distance = max(2.0, light_obj.data.energy * 0.3)
            return light_location + direction * distance
            
    except Exception as e:
        logger.error(f"Error in lumi_calculate_light_target_position: {e}")
        # Ultimate fallback: return position slightly below the light
        return light_obj.location + Vector((0, 0, -1))


# Export specialized light utilities (excluding common ones)
__all__ = [
    'lumi_get_light_pivot',
    'lumi_set_light_pivot',
    'lumi_update_light_orientation',
    'lumi_initialize_pivot_for_existing_light',
    'lumi_get_light_facing_direction',
    'lumi_initialize_pivots_for_all_existing_lights',
    'lumi_calculate_light_intensity',
    'lumi_calculate_light_size',
    'lumi_get_viewport_camera_position',
    'create_smart_light',
    'lumi_get_selected_lights',
    'lumi_calculate_light_target_position'
]

