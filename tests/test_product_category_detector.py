"""
Unit tests for ProductCategoryDetector.

Tests cover:
- Name-based detection
- Material-based detection
- Geometry-based detection
- Combined detection
- Lookup table verification

Run with: python -m pytest tests/test_product_category_detector.py -v
"""

import unittest
from unittest.mock import MagicMock, patch
from mathutils import Vector

# Import module under test
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.scene_context.product_category_detector import (
    ProductCategoryDetector,
    ProductCategoryResult,
    ProductCategory,
    ProductSubcategory,
    CATEGORY_LIGHTING_PARAMS,
    NAME_PATTERNS,
)
from utils.scene_context.material_analyzer import MaterialData
from utils.scene_context.bounds_calculator import BoundsData


class TestProductCategoryDetector(unittest.TestCase):
    """Test cases for ProductCategoryDetector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = ProductCategoryDetector()
    
    # =========================================================================
    # Test Name Pattern Detection
    # =========================================================================
    
    def test_detect_jewelry_from_name(self):
        """Test detection of jewelry category from object name."""
        # Create mock object with jewelry name
        mock_obj = MagicMock()
        mock_obj.name = "Gold_Ring_001"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.JEWELRY)
        self.assertEqual(result.detection_method, "name")
        self.assertGreater(result.confidence, 0.5)
    
    def test_detect_food_from_name(self):
        """Test detection of food category from object name."""
        mock_obj = MagicMock()
        mock_obj.name = "Coffee_Cup_Ceramic"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.FOOD)
    
    def test_detect_electronics_from_name(self):
        """Test detection of electronics from object name."""
        mock_obj = MagicMock()
        mock_obj.name = "Smartphone_Model"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.ELECTRONICS)
    
    def test_detect_automotive_from_name(self):
        """Test detection of automotive from object name."""
        mock_obj = MagicMock()
        mock_obj.name = "Car_Body_Sports"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.AUTOMOTIVE)
    
    def test_no_match_returns_none(self):
        """Test that unknown names return None."""
        mock_obj = MagicMock()
        mock_obj.name = "Cube.001"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNone(result)
    
    def test_multiple_matches_increase_confidence(self):
        """Test that multiple pattern matches increase confidence."""
        mock_obj1 = MagicMock()
        mock_obj1.name = "Diamond_Ring"
        mock_obj2 = MagicMock()
        mock_obj2.name = "Gold_Necklace"
        
        result = self.detector._detect_from_names([mock_obj1, mock_obj2])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.JEWELRY)
        self.assertGreater(result.confidence, 0.7)
    
    def test_subcategory_detection(self):
        """Test subcategory detection from name patterns."""
        mock_obj = MagicMock()
        mock_obj.name = "Wedding_Ring_Gold"
        
        result = self.detector._detect_from_names([mock_obj])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.subcategory, ProductSubcategory.RING)
    
    # =========================================================================
    # Test Material-Based Detection
    # =========================================================================
    
    def test_detect_jewelry_from_material(self):
        """Test jewelry detection from high metallic, low roughness."""
        material_data = MaterialData(
            dominant_type='metallic',
            has_emission=False,
            average_roughness=0.1,
            average_metallic=0.9,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.8, 0.7, 0.3),  # Gold-ish
        )
        
        result = self.detector._detect_from_materials(material_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.JEWELRY)
        self.assertEqual(result.detection_method, "material")
    
    def test_detect_automotive_from_material(self):
        """Test automotive detection from metallic with medium roughness."""
        material_data = MaterialData(
            dominant_type='metallic',
            has_emission=False,
            average_roughness=0.35,
            average_metallic=0.7,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.5, 0.5, 0.5),
        )
        
        result = self.detector._detect_from_materials(material_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.AUTOMOTIVE)
    
    def test_detect_cosmetics_from_glass(self):
        """Test cosmetics detection from glass material."""
        material_data = MaterialData(
            dominant_type='glass',
            has_emission=False,
            average_roughness=0.05,
            average_metallic=0.0,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.9, 0.9, 0.9),
            has_transmission=True,
            average_transmission=0.8,
        )
        
        result = self.detector._detect_from_materials(material_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.COSMETICS)
    
    def test_detect_food_from_sss(self):
        """Test food detection from SSS material."""
        material_data = MaterialData(
            dominant_type='organic',
            has_emission=False,
            average_roughness=0.5,
            average_metallic=0.0,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.8, 0.4, 0.2),  # Orange-ish (food)
            has_sss=True,
            average_sss=0.5,
        )
        
        result = self.detector._detect_from_materials(material_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.FOOD)
    
    # =========================================================================
    # Test Geometry-Based Detection
    # =========================================================================
    
    def test_detect_jewelry_from_small_complex_geometry(self):
        """Test jewelry detection from small, complex geometry."""
        mock_obj = MagicMock()
        mock_obj.type = 'MESH'
        mock_obj.data = MagicMock()
        mock_obj.data.vertices = [MagicMock()] * 50000  # High vertex count
        mock_obj.data.polygons = [MagicMock()] * 25000
        mock_obj.dimensions = Vector((0.02, 0.02, 0.01))  # Small
        
        bounds = BoundsData(
            min=Vector((0, 0, 0)),
            max=Vector((0.05, 0.05, 0.02)),
            center=Vector((0.025, 0.025, 0.01)),
            dimensions=Vector((0.05, 0.05, 0.02)),
            radius=0.03,
            diagonal=0.07,
        )
        
        result = self.detector._detect_from_geometry([mock_obj], bounds)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.JEWELRY)
    
    def test_detect_furniture_from_large_geometry(self):
        """Test furniture detection from large geometry."""
        mock_obj = MagicMock()
        mock_obj.type = 'MESH'
        mock_obj.data = MagicMock()
        mock_obj.data.vertices = [MagicMock()] * 1000
        mock_obj.data.polygons = [MagicMock()] * 500
        mock_obj.dimensions = Vector((1.0, 0.8, 1.2))
        
        bounds = BoundsData(
            min=Vector((0, 0, 0)),
            max=Vector((1.0, 0.8, 1.2)),
            center=Vector((0.5, 0.4, 0.6)),
            dimensions=Vector((1.0, 0.8, 1.2)),
            radius=0.9,
            diagonal=1.8,
        )
        
        result = self.detector._detect_from_geometry([mock_obj], bounds)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category, ProductCategory.FURNITURE)
    
    # =========================================================================
    # Test Combined Detection
    # =========================================================================
    
    def test_combined_detection_boosts_confidence(self):
        """Test that multiple methods agreeing boosts confidence."""
        # Create mock object with jewelry name
        mock_obj = MagicMock()
        mock_obj.name = "Diamond_Ring"
        mock_obj.type = 'MESH'
        mock_obj.data = MagicMock()
        mock_obj.data.vertices = [MagicMock()] * 50000
        mock_obj.data.polygons = [MagicMock()] * 25000
        mock_obj.dimensions = Vector((0.02, 0.02, 0.01))
        
        # Material data suggesting jewelry (high metallic, low roughness)
        material_data = MaterialData(
            dominant_type='metallic',
            has_emission=False,
            average_roughness=0.1,
            average_metallic=0.9,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.8, 0.7, 0.3),
        )
        
        # Small bounds
        bounds = BoundsData(
            min=Vector((0, 0, 0)),
            max=Vector((0.05, 0.05, 0.02)),
            center=Vector((0.025, 0.025, 0.01)),
            dimensions=Vector((0.05, 0.05, 0.02)),
            radius=0.03,
            diagonal=0.07,
        )
        
        result = self.detector.detect([mock_obj], material_data, bounds)
        
        self.assertEqual(result.category, ProductCategory.JEWELRY)
        self.assertGreater(result.confidence, 0.8)
        self.assertEqual(result.detection_method, "combined")
    
    def test_default_result_for_no_signals(self):
        """Test that no signals returns generic category."""
        mock_obj = MagicMock()
        mock_obj.name = "Cube.001"  # No pattern match
        mock_obj.type = 'MESH'
        mock_obj.data = MagicMock()
        mock_obj.data.vertices = [MagicMock()] * 8
        mock_obj.data.polygons = [MagicMock()] * 6
        mock_obj.dimensions = Vector((1, 1, 1))
        
        # Generic material
        material_data = MaterialData(
            dominant_type='dielectric',
            has_emission=False,
            average_roughness=0.5,
            average_metallic=0.0,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.5, 0.5, 0.5),
        )
        
        # Medium bounds
        bounds = BoundsData(
            min=Vector((-0.5, -0.5, -0.5)),
            max=Vector((0.5, 0.5, 0.5)),
            center=Vector((0, 0, 0)),
            dimensions=Vector((1, 1, 1)),
            radius=0.87,
            diagonal=1.73,
        )
        
        result = self.detector.detect([mock_obj], material_data, bounds)
        
        # Should return some result, possibly generic or plastic
        self.assertIsNotNone(result)
        self.assertIn(result.category, [ProductCategory.GENERIC, ProductCategory.PLASTIC])
    
    # =========================================================================
    # Test Lookup Tables
    # =========================================================================
    
    def test_all_categories_have_lighting_params(self):
        """Test that all categories have lighting parameters defined."""
        for category in ProductCategory:
            self.assertIn(category, CATEGORY_LIGHTING_PARAMS)
            params = CATEGORY_LIGHTING_PARAMS[category]
            self.assertIn('color_temp', params)
            self.assertIn('key_fill_ratio', params)
            self.assertIn('style', params)
            self.assertIn('intensity_multiplier', params)
            self.assertIn('size_multiplier', params)
    
    def test_all_categories_have_name_patterns(self):
        """Test that primary categories have name patterns."""
        primary_categories = [
            ProductCategory.JEWELRY,
            ProductCategory.FOOD,
            ProductCategory.COSMETICS,
            ProductCategory.ELECTRONICS,
            ProductCategory.AUTOMOTIVE,
            ProductCategory.APPAREL,
            ProductCategory.FURNITURE,
        ]
        for category in primary_categories:
            self.assertIn(category, NAME_PATTERNS)
            self.assertGreater(len(NAME_PATTERNS[category]), 0)
    
    def test_get_lighting_params(self):
        """Test get_lighting_params helper method."""
        params = self.detector.get_lighting_params(ProductCategory.JEWELRY)
        
        self.assertEqual(params['color_temp'], 5800)
        self.assertEqual(params['key_fill_ratio'], 4.0)
        self.assertEqual(params['style'], 'dramatic')
    
    # =========================================================================
    # Test Result Object
    # =========================================================================
    
    def test_result_contains_recommendations(self):
        """Test that result contains all recommendation fields."""
        mock_obj = MagicMock()
        mock_obj.name = "Gold_Ring"
        
        result = self.detector.detect([mock_obj])
        
        self.assertIsNotNone(result.recommended_color_temp)
        self.assertIsNotNone(result.recommended_key_fill_ratio)
        self.assertIsNotNone(result.recommended_style)
        self.assertIsNotNone(result.intensity_multiplier)
        self.assertIsNotNone(result.size_multiplier)
    
    def test_default_result(self):
        """Test ProductCategoryResult.default() method."""
        result = ProductCategoryResult.default()
        
        self.assertEqual(result.category, ProductCategory.GENERIC)
        self.assertEqual(result.subcategory, ProductSubcategory.GENERIC)
        self.assertEqual(result.detection_method, "fallback")
        self.assertLess(result.confidence, 0.5)


class TestNamePatternCoverage(unittest.TestCase):
    """Test coverage of name patterns for each category."""
    
    def test_jewelry_patterns(self):
        """Test jewelry name patterns."""
        patterns = NAME_PATTERNS[ProductCategory.JEWELRY]
        expected = ['ring', 'necklace', 'diamond', 'gold', 'silver', 'watch']
        for exp in expected:
            self.assertIn(exp, patterns)
    
    def test_food_patterns(self):
        """Test food name patterns."""
        patterns = NAME_PATTERNS[ProductCategory.FOOD]
        expected = ['food', 'dish', 'plate', 'coffee', 'wine', 'fruit']
        for exp in expected:
            self.assertIn(exp, patterns)
    
    def test_electronics_patterns(self):
        """Test electronics name patterns."""
        patterns = NAME_PATTERNS[ProductCategory.ELECTRONICS]
        expected = ['phone', 'laptop', 'camera', 'computer', 'tablet']
        for exp in expected:
            self.assertIn(exp, patterns)


if __name__ == '__main__':
    unittest.main()
