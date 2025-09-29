"""
Info Overlay Module
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
    
    # Rendering preparation
    colors = get_config_colors(context)
    (info_x, info_y), _ = get_overlay_positions(context, region)
    font_scale, line_spacing = get_text_settings(context)
    
    info_lines = get_info_lines(selected_lights[0], context, colors)
    
    if info_lines:
        draw_text(info_lines, (info_x, info_y), font_scale=font_scale, line_spacing=line_spacing)


def get_info_lines(light_obj, context, colors):
    """Get info lines for light display using centralized mode management."""
    data = light_obj.data
    ltype = data.type
    
    smart_mode = getattr(context.scene, 'lumi_smart_mode', 'DISTANCE')
    scroll_control_active = getattr(context.scene, 'lumi_scroll_control_enabled', False)
    
    display_type = ltype
    if ltype == 'AREA':
        shape = getattr(data, "shape", "SQUARE")
        display_type = f"{ltype} {shape}"
    
    lines = [
        (display_type, "", colors['normal'], 0.3, 0.5, 1.0),  
        (light_obj.name, "", colors['normal'], 0.5, 0.5, 1.0)   
    ]
    
    all_modes_info = ModeManager.get_all_modes_info(light_obj, context)
    
    for label, value in all_modes_info:
        mode_name = None
        for mode in ModeManager.MODES.keys():
            if ModeManager.get_mode_display_name(mode, ltype) == label:
                mode_name = mode
                break
        
        if mode_name and scroll_control_active and smart_mode == mode_name:
            color = colors['highlight']
        else:
            color = colors['secondary']
        
        if 'm' in value and not value.endswith('m'):
            clean_value = value.replace('m', '').strip() + 'm'
        elif 'K' in value and not value.endswith('K'):
            clean_value = value.replace(' K', '').strip() + 'K'
        else:
            clean_value = value
        
        lines.append((label, f": {clean_value}", color, 0.5, 0.5))  
    
    if hasattr(data, 'color') and len(data.color) >= 3:
        r, g, b = data.color[:]
        h, s, v = lumi_rgb_to_hsv(r, g, b)
        if h > 0 or s > 0 or v > 0:
            lines.append(("HSV", f": {h:.0f}Â°/{s:.0f}%/{v:.0f}%", colors['secondary'], 0.2, 0.5))  # spacing_before=0.2, spacing_after=0.5
    
    return lines

