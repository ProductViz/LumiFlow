"""
Menus Module
Contains all menu classes for the LumiFlow Blender addon UI.
"""

import bpy
# Import dari modul lokal addon
from . import pie_menus

# Import semua menu untuk external access
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

# Explicit list of all menu classes
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

# Export untuk backward compatibility
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

# # Fungsi untuk mendaftarkan class ke Blender
def register():
    for cls in menu_classes:
        # # Daftarkan class ke sistem Blender
        bpy.utils.register_class(cls)

# # Fungsi untuk membatalkan pendaftaran class
def unregister():
    for cls in reversed(menu_classes):
        # # Batalkan pendaftaran class
        bpy.utils.unregister_class(cls)

