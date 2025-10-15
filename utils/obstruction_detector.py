# LumiFlow - Enhanced Smart Obstruction Detector
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Enhanced Smart Obstruction Detector
Menggunakan metode spatial analysis, bounding box comparison, dan
camera frustum analysis untuk pemisahan background yang lebih akurat.
"""

import bpy
import logging
import bmesh
from typing import Dict, List, Tuple, Optional, Any, Set
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from enum import Enum
import math

logger = logging.getLogger(__name__)

class ObjectType(Enum):
    """Classification of objects in the scene"""
    PRODUCT = "product"
    BACKGROUND = "background"
    LIGHTING = "lighting"
    SUPPORT = "support"
    UNKNOWN = "unknown"


class SpatialRelationship(Enum):
    """Spatial relationship between objects"""
    IN_FRONT = "in_front"
    BEHIND = "behind"
    BESIDE = "beside"
    ABOVE = "above"
    BELOW = "below"
    OVERLAPPING = "overlapping"


class EnhancedBackgroundDetector:
    """
    Enhanced detector menggunakan spatial analysis dan camera-based detection
    """
    
    # Keywords untuk klasifikasi
    LIGHTING_KEYWORDS = {
        'light', 'lamp', 'bulb', 'fixture', 'spot', 'flood', 'panel', 
        'softbox', 'umbrella', 'reflector', 'led', 'studio'
    }
    
    BACKGROUND_KEYWORDS = {
        'background', 'backdrop', 'back', 'bg', 'floor', 'ground', 
        'wall', 'ceiling', 'seamless', 'cyc', 'cyclorama'
    }
    
    def __init__(self):
        self.classifications = {}
        self.spatial_graph = {}  # Graph of spatial relationships
        self.scene_bounds = None
        self.camera_info = None
        
    def analyze_scene(self, context: bpy.types.Context,
                     selected_objects: Optional[List[bpy.types.Object]] = None,
                     auto_detect_subject: bool = True) -> Dict[str, List]:
        """
        Enhanced scene analysis dengan auto-detection
        
        Args:
            context: Blender context
            selected_objects: Pre-selected objects (optional)
            auto_detect_subject: Auto-detect main subject if no selection
        """
        self.classifications = {}
        
        # Get all mesh objects
        all_objects = [obj for obj in context.scene.objects if obj.type == 'MESH']
        
        # Build spatial graph
        self._build_spatial_graph(all_objects, context)
        
        # Get camera info
        self._analyze_camera(context)
        
        # Calculate scene bounds
        self._calculate_scene_bounds(all_objects)
        
        # Detect subject/product
        if selected_objects and len(selected_objects) > 0:
            subject_objects = selected_objects
        elif auto_detect_subject:
            subject_objects = self._auto_detect_subject(all_objects, context)
        else:
            subject_objects = []
        
        # Classify each object
        for obj in all_objects:
            classification = self._enhanced_classify(obj, subject_objects, 
                                                    all_objects, context)
            obj_type = classification['type'].value
            
            if obj_type not in self.classifications:
                self.classifications[obj_type] = []
            
            self.classifications[obj_type].append(classification)
        
        # Sort by confidence
        for obj_type in self.classifications:
            self.classifications[obj_type].sort(
                key=lambda x: x['confidence'], reverse=True
            )
        
        return self.classifications
    
    def _build_spatial_graph(self, objects: List[bpy.types.Object], 
                            context: bpy.types.Context):
        """Build graph of spatial relationships between objects"""
        self.spatial_graph = {}
        
        for obj in objects:
            self.spatial_graph[obj.name] = {
                'object': obj,
                'bbox': self._get_world_bbox(obj),
                'center': self._get_world_center(obj),
                'relationships': {}
            }
        
        # Calculate relationships
        for obj1_name, obj1_data in self.spatial_graph.items():
            for obj2_name, obj2_data in self.spatial_graph.items():
                if obj1_name == obj2_name:
                    continue
                
                relationship = self._calculate_spatial_relationship(
                    obj1_data, obj2_data, context
                )
                obj1_data['relationships'][obj2_name] = relationship
    
    def _calculate_spatial_relationship(self, obj1_data: Dict, 
                                       obj2_data: Dict,
                                       context: bpy.types.Context) -> Dict:
        """Calculate spatial relationship between two objects"""
        center1 = obj1_data['center']
        center2 = obj2_data['center']
        bbox1 = obj1_data['bbox']
        bbox2 = obj2_data['bbox']
        
        # Calculate relative position
        direction = center2 - center1
        distance = direction.length
        
        if distance > 0:
            direction.normalize()
        
        # Check camera-relative position if camera exists
        camera_relative = None
        if context.scene.camera:
            camera_relative = self._get_camera_relative_position(
                obj1_data, obj2_data, context.scene.camera
            )
        
        # Check bounding box overlap
        overlapping = self._check_bbox_overlap(bbox1, bbox2)
        
        return {
            'distance': distance,
            'direction': direction,
            'overlapping': overlapping,
            'camera_relative': camera_relative
        }
    
    def _get_camera_relative_position(self, obj1_data: Dict, 
                                     obj2_data: Dict,
                                     camera: bpy.types.Object) -> str:
        """Get relative position of obj2 to obj1 from camera perspective"""
        camera_pos = camera.location
        camera_forward = camera.matrix_world.to_quaternion() @ Vector((0, 0, -1))
        
        center1 = obj1_data['center']
        center2 = obj2_data['center']
        
        # Vectors from camera to objects
        to_obj1 = (center1 - camera_pos).normalized()
        to_obj2 = (center2 - camera_pos).normalized()
        
        # Calculate angles
        angle = math.degrees(to_obj1.angle(to_obj2))
        
        # Distance from camera
        dist1 = (center1 - camera_pos).length
        dist2 = (center2 - camera_pos).length
        
        # Determine position
        if dist2 > dist1 * 1.2 and angle < 30:
            return "behind"
        elif dist2 < dist1 * 0.8 and angle < 30:
            return "in_front"
        elif angle > 60:
            return "beside"
        else:
            return "overlapping"
    
    def _get_world_bbox(self, obj: bpy.types.Object) -> Tuple[Vector, Vector]:
        """Get world-space bounding box"""
        if not obj.data or not hasattr(obj.data, 'vertices'):
            return (obj.location.copy(), obj.location.copy())
        
        bbox_corners = [obj.matrix_world @ Vector(corner) 
                       for corner in obj.bound_box]
        
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
    
    def _get_world_center(self, obj: bpy.types.Object) -> Vector:
        """Get world-space center"""
        min_corner, max_corner = self._get_world_bbox(obj)
        return (min_corner + max_corner) / 2
    
    def _check_bbox_overlap(self, bbox1: Tuple[Vector, Vector], 
                           bbox2: Tuple[Vector, Vector]) -> bool:
        """Check if two bounding boxes overlap"""
        min1, max1 = bbox1
        min2, max2 = bbox2
        
        return (min1.x <= max2.x and max1.x >= min2.x and
                min1.y <= max2.y and max1.y >= min2.y and
                min1.z <= max2.z and max1.z >= min2.z)
    
    def _analyze_camera(self, context: bpy.types.Context):
        """Analyze camera and calculate frustum"""
        if not context.scene.camera:
            self.camera_info = None
            return
        
        camera = context.scene.camera
        
        self.camera_info = {
            'object': camera,
            'location': camera.location.copy(),
            'forward': camera.matrix_world.to_quaternion() @ Vector((0, 0, -1)),
            'up': camera.matrix_world.to_quaternion() @ Vector((0, 1, 0)),
            'right': camera.matrix_world.to_quaternion() @ Vector((1, 0, 0)),
            'fov': self._get_camera_fov(camera, context)
        }
    
    def _get_camera_fov(self, camera: bpy.types.Object, 
                       context: bpy.types.Context) -> float:
        """Get camera field of view in radians"""
        if camera.data.type == 'PERSP':
            return camera.data.angle
        else:
            # For ortho, use approximation
            return math.radians(60)
    
    def _calculate_scene_bounds(self, objects: List[bpy.types.Object]):
        """Calculate overall scene bounds"""
        if not objects:
            self.scene_bounds = None
            return
        
        all_corners = []
        for obj in objects:
            if obj.name in self.spatial_graph:
                bbox = self.spatial_graph[obj.name]['bbox']
                all_corners.extend([bbox[0], bbox[1]])
        
        if not all_corners:
            self.scene_bounds = None
            return
        
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
        
        self.scene_bounds = {
            'min': min_corner,
            'max': max_corner,
            'center': (min_corner + max_corner) / 2,
            'size': max_corner - min_corner
        }
    
    def _auto_detect_subject(self, objects: List[bpy.types.Object],
                            context: bpy.types.Context) -> List[bpy.types.Object]:
        """
        Auto-detect main subject using multiple criteria:
        1. Camera proximity and visibility
        2. Object size (medium-sized objects)
        3. Central position in scene
        4. High geometric complexity
        5. Rich materials
        """
        if not objects or not self.camera_info:
            return []
        
        subject_scores = {}
        
        camera_pos = self.camera_info['location']
        camera_forward = self.camera_info['forward']
        
        for obj in objects:
            if obj.name not in self.spatial_graph:
                continue
            
            score = 0.0
            obj_data = self.spatial_graph[obj.name]
            obj_center = obj_data['center']
            
            # 1. Camera alignment score
            to_obj = (obj_center - camera_pos).normalized()
            alignment = camera_forward.dot(to_obj)
            if alignment > 0:  # In front of camera
                score += alignment * 2.0
            
            # 2. Distance score (prefer medium distance)
            distance = (obj_center - camera_pos).length
            optimal_distance = 5.0  # Can be adjusted
            distance_score = 1.0 - abs(distance - optimal_distance) / optimal_distance
            distance_score = max(0, distance_score)
            score += distance_score * 1.5
            
            # 3. Centrality score
            if self.scene_bounds:
                scene_center = self.scene_bounds['center']
                to_center_dist = (obj_center - scene_center).length
                scene_size = self.scene_bounds['size'].length
                centrality = 1.0 - (to_center_dist / (scene_size / 2))
                centrality = max(0, centrality)
                score += centrality * 1.0
            
            # 4. Size score (prefer medium-sized)
            bbox = obj_data['bbox']
            obj_size = (bbox[1] - bbox[0]).length
            if self.scene_bounds:
                scene_size = self.scene_bounds['size'].length
                relative_size = obj_size / scene_size
                # Prefer objects that are 10-40% of scene size
                if 0.1 <= relative_size <= 0.4:
                    score += 1.5
                elif relative_size < 0.1:
                    score -= 0.5
            
            # 5. Complexity score
            complexity = self._get_geometric_complexity(obj)
            score += complexity * 0.8
            
            # 6. Material richness score
            material_score = self._get_material_richness(obj)
            score += material_score * 0.5
            
            subject_scores[obj.name] = {
                'object': obj,
                'score': score
            }
        
        # Select top candidates (above threshold)
        threshold = 3.0
        subjects = [
            data['object'] for name, data in subject_scores.items()
            if data['score'] >= threshold
        ]
        
        # If no subjects found, take top 1-3 highest scores
        if not subjects:
            sorted_scores = sorted(subject_scores.items(), 
                                 key=lambda x: x[1]['score'], 
                                 reverse=True)
            subjects = [data['object'] for name, data in sorted_scores[:3]]
        
        return subjects
    
    def _get_geometric_complexity(self, obj: bpy.types.Object) -> float:
        """Calculate geometric complexity (0-1)"""
        if not obj.data or not hasattr(obj.data, 'vertices'):
            return 0.0
        
        try:
            vert_count = len(obj.data.vertices)
            face_count = len(obj.data.polygons)
            
            if face_count == 0:
                return 0.0
            
            # Normalize based on expected ranges
            complexity = min(1.0, (vert_count / 1000) * 0.5 + (face_count / 500) * 0.5)
            return complexity
        except:
            return 0.0
    
    def _get_material_richness(self, obj: bpy.types.Object) -> float:
        """Calculate material richness (0-1)"""
        if not obj.data or not hasattr(obj.data, 'materials'):
            return 0.0
        
        try:
            mat_count = len([m for m in obj.data.materials if m])
            
            # Check for shader complexity
            shader_complexity = 0
            for mat in obj.data.materials:
                if mat and mat.use_nodes:
                    shader_complexity += len(mat.node_tree.nodes)
            
            richness = min(1.0, (mat_count / 5) * 0.5 + (shader_complexity / 20) * 0.5)
            return richness
        except Exception as e:
            logger.debug(f"Cannot check material richness: {e}")
            return 0.0
    
    def _analyze_materials(self, obj: bpy.types.Object) -> Dict:
        """Analyze object materials"""
        result = {'has_emission': False}
        
        try:
            if not obj.data or not hasattr(obj.data, 'materials'):
                return result
            
            for mat_slot in obj.material_slots:
                if not mat_slot.material:
                    continue
                
                mat = mat_slot.material
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'EMISSION':
                            result['has_emission'] = True
                            return result
        except Exception as e:
            logger.debug(f"Cannot check material emission: {e}")
        
        return result
    
    def _create_classification_result(self, obj: bpy.types.Object,
                                     obj_type: ObjectType,
                                     confidence: float,
                                     reasons: List[str]) -> Dict:
        """Create classification result dictionary"""
        return {
            'object': obj,
            'type': obj_type,
            'confidence': confidence,
            'reasons': reasons
        }
    
    # === PUBLIC API METHODS ===
    
    def get_background_objects(self) -> List[bpy.types.Object]:
        """Get objects classified as background"""
        if ObjectType.BACKGROUND.value not in self.classifications:
            return []
        return [c['object'] for c in self.classifications[ObjectType.BACKGROUND.value]]
    
    def get_product_objects(self) -> List[bpy.types.Object]:
        """Get objects classified as products"""
        if ObjectType.PRODUCT.value not in self.classifications:
            return []
        return [c['object'] for c in self.classifications[ObjectType.PRODUCT.value]]
    
    def print_analysis(self):
        """Print analysis summary"""
        print("\n=== Enhanced Background Detection Analysis ===")
        
        for obj_type_name, classifications in self.classifications.items():
            print(f"\n{obj_type_name.upper()}: {len(classifications)} objects")
            for cls in classifications[:5]:
                print(f"  - {cls['object'].name}")
                print(f"    Confidence: {cls['confidence']:.2f}")
                print(f"    Reasons: {', '.join(cls['reasons'][:3])}")
            
            if len(classifications) > 5:
                print(f"  ... and {len(classifications) - 5} more")


# Global instance
_detector_instance = None


def get_enhanced_detector() -> EnhancedBackgroundDetector:
    """Get global instance of enhanced detector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = EnhancedBackgroundDetector()
    return _detector_instance


def analyze_scene_enhanced(context: bpy.types.Context,
                          selected_objects: Optional[List[bpy.types.Object]] = None,
                          auto_detect: bool = True) -> Dict[str, List]:
    """
    Convenience function for enhanced scene analysis
    
    Args:
        context: Blender context
        selected_objects: Pre-selected subject objects
        auto_detect: Auto-detect subject if no selection
    
    Returns:
        Classifications dictionary
    """
    detector = get_enhanced_detector()
    return detector.analyze_scene(context, selected_objects, auto_detect)


# === INTEGRATION WITH EXISTING CODE ===

class BackgroundDetectorAdapter:
    """
    Adapter class untuk integrasi dengan kode existing
    Menyediakan interface yang sama dengan SmartObstructionDetector
    """
    
    def __init__(self):
        self.detector = EnhancedBackgroundDetector()
        self.classifications = {}
    
    def analyze_scene(self, context: bpy.types.Context,
                     selected_objects: Optional[List[bpy.types.Object]] = None) -> Dict:
        """
        Analyze scene dan convert ke format ObjectClassification lama
        """
        # Run enhanced analysis
        enhanced_results = self.detector.analyze_scene(
            context, selected_objects, auto_detect=True
        )
        
        # Convert to old format for compatibility
        converted = {}
        for obj_type_name, classifications in enhanced_results.items():
            converted[obj_type_name] = []
            
            for cls in classifications:
                # Create ObjectClassification-like object
                old_format = type('ObjectClassification', (), {
                    'object': cls['object'],
                    'type': cls['type'],
                    'confidence': cls['confidence'],
                    'reasons': cls['reasons']
                })()
                
                converted[obj_type_name].append(old_format)
        
        self.classifications = converted
        return converted
    
    def get_target_objects(self) -> List[bpy.types.Object]:
        """Get product/target objects"""
        return self.detector.get_product_objects()
    
    def get_background_objects(self) -> List[bpy.types.Object]:
        """Get background objects"""
        return self.detector.get_background_objects()
    
    def get_obstruction_candidates(self) -> List[bpy.types.Object]:
        """Get potential obstruction objects"""
        bg_objects = self.get_background_objects()
        
        # Add unknown objects as potential obstructions
        if ObjectType.UNKNOWN.value in self.classifications:
            unknown_objects = [cls.object for cls in 
                             self.classifications[ObjectType.UNKNOWN.value]]
            bg_objects.extend(unknown_objects)
        
        return bg_objects


# === USAGE EXAMPLES ===

def example_basic_usage():
    """Example: Basic usage"""
    import bpy
    
    context = bpy.context
    
    # Method 1: Auto-detect everything
    detector = get_enhanced_detector()
    results = detector.analyze_scene(context, auto_detect=True)
    
    # Get background objects
    backgrounds = detector.get_background_objects()
    print(f"Found {len(backgrounds)} background objects")
    
    # Get products
    products = detector.get_product_objects()
    print(f"Found {len(products)} product objects")


def example_with_selection():
    """Example: With pre-selected objects"""
    import bpy
    
    context = bpy.context
    selected = list(context.selected_objects)
    
    detector = get_enhanced_detector()
    results = detector.analyze_scene(context, selected_objects=selected)
    
    detector.print_analysis()


def example_compatible_mode():
    """Example: Using adapter for compatibility"""
    import bpy
    
    context = bpy.context
    
    # Use adapter for old code compatibility
    adapter = BackgroundDetectorAdapter()
    results = adapter.analyze_scene(context)
    
    # Use old API methods
    targets = adapter.get_target_objects()
    backgrounds = adapter.get_background_objects()
    obstructions = adapter.get_obstruction_candidates()


# === ADVANCED FEATURES ===

class AdaptiveThresholdCalculator:
    """
    Calculate adaptive thresholds based on scene characteristics
    """
    
    @staticmethod
    def calculate_distance_threshold(scene_bounds: Dict) -> float:
        """Calculate adaptive distance threshold"""
        if not scene_bounds:
            return 5.0  # Default
        
        scene_size = scene_bounds['size'].length
        # Use 20% of scene size as threshold
        return scene_size * 0.2
    
    @staticmethod
    def calculate_size_threshold(subject_sizes: List[float]) -> Dict[str, float]:
        """Calculate adaptive size thresholds"""
        if not subject_sizes:
            return {'large': 3.0, 'small': 0.5}
        
        avg_size = sum(subject_sizes) / len(subject_sizes)
        
        return {
            'large': avg_size * 3.0,
            'small': avg_size * 0.3
        }


class CameraFrustumAnalyzer:
    """
    Advanced camera frustum analysis for better background detection
    """
    
    def __init__(self, camera: bpy.types.Object, context: bpy.types.Context):
        self.camera = camera
        self.context = context
        self.frustum_planes = self._calculate_frustum_planes()
    
    def _calculate_frustum_planes(self) -> List[Tuple[Vector, Vector]]:
        """Calculate camera frustum planes"""
        # Get camera parameters
        cam_data = self.camera.data
        cam_matrix = self.camera.matrix_world
        
        # Calculate frustum corners
        aspect_ratio = self.context.scene.render.resolution_x / self.context.scene.render.resolution_y
        
        if cam_data.type == 'PERSP':
            fov = cam_data.angle
        else:
            fov = math.radians(60)
        
        # Near and far planes
        near = cam_data.clip_start
        far = cam_data.clip_end
        
        # Calculate frustum geometry
        near_height = 2.0 * math.tan(fov / 2.0) * near
        near_width = near_height * aspect_ratio
        
        far_height = 2.0 * math.tan(fov / 2.0) * far
        far_width = far_height * aspect_ratio
        
        # Frustum corners in camera space
        corners = []
        
        # Near plane corners
        corners.append(Vector((-near_width/2, -near_height/2, -near)))
        corners.append(Vector((near_width/2, -near_height/2, -near)))
        corners.append(Vector((near_width/2, near_height/2, -near)))
        corners.append(Vector((-near_width/2, near_height/2, -near)))
        
        # Far plane corners
        corners.append(Vector((-far_width/2, -far_height/2, -far)))
        corners.append(Vector((far_width/2, -far_height/2, -far)))
        corners.append(Vector((far_width/2, far_height/2, -far)))
        corners.append(Vector((-far_width/2, far_height/2, -far)))
        
        # Transform to world space
        world_corners = [cam_matrix @ corner for corner in corners]
        
        # Calculate planes (stored as point + normal)
        planes = []
        
        # Near plane
        planes.append(self._plane_from_points(
            world_corners[0], world_corners[1], world_corners[2]
        ))
        
        # Far plane
        planes.append(self._plane_from_points(
            world_corners[4], world_corners[5], world_corners[6]
        ))
        
        # Side planes
        # Left
        planes.append(self._plane_from_points(
            world_corners[0], world_corners[4], world_corners[3]
        ))
        
        # Right
        planes.append(self._plane_from_points(
            world_corners[1], world_corners[2], world_corners[5]
        ))
        
        # Top
        planes.append(self._plane_from_points(
            world_corners[2], world_corners[3], world_corners[6]
        ))
        
        # Bottom
        planes.append(self._plane_from_points(
            world_corners[0], world_corners[1], world_corners[4]
        ))
        
        return planes
    
    def _plane_from_points(self, p1: Vector, p2: Vector, p3: Vector) -> Tuple[Vector, Vector]:
        """Calculate plane from 3 points"""
        v1 = p2 - p1
        v2 = p3 - p1
        normal = v1.cross(v2).normalized()
        return (p1, normal)
    
    def is_in_frustum(self, point: Vector) -> bool:
        """Check if point is inside camera frustum"""
        for plane_point, plane_normal in self.frustum_planes:
            to_point = point - plane_point
            if to_point.dot(plane_normal) < 0:
                return False
        return True
    
    def get_frustum_distance(self, point: Vector) -> float:
        """Get minimum distance from point to frustum boundaries"""
        min_dist = float('inf')
        
        for plane_point, plane_normal in self.frustum_planes:
            to_point = point - plane_point
            dist = abs(to_point.dot(plane_normal))
            min_dist = min(min_dist, dist)
        
        return min_dist


# === INTEGRATION HELPER ===

def replace_obstruction_detector_in_registration():
    """
    Helper function untuk mengganti SmartObstructionDetector
    dengan EnhancedBackgroundDetector di registration.py
    
    Tambahkan ke registration.py:
    
    from .utils.obstruction_detector import (
        get_enhanced_detector,
        BackgroundDetectorAdapter
    )
    
    # Ganti semua penggunaan get_smart_obstruction_detector()
    # dengan get_enhanced_detector() atau BackgroundDetectorAdapter()
    """
    pass


# === EXPORT ===

__all__ = [
    'ObjectType',
    'EnhancedBackgroundDetector',
    'BackgroundDetectorAdapter',
    'get_enhanced_detector',
    'analyze_scene_enhanced',
    'AdaptiveThresholdCalculator',
    'CameraFrustumAnalyzer'
]