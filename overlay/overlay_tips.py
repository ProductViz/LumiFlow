"""
Tips Overlay Module
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
    
    from .utils import draw_text
    draw_text(tips_lines, (tips_x, tips_y), font_scale, line_spacing, is_tips=True)

def get_general_tips_template(colors=None):
    """Get general tips template"""
    if colors is None:
        colors = OverlayConfig.get_all_colors()
    
    return [
        ("💡 LumiFlow Tips", "", colors['header'], 0.7, 70, 1.3),  
        ("Select a light to begin", "", colors['normal'], 0.5, 70, 1.1),
        ("Flip", ": Ctrl + Shift + C", colors['secondary'], 0.5, 30, 1.1),
        ("Linking", ": Ctrl + Shift + X", colors['secondary'], 0.5, 45, 1.1),
        ("Solo", ": Ctrl + Shift + D", colors['secondary'], 0.7, 30, 1.1),
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



