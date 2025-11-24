"""
LightRoleAnalyzer - Advanced light role detection for intelligent operators.

Detects 6 light roles:
- KEY: Main illumination source (highest contribution, front position)
- FILL: Shadow fill (medium contribution, side position)
- BACK: Subject separation from background (behind subject)
- RIM: Edge highlighting (side-back, high position)
- ACCENT: Detail/spot lighting (low contribution)
- UNKNOWN: Cannot determine role

Detection based on:
1. Position relative to camera and product
2. Illumination contribution percentage
3. Light type and properties
4. Direction category

Usage:
    from utils.scene_context import LightRoleAnalyzer
    
    analyzer = LightRoleAnalyzer(context)
    results = analyzer.analyze(camera_data, product_center)
    
    for result in results:
        print(f"{result.light.name}: {result.role} ({result.confidence:.0%})")
"""

import bpy
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from mathutils import Vector

from .camera_analyzer import CameraData
from .bounds_calculator import BoundsData


class LightRole(str, Enum):
    """Light role in lighting setup."""
    KEY = "key"          # Main light, primary illumination
    FILL = "fill"        # Shadow fill, secondary
    BACK = "back"        # Separation from background
    RIM = "rim"          # Edge highlighting
    ACCENT = "accent"    # Detail/spot lighting
    BACKGROUND = "background"  # Background illumination only
    UNKNOWN = "unknown"  # Cannot determine


class DirectionCategory(str, Enum):
    """Light direction relative to camera."""
    FRONT = "front"              # 0-45° from camera axis
    FRONT_SIDE = "front_side"    # 45-90° from camera axis
    SIDE = "side"                # ~90° from camera axis
    BACK_SIDE = "back_side"      # 90-135° from camera axis
    BACK = "back"                # 135-180° from camera axis
    TOP = "top"                  # Above product (high angle)
    BOTTOM = "bottom"            # Below product


@dataclass
class LightRoleResult:
    """Result of light role analysis for a single light."""
    light: bpy.types.Object
    role: LightRole
    contribution: float         # 0.0 - 1.0 (percentage of total illumination)
    confidence: float           # 0.0 - 1.0
    direction_category: DirectionCategory
    
    # Position analysis
    angle_from_camera: float    # Degrees (0 = same direction as camera)
    height_relative: float      # Meters above/below product center
    distance_to_product: float  # Meters
    
    # Detection details
    detection_reasons: List[str] = field(default_factory=list)
    
    def __repr__(self):
        return f"LightRoleResult({self.light.name}: {self.role.value}, {self.confidence:.0%})"


# Role detection thresholds
ROLE_THRESHOLDS = {
    'key_min_contribution': 0.35,      # Minimum contribution to be KEY
    'fill_max_contribution': 0.50,     # Maximum contribution to be FILL
    'fill_min_contribution': 0.10,     # Minimum contribution to be FILL
    'accent_max_contribution': 0.15,   # Maximum contribution to be ACCENT
    'front_angle_max': 60,             # Max angle from camera to be FRONT
    'side_angle_min': 60,              # Min angle to be SIDE
    'side_angle_max': 120,             # Max angle to be SIDE
    'back_angle_min': 120,             # Min angle to be BACK
    'top_height_threshold': 0.8,       # Height above product to be TOP
    'bottom_height_threshold': -0.3,   # Height below product to be BOTTOM
}


class LightRoleAnalyzer:
    """
    Analyzes light roles in scene with confidence scoring.
    
    Provides detailed analysis of each light's role based on:
    - Position relative to camera and product
    - Contribution to total illumination
    - Light properties (type, energy, size)
    
    Usage:
        analyzer = LightRoleAnalyzer(context)
        results = analyzer.analyze(camera_data, product_center)
        
        key_light = next((r for r in results if r.role == LightRole.KEY), None)
        if key_light:
            print(f"Key light: {key_light.light.name}")
    """
    
    def __init__(self, context: bpy.types.Context):
        self.context = context
        self.thresholds = ROLE_THRESHOLDS.copy()
    
    def analyze(self,
                camera_data: CameraData,
                product_center: Vector,
                lights: Optional[List[bpy.types.Object]] = None,
                product_radius: float = 1.0) -> List[LightRoleResult]:
        """
        Analyze role of each light in scene.
        
        Args:
            camera_data: Camera analysis data
            product_center: Center point of product/subject
            lights: Optional list of lights (if None, uses all scene lights)
            product_radius: Approximate radius of product for distance scaling
            
        Returns:
            List of LightRoleResult for each light
        """
        if lights is None:
            lights = [obj for obj in self.context.scene.objects 
                     if obj.type == 'LIGHT' and obj.data]
        
        if not lights:
            return []
        
        results = []
        
        # Calculate total illumination for contribution percentage
        total_illumination = self._calculate_total_illumination(lights, product_center)
        
        for light in lights:
            result = self._analyze_single_light(
                light, camera_data, product_center, 
                total_illumination, product_radius
            )
            results.append(result)
        
        # Post-process: Validate and adjust roles for logical consistency
        results = self._validate_roles(results)
        
        return results
    
    def _analyze_single_light(self,
                              light: bpy.types.Object,
                              camera_data: CameraData,
                              product_center: Vector,
                              total_illumination: float,
                              product_radius: float) -> LightRoleResult:
        """Analyze role of a single light."""
        
        light_pos = light.matrix_world.translation.copy()
        
        # Calculate position metrics
        # Vector from camera to product (view direction)
        camera_to_product = (product_center - camera_data.location).normalized()
        
        # Vector from product to light
        product_to_light = light_pos - product_center
        distance_to_product = product_to_light.length
        
        if distance_to_product > 0.001:
            product_to_light_dir = product_to_light.normalized()
        else:
            product_to_light_dir = Vector((0, 0, 1))
        
        # Angle from camera axis (0° = same direction as camera looking at product)
        # We want angle between camera_to_product and product_to_light
        angle_from_camera = self._angle_between_vectors(
            camera_to_product, product_to_light_dir
        )
        
        # Height relative to product center
        height_relative = light_pos.z - product_center.z
        
        # Calculate illumination contribution
        illumination = self._calculate_light_illumination(light, product_center)
        contribution = illumination / max(0.001, total_illumination)
        
        # Determine direction category
        direction = self._get_direction_category(
            angle_from_camera, height_relative, product_radius
        )
        
        # Determine role based on all factors
        role, confidence, reasons = self._determine_role(
            angle_from_camera, height_relative, contribution, 
            direction, light, distance_to_product, product_radius
        )
        
        return LightRoleResult(
            light=light,
            role=role,
            contribution=contribution,
            confidence=confidence,
            direction_category=direction,
            angle_from_camera=angle_from_camera,
            height_relative=height_relative,
            distance_to_product=distance_to_product,
            detection_reasons=reasons
        )
    
    def _determine_role(self,
                        angle: float,
                        height: float,
                        contribution: float,
                        direction: DirectionCategory,
                        light: bpy.types.Object,
                        distance: float,
                        product_radius: float) -> Tuple[LightRole, float, List[str]]:
        """
        Determine light role from metrics.
        
        Role determination priority:
        1. High contribution + front = KEY
        2. Medium contribution + side = FILL
        3. Back direction = BACK or RIM
        4. Low contribution = ACCENT
        5. Unknown
        """
        reasons = []
        th = self.thresholds
        
        # High contribution + front/front-side direction = KEY
        if (contribution >= th['key_min_contribution'] and 
            direction in [DirectionCategory.FRONT, DirectionCategory.FRONT_SIDE]):
            role = LightRole.KEY
            # Higher confidence with higher contribution
            confidence = min(0.95, 0.70 + contribution * 0.3)
            reasons.append(f"High contribution ({contribution:.0%}) from {direction.value}")
            return role, confidence, reasons
        
        # Medium contribution + side/front-side = FILL
        if (th['fill_min_contribution'] <= contribution <= th['fill_max_contribution'] and
            direction in [DirectionCategory.FRONT_SIDE, DirectionCategory.SIDE]):
            role = LightRole.FILL
            confidence = 0.75
            reasons.append(f"Medium contribution ({contribution:.0%}) from {direction.value}")
            return role, confidence, reasons
        
        # Back direction with height = RIM
        if direction in [DirectionCategory.BACK, DirectionCategory.BACK_SIDE]:
            if height > product_radius * 0.3:  # Above product
                role = LightRole.RIM
                confidence = 0.80
                reasons.append(f"Back position ({direction.value}), elevated ({height:.2f}m above)")
            else:
                role = LightRole.BACK
                confidence = 0.75
                reasons.append(f"Back position ({direction.value})")
            return role, confidence, reasons
        
        # Top position with any contribution = potential RIM or ACCENT
        if direction == DirectionCategory.TOP:
            if contribution >= th['fill_min_contribution']:
                role = LightRole.RIM
                confidence = 0.65
                reasons.append(f"Top position with moderate contribution ({contribution:.0%})")
            else:
                role = LightRole.ACCENT
                confidence = 0.60
                reasons.append(f"Top position, low contribution ({contribution:.0%})")
            return role, confidence, reasons
        
        # Low contribution from any direction = ACCENT
        if contribution < th['accent_max_contribution']:
            role = LightRole.ACCENT
            confidence = 0.65
            reasons.append(f"Low contribution ({contribution:.0%})")
            return role, confidence, reasons
        
        # Side position with medium-high contribution = could be KEY or FILL
        if direction == DirectionCategory.SIDE:
            if contribution >= th['key_min_contribution']:
                role = LightRole.KEY
                confidence = 0.60  # Lower confidence for side key
                reasons.append(f"Side position with high contribution ({contribution:.0%})")
            else:
                role = LightRole.FILL
                confidence = 0.65
                reasons.append(f"Side position with medium contribution ({contribution:.0%})")
            return role, confidence, reasons
        
        # Front position with lower contribution = likely FILL
        if direction == DirectionCategory.FRONT and contribution < th['key_min_contribution']:
            role = LightRole.FILL
            confidence = 0.60
            reasons.append(f"Front position but lower contribution ({contribution:.0%})")
            return role, confidence, reasons
        
        # Default: Unknown
        role = LightRole.UNKNOWN
        confidence = 0.30
        reasons.append(f"Could not determine clear role (angle={angle:.0f}°, contribution={contribution:.0%})")
        return role, confidence, reasons
    
    def _get_direction_category(self,
                                angle: float,
                                height: float,
                                product_radius: float) -> DirectionCategory:
        """Get direction category from angle and height."""
        th = self.thresholds
        
        # Check height-based categories first
        if height > th['top_height_threshold'] * product_radius:
            return DirectionCategory.TOP
        if height < th['bottom_height_threshold'] * product_radius:
            return DirectionCategory.BOTTOM
        
        # Angle-based categories (horizontal plane)
        if angle < th['front_angle_max']:
            return DirectionCategory.FRONT
        elif angle < th['side_angle_min']:
            return DirectionCategory.FRONT_SIDE
        elif angle < th['side_angle_max']:
            return DirectionCategory.SIDE
        elif angle < th['back_angle_min']:
            return DirectionCategory.BACK_SIDE
        else:
            return DirectionCategory.BACK
    
    def _calculate_light_illumination(self,
                                      light: bpy.types.Object,
                                      target: Vector) -> float:
        """
        Calculate illumination contribution from light to target.
        Uses inverse square law for point sources.
        """
        distance = (light.matrix_world.translation - target).length
        energy = getattr(light.data, 'energy', 0.0)
        
        if distance < 0.01:
            distance = 0.01  # Avoid division by zero
        
        # Apply inverse square law for point sources
        if light.data.type in ['POINT', 'SPOT', 'AREA']:
            # Scale by area light size if applicable
            if light.data.type == 'AREA':
                size = getattr(light.data, 'size', 1.0)
                energy *= size  # Larger lights contribute more
            
            illumination = energy / (distance ** 2)
        else:  # SUN - no distance falloff
            illumination = energy
        
        return max(0.0, illumination)
    
    def _calculate_total_illumination(self,
                                      lights: List[bpy.types.Object],
                                      target: Vector) -> float:
        """Calculate total illumination from all lights."""
        total = sum(self._calculate_light_illumination(l, target) for l in lights)
        return max(0.001, total)  # Avoid division by zero
    
    def _angle_between_vectors(self, v1: Vector, v2: Vector) -> float:
        """Calculate angle between two vectors in degrees."""
        v1_n = v1.normalized()
        v2_n = v2.normalized()
        dot = v1_n.dot(v2_n)
        # Clamp to avoid acos errors from floating point
        dot = max(-1.0, min(1.0, dot))
        return math.degrees(math.acos(dot))
    
    def _validate_roles(self, results: List[LightRoleResult]) -> List[LightRoleResult]:
        """
        Validate and adjust roles for logical consistency.
        
        Rules:
        - Only one KEY light (highest contribution wins)
        - At most 2 FILL lights
        - RIM/BACK lights should be behind product
        """
        if not results:
            return results
        
        # Ensure only one KEY light
        key_lights = [r for r in results if r.role == LightRole.KEY]
        if len(key_lights) > 1:
            # Keep the one with highest contribution
            key_lights.sort(key=lambda r: r.contribution, reverse=True)
            for r in key_lights[1:]:
                r.role = LightRole.FILL
                r.confidence *= 0.85
                r.detection_reasons.append(
                    "Demoted from KEY (another light has higher contribution)"
                )
        
        # If no KEY light was detected, promote highest contributor
        if not any(r.role == LightRole.KEY for r in results):
            # Find highest contributor that's in front
            front_results = [r for r in results 
                           if r.direction_category in [
                               DirectionCategory.FRONT, 
                               DirectionCategory.FRONT_SIDE,
                               DirectionCategory.SIDE
                           ]]
            if front_results:
                best = max(front_results, key=lambda r: r.contribution)
                best.role = LightRole.KEY
                best.confidence = min(0.7, best.confidence + 0.1)
                best.detection_reasons.append("Promoted to KEY (highest front contributor)")
        
        return results
    
    def get_role_summary(self, results: List[LightRoleResult]) -> Dict[LightRole, List[str]]:
        """Get summary of lights by role."""
        summary = {role: [] for role in LightRole}
        for result in results:
            summary[result.role].append(result.light.name)
        return summary
    
    def get_key_light(self, results: List[LightRoleResult]) -> Optional[LightRoleResult]:
        """Get the KEY light from results."""
        for result in results:
            if result.role == LightRole.KEY:
                return result
        return None
    
    def get_lights_by_role(self, 
                           results: List[LightRoleResult], 
                           role: LightRole) -> List[LightRoleResult]:
        """Get all lights with a specific role."""
        return [r for r in results if r.role == role]


__all__ = [
    'LightRoleAnalyzer',
    'LightRoleResult',
    'LightRole',
    'DirectionCategory',
    'ROLE_THRESHOLDS',
]
