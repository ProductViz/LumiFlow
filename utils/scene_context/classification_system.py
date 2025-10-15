"""
ClassificationSystem - Object classification untuk background/product detection.
Menggantikan logic dari:
- obstruction_detector.analyze_scene() classification logic
- scene_analysis.classify_objects_by_background()
"""

import bpy
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from mathutils import Vector

from .camera_analyzer import CameraData


@dataclass
class ObjectClassification:
    """Classification result untuk single object."""
    type: str  # 'product', 'background', 'camera', 'other'
    confidence: float  # 0.0 to 1.0
    reasons: List[str]  # Why this classification


class ObjectClassifier:
    """
    Classifies objects sebagai product/subject atau background.
    """

    def classify_objects(self, all_objects: List[bpy.types.Object],
                        selected_objects: List[bpy.types.Object],
                        camera_data: Optional[CameraData] = None) -> Dict[bpy.types.Object, ObjectClassification]:
        """
        Classify all objects in scene.

        Args:
            all_objects: All mesh objects in scene
            selected_objects: User-selected objects (considered product)
            camera_data: Camera information untuk classification

        Returns:
            Dict mapping objects to their classifications
        """
        classifications = {}

        # Selected objects are always product/subject
        for obj in selected_objects:
            classifications[obj] = ObjectClassification(
                type='product',
                confidence=1.0,
                reasons=['User selected']
            )

        # Classify remaining objects
        for obj in all_objects:
            if obj in classifications:
                continue  # Already classified

            classification = self._classify_single_object(obj, camera_data, selected_objects)
            classifications[obj] = classification

        return classifications

    def _classify_single_object(self, obj: bpy.types.Object,
                               camera_data: Optional[CameraData],
                               selected_objects: List[bpy.types.Object]) -> ObjectClassification:
        """
        Classify single object berdasarkan various heuristics.
        """
        reasons = []
        confidence = 0.5  # Base confidence

        # Check if object is visible to camera
        if camera_data:
            in_frustum = self._is_in_camera_frustum(obj, camera_data)
            if not in_frustum:
                reasons.append('Outside camera frustum')
                confidence += 0.3  # Likely background
            else:
                reasons.append('In camera frustum')
                confidence -= 0.2  # Could be product

        # Check distance dari selected objects
        if selected_objects:
            avg_distance = self._average_distance_to_objects(obj, selected_objects)
            if avg_distance > 10.0:  # Arbitrary threshold
                reasons.append(f'Far from subjects ({avg_distance:.1f} units)')
                confidence += 0.2
            else:
                reasons.append(f'Near subjects ({avg_distance:.1f} units)')
                confidence -= 0.1

        # Check object properties
        if obj.name.lower().startswith(('ground', 'floor', 'wall', 'background')):
            reasons.append('Name suggests background')
            confidence += 0.4

        if obj.name.lower().find('light') != -1:
            reasons.append('Likely a light object')
            return ObjectClassification(
                type='other',
                confidence=0.9,
                reasons=reasons
            )

        # Size heuristic - very large objects likely background
        bounds_size = self._get_object_size(obj)
        if bounds_size > 50.0:  # Arbitrary large threshold
            reasons.append(f'Very large object ({bounds_size:.1f})')
            confidence += 0.3

        # Determine final classification
        if confidence > 0.7:
            obj_type = 'background'
        elif confidence < 0.3:
            obj_type = 'product'
        else:
            obj_type = 'other'

        return ObjectClassification(
            type=obj_type,
            confidence=min(confidence, 1.0),
            reasons=reasons
        )

    def _is_in_camera_frustum(self, obj: bpy.types.Object, camera_data: CameraData) -> bool:
        """Check if object is in camera frustum."""
        from .camera_analyzer import CameraAnalyzer
        analyzer = CameraAnalyzer(None)  # Context not needed for this method
        return analyzer.is_in_frustum(obj, camera_data)

    def _average_distance_to_objects(self, obj: bpy.types.Object,
                                   other_objects: List[bpy.types.Object]) -> float:
        """Calculate average distance ke other objects."""
        if not other_objects:
            return 0.0

        total_distance = 0.0
        for other in other_objects:
            distance = (obj.location - other.location).length
            total_distance += distance

        return total_distance / len(other_objects)

    def _get_object_size(self, obj: bpy.types.Object) -> float:
        """Get approximate object size."""
        if not obj.bound_box:
            return 1.0

        # Calculate diagonal of bounding box
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        if not bbox_corners:
            return 1.0

        min_corner = Vector((
            min(c.x for c in bbox_corners),
            min(c.y for c in bbox_corners),
            min(c.z for c in bbox_corners)
        ))

        max_corner = Vector((
            max(c.x for c in bbox_corners),
            max(c.y for c in bbox_corners),
            max(c.z for c in bbox_corners)
        ))

        diagonal = (max_corner - min_corner).length
        return diagonal


__all__ = ['ObjectClassifier', 'ObjectClassification']