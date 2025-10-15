"""
BoundsCalculator - Centralized bounding box calculations.
Menggantikan logic dari:
- obstruction_detector._get_world_bbox()
- template_analyzer.calculate_bounds()
- Implicit bbox calculations di scene_analysis
"""

import bpy
from typing import List, Tuple
from dataclasses import dataclass
from mathutils import Vector


@dataclass
class BoundsData:
    """Bounding box information."""
    min: Vector
    max: Vector
    center: Vector
    dimensions: Vector
    radius: float
    diagonal: float

    @staticmethod
    def empty() -> 'BoundsData':
        """Empty bounds at origin."""
        return BoundsData(
            min=Vector((0, 0, 0)),
            max=Vector((0, 0, 0)),
            center=Vector((0, 0, 0)),
            dimensions=Vector((1, 1, 1)),
            radius=0.5,
            diagonal=1.0
        )


class BoundsCalculator:
    """
    Single source of truth untuk bounding box calculations.
    """

    def calculate(self, objects: List[bpy.types.Object]) -> BoundsData:
        """
        Calculate world-space combined bounding box.

        Args:
            objects: List of objects to calculate bounds for

        Returns:
            BoundsData with min, max, center, dimensions, etc.
        """
        if not objects:
            return BoundsData.empty()

        # Get combined bbox
        min_corner, max_corner = self._get_combined_world_bbox(objects)

        # Calculate derived properties
        center = (min_corner + max_corner) * 0.5
        dimensions = max_corner - min_corner
        diagonal = dimensions.length
        radius = diagonal * 0.5

        return BoundsData(
            min=min_corner,
            max=max_corner,
            center=center,
            dimensions=dimensions,
            radius=radius,
            diagonal=diagonal
        )

    def calculate_single(self, obj: bpy.types.Object) -> Tuple[Vector, Vector]:
        """
        Get world-space bounding box for single object.

        Returns:
            Tuple of (min_corner, max_corner)
        """
        if not obj.bound_box:
            return (obj.location.copy(), obj.location.copy())

        # Transform bound_box to world space
        bbox_corners = [obj.matrix_world @ Vector(corner)
                       for corner in obj.bound_box]

        # Find min/max
        min_corner = Vector((
            min(corner.x for corner in bbox_corners),
            min(corner.y for corner in bbox_corners),
            min(corner.z for corner in bbox_corners)
        ))

        max_corner = Vector((
            max(corner.x for corner in bbox_corners),
            max(corner.y for corner in bbox_corners),
            max(corner.z for corner in bbox_corners)
        ))

        return (min_corner, max_corner)

    def _get_combined_world_bbox(self, objects: List) -> Tuple[Vector, Vector]:
        """Get combined world-space bbox for multiple objects."""
        all_corners = []

        for obj in objects:
            if not hasattr(obj, 'bound_box'):
                continue

            try:
                bbox_corners = [obj.matrix_world @ Vector(corner)
                              for corner in obj.bound_box]
                all_corners.extend(bbox_corners)
            except:
                continue

        if not all_corners:
            origin = Vector((0, 0, 0))
            return (origin, origin)

        min_corner = Vector((
            min(c.x for c in all_corners),
            min(c.y for c in all_corners),
            min(c.z for c in all_corners)
        ))

        max_corner = Vector((
            max(c.x for c in all_corners),
            max(c.y for c in all_corners),
            max(c.z for c in all_corners)
        ))

        return (min_corner, max_corner)


__all__ = ['BoundsCalculator', 'BoundsData']