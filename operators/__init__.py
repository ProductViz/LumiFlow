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
LumiFlow Operators Module
Central hub for all LumiFlow operators organized by functionality.
"""

# # Import modul utama Blender
import bpy

# Import dari submodules yang sudah diorganisir
from .positioning import *  # Semua operator positioning
from .linking import *      # Semua operator linking
from .smart_control import *        # Semua smart operators
from .smart_template import *    # Smart template system

# Import operators yang tetap di level utama
from .menus_ops import (
    LUMI_OT_smart_light_pie_call, LUMI_OT_add_smart_light,
    LUMI_OT_template_menu_call,  # Template menu caller operator
    LUMI_OT_flip_menu_call,  # Flip menu caller operator
    LUMI_OT_set_light_assignment_mode  # Light assignment mode operator
)
from .selection_ops import LUMI_OT_select_light, LUMI_OT_delete_light, LUMI_OT_delete_collection, LUMI_OT_cycle_lights_modal, LUMI_OT_quick_solo_light
from .panels_ops import LUMI_OT_toggle_overlay_info, LUMI_OT_toggle_overlay_tips, LUMI_OT_toggle_addon

# Import submodule __all__ lists
from .positioning import __all__ as positioning_all
from .linking import __all__ as linking_all
from .smart_control import __all__ as smart_all
from .smart_template import __all__ as smart_template_all

# Daftar operator yang tetap di level utama
main_operators = [
    # Pie menu operators
    'LUMI_OT_smart_light_pie_call', 'LUMI_OT_add_smart_light',
    'LUMI_OT_template_menu_call',  # Template menu caller operator
    'LUMI_OT_flip_menu_call',  # Flip menu caller operator
    'LUMI_OT_set_light_assignment_mode',  # Light assignment mode operator
    
    # Utility operators
    'LUMI_OT_select_light', 'LUMI_OT_delete_light', 'LUMI_OT_delete_collection', 'LUMI_OT_cycle_lights_modal', 'LUMI_OT_quick_solo_light',
    'LUMI_OT_toggle_overlay_info', 'LUMI_OT_toggle_overlay_tips', 'LUMI_OT_toggle_addon'
]

# Gabungkan semua exports dari submodules
__all__ = positioning_all + linking_all + smart_all + smart_template_all + main_operators

# Daftar semua operator classes untuk registrasi
operator_classes = []

# Ambil classes dari submodules
# # Import dari modul lokal addon
from . import positioning, linking, smart_control, smart_template
# # Import modul utama Blender
import bpy
import inspect

# Collect positioning classes
for name in positioning_all:
    if hasattr(positioning, name):
        obj = getattr(positioning, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Collect linking classes
for name in linking_all:
    if hasattr(linking, name):
        obj = getattr(linking, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Collect smart classes
for name in smart_all:
    if hasattr(smart_control, name):
        obj = getattr(smart_control, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Collect smart_template classes
for name in smart_template_all:
    if hasattr(smart_template, name):
        obj = getattr(smart_template, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            # # Coba eksekusi kode dengan error handling
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            # # Tangani error jika terjadi
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Add main operators
# # Import dari modul lokal addon
from . import menus_ops, selection_ops, panels_ops
main_modules = [menus_ops, selection_ops, panels_ops]

for module in main_modules:
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if (hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna')) and obj.__module__ == module.__name__:
            operator_classes.append(obj)

# # Fungsi untuk mendaftarkan class ke Blender
def register():
    """Daftarkan semua kelas operator"""
    for cls in operator_classes:
        # # Coba eksekusi kode dengan error handling
        try:
            # # Daftarkan class ke sistem Blender
            bpy.utils.register_class(cls)
        # # Tangani error jika terjadi
        except Exception:
            # Gagal register, lanjut saja
            pass

# # Fungsi untuk membatalkan pendaftaran class
def unregister():
    """Hapus registrasi semua kelas operator"""
    for cls in reversed(operator_classes):
        # # Coba eksekusi kode dengan error handling
        try:
            # # Batalkan pendaftaran class
            bpy.utils.unregister_class(cls)
        # # Tangani error jika terjadi
        except Exception:
            # Gagal unregister, lanjut saja
            pass

