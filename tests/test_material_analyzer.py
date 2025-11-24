"""
Unit tests for Enhanced MaterialAnalyzer.

Tests cover:
- MaterialType classification
- MaterialSubtype classification
- Color-based detection helpers
- MaterialData fields

Run with: python -m pytest tests/test_material_analyzer.py -v
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.scene_context.material_analyzer import (
    MaterialAnalyzer,
    MaterialData,
    MaterialType,
    MaterialSubtype,
)


class TestMaterialAnalyzer(unittest.TestCase):
    """Test cases for MaterialAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = MaterialAnalyzer()
    
    # =========================================================================
    # Test Enhanced Classification
    # =========================================================================
    
    def test_classify_polished_metal(self):
        """Test classification of polished metal (high metallic, low roughness)."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.9,
            roughness=0.05,
            transmission=0.0,
            sss=0.0,
            color=(0.8, 0.8, 0.8),
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.METALLIC.value)
        self.assertEqual(subtype, MaterialSubtype.POLISHED_METAL.value)
    
    def test_classify_brushed_metal(self):
        """Test classification of brushed metal."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.8,
            roughness=0.3,
            transmission=0.0,
            sss=0.0,
            color=(0.6, 0.6, 0.6),
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.METALLIC.value)
        self.assertEqual(subtype, MaterialSubtype.BRUSHED_METAL.value)
    
    def test_classify_rough_metal(self):
        """Test classification of rough metal."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.7,
            roughness=0.6,
            transmission=0.0,
            sss=0.0,
            color=(0.5, 0.4, 0.3),
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.METALLIC.value)
        self.assertEqual(subtype, MaterialSubtype.ROUGH_METAL.value)
    
    def test_classify_clear_glass(self):
        """Test classification of clear glass."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.02,
            transmission=0.9,
            sss=0.0,
            color=(0.95, 0.95, 0.95),  # Near white (not colored)
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.GLASS.value)
        self.assertEqual(subtype, MaterialSubtype.CLEAR_GLASS.value)
    
    def test_classify_colored_glass(self):
        """Test classification of colored glass."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.02,
            transmission=0.8,
            sss=0.0,
            color=(0.2, 0.8, 0.3),  # Green tint
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.GLASS.value)
        self.assertEqual(subtype, MaterialSubtype.COLORED_GLASS.value)
    
    def test_classify_frosted_glass(self):
        """Test classification of frosted glass."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.4,
            transmission=0.6,
            sss=0.0,
            color=(0.9, 0.9, 0.9),
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.GLASS.value)
        self.assertEqual(subtype, MaterialSubtype.FROSTED_GLASS.value)
    
    def test_classify_food_organic(self):
        """Test classification of food (SSS material)."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.5,
            transmission=0.0,
            sss=0.3,
            color=(0.8, 0.4, 0.2),  # Orange-ish (food)
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.ORGANIC.value)
        self.assertEqual(subtype, MaterialSubtype.FOOD.value)
    
    def test_classify_plant_organic(self):
        """Test classification of plant (green SSS material)."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.5,
            transmission=0.0,
            sss=0.25,
            color=(0.2, 0.6, 0.15),  # Green
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.ORGANIC.value)
        self.assertEqual(subtype, MaterialSubtype.PLANT.value)
    
    def test_classify_skin_organic(self):
        """Test classification of skin (warm SSS material)."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.5,
            transmission=0.0,
            sss=0.4,
            color=(0.8, 0.6, 0.5),  # Skin tone (r > g > b)
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.ORGANIC.value)
        self.assertEqual(subtype, MaterialSubtype.SKIN.value)
    
    def test_classify_porcelain_ceramic(self):
        """Test classification of porcelain."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.05,
            transmission=0.0,
            sss=0.0,
            color=(0.95, 0.95, 0.95),  # White
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.CERAMIC.value)
        self.assertEqual(subtype, MaterialSubtype.PORCELAIN.value)
    
    def test_classify_cotton_fabric(self):
        """Test classification of cotton fabric."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.75,
            transmission=0.0,
            sss=0.0,
            color=(0.8, 0.8, 0.9),  # Light fabric
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.FABRIC.value)
        self.assertEqual(subtype, MaterialSubtype.COTTON.value)
    
    def test_classify_leather_fabric(self):
        """Test classification of leather."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.15,  # Slightly metallic
            roughness=0.7,
            transmission=0.0,
            sss=0.0,
            color=(0.4, 0.25, 0.15),  # Brown
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.FABRIC.value)
        self.assertEqual(subtype, MaterialSubtype.LEATHER.value)
    
    def test_classify_natural_wood(self):
        """Test classification of natural wood."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.5,
            transmission=0.0,
            sss=0.0,
            color=(0.5, 0.35, 0.2),  # Brown/tan wood color
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.WOOD.value)
        self.assertEqual(subtype, MaterialSubtype.NATURAL_WOOD.value)
    
    def test_classify_glossy_plastic(self):
        """Test classification of glossy plastic."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.25,
            transmission=0.0,
            sss=0.0,
            color=(0.9, 0.1, 0.1),  # Bright red plastic
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.PLASTIC.value)
        self.assertEqual(subtype, MaterialSubtype.GLOSSY_PLASTIC.value)
    
    def test_classify_rubber(self):
        """Test classification of rubber."""
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.55,
            transmission=0.0,
            sss=0.0,
            color=(0.05, 0.05, 0.05),  # Dark black rubber
            emission_materials=[]
        )
        
        self.assertEqual(mat_type, MaterialType.PLASTIC.value)
        self.assertEqual(subtype, MaterialSubtype.RUBBER.value)
    
    def test_classify_emissive(self):
        """Test classification of emissive material."""
        mock_emission = MagicMock()
        mat_type, subtype = self.analyzer._classify_material_enhanced(
            metallic=0.0,
            roughness=0.5,
            transmission=0.0,
            sss=0.0,
            color=(1.0, 0.8, 0.3),
            emission_materials=[mock_emission]
        )
        
        self.assertEqual(mat_type, MaterialType.EMISSIVE.value)
        self.assertEqual(subtype, MaterialSubtype.GENERIC.value)
    
    # =========================================================================
    # Test Color Helper Methods
    # =========================================================================
    
    def test_is_colored_true(self):
        """Test _is_colored returns True for colored."""
        self.assertTrue(self.analyzer._is_colored((0.9, 0.2, 0.2)))  # Red
        self.assertTrue(self.analyzer._is_colored((0.2, 0.8, 0.3)))  # Green
        self.assertTrue(self.analyzer._is_colored((0.2, 0.3, 0.9)))  # Blue
    
    def test_is_colored_false(self):
        """Test _is_colored returns False for grayscale."""
        self.assertFalse(self.analyzer._is_colored((0.5, 0.5, 0.5)))  # Gray
        self.assertFalse(self.analyzer._is_colored((0.9, 0.9, 0.9)))  # Near white
        self.assertFalse(self.analyzer._is_colored((0.1, 0.1, 0.1)))  # Near black
    
    def test_is_green_color(self):
        """Test _is_green_color detection."""
        self.assertTrue(self.analyzer._is_green_color((0.2, 0.7, 0.15)))
        self.assertFalse(self.analyzer._is_green_color((0.7, 0.2, 0.15)))  # Red
        self.assertFalse(self.analyzer._is_green_color((0.2, 0.15, 0.7)))  # Blue
    
    def test_is_skin_tone(self):
        """Test _is_skin_tone detection."""
        self.assertTrue(self.analyzer._is_skin_tone((0.85, 0.65, 0.5)))  # Light skin
        self.assertTrue(self.analyzer._is_skin_tone((0.6, 0.45, 0.35)))  # Medium skin
        self.assertFalse(self.analyzer._is_skin_tone((0.2, 0.7, 0.15)))  # Green
    
    def test_is_wood_color(self):
        """Test _is_wood_color detection."""
        self.assertTrue(self.analyzer._is_wood_color((0.5, 0.35, 0.2)))  # Brown
        self.assertTrue(self.analyzer._is_wood_color((0.6, 0.45, 0.25)))  # Tan
        self.assertFalse(self.analyzer._is_wood_color((0.2, 0.7, 0.15)))  # Green
        self.assertFalse(self.analyzer._is_wood_color((0.95, 0.95, 0.95)))  # White
    
    def test_is_dark_color(self):
        """Test _is_dark_color detection."""
        self.assertTrue(self.analyzer._is_dark_color((0.05, 0.05, 0.05)))  # Black
        self.assertTrue(self.analyzer._is_dark_color((0.1, 0.08, 0.05)))  # Dark brown
        self.assertFalse(self.analyzer._is_dark_color((0.5, 0.5, 0.5)))  # Gray
        self.assertFalse(self.analyzer._is_dark_color((0.9, 0.9, 0.9)))  # White
    
    def test_calculate_saturation(self):
        """Test _calculate_saturation calculation."""
        # Full saturation (pure red)
        sat = self.analyzer._calculate_saturation((1.0, 0.0, 0.0))
        self.assertAlmostEqual(sat, 1.0, places=2)
        
        # No saturation (gray)
        sat = self.analyzer._calculate_saturation((0.5, 0.5, 0.5))
        self.assertAlmostEqual(sat, 0.0, places=2)
        
        # Medium saturation
        sat = self.analyzer._calculate_saturation((0.8, 0.4, 0.4))
        self.assertGreater(sat, 0.3)
        self.assertLess(sat, 0.7)
    
    # =========================================================================
    # Test MaterialData Fields
    # =========================================================================
    
    def test_material_data_has_all_fields(self):
        """Test MaterialData has all expected fields."""
        data = MaterialData(
            dominant_type='metallic',
            has_emission=False,
            average_roughness=0.1,
            average_metallic=0.9,
            material_count=1,
            emission_strength=0.0,
            dominant_color=(0.8, 0.8, 0.8),
        )
        
        # Check required fields
        self.assertEqual(data.dominant_type, 'metallic')
        self.assertFalse(data.has_emission)
        self.assertEqual(data.average_roughness, 0.1)
        self.assertEqual(data.average_metallic, 0.9)
        
        # Check default optional fields
        self.assertEqual(data.material_subtype, 'generic')
        self.assertFalse(data.has_transmission)
        self.assertEqual(data.average_transmission, 0.0)
        self.assertFalse(data.has_sss)
        self.assertEqual(data.average_sss, 0.0)
        self.assertFalse(data.is_reflective)
        self.assertFalse(data.is_transparent)
        self.assertFalse(data.is_organic)
        self.assertEqual(data.color_saturation, 0.0)
    
    def test_empty_analysis(self):
        """Test _empty_analysis returns valid default MaterialData."""
        data = self.analyzer._empty_analysis()
        
        self.assertEqual(data.dominant_type, 'dielectric')
        self.assertFalse(data.has_emission)
        self.assertEqual(data.average_roughness, 0.5)
        self.assertEqual(data.average_metallic, 0.0)
        self.assertEqual(data.material_count, 0)
        self.assertEqual(data.material_subtype, 'generic')
    
    # =========================================================================
    # Test MaterialType and MaterialSubtype Enums
    # =========================================================================
    
    def test_material_type_values(self):
        """Test MaterialType enum has all expected values."""
        expected = ['metallic', 'glass', 'ceramic', 'fabric', 'wood', 
                    'plastic', 'organic', 'dielectric', 'emissive']
        for exp in expected:
            self.assertTrue(any(mt.value == exp for mt in MaterialType))
    
    def test_material_subtype_values(self):
        """Test MaterialSubtype enum has representative values."""
        # Metallic subtypes
        self.assertEqual(MaterialSubtype.POLISHED_METAL.value, 'polished_metal')
        self.assertEqual(MaterialSubtype.BRUSHED_METAL.value, 'brushed_metal')
        
        # Glass subtypes
        self.assertEqual(MaterialSubtype.CLEAR_GLASS.value, 'clear_glass')
        self.assertEqual(MaterialSubtype.FROSTED_GLASS.value, 'frosted_glass')
        
        # Organic subtypes
        self.assertEqual(MaterialSubtype.FOOD.value, 'food')
        self.assertEqual(MaterialSubtype.PLANT.value, 'plant')
        self.assertEqual(MaterialSubtype.SKIN.value, 'skin')


if __name__ == '__main__':
    unittest.main()
