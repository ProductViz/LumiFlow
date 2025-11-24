"""
Unit tests for LightRoleAnalyzer.

Tests cover:
- Light role detection (KEY, FILL, BACK, RIM, ACCENT)
- Direction category classification
- Contribution calculation
- Role validation

Run with: python -m pytest tests/test_light_role_analyzer.py -v
"""

import unittest
from unittest.mock import MagicMock, PropertyMock
import math

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mathutils import Vector

from utils.scene_context.light_role_analyzer import (
    LightRoleAnalyzer,
    LightRoleResult,
    LightRole,
    DirectionCategory,
    ROLE_THRESHOLDS,
)
from utils.scene_context.camera_analyzer import CameraData


class MockLight:
    """Mock light object for testing."""
    def __init__(self, name, location, energy=1000, light_type='AREA', size=1.0):
        self.name = name
        self.type = 'LIGHT'
        self.matrix_world = MagicMock()
        self.matrix_world.translation = location.copy()
        
        self.data = MagicMock()
        self.data.energy = energy
        self.data.type = light_type
        self.data.size = size


class MockCameraData:
    """Mock camera data for testing."""
    def __init__(self, location=None, forward=None):
        self.location = location or Vector((0, -5, 1.5))
        self.forward = forward or Vector((0, 1, 0))


class TestLightRoleAnalyzer(unittest.TestCase):
    """Test cases for LightRoleAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_context = MagicMock()
        self.mock_context.scene.objects = []
        
        self.analyzer = LightRoleAnalyzer(self.mock_context)
        self.camera_data = MockCameraData()
        self.product_center = Vector((0, 0, 0))
    
    # =========================================================================
    # Test Direction Category
    # =========================================================================
    
    def test_direction_front(self):
        """Test front direction detection."""
        # Light in front of product, same direction as camera looking
        direction = self.analyzer._get_direction_category(
            angle=30, height=0.5, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.FRONT)
    
    def test_direction_front_side(self):
        """Test front-side direction detection."""
        direction = self.analyzer._get_direction_category(
            angle=70, height=0.5, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.FRONT_SIDE)
    
    def test_direction_side(self):
        """Test side direction detection."""
        direction = self.analyzer._get_direction_category(
            angle=90, height=0.5, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.SIDE)
    
    def test_direction_back_side(self):
        """Test back-side direction detection."""
        direction = self.analyzer._get_direction_category(
            angle=110, height=0.3, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.BACK_SIDE)
    
    def test_direction_back(self):
        """Test back direction detection."""
        direction = self.analyzer._get_direction_category(
            angle=150, height=0.3, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.BACK)
    
    def test_direction_top(self):
        """Test top direction detection (high above product)."""
        direction = self.analyzer._get_direction_category(
            angle=45, height=2.0, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.TOP)
    
    def test_direction_bottom(self):
        """Test bottom direction detection."""
        direction = self.analyzer._get_direction_category(
            angle=45, height=-0.5, product_radius=1.0
        )
        self.assertEqual(direction, DirectionCategory.BOTTOM)
    
    # =========================================================================
    # Test Role Detection
    # =========================================================================
    
    def test_detect_key_light_high_contribution_front(self):
        """Test KEY light detection: high contribution from front."""
        role, confidence, reasons = self.analyzer._determine_role(
            angle=45,
            height=0.5,
            contribution=0.6,
            direction=DirectionCategory.FRONT,
            light=MagicMock(),
            distance=2.0,
            product_radius=1.0
        )
        
        self.assertEqual(role, LightRole.KEY)
        self.assertGreater(confidence, 0.7)
    
    def test_detect_fill_light_medium_contribution_side(self):
        """Test FILL light detection: medium contribution from side."""
        role, confidence, reasons = self.analyzer._determine_role(
            angle=90,
            height=0.3,
            contribution=0.25,
            direction=DirectionCategory.SIDE,
            light=MagicMock(),
            distance=2.5,
            product_radius=1.0
        )
        
        self.assertEqual(role, LightRole.FILL)
        self.assertGreater(confidence, 0.6)
    
    def test_detect_back_light_back_direction(self):
        """Test BACK light detection: back direction, level height."""
        role, confidence, reasons = self.analyzer._determine_role(
            angle=150,
            height=0.2,
            contribution=0.3,
            direction=DirectionCategory.BACK,
            light=MagicMock(),
            distance=2.0,
            product_radius=1.0
        )
        
        self.assertEqual(role, LightRole.BACK)
    
    def test_detect_rim_light_back_elevated(self):
        """Test RIM light detection: back direction, elevated."""
        role, confidence, reasons = self.analyzer._determine_role(
            angle=140,
            height=1.5,
            contribution=0.25,
            direction=DirectionCategory.BACK_SIDE,
            light=MagicMock(),
            distance=2.0,
            product_radius=1.0
        )
        
        self.assertEqual(role, LightRole.RIM)
    
    def test_detect_accent_light_low_contribution(self):
        """Test ACCENT light detection: low contribution."""
        role, confidence, reasons = self.analyzer._determine_role(
            angle=90,
            height=0.3,
            contribution=0.05,
            direction=DirectionCategory.SIDE,
            light=MagicMock(),
            distance=3.0,
            product_radius=1.0
        )
        
        self.assertEqual(role, LightRole.ACCENT)
    
    # =========================================================================
    # Test Full Analysis
    # =========================================================================
    
    def test_analyze_single_key_light(self):
        """Test analysis with single key light."""
        # Create key light in front
        key_light = MockLight(
            "KeyLight",
            location=Vector((1, -2, 1)),
            energy=1000
        )
        
        results = self.analyzer.analyze(
            camera_data=self.camera_data,
            product_center=self.product_center,
            lights=[key_light],
            product_radius=0.5
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].role, LightRole.KEY)
        self.assertEqual(results[0].contribution, 1.0)  # Only light = 100%
    
    def test_analyze_three_point_lighting(self):
        """Test analysis with classic 3-point lighting setup."""
        # Key light - front-side, high contribution
        key_light = MockLight(
            "KeyLight",
            location=Vector((2, -2, 2)),
            energy=1000
        )
        
        # Fill light - opposite side, lower energy
        fill_light = MockLight(
            "FillLight",
            location=Vector((-1.5, -2, 1)),
            energy=350
        )
        
        # Back light - behind product
        back_light = MockLight(
            "BackLight",
            location=Vector((0, 2, 1.5)),
            energy=500
        )
        
        results = self.analyzer.analyze(
            camera_data=self.camera_data,
            product_center=self.product_center,
            lights=[key_light, fill_light, back_light],
            product_radius=0.5
        )
        
        self.assertEqual(len(results), 3)
        
        # Check roles are properly assigned
        roles = {r.light.name: r.role for r in results}
        self.assertEqual(roles["KeyLight"], LightRole.KEY)
        # Fill and Back should be detected
        self.assertIn(roles["FillLight"], [LightRole.FILL, LightRole.KEY])
        self.assertIn(roles["BackLight"], [LightRole.BACK, LightRole.RIM])
    
    def test_validate_only_one_key(self):
        """Test that validation ensures only one KEY light."""
        # Two lights with similar properties in front
        light1 = MockLight("Light1", Vector((1, -2, 1)), energy=1000)
        light2 = MockLight("Light2", Vector((1.5, -2, 1.2)), energy=900)
        
        results = self.analyzer.analyze(
            camera_data=self.camera_data,
            product_center=self.product_center,
            lights=[light1, light2],
            product_radius=0.5
        )
        
        # Only one should be KEY
        key_count = sum(1 for r in results if r.role == LightRole.KEY)
        self.assertEqual(key_count, 1)
    
    # =========================================================================
    # Test Helper Methods
    # =========================================================================
    
    def test_angle_between_vectors(self):
        """Test angle calculation between vectors."""
        v1 = Vector((1, 0, 0))
        v2 = Vector((0, 1, 0))
        
        angle = self.analyzer._angle_between_vectors(v1, v2)
        self.assertAlmostEqual(angle, 90.0, places=1)
        
        v3 = Vector((1, 1, 0)).normalized()
        angle2 = self.analyzer._angle_between_vectors(v1, v3)
        self.assertAlmostEqual(angle2, 45.0, places=1)
    
    def test_calculate_illumination_inverse_square(self):
        """Test illumination uses inverse square law."""
        light = MockLight("Test", Vector((0, 0, 2)), energy=1000)
        target = Vector((0, 0, 0))
        
        illum1 = self.analyzer._calculate_light_illumination(light, target)
        
        # Double the distance
        light.matrix_world.translation = Vector((0, 0, 4))
        illum2 = self.analyzer._calculate_light_illumination(light, target)
        
        # At double distance, illumination should be ~1/4 (inverse square)
        ratio = illum2 / illum1
        self.assertAlmostEqual(ratio, 0.25, places=2)
    
    def test_get_role_summary(self):
        """Test get_role_summary helper method."""
        results = [
            LightRoleResult(
                light=MockLight("Key", Vector((0,0,0))),
                role=LightRole.KEY,
                contribution=0.6,
                confidence=0.9,
                direction_category=DirectionCategory.FRONT,
                angle_from_camera=30,
                height_relative=0.5,
                distance_to_product=2.0
            ),
            LightRoleResult(
                light=MockLight("Fill", Vector((0,0,0))),
                role=LightRole.FILL,
                contribution=0.3,
                confidence=0.8,
                direction_category=DirectionCategory.SIDE,
                angle_from_camera=90,
                height_relative=0.3,
                distance_to_product=2.5
            ),
        ]
        
        summary = self.analyzer.get_role_summary(results)
        
        self.assertIn("Key", summary[LightRole.KEY])
        self.assertIn("Fill", summary[LightRole.FILL])
    
    def test_get_key_light(self):
        """Test get_key_light helper method."""
        results = [
            LightRoleResult(
                light=MockLight("Key", Vector((0,0,0))),
                role=LightRole.KEY,
                contribution=0.6,
                confidence=0.9,
                direction_category=DirectionCategory.FRONT,
                angle_from_camera=30,
                height_relative=0.5,
                distance_to_product=2.0
            ),
            LightRoleResult(
                light=MockLight("Fill", Vector((0,0,0))),
                role=LightRole.FILL,
                contribution=0.3,
                confidence=0.8,
                direction_category=DirectionCategory.SIDE,
                angle_from_camera=90,
                height_relative=0.3,
                distance_to_product=2.5
            ),
        ]
        
        key = self.analyzer.get_key_light(results)
        
        self.assertIsNotNone(key)
        self.assertEqual(key.light.name, "Key")


class TestDirectionCategory(unittest.TestCase):
    """Test DirectionCategory enum values."""
    
    def test_all_directions_exist(self):
        """Test all expected direction categories exist."""
        expected = ['front', 'front_side', 'side', 'back_side', 'back', 'top', 'bottom']
        for exp in expected:
            self.assertTrue(any(dc.value == exp for dc in DirectionCategory))


class TestLightRole(unittest.TestCase):
    """Test LightRole enum values."""
    
    def test_all_roles_exist(self):
        """Test all expected light roles exist."""
        expected = ['key', 'fill', 'back', 'rim', 'accent', 'background', 'unknown']
        for exp in expected:
            self.assertTrue(any(lr.value == exp for lr in LightRole))


if __name__ == '__main__':
    unittest.main()
