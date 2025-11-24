# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Template Integration Bridge.

Provides compatibility layer between:
- ProductCategoryDetector (scene-analysis)
- Template system (feature/template)

This module ensures smooth integration when merging branches
and provides mapping functions between different naming conventions.

Usage:
    from utils.template_integration import (
        get_template_product_type,
        get_template_recommendations,
        enhance_template_params
    )
    
    # Convert ProductCategory to template string
    template_type = get_template_product_type(category_result.category)
    
    # Get template recommendations
    templates = get_template_recommendations(category_result, material_data)
    
    # Get parameter enhancements
    overrides = enhance_template_params(template_id, category_result, material_data)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene_context.product_category_detector import (
        ProductCategoryResult, ProductCategory, ProductSubcategory
    )
    from .scene_context.material_analyzer import MaterialData, MaterialType, MaterialSubtype
    from .scene_context.composition_analyzer import CompositionAnalysisResult, LightingStyle


# =============================================================================
# Category Mapping
# =============================================================================

def get_template_product_type(category) -> str:
    """
    Convert ProductCategory enum to template product_type string.
    
    Args:
        category: ProductCategory enum or string
        
    Returns:
        Template-compatible product type string
    """
    from .scene_context.product_category_detector import ProductCategory
    
    CATEGORY_TO_TEMPLATE = {
        ProductCategory.JEWELRY: "jewelry",
        ProductCategory.FOOD: "food",
        ProductCategory.COSMETICS: "cosmetics",
        ProductCategory.ELECTRONICS: "electronics",
        ProductCategory.AUTOMOTIVE: "automotive",
        ProductCategory.APPAREL: "apparel",
        ProductCategory.FURNITURE: "furniture",
        ProductCategory.GENERIC: "generic",
    }
    
    if isinstance(category, str):
        return category
    
    return CATEGORY_TO_TEMPLATE.get(category, "generic")


def get_product_category_from_string(product_type: str):
    """
    Convert template product_type string to ProductCategory enum.
    
    Args:
        product_type: Template product type string
        
    Returns:
        ProductCategory enum value
    """
    from .scene_context.product_category_detector import ProductCategory
    
    TEMPLATE_TO_CATEGORY = {
        "jewelry": ProductCategory.JEWELRY,
        "watches": ProductCategory.JEWELRY,  # Map to parent
        "food": ProductCategory.FOOD,
        "cosmetics": ProductCategory.COSMETICS,
        "electronics": ProductCategory.ELECTRONICS,
        "automotive": ProductCategory.AUTOMOTIVE,
        "apparel": ProductCategory.APPAREL,
        "furniture": ProductCategory.FURNITURE,
        "generic": ProductCategory.GENERIC,
    }
    
    return TEMPLATE_TO_CATEGORY.get(product_type.lower(), ProductCategory.GENERIC)


# =============================================================================
# Material Mapping
# =============================================================================

def get_template_material(material_type, material_subtype=None) -> str:
    """
    Convert MaterialType/MaterialSubtype to template material string.
    
    Args:
        material_type: MaterialType enum or string
        material_subtype: Optional MaterialSubtype enum
        
    Returns:
        Template-compatible material string
    """
    from .scene_context.material_analyzer import MaterialType, MaterialSubtype
    
    # Subtype-specific mapping (more specific)
    SUBTYPE_TO_TEMPLATE = {
        MaterialSubtype.POLISHED_METAL: "metallic",
        MaterialSubtype.BRUSHED_METAL: "metallic",
        MaterialSubtype.ROUGH_METAL: "metallic",
        MaterialSubtype.CLEAR_GLASS: "glass",
        MaterialSubtype.FROSTED_GLASS: "glass",
        MaterialSubtype.COLORED_GLASS: "glass",
        MaterialSubtype.PORCELAIN: "ceramic",
        MaterialSubtype.POTTERY: "ceramic",
        MaterialSubtype.MATTE_CERAMIC: "ceramic",
        MaterialSubtype.SILK: "fabric",
        MaterialSubtype.COTTON: "fabric",
        MaterialSubtype.VELVET: "fabric",
        MaterialSubtype.LEATHER: "leather",
        MaterialSubtype.POLISHED_WOOD: "wood",
        MaterialSubtype.NATURAL_WOOD: "wood",
        MaterialSubtype.ROUGH_WOOD: "wood",
        MaterialSubtype.GLOSSY_PLASTIC: "plastic",
        MaterialSubtype.MATTE_PLASTIC: "plastic",
        MaterialSubtype.RUBBER: "plastic",
        MaterialSubtype.FOOD: "organic",
        MaterialSubtype.PLANT: "organic",
        MaterialSubtype.SKIN: "skin",
    }
    
    # Type-level mapping (fallback)
    TYPE_TO_TEMPLATE = {
        MaterialType.METALLIC: "metallic",
        MaterialType.GLASS: "glass",
        MaterialType.CERAMIC: "ceramic",
        MaterialType.FABRIC: "fabric",
        MaterialType.WOOD: "wood",
        MaterialType.PLASTIC: "plastic",
        MaterialType.ORGANIC: "organic",
        MaterialType.EMISSIVE: "emissive",
        MaterialType.DIELECTRIC: "dielectric",
    }
    
    # Try subtype first
    if material_subtype:
        if isinstance(material_subtype, str):
            # Try to find matching subtype
            for st in MaterialSubtype:
                if st.value == material_subtype:
                    material_subtype = st
                    break
        
        if material_subtype in SUBTYPE_TO_TEMPLATE:
            return SUBTYPE_TO_TEMPLATE[material_subtype]
    
    # Fall back to type
    if isinstance(material_type, str):
        return material_type
    
    return TYPE_TO_TEMPLATE.get(material_type, "dielectric")


def get_material_profile_name(material_data) -> str:
    """
    Get material profile name for template lookup.
    
    Maps MaterialData to research_lookup_tables.json material_profiles.
    
    Args:
        material_data: MaterialData from MaterialAnalyzer
        
    Returns:
        Material profile name string
    """
    if not material_data:
        return "mixed"
    
    # High metallic + low roughness = high gloss
    if material_data.average_metallic > 0.7 and material_data.average_roughness < 0.2:
        return "metallic_high_gloss"
    
    # Low metallic + high roughness = dark matte
    if material_data.average_metallic < 0.2 and material_data.average_roughness > 0.7:
        return "dark_matte"
    
    # Glass-like
    if hasattr(material_data, 'has_transmission') and material_data.has_transmission:
        return "glass"
    
    # Gemstone (high metallic-like with transmission)
    if material_data.average_metallic > 0.5 and material_data.average_roughness < 0.3:
        return "gemstone"
    
    return "mixed"


# =============================================================================
# Style Mapping
# =============================================================================

def get_template_moods(style) -> List[str]:
    """
    Convert LightingStyle to template mood strings.
    
    Args:
        style: LightingStyle enum
        
    Returns:
        List of mood strings for template matching
    """
    from .scene_context.composition_analyzer import LightingStyle
    
    STYLE_TO_MOODS = {
        LightingStyle.FLAT: ["soft", "clean", "high_key"],
        LightingStyle.NATURAL: ["natural", "soft", "low_contrast"],
        LightingStyle.STUDIO: ["studio", "clean", "commercial"],
        LightingStyle.DRAMATIC: ["dramatic", "low_key", "high_contrast"],
        LightingStyle.HIGH_KEY: ["high_key", "clean", "bright"],
        LightingStyle.LOW_KEY: ["low_key", "dramatic", "moody"],
        LightingStyle.UNKNOWN: ["studio"],
    }
    
    return STYLE_TO_MOODS.get(style, ["studio"])


# =============================================================================
# Template Recommendations
# =============================================================================

def get_template_recommendations(
    category_result: Optional[ProductCategoryResult],
    material_data: Optional[MaterialData] = None,
    target_style: Optional[LightingStyle] = None
) -> List[str]:
    """
    Get recommended template IDs based on detected category and materials.
    
    Integrates with research_lookup_tables.json product_to_template_prior.
    
    Args:
        category_result: ProductCategoryResult from ProductCategoryDetector
        material_data: Optional MaterialData from MaterialAnalyzer
        target_style: Optional desired LightingStyle
        
    Returns:
        List of template IDs sorted by relevance
    """
    try:
        from .template_intelligence import get_research_lookup_tables
        tables = get_research_lookup_tables()
    except ImportError:
        # feature/template not merged yet
        return _get_default_recommendations(category_result)
    
    if not tables:
        return _get_default_recommendations(category_result)
    
    priors = tables.get("product_to_template_prior", [])
    templates = tables.get("templates", [])
    
    if not category_result:
        return ["three_point_setup"]
    
    # Get template product type
    product_type = get_template_product_type(category_result.category)
    
    # Find matching priors
    recommendations = []
    
    for prior in priors:
        if prior.get("product_type") == product_type:
            template_priors = prior.get("templates", [])
            # Sort by prior probability
            template_priors.sort(key=lambda t: t.get("prior", 0), reverse=True)
            recommendations = [t["id"] for t in template_priors]
            break
    
    # If we have material data, filter/reorder based on material match
    if material_data and templates:
        material_str = get_template_material(
            material_data.dominant_type,
            getattr(material_data, 'material_subtype', None)
        )
        
        # Score templates by material match
        scored = []
        for tid in recommendations:
            template = next((t for t in templates if t.get("id") == tid), None)
            if template:
                primary_mats = template.get("primary_materials", [])
                score = 1.0
                if material_str in primary_mats:
                    score += 0.3  # Boost for material match
                scored.append((tid, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        recommendations = [tid for tid, _ in scored]
    
    # If we have target style, filter/reorder based on mood match
    if target_style and templates:
        moods = get_template_moods(target_style)
        
        scored = []
        for tid in recommendations:
            template = next((t for t in templates if t.get("id") == tid), None)
            if template:
                template_moods = template.get("mood", [])
                score = 1.0
                # Check for mood overlap
                overlap = len(set(moods) & set(template_moods))
                score += overlap * 0.2
                scored.append((tid, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        recommendations = [tid for tid, _ in scored]
    
    return recommendations if recommendations else ["three_point_setup"]


def _get_default_recommendations(category_result) -> List[str]:
    """Default recommendations when lookup tables not available."""
    from .scene_context.product_category_detector import ProductCategory
    
    DEFAULTS = {
        ProductCategory.JEWELRY: ["jewelry_macro", "clamshell_beauty"],
        ProductCategory.FOOD: ["food_high_key_clean", "food_rustic_side_soft"],
        ProductCategory.COSMETICS: ["cosmetics_soft_gradient", "clamshell_beauty"],
        ProductCategory.ELECTRONICS: ["electronics_lowkey_rim", "product_hero_shot"],
        ProductCategory.AUTOMOTIVE: ["automotive_showroom_soft", "overcast_day"],
        ProductCategory.APPAREL: ["three_point_setup", "catalog_product"],
        ProductCategory.FURNITURE: ["furniture_lifestyle_soft", "catalog_product"],
        ProductCategory.GENERIC: ["three_point_setup", "high_key_ecommerce"],
    }
    
    if not category_result:
        return ["three_point_setup"]
    
    return DEFAULTS.get(category_result.category, ["three_point_setup"])


# =============================================================================
# Parameter Enhancement
# =============================================================================

def enhance_template_params(
    template_id: str,
    category_result: Optional[ProductCategoryResult] = None,
    material_data: Optional[MaterialData] = None,
    composition: Optional[CompositionAnalysisResult] = None
) -> Dict[str, Any]:
    """
    Enhance template parameters based on scene analysis.
    
    Returns dict of parameter overrides for template application.
    
    Args:
        template_id: Template ID being applied
        category_result: ProductCategoryResult from ProductCategoryDetector
        material_data: MaterialData from MaterialAnalyzer
        composition: CompositionAnalysisResult from CompositionAnalyzer
        
    Returns:
        Dict of parameter overrides
    """
    overrides = {}
    
    # Category-based overrides
    if category_result:
        # Color temperature
        if category_result.recommended_color_temp:
            overrides['color_temp'] = category_result.recommended_color_temp
        
        # Key:fill ratio
        if category_result.recommended_key_fill_ratio:
            overrides['key_fill_ratio'] = category_result.recommended_key_fill_ratio
        
        # Intensity/size multipliers
        if category_result.intensity_multiplier:
            overrides['intensity_multiplier'] = category_result.intensity_multiplier
        if category_result.size_multiplier:
            overrides['size_multiplier'] = category_result.size_multiplier
    
    # Material-based overrides
    if material_data:
        from .material_adaptation import MATERIAL_LIGHTING_RULES
        
        material_type = material_data.dominant_type
        if material_type in MATERIAL_LIGHTING_RULES:
            rules = MATERIAL_LIGHTING_RULES[material_type]
            
            # Don't override if already set by category
            if 'intensity_multiplier' not in overrides:
                overrides['intensity_multiplier'] = rules.get('intensity_multiplier', 1.0)
            if 'size_multiplier' not in overrides:
                overrides['size_multiplier'] = rules.get('size_multiplier', 1.0)
            
            # Material-specific adjustments
            if rules.get('reduce_shadows'):
                overrides['shadow_softness'] = 'soft'
            if rules.get('warm_up'):
                current_temp = overrides.get('color_temp', 5500)
                overrides['color_temp'] = current_temp - 300  # Warm up
    
    # Composition-based overrides
    if composition:
        from .scene_context.composition_analyzer import LightingStyle
        
        # Adjust ratio based on detected style
        if composition.style == LightingStyle.DRAMATIC:
            current_ratio = overrides.get('key_fill_ratio', 3.0)
            overrides['key_fill_ratio'] = max(current_ratio, 4.0)
        elif composition.style == LightingStyle.FLAT:
            current_ratio = overrides.get('key_fill_ratio', 3.0)
            overrides['key_fill_ratio'] = min(current_ratio, 2.0)
    
    return overrides


# =============================================================================
# Compatibility Helpers
# =============================================================================

def convert_scene_context_to_template_data(scene_ctx) -> Dict[str, Any]:
    """
    Convert SceneContext to format expected by template system.
    
    Provides backward compatibility with feature/template code.
    
    Args:
        scene_ctx: SceneContext from SceneAnalyzer
        
    Returns:
        Dict with template-compatible fields
    """
    result = {
        'bounds': scene_ctx.bounds,
        'camera': scene_ctx.camera,
        'product_type': getattr(scene_ctx, 'product_type', 'unknown'),
    }
    
    # Add material info in simple format
    if scene_ctx.materials:
        result['material_type'] = scene_ctx.materials.dominant_type
        result['is_reflective'] = (
            scene_ctx.materials.average_metallic > 0.5 or 
            scene_ctx.materials.average_roughness < 0.2
        )
        result['is_emissive'] = scene_ctx.materials.has_emission
    
    # Add product category if available
    if hasattr(scene_ctx, 'product_category') and scene_ctx.product_category:
        result['product_type'] = get_template_product_type(
            scene_ctx.product_category.category
        )
    
    return result


__all__ = [
    # Category mapping
    'get_template_product_type',
    'get_product_category_from_string',
    # Material mapping
    'get_template_material',
    'get_material_profile_name',
    # Style mapping
    'get_template_moods',
    # Recommendations
    'get_template_recommendations',
    # Parameter enhancement
    'enhance_template_params',
    # Compatibility
    'convert_scene_context_to_template_data',
]
