"""
Scene Context System - Unified scene analysis for LumiFlow.

Main exports:
- SceneAnalyzer: Main facade class
- SceneContext: Data container
- analyze_scene(): Quick function

Usage:
    from utils.scene_context import SceneAnalyzer

    analyzer = SceneAnalyzer(context)
    scene_ctx = analyzer.analyze_scene(context.selected_objects)

    # Access data
    center = scene_ctx.bounds.center
    camera_pos = scene_ctx.camera.location if scene_ctx.camera else None
    backgrounds = scene_ctx.get_background_objects()
"""

from .scene_analyzer import SceneAnalyzer, SceneContext, analyze_scene
from .camera_analyzer import CameraAnalyzer, CameraData, FrustumPlane
from .bounds_calculator import BoundsCalculator, BoundsData
from .material_analyzer import MaterialAnalyzer, MaterialData
from .spatial_analyzer import SpatialAnalyzer, SpatialGraph
from .classification_system import ObjectClassifier, ObjectClassification

__all__ = [
    'SceneAnalyzer',
    'SceneContext',
    'analyze_scene',
    'CameraAnalyzer',
    'CameraData',
    'BoundsCalculator',
    'BoundsData',
    'MaterialAnalyzer',
    'MaterialData',
    'SpatialAnalyzer',
    'ObjectClassifier',
    'ObjectClassification',
]