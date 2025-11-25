# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Background Awareness System
Provides intelligent detection and suggestions for background/lighting interaction.
Used by both template system and background system.
"""

import bpy
from typing import List, Optional, Dict, Any, Tuple
from mathutils import Vector


class BackgroundAnalysis:
    """Analysis result for background detection."""
    
    def __init__(self):
        self.has_background: bool = False
        self.background_objects: List[bpy.types.Object] = []
        self.background_type: str = "unknown"  # seamless, backdrop, ground, custom
        self.background_color: Tuple[float, float, float] = (0.5, 0.5, 0.5)
        self.is_lumiflow_background: bool = False
        self.has_background_lights: bool = False
        self.background_lights: List[bpy.types.Object] = []
        self.recommended_lighting: str = "none"
        self.recommended_isolation: bool = False
        self.suggestions: List[str] = []


class ProductAnalysis:
    """Analysis result for product detection."""
    
    def __init__(self):
        self.has_product: bool = False
        self.product_objects: List[bpy.types.Object] = []
        self.product_center: Vector = Vector((0, 0, 0))
        self.product_dimensions: Vector = Vector((1, 1, 1))
        self.has_product_lights: bool = False
        self.product_lights: List[bpy.types.Object] = []
        self.current_template: str = ""


def analyze_background(context) -> BackgroundAnalysis:
    """
    Analyze scene for background objects and their properties.
    
    Args:
        context: Blender context
    
    Returns:
        BackgroundAnalysis with detection results
    """
    analysis = BackgroundAnalysis()
    
    # Find background objects
    for obj in context.scene.objects:
        if obj.type != 'MESH':
            continue
        
        is_bg = False
        
        # Check LumiFlow marker
        if obj.get("lumiflow_background"):
            is_bg = True
            analysis.is_lumiflow_background = True
            analysis.background_type = obj.get("lumiflow_bg_type", "seamless")
        
        # Check name patterns
        name_lower = obj.name.lower()
        if any(kw in name_lower for kw in ["background", "backdrop", "cyclorama", "seamless", "studio_bg"]):
            is_bg = True
        
        # Check if it's a large flat object behind other objects
        if not is_bg:
            dims = obj.dimensions
            # Large and relatively flat
            if max(dims.x, dims.y) > 5 and min(dims) < 0.5:
                is_bg = True
                analysis.background_type = "backdrop"
        
        if is_bg:
            analysis.background_objects.append(obj)
    
    analysis.has_background = len(analysis.background_objects) > 0
    
    # Analyze background color if found
    if analysis.has_background:
        bg_obj = analysis.background_objects[0]
        analysis.background_color = _get_object_base_color(bg_obj)
        
        # Determine type from color if not set
        if analysis.background_type == "unknown":
            r, g, b = analysis.background_color
            avg = (r + g + b) / 3
            
            if avg > 0.9:
                analysis.background_type = "white"
            elif avg < 0.1:
                analysis.background_type = "black"
            elif abs(r - g) < 0.1 and abs(g - b) < 0.1:
                analysis.background_type = "gray"
            else:
                analysis.background_type = "colored"
    
    # Find background lights
    for obj in context.scene.objects:
        if obj.type == 'LIGHT':
            if obj.get("lumiflow_bg_light"):
                analysis.background_lights.append(obj)
            elif obj.get("lumiflow_layer") == "background":
                analysis.background_lights.append(obj)
            elif "bg" in obj.name.lower() or "background" in obj.name.lower():
                analysis.background_lights.append(obj)
    
    analysis.has_background_lights = len(analysis.background_lights) > 0
    
    # Generate recommendations
    _generate_background_recommendations(analysis)
    
    return analysis


def analyze_product(context) -> ProductAnalysis:
    """
    Analyze scene for product objects and their lighting.
    
    Args:
        context: Blender context
    
    Returns:
        ProductAnalysis with detection results
    """
    analysis = ProductAnalysis()
    
    # Get background objects to exclude
    bg_analysis = analyze_background(context)
    bg_set = set(bg_analysis.background_objects)
    
    # Find product objects from selection
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj not in bg_set:
            analysis.product_objects.append(obj)
    
    # If nothing selected, find reasonable product candidates
    if not analysis.product_objects:
        for obj in context.scene.objects:
            if obj.type == 'MESH' and obj not in bg_set:
                dims = obj.dimensions
                # Reasonable product size (not too large)
                if max(dims) < 20:
                    analysis.product_objects.append(obj)
    
    analysis.has_product = len(analysis.product_objects) > 0
    
    # Calculate product bounds
    if analysis.has_product:
        min_co = Vector((float('inf'), float('inf'), float('inf')))
        max_co = Vector((float('-inf'), float('-inf'), float('-inf')))
        
        for obj in analysis.product_objects:
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ Vector(corner)
                min_co.x = min(min_co.x, world_corner.x)
                min_co.y = min(min_co.y, world_corner.y)
                min_co.z = min(min_co.z, world_corner.z)
                max_co.x = max(max_co.x, world_corner.x)
                max_co.y = max(max_co.y, world_corner.y)
                max_co.z = max(max_co.z, world_corner.z)
        
        analysis.product_center = (min_co + max_co) / 2
        analysis.product_dimensions = max_co - min_co
    
    # Find product lights
    for obj in context.scene.objects:
        if obj.type == 'LIGHT':
            # Skip background lights
            if obj.get("lumiflow_bg_light"):
                continue
            if obj.get("lumiflow_layer") == "background":
                continue
            
            # Check if it's a product light
            if obj.get("lumiflow_layer") == "product":
                analysis.product_lights.append(obj)
            elif any(kw in obj.name.lower() for kw in ["key", "fill", "rim", "main", "product"]):
                analysis.product_lights.append(obj)
            else:
                # Default: assume it's a product light if not marked as background
                analysis.product_lights.append(obj)
    
    analysis.has_product_lights = len(analysis.product_lights) > 0
    
    return analysis


def _get_object_base_color(obj: bpy.types.Object) -> Tuple[float, float, float]:
    """Get base color from object's material."""
    if not obj.data.materials:
        return (0.5, 0.5, 0.5)
    
    mat = obj.data.materials[0]
    if not mat or not mat.use_nodes:
        return (0.5, 0.5, 0.5)
    
    # Find Principled BSDF
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            color = node.inputs['Base Color'].default_value
            return (color[0], color[1], color[2])
    
    return (0.5, 0.5, 0.5)


def _generate_background_recommendations(analysis: BackgroundAnalysis) -> None:
    """Generate recommendations based on background analysis."""
    
    if not analysis.has_background:
        analysis.suggestions.append("No background detected. Consider adding one with Ctrl+Shift+B")
        return
    
    bg_type = analysis.background_type
    
    # Lighting recommendations
    if bg_type in ("white", "seamless"):
        analysis.recommended_lighting = "even_fill_high"
        analysis.recommended_isolation = True
        if not analysis.has_background_lights:
            analysis.suggestions.append("White background detected - add background lighting for pure white")
    
    elif bg_type == "black":
        analysis.recommended_lighting = "none"
        analysis.recommended_isolation = True
        analysis.suggestions.append("Black background - consider rim accent for separation")
    
    elif bg_type == "gray":
        analysis.recommended_lighting = "even_fill_medium"
        analysis.recommended_isolation = True
    
    elif bg_type == "colored":
        analysis.recommended_lighting = "even_fill_medium"
        analysis.recommended_isolation = True
        analysis.suggestions.append("Colored background - enable isolation to prevent color cast on product")
    
    # Check if isolation is needed
    if analysis.has_background and not analysis.recommended_isolation:
        r, g, b = analysis.background_color
        # If background is not neutral, recommend isolation
        if not (abs(r - g) < 0.1 and abs(g - b) < 0.1):
            analysis.recommended_isolation = True


def get_smart_suggestions(context) -> Dict[str, Any]:
    """
    Get smart suggestions for current scene state.
    
    Returns:
        Dictionary with suggestions for user
    """
    bg_analysis = analyze_background(context)
    product_analysis = analyze_product(context)
    
    suggestions = {
        "background": bg_analysis,
        "product": product_analysis,
        "actions": [],
    }
    
    # Generate action suggestions
    if not bg_analysis.has_background and product_analysis.has_product:
        suggestions["actions"].append({
            "type": "add_background",
            "message": "Add a background for your product",
            "operator": "lumi.background_menu_call",
        })
    
    if bg_analysis.has_background and not bg_analysis.has_background_lights:
        if bg_analysis.background_type in ("white", "seamless"):
            suggestions["actions"].append({
                "type": "add_bg_lighting",
                "message": "Add background lighting for pure white",
                "operator": "lumi.apply_background",
                "preset": "even_fill_high",
            })
    
    if (bg_analysis.has_background and product_analysis.has_product_lights 
        and bg_analysis.recommended_isolation):
        suggestions["actions"].append({
            "type": "apply_isolation",
            "message": "Apply layer isolation for better control",
            "operator": "lumi.apply_layer_isolation",
        })
    
    return suggestions


def should_suggest_background(context) -> bool:
    """Check if we should suggest adding a background."""
    bg_analysis = analyze_background(context)
    product_analysis = analyze_product(context)
    
    return product_analysis.has_product and not bg_analysis.has_background


def should_suggest_isolation(context) -> bool:
    """Check if we should suggest layer isolation."""
    bg_analysis = analyze_background(context)
    product_analysis = analyze_product(context)
    
    return (bg_analysis.has_background 
            and product_analysis.has_product_lights 
            and bg_analysis.recommended_isolation)


def get_recommended_lighting_for_background(context) -> str:
    """Get recommended lighting preset for current background."""
    bg_analysis = analyze_background(context)
    return bg_analysis.recommended_lighting
