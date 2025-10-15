"""
SpatialAnalyzer - Spatial relationship analysis and line-of-sight calculations.
Menggantikan ray casting logic dari berbagai tempat.
"""

import bpy
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from mathutils import Vector


@dataclass
class SpatialGraph:
    """Spatial relationship graph."""
    nodes: Dict[bpy.types.Object, Dict] = None
    edges: List[tuple] = None  # (obj1, obj2, relationship_type)


class SpatialAnalyzer:
    """
    Handles spatial analysis: line-of-sight, occlusion, relationships.
    """

    def __init__(self, context: bpy.types.Context):
        self.context = context

    def build_graph(self, classifications: Dict) -> SpatialGraph:
        """
        Build spatial relationship graph dari classifications.
        Expensive operation, use sparingly.
        """
        # Simplified implementation - bisa dikembangkan nanti
        nodes = {}
        edges = []

        for obj, cls in classifications.items():
            nodes[obj] = {
                'classification': cls,
                'bounds': self._get_object_bounds(obj)
            }

        return SpatialGraph(nodes=nodes, edges=edges)

    def check_line_of_sight(self, from_pos: Vector, to_pos: Vector,
                           exclude_objects: List[bpy.types.Object] = None) -> bool:
        """
        Check if there's clear line of sight between two positions.
        Replacement untuk lumi_ray_cast_between_points.
        """
        # Use Blender's ray_cast
        direction = to_pos - from_pos
        distance = direction.length

        if distance == 0:
            return True

        direction.normalize()

        # Perform raycast
        depsgraph = self.context.evaluated_depsgraph_get()
        result = self.context.scene.ray_cast(
            depsgraph,
            from_pos,
            direction,
            distance=distance
        )

        hit, hit_location, hit_normal, hit_index, hit_obj, hit_matrix = result

        # If no hit, clear line of sight
        if not hit:
            return True

        # Check if hit object is in exclude list
        if exclude_objects and hit_obj in exclude_objects:
            return True

        # Hit something that's not excluded
        return False

    def _get_object_bounds(self, obj: bpy.types.Object) -> Dict:
        """Get simplified bounds info untuk spatial graph."""
        if not obj.bound_box:
            return {'center': obj.location, 'radius': 1.0}

        # Calculate center and approximate radius
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        center = sum(bbox_corners, Vector()) / len(bbox_corners)
        radius = max((corner - center).length for corner in bbox_corners)

        return {'center': center, 'radius': radius}


__all__ = ['SpatialAnalyzer', 'SpatialGraph']