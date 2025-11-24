"""
MaterialAnalyzer - Centralized material analysis for lighting adaptation.
Menggantikan logic dari:
- obstruction_detector._analyze_materials()
- template_analyzer.analyze_materials()
"""

import bpy
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class MaterialType(str, Enum):
    """Primary material types."""
    METALLIC = "metallic"
    GLASS = "glass"
    CERAMIC = "ceramic"
    FABRIC = "fabric"
    WOOD = "wood"
    PLASTIC = "plastic"
    ORGANIC = "organic"
    DIELECTRIC = "dielectric"  # Default/fallback
    EMISSIVE = "emissive"


class MaterialSubtype(str, Enum):
    """Material subtypes for more precise classification."""
    # Metallic
    POLISHED_METAL = "polished_metal"     # Low roughness metallic
    BRUSHED_METAL = "brushed_metal"       # Medium roughness metallic
    ROUGH_METAL = "rough_metal"           # High roughness metallic
    
    # Glass
    CLEAR_GLASS = "clear_glass"           # High transmission, low roughness
    FROSTED_GLASS = "frosted_glass"       # High transmission, medium roughness
    COLORED_GLASS = "colored_glass"       # Tinted glass
    
    # Ceramic
    PORCELAIN = "porcelain"               # Low roughness ceramic
    POTTERY = "pottery"                   # Medium roughness ceramic
    MATTE_CERAMIC = "matte_ceramic"       # High roughness ceramic
    
    # Fabric
    SILK = "silk"                         # Low roughness fabric
    COTTON = "cotton"                     # Medium roughness fabric
    LEATHER = "leather"                   # Medium roughness, slightly metallic
    VELVET = "velvet"                     # High roughness fabric
    
    # Wood
    POLISHED_WOOD = "polished_wood"       # Low roughness wood
    NATURAL_WOOD = "natural_wood"         # Medium roughness wood
    ROUGH_WOOD = "rough_wood"             # High roughness wood
    
    # Plastic
    GLOSSY_PLASTIC = "glossy_plastic"     # Low roughness plastic
    MATTE_PLASTIC = "matte_plastic"       # Medium roughness plastic
    RUBBER = "rubber"                     # High roughness, dark
    
    # Organic
    FOOD = "food"                         # SSS materials
    PLANT = "plant"                       # Green, SSS
    SKIN = "skin"                         # SSS, flesh tones
    
    # Default
    GENERIC = "generic"                   # Unclassified


@dataclass
class MaterialData:
    """Material analysis results with enhanced subcategories."""
    dominant_type: str  # MaterialType value
    has_emission: bool
    average_roughness: float
    average_metallic: float
    material_count: int
    emission_strength: float
    dominant_color: tuple  # (r, g, b)
    
    # Enhanced classification
    material_subtype: str = "generic"  # MaterialSubtype value
    
    # Enrichment fields
    has_transmission: bool = False
    average_transmission: float = 0.0
    has_sss: bool = False
    average_sss: float = 0.0
    texture_complexity: str = 'solid'  # 'solid' | 'simple' | 'complex'
    
    # Additional analysis
    is_reflective: bool = False      # High specular reflection
    is_transparent: bool = False     # Has significant transmission
    is_organic: bool = False         # Has SSS (organic-looking)
    color_saturation: float = 0.0    # 0.0-1.0, how colorful


class MaterialAnalyzer:
    """
    Analyzes materials in selected objects untuk lighting adaptation.
    """

    def analyze(self, objects: List[bpy.types.Object]) -> MaterialData:
        """
        Analyze materials dari selected objects.

        Args:
            objects: Objects to analyze

        Returns:
            MaterialData dengan analysis results
        """
        if not objects:
            return self._empty_analysis()

        all_materials = []
        emission_materials = []
        roughness_values = []
        metallic_values = []
        colors = []
        transmission_values = []
        sss_values = []
        texture_counts = []

        # Collect material data dari semua objects
        for obj in objects:
            if not hasattr(obj, 'data') or not hasattr(obj.data, 'materials'):
                continue

            for material in obj.data.materials:
                if not material:
                    continue

                all_materials.append(material)

                # Check for emission & texture usage
                has_emission = False
                tex_count = 0
                if material.node_tree:
                    for node in material.node_tree.nodes:
                        if node.type == 'EMISSION':
                            has_emission = True
                        elif node.type == 'TEX_IMAGE':
                            tex_count += 1
                if has_emission:
                    emission_materials.append(material)
                texture_counts.append(tex_count)

                # Get Principled BSDF properties
                principled = self._get_principled_bsdf(material)
                if principled:
                    roughness_values.append(principled.inputs['Roughness'].default_value)
                    metallic_values.append(principled.inputs['Metallic'].default_value)

                    # Transmission & SSS
                    if 'Transmission' in principled.inputs:
                        transmission_values.append(principled.inputs['Transmission'].default_value)
                    if 'Subsurface' in principled.inputs:
                        sss_values.append(principled.inputs['Subsurface'].default_value)

                    # Get base color
                    color_input = principled.inputs['Base Color']
                    if color_input.is_linked:
                        # Handle linked color (simplified)
                        colors.append((0.8, 0.8, 0.8))  # Default gray
                    else:
                        color = color_input.default_value
                        colors.append((color[0], color[1], color[2]))

        # Calculate averages
        avg_roughness = sum(roughness_values) / len(roughness_values) if roughness_values else 0.5
        avg_metallic = sum(metallic_values) / len(metallic_values) if metallic_values else 0.0

        # Determine dominant type
        dominant_type = self._classify_material_type(avg_metallic, avg_roughness, emission_materials)

        # Calculate dominant color
        dominant_color = self._calculate_dominant_color(colors)

        # Calculate emission strength
        emission_strength = len(emission_materials) / len(all_materials) if all_materials else 0.0

        # Transmission & SSS metrics
        has_transmission = any(t > 0.1 for t in transmission_values)
        avg_transmission = sum(transmission_values) / len(transmission_values) if transmission_values else 0.0
        has_sss = any(s > 0.1 for s in sss_values)
        avg_sss = sum(sss_values) / len(sss_values) if sss_values else 0.0

        texture_complexity = self._estimate_texture_complexity(texture_counts)
        
        # Enhanced classification
        dominant_type, material_subtype = self._classify_material_enhanced(
            avg_metallic, avg_roughness, avg_transmission, avg_sss,
            dominant_color, emission_materials
        )
        
        # Calculate derived properties
        is_reflective = avg_metallic > 0.5 or avg_roughness < 0.2
        is_transparent = avg_transmission > 0.3
        is_organic = avg_sss > 0.1
        color_saturation = self._calculate_saturation(dominant_color)

        return MaterialData(
            dominant_type=dominant_type,
            has_emission=len(emission_materials) > 0,
            average_roughness=avg_roughness,
            average_metallic=avg_metallic,
            material_count=len(all_materials),
            emission_strength=emission_strength,
            dominant_color=dominant_color,
            material_subtype=material_subtype,
            has_transmission=has_transmission,
            average_transmission=avg_transmission,
            has_sss=has_sss,
            average_sss=avg_sss,
            texture_complexity=texture_complexity,
            is_reflective=is_reflective,
            is_transparent=is_transparent,
            is_organic=is_organic,
            color_saturation=color_saturation,
        )

    def _empty_analysis(self) -> MaterialData:
        """Return empty analysis for no objects."""
        return MaterialData(
            dominant_type='dielectric',
            has_emission=False,
            average_roughness=0.5,
            average_metallic=0.0,
            material_count=0,
            emission_strength=0.0,
            dominant_color=(0.8, 0.8, 0.8),
            material_subtype='generic',
            has_transmission=False,
            average_transmission=0.0,
            has_sss=False,
            average_sss=0.0,
            texture_complexity='solid',
            is_reflective=False,
            is_transparent=False,
            is_organic=False,
            color_saturation=0.0,
        )

    def _get_principled_bsdf(self, material: bpy.types.Material) -> Optional[bpy.types.Node]:
        """Get Principled BSDF node dari material."""
        if not material.node_tree:
            return None

        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                return node
        return None

    def _classify_material_type(self, metallic: float, roughness: float,
                               emission_materials: List) -> str:
        """Classify material type berdasarkan properties (legacy)."""
        if metallic > 0.8:
            return 'metallic'
        elif len(emission_materials) > 0:
            return 'emissive'
        elif roughness < 0.1:
            return 'glass'
        else:
            return 'dielectric'
    
    def _classify_material_enhanced(self, metallic: float, roughness: float,
                                    transmission: float, sss: float,
                                    color: tuple, emission_materials: List) -> tuple:
        """
        Enhanced material classification with type and subtype.
        
        Returns:
            Tuple of (MaterialType value, MaterialSubtype value)
        """
        # Emissive check first
        if len(emission_materials) > 0:
            return MaterialType.EMISSIVE.value, MaterialSubtype.GENERIC.value
        
        # Metallic materials
        if metallic > 0.6:
            if roughness < 0.15:
                return MaterialType.METALLIC.value, MaterialSubtype.POLISHED_METAL.value
            elif roughness < 0.4:
                return MaterialType.METALLIC.value, MaterialSubtype.BRUSHED_METAL.value
            else:
                return MaterialType.METALLIC.value, MaterialSubtype.ROUGH_METAL.value
        
        # Glass/transparent materials
        if transmission > 0.3:
            if roughness < 0.1:
                # Check if colored
                if self._is_colored(color):
                    return MaterialType.GLASS.value, MaterialSubtype.COLORED_GLASS.value
                return MaterialType.GLASS.value, MaterialSubtype.CLEAR_GLASS.value
            else:
                return MaterialType.GLASS.value, MaterialSubtype.FROSTED_GLASS.value
        
        # Organic/SSS materials
        if sss > 0.1:
            # Check color for food vs plant vs skin
            if self._is_green_color(color):
                return MaterialType.ORGANIC.value, MaterialSubtype.PLANT.value
            elif self._is_skin_tone(color):
                return MaterialType.ORGANIC.value, MaterialSubtype.SKIN.value
            else:
                return MaterialType.ORGANIC.value, MaterialSubtype.FOOD.value
        
        # Non-metallic materials based on roughness and color
        # Ceramic (smooth, often white/colored)
        if roughness < 0.3 and not self._is_wood_color(color):
            if roughness < 0.1:
                return MaterialType.CERAMIC.value, MaterialSubtype.PORCELAIN.value
            else:
                return MaterialType.CERAMIC.value, MaterialSubtype.POTTERY.value
        
        # Fabric (high roughness, soft colors)
        if roughness > 0.6:
            # Check for leather (slightly metallic, medium roughness)
            if metallic > 0.1 and roughness < 0.8:
                return MaterialType.FABRIC.value, MaterialSubtype.LEATHER.value
            elif roughness > 0.85:
                return MaterialType.FABRIC.value, MaterialSubtype.VELVET.value
            else:
                return MaterialType.FABRIC.value, MaterialSubtype.COTTON.value
        
        # Wood (brown/tan colors, medium roughness)
        if self._is_wood_color(color) and 0.3 <= roughness <= 0.7:
            if roughness < 0.4:
                return MaterialType.WOOD.value, MaterialSubtype.POLISHED_WOOD.value
            elif roughness < 0.6:
                return MaterialType.WOOD.value, MaterialSubtype.NATURAL_WOOD.value
            else:
                return MaterialType.WOOD.value, MaterialSubtype.ROUGH_WOOD.value
        
        # Plastic (medium roughness, often saturated colors)
        if 0.2 <= roughness <= 0.6:
            if roughness < 0.35:
                return MaterialType.PLASTIC.value, MaterialSubtype.GLOSSY_PLASTIC.value
            elif self._is_dark_color(color) and roughness > 0.5:
                return MaterialType.PLASTIC.value, MaterialSubtype.RUBBER.value
            else:
                return MaterialType.PLASTIC.value, MaterialSubtype.MATTE_PLASTIC.value
        
        # Default fallback
        return MaterialType.DIELECTRIC.value, MaterialSubtype.GENERIC.value
    
    def _is_colored(self, color: tuple) -> bool:
        """Check if color is significantly tinted (not grayscale)."""
        if len(color) < 3:
            return False
        r, g, b = color[:3]
        avg = (r + g + b) / 3
        variance = abs(r - avg) + abs(g - avg) + abs(b - avg)
        return variance > 0.15
    
    def _is_green_color(self, color: tuple) -> bool:
        """Check if color is greenish (plants)."""
        if len(color) < 3:
            return False
        r, g, b = color[:3]
        return g > r and g > b and g > 0.3
    
    def _is_skin_tone(self, color: tuple) -> bool:
        """Check if color is skin-like."""
        if len(color) < 3:
            return False
        r, g, b = color[:3]
        # Skin tones: r > g > b, warm colors
        return r > g > b and r > 0.5 and b < 0.6
    
    def _is_wood_color(self, color: tuple) -> bool:
        """Check if color is brown/tan (wood)."""
        if len(color) < 3:
            return False
        r, g, b = color[:3]
        # Brown/tan: r >= g > b, warm
        return r >= g and g > b and r > 0.3 and r < 0.8 and b < 0.4
    
    def _is_dark_color(self, color: tuple) -> bool:
        """Check if color is dark."""
        if len(color) < 3:
            return False
        r, g, b = color[:3]
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 0.2
    
    def _calculate_saturation(self, color: tuple) -> float:
        """Calculate color saturation (0-1)."""
        if len(color) < 3:
            return 0.0
        r, g, b = color[:3]
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        if max_c == 0:
            return 0.0
        return (max_c - min_c) / max_c

    def _calculate_dominant_color(self, colors: List[tuple]) -> tuple:
        """Calculate dominant color dari list of colors."""
        if not colors:
            return (0.8, 0.8, 0.8)

        # Simple average untuk sekarang
        r_sum = sum(c[0] for c in colors)
        g_sum = sum(c[1] for c in colors)
        b_sum = sum(c[2] for c in colors)

        count = len(colors)
        return (r_sum/count, g_sum/count, b_sum/count)

    def _estimate_texture_complexity(self, texture_counts: List[int]) -> str:
        """Estimate texture complexity based on jumlah image texture per material."""
        if not texture_counts:
            return 'solid'

        max_count = max(texture_counts)
        if max_count == 0:
            return 'solid'
        if max_count <= 2:
            return 'simple'
        return 'complex'


__all__ = [
    'MaterialAnalyzer',
    'MaterialData',
    'MaterialType',
    'MaterialSubtype',
]