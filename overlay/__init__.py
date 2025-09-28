# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
"""
LumiFlow Draw Module
Modular drawing system for the LumiFlow Blender addon.
"""

# Import semua fungsi dari modul-modul baru
from .overlay_light import (
    lumi_draw_light_lines,
    render_batches
)

from .overlay_info import (
    draw_overlay_info
)

from .overlay_tips import (
    draw_overlay_tips
)

from .overlay_cursor import (
    draw_overlay_cursor,
    get_smart_overlay
)

from ..utils.light import (
    lumi_get_selected_lights,
    lumi_calculate_light_target_position
)

from .overlay_mesh import (
    _draw_scene_object_strokes_if_no_lights
)

from .overlay_handlers import (
    lumi_enable_draw_handler,
    lumi_disable_draw_handler,
    lumi_enable_overlay_draw_handler,
    lumi_disable_overlay_draw_handler,
    lumi_enable_stroke_overlay_handler,
    lumi_disable_stroke_overlay_handler,
    lumi_enable_tips_overlay_handler,
    lumi_disable_tips_overlay_handler,
    lumi_enable_cursor_overlay_handler,
    lumi_disable_cursor_overlay_handler,
    lumi_scene_update_handler,
    debug_overlay_status
)

# Export semua fungsi yang diperlukan
__all__ = [
    # Light visualization functions
    'lumi_draw_light_lines',
    'render_batches',
    
    # Info display functions
    'draw_overlay_info',
    
    # Tips functions
    'draw_overlay_tips',
    
    # Scroll functions
    'draw_overlay_cursor',
    'get_smart_overlay',
    
    # Light selection and target functions
    'lumi_get_selected_lights',
    'lumi_calculate_light_target_position',
    
    # Mesh functions
    '_draw_scene_object_strokes_if_no_lights',
    
    # Handler functions
    'lumi_enable_draw_handler',
    'lumi_disable_draw_handler',
    'lumi_enable_overlay_draw_handler',
    'lumi_disable_overlay_draw_handler',
    'lumi_enable_stroke_overlay_handler',
    'lumi_disable_stroke_overlay_handler',
    'lumi_enable_tips_overlay_handler',
    'lumi_disable_tips_overlay_handler',
    'lumi_enable_cursor_overlay_handler',
    'lumi_disable_cursor_overlay_handler',
    'lumi_scene_update_handler',
    'debug_overlay_status'
]


