# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Tips Overlay Module
Contains tips display functions.
"""
import bpy
import blf
from typing import List, Tuple
from mathutils import Vector

from .config import OverlayConfig
from .utils import get_overlay_positions, draw_text, get_text_settings, get_config_colors
from ..utils import lumi_get_light_collection
from ..utils.mode_manager import ModeManager

# draw_scroll_overlay() moved to overlay_cursor.py as draw_overlay_cursor()
# get_smart_overlay() moved to overlay_cursor.py

def draw_overlay_tips():
    """Draw tips when no lights are selected or present in the scene."""
    context = bpy.context
    region = context.region
    if not region:
        return
    
    # Check if overlay tips is enabled
    show_tips = getattr(context.scene, 'lumi_show_overlay_tips', True)
    if not show_tips:
        return
    
    font_id = 0
    blf.size(font_id, 12)
    
    colors = get_config_colors(context)
    (info_x, info_y), (tips_x, tips_y) = get_overlay_positions(context, region)
    
    # Check if there are any lights in the scene
    light_col = lumi_get_light_collection(context.scene)
    lights = [obj for obj in light_col.objects if obj.type == 'LIGHT'] if light_col else []
    
    # Check if there's a selected light
    selected_light = None
    if context.selected_objects:
        # Get selected lights that are in LumiFlow collection
        selected_lights = [obj for obj in context.selected_objects 
                          if obj.type == 'LIGHT' and (not light_col or obj.name in light_col.objects)]
        if selected_lights:
            selected_light = selected_lights[0]  # Use first selected light
    
    if not lights:
        # No lights in scene - show creation tips
        tips_lines = [
            ("ðŸ’¡ LumiFlow Tips", "", colors['header'], 0.5, 1.0, 1.3),  
            ("ðŸš€ Create Your First Light:", "", colors['normal'], 0.3, 0.8, 1.1),   
            ("1. Select or Point mouse at mesh surface", "", colors['secondary'], 0.5, 0.5, 1.0),  
            ("2. Press", ": Ctrl + Shift + A", colors['secondary'], 0.5, 50, 1.0),
            ("3. Choose light type from menu", "", colors['secondary'], 0.5, 1.0, 1.0),
        ]
    elif selected_light:
        # Has selected light - show available smart control modes
        tips_lines = get_selected_light_tips_template(selected_light, colors)
    else:
        # Has lights but none selected - show general tips
        tips_lines = get_general_tips_template(colors)
    
    font_scale, line_spacing = get_text_settings(context)
    
    # Draw tips using the proven draw_text function
    from .utils import draw_text
    draw_text(tips_lines, (tips_x, tips_y), font_scale, line_spacing, is_tips=True)

def get_general_tips_template(colors=None):
    """Get general tips template"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    return [
        ("ðŸ’¡ LumiFlow Tips", "", colors['header'], 0.7, 1.0, 1.3),  
        ("Select a light to begin", "", colors['normal'], 0.5, 0.8, 1.1),
        ("Flip Light", ": Ctrl + Shift + C", colors['secondary'], 0.5, 90, 1.0),
        ("Light Linking", ": Ctrl + Shift + X", colors['secondary'], 0.5, 90, 1.0),
        ("Cycle Selection", ": Ctrl + Shift + D", colors['secondary'], 0.7, 90, 1.0),
        ("Or Add More Ligt", "", colors['normal'], 0.5, 0.5, 1.0),
        ("Smart Add", ": Ctrl + Shift + A", colors['dim'], 0.5, 90,1.0),

    ]

def get_selected_light_tips_template(selected_light, colors=None):
    """Get tips template for selected light showing available smart control and positioning modes using centralized system"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    # Get available modes for this light type using centralized system
    light_type = selected_light.data.type
    
    tips_lines = [
        ("ðŸ’¡ LumiFlow Tips", "", colors['header'], 0.7, 1.0, 1.3), 
        ("Smart Controls:", "", colors['normal'], 0.5, 0.8, 1.1),
    ]
    
    # Add smart control modes based on light type
    if light_type == 'POINT':
        tips_lines.extend([
            ("  Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Radius", ": Alt + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Temperature", ": Ctrl+Alt + MMB_Drag", colors['secondary'], 0.7, 95, 1.0),
        ])
    elif light_type == 'SUN':
        tips_lines.extend([
            ("  Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Angle", ": Alt + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Temperature", ": Ctrl+Alt + MMB_Drag", colors['secondary'], 0.7, 95, 1.0),
        ])
    elif light_type == 'SPOT':
        tips_lines.extend([
            ("  Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Angle", ": Alt + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Blend", ": Ctrl+Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Temperature", ": Shift+Alt + MMB_Drag", colors['secondary'], 0.7, 95, 1.0),
        ])
    elif light_type == 'AREA':
        tips_lines.extend([
            ("  Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Scale", ": Alt + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Blend", ": Ctrl+Shift + MMB_Drag", colors['secondary'], 0.5, 95, 1.0),
            ("  Temperature", ": Shift+Alt + MMB_Drag", colors['secondary'], 0.7, 95, 1.0),
        ])
    
    # Add positioning modes section
    tips_lines.extend([
        ("Positioning Modes:", "", colors['normal'], 0.5, 70, 1.0),
        ("  Highlight", ": Ctrl + LMB_Drag", colors['secondary'], 0.5, 70, 1.0),
        ("  Normal", ": Shift + LMB_Drag", colors['secondary'], 0.5, 70, 1.0),
        ("  Orbit", ": Alt + LMB_Drag", colors['secondary'], 0.5, 70, 1.0),
        ("  Target", ": Ctrl+Alt + LMB_Drag", colors['secondary'], 0.5, 70, 1.0),
        ("  Free", ": Ctrl+Shift + LMB_Drag", colors['secondary'], 0.5, 70, 1.0),
        ("  Move", ": Shift+Alt + LMB_Drag", colors['secondary'], 0.7, 70, 1.0),
    ])
    
    # Add general tips
    tips_lines.extend([
        ("Other Options:", "", colors['normal'], 0.5, 0.3, 1.0),
        ("  Flip Light", ": Ctrl + Shift + C", colors['secondary'], 0.5, 90, 1.0),
        ("  Light Linking", ": Ctrl + Shift + X", colors['secondary'], 0.5, 90, 1.0),
        ("  Cycle Select", ": Ctrl + Shift + D", colors['secondary'], 0.5, 90, 1.0),
        
    ])
    
    return tips_lines



