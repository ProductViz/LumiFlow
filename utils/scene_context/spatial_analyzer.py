"""
SpatialAnalyzer - Spatial relationship analysis and line-of-sight calculations.
Menggantikan ray casting logic dari berbagai tempat.
"""

import bpy
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from mathutils import Vector

from .camera_analyzer import CameraAnalyzer, CameraData


@dataclass
class SpatialRelationship:
    """Simple spatial relationship descriptor untuk sepasang objek."""
    type: str  # 'NEAR_FRONT', 'NEAR_BACK', 'ABOVE', 'BELOW', etc.
    distance: float
    confidence: float


@dataclass
class SpatialGraph:
    """Spatial relationship graph."""
    nodes: Dict[bpy.types.Object, Dict] = None
    edges: List[tuple] = None  # (obj1, obj2, relationship)


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
        nodes: Dict[bpy.types.Object, Dict[str, Any]] = {}
        edges: List[tuple] = []

        # Build nodes with basic bounds info
        for obj, cls in classifications.items():
            nodes[obj] = {
                'classification': cls,
                'bounds': self._get_object_bounds(obj)
            }

        # Derive simple relationships antara product dan background
        products = [obj for obj, cls in classifications.items()
                    if getattr(cls, 'type', None) == 'product']
        backgrounds = [obj for obj, cls in classifications.items()
                       if getattr(cls, 'type', None) == 'background']

        camera_data: Optional[CameraData] = None
        cam_obj = self.context.scene.camera
        if cam_obj is not None:
            try:
                cam_analyzer = CameraAnalyzer(self.context)
                camera_data = cam_analyzer.analyze(cam_obj)
            except Exception:
                camera_data = None

        for product in products:
            p_bounds = nodes.get(product, {}).get('bounds') or {}
            for background in backgrounds:
                b_bounds = nodes.get(background, {}).get('bounds') or {}
                relationships = self._analyze_relationship(
                    product,
                    background,
                    p_bounds,
                    b_bounds,
                    camera_data,
                )
                for rel in relationships:
                    edges.append((product, background, rel))

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

    def _analyze_relationship(
        self,
        product: bpy.types.Object,
        background: bpy.types.Object,
        product_bounds: Dict[str, Any],
        background_bounds: Dict[str, Any],
        camera_data: Optional[CameraData],
    ) -> List[SpatialRelationship]:
        """Tentukan hubungan spasial sederhana antara product dan background."""
        relationships: List[SpatialRelationship] = []

        p_center: Vector = product_bounds.get('center') or product.location
        b_center: Vector = background_bounds.get('center') or background.location

        delta = b_center - p_center
        distance = delta.length
        if distance == 0:
            return relationships

        # ABOVE / BELOW (world Z)
        vertical_delta = b_center.z - p_center.z
        if abs(vertical_delta) > 0.01:
            if vertical_delta > 0:
                relationships.append(SpatialRelationship('ABOVE', distance, 0.7))
            else:
                relationships.append(SpatialRelationship('BELOW', distance, 0.7))

        # NEAR_FRONT / NEAR_BACK relatif ke kamera jika tersedia
        if camera_data is not None:
            cam_pos = camera_data.location
            cam_forward = camera_data.forward

            # Proyeksi jarak sepanjang arah kamera
            dp = (p_center - cam_pos).dot(cam_forward)
            db = (b_center - cam_pos).dot(cam_forward)

            # Background lebih jauh sepanjang arah pandang kamera
            if db > dp:
                relationships.append(SpatialRelationship('NEAR_BACK', abs(db - dp), 0.6))

        # Jika tidak ada relasi spesifik, tapi jarak cukup dekat, tandai NEAR_FRONT generic
        if not relationships and distance < (product_bounds.get('radius') or 1.0) * 4.0:
            relationships.append(SpatialRelationship('NEAR_FRONT', distance, 0.5))

        return relationships


__all__ = ['SpatialAnalyzer', 'SpatialGraph']