"""
Positioning utilities - Extracted dari lighting_templates.py calculate_initial_light_positions()

Key functions:
- calculate_spherical_position()
- calculate_cartesian_position()
- apply_camera_relative_transform()
- calculate_position_from_template()
"""

import bpy
import math
from typing import Dict, Any, Optional
from mathutils import Vector, Matrix


def calculate_spherical_position(center: Vector, azimuth: float, elevation: float, distance: float) -> Vector:
    """Convert spherical coordinates to world position."""
    x = distance * math.cos(elevation) * math.sin(azimuth)
    y = -distance * math.cos(elevation) * math.cos(azimuth)
    z = distance * math.sin(elevation)
    return center + Vector((x, y, z))


def calculate_cartesian_position(center: Vector, offset: Vector, scale: float = 1.0) -> Vector:
    """Calculate from cartesian offset."""
    return center + (offset * scale)


def apply_camera_relative_transform(position: Vector, center: Vector, camera_matrix: Matrix) -> Vector:
    """Transform position relative to camera."""
    cam_matrix_3x3 = camera_matrix.to_3x3()
    cam_forward = cam_matrix_3x3 @ Vector((0, 0, -1))
    cam_right = cam_matrix_3x3 @ Vector((1, 0, 0))
    cam_up = cam_matrix_3x3 @ Vector((0, 1, 0))

    local_offset = position - center
    transformed_offset = (
        local_offset.x * cam_right +
        local_offset.y * cam_forward +
        local_offset.z * cam_up
    )
    return center + transformed_offset


def calculate_position_from_template(light_config: Dict, center: Vector, base_distance: float, **kwargs) -> Vector:
    """Main function - delegates to spherical/cartesian/direct methods."""
    method = light_config.get('position', {}).get('method', 'spherical')

    if method == 'spherical':
        return _calculate_spherical_from_config(light_config, center, base_distance, **kwargs)
    elif method == 'cartesian':
        return _calculate_cartesian_from_config(light_config, center, base_distance, **kwargs)
    elif method == 'direct':
        return _calculate_direct_from_config(light_config, center, base_distance, **kwargs)
    else:
        # Default to spherical
        return _calculate_spherical_from_config(light_config, center, base_distance, **kwargs)


def _calculate_spherical_from_config(light_config: Dict, center: Vector, base_distance: float, **kwargs) -> Vector:
    """Calculate position using spherical coordinates dari config."""
    pos_config = light_config.get('position', {})

    # PENTING: Extract params dari nested structure
    params = pos_config.get('params', {})

    # Get angles (in degrees, convert to radians)
    # Template structure: position.params.azimuth
    azimuth = math.radians(params.get('azimuth', 0))
    elevation = math.radians(params.get('elevation', 30))  # Default 30° bukan 45°

    # Get distance multiplier
    distance = params.get('distance', 1.0) * base_distance

    # Calculate base position
    position = calculate_spherical_position(center, azimuth, elevation, distance)

    # Apply camera relative transform if needed
    camera_matrix = kwargs.get('camera_matrix')
    use_camera_relative = kwargs.get('use_camera_relative', False)

    if use_camera_relative and camera_matrix:
        position = apply_camera_relative_transform(position, center, camera_matrix)

    return position


def _calculate_cartesian_from_config(light_config: Dict, center: Vector, base_distance: float, **kwargs) -> Vector:
    """Calculate position using cartesian coordinates dari config."""
    pos_config = light_config.get('position', {})

    # PENTING: Extract params dari nested structure
    params = pos_config.get('params', {})

    # Get offset dari params
    # Template structure: position.params.x/y/z
    x = params.get('x', 0) * base_distance
    y = params.get('y', 0) * base_distance
    z = params.get('z', 0) * base_distance

    offset = Vector((x, y, z))

    # Simple addition - scale sudah applied di x, y, z
    return center + offset


def _calculate_direct_from_config(light_config: Dict, center: Vector, base_distance: float, **kwargs) -> Vector:
    """Calculate direct position (absolute or relative)."""
    pos_config = light_config.get('position', {})

    # PENTING: Extract params dari nested structure
    params = pos_config.get('params', {})

    # Get location dari params
    # Template structure: position.params.location
    location = params.get('location', (0, 0, 0))

    # Validate location
    if isinstance(location, (list, tuple)) and len(location) >= 3 and all(loc is not None for loc in location):
        world_position = Vector(location)
    else:
        # Fallback: offset dari center
        world_position = center + Vector((0, -base_distance, base_distance))

    return world_position


def calculate_optimal_distance(bounds_data, template_distance: float = 2.0, auto_scale: bool = True) -> float:
    """Calculate optimal light distance berdasarkan scene bounds.
    
    Scale factor is clamped between 0.5x and 5.0x:
    - Minimum 0.5x: prevents lights too close on tiny objects (<1m)
    - Maximum 5.0x: prevents lights too far on huge objects (>10m)
    
    Examples:
    - Small object (0.2m): scale=0.5, distance=1.0m (for 2.0m base)
    - Normal object (2.0m): scale=1.73, distance=3.46m
    - Large object (10m): scale=5.0 (clamped), distance=10.0m
    """
    if not auto_scale:
        return template_distance

    # Use RADIUS (bukan diagonal) untuk scaling
    # Radius = diagonal / 2
    subject_radius = bounds_data.radius
    
    # Clamp scale factor: 0.5x minimum, 5.0x maximum
    # - 0.5x prevents lights < 1.0m for tiny objects
    # - 5.0x prevents lights > 10m for architectural/large objects
    scale_factor = max(0.5, min(5.0, subject_radius))

    # Scale template distance dengan factor
    optimal_distance = template_distance * scale_factor

    return optimal_distance


__all__ = [
    'calculate_spherical_position',
    'calculate_cartesian_position',
    'apply_camera_relative_transform',
    'calculate_position_from_template',
    'calculate_optimal_distance'
]