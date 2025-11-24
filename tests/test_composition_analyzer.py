"""
Unit tests for CompositionAnalyzer and NeededLightRecommender.

Tests cover:
- Composition analysis
- Style detection
- Quality assessment
- Light recommendations

Run with: python -m pytest tests/test_composition_analyzer.py -v
"""

import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mathutils import Vector

from utils.scene_context.light_role_analyzer import (
    LightRoleResult,
    LightRole,
    DirectionCategory,
)
from utils.scene_context.composition_analyzer import (
    CompositionAnalyzer,
    CompositionAnalysisResult,
    LightingStyle,
    CompositionQuality,
)
from utils.scene_context.needed_light_recommender import (
    NeededLightRecommender,
    LightRecommendation,
    RecommendationPriority,
)
from utils.scene_context.product_category_detector import (
    ProductCategoryResult,
    ProductCategory,
    ProductSubcategory,
)


def create_mock_role_result(name, role, contribution, direction, angle=45, height=0.5):
    """Helper to create mock LightRoleResult."""
    mock_light = MagicMock()
    mock_light.name = name
    
    return LightRoleResult(
        light=mock_light,
        role=role,
        contribution=contribution,
        confidence=0.8,
        direction_category=direction,
        angle_from_camera=angle,
        height_relative=height,
        distance_to_product=2.0,
        detection_reasons=[]
    )


class TestCompositionAnalyzer(unittest.TestCase):
    """Test cases for CompositionAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CompositionAnalyzer()
    
    # =========================================================================
    # Test Basic Composition Analysis
    # =========================================================================
    
    def test_analyze_empty_returns_incomplete(self):
        """Test that empty input returns incomplete composition."""
        result = self.analyzer.analyze([])
        
        self.assertEqual(result.quality, CompositionQuality.INCOMPLETE)
        self.assertFalse(result.has_key_light)
        self.assertEqual(result.total_count, 0)
    
    def test_analyze_single_key_light(self):
        """Test composition with single key light."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 1.0, DirectionCategory.FRONT
            )
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertTrue(result.has_key_light)
        self.assertFalse(result.has_fill_light)
        self.assertEqual(result.key_count, 1)
        self.assertEqual(result.key_fill_ratio, 0.0)  # No fill
        self.assertIn("fill", result.missing_roles)
    
    def test_analyze_key_fill_setup(self):
        """Test composition with key and fill lights."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.7, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.3, DirectionCategory.SIDE, angle=90
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertTrue(result.has_key_light)
        self.assertTrue(result.has_fill_light)
        self.assertGreater(result.key_fill_ratio, 0)
        self.assertNotIn("key", result.missing_roles)
        self.assertNotIn("fill", result.missing_roles)
    
    def test_analyze_three_point_setup(self):
        """Test composition with full 3-point lighting."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.55, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.25, DirectionCategory.SIDE
            ),
            create_mock_role_result(
                "Back", LightRole.BACK, 0.20, DirectionCategory.BACK
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertTrue(result.has_key_light)
        self.assertTrue(result.has_fill_light)
        self.assertTrue(result.has_back_light)
        self.assertEqual(result.total_count, 3)
        self.assertEqual(len(result.missing_roles), 0)
    
    # =========================================================================
    # Test Key:Fill Ratio Calculation
    # =========================================================================
    
    def test_ratio_calculation(self):
        """Test key:fill ratio calculation."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.75, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.25, DirectionCategory.SIDE
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        # 0.75 / 0.25 = 3.0
        self.assertAlmostEqual(result.key_fill_ratio, 3.0, places=1)
    
    def test_ratio_no_fill_returns_zero(self):
        """Test ratio returns 0 when no fill light."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 1.0, DirectionCategory.FRONT
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        self.assertEqual(result.key_fill_ratio, 0.0)
    
    # =========================================================================
    # Test Style Detection
    # =========================================================================
    
    def test_detect_flat_style(self):
        """Test detection of flat lighting style (low ratio)."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.55, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.45, DirectionCategory.SIDE
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        # Ratio ~1.2:1 should be FLAT
        self.assertEqual(result.style, LightingStyle.FLAT)
    
    def test_detect_natural_style(self):
        """Test detection of natural lighting style."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.70, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.30, DirectionCategory.SIDE
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        # Ratio ~2.3:1 should be NATURAL
        self.assertIn(result.style, [LightingStyle.NATURAL, LightingStyle.FLAT])
    
    def test_detect_dramatic_style(self):
        """Test detection of dramatic lighting style (high ratio)."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.85, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.15, DirectionCategory.SIDE
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        # Ratio ~5.7:1 should be DRAMATIC
        self.assertIn(result.style, [LightingStyle.DRAMATIC, LightingStyle.STUDIO])
    
    def test_detect_studio_style_with_back(self):
        """Test detection of studio style (moderate ratio + back light)."""
        roles = [
            create_mock_role_result(
                "Key", LightRole.KEY, 0.55, DirectionCategory.FRONT
            ),
            create_mock_role_result(
                "Fill", LightRole.FILL, 0.20, DirectionCategory.SIDE
            ),
            create_mock_role_result(
                "Back", LightRole.BACK, 0.25, DirectionCategory.BACK
            ),
        ]
        
        result = self.analyzer.analyze(roles)
        
        # With back light and ~2.75:1 ratio
        self.assertIn(result.style, [LightingStyle.STUDIO, LightingStyle.NATURAL])
    
    # =========================================================================
    # Test Quality Assessment
    # =========================================================================
    
    def test_quality_excellent(self):
        """Test excellent quality for complete setup."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 0.50, DirectionCategory.FRONT),
            create_mock_role_result("Fill", LightRole.FILL, 0.20, DirectionCategory.SIDE),
            create_mock_role_result("Back", LightRole.BACK, 0.30, DirectionCategory.BACK),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertIn(result.quality, [CompositionQuality.EXCELLENT, CompositionQuality.GOOD])
        self.assertGreater(result.quality_score, 0.7)
    
    def test_quality_incomplete_no_key(self):
        """Test incomplete quality when missing key light."""
        roles = [
            create_mock_role_result("Fill", LightRole.FILL, 0.5, DirectionCategory.SIDE),
            create_mock_role_result("Accent", LightRole.ACCENT, 0.5, DirectionCategory.SIDE),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertIn(result.quality, [
            CompositionQuality.NEEDS_WORK,
            CompositionQuality.INCOMPLETE,
            CompositionQuality.ACCEPTABLE
        ])
    
    # =========================================================================
    # Test Suggestions
    # =========================================================================
    
    def test_suggests_key_when_missing(self):
        """Test suggestion to add key light."""
        roles = [
            create_mock_role_result("Fill", LightRole.FILL, 1.0, DirectionCategory.SIDE),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertIn("key", result.missing_roles)
        self.assertTrue(any("key" in s.lower() for s in result.suggestions))
    
    def test_suggests_fill_when_missing(self):
        """Test suggestion to add fill light."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 1.0, DirectionCategory.FRONT),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertIn("fill", result.missing_roles)
    
    def test_suggests_back_when_missing(self):
        """Test suggestion to add back/rim light."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 0.7, DirectionCategory.FRONT),
            create_mock_role_result("Fill", LightRole.FILL, 0.3, DirectionCategory.SIDE),
        ]
        
        result = self.analyzer.analyze(roles)
        
        self.assertIn("back_or_rim", result.missing_roles)


class TestNeededLightRecommender(unittest.TestCase):
    """Test cases for NeededLightRecommender."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recommender = NeededLightRecommender()
        self.comp_analyzer = CompositionAnalyzer()
    
    def _create_category_result(self, category=ProductCategory.GENERIC):
        """Create mock category result."""
        return ProductCategoryResult(
            category=category,
            subcategory=ProductSubcategory.GENERIC,
            confidence=0.8,
            detection_method="test",
            recommended_color_temp=5500,
            recommended_key_fill_ratio=3.0,
            recommended_style="studio",
            intensity_multiplier=1.0,
            size_multiplier=1.0,
            detection_reasons=[]
        )
    
    # =========================================================================
    # Test Recommendations
    # =========================================================================
    
    def test_recommend_key_when_missing(self):
        """Test recommending key light when none exists."""
        # Empty composition
        roles = []
        composition = self.comp_analyzer.analyze(roles)
        
        recommendation = self.recommender.recommend(composition)
        
        self.assertIsNotNone(recommendation)
        self.assertEqual(recommendation.role, LightRole.KEY)
        self.assertEqual(recommendation.priority, RecommendationPriority.CRITICAL)
    
    def test_recommend_fill_when_missing(self):
        """Test recommending fill light after key exists."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 1.0, DirectionCategory.FRONT),
        ]
        composition = self.comp_analyzer.analyze(roles)
        
        recommendation = self.recommender.recommend(composition)
        
        self.assertIsNotNone(recommendation)
        self.assertEqual(recommendation.role, LightRole.FILL)
        self.assertEqual(recommendation.priority, RecommendationPriority.HIGH)
    
    def test_recommend_back_after_key_fill(self):
        """Test recommending back/rim light after key and fill exist."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 0.7, DirectionCategory.FRONT),
            create_mock_role_result("Fill", LightRole.FILL, 0.3, DirectionCategory.SIDE),
        ]
        composition = self.comp_analyzer.analyze(roles)
        
        recommendation = self.recommender.recommend(composition)
        
        self.assertIsNotNone(recommendation)
        self.assertIn(recommendation.role, [LightRole.BACK, LightRole.RIM])
        self.assertEqual(recommendation.priority, RecommendationPriority.HIGH)
    
    def test_recommend_additional_fill_high_ratio(self):
        """Test recommending additional fill when ratio too high."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 0.90, DirectionCategory.FRONT),
            create_mock_role_result("Fill", LightRole.FILL, 0.10, DirectionCategory.SIDE),
        ]
        composition = self.comp_analyzer.analyze(roles)
        
        # Ratio is 9:1 which is too high
        recommendation = self.recommender.recommend(composition)
        
        self.assertIsNotNone(recommendation)
        self.assertEqual(recommendation.role, LightRole.FILL)
    
    def test_no_recommendation_complete_setup(self):
        """Test no critical recommendation for complete setup."""
        roles = [
            create_mock_role_result("Key", LightRole.KEY, 0.50, DirectionCategory.FRONT),
            create_mock_role_result("Fill", LightRole.FILL, 0.25, DirectionCategory.SIDE),
            create_mock_role_result("Back", LightRole.BACK, 0.25, DirectionCategory.BACK),
        ]
        composition = self.comp_analyzer.analyze(roles)
        
        recommendation = self.recommender.recommend(composition)
        
        # Either None or low priority
        if recommendation:
            self.assertIn(recommendation.priority, [
                RecommendationPriority.LOW,
                RecommendationPriority.MEDIUM
            ])
    
    # =========================================================================
    # Test Category-Specific Parameters
    # =========================================================================
    
    def test_jewelry_category_params(self):
        """Test jewelry-specific lighting parameters."""
        roles = []
        composition = self.comp_analyzer.analyze(roles)
        category = self._create_category_result(ProductCategory.JEWELRY)
        
        recommendation = self.recommender.recommend(composition, category)
        
        self.assertIsNotNone(recommendation)
        # Jewelry typically uses cooler temps and dramatic ratios
        self.assertGreater(recommendation.suggested_color_temp, 5500)
    
    def test_food_category_params(self):
        """Test food-specific lighting parameters."""
        roles = []
        composition = self.comp_analyzer.analyze(roles)
        category = self._create_category_result(ProductCategory.FOOD)
        
        recommendation = self.recommender.recommend(composition, category)
        
        self.assertIsNotNone(recommendation)
        # Food uses warmer temps
        self.assertLess(recommendation.suggested_color_temp, 5000)
    
    # =========================================================================
    # Test Recommendation Fields
    # =========================================================================
    
    def test_recommendation_has_all_fields(self):
        """Test recommendation contains all required fields."""
        roles = []
        composition = self.comp_analyzer.analyze(roles)
        
        rec = self.recommender.recommend(composition)
        
        self.assertIsNotNone(rec.role)
        self.assertIsNotNone(rec.priority)
        self.assertIsNotNone(rec.suggested_position)
        self.assertIsNotNone(rec.suggested_energy)
        self.assertIsNotNone(rec.suggested_size)
        self.assertIsNotNone(rec.suggested_color_temp)
        self.assertIsNotNone(rec.reason)
        self.assertIsInstance(rec.benefits, list)


class TestLightingStyle(unittest.TestCase):
    """Test LightingStyle enum."""
    
    def test_all_styles_exist(self):
        """Test all expected styles exist."""
        expected = ['flat', 'natural', 'studio', 'dramatic', 'high_key', 'low_key']
        for exp in expected:
            self.assertTrue(any(ls.value == exp for ls in LightingStyle))


class TestCompositionQuality(unittest.TestCase):
    """Test CompositionQuality enum."""
    
    def test_all_qualities_exist(self):
        """Test all expected quality levels exist."""
        expected = ['excellent', 'good', 'acceptable', 'needs_work', 'incomplete']
        for exp in expected:
            self.assertTrue(any(cq.value == exp for cq in CompositionQuality))


if __name__ == '__main__':
    unittest.main()
