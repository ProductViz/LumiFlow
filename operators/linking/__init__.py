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
LumiFlow Light Linking Operations Module
Contains all operators and data structures for light linking management.

OPTIMIZATION NOTES:
- Light groups are now READ-ONLY (managed through collections)
- Some operators are DEPRECATED but kept for compatibility
- Focus shifted to linking functionality rather than group management
"""

# Import semua linking operators dan properties
from .linking_ops import (
    # Constants
    DEFAULT_GROUP_NAME,
    
    # Data structures
    LUMI_ObjectGroupLinkStatus,
    LUMI_ObjectItem, 
    LUMI_ObjectGroup, 
    LUMI_UL_object_groups, 
    LUMI_UL_objects_in_group,
    LUMI_LightItem, 
    LUMI_LightGroup, 
    LUMI_UL_light_groups, 
    LUMI_UL_lights_in_group,
    LUMI_UnGroupedLightItem,
    
    # Object group management operators (ACTIVE)
    LUMI_OT_add_group, 
    LUMI_OT_remove_group,
    LUMI_OT_add_object_to_group, 
    LUMI_OT_remove_object_from_group, 
    LUMI_OT_select_object_from_group,
    LUMI_OT_sync_object_selection,
    LUMI_OT_toggle_select_all_objects_in_group,
    
    # Light group management operators (DEPRECATED - read-only)
    LUMI_OT_add_light_group, 
    LUMI_OT_remove_light_group,
    LUMI_OT_add_light_to_group, 
    LUMI_OT_remove_light_from_group, 
    LUMI_OT_select_light_from_group,
    LUMI_OT_select_un_grouped_light,
    LUMI_OT_toggle_select_all_lights_in_group,
    
    # Linking operators (ACTIVE)
    LUMI_OT_update_light_linking, 
    LUMI_OT_clear_light_linking,
    LUMI_OT_quick_link_to_target,
    
    # Helper functions
    object_group_index_update,
    sync_marked_with_links,
    # Handler functions (note: some removed due to optimization)
    lumi_light_groups_update_handler,
    depsgraph_update_default_group
)

# Export semua linking components dengan dokumentasi optimasi
__all__ = [
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
    
    # Light group management operators (DEPRECATED - use collections)
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
    'lumi_light_groups_update_handler',
    'depsgraph_update_default_group'
]



