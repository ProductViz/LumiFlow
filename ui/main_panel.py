# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Main UI Panel
Defines the main UI panel and all UI drawing logic for LumiFlow Blender addon.
"""
import bpy
from ..utils import lumi_is_addon_enabled

# Import UIList classes for template lists
try:
    from .light_mixer import draw_light_mixer_ui
except ImportError:
    # Fallback if import fails
    def draw_light_mixer_ui(layout, context):
        layout.label(text="Light mixer not available", icon='ERROR')

# Color controls have been removed
def draw_color_controls_ui(layout, context):
    layout.label(text="Color controls not available", icon='ERROR')

# Import template browser helper
try:
    from .template_browser import draw_template_quick_access
except ImportError:
    def draw_template_quick_access(layout, context):
        # Fallback if template browser not available
        pass

class LUMI_PT_light_control(bpy.types.Panel):
    """Main LumiFlow panel for lighting control"""
    bl_label = "💡 LumiFlow"
    bl_idname = "LUMI_PT_light_control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LumiFlow"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        scene = context.scene

        # Early return pattern for better readability
        self._draw_main_toggle(layout, scene)
        
        if not lumi_is_addon_enabled():
            return

        # Template Quick Access - Professional lighting templates
        self._draw_template_quick_access(layout, context)

        # Cache selected lights to avoid multiple calculations
        selected_lights = self._get_selected_lights(context)
        
        # Light management section disabled - only show in Light Mixer panel
        self._draw_light_management_section(layout, context, selected_lights)        

        self._draw_expandable_sections(layout, scene)

    def _draw_main_toggle(self, layout, scene):
        """Enable/Disable toggle"""
        box = layout.box()
        row = box.row()
        row.scale_y = 1.5
        
        if lumi_is_addon_enabled():
            row.prop(scene, "lumi_enabled", text="✅ ENABLED", toggle=True, icon='CHECKMARK')
        else:
            row.prop(scene, "lumi_enabled", text="❌ DISABLED", toggle=True, icon='CANCEL')
            box.label(text="Click above to enable LumiFlow", icon='INFO')
            return
        
        # Light Assignment Mode buttons
        assignment_box = layout.box()
        assignment_row = assignment_box.row(align=True)
        assignment_row.label(text="Assign to : ", icon='LIGHT')
        
        # Scene button
        scene_active = getattr(scene, 'lumi_light_assignment_mode', 'SCENE') == 'SCENE'
        scene_op = assignment_row.operator("lumi.set_light_assignment_mode", text="Scene", depress=scene_active, icon='SCENE_DATA')
        scene_op.mode = 'SCENE'
        
        # Camera button  
        camera_active = getattr(scene, 'lumi_light_assignment_mode', 'SCENE') == 'CAMERA'
        camera_op = assignment_row.operator("lumi.set_light_assignment_mode", text="Camera", depress=camera_active, icon='CAMERA_DATA')
        camera_op.mode = 'CAMERA'

    def _draw_template_quick_access(self, layout: bpy.types.UILayout, context: bpy.types.Context):
        """Template Quick Access - Only most popular templates for main panel"""
        try:
            # Enhanced template section for main panel
            box = layout.box()
            header_row = box.row(align=True)
            header_row.label(text="Quick Templates", icon='LIGHT')
            
            # Quick access to most popular templates only
            selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
            enabled = bool(selected_meshes)
            # Always show the template buttons, but disable them when no mesh is selected
            col = box.column(align=True)
            quick_row = col.row(align=True)
            quick_row.scale_y = 1.0
            quick_row.enabled = enabled
            try:
                quick_row.operator("lumi.apply_template_default", text="Key Light").template_id = "key_light_only"
                quick_row.operator("lumi.apply_template_default", text="Rim Light").template_id = "rim_light_only"
                quick_row.operator("lumi.apply_lighting_template", text="Three-Point").template_id = "three_point_setup"
            except:
                # Fallback to basic operators
                quick_row.operator("object.light_add", text="Key Light").type = 'AREA'
                quick_row.operator("object.light_add", text="3-Point").type = 'SPOT'
                quick_row.operator("object.light_add", text="Three-Point").type = 'SPOT'
            
            quick_row2 = col.row(align=True)
            quick_row2.scale_y = 1.0
            quick_row2.enabled = enabled
            try:
                quick_row2.operator("lumi.apply_template_default", text="Fill Light").template_id = "fill_light_only"
                quick_row2.operator("lumi.apply_template_default", text="Background").template_id = "backlight_only"
                quick_row2.operator("lumi.apply_lighting_template", text="Loop Portrait").template_id = "loop_portrait"
            except:
                # Fallback to basic operators
                quick_row2.operator("object.light_add", text="Portrait").type = 'POINT'
                quick_row2.operator("object.light_add", text="Product").type = 'SUN'
                quick_row2.operator("object.light_add", text="Loop Portrait").type = 'POINT'           
                
        except Exception as e:
            # Fallback if template system not available
            box = layout.box()
            box.label(text="Quick Templates", icon='LIGHT')
            box.label(text="Select objects to apply templates", icon='INFO')

    def _draw_light_management_section(self, layout: bpy.types.UILayout, context: bpy.types.Context, selected_lights: list[bpy.types.Object]):
        """Combined light list and positioning controls"""
        
        
        # Always show positioning controls; disable interaction when no lights are selected
        try:
            box = layout.box()
            box.enabled = bool(selected_lights)
            self._draw_positioning_controls(box, context)
        except (AttributeError, RuntimeError):
            # Fallback: try to draw normally if the boxed layout fails
            try:
                self._draw_positioning_controls(layout, context)
            except (AttributeError, RuntimeError):
                pass

    def _draw_expandable_sections(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
        """Essential expandable sections only - Advanced features moved to sub panels"""
        # Set compact layout for all sections
        layout.use_property_split = False
        layout.use_property_decorate = False
        
       
              
        # Only essential expandable sections remain in main panel       
        self._draw_scroll_settings(layout, scene)
        
        self._draw_overlay_controls(layout, scene)

    def _draw_scroll_settings(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
            """Scroll settings with improved layout"""
            # Use layout directly instead of box for flat appearance
            header_row = layout.row(align=True)
            header_row.scale_y = 1.3
            header_row.alignment = 'LEFT'
            header_row.use_property_decorate = False
            
            icon = 'DOWNARROW_HLT' if getattr(scene, 'lumi_scroll_settings_expanded', False) else 'RIGHTARROW'
            header_row.prop(scene, "lumi_scroll_settings_expanded", text="", icon=icon, emboss=False)
            header_row.prop(scene, "lumi_scroll_settings_expanded", text="Smart Control", 
                        icon='MOUSE_LMB', emboss=False)
            
            if getattr(scene, 'lumi_scroll_settings_expanded', False):
                # Use layout directly instead of content_box
                try:
                    self._draw_smart_controls(layout, scene)
                except (AttributeError, RuntimeError):
                    error_row = layout.row()
                    error_row.label(text="Error accessing scroll settings", icon='ERROR')

    def _get_selected_lights(self, context: bpy.types.Context) -> list[bpy.types.Object]:
        """Safe method to get selected lights with error handling"""
        try:
            return [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        except (AttributeError, RuntimeError):
            return []
    
    def _draw_positioning_controls(self, layout: bpy.types.UILayout, context: bpy.types.Context):
        """Improved positioning controls with better organization"""
        try:
            props = context.scene.light_props if hasattr(context.scene, 'light_props') else None
            
            # Header with current mode indicator
            box = layout.box()
            header_row = box.row(align=True)
            header_row.label(text="Positioning Mode", icon='TOOL_SETTINGS')
            
            # Mode buttons in a cleaner grid
            if props is not None:
                self._draw_positioning_mode_buttons(box, props)
            else:
                box.label(text="Light properties not available", icon='ERROR')
            
        except (AttributeError, RuntimeError):
            error_row = layout.row()
            error_row.label(text="Error Positioning Mode", icon='ERROR')

    def _draw_positioning_mode_buttons(self, layout: bpy.types.UILayout, props: bpy.types.PropertyGroup):
        """Clean grid layout for positioning mode buttons"""
        modes = [
            ('HIGHLIGHT', 'lumi.highlight_positioning', 'Highlight', 'OUTLINER_OB_LIGHT'),
            ('NORMAL', 'lumi.normal_positioning', 'Normal', 'MODIFIER'),
            ('TARGET', 'lumi.target_positioning', 'Target', 'CONSTRAINT'),
            ('ORBIT', 'lumi.orbit_positioning', 'Orbit', 'FORCE_FORCE'),
            ('FREE', 'lumi.free_positioning', 'Free', 'ORIENTATION_GLOBAL'),
            ('MOVE', 'lumi.move_positioning', 'Move', 'HAND')
        ]
        
        # Create 3x2 grid
        for i in range(0, len(modes), 3):
            row = layout.row(align=True)
            row.scale_y = 1.3
            
            for j in range(3):
                if i + j < len(modes):
                    mode_id, op_name, label, icon = modes[i + j]
                    try:
                        is_active = props and hasattr(props, 'positioning_mode') and props.positioning_mode == mode_id
                        row.operator(op_name, text=label, icon=icon, depress=is_active)
                    except:
                        # Fallback to basic operators
                        if mode_id == 'HIGHLIGHT':
                            row.operator("lumi.highlight_positioning", text=label, icon=icon)
                        elif mode_id == 'NORMAL':
                            row.operator("lumi.normal_positioning", text=label, icon=icon)
                        elif mode_id == 'TARGET':
                            row.operator("lumi.target_positioning", text=label, icon=icon)
                        elif mode_id == 'ORBIT':
                            row.operator("lumi.orbit_positioning", text=label, icon=icon)
                        elif mode_id == 'FREE':
                            row.operator("lumi.free_positioning", text=label, icon=icon)
                        elif mode_id == 'MOVE':
                            row.operator("lumi.move_positioning", text=label, icon=icon)

    def _draw_smart_controls(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
        """Improved smart controls layout"""
        col = layout.column(align=True)
        # Tighter spacing overall
        col.separator(factor=0.5)
        
        # Axis settings
        axis_box = col.box()
        axis_col = axis_box.column(align=True)
        axis_col.scale_y = 0.85
        axis_hdr = axis_col.row(align=True)
        axis_hdr.scale_y = 0.9
        axis_hdr.label(text="Scale Axis", icon='ORIENTATION_LOCAL')
        if hasattr(scene, 'lumi_scale_axis'):
            axis_row = axis_col.split(factor=0.3)
            axis_left = axis_row.row(align=True)
            axis_left.alignment = 'RIGHT'
            axis_left.label(text="Axis :")
            axis_right = axis_row.row(align=True)
            axis_right.use_property_decorate = False
            axis_right.prop(scene, "lumi_scale_axis", text="")

    def _draw_overlay_controls(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
        """Overlay controls at bottom"""
        row = layout.row(align=True)
        row.scale_y = 1.1     
        if hasattr(scene, 'lumi_show_overlay_tips'):
            row.prop(scene, "lumi_show_overlay_tips", text="", icon='QUESTION')
        if hasattr(scene, 'lumi_show_overlay_info'):
            row.prop(scene, "lumi_show_overlay_info", text="", icon='INFO')


# =====================================================================
# REGISTRATION CLASSES - GUARANTEED TO WORK
# =====================================================================

MAIN_PANEL_CLASSES = [
    LUMI_PT_light_control,
]

def register():
    """Register all panel classes"""
    for cls in MAIN_PANEL_CLASSES:
        try:
            bpy.utils.register_class(cls)
            print(f"✅ Registered: {cls.__name__}")
        except Exception as e:
            print(f"❌ Failed to register {cls.__name__}: {e}")


def unregister():
    """Unregister all panel classes"""
    for cls in reversed(MAIN_PANEL_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
            print(f"✅ Unregistered: {cls.__name__}")
        except Exception as e:
            print(f"❌ Failed to unregister {cls.__name__}: {e}")


# Make classes available for import
__all__ = [
    'LUMI_PT_light_control',
    'MAIN_PANEL_CLASSES'
]
