"""
CompositionAnalyzer - Analyzes overall lighting composition.

Provides:
- Key:Fill ratio analysis
- Light balance assessment
- Style detection (dramatic, flat, natural, studio)
- Missing role identification
- Composition quality scoring

Usage:
    from utils.scene_context import CompositionAnalyzer, LightRoleAnalyzer
    
    role_analyzer = LightRoleAnalyzer(context)
    light_roles = role_analyzer.analyze(camera_data, product_center)
    
    composition_analyzer = CompositionAnalyzer()
    composition = composition_analyzer.analyze(light_roles)
    
    print(f"Style: {composition.style}")
    print(f"Key:Fill Ratio: {composition.key_fill_ratio}")
    print(f"Missing: {composition.missing_roles}")
"""

import bpy
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .light_role_analyzer import LightRoleResult, LightRole, DirectionCategory


class LightingStyle(str, Enum):
    """Detected lighting style."""
    FLAT = "flat"           # Low contrast, even lighting (ratio < 2:1)
    NATURAL = "natural"     # Moderate contrast (ratio 2:1 - 3:1)
    STUDIO = "studio"       # Professional look with back/rim (ratio 3:1 - 4:1)
    DRAMATIC = "dramatic"   # High contrast (ratio > 4:1)
    HIGH_KEY = "high_key"   # Bright, low contrast
    LOW_KEY = "low_key"     # Dark, high contrast
    UNKNOWN = "unknown"


class CompositionQuality(str, Enum):
    """Overall composition quality assessment."""
    EXCELLENT = "excellent"   # All essential roles present, good ratios
    GOOD = "good"             # Most roles present, acceptable ratios
    ACCEPTABLE = "acceptable" # Minimum requirements met
    NEEDS_WORK = "needs_work" # Missing key elements
    INCOMPLETE = "incomplete" # Critical elements missing


@dataclass
class CompositionAnalysisResult:
    """Result of lighting composition analysis."""
    
    # Light presence
    has_key_light: bool
    has_fill_light: bool
    has_back_light: bool
    has_rim_light: bool
    has_accent_light: bool
    
    # Light counts
    key_count: int
    fill_count: int
    back_count: int
    rim_count: int
    accent_count: int
    total_count: int
    
    # Ratios
    key_fill_ratio: float       # Key intensity / Fill intensity (0 if no fill)
    key_back_ratio: float       # Key intensity / Back intensity (0 if no back)
    
    # Balance
    left_right_balance: float   # -1.0 (left heavy) to 1.0 (right heavy)
    front_back_balance: float   # -1.0 (front heavy) to 1.0 (back heavy)
    
    # Style detection
    style: LightingStyle
    style_confidence: float
    
    # Quality assessment
    quality: CompositionQuality
    quality_score: float        # 0.0 - 1.0
    
    # Recommendations
    missing_roles: List[str]    # Roles that should be added
    suggestions: List[str]      # Improvement suggestions
    
    # Details
    key_contribution: float     # Total key light contribution
    fill_contribution: float    # Total fill light contribution
    back_contribution: float    # Total back/rim contribution


# Style detection thresholds
STYLE_THRESHOLDS = {
    'flat_max_ratio': 2.0,
    'natural_max_ratio': 3.0,
    'studio_max_ratio': 4.0,
    'dramatic_min_ratio': 4.0,
    'high_key_min_fill': 0.5,   # Fill contribution > 50% of key
    'low_key_max_fill': 0.2,    # Fill contribution < 20% of key
}


class CompositionAnalyzer:
    """
    Analyzes overall lighting composition from role analysis results.
    
    Provides insights into:
    - Lighting ratios (key:fill, key:back)
    - Light balance (left/right, front/back)
    - Style classification (dramatic, flat, natural, studio)
    - Quality assessment
    - Recommendations for improvement
    """
    
    def __init__(self):
        self.thresholds = STYLE_THRESHOLDS.copy()
    
    def analyze(self, light_roles: List[LightRoleResult]) -> CompositionAnalysisResult:
        """
        Analyze lighting composition from role analysis.
        
        Args:
            light_roles: List of LightRoleResult from LightRoleAnalyzer
            
        Returns:
            CompositionAnalysisResult with detailed analysis
        """
        if not light_roles:
            return self._empty_result()
        
        # Group lights by role
        key_lights = [r for r in light_roles if r.role == LightRole.KEY]
        fill_lights = [r for r in light_roles if r.role == LightRole.FILL]
        back_lights = [r for r in light_roles if r.role == LightRole.BACK]
        rim_lights = [r for r in light_roles if r.role == LightRole.RIM]
        accent_lights = [r for r in light_roles if r.role == LightRole.ACCENT]
        
        # Calculate contributions
        key_contrib = sum(r.contribution for r in key_lights)
        fill_contrib = sum(r.contribution for r in fill_lights)
        back_contrib = sum(r.contribution for r in back_lights)
        rim_contrib = sum(r.contribution for r in rim_lights)
        
        # Calculate ratios
        key_fill_ratio = self._calculate_ratio(key_contrib, fill_contrib)
        key_back_ratio = self._calculate_ratio(key_contrib, back_contrib + rim_contrib)
        
        # Calculate balance
        left_right, front_back = self._calculate_balance(light_roles)
        
        # Detect style
        style, style_confidence = self._detect_style(
            key_contrib, fill_contrib, back_contrib + rim_contrib,
            key_fill_ratio, bool(back_lights or rim_lights)
        )
        
        # Identify missing roles
        missing_roles = self._identify_missing_roles(
            key_lights, fill_lights, back_lights, rim_lights
        )
        
        # Assess quality
        quality, quality_score = self._assess_quality(
            key_lights, fill_lights, back_lights, rim_lights,
            key_fill_ratio, missing_roles
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            key_fill_ratio, left_right, front_back, style,
            missing_roles, quality
        )
        
        return CompositionAnalysisResult(
            has_key_light=bool(key_lights),
            has_fill_light=bool(fill_lights),
            has_back_light=bool(back_lights),
            has_rim_light=bool(rim_lights),
            has_accent_light=bool(accent_lights),
            key_count=len(key_lights),
            fill_count=len(fill_lights),
            back_count=len(back_lights),
            rim_count=len(rim_lights),
            accent_count=len(accent_lights),
            total_count=len(light_roles),
            key_fill_ratio=key_fill_ratio,
            key_back_ratio=key_back_ratio,
            left_right_balance=left_right,
            front_back_balance=front_back,
            style=style,
            style_confidence=style_confidence,
            quality=quality,
            quality_score=quality_score,
            missing_roles=missing_roles,
            suggestions=suggestions,
            key_contribution=key_contrib,
            fill_contribution=fill_contrib,
            back_contribution=back_contrib + rim_contrib,
        )
    
    def _calculate_ratio(self, primary: float, secondary: float) -> float:
        """Calculate ratio between two values."""
        if secondary <= 0.001:
            return 0.0  # Cannot calculate ratio without secondary
        return primary / secondary
    
    def _calculate_balance(self, light_roles: List[LightRoleResult]) -> Tuple[float, float]:
        """
        Calculate left/right and front/back balance.
        
        Returns:
            Tuple of (left_right_balance, front_back_balance)
            Range: -1.0 to 1.0 (negative = left/front heavy, positive = right/back heavy)
        """
        if not light_roles:
            return 0.0, 0.0
        
        left_contrib = 0.0
        right_contrib = 0.0
        front_contrib = 0.0
        back_contrib = 0.0
        
        for result in light_roles:
            contrib = result.contribution
            direction = result.direction_category
            
            # Front/Back classification
            if direction in [DirectionCategory.FRONT, DirectionCategory.FRONT_SIDE]:
                front_contrib += contrib
            elif direction in [DirectionCategory.BACK, DirectionCategory.BACK_SIDE]:
                back_contrib += contrib
            
            # Left/Right would need actual position data - simplified for now
            # Using angle as proxy (negative angles = left, positive = right)
            # This is a simplification
            angle = result.angle_from_camera
            if 45 < angle < 135:  # Side positions
                # Use height as proxy for left/right (simplified)
                if result.height_relative > 0:
                    right_contrib += contrib * 0.5
                else:
                    left_contrib += contrib * 0.5
        
        total = sum(r.contribution for r in light_roles)
        if total <= 0.001:
            return 0.0, 0.0
        
        # Calculate normalized balance (-1 to 1)
        lr_balance = (right_contrib - left_contrib) / total
        fb_balance = (back_contrib - front_contrib) / total
        
        return max(-1.0, min(1.0, lr_balance)), max(-1.0, min(1.0, fb_balance))
    
    def _detect_style(self,
                      key_contrib: float,
                      fill_contrib: float,
                      back_contrib: float,
                      ratio: float,
                      has_back: bool) -> Tuple[LightingStyle, float]:
        """Detect lighting style from contributions and ratio."""
        th = self.thresholds
        
        # Check for high-key or low-key first
        if key_contrib > 0 and fill_contrib > 0:
            fill_ratio = fill_contrib / key_contrib
            
            if fill_ratio >= th['high_key_min_fill']:
                return LightingStyle.HIGH_KEY, 0.75
            elif fill_ratio <= th['low_key_max_fill']:
                return LightingStyle.LOW_KEY, 0.70
        
        # Check based on key:fill ratio
        if ratio <= 0:
            # No valid ratio (no fill light)
            if key_contrib > 0:
                return LightingStyle.DRAMATIC, 0.60
            return LightingStyle.UNKNOWN, 0.30
        
        if ratio < th['flat_max_ratio']:
            return LightingStyle.FLAT, 0.80
        elif ratio < th['natural_max_ratio']:
            return LightingStyle.NATURAL, 0.75
        elif ratio < th['studio_max_ratio']:
            if has_back:
                return LightingStyle.STUDIO, 0.85
            else:
                return LightingStyle.NATURAL, 0.70
        else:  # ratio >= dramatic threshold
            return LightingStyle.DRAMATIC, 0.80
    
    def _identify_missing_roles(self,
                                key_lights: List,
                                fill_lights: List,
                                back_lights: List,
                                rim_lights: List) -> List[str]:
        """Identify which roles are missing for a complete setup."""
        missing = []
        
        if not key_lights:
            missing.append("key")
        if not fill_lights:
            missing.append("fill")
        if not back_lights and not rim_lights:
            missing.append("back_or_rim")
        
        return missing
    
    def _assess_quality(self,
                        key_lights: List,
                        fill_lights: List,
                        back_lights: List,
                        rim_lights: List,
                        ratio: float,
                        missing: List[str]) -> Tuple[CompositionQuality, float]:
        """Assess overall composition quality."""
        score = 0.0
        
        # Key light presence (40%)
        if key_lights:
            score += 0.40
        
        # Fill light presence (25%)
        if fill_lights:
            score += 0.25
        
        # Back/Rim light presence (20%)
        if back_lights or rim_lights:
            score += 0.20
        
        # Ratio quality (15%)
        if 2.0 <= ratio <= 5.0:  # Good ratio range
            score += 0.15
        elif 1.5 <= ratio <= 6.0:  # Acceptable range
            score += 0.10
        elif ratio > 0:
            score += 0.05
        
        # Determine quality level
        if score >= 0.85:
            quality = CompositionQuality.EXCELLENT
        elif score >= 0.70:
            quality = CompositionQuality.GOOD
        elif score >= 0.50:
            quality = CompositionQuality.ACCEPTABLE
        elif score >= 0.30:
            quality = CompositionQuality.NEEDS_WORK
        else:
            quality = CompositionQuality.INCOMPLETE
        
        return quality, score
    
    def _generate_suggestions(self,
                              ratio: float,
                              lr_balance: float,
                              fb_balance: float,
                              style: LightingStyle,
                              missing: List[str],
                              quality: CompositionQuality) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Missing role suggestions
        if "key" in missing:
            suggestions.append("Add a key light as the main illumination source")
        if "fill" in missing:
            suggestions.append("Add a fill light to reduce shadow contrast")
        if "back_or_rim" in missing:
            suggestions.append("Add a back or rim light for subject separation")
        
        # Ratio suggestions
        if ratio > 6.0:
            suggestions.append("Consider adding or increasing fill light - contrast may be too high")
        elif 0 < ratio < 1.5:
            suggestions.append("Consider reducing fill light - scene may appear flat")
        
        # Balance suggestions
        if abs(lr_balance) > 0.5:
            side = "left" if lr_balance < 0 else "right"
            suggestions.append(f"Lighting appears {side}-heavy - consider rebalancing")
        
        if fb_balance > 0.4:
            suggestions.append("Strong back lighting - ensure subject is not silhouetted")
        elif fb_balance < -0.6:
            suggestions.append("Front-heavy lighting - consider adding separation light")
        
        return suggestions
    
    def _empty_result(self) -> CompositionAnalysisResult:
        """Return empty result for no lights."""
        return CompositionAnalysisResult(
            has_key_light=False,
            has_fill_light=False,
            has_back_light=False,
            has_rim_light=False,
            has_accent_light=False,
            key_count=0,
            fill_count=0,
            back_count=0,
            rim_count=0,
            accent_count=0,
            total_count=0,
            key_fill_ratio=0.0,
            key_back_ratio=0.0,
            left_right_balance=0.0,
            front_back_balance=0.0,
            style=LightingStyle.UNKNOWN,
            style_confidence=0.0,
            quality=CompositionQuality.INCOMPLETE,
            quality_score=0.0,
            missing_roles=["key", "fill", "back_or_rim"],
            suggestions=["Add lights to create a basic lighting setup"],
            key_contribution=0.0,
            fill_contribution=0.0,
            back_contribution=0.0,
        )


__all__ = [
    'CompositionAnalyzer',
    'CompositionAnalysisResult',
    'LightingStyle',
    'CompositionQuality',
    'STYLE_THRESHOLDS',
]
