# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Smart Obstruction Detector
Intelligent detection and classification of scene objects for obstruction analysis.
Distinguishes between products, background objects, and lighting equipment.
"""

import bpy
import re
from typing import Dict, List, Tuple, Optional, Any, Set
from mathutils import Vector
from enum import Enum

# Import LumiFlow utilities
from .common import lumi_get_light_collection


class ObjectType(Enum):
    """Classification of objects in the scene"""
    PRODUCT = "product"           # Main subject to be lit
    BACKGROUND = "background"     # Potential obstructions
    LIGHTING = "lighting"         # Lighting equipment (ignore)
    SUPPORT = "support"           # Support structures (tripods, stands)
    UNKNOWN = "unknown"           # Unclassified


class ObjectClassification:
    """Classification result for a scene object"""

    def __init__(self, obj: bpy.types.Object, obj_type: ObjectType,
                 confidence: float, reasons: List[str]):
        self.object = obj
        self.type = obj_type
        self.confidence = confidence
        self.reasons = reasons
        self.properties = self._extract_properties()

    def _extract_properties(self) -> Dict[str, Any]:
        """Extract relevant properties for analysis"""
        props = {
            'name': self.object.name,
            'type': self.object.type,
            'dimensions': self.object.dimensions if hasattr(self.object, 'dimensions') else Vector(),
            'location': self.object.location.copy(),
            'has_materials': bool(self.object.data and hasattr(self.object.data, 'materials') and self.object.data.materials),
            'material_count': len(self.object.data.materials) if self.object.data and hasattr(self.object.data, 'materials') else 0,
            'vertex_count': len(self.object.data.vertices) if self.object.data and hasattr(self.object.data, 'vertices') else 0,
            'face_count': len(self.object.data.polygons) if self.object.data and hasattr(self.object.data, 'polygons') else 0,
        }

        # Check for custom properties
        if hasattr(self.object, 'get'):
            props['is_lumiflow_light'] = self.object.get('lumi_light_type', None) is not None
            props['lumiflow_pivot'] = self.object.get('Lumi_pivot_world', None)

        return props

    def __repr__(self):
        return f"ObjectClassification({self.object.name}: {self.type.value}, confidence={self.confidence:.2f})"


class SmartObstructionDetector:
    """
    Intelligent detector that classifies scene objects for obstruction analysis.
    """

    # Keywords that indicate lighting equipment
    LIGHTING_KEYWORDS = {
        'light', 'lamp', 'bulb', 'fixture', 'spot', 'flood', 'panel', 'softbox',
        'umbrella', 'reflector', 'diffuser', 'gobo', 'barn', 'flag', 'cutter',
        'snoot', 'grid', 'honeycomb', 'beauty', 'ring', 'led', 'cfl', 'halogen',
        'fluorescent', 'studio', 'photography', 'lighting'
    }

    # Keywords that indicate support structures
    SUPPORT_KEYWORDS = {
        'stand', 'tripod', 'boom', 'arm', 'bracket', 'mount', 'holder', 'clamp',
        'c_stand', 'century_stand', 'background_stand', 'light_stand', 'pole',
        'mast', 'tower', 'platform', 'base', 'foot', 'leg', 'support'
    }

    # Material types that suggest product objects
    PRODUCT_MATERIAL_INDICATORS = {
        'metallic', 'glass', 'plastic', 'fabric', 'leather', 'wood', 'ceramic',
        'stone', 'precious', 'luxury', 'jewelry', 'cosmetic', 'food', 'organic'
    }

    def __init__(self):
        self.classifications = {}
        self.scene_analysis_cache = None

    def analyze_scene(self, context: bpy.types.Context,
                     selected_objects: Optional[List[bpy.types.Object]] = None) -> Dict[str, List[ObjectClassification]]:
        """
        Analyze entire scene and classify all objects.

        Args:
            context: Blender context
            selected_objects: Currently selected objects (if None, use context.selected_objects)

        Returns:
            Dictionary mapping ObjectType to list of classifications
        """
        if selected_objects is None:
            selected_objects = list(context.selected_objects)

        # Clear previous analysis
        self.classifications = {}

        # Get all mesh objects in scene
        all_mesh_objects = [obj for obj in context.scene.objects if obj.type == 'MESH']


        # Classify each object
        for obj in all_mesh_objects:
            classification = self._classify_object(obj, selected_objects, context)
            obj_type = classification.type.value

            if obj_type not in self.classifications:
                self.classifications[obj_type] = []

            self.classifications[obj_type].append(classification)

        # Sort by confidence
        for obj_type in self.classifications:
            self.classifications[obj_type].sort(key=lambda x: x.confidence, reverse=True)

        return self.classifications

    def _classify_object(self, obj: bpy.types.Object,
                         selected_objects: List[bpy.types.Object],
                         context: bpy.types.Context) -> ObjectClassification:
        """
        Classify a single object using multiple heuristics.
        """
        reasons = []
        scores = {obj_type: 0.0 for obj_type in ObjectType}

        # Heuristic 1: Selection status (highest priority)
        if obj in selected_objects:
            scores[ObjectType.PRODUCT] += 0.8
            reasons.append("selected_object")

        # Heuristic 2: LumiFlow light collection
        light_collection = lumi_get_light_collection(context.scene)
        if light_collection and obj.name in light_collection.objects:
            scores[ObjectType.LIGHTING] += 1.0
            reasons.append("in_light_collection")

        # Heuristic 3: Custom properties
        if hasattr(obj, 'get'):
            if obj.get('lumi_light_type') is not None:
                scores[ObjectType.LIGHTING] += 1.0
                reasons.append("lumiflow_light_property")
            if obj.get('Lumi_pivot_world') is not None:
                scores[ObjectType.LIGHTING] += 0.5
                reasons.append("lumiflow_pivot_property")

        # Heuristic 4: Object name analysis
        name_lower = obj.name.lower()
        lighting_score = self._check_name_keywords(name_lower, self.LIGHTING_KEYWORDS)
        support_score = self._check_name_keywords(name_lower, self.SUPPORT_KEYWORDS)

        if lighting_score > 0:
            scores[ObjectType.LIGHTING] += lighting_score * 0.7
            reasons.append("name_contains_lighting_keywords")
        if support_score > 0:
            scores[ObjectType.SUPPORT] += support_score * 0.6
            reasons.append("name_contains_support_keywords")

        # Heuristic 5: Material analysis
        material_info = self._analyze_object_materials(obj)
        if material_info['has_emission']:
            scores[ObjectType.LIGHTING] += 0.9
            reasons.append("emission_material")

        product_material_score = self._check_material_keywords(material_info)
        if product_material_score > 0:
            scores[ObjectType.PRODUCT] += product_material_score * 0.4
            reasons.append("product_material_indicators")

        # Heuristic 6: Size and scale analysis
        size_score = self._analyze_object_size(obj, context)
        if size_score['is_large']:
            scores[ObjectType.BACKGROUND] += 0.3
            reasons.append("large_scale_object")
        if size_score['is_small']:
            scores[ObjectType.PRODUCT] += 0.2
            reasons.append("small_scale_object")

        # Heuristic 7: Geometric complexity
        complexity_score = self._analyze_geometric_complexity(obj)
        if complexity_score > 0.8:
            scores[ObjectType.PRODUCT] += 0.3
            reasons.append("high_geometric_complexity")
        elif complexity_score < 0.2:
            scores[ObjectType.BACKGROUND] += 0.2
            reasons.append("low_geometric_complexity")

        # Determine final classification
        best_type = max(scores.keys(), key=lambda x: scores[x])
        confidence = scores[best_type]

        # Apply minimum confidence threshold
        if confidence < 0.1:
            best_type = ObjectType.UNKNOWN
            confidence = 0.0


        return ObjectClassification(obj, best_type, confidence, reasons)

    def _check_name_keywords(self, name: str, keywords: Set[str]) -> float:
        """Check how many keywords are present in object name"""
        found_keywords = 0
        for keyword in keywords:
            if keyword in name:
                found_keywords += 1
        return min(1.0, found_keywords / 3.0)  # Cap at 3 keywords

    def _analyze_object_materials(self, obj: bpy.types.Object) -> Dict[str, Any]:
        """Analyze materials of an object"""
        material_info = {
            'has_emission': False,
            'dominant_type': 'dielectric',
            'material_names': [],
            'emission_strength': 0.0
        }

        try:
            if not obj.data or not hasattr(obj.data, 'materials'):
                return material_info

            for mat_slot in obj.material_slots:
                if not mat_slot.material:
                    continue

                material = mat_slot.material
                material_info['material_names'].append(material.name.lower())

                # Check for emission
                if material.use_nodes:
                    for node in material.node_tree.nodes:
                        if node.type == 'EMISSION':
                            material_info['has_emission'] = True
                            if hasattr(node.inputs, 'Strength'):
                                strength = node.inputs['Strength'].default_value
                                material_info['emission_strength'] = max(material_info['emission_strength'], strength)
                        elif node.type == 'BSDF_PRINCIPLED':
                            emission_input = node.inputs.get('Emission')
                            if emission_input:
                                emission_color = emission_input.default_value
                                if len(emission_color) >= 3 and any(c > 0.01 for c in emission_color[:3]):
                                    material_info['has_emission'] = True
                                    material_info['emission_strength'] = max(material_info['emission_strength'],
                                                                           sum(emission_color[:3]) / 3.0)

        except Exception as e:
            pass

        return material_info

    def _check_material_keywords(self, material_info: Dict[str, Any]) -> float:
        """Check material names for product indicators"""
        score = 0.0
        for mat_name in material_info['material_names']:
            for indicator in self.PRODUCT_MATERIAL_INDICATORS:
                if indicator in mat_name:
                    score += 0.3
                    break
        return min(1.0, score)

    def _analyze_object_size(self, obj: bpy.types.Object, context: bpy.types.Context) -> Dict[str, Any]:
        """Analyze object size relative to scene"""
        result = {'is_large': False, 'is_small': False, 'relative_size': 1.0}

        try:
            # Get object dimensions
            if hasattr(obj, 'dimensions'):
                obj_size = max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z)
            else:
                obj_size = 1.0

            # Compare to scene scale
            scene_scale = getattr(context.scene.unit_settings, 'scale_length', 1.0)

            # Get average size of all mesh objects for comparison
            all_mesh = [o for o in context.scene.objects if o.type == 'MESH' and o != obj]
            if all_mesh:
                avg_size = sum(max(o.dimensions.x, o.dimensions.y, o.dimensions.z)
                             for o in all_mesh if hasattr(o, 'dimensions')) / len(all_mesh)
                result['relative_size'] = obj_size / avg_size if avg_size > 0 else 1.0

                if result['relative_size'] > 2.0:
                    result['is_large'] = True
                elif result['relative_size'] < 0.3:
                    result['is_small'] = True

        except Exception as e:
            pass

        return result

    def _analyze_geometric_complexity(self, obj: bpy.types.Object) -> float:
        """Analyze geometric complexity of object"""
        try:
            if not obj.data or not hasattr(obj.data, 'vertices') or not hasattr(obj.data, 'polygons'):
                return 0.0

            vertex_count = len(obj.data.vertices)
            face_count = len(obj.data.polygons)

            if face_count == 0 or vertex_count == 0:
                return 0.0
    
            # Complexity based on faces per vertex ratio
            complexity = face_count / vertex_count

            # Normalize to 0-1 range (typical range 0.5-3.0)
            normalized = min(1.0, complexity / 2.0)

            return normalized

        except Exception as e:
            return 0.0

    def get_target_objects(self, classifications: Optional[Dict[str, List[ObjectClassification]]] = None) -> List[bpy.types.Object]:
        """Get objects classified as products/targets"""
        if classifications is None:
            classifications = self.classifications

        targets = []
        if ObjectType.PRODUCT.value in classifications:
            targets.extend([cls.object for cls in classifications[ObjectType.PRODUCT.value]])

        return targets

    def get_background_objects(self, classifications: Optional[Dict[str, List[ObjectClassification]]] = None) -> List[bpy.types.Object]:
        """Get objects classified as background/potential obstructions"""
        if classifications is None:
            classifications = self.classifications

        background = []
        if ObjectType.BACKGROUND.value in classifications:
            background.extend([cls.object for cls in classifications[ObjectType.BACKGROUND.value]])

        return background

    def get_lighting_objects(self, classifications: Optional[Dict[str, List[ObjectClassification]]] = None) -> List[bpy.types.Object]:
        """Get objects classified as lighting equipment"""
        if classifications is None:
            classifications = self.classifications

        lighting = []
        if ObjectType.LIGHTING.value in classifications:
            lighting.extend([cls.object for cls in classifications[ObjectType.LIGHTING.value]])

        return lighting

    def get_obstruction_candidates(self, classifications: Optional[Dict[str, List[ObjectClassification]]] = None) -> List[bpy.types.Object]:
        """Get all objects that could be obstructions (background + unknown)"""
        if classifications is None:
            classifications = self.classifications

        candidates = []
        for obj_type in [ObjectType.BACKGROUND, ObjectType.UNKNOWN]:
            if obj_type.value in classifications:
                candidates.extend([cls.object for cls in classifications[obj_type.value]])

        return candidates

    def print_analysis_summary(self, classifications: Optional[Dict[str, List[ObjectClassification]]] = None):
        """Print summary of object classifications"""
        if classifications is None:
            classifications = self.classifications

        print("\n=== Smart Obstruction Detector Analysis ===")

        for obj_type, cls_list in classifications.items():
            print(f"{obj_type.upper()}: {len(cls_list)} objects")
            for cls in cls_list[:5]:  # Show top 5
                print(f"  - {cls.object.name} (confidence: {cls.confidence:.2f})")
                if cls.reasons:
                    print(f"    Reasons: {', '.join(cls.reasons[:3])}")
            if len(cls_list) > 5:
                print(f"  ... and {len(cls_list) - 5} more")

        print("=== End Analysis ===\n")


# Global instance for easy access
_detector_instance = None

def get_smart_obstruction_detector() -> SmartObstructionDetector:
    """Get global instance of the detector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SmartObstructionDetector()
    return _detector_instance


def analyze_scene_for_obstructions(context: bpy.types.Context,
                                 selected_objects: Optional[List[bpy.types.Object]] = None) -> Dict[str, List[ObjectClassification]]:
    """
    Convenience function to analyze scene and get classifications.

    Args:
        context: Blender context
        selected_objects: Selected objects (optional)

    Returns:
        Dictionary of object classifications by type
    """
    detector = get_smart_obstruction_detector()
    return detector.analyze_scene(context, selected_objects)


# Export functions
__all__ = [
    'ObjectType',
    'ObjectClassification',
    'SmartObstructionDetector',
    'get_smart_obstruction_detector',
    'analyze_scene_for_obstructions'
]