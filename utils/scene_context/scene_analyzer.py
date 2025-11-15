"""
SceneAnalyzer - Main facade for all scene analysis operations.
Single entry point untuk default light system, smart template, dan sistem lain.
"""

import bpy
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from mathutils import Vector, Matrix

from .camera_analyzer import CameraAnalyzer, CameraData
from .bounds_calculator import BoundsCalculator, BoundsData
from .material_analyzer import MaterialAnalyzer, MaterialData
from .spatial_analyzer import SpatialAnalyzer, SpatialGraph
from .classification_system import ObjectClassifier, ObjectClassification


@dataclass
class SceneContext:
    """
    Unified scene context data.
    Immutable snapshot of scene state untuk light calculations.

    Field ``product_type`` disiapkan sebagai placeholder untuk menyimpan
    kategori produk scene (mis. jewelry, food, dsb.) ketika sistem
    klasifikasi produk terintegrasi penuh. Untuk saat ini nilainya
    default "unknown" dan boleh diabaikan oleh pemanggil yang belum
    membutuhkannya.
    """
    bounds: BoundsData
    camera: Optional[CameraData] = None
    classifications: Dict[bpy.types.Object, ObjectClassification] = None
    materials: MaterialData = None
    spatial: SpatialGraph = None
    timestamp: float = 0.0
    frame: int = 0
    product_type: str = "unknown"

    def get_background_objects(self) -> List[bpy.types.Object]:
        """Get all background classified objects."""
        if not self.classifications:
            return []
        return [obj for obj, cls in self.classifications.items()
                if cls.type == "background"]

    def get_product_objects(self) -> List[bpy.types.Object]:
        """Get all product/subject objects."""
        if not self.classifications:
            return []
        return [obj for obj, cls in self.classifications.items()
                if cls.type == "product"]


class SceneAnalyzer:
    """
    Unified facade for scene analysis.
    Centralized system untuk menggantikan:
    - obstruction_detector.analyze_scene_enhanced()
    - scene_analysis.classify_objects_by_background()
    - smart_calc.analyze_scene_for_lighting()
    - template_analyzer.analyze_subject() (partial)
    """

    def __init__(self, context: bpy.types.Context):
        self.context = context
        self._camera_analyzer = CameraAnalyzer(context)
        self._bounds_calculator = BoundsCalculator()
        self._material_analyzer = MaterialAnalyzer()
        self._spatial_analyzer = SpatialAnalyzer(context)
        self._classifier = ObjectClassifier()

    def analyze_scene(self,
                     selected_objects: List[bpy.types.Object],
                     include_camera: bool = True,
                     include_classification: bool = True,
                     include_materials: bool = True,
                     include_spatial: bool = False) -> SceneContext:
        """
        Full scene analysis dengan optional components.

        Args:
            selected_objects: Objects yang dipilih sebagai subject
            include_camera: Analyze camera data
            include_classification: Classify all objects
            include_materials: Analyze materials
            include_spatial: Build spatial relationship graph

        Returns:
            SceneContext dengan data lengkap
        """
        import time

        # 1. Bounds (always required)
        bounds = self._bounds_calculator.calculate(selected_objects)

        # 2. Camera (optional)
        camera = None
        if include_camera and self.context.scene.camera:
            camera = self._camera_analyzer.analyze(self.context.scene.camera)

        # 3. Classification (optional)
        classifications = None
        if include_classification:
            all_objects = [obj for obj in self.context.scene.objects
                          if obj.type == 'MESH']
            classifications = self._classifier.classify_objects(
                all_objects, selected_objects, camera
            )

        # 4. Materials (optional)
        materials = None
        if include_materials:
            materials = self._material_analyzer.analyze(selected_objects)

        # 5. Spatial graph (optional - expensive)
        spatial = None
        if include_spatial and classifications:
            spatial = self._spatial_analyzer.build_graph(classifications)

        return SceneContext(
            bounds=bounds,
            camera=camera,
            classifications=classifications,
            materials=materials,
            spatial=spatial,
            timestamp=time.time(),
            frame=self.context.scene.frame_current,
            product_type=getattr(self.context.scene, "lumi_product_type", "unknown"),
        )

    def quick_bounds(self, objects: List[bpy.types.Object]) -> BoundsData:
        """Quick bounds calculation only."""
        return self._bounds_calculator.calculate(objects)

    def quick_classify(self, selected_objects: List[bpy.types.Object]) -> Dict:
        """Quick classification only."""
        all_objects = [obj for obj in self.context.scene.objects
                      if obj.type == 'MESH']
        camera_data = None
        if self.context.scene.camera:
            camera_data = self._camera_analyzer.analyze(self.context.scene.camera)

        return self._classifier.classify_objects(
            all_objects, selected_objects, camera_data
        )

    def check_line_of_sight(self, from_pos: Vector, to_pos: Vector,
                           exclude_objects: List[bpy.types.Object] = None) -> bool:
        """
        Check if there's clear line of sight between two positions.
        Replacement untuk lumi_ray_cast_between_points.
        """
        return self._spatial_analyzer.check_line_of_sight(
            from_pos, to_pos, exclude_objects or []
        )


# Convenience functions untuk backward compatibility
def analyze_scene(context: bpy.types.Context,
                 selected_objects: List[bpy.types.Object]) -> SceneContext:
    """Quick analysis function."""
    analyzer = SceneAnalyzer(context)
    return analyzer.analyze_scene(selected_objects)


__all__ = ['SceneAnalyzer', 'SceneContext', 'analyze_scene']