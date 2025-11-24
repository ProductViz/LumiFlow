"""
SceneAnalyzer - Main facade for all scene analysis operations.
Single entry point untuk default light system, smart template, dan sistem lain.
"""

import bpy
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from mathutils import Vector, Matrix

from .camera_analyzer import CameraAnalyzer, CameraData
from .bounds_calculator import BoundsCalculator, BoundsData
from .material_analyzer import MaterialAnalyzer, MaterialData
from .spatial_analyzer import SpatialAnalyzer, SpatialGraph
from .classification_system import ObjectClassifier, ObjectClassification
from .thickness_analyzer import ThicknessAnalyzer, ThicknessData
from .lighting_analyzer import LightingAnalyzer, LightingData
from .cache_manager import CacheKey, AnalysisCache


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
    lighting: Optional[LightingData] = None
    thickness: Optional[ThicknessData] = None
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

    def get_ground_objects(self) -> List[bpy.types.Object]:
        """Get all background objects yang disubtype sebagai ground."""
        if not self.classifications:
            return []
        return [obj for obj, cls in self.classifications.items()
                if cls.type == "background" and getattr(cls, 'subtype', None) == 'ground']

    def get_backdrop_objects(self) -> List[bpy.types.Object]:
        """Get all background objects yang disubtype sebagai backdrop."""
        if not self.classifications:
            return []
        return [obj for obj, cls in self.classifications.items()
                if cls.type == "background" and getattr(cls, 'subtype', None) == 'backdrop']

    def _object_importance_score(self, obj: bpy.types.Object) -> float:
        """Heuristik sederhana: kombinasi ukuran dan kedekatan ke bounds center."""
        try:
            if not obj.bound_box:
                return 0.0
            bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            min_corner = Vector((
                min(c.x for c in bbox_corners),
                min(c.y for c in bbox_corners),
                min(c.z for c in bbox_corners),
            ))
            max_corner = Vector((
                max(c.x for c in bbox_corners),
                max(c.y for c in bbox_corners),
                max(c.z for c in bbox_corners),
            ))
            size = (max_corner - min_corner).length
        except Exception:
            size = 0.0

        center = getattr(self.bounds, 'center', None)
        if center is not None:
            try:
                dist = (obj.location - center).length
            except Exception:
                dist = 0.0
            # Lebih besar dan lebih dekat ke center = skor lebih tinggi
            return size - dist * 0.1
        return size

    def get_main_product(self) -> Optional[bpy.types.Object]:
        """Dapatkan objek product utama (paling penting)."""
        products = self.get_product_objects()
        if not products:
            return None
        return max(products, key=self._object_importance_score)

    def get_main_ground_for_product(self, product: bpy.types.Object) -> Optional[bpy.types.Object]:
        """Cari ground utama untuk product berdasarkan SpatialGraph dan subtype."""
        if not self.spatial or not getattr(self.spatial, 'edges', None):
            grounds = self.get_ground_objects()
            return grounds[0] if grounds else None

        candidates: List[tuple] = []  # (distance, obj)
        for obj1, obj2, rel in self.spatial.edges:
            if obj1 is not product:
                continue
            rel_type = getattr(rel, 'type', '')
            if rel_type not in ('BELOW', 'NEAR_BACK', 'NEAR_FRONT'):
                continue
            cls = self.classifications.get(obj2)
            if not cls or getattr(cls, 'subtype', None) != 'ground':
                continue
            dist = float(getattr(rel, 'distance', 0.0))
            candidates.append((dist, obj2))

        if not candidates:
            grounds = self.get_ground_objects()
            return grounds[0] if grounds else None

        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    def get_lighting_summary(self) -> Optional[LightingData]:
        """Shortcut untuk akses lighting summary."""
        return self.lighting

    def get_camera_to_product_distance(self) -> float:
        """Jarak antara kamera dan main product (kalau ada)."""
        if not self.camera:
            return 0.0
        main_product = self.get_main_product()
        if not main_product:
            return 0.0
        try:
            return (self.camera.location - main_product.location).length
        except Exception:
            return 0.0


class AnalysisLevel(str, Enum):
    """Preset analysis levels for SceneAnalyzer."""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


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
        self._thickness_analyzer = ThicknessAnalyzer(context)
        self._lighting_analyzer = LightingAnalyzer(context)
        self._cache = AnalysisCache()

    def analyze_scene(self,
                     selected_objects: List[bpy.types.Object],
                     level: AnalysisLevel | str = AnalysisLevel.STANDARD,
                     **override_flags: Any) -> SceneContext:
        """
        Full scene analysis dengan optional components.

        Args:
            selected_objects: Objects yang dipilih sebagai subject
            level: Analysis level preset
            **override_flags: Override flags for specific components

        Returns:
            SceneContext dengan data lengkap
        """
        import time
        # Determine flags based on analysis level

        if isinstance(level, AnalysisLevel):
            level_value = level.value
        else:
            level_value = str(level) if level is not None else AnalysisLevel.STANDARD.value

        if level_value == AnalysisLevel.QUICK.value:
            include_camera = False
            include_classification = False
            include_materials = False
            include_spatial = False
        elif level_value == AnalysisLevel.DEEP.value:
            include_camera = True
            include_classification = True
            include_materials = True
            include_spatial = True
        else:  # STANDARD (default)
            include_camera = True
            include_classification = True
            include_materials = True
            include_spatial = False

        # Apply explicit overrides if provided
        if "include_camera" in override_flags:
            include_camera = override_flags.pop("include_camera")
        if "include_classification" in override_flags:
            include_classification = override_flags.pop("include_classification")
        if "include_materials" in override_flags:
            include_materials = override_flags.pop("include_materials")
        if "include_spatial" in override_flags:
            include_spatial = override_flags.pop("include_spatial")

        # Build cache key berdasarkan frame + selection + effective flags
        selection_hash = self._hash_selection(selected_objects)
        overrides_sig = ""
        if override_flags:
            try:
                overrides_sig = repr(sorted(override_flags.items()))
            except Exception:
                overrides_sig = str(len(override_flags))

        flags_sig = (
            f"{level_value}|cam={int(include_camera)}|cls={int(include_classification)}|"
            f"mat={int(include_materials)}|spat={int(include_spatial)}"
        )

        cache_key = CacheKey(
            frame=self.context.scene.frame_current,
            selection_hash=selection_hash,
            level=flags_sig,
            overrides=overrides_sig,
        )

        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

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

        # 6. Lighting summary (STANDARD & DEEP levels)
        lighting = None
        if level_value in (AnalysisLevel.STANDARD.value, AnalysisLevel.DEEP.value):
            product_center = getattr(bounds, "center", None)
            lighting = self._lighting_analyzer.analyze(
                camera_data=camera,
                product_center=product_center,
            )

        # 7. Thickness (only for DEEP level for now)
        thickness = None
        if level_value == AnalysisLevel.DEEP.value and selected_objects:
            thickness = self._thickness_analyzer.analyze(selected_objects)

        context = SceneContext(
            bounds=bounds,
            camera=camera,
            classifications=classifications,
            materials=materials,
            spatial=spatial,
            lighting=lighting,
            thickness=thickness,
            timestamp=time.time(),
            frame=self.context.scene.frame_current,
            product_type=getattr(self.context.scene, "lumi_product_type", "unknown"),
        )

        self._cache.put(cache_key, context)
        return context

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

    def _hash_selection(self, objects: List[bpy.types.Object]) -> str:
        """Hash sederhana untuk daftar objek + transformasinya.

        Digunakan sebagai bagian dari CacheKey agar analisis yang sama
        (frame, selection, level/flags) bisa diambil dari cache.
        """
        if not objects:
            return "empty"

        parts = []
        for obj in objects:
            try:
                mat = obj.matrix_world
                flat_values = []
                for row in mat:
                    flat_values.extend(row)
                flat_rounded = [round(float(v), 4) for v in flat_values]
                parts.append(f"{obj.name}|{tuple(flat_rounded)}")
            except Exception:
                parts.append(obj.name)

        parts.sort()
        return "||".join(parts)

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


__all__ = ['SceneAnalyzer', 'SceneContext', 'AnalysisLevel', 'analyze_scene']