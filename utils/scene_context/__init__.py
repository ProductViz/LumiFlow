"""
Scene Context System - Unified scene analysis for LumiFlow.

Main exports:
- SceneAnalyzer: Main facade class
- SceneContext: Data container
- analyze_scene(): Quick function

Enhanced with (Phase 1):
- ProductCategoryDetector: Detects product category (jewelry, food, etc.)
- MaterialType/MaterialSubtype: Enhanced material classification

Light Intelligence (Phase 2):
- LightRoleAnalyzer: Detects light roles (KEY, FILL, BACK, RIM, ACCENT)
- CompositionAnalyzer: Analyzes lighting composition and style
- NeededLightRecommender: Recommends next light to add

Usage:
    from utils.scene_context import (
        SceneAnalyzer, ProductCategoryDetector,
        LightRoleAnalyzer, CompositionAnalyzer, NeededLightRecommender
    )

    analyzer = SceneAnalyzer(context)
    scene_ctx = analyzer.analyze_scene(context.selected_objects)

    # Product category detection
    detector = ProductCategoryDetector()
    category = detector.detect(objects, scene_ctx.materials, scene_ctx.bounds)
    
    # Light role analysis
    role_analyzer = LightRoleAnalyzer(context)
    light_roles = role_analyzer.analyze(scene_ctx.camera, scene_ctx.bounds.center)
    
    # Composition analysis
    comp_analyzer = CompositionAnalyzer()
    composition = comp_analyzer.analyze(light_roles)
    
    # Light recommendation
    recommender = NeededLightRecommender()
    recommendation = recommender.recommend(composition, category)
"""

from .scene_analyzer import SceneAnalyzer, SceneContext, AnalysisLevel, analyze_scene
from .camera_analyzer import CameraAnalyzer, CameraData, FrustumPlane
from .bounds_calculator import BoundsCalculator, BoundsData
from .material_analyzer import MaterialAnalyzer, MaterialData, MaterialType, MaterialSubtype
from .spatial_analyzer import SpatialAnalyzer, SpatialGraph
from .classification_system import ObjectClassifier, ObjectClassification
from .thickness_analyzer import ThicknessAnalyzer, ThicknessData, ObjectThicknessData
from .lighting_analyzer import LightingAnalyzer, LightingData
from .product_category_detector import (
    ProductCategoryDetector,
    ProductCategoryResult,
    ProductCategory,
    ProductSubcategory,
    CATEGORY_LIGHTING_PARAMS,
)
from .light_role_analyzer import (
    LightRoleAnalyzer,
    LightRoleResult,
    LightRole,
    DirectionCategory,
)
from .composition_analyzer import (
    CompositionAnalyzer,
    CompositionAnalysisResult,
    LightingStyle,
    CompositionQuality,
)
from .needed_light_recommender import (
    NeededLightRecommender,
    LightRecommendation,
    RecommendationPriority,
)

__all__ = [
    # Core analyzers
    'SceneAnalyzer',
    'SceneContext',
    'AnalysisLevel',
    'analyze_scene',
    'CameraAnalyzer',
    'CameraData',
    'BoundsCalculator',
    'BoundsData',
    'MaterialAnalyzer',
    'MaterialData',
    'MaterialType',
    'MaterialSubtype',
    'SpatialAnalyzer',
    'SpatialGraph',
    'ObjectClassifier',
    'ObjectClassification',
    'ThicknessAnalyzer',
    'ThicknessData',
    'ObjectThicknessData',
    'LightingAnalyzer',
    'LightingData',
    # Product category detection (Phase 1)
    'ProductCategoryDetector',
    'ProductCategoryResult',
    'ProductCategory',
    'ProductSubcategory',
    'CATEGORY_LIGHTING_PARAMS',
    # Light role analysis (Phase 2)
    'LightRoleAnalyzer',
    'LightRoleResult',
    'LightRole',
    'DirectionCategory',
    # Composition analysis (Phase 2)
    'CompositionAnalyzer',
    'CompositionAnalysisResult',
    'LightingStyle',
    'CompositionQuality',
    # Light recommendation (Phase 2)
    'NeededLightRecommender',
    'LightRecommendation',
    'RecommendationPriority',
]