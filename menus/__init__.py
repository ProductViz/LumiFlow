# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Menus Module
Contains all menu classes for the LumiFlow Blender addon UI.
"""

import bpy
from . import pie_menus

from .pie_menus import (
    LUMI_MT_add_light_pie,
    LUMI_MT_smart_template_light_pie,
    LUMI_MT_template_menu,
    LUMI_MT_template_favorites,
    # Template category menus
    LUMI_MT_template_studio_commercial,
    LUMI_MT_template_dramatic_cinematic,
    LUMI_MT_template_environment_realistic,
    LUMI_MT_template_utilities_single,
    # Flip operations menus
    LUMIFLOW_MT_flip_to_camera,
    LUMIFLOW_MT_light_flip_menu,
)

menu_classes = [
    LUMI_MT_add_light_pie,
    LUMI_MT_smart_template_light_pie,
    LUMI_MT_template_menu,
    LUMI_MT_template_favorites,
    # Template category menus
    LUMI_MT_template_studio_commercial,
    LUMI_MT_template_dramatic_cinematic,
    LUMI_MT_template_environment_realistic,
    LUMI_MT_template_utilities_single,
    # Flip operations menus
    LUMIFLOW_MT_flip_to_camera,
    LUMIFLOW_MT_light_flip_menu,
]

# Export for backward compatibility
__all__ = [
    'LUMI_MT_add_light_pie',
    'LUMI_MT_smart_template_light_pie',
    'LUMI_MT_template_menu',
    'LUMI_MT_template_favorites',
    # Template category menus
    'LUMI_MT_template_studio_commercial',
    'LUMI_MT_template_dramatic_cinematic',
    'LUMI_MT_template_environment_realistic',
    'LUMI_MT_template_utilities_single',
    # Flip operations menus
    'LUMIFLOW_MT_flip_to_camera',
    'LUMIFLOW_MT_light_flip_menu',
]

def register():
    for cls in menu_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(menu_classes):
        bpy.utils.unregister_class(cls)

