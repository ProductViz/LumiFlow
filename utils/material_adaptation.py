"""
Material Adaptation utilities - Lighting adjustments berdasarkan material analysis.
Extracted dari template_analyzer.py material adjustment logic.
"""

import bpy
from .scene_context import MaterialData

MATERIAL_LIGHTING_RULES = {
    'metallic': {
        'intensity_multiplier': 1.2,
        'size_multiplier': 1.3,
        'color_temperature': 5500,
    },
    'glass': {
        'intensity_multiplier': 1.4,
        'size_multiplier': 1.0,
        'color_temperature': 6500,
    },
    'dielectric': {
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.0,
        'color_temperature': 5500,
    }
}

def generate_lighting_recommendations(material_data: MaterialData) -> dict:
    """Generate lighting recommendations from material analysis."""
    recs = MATERIAL_LIGHTING_RULES.get(material_data.dominant_type, {}).copy()

    # Adjust for emission
    if material_data.has_emission:
        recs['intensity_multiplier'] *= 0.8

    # Adjust for roughness extremes
    if material_data.average_roughness < 0.1 or material_data.average_roughness > 0.9:
        recs['size_multiplier'] *= 1.2

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
    'MATERIAL_LIGHTING_RULES'
]