"""
NeededLightRecommender - Recommends next light to add based on composition.

Provides intelligent recommendations for:
- Which light role is most needed
- Optimal position for the new light
- Suggested energy/power level
- Suggested light size
- Suggested color temperature

Usage:
    from utils.scene_context import (
        LightRoleAnalyzer, CompositionAnalyzer, NeededLightRecommender
    )
    
    # Analyze current setup
    roles = role_analyzer.analyze(camera_data, product_center)
    composition = composition_analyzer.analyze(roles)
    
    # Get recommendation
    recommender = NeededLightRecommender()
    recommendation = recommender.recommend(composition, product_category)
    
    if recommendation:
        print(f"Add {recommendation.role} light at {recommendation.suggested_position}")
"""

import bpy
from typing import Optional, List
from dataclasses import dataclass, field
from mathutils import Vector

from .light_role_analyzer import LightRole
from .composition_analyzer import CompositionAnalysisResult, LightingStyle
from .product_category_detector import ProductCategoryResult, ProductCategory, CATEGORY_LIGHTING_PARAMS


class RecommendationPriority(str):
    """Priority level for light recommendation."""
    CRITICAL = "critical"    # Essential for basic lighting
    HIGH = "high"            # Strongly recommended
    MEDIUM = "medium"        # Would improve setup
    LOW = "low"              # Nice to have
    NONE = "none"            # No recommendation needed


@dataclass
class LightRecommendation:
    """Recommendation for next light to add."""
    
    # Recommended role
    role: LightRole
    priority: str  # RecommendationPriority value
    
    # Position guidance
    suggested_position: str      # Description like "45° front-left, above product"
    position_angle: float        # Degrees from camera axis
    position_height: str         # "above", "level", "below"
    
    # Suggested parameters
    suggested_energy: float      # Watts
    suggested_size: float        # Area light size in meters
    suggested_color_temp: int    # Kelvin
    
    # Relative to existing lights
    energy_relative_to_key: float  # Multiplier (0.3 = 30% of key)
    
    # Reasoning
    reason: str
    benefits: List[str] = field(default_factory=list)
    
    # Confidence
    confidence: float = 0.8


# Default light parameters by role
ROLE_DEFAULT_PARAMS = {
    LightRole.KEY: {
        'position_angle': 45,
        'position_height': 'above',
        'position_desc': '45° front-side, above product',
        'energy_base': 1000,
        'size': 1.0,
        'color_temp': 5500,
        'energy_ratio': 1.0,
    },
    LightRole.FILL: {
        'position_angle': -45,  # Opposite side of key
        'position_height': 'level',
        'position_desc': 'Opposite side of key light, at product level',
        'energy_base': 400,
        'size': 1.2,
        'color_temp': 5500,
        'energy_ratio': 0.33,  # 1/3 of key
    },
    LightRole.BACK: {
        'position_angle': 150,
        'position_height': 'above',
        'position_desc': 'Behind product, elevated',
        'energy_base': 600,
        'size': 0.8,
        'color_temp': 6000,
        'energy_ratio': 0.5,
    },
    LightRole.RIM: {
        'position_angle': 135,
        'position_height': 'above',
        'position_desc': 'Side-back, high position for edge highlight',
        'energy_base': 500,
        'size': 0.6,
        'color_temp': 6000,
        'energy_ratio': 0.4,
    },
    LightRole.ACCENT: {
        'position_angle': 90,
        'position_height': 'level',
        'position_desc': 'Side position for detail highlight',
        'energy_base': 200,
        'size': 0.4,
        'color_temp': 5500,
        'energy_ratio': 0.2,
    },
}


class NeededLightRecommender:
    """
    Recommends next light to add based on composition analysis.
    
    Takes into account:
    - Missing roles in current setup
    - Product category lighting requirements
    - Desired style
    - Key:fill ratio targets
    """
    
    def __init__(self):
        self.role_params = ROLE_DEFAULT_PARAMS.copy()
    
    def recommend(self,
                  composition: CompositionAnalysisResult,
                  category_result: Optional[ProductCategoryResult] = None,
                  target_style: Optional[LightingStyle] = None) -> Optional[LightRecommendation]:
        """
        Get recommendation for next light to add.
        
        Args:
            composition: Current lighting composition analysis
            category_result: Product category (for category-specific params)
            target_style: Desired lighting style (optional)
            
        Returns:
            LightRecommendation or None if setup is complete
        """
        # Priority 1: KEY light (if missing)
        if not composition.has_key_light:
            return self._recommend_key_light(category_result)
        
        # Priority 2: FILL light (if missing or ratio too high)
        if not composition.has_fill_light:
            return self._recommend_fill_light(composition, category_result)
        
        # Check if ratio is too high (need more fill)
        if composition.key_fill_ratio > 5.0:
            return self._recommend_additional_fill(composition, category_result)
        
        # Priority 3: BACK or RIM light (for separation)
        if not composition.has_back_light and not composition.has_rim_light:
            return self._recommend_separation_light(composition, category_result)
        
        # Priority 4: Style-specific enhancements
        if target_style:
            style_rec = self._recommend_for_style(composition, target_style, category_result)
            if style_rec:
                return style_rec
        
        # No critical recommendations - setup is reasonably complete
        return self._recommend_optional_enhancement(composition, category_result)
    
    def _recommend_key_light(self, 
                             category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend adding a key light."""
        params = self.role_params[LightRole.KEY].copy()
        
        # Apply category-specific adjustments
        if category:
            cat_params = CATEGORY_LIGHTING_PARAMS.get(
                category.category, 
                CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
            )
            params['color_temp'] = cat_params['color_temp']
            params['energy_base'] *= cat_params['intensity_multiplier']
            params['size'] *= cat_params['size_multiplier']
        
        return LightRecommendation(
            role=LightRole.KEY,
            priority=RecommendationPriority.CRITICAL,
            suggested_position=params['position_desc'],
            position_angle=params['position_angle'],
            position_height=params['position_height'],
            suggested_energy=params['energy_base'],
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=1.0,
            reason="No key light detected - this is essential for any lighting setup",
            benefits=[
                "Establishes main illumination direction",
                "Creates form and dimension",
                "Sets the overall mood and exposure"
            ],
            confidence=0.95
        )
    
    def _recommend_fill_light(self,
                              composition: CompositionAnalysisResult,
                              category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend adding a fill light."""
        params = self.role_params[LightRole.FILL].copy()
        
        # Adjust based on category
        if category:
            cat_params = CATEGORY_LIGHTING_PARAMS.get(
                category.category,
                CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
            )
            params['color_temp'] = cat_params['color_temp']
            # Adjust energy ratio based on target key:fill ratio
            target_ratio = cat_params['key_fill_ratio']
            params['energy_ratio'] = 1.0 / target_ratio
            params['energy_base'] = composition.key_contribution * 1000 * params['energy_ratio']
        
        return LightRecommendation(
            role=LightRole.FILL,
            priority=RecommendationPriority.HIGH,
            suggested_position=params['position_desc'],
            position_angle=params['position_angle'],
            position_height=params['position_height'],
            suggested_energy=max(100, params['energy_base']),
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=params['energy_ratio'],
            reason="No fill light - shadows may be too harsh",
            benefits=[
                "Reduces shadow contrast",
                "Shows detail in shadow areas",
                "Creates more flattering appearance"
            ],
            confidence=0.90
        )
    
    def _recommend_additional_fill(self,
                                   composition: CompositionAnalysisResult,
                                   category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend additional fill when ratio is too high."""
        params = self.role_params[LightRole.FILL].copy()
        
        # Calculate how much additional fill is needed
        current_ratio = composition.key_fill_ratio
        target_ratio = 3.5  # Default target
        
        if category:
            cat_params = CATEGORY_LIGHTING_PARAMS.get(
                category.category,
                CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
            )
            target_ratio = cat_params['key_fill_ratio']
        
        # How much more fill do we need?
        needed_fill_mult = (current_ratio / target_ratio) - 1.0
        
        return LightRecommendation(
            role=LightRole.FILL,
            priority=RecommendationPriority.MEDIUM,
            suggested_position="Opposite side of existing fill, or closer to key axis",
            position_angle=-30,
            position_height='level',
            suggested_energy=composition.fill_contribution * 1000 * needed_fill_mult,
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=0.2,
            reason=f"Key:fill ratio is {current_ratio:.1f}:1 - target is {target_ratio:.1f}:1",
            benefits=[
                "Reduces shadow contrast",
                "Creates more balanced lighting",
                f"Brings ratio closer to {target_ratio:.1f}:1"
            ],
            confidence=0.75
        )
    
    def _recommend_separation_light(self,
                                    composition: CompositionAnalysisResult,
                                    category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend back or rim light for separation."""
        # Choose rim for smaller products, back for larger
        if category and category.category in [ProductCategory.JEWELRY, ProductCategory.COSMETICS]:
            return self._recommend_rim_light(composition, category)
        else:
            return self._recommend_back_light(composition, category)
    
    def _recommend_back_light(self,
                              composition: CompositionAnalysisResult,
                              category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend back light."""
        params = self.role_params[LightRole.BACK].copy()
        
        if category:
            cat_params = CATEGORY_LIGHTING_PARAMS.get(
                category.category,
                CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
            )
            params['energy_ratio'] = cat_params.get('back_light_intensity', 0.5)
            params['energy_base'] = composition.key_contribution * 1000 * params['energy_ratio']
        
        return LightRecommendation(
            role=LightRole.BACK,
            priority=RecommendationPriority.HIGH,
            suggested_position=params['position_desc'],
            position_angle=params['position_angle'],
            position_height=params['position_height'],
            suggested_energy=max(200, params['energy_base']),
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=params['energy_ratio'],
            reason="No back/rim light - subject may blend with background",
            benefits=[
                "Separates subject from background",
                "Adds depth to the image",
                "Creates professional 3-point lighting setup"
            ],
            confidence=0.85
        )
    
    def _recommend_rim_light(self,
                             composition: CompositionAnalysisResult,
                             category: Optional[ProductCategoryResult]) -> LightRecommendation:
        """Recommend rim light."""
        params = self.role_params[LightRole.RIM].copy()
        
        if category:
            cat_params = CATEGORY_LIGHTING_PARAMS.get(
                category.category,
                CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
            )
            params['energy_ratio'] = cat_params.get('back_light_intensity', 0.4)
            params['energy_base'] = composition.key_contribution * 1000 * params['energy_ratio']
        
        return LightRecommendation(
            role=LightRole.RIM,
            priority=RecommendationPriority.HIGH,
            suggested_position=params['position_desc'],
            position_angle=params['position_angle'],
            position_height=params['position_height'],
            suggested_energy=max(150, params['energy_base']),
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=params['energy_ratio'],
            reason="No rim light - edges may lack definition",
            benefits=[
                "Highlights product edges",
                "Creates sparkle on reflective surfaces",
                "Adds dimensionality and premium feel"
            ],
            confidence=0.85
        )
    
    def _recommend_for_style(self,
                             composition: CompositionAnalysisResult,
                             target_style: LightingStyle,
                             category: Optional[ProductCategoryResult]) -> Optional[LightRecommendation]:
        """Recommend light to achieve specific style."""
        
        if target_style == LightingStyle.DRAMATIC:
            # For dramatic, might need to reduce fill or add rim
            if composition.key_fill_ratio < 4.0 and composition.has_fill_light:
                return None  # Would need to modify existing, not add new
            if not composition.has_rim_light:
                rec = self._recommend_rim_light(composition, category)
                rec.reason = "Adding rim light for dramatic style"
                return rec
        
        elif target_style == LightingStyle.STUDIO:
            # Studio needs back/rim light
            if not composition.has_back_light and not composition.has_rim_light:
                return self._recommend_back_light(composition, category)
        
        return None
    
    def _recommend_optional_enhancement(self,
                                        composition: CompositionAnalysisResult,
                                        category: Optional[ProductCategoryResult]) -> Optional[LightRecommendation]:
        """Recommend optional enhancement for already-complete setup."""
        
        # If quality is excellent, no recommendation needed
        if composition.quality_score >= 0.85:
            return None
        
        # Suggest accent light for detail
        params = self.role_params[LightRole.ACCENT].copy()
        
        return LightRecommendation(
            role=LightRole.ACCENT,
            priority=RecommendationPriority.LOW,
            suggested_position=params['position_desc'],
            position_angle=params['position_angle'],
            position_height=params['position_height'],
            suggested_energy=params['energy_base'],
            suggested_size=params['size'],
            suggested_color_temp=params['color_temp'],
            energy_relative_to_key=params['energy_ratio'],
            reason="Setup is complete - accent light would add detail emphasis",
            benefits=[
                "Highlights specific details",
                "Adds visual interest",
                "Creates catchlights on reflective surfaces"
            ],
            confidence=0.60
        )


__all__ = [
    'NeededLightRecommender',
    'LightRecommendation',
    'RecommendationPriority',
    'ROLE_DEFAULT_PARAMS',
]
