"""
Text Overlay Module
Contains all text-based overlay functions: info display, tips, and cursor overlays.
Merged from overlay_info.py, overlay_tips.py, and overlay_cursor.py.
"""

import bpy
import blf
import math
from typing import List, Tuple
from mathutils import Vector
from bpy_extras import view3d_utils

from .config import OverlayConfig
from .utils import (
    get_text_settings, 
    get_config_colors, 
    get_overlay_positions, 
    draw_text
)
from ...utils import lumi_rgb_to_hsv, lumi_get_light_pivot, lumi_get_light_collection
from ...utils.light import lumi_get_selected_lights
from ...utils.mode_manager import ModeManager


# ============================================================================
# INFO OVERLAY - Light information display
# ============================================================================

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
            lines.append(("HSV", f": {h:.0f}°/{s:.0f}%/{v:.0f}%", colors['secondary'], 0.2, 0.5))
    
    return lines


# ============================================================================
# TIPS OVERLAY - User guidance and shortcuts
# ============================================================================

def draw_overlay_tips():
    """Draw tips when no lights are selected or present in the scene."""
    context = bpy.context
    region = context.region
    if not region:
        return
    
    show_tips = getattr(context.scene, 'lumi_show_overlay_tips', True)
    if not show_tips:
        return
    
    font_id = 0
    blf.size(font_id, 12)
    
    colors = get_config_colors(context)
    (info_x, info_y), (tips_x, tips_y) = get_overlay_positions(context, region)
    
    light_col = lumi_get_light_collection(context.scene)
    lights = [obj for obj in light_col.objects if obj.type == 'LIGHT'] if light_col else []
    
    selected_light = None
    if context.selected_objects:
        selected_lights = [obj for obj in context.selected_objects 
                          if obj.type == 'LIGHT' and (not light_col or obj.name in light_col.objects)]
        if selected_lights:
            selected_light = selected_lights[0]
    
    if not lights:
        tips_lines = [
            ("💡 LumiFlow Tips", "", colors['header'], 0.5, 70, 1.3),  
            ("🚀 Create Your First Light:", "", colors['normal'], 0.5, 70, 1.1),   
            ("1. Select or Point mouse at mesh surface", "", colors['secondary'], 0.5, 70, 1.0),  
            ("2. Press", ": Ctrl + Shift + A", colors['secondary'], 0.5, 50, 1.0),
            ("3. Choose light type from menu", "", colors['secondary'], 0.5, 70, 1.0),
        ]
    elif selected_light:
        tips_lines = get_selected_light_tips_template(selected_light, colors)
    else:
        tips_lines = get_general_tips_template(colors)
    
    font_scale, line_spacing = get_text_settings(context)
    draw_text(tips_lines, (tips_x, tips_y), font_scale, line_spacing, is_tips=True)


def get_general_tips_template(colors=None):
    """Get general tips template"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    return [
        ("💡 LumiFlow Tips", "", colors['header'], 0.7, 70, 1.3),  
        ("Select a light to begin", "", colors['normal'], 0.5, 70, 1.1),
        ("Flip", ": Ctrl + Shift + C", colors['secondary'], 0.5, 50, 1.1),
        ("Linking", ": Ctrl + Shift + X", colors['secondary'], 0.5, 50, 1.1),
        ("Solo", ": Ctrl + Shift + D", colors['secondary'], 0.7, 50, 1.1),
        ("Or Add More Ligt", "", colors['normal'], 0.5, 70, 1.1),
        ("Smart Add", ": Ctrl + Shift + A", colors['secondary'], 0.5, 70,1.1),

    ]


def get_selected_light_tips_template(selected_light, colors=None):
    """Get tips template for selected light showing available smart control and positioning modes using centralized system"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    light_type = selected_light.data.type
    
    tips_lines = [
        ("💡 LumiFlow Tips", "", colors['header'], 0.8, 70, 1.3), 
        ("Smart Controls", "", colors['normal'], 0.55, 70, 1.1),
    ]
    
    if light_type == 'POINT':
        tips_lines.extend([
            ("Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Radius", ": Alt + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Temp.", ": Ctrl+Alt + MMB_Drag", colors['secondary'], 0.8, 70, 1.1),
        ])
    elif light_type == 'SUN':
        tips_lines.extend([
            ("Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Angle", ": Alt + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Temp.", ": Ctrl+Alt + MMB_Drag", colors['secondary'], 0.8, 70, 1.1),
        ])
    elif light_type == 'SPOT':
        tips_lines.extend([
            ("Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Angle", ": Alt + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Blend", ": Ctrl+Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Temp.", ": Shift+Alt + MMB_Drag", colors['secondary'], 0.8, 70, 1.1),
        ])
    elif light_type == 'AREA':
        tips_lines.extend([
            ("Distance", ": Ctrl + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Power", ": Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Scale", ": Alt + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Blend", ": Ctrl+Shift + MMB_Drag", colors['secondary'], 0.5, 70, 1.1),
            ("Temp.", ": Shift+Alt + MMB_Drag", colors['secondary'], 0.8, 70, 1.1),
        ])
    
    tips_lines.extend([
        ("Positioning Modes", "", colors['normal'], 0.55, 70, 1.1),
        ("Highlight", ": Ctrl + LMB_Drag", colors['secondary'], 0.5, 70, 1.1),
        ("Normal", ": Shift + LMB_Drag", colors['secondary'], 0.5, 70, 1.1),
        ("Orbit", ": Alt + LMB_Drag", colors['secondary'], 0.5, 70, 1.1),
        ("Target", ": Ctrl+Alt + LMB_Drag", colors['secondary'], 0.5, 70, 1.1),
        ("Free", ": Ctrl+Shift + LMB_Drag", colors['secondary'], 0.5, 70, 1.1),
        ("Move", ": Shift+Alt + LMB_Drag", colors['secondary'], 0.8, 70, 1.1),
        ("Menu", "", colors['normal'], 0.55, 70, 1.1),
        ("Smart Add", ": Ctrl + Shift + A", colors['secondary'], 0.5, 70, 1.1),
        ("Flip", ": Ctrl + Shift + C", colors['secondary'], 0.5, 70, 1.1),
        ("Linking", ": Ctrl + Shift + X", colors['secondary'], 0.5, 70, 1.1),
        ("Solo", ": Ctrl + Shift + D", colors['secondary'], 0.8, 70, 1.1),
        ("Select", "", colors['normal'], 0.55, 70, 1.1),
        ("Cycle", ": D", colors['secondary'], 0.5, 70, 1.1),
        
    ])
    
    return tips_lines


# ============================================================================
# CURSOR OVERLAY - Smart control value display at cursor
# ============================================================================

def draw_overlay_cursor():
    """Draw smart control overlay with current value and controls using OverlayConfig."""
    context = bpy.context
    scene = context.scene
    
    scroll_control_enabled = getattr(scene, 'lumi_scroll_control_enabled', False)
    
    active_positioning_mode = None
    if hasattr(context, 'selected_objects') and context.selected_objects:
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        if selected_lights:
            active_positioning_mode = ModeManager.get_active_positioning_mode(context)
    
    if not scroll_control_enabled and not active_positioning_mode:
        return

    selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
    if not selected_lights:
        return

    region = bpy.context.region
    rv3d = bpy.context.region_data
    if not region or not rv3d:
        return

    font_scale, line_spacing = get_text_settings(context)
    line_spacing *= 0.5
    colors = get_config_colors(context)
    
    scroll_mode = getattr(scene, 'lumi_smart_mode', 'DISTANCE')
    
    mouse_x = getattr(scene, "lumi_smart_mouse_x", region.width // 2)
    mouse_y = getattr(scene, "lumi_smart_mouse_y", region.height // 2)
    
    center = Vector((mouse_x, mouse_y))

    value_label = ""
    
    if selected_lights:
        lamp = selected_lights[0]
        light_type = lamp.data.type
        
        active_positioning_mode = ModeManager.get_active_positioning_mode(context)
        
        if active_positioning_mode:
            positioning_display_name = ModeManager.get_mode_display_name(active_positioning_mode, light_type)
            value_label = positioning_display_name
        else:
            label, value, is_available = ModeManager.get_mode_info(scroll_mode, lamp, context)
            
            if is_available:
                value_label = f"{label}: {value}"
            else:
                value_label = value
    
    overlay_lines = get_smart_overlay(scroll_mode, value_label, colors, context)
    
    estimated_height = len([line for line in overlay_lines if line[0]]) * int(18 * font_scale * line_spacing * 1.2)
    start_y = center.y - estimated_height - 10
    
    start_x = int(center.x - 20)
    
    draw_text(overlay_lines, (start_x, int(start_y)), font_scale=font_scale, line_spacing=line_spacing, alignment='right')


def get_smart_overlay(mode, value_text, colors=None, context=None):
    """Get smart overlay template"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    is_unavailable = value_text.startswith("⌀")
    value_color = colors['error'] if is_unavailable else colors['scroll_value']
    
    base_tips = [
        (value_text, "", value_color, 0.3, 0.5, 1.3),
    ]
    
    if is_unavailable:
        base_tips.append(("Release to continue", "", colors['scroll_text'], 0.2, 0.3))
        return base_tips     
    
    return base_tips
