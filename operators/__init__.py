
import bpy
from .positioning import *
from .linking_ops import *
from .smart_ops import *
from .smart_template import *

from .menus_ops import (
    LUMI_OT_smart_light_pie_call, LUMI_OT_add_smart_light,
    LUMI_OT_template_menu_call,  # Template menu caller operator
    LUMI_OT_flip_menu_call,  # Flip menu caller operator
    LUMI_OT_set_light_assignment_mode  # Light assignment mode operator
)
from .selection_ops import LUMI_OT_select_light, LUMI_OT_delete_light, LUMI_OT_delete_collection, LUMI_OT_cycle_lights_modal, LUMI_OT_quick_solo_light
from .panels_ops import LUMI_OT_toggle_overlay_info, LUMI_OT_toggle_overlay_tips, LUMI_OT_toggle_addon

from .positioning import __all__ as positioning_all
linking_all = [
    # Constants
    'DEFAULT_GROUP_NAME',
    
    # Data structures
    'LUMI_ObjectGroupLinkStatus',
    'LUMI_ObjectItem', 
    'LUMI_ObjectGroup', 
    'LUMI_UL_object_groups', 
    'LUMI_UL_objects_in_group',
    'LUMI_LightItem', 
    'LUMI_LightGroup', 
    'LUMI_UL_light_groups', 
    'LUMI_UL_lights_in_group',
    'LUMI_UnGroupedLightItem',
    
    # Object group management operators (ACTIVE)
    'LUMI_OT_add_group', 
    'LUMI_OT_remove_group',
    'LUMI_OT_add_object_to_group', 
    'LUMI_OT_remove_object_from_group', 
    'LUMI_OT_select_object_from_group',
    'LUMI_OT_sync_object_selection',
    'LUMI_OT_toggle_select_all_objects_in_group',
    
    # Light group management operators (DEPRECATED - read-only)
    'LUMI_OT_add_light_group', 
    'LUMI_OT_remove_light_group',
    'LUMI_OT_add_light_to_group', 
    'LUMI_OT_remove_light_from_group', 
    'LUMI_OT_select_light_from_group',
    'LUMI_OT_select_un_grouped_light',
    'LUMI_OT_toggle_select_all_lights_in_group',
    
    # Linking operators (ACTIVE)
    'LUMI_OT_update_light_linking', 
    'LUMI_OT_clear_light_linking',
    'LUMI_OT_quick_link_to_target',
    
    # Helper functions
    'object_group_index_update',
    'sync_marked_with_links',
    # Handler functions (note: some removed due to optimization)
    'lumi_light_groups_update_handler',
    'depsgraph_update_default_group'
]
from .smart_ops import __all__ as smart_all
from .smart_template import __all__ as smart_template_all

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

__all__ = list(positioning_all) + linking_all + list(smart_all) + list(smart_template_all) + main_operators

operator_classes = []

from . import positioning, smart_ops, smart_template
from . import linking_ops
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
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Collect linking classes
for name in linking_all:
    if hasattr(linking_ops, name):
        obj = getattr(linking_ops, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

# Collect smart classes
for name in smart_all:
    if hasattr(smart_ops, name):
        obj = getattr(smart_ops, name)
        if inspect.isclass(obj):
            # Check registration criteria
            should_register = False
            
            # Check for bl_idname or bl_rna (operators, panels)
            if hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna'):
                should_register = True
            
            # Check for UIList subclass
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
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
            try:
                if issubclass(obj, bpy.types.UIList):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            # Check for PropertyGroup subclass  
            try:
                if issubclass(obj, bpy.types.PropertyGroup):
                    should_register = True
            except (TypeError, AttributeError):
                pass
                
            if should_register:
                operator_classes.append(obj)

from . import menus_ops, selection_ops, panels_ops
main_modules = [menus_ops, selection_ops, panels_ops]

for module in main_modules:
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if (hasattr(obj, 'bl_idname') or hasattr(obj, 'bl_rna')) and obj.__module__ == module.__name__:
            operator_classes.append(obj)

def register():
    """Register all operator classes"""
    for cls in operator_classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass

def unregister():
    """Unregister all operator classes"""
    for cls in reversed(operator_classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
