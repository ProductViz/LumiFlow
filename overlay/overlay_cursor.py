"""
Cursor Overlay Module
Contains cursor and mouse interaction functions and smart overlay template.
"""

import bpy
import math
import blf
from mathutils import Vector
from bpy_extras import view3d_utils

from .utils import get_text_settings, get_config_colors, get_overlay_positions, draw_text
from ..utils.light import lumi_get_light_pivot
from ..utils.mode_manager import ModeManager
from .config import OverlayConfig


def get_smart_overlay(mode, value_text, colors=None, context=None):
    """Get smart overlay template"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    is_unavailable = value_text.startswith("âŒ")
    value_color = colors['error'] if is_unavailable else colors['scroll_value']
    
    base_tips = [
        (value_text, "", value_color, 0.3, 0.5, 1.3),  # spacing_before=0.3, spacing_after=0.5, font_scale=1.3
    ]
    
    if is_unavailable:
        base_tips.append(("Release to continue", "", colors['scroll_text'], 0.2, 0.3))  # small spacing
        return base_tips     
    
    #base_tips += [
        #("â†   -   Drag   +   â†’", "", colors['scroll_text'], 0.01),
    #]
    return base_tips


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
    start_y = center.y - estimated_height - 10  # Position lower (more negative = lower)
    
    start_x = int(center.x - 20)
    
    draw_text(overlay_lines, (start_x, int(start_y)), font_scale=font_scale, line_spacing=line_spacing, alignment='right')


