# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Info Display Module
Contains information display and text overlay functions.
"""

import bpy
import math
from mathutils import Vector
from .utils import get_text_settings, get_config_colors, get_overlay_positions, draw_text
from ..utils import lumi_rgb_to_hsv, lumi_get_light_pivot
from ..utils.light import lumi_get_selected_lights
from ..utils.mode_manager import ModeManager


def draw_overlay_info():
    """Draw overlay info for selected lights."""
    context = bpy.context
    region = context.region
    if not region:
        return
    
    if not getattr(context.scene, "lumi_show_overlay_info", True):
        return
    
    selected_lights = lumi_get_selected_lights()
    if not selected_lights:
        return
    
    # Persiapan rendering
    colors = get_config_colors(context)
    (info_x, info_y), _ = get_overlay_positions(context, region)
    font_scale, line_spacing = get_text_settings(context)
    
    # Generate info lines
    info_lines = get_info_lines(selected_lights[0], context, colors)
    
    # Render
    if info_lines:
        draw_text(info_lines, (info_x, info_y), font_scale=font_scale, line_spacing=line_spacing)


def get_info_lines(light_obj, context, colors):
    """Get info lines for light display using centralized mode management."""
    data = light_obj.data
    ltype = data.type
    
    # Get current smart control mode and check if scroll control is active
    smart_mode = getattr(context.scene, 'lumi_smart_mode', 'DISTANCE')
    scroll_control_active = getattr(context.scene, 'lumi_scroll_control_enabled', False)
    
    # Light type and name
    display_type = ltype
    if ltype == 'AREA':
        shape = getattr(data, "shape", "SQUARE")
        display_type = f"{ltype} {shape}"
    
    lines = [
        (display_type, "", colors['normal'], 0.3, 0.5, 1.0),  
        (light_obj.name, "", colors['normal'], 0.5, 0.5, 1.0)   
    ]
    
    # Get all available modes information using centralized system
    all_modes_info = ModeManager.get_all_modes_info(light_obj, context)
    
    # Process each mode for display
    for label, value in all_modes_info:
        # Determine which mode this corresponds to for highlighting
        mode_name = None
        for mode in ModeManager.MODES.keys():
            if ModeManager.get_mode_display_name(mode, ltype) == label:
                mode_name = mode
                break
        
        # Apply highlighting if this mode is active and scroll control is active
        if mode_name and scroll_control_active and smart_mode == mode_name:
            color = colors['highlight']
        else:
            color = colors['secondary']
        
        # Special formatting for certain values
        if 'm' in value and not value.endswith('m'):
            # Ensure meter values have proper formatting
            clean_value = value.replace('m', '').strip() + 'm'
        elif 'K' in value and not value.endswith('K'):
            # Ensure temperature values have proper formatting
            clean_value = value.replace(' K', '').strip() + 'K'
        else:
            clean_value = value
        
        lines.append((label, f": {clean_value}", color, 0.5, 0.5))  
    
    # Add HSV color information (not handled by mode system)
    if hasattr(data, 'color') and len(data.color) >= 3:
        r, g, b = data.color[:]
        h, s, v = lumi_rgb_to_hsv(r, g, b)
        if h > 0 or s > 0 or v > 0:
            lines.append(("HSV", f": {h:.0f}Â°/{s:.0f}%/{v:.0f}%", colors['secondary'], 0.2, 0.5))  # spacing_before=0.2, spacing_after=0.5
    
    return lines

