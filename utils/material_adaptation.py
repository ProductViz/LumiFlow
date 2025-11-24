"""
Material Adaptation utilities - Lighting adjustments berdasarkan material analysis.

Enhanced with detailed rules for 8+ material types and subtypes:
- metallic: polished_metal, brushed_metal, rough_metal
- glass: clear_glass, frosted_glass, colored_glass
- ceramic: porcelain, pottery, matte_ceramic
- fabric: silk, cotton, leather, velvet
- wood: polished_wood, natural_wood, rough_wood
- plastic: glossy_plastic, matte_plastic, rubber
- organic: food, plant, skin
- dielectric: generic fallback
"""

import bpy
from .scene_context import MaterialData, MaterialType, MaterialSubtype

# ============================================================================
# PRIMARY MATERIAL TYPE RULES
# ============================================================================

MATERIAL_LIGHTING_RULES = {
    # Metallic - needs larger soft sources to show form, reduce harsh reflections
    'metallic': {
        'intensity_multiplier': 1.2,
        'size_multiplier': 1.4,
        'color_temperature': 5500,
        'key_fill_ratio': 3.5,
        'back_light_intensity': 0.6,
    },
    # Glass - needs backlighting and careful positioning to avoid harsh reflections
    'glass': {
        'intensity_multiplier': 1.3,
        'size_multiplier': 1.0,
        'color_temperature': 6000,
        'key_fill_ratio': 2.5,
        'back_light_intensity': 0.8,  # Strong backlight for transparency
    },
    # Ceramic - medium soft light, shows form well
    'ceramic': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.2,
        'color_temperature': 5200,
        'key_fill_ratio': 3.0,
        'back_light_intensity': 0.4,
    },
    # Fabric - soft diffused light, minimal specular
    'fabric': {
        'intensity_multiplier': 0.9,
        'size_multiplier': 1.5,
        'color_temperature': 5000,
        'key_fill_ratio': 2.0,
        'back_light_intensity': 0.3,
    },
    # Wood - warm light, medium contrast
    'wood': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.2,
        'color_temperature': 4500,
        'key_fill_ratio': 2.5,
        'back_light_intensity': 0.35,
    },
    # Plastic - can handle more contrast
    'plastic': {
        'intensity_multiplier': 1.1,
        'size_multiplier': 1.1,
        'color_temperature': 5500,
        'key_fill_ratio': 3.0,
        'back_light_intensity': 0.5,
    },
    # Organic - soft, warm light for appetizing/natural look
    'organic': {
        'intensity_multiplier': 0.85,
        'size_multiplier': 1.6,
        'color_temperature': 4000,
        'key_fill_ratio': 2.0,
        'back_light_intensity': 0.4,
    },
    # Emissive - reduce external lighting
    'emissive': {
        'intensity_multiplier': 0.7,
        'size_multiplier': 1.0,
        'color_temperature': 5500,
        'key_fill_ratio': 2.0,
        'back_light_intensity': 0.2,
    },
    # Dielectric (default)
    'dielectric': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.0,
        'color_temperature': 5500,
        'key_fill_ratio': 3.0,
        'back_light_intensity': 0.5,
    },
}

# ============================================================================
# SUBTYPE-SPECIFIC ADJUSTMENTS (applied on top of primary rules)
# ============================================================================

MATERIAL_SUBTYPE_ADJUSTMENTS = {
    # Metallic subtypes
    'polished_metal': {
        'intensity_multiplier': 1.1,  # Slightly brighter for reflections
        'size_multiplier': 1.5,       # Larger source for smoother reflections
    },
    'brushed_metal': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.3,
    },
    'rough_metal': {
        'intensity_multiplier': 0.95,
        'size_multiplier': 1.2,
    },
    
    # Glass subtypes
    'clear_glass': {
        'intensity_multiplier': 1.2,
        'back_light_intensity': 0.9,  # Strong backlight
    },
    'frosted_glass': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.3,
    },
    'colored_glass': {
        'intensity_multiplier': 1.1,
        'color_temperature': 5500,    # Neutral to show color
    },
    
    # Ceramic subtypes
    'porcelain': {
        'intensity_multiplier': 1.1,
        'size_multiplier': 1.3,
    },
    'pottery': {
        'intensity_multiplier': 1.0,
        'color_temperature': 4800,
    },
    'matte_ceramic': {
        'intensity_multiplier': 0.95,
        'size_multiplier': 1.1,
    },
    
    # Fabric subtypes
    'silk': {
        'intensity_multiplier': 1.1,
        'size_multiplier': 1.3,
    },
    'cotton': {
        'intensity_multiplier': 0.95,
        'size_multiplier': 1.4,
    },
    'leather': {
        'intensity_multiplier': 1.0,
        'color_temperature': 4800,
    },
    'velvet': {
        'intensity_multiplier': 0.9,
        'size_multiplier': 1.6,
    },
    
    # Wood subtypes
    'polished_wood': {
        'intensity_multiplier': 1.1,
        'size_multiplier': 1.3,
    },
    'natural_wood': {
        'intensity_multiplier': 1.0,
    },
    'rough_wood': {
        'intensity_multiplier': 0.95,
        'size_multiplier': 1.1,
    },
    
    # Plastic subtypes
    'glossy_plastic': {
        'intensity_multiplier': 1.15,
        'size_multiplier': 1.2,
    },
    'matte_plastic': {
        'intensity_multiplier': 1.0,
    },
    'rubber': {
        'intensity_multiplier': 0.9,
        'color_temperature': 5200,
    },
    
    # Organic subtypes
    'food': {
        'intensity_multiplier': 0.9,
        'color_temperature': 3800,    # Warm for appetizing
        'size_multiplier': 1.5,
    },
    'plant': {
        'intensity_multiplier': 1.0,
        'color_temperature': 5500,    # Daylight for natural
    },
    'skin': {
        'intensity_multiplier': 0.85,
        'color_temperature': 4500,    # Warm, flattering
        'size_multiplier': 1.7,
    },
}

def generate_lighting_recommendations(material_data: MaterialData) -> dict:
    """Generate lighting recommendations from material analysis."""
    base = MATERIAL_LIGHTING_RULES.get(material_data.dominant_type)

    # Start from rule for dominant_type if available, otherwise neutral defaults
    if base is not None:
        recs = base.copy()
    else:
        recs = {
            'intensity_multiplier': 1.0,
            'size_multiplier': 1.0,
        }

    # Apply subtype-specific adjustments
    subtype_adjustments = MATERIAL_SUBTYPE_ADJUSTMENTS.get(material_data.material_subtype, {})
    for key, value in subtype_adjustments.items():
        recs[key] = recs.get(key, 1.0) * value

    # Adjust for emission
    if material_data.has_emission:
        recs['intensity_multiplier'] = recs.get('intensity_multiplier', 1.0) * 0.8

    # Adjust for roughness extremes
    if material_data.average_roughness < 0.1 or material_data.average_roughness > 0.9:
        recs['size_multiplier'] = recs.get('size_multiplier', 1.0) * 1.2

    return recs

def apply_material_adjustments_to_light(light: bpy.types.Object,
                                       recommendations: dict) -> None:
    """Apply material-based adjustments to light object."""
    if not light or light.type != 'LIGHT':
        return

    # Adjust intensity
    intensity_mult = recommendations.get('intensity_multiplier', 1.0)
    if hasattr(light.data, 'energy'):
        light.data.energy *= intensity_mult

    # Adjust size (area lights)
    if light.data.type == 'AREA':
        size_mult = recommendations.get('size_multiplier', 1.0)
        if hasattr(light.data, 'size'):
            light.data.size *= size_mult

    # Apply color temperature
    color_temp = recommendations.get('color_temperature')
    if color_temp:
        light.data.color = kelvin_to_rgb(color_temp)

def kelvin_to_rgb(kelvin: float) -> tuple:
    """Convert kelvin temperature to RGB color."""
    if kelvin <= 3000:
        return (1.0, 0.6, 0.2)
    elif kelvin <= 4000:
        return (1.0, 0.8, 0.5)
    elif kelvin <= 5500:
        return (1.0, 1.0, 1.0)
    elif kelvin <= 7000:
        return (0.8, 0.9, 1.0)
    else:
        return (0.6, 0.8, 1.0)

__all__ = [
    'generate_lighting_recommendations',
    'apply_material_adjustments_to_light',
    'kelvin_to_rgb',
    'MATERIAL_LIGHTING_RULES',
    'MATERIAL_SUBTYPE_ADJUSTMENTS',
]