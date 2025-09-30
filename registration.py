# SPDX-License-Identifier: GPL-3.0-or-later
#
# LumiFlow - Smart lighting tools for Blender
# Copyright (C) 2024 LumiFlow Developer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
LumiFlow Addon Registration Module
Handles registration and unregistration of all classes, properties, handlers, and keymaps for the LumiFlow Blender addon.
"""
import bpy
from bpy.props import CollectionProperty, IntProperty, StringProperty

# Import state and utility functions
from .core.state import get_state
# PropertyGroup for camera-light assignments
class LumiCameraLightAssignment(bpy.types.PropertyGroup):
    camera_name = bpy.props.StringProperty(
        name="Camera Name", 
        description="Name of the camera",
        default=""
    )
    light_names = bpy.props.StringProperty(
        name="Light Names", 
        description="Comma-separated list of light names assigned to this camera",
        default=""
    )

# PropertyGroup for scrollable light list
class LumiLightItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()

# Import all operators from operators module
from .operators import *
from .utils.properties import LightControlProperties, LightPositioningProperties, ProfessionalLightingProperties

# Import explicit template operators
from .operators.smart_template.template_ops import (
    LUMI_OT_toggle_template_favorite,
    LUMI_OT_set_template_category,
    LUMI_OT_save_lighting_template,
    LUMI_OT_apply_template_direct,
    LUMI_OT_apply_template_default,
    LUMI_OT_apply_template,
    LUMI_OT_show_all_templates
)

# Import main panel class with specific import to avoid issues
from .ui.main_panel import (
    LUMI_PT_light_control,
)

# Template settings panel classes have been deleted

# Template browser classes have been deleted

# Import menu classes from pie_menus
from .ui.pie_menus import (
    LUMI_MT_add_light_pie,
    LUMI_MT_smart_template_light_pie,
    LUMI_MT_template_menu,
    LUMI_MT_template_favorites,
)

# Import menu, draw, and utils modules
from .ui.pie_menus import *
from .utils import *
from .ui.overlay import lumi_scene_update_handler

# Import free positioning operators explicitly
from .operators.positioning.free_ops import (
    LUMI_OT_free_positioning
)

# Explicit import for PropertyGroup classes and optimized operators
from .operators.linking_ops import (
    LUMI_ObjectGroupLinkStatus,
    LUMI_ObjectGroup,
    LUMI_LightGroup,
    LUMI_ObjectItem,
    LUMI_LightItem,
    LUMI_UnGroupedLightItem,
    LUMI_UL_object_groups,
    LUMI_UL_objects_in_group,
    LUMI_UL_light_groups,
    LUMI_UL_lights_in_group,
    LUMI_OT_quick_link_to_target,
    # DEPRECATED operators (now disabled for read-only light groups)
    LUMI_OT_add_light_group,
    LUMI_OT_remove_light_group,
    LUMI_OT_add_light_to_group,
    LUMI_OT_remove_light_from_group,
    LUMI_OT_select_un_grouped_light,
    LUMI_MT_group_actions,
    LUMI_OT_select_light_from_group,
    LUMI_OT_toggle_select_all_lights_in_group,
    # Active operators (still functional)
    LUMI_OT_add_group,
    LUMI_OT_remove_group,
    LUMI_OT_add_object_to_group,
    LUMI_OT_remove_object_from_group,
    LUMI_OT_sync_object_selection,
    LUMI_OT_select_object_from_group,
    LUMI_OT_toggle_select_all_objects_in_group,
    LUMI_OT_update_light_linking,
    LUMI_OT_clear_light_linking,
    # Helper functions
    object_group_index_update,
    lumi_light_groups_update_handler,
    depsgraph_update_default_group,
    cleanup_dynamic_menu_classes
)

# Import smart control operators
from .operators.smart_ops import (
    LUMI_OT_smart_control,
)
from .preferences import LumiFlowAddonPreferences
from .core.state import get_state

# Template error handling system import
from .operators.smart_template import (
    initialize_error_handling,
    cleanup_error_handling
)



# Import accordion update functions from utils.properties
# Update functions for deleted panels removed
from .utils.properties import (
    lumi_enabled_update,
    lumi_light_linking_expanded_update,
    lumi_color_controls_expanded_update,
    lumi_light_linking_expanded_accordion_update,
    lumi_scroll_settings_expanded_update
)

# Import new Light Mixer classes
# light_mixer file has been deleted

# Collect all classes from automatically imported modules
import inspect
# Import from local addon modules
from . import operators, utils, ui

def get_classes():
    """Collect all classes from modules dynamically"""
    classes_list = []
    
    # Get classes from operators module
    if hasattr(operators, '__all__'):
        for name in operators.__all__:
            obj = getattr(operators, name)
            if inspect.isclass(obj):
                classes_list.append(obj)
    
    # Get classes from ui module (pie_menus, main_panel)
    if hasattr(ui, '__all__'):
        for name in ui.__all__:
            obj = getattr(ui, name)
            if inspect.isclass(obj):
                classes_list.append(obj)
    
    # Get classes from utils module
    if hasattr(utils, '__all__'):
        for name in utils.__all__:
            obj = getattr(utils, name)
            if inspect.isclass(obj):
                classes_list.append(obj)
    
    return tuple(classes_list)

# Light mixer classes have been deleted
light_mixer_classes = []

# Add UIList classes from linking module
# Light Linking UI classes (optimized for read-only light groups)
linking_ui_classes = [
    # PropertyGroups
    LUMI_ObjectGroupLinkStatus,
    LUMI_ObjectGroup,
    LUMI_LightGroup,
    LUMI_ObjectItem,
    LUMI_LightItem,
    LUMI_UnGroupedLightItem,
    # UI Lists
    LUMI_UL_object_groups,
    LUMI_UL_objects_in_group,
    LUMI_UL_light_groups,
    LUMI_UL_lights_in_group,
    # Active operators (fully functional)
    LUMI_OT_add_group,
    LUMI_OT_remove_group,
    LUMI_OT_add_object_to_group,
    LUMI_OT_remove_object_from_group,
    LUMI_OT_sync_object_selection,
    LUMI_OT_select_object_from_group,
    LUMI_OT_toggle_select_all_objects_in_group,
    LUMI_OT_update_light_linking,
    LUMI_MT_group_actions,
    LUMI_OT_clear_light_linking,
    LUMI_OT_quick_link_to_target,
    # DEPRECATED operators (kept for compatibility, show info messages)
    LUMI_OT_add_light_group,
    LUMI_OT_remove_light_group,
    LUMI_OT_add_light_to_group,
    LUMI_OT_remove_light_from_group,
    LUMI_OT_select_un_grouped_light,
    LUMI_OT_select_light_from_group,
    LUMI_OT_toggle_select_all_lights_in_group,
]

# Panel classes from explicit import
panel_classes = [
    LUMI_PT_light_control,
]

# Template Settings classes have been deleted
# Template browser classes have been deleted


# AI-Powered Template Recommendation classes  
from .operators.menus_ops import (
    LUMI_OT_studio_commercial_menu,
    LUMI_OT_dramatic_cinematic_menu,
    LUMI_OT_environment_realistic_menu,
    LUMI_OT_utilities_single_lights_menu,
    LUMI_OT_template_category_browser,
    LUMI_OT_smart_template_light_pie_call,
    LUMI_OT_template_favorites,
    LUMI_OT_background_light_setup
)
# Pie Menu classes
pie_menu_classes = [
    LUMI_MT_add_light_pie,
    LUMI_MT_smart_template_light_pie,
    LUMI_MT_template_menu,
    LUMI_MT_template_favorites,
]


classes = get_classes() + tuple(linking_ui_classes) + tuple(panel_classes) + tuple(pie_menu_classes)
addon_keymaps = []

def register_properties() -> None:
    """Enhanced property registration with proper persistence"""
    # Register PropertyGroup for camera-light assignments
    try:
        bpy.utils.register_class(LumiCameraLightAssignment)
    except Exception:
        pass
    # Register PropertyGroup for scrollable light list
    try:
        bpy.utils.register_class(LumiLightItem)
    except Exception:
        pass
    # Register PropertyGroup for light positioning
    try:
        bpy.utils.register_class(LightPositioningProperties)
    except Exception:
        pass
    # Register PropertyGroup for professional lighting
    try:
        bpy.utils.register_class(ProfessionalLightingProperties)
    except Exception:
        pass
    props = [
        ("lumi_toggle_highlight", bpy.props.BoolProperty(name="Toggle Highlight", default=False, description="Aktifkan mode highlight pada lampu")),
        ("light_target", bpy.props.PointerProperty(name="Target", type=bpy.types.Object)),
        ("light_distance", bpy.props.FloatProperty(name="Distance", default=2.0, min=0.1, max=100.0)),
        ("align_to_face_active", bpy.props.BoolProperty(name="Align to Face Active", default=False)),
        ("lumi_enabled", bpy.props.BoolProperty(
            name="Enable LumiFlow", 
            description="Enable/disable all LumiFlow features", 
            default=False, 
            update=lumi_enabled_update
        )),
        ("lumi_scale_axis", bpy.props.EnumProperty(name="Scale Axis", description="Choose axis for light scaling",
         items=[('XY', "XY (Uniform)", "Uniform X and Y scaling"), ('X', "X", "X axis only"), ('Y', "Y", "Y axis only")], default='XY')),
        ("lumi_show_help", bpy.props.BoolProperty(name="Show Help", description="Show/hide help panel", default=False)),
        ("lumi_temp_hit_obj", bpy.props.PointerProperty(name="Temp Hit Object", type=bpy.types.Object)),
        ("lumi_temp_hit_location", bpy.props.FloatVectorProperty(name="Temp Hit Location", size=3)),
        ("lumi_temp_hit_normal", bpy.props.FloatVectorProperty(name="Temp Hit Normal", size=3)),
        ("lumi_temp_hit_index", bpy.props.IntProperty(name="Temp Hit Index")),
        ("lumi_temp_selected_obj", bpy.props.PointerProperty(name="Temp Selected Object", type=bpy.types.Object)),
        ("lumi_temp_selected_location", bpy.props.FloatVectorProperty(name="Temp Selected Location", size=3)),
        ("lumi_temp_selected_normal", bpy.props.FloatVectorProperty(name="Temp Selected Normal", size=3)),
        ("lumi_temp_selected_index", bpy.props.IntProperty(name="Temp Selected Index")),
        ("lumi_scroll_settings_expanded", bpy.props.BoolProperty(name="Show Scroll Settings", default=False, description="Show/hide scroll settings panel", update=lumi_scroll_settings_expanded_update)),
        ("lumi_light_linking_expanded", bpy.props.BoolProperty(name="Show Light Linking Manager", default=False, description="Show/hide light linking manager panel", update=lumi_light_linking_expanded_accordion_update)),
        ("lumi_color_controls_expanded", bpy.props.BoolProperty(name="Show Color Controls", default=False, description="Show/hide color controls panel", update=lumi_color_controls_expanded_update)),
        ("lumi_color_enabled", bpy.props.BoolProperty(name="Color Control Enabled", default=False, description="Enable color and temperature controls", update=lumi_color_enabled_update)),
        ("lumi_color_temperature", bpy.props.IntProperty(name="Color Temperature", default=5500, min=1000, max=20000, description="Light color temperature in Kelvin")),
        ("lumi_smart_enabled", bpy.props.BoolProperty(name="Smart Controls Enabled", default=False, description="Enable smart control settings")),
        ("lumi_status_distance_active", bpy.props.BoolProperty(default=False)),
        ("lumi_status_power_active", bpy.props.BoolProperty(default=False)),        
        ("lumi_status_scale_active", bpy.props.BoolProperty(default=False)),      
        ("lumi_status_temperature_active", bpy.props.BoolProperty(default=False)),
        ("lumi_status_hue_active", bpy.props.BoolProperty(default=False)),
        ("lumi_status_saturation_active", bpy.props.BoolProperty(default=False)),
        ("lumi_smart_template_expanded", bpy.props.BoolProperty(name="Show Smart Template Tips", default=True)),
        ("light_target_face_location", bpy.props.FloatVectorProperty(name="Target Face Location", size=3)),
        ("lumi_overlay_info_enabled", bpy.props.BoolProperty(name="Overlay Info Enabled", default=True, description="Show/hide LumiFlow overlay info")),
        ("lumi_status_angle_active", bpy.props.BoolProperty(default=False)),        
        ("lumi_enable_pending", bpy.props.BoolProperty(default=False)),
        ("lumi_scroll_control_enabled", bpy.props.BoolProperty(name="Smart Control Enabled", default=False)),
        ("lumi_show_overlay_info", bpy.props.BoolProperty(name="Show Overlay Info", description="Show/hide the detailed light info on screen", default=True)),
        ("lumi_show_overlay_tips", bpy.props.BoolProperty(name="Show Overlay Tips", description="Show/hide the tips on screen", default=True)),
        ("lumi_smart_mode", bpy.props.StringProperty(name="Smart Mode", default="DISTANCE")),
        ("lumi_smart_mouse_x", bpy.props.IntProperty(name="Smart Mouse X", default=0)),
        ("lumi_smart_mouse_y", bpy.props.IntProperty(name="Smart Mouse Y", default=0)),
        ("lumi_show_objects_in_group", bpy.props.BoolProperty(default=True)),
        ("lumi_show_lights_in_group", bpy.props.BoolProperty(default=False)),
        ("lumi_object_group_link_status", bpy.props.CollectionProperty(type=LUMI_ObjectGroupLinkStatus)),      
        ("lumi_template_view_mode", bpy.props.EnumProperty(
            name="View Mode",
            description="Template display mode",
            items=[
                ('GRID', "Grid", "Grid view with icons", 'MESH_GRID', 0),
                ('LIST', "List", "List view with details", 'ALIGN_JUSTIFY', 1)
            ],
            default='GRID'
        )),        
        ("lumi_template_favorites", bpy.props.StringProperty(
            name="Favorites",
            description="Comma-separated favorite template IDs",
            default=""
        )),
        ("lumi_template_auto_scale", bpy.props.BoolProperty(
            name="Auto Scale",
            description="Automatically scale templates to subject size",
            default=True
        )),
        ("lumi_template_camera_relative", bpy.props.BoolProperty(
            name="Camera Relative",
            description="Position templates relative to camera",
            default=True
        )),
        ("lumi_template_intensity_multiplier", bpy.props.FloatProperty(
            name="Intensity",
            description="Global intensity multiplier for templates",
            default=1.0,
            min=0.1,
            max=10.0,
            step=10,
            precision=2
        )),
        ("lumi_template_size_multiplier", bpy.props.FloatProperty(
            name="Size Multiplier",
            description="Global size multiplier for area lights",
            default=1.0,
            min=0.1,
            max=5.0,
            step=10,
            precision=2
        )),
        ("lumi_template_manual_distance", bpy.props.FloatProperty(
            name="Manual Distance",
            description="Override automatic distance calculation",
            default=0.0,
            min=0.0,
            max=50.0,
            step=10,
            precision=2
        )),
        ("lumi_template_preserve_existing", bpy.props.BoolProperty(
            name="Preserve Existing",
            description="Keep existing lights when applying template",
            default=False
        )),
        ("lumi_template_use_material_adaptation", bpy.props.BoolProperty(
            name="Material Adaptation",
            description="Adjust lighting based on material analysis",
            default=True
        )),
        ("lumi_object_groups_index", bpy.props.IntProperty(default=0, update=object_group_index_update)),
        ("lumi_light_index", bpy.props.IntProperty(
            name="Light Index",
            description="Selected light index in template_list",
            default=0,
            min=0
        )),
        
        ("lumi_object_groups", bpy.props.CollectionProperty(type=LUMI_ObjectGroup)),
        ("lumi_light_groups", bpy.props.CollectionProperty(type=LUMI_LightGroup)),
        ("lumi_light_groups_index", bpy.props.IntProperty(default=0)),
        ("lumi_light_linking_index", bpy.props.IntProperty(default=0)),              
        ("lumi_show_light_linking", bpy.props.BoolProperty(default=True)),
        ("lumi_objects_in_group_index", bpy.props.IntProperty(default=0)),
        ("lumi_lights_in_group_index", bpy.props.IntProperty(default=0)), 
        ("lumi_un_grouped_lights", bpy.props.CollectionProperty(type=LUMI_UnGroupedLightItem)),
        ("lumi_camera_light_assignments", bpy.props.CollectionProperty(type=LumiCameraLightAssignment)),
        ("lumi_light_assignment_mode", bpy.props.EnumProperty(
            name="Light Assignment Mode",
            description="Control how new lights are assigned to cameras",
            items=[
                ('SCENE', "Scene", "New lights are visible to all cameras (global)", 'SCENE_DATA', 0),
                ('CAMERA', "Camera", "New lights are only visible to the active camera", 'CAMERA_DATA', 1)
            ],
            default='SCENE'
        )),
        ("lumi_director_active", bpy.props.BoolProperty(name="Key Light Director Active", default=False, description="Key Light Director modal is active")),
        ("lumi_director_target_object", bpy.props.PointerProperty(name="Director Target Object", type=bpy.types.Object)),
        ("lumi_director_target_location", bpy.props.FloatVectorProperty(name="Director Target Location", size=3)),            
        ("lumi_light_index", IntProperty(name="Lumi Light Index", default=0)),
    ]    
    for prop_name, prop_def in props:
        setattr(bpy.types.Scene, prop_name, prop_def)

def unregister_properties() -> None:
    """Remove all LumiFlow scene properties"""
    # Unregister PropertyGroup classes
    try:
        bpy.utils.unregister_class(LumiCameraLightAssignment)
    except Exception:
        pass
    try:
        bpy.utils.unregister_class(LumiLightItem)
    except Exception:
        pass
    try:
        bpy.utils.unregister_class(LightPositioningProperties)
    except Exception:
        pass
    try:
        bpy.utils.unregister_class(ProfessionalLightingProperties)
    except Exception:
        pass
    
    prop_names = [
        "lumi_toggle_highlight", "light_target", "light_distance", "align_to_face_active", "lumi_enabled",
        "lumi_scale_axis", "lumi_show_help", "lumi_temp_hit_obj",
        "lumi_temp_hit_location", "lumi_temp_hit_normal", "lumi_temp_hit_index",
        "lumi_temp_selected_obj", "lumi_temp_selected_location", "lumi_temp_selected_normal", "lumi_temp_selected_index",
        "lumi_distance_step", "lumi_scale_step", "lumi_power_sensitivity", "lumi_scroll_settings_expanded", "lumi_light_linking_expanded",
        "lumi_color_enabled", "lumi_color_temperature", "lumi_color_step", "lumi_smart_template_expanded", 
        "light_target_face_location", "lumi_overlay_info_enabled", "lumi_status_angle_active",
        "lumi_enable_pending", "lumi_scroll_control_enabled", "lumi_smart_mode",
        "lumi_status_distance_active", "lumi_status_power_active", "lumi_status_scale_active", 
        "lumi_status_temperature_active", "lumi_status_hue_active", "lumi_status_saturation_active",
        "lumi_show_overlay_info", "lumi_show_overlay_tips", "lumi_show_keymap_icons", "lumi_icon_size", "lumi_smart_mouse_x", "lumi_smart_mouse_y",
        "lumi_light_index",
        # Light Linking Properties
        "lumi_show_objects_in_group", "lumi_show_lights_in_group",
        "lumi_object_group_link_status",
        "lumi_object_groups_index",
        "lumi_object_groups", 
        "lumi_light_groups", "lumi_light_groups_index",
        "lumi_light_linking_index", 
        "lumi_show_light_linking", "lumi_objects_in_group_index", "lumi_lights_in_group_index",
        "lumi_un_grouped_lights",
        "lumi_camera_light_assignments",
        # Key Light Director Properties
        "lumi_director_active", "lumi_director_target_object", "lumi_director_target_location",
        # Light Assignment Mode Property
        "lumi_light_assignment_mode",
        # Template Browser Properties
        "lumi_template_view_mode", "lumi_template_favorites", "lumi_template_auto_scale",
        "lumi_template_camera_relative", "lumi_template_intensity_multiplier", "lumi_template_size_multiplier",
        "lumi_template_manual_distance", "lumi_template_preserve_existing", "lumi_template_use_material_adaptation",
        # Template Settings Properties (legacy - for backward compatibility)
        "lumi_template_auto_position", "lumi_template_default_scale", "lumi_template_default_intensity",
        "lumi_template_collection", "lumi_template_auto_organize", "lumi_template_auto_save",
        "lumi_template_validate", "lumi_template_backup", "lumi_template_optimize", "lumi_template_category",
        # Manual Properties (registered outside register_properties function)
        "lumi_shadow_density", "lumi_negative_fill", "lumi_use_material_shadows", "lumi_artistic_override",
        "lumi_haze_density", "lumi_fog_absorption", "lumi_scattering", "lumi_godrays_strength",
        # Additional Manual Properties
        "lumi_professional_props", "lumi_light_control_props", "light_props",
        "lumi_harmony_type", "lumi_base_hue", "lumi_saturation", "lumi_mood_type",
        "lumi_time_of_day", "lumi_penumbra_factor", "lumi_contact_shadow"
    ]
    for prop in prop_names:
        if hasattr(bpy.types.Scene, prop):
            try:
                delattr(bpy.types.Scene, prop)
            except Exception:
                pass

def register_keymaps() -> None:
    """Register all keymaps for LumiFlow"""
    try:
        wm = bpy.context.window_manager
        if not wm:
            return  # Window manager not available
            
        kc = wm.keyconfigs.addon
        if not kc:
            return  # Addon keyconfig not available
            
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        shortcuts = [
           
            ('lumi.template_menu_call', 'A', 'PRESS', True, True, False),
            ('lumi.flip_menu_call', 'C', 'PRESS', True, True, False),
            ('lumi.quick_link_to_target', 'X', 'PRESS', True, True, False),
            ('lumi.toggle_addon', 'D', 'PRESS', True, True, True),
            ('lumi.cycle_lights_modal', 'D', 'PRESS', False, False, False),
            ('lumi.quick_solo_light', 'D', 'PRESS', True, True, False),
        ]
        for op, key, action, ctrl, shift, alt in shortcuts:
            kmi = km.keymap_items.new(op, key, action, ctrl=ctrl, shift=shift, alt=alt)
            addon_keymaps.append((km, kmi))

        # Direct positioning mode shortcuts - replace pie menu with direct operator calls
        # Highlight Positioning: Ctrl + LMB drag
        kmi = km.keymap_items.new('lumi.highlight_positioning', 'LEFTMOUSE', 'PRESS', ctrl=True, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        
        # Normal Positioning: Shift + LMB drag
        kmi = km.keymap_items.new('lumi.normal_positioning', 'LEFTMOUSE', 'PRESS', ctrl=False, shift=True, alt=False)
        addon_keymaps.append((km, kmi))
        
        # Orbit Positioning: Alt + LMB drag
        kmi = km.keymap_items.new('lumi.orbit_positioning', 'LEFTMOUSE', 'PRESS', ctrl=False, shift=False, alt=True)
        addon_keymaps.append((km, kmi))
        
        # Target Positioning: Ctrl+Alt + LMB drag
        kmi = km.keymap_items.new('lumi.target_positioning', 'LEFTMOUSE', 'PRESS', ctrl=True, shift=False, alt=True)
        addon_keymaps.append((km, kmi))
        
        # Free Positioning: Ctrl+Shift + LMB drag
        kmi = km.keymap_items.new('lumi.free_positioning', 'LEFTMOUSE', 'PRESS', ctrl=True, shift=True, alt=False)
        addon_keymaps.append((km, kmi))
        
        # Move Positioning: Shift+Alt + LMB drag
        kmi = km.keymap_items.new('lumi.move_positioning', 'LEFTMOUSE', 'PRESS', ctrl=False, shift=True, alt=True)
        addon_keymaps.append((km, kmi))

        # Smart control shortcuts - using consolidated operator
        # Main toggle: Ctrl+Shift+Alt+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True, alt=True)
        addon_keymaps.append((km, kmi))
        
        # Mode-specific smart control with preset mode
        # Distance mode: Ctrl+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', ctrl=True)
        kmi.properties.mode = 'DISTANCE'
        addon_keymaps.append((km, kmi))
        
        # Power mode: Shift+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', shift=True)
        kmi.properties.mode = 'POWER'
        addon_keymaps.append((km, kmi))
        
        # Scale mode: Alt+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', alt=True)
        kmi.properties.mode = 'SCALE'
        addon_keymaps.append((km, kmi))
        
        # Angle mode: Ctrl+Shift+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
        kmi.properties.mode = 'ANGLE'
        addon_keymaps.append((km, kmi))
        
        # Temperature mode: Ctrl+Alt+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', ctrl=True, alt=True)
        kmi.properties.mode = 'TEMPERATURE'
        addon_keymaps.append((km, kmi))
        
        # Blend mode: Shift+Alt+MIDDLEMOUSE
        kmi = km.keymap_items.new('lumi.smart_control', 'MIDDLEMOUSE', 'PRESS', shift=True, alt=True)
        kmi.properties.mode = 'BLEND'
        addon_keymaps.append((km, kmi))

    except (AttributeError, RuntimeError):
        pass

def unregister_keymaps() -> None:
    """Unregister all LumiFlow keymaps"""
    try:
        for km, kmi in addon_keymaps:
            if km and kmi:
                km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    except Exception:
        addon_keymaps.clear()

def register_handlers() -> None:
    if lumi_scene_update_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(lumi_scene_update_handler)

    if depsgraph_update_default_group not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(depsgraph_update_default_group)
        
    # Special handler for light groups update
    if lumi_light_groups_update_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(lumi_light_groups_update_handler)

    # Handler for syncing light groups when file is loaded
    if depsgraph_update_default_group not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(depsgraph_update_default_group)

def unregister_handlers() -> None:
    try:
        # Remove handler from depsgraph_update_post
        if lumi_scene_update_handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(lumi_scene_update_handler)
        # Remove handler from depsgraph_update_post
        if depsgraph_update_default_group in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update_default_group)
        # Remove special handler for light groups update
        if lumi_light_groups_update_handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(lumi_light_groups_update_handler)
        # Remove handler for syncing light groups when file is loaded
        if depsgraph_update_default_group in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(depsgraph_update_default_group)
    except Exception:
        pass


# =====================================================================
# SIMPLE PERSISTENT FILE DETECTION SYSTEM
# =====================================================================

from bpy.app.handlers import persistent

# Simple global state
detection_count = 0

@persistent
def lumiflow_pre_load_handler(dummy):
    """Called BEFORE Blender starts opening file"""
    global detection_count
    detection_count += 1
    
    # Force disable addon
    if hasattr(bpy.context, 'scene') and bpy.context.scene:
        if hasattr(bpy.context.scene, 'lumi_enabled') and bpy.context.scene.lumi_enabled:
            bpy.context.scene.lumi_enabled = False

def reinitialize_overlay_system():
    """Re-initialize overlay system after file load or addon enable"""
    try:
        # Clean up and reset overlay system using overlay_manager
        from .ui.overlay.config import overlay_manager
        overlay_manager.disable_all_handlers()
        overlay_manager.handlers.clear()
        
        # Re-register overlay handlers if addon is enabled
        if hasattr(bpy.context, 'scene') and bpy.context.scene:
            if hasattr(bpy.context.scene, 'lumi_enabled') and bpy.context.scene.lumi_enabled:
                from .ui.overlay import (
                    lumi_enable_draw_handler,
                    lumi_enable_overlay_draw_handler,
                    lumi_enable_stroke_overlay_handler,
                    lumi_enable_tips_overlay_handler,
                    lumi_enable_cursor_overlay_handler
                )
                
                # Re-enable overlay handlers
                lumi_enable_draw_handler()
                lumi_enable_overlay_draw_handler()
                lumi_enable_stroke_overlay_handler()
                lumi_enable_tips_overlay_handler()
                
                # Enable cursor overlay handler (now used for both smart control and positioning modes)
                lumi_enable_cursor_overlay_handler()
                
                # Force redraw
                if hasattr(bpy.context, 'region') and bpy.context.region:
                    bpy.context.region.tag_redraw()
                    
    except Exception as e:
        pass

@persistent  
def lumiflow_save_pre_handler(dummy):
    """Called BEFORE Blender saves file"""
    
    try:
        # Save camera-light assignments to persistent properties before saving
        if hasattr(bpy.context, 'scene') and bpy.context.scene:
            try:
                from .core.camera_manager import get_camera_light_manager
                camera_manager = get_camera_light_manager()
                camera_manager._save_assignments_to_properties()
                print("💾 Camera-light assignments saved to file")
            except Exception as e:
                print(f"⚠️  Failed to save camera-light assignments: {e}")
                
    except Exception as e:
        pass

@persistent  
def lumiflow_post_load_handler(dummy):
    """Called AFTER Blender finishes reading file"""
    
    try:
        # Only disable addon if it was previously enabled (prevent aggressive disable)
        if hasattr(bpy.context, 'scene') and bpy.context.scene:
            addon_was_enabled = hasattr(bpy.context.scene, 'lumi_enabled') and bpy.context.scene.lumi_enabled
            
            if addon_was_enabled:
                bpy.context.scene.lumi_enabled = False
            
            # Cleanup state (but preserve overlay capability)
            try:
                from .core.state import get_state
                state = get_state()
                if state:
                    state.cleanup()
            except:
                pass
            
            # Load camera-light assignments from persistent properties
            try:
                from .core.camera_manager import get_camera_light_manager
                camera_manager = get_camera_light_manager()
                camera_manager._load_assignments_from_properties()
                print("📖 Camera-light assignments loaded from file")
            except Exception as e:
                print(f"⚠️  Failed to load camera-light assignments: {e}")
                
    except Exception as e:
        pass

def register_file_detection_system():
    """Register file detection handlers"""
    
    # Register load handlers
    if lumiflow_pre_load_handler not in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.append(lumiflow_pre_load_handler)
    
    if lumiflow_post_load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(lumiflow_post_load_handler)
    
    # Register save handler
    if lumiflow_save_pre_handler not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(lumiflow_save_pre_handler)

def unregister_file_detection_system():
    """Unregister file detection handlers"""
    
    # Unregister load handlers
    if lumiflow_pre_load_handler in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.remove(lumiflow_pre_load_handler)
    
    if lumiflow_post_load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(lumiflow_post_load_handler)
    
    # Unregister save handler
    if lumiflow_save_pre_handler in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(lumiflow_save_pre_handler)



# preferences class now imported from preferences.py

# Function to register classes to Blender
def register() -> None:
    """Register all classes, properties, handlers, and keymaps for the addon"""
    try:
        # Register class to Blender system
        bpy.utils.register_class(LumiFlowAddonPreferences)
    except Exception:
        pass
    
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass
    
    register_properties()
    bpy.types.Scene.light_props = bpy.props.PointerProperty(type=LightPositioningProperties)
    bpy.types.Scene.lumi_professional_props = bpy.props.PointerProperty(type=ProfessionalLightingProperties)
    bpy.types.Scene.lumi_light_control_props = bpy.props.PointerProperty(type=LightControlProperties)
    
    # Add individual professional lighting properties for UI access
    bpy.types.Scene.lumi_harmony_type = bpy.props.EnumProperty(
        name="Harmony Type",
        items=[
            ('complementary', "Complementary", "Opposite colors on color wheel"),
            ('triadic', "Triadic", "Three colors equally spaced"),
            ('analogous', "Analogous", "Adjacent colors on color wheel"),
        ],
        default='complementary'
    )
    bpy.types.Scene.lumi_base_hue = bpy.props.FloatProperty(name="Base Hue", default=60.0, min=0.0, max=360.0)
    bpy.types.Scene.lumi_saturation = bpy.props.FloatProperty(name="Saturation", default=0.8, min=0.0, max=1.0)
    bpy.types.Scene.lumi_mood_type = bpy.props.EnumProperty(
        name="Mood",
        items=[('dramatic', "Dramatic", ""), ('romantic', "Romantic", ""), ('horror', "Horror", "")],
        default='dramatic'
    )
    bpy.types.Scene.lumi_time_of_day = bpy.props.EnumProperty(
        name="Time",
        items=[('golden_hour', "Golden Hour", ""), ('blue_hour', "Blue Hour", ""), ('midday', "Midday", "")],
        default='golden_hour'
    )
    bpy.types.Scene.lumi_penumbra_factor = bpy.props.FloatProperty(name="Penumbra", default=1.0, min=0.1, max=5.0)
    bpy.types.Scene.lumi_contact_shadow = bpy.props.FloatProperty(name="Contact Shadow", default=0.5, min=0.0, max=1.0)
    bpy.types.Scene.lumi_shadow_density = bpy.props.FloatProperty(name="Shadow Density", default=1.0, min=0.0, max=2.0)
    bpy.types.Scene.lumi_negative_fill = bpy.props.FloatProperty(name="Negative Fill", default=0.2, min=0.0, max=1.0)
    bpy.types.Scene.lumi_use_material_shadows = bpy.props.BoolProperty(name="Material Shadows", default=True)
    bpy.types.Scene.lumi_artistic_override = bpy.props.FloatProperty(name="Artistic Override", default=0.3, min=0.0, max=1.0)
    bpy.types.Scene.lumi_haze_density = bpy.props.FloatProperty(name="Haze Density", default=0.1, min=0.0, max=1.0)
    bpy.types.Scene.lumi_fog_absorption = bpy.props.FloatProperty(name="Fog Absorption", default=0.8, min=0.0, max=1.0)
    bpy.types.Scene.lumi_scattering = bpy.props.FloatProperty(name="Scattering", default=0.0, min=-1.0, max=1.0)
    bpy.types.Scene.lumi_godrays_strength = bpy.props.FloatProperty(name="God Rays", default=0.5, min=0.0, max=2.0)
    
    # Template Browser Properties
    bpy.types.Scene.lumi_template_category = bpy.props.EnumProperty(
        name="Category",
        description="Filter templates by category",
        items=[
            ('ALL', "All", "Show all templates"),
            ('STUDIO_COMMERCIAL', "Studio & Commercial", "Studio & Commercial lighting templates"),
            ('DRAMATIC_CINEMATIC', "Dramatic & Cinematic", "Dramatic & Cinematic lighting templates"),
            ('ENVIRONMENT_REALISTIC', "Environment & Realistic", "Environment & Realistic lighting templates"),
            ('UTILITIES_SINGLE', "Utilities & Single Lights", "Utilities & Single Lights templates"),
        ],
        default='ALL'
    )

    # Sanitize stored enum values across existing scenes to avoid RNA warnings
    try:
        valid_cats = {'ALL', 'STUDIO_COMMERCIAL', 'DRAMATIC_CINEMATIC', 'ENVIRONMENT_REALISTIC', 'UTILITIES_SINGLE'}
        for sc in bpy.data.scenes:
            try:
                cur = getattr(sc, 'lumi_template_category', None)
                if cur not in valid_cats:
                    sc.lumi_template_category = 'ALL'
            except Exception:
                pass
    except Exception:
        pass
    
    bpy.types.Scene.lumi_template_view_mode = bpy.props.EnumProperty(
        name="View Mode",
        description="Template display mode",
        items=[
            ('GRID', "Grid", "Grid view", 'MESH_GRID', 0),
            ('LIST', "List", "List view", 'LONGDISPLAY', 1),
        ],
        default='GRID'
    )
    
    # Template Settings Properties
    bpy.types.Scene.lumi_template_auto_position = bpy.props.BoolProperty(
        name="Auto Position",
        description="Automatically position template lights",
        default=True
    )
    
    bpy.types.Scene.lumi_template_default_scale = bpy.props.FloatProperty(
        name="Default Scale",
        description="Default scale for template lights",
        default=1.0,
        min=0.1,
        max=10.0,
        step=0.1
    )
    
    bpy.types.Scene.lumi_template_default_intensity = bpy.props.FloatProperty(
        name="Default Intensity",
        description="Default intensity for template lights",
        default=10.0,
        min=0.1,
        max=1000.0,
        step=1.0
    )
    
    bpy.types.Scene.lumi_template_collection = bpy.props.StringProperty(
        name="Template Collection",
        description="Collection for template lights",
        default="LumiFlow Lights"
    )
    
    bpy.types.Scene.lumi_template_auto_organize = bpy.props.BoolProperty(
        name="Auto Organize",
        description="Automatically organize lights in collections",
        default=True
    )
    
    bpy.types.Scene.lumi_template_auto_save = bpy.props.BoolProperty(
        name="Auto Save",
        description="Automatically save template settings",
        default=True
    )
    
    bpy.types.Scene.lumi_template_validate = bpy.props.BoolProperty(
        name="Validate Templates",
        description="Validate templates before applying",
        default=True
    )
    
    bpy.types.Scene.lumi_template_backup = bpy.props.BoolProperty(
        name="Create Backup",
        description="Create backup before applying templates",
        default=True
    )
    
    bpy.types.Scene.lumi_template_optimize = bpy.props.BoolProperty(
        name="Optimize Performance",
        description="Optimize performance when applying templates",
        default=True
    )
    
    bpy.types.Scene.lumi_template_favorites = bpy.props.StringProperty(
        name="Favorites",
        description="Comma-separated list of favorite template IDs",
        default=""
    )
    
    bpy.types.Scene.lumi_template_auto_scale = bpy.props.BoolProperty(
        name="Auto Scale",
        description="Automatically scale lights based on scene size",
        default=True
    )
    
    bpy.types.Scene.lumi_template_intensity_multiplier = bpy.props.FloatProperty(
        name="Intensity Multiplier",
        description="Global intensity multiplier for template lights",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    bpy.types.Scene.lumi_template_camera_relative = bpy.props.BoolProperty(
        name="Camera Relative",
        description="Position lights relative to camera",
        default=False
    )
    
    bpy.types.Scene.lumi_template_preserve_existing = bpy.props.BoolProperty(
        name="Preserve Existing",
        description="Keep existing lights when applying template",
        default=False
    )
    
    # Initialize default properties for force disable behavior
    def init_default_properties():
        """Initialize default properties with force disable behavior"""
        try:
            if bpy.context and bpy.context.scene:
                # Force disable positioning mode
                bpy.context.scene.light_props.positioning_mode = 'DISABLE'
                bpy.context.scene.lumi_enabled = False
        except (AttributeError, RuntimeError):
            pass
    
    # Try to initialize now, but if it fails it's not a problem
    init_default_properties()
    
    # Initialize template systems
    try:
        initialize_error_handling()
        # Professional lighting has been removed
    except Exception:
        pass
    
    # Register handlers and keymaps
    register_handlers()
    register_keymaps()
    
    # Register file detection system
    register_file_detection_system()
    
    # Cleanup orphaned collections at startup
    from .utils.common import cleanup_lumiflow_collections
    cleanup_lumiflow_collections()
    
    # Registration completed successfully

# Function to unregister classes
def unregister() -> None:
    """Unregister all classes, properties, handlers, and keymaps"""
    # Cleanup template systems first
    try:
        cleanup_error_handling()
        # Professional lighting has been removed
    except Exception:
        pass
    
    # Clean up Quick Solo Light state
    try:
        from .operators.selection_ops import cleanup_quick_solo_state
        cleanup_quick_solo_state()
    except Exception:
        pass
    
    # Clean up Camera Light state
    try:
        from .operators.selection_ops import cleanup_camera_light_state
        cleanup_camera_light_state()
    except Exception as e:
        pass
    
    # Clean up state
    try:
        state = get_state()
        state.cleanup()
    except Exception:
        pass
    
    # Clean up icon manager
    try:
        from .ui.overlay.icon_manager import cleanup_icon_manager
        cleanup_icon_manager()
    except Exception:
        pass
    
    # Clean up dynamic menu classes
    try:
        cleanup_dynamic_menu_classes()
    except Exception:
        pass
        
    unregister_keymaps()
    unregister_handlers()
    
    # Remove pointer properties first
    
    if hasattr(bpy.types.Scene, 'light_props'):
        try:
            del bpy.types.Scene.light_props
        except Exception:
            pass
    
    if hasattr(bpy.types.Scene, 'lumi_professional_props'):
        try:
            del bpy.types.Scene.lumi_professional_props
        except Exception:
            pass
    
    if hasattr(bpy.types.Scene, 'lumi_light_control_props'):
        try:
            del bpy.types.Scene.lumi_light_control_props
        except Exception:
            pass
    
    # Unregister AddonPreferences
    try:
        bpy.utils.unregister_class(LumiFlowAddonPreferences)
    except Exception:
        pass
    
    # Unregister classes in reverse order, skip PropertyGroup that are already unregistered
    safe_classes = []
    for cls in reversed(classes):
        if hasattr(cls, 'bl_rna'):
            safe_classes.append(cls)
    
    for cls in safe_classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
    
    unregister_properties()
    
    # Cleanup orphaned collections
    from .utils.common import cleanup_lumiflow_collections
    cleanup_lumiflow_collections()
    
    # Unregister file detection system
    unregister_file_detection_system()
    
    # Unregistration completed successfully

