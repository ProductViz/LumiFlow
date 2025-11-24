"""
MaterialAnalyzer - Centralized material analysis for lighting adaptation.
Menggantikan logic dari:
- obstruction_detector._analyze_materials()
- template_analyzer.analyze_materials()
"""

import bpy
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class MaterialData:
    """Material analysis results."""
    dominant_type: str  # 'metallic', 'glass', 'dielectric', etc.
    has_emission: bool
    average_roughness: float
    average_metallic: float
    material_count: int
    emission_strength: float
    dominant_color: tuple  # (r, g, b)
    # Enrichment fields
    has_transmission: bool = False
    average_transmission: float = 0.0
    has_sss: bool = False
    average_sss: float = 0.0
    texture_complexity: str = 'solid'  # 'solid' | 'simple' | 'complex'


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

        return MaterialData(
            dominant_type=dominant_type,
            has_emission=len(emission_materials) > 0,
            average_roughness=avg_roughness,
            average_metallic=avg_metallic,
            material_count=len(all_materials),
            emission_strength=emission_strength,
            dominant_color=dominant_color,
            has_transmission=has_transmission,
            average_transmission=avg_transmission,
            has_sss=has_sss,
            average_sss=avg_sss,
            texture_complexity=texture_complexity,
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
            has_transmission=False,
            average_transmission=0.0,
            has_sss=False,
            average_sss=0.0,
            texture_complexity='solid',
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
        """Classify material type berdasarkan properties."""
        if metallic > 0.8:
            return 'metallic'
        elif len(emission_materials) > 0:
            return 'emissive'
        elif roughness < 0.1:
            return 'glass'
        else:
            return 'dielectric'

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


__all__ = ['MaterialAnalyzer', 'MaterialData']