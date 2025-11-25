# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Main UI Panel
Defines the main UI panel and all UI drawing logic for LumiFlow Blender addon.
"""
import bpy
from ..utils import lumi_is_addon_enabled
from .overlay.config import viewport_overlay_manager

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

        self._draw_positioning_controls(layout, context)

        self._draw_smart_setting(layout, scene)

        # Quick Smart Add Exclude overview - shown below Smart Control
        self._draw_quick_exclude_overview(layout, context)
        
        self._draw_overlay_controls(layout, scene)  
        # Conditional panel rendering - only show one at a time
        if scene.show_donate_panel:
            self.draw_donate_section(context, layout)
        elif scene.show_update_panel:
            self.draw_update_section(context, layout)

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

        # Positioning Mode Toggle - MOVE TO HEADER (as per user request)

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
                quick_row2.operator("lumi.apply_lighting_template", text="Clamshell").template_id = "clamshell_beauty"
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
        
        # Background System Quick Access
        self._draw_background_quick_access(layout, context)

    def _draw_background_quick_access(self, layout: bpy.types.UILayout, context: bpy.types.Context):
        """Background System Quick Access"""
        try:
            box = layout.box()
            header_row = box.row(align=True)
            header_row.label(text="Background System", icon='IMAGE_BACKGROUND')
            
            # Check for existing backgrounds
            existing_bg = None
            bg_lights_count = 0
            for obj in context.scene.objects:
                if obj.get("lumiflow_background"):
                    existing_bg = obj
                if obj.type == 'LIGHT' and obj.get("lumiflow_bg_light"):
                    bg_lights_count += 1
            
            col = box.column(align=True)
            
            if existing_bg:
                # Show existing background info
                info_row = col.row(align=True)
                info_row.label(text=f"Active: {existing_bg.name}", icon='CHECKMARK')
                
                # Show background lights count
                if bg_lights_count > 0:
                    light_row = col.row(align=True)
                    light_row.label(text=f"BG Lights: {bg_lights_count}", icon='LIGHT')
                
                # Quick actions
                action_row = col.row(align=True)
                action_row.operator("lumi.background_menu_call", text="Modify", icon='MODIFIER')
                action_row.operator("lumi.remove_background", text="Remove", icon='X')
                
                # Layer isolation button (Phase 2)
                try:
                    from ..operators.background.light_linking import is_light_linking_available
                    if is_light_linking_available():
                        iso_row = col.row(align=True)
                        iso_row.operator("lumi.apply_layer_isolation", text="Apply Isolation", icon='UNLINKED')
                        iso_row.operator("lumi.clear_layer_isolation", text="Clear", icon='X')
                except ImportError:
                    pass
            else:
                # No background - show create button
                col.operator("lumi.background_menu_call", text="Add Background (Ctrl+Shift+B)", icon='ADD')
                col.label(text="Select product first for auto-sizing", icon='INFO')
                
        except Exception:
            pass

    def _draw_quick_exclude_overview(self, layout: bpy.types.UILayout, context: bpy.types.Context):
        scene = context.scene
        exclude_targets = [obj for obj in scene.objects if obj.type == 'MESH' and getattr(obj, "lumi_exclude_quick_add", False)]

        if not exclude_targets:
            return

        box = layout.box()
        header = box.row(align=True)
        header.label(text="Quick Smart Add Exclude", icon='RESTRICT_SELECT_OFF')

        # List excluded objects with per-object remove button
        list_col = box.column(align=True)
        for obj in exclude_targets:
            item_box = list_col.box()
            row = item_box.row(align=True)
            row.label(text=obj.name, icon='MESH_CUBE')
            row.prop(obj, "lumi_exclude_quick_add", text="", icon='CANCEL', toggle=True)

    def _draw_smart_setting(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
            """Smart control settings with toggle only (axis controlled via viewport menu)"""
            box = layout.box()

            # Smart Control Mode toggle
            toggle_row = box.row()
            toggle_row.scale_y = 1.3

            smart_control_enabled = getattr(scene, 'lumi_smart_control_mode_enabled', True)
            if smart_control_enabled:
                toggle_row.prop(scene, "lumi_smart_control_mode_enabled", text="✅ SMART CONTROL ENABLED", toggle=True)
            else:
                toggle_row.prop(scene, "lumi_smart_control_mode_enabled", text="❌ SMART CONTROL DISABLED", toggle=True)

    def _get_selected_lights(self, context: bpy.types.Context) -> list[bpy.types.Object]:
        """Safe method to get selected lights with error handling"""
        try:
            return [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        except (AttributeError, RuntimeError):
            return []
    
    def _draw_positioning_controls(self, layout: bpy.types.UILayout, context: bpy.types.Context):
        """Clean positioning controls - just buttons in a box"""
        try:
            scene = context.scene
            props = context.scene.light_props if hasattr(context.scene, 'light_props') else None

            # Style positioning toggle to match main addon enable toggle
            positioning_box = layout.box()
            positioning_row = positioning_box.row()
            positioning_row.scale_y = 1.3  # Match main toggle height

            if getattr(scene, 'lumi_positioning_mode_enabled', True):
                positioning_row.prop(scene, "lumi_positioning_mode_enabled", text=" POSITIONING ENABLED", toggle=True)
            else:
                positioning_row.prop(scene, "lumi_positioning_mode_enabled", text=" POSITIONING DISABLED", toggle=True)

        except (AttributeError, RuntimeError):
            error_row = layout.row()
            error_row.label(text="Error: Positioning Mode", icon='ERROR')

    def _draw_smart_controls(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
        """Deprecated smart controls layout (no UI currently drawn)"""
        return

    def _draw_overlay_controls(self, layout: bpy.types.UILayout, scene: bpy.types.Scene):
        """Overlay controls at bottom with viewport-specific management"""
        context = bpy.context

        # Set current context area for viewport-specific state management
        viewport_overlay_manager.set_current_context_area(context)

        # Get current viewport ID for state management
        viewport_id = viewport_overlay_manager.get_viewport_id(context)

        # Initialize viewport states if needed
        viewport_overlay_manager.initialize_viewport_states(context)

        row = layout.row(align=True)
        row.scale_y = 1.1

        # Tips overlay toggle with viewport-specific state
        if hasattr(scene, 'lumi_show_overlay_tips'):
            tips_enabled = viewport_overlay_manager.get_overlay_state(context, 'overlay_tips')
            tips_prop = row.operator("lumi.toggle_viewport_overlay", text="", icon='QUESTION', depress=tips_enabled)
            tips_prop.overlay_type = 'overlay_tips'
            tips_prop.viewport_id = viewport_id or ""

        # Info overlay toggle with viewport-specific state
        if hasattr(scene, 'lumi_show_overlay_info'):
            info_enabled = viewport_overlay_manager.get_overlay_state(context, 'overlay_info')
            info_prop = row.operator("lumi.toggle_viewport_overlay", text="", icon='INFO', depress=info_enabled)
            info_prop.overlay_type = 'overlay_info'
            info_prop.viewport_id = viewport_id or ""

        # Clean viewport toggle button with dynamic icon (viewport-specific)
        clean_active = viewport_overlay_manager.get_overlay_state(context, 'clean_viewport')
        clean_icon = 'RESTRICT_VIEW_ON' if clean_active else 'RESTRICT_VIEW_OFF'
        row.operator("lumi.clean_viewport", text="", icon=clean_icon, depress=clean_active)

        # Light Picker toggle button
        picker_enabled = scene.enable_light_picker
        picker_icon = 'RESTRICT_SELECT_ON' if picker_enabled else 'RESTRICT_SELECT_OFF'
        row.prop(scene, "enable_light_picker", text="", icon=picker_icon, toggle=True)

        # User Guide button
        row.operator("lumi.open_user_guide", text="", icon='HELP')

        # Update panel toggle
        row.prop(scene, "show_update_panel", text="Check updates", icon='FILE_REFRESH')

        # Donate toggle button
        row.prop(scene, "show_donate_panel", text="Donate", icon='FUND')

        row.operator("lumi.open_community_discord", text="", icon='COMMUNITY')

    def draw_update_section(self, context, layout):
        """Draw update information section"""
        wm = context.window_manager

        # Separator for visual clarity
        layout.separator()

        # Update section box
        update_box = layout.box()

        # Header
        header_row = update_box.row()
        header_row.label(text="Addon Update", icon='FILE_REFRESH')

        # Get update info
        update_info = wm.lumiflow_update_info

        if not update_info:
            # Still checking or first time
            check_box = update_box.box()
            check_box.label(text="Checking for updates...", icon='SORTTIME')
            return

        # Parse update info: "STATUS|version|download_url"
        parts = update_info.split("|")
        status = parts[0]

        if status == "ERROR":
            # Error occurred
            error_box = update_box.box()
            error_box.label(text="Error:", icon='ERROR')
            if len(parts) > 1:
                error_box.label(text=parts[1])

        elif status == "UPTODATE":
            # Up to date
            uptodate_box = update_box.box()
            col = uptodate_box.column(align=True)
            col.label(text="Up to Date", icon='CHECKMARK')
            if len(parts) > 1:
                col.label(text=f"Current: {parts[1]}")

        elif status == "SUCCESS":
            # Update successful - show restart message
            success_box = update_box.box()
            col = success_box.column(align=True)
            col.label(text="Update Successful!", icon='CHECKMARK')
            
            if len(parts) > 1:
                new_version = parts[1]
                col.separator(factor=0.5)
                col.label(text=f"Updated to: {new_version}")
            
            col.separator(factor=0.5)
            
            # Restart warning - prominent display
            warning_box = col.box()
            warning_col = warning_box.column(align=True)
            warning_col.scale_y = 1.3
            warning_col.label(text="⚠ Please Restart Blender", icon='ERROR')
            warning_col.label(text="to complete the update")

        elif status == "UPDATE":
            # New version available
            update_available_box = update_box.box()

            col = update_available_box.column(align=True)
            col.label(text="New Version Available", icon='INFO')

            # Version info
            if len(parts) > 1:
                new_version = parts[1]
                col.separator(factor=0.5)

                # Current vs New version in 2 columns
                row = col.row(align=True)
                split = row.split(factor=0.5)

                # Current version (left)
                left_col = split.column(align=True)
                left_col.label(text="Current:")
                from .. import bl_info
                current = bl_info["version"]
                current_str = f"v{current[0]}.{current[1]}.{current[2]}"
                left_col.label(text=current_str)

                # New version (right)
                right_col = split.column(align=True)
                right_col.label(text="Latest:")
                right_col.label(text=new_version)

            col.separator(factor=0.5)

            # Update buttons - 2 options
            if len(parts) > 2:
                download_url = parts[2]
                
                # Row 1: Update Now button (auto install)
                row = col.row()
                row.scale_y = 1.5
                op = row.operator("lumiflow.update_addon", text="Update Now", icon='IMPORT')
                op.download_url = download_url
                op.new_version = new_version
                
                # Row 2: Download from GitHub button (manual)
                row2 = col.row()
                row2.scale_y = 1.2
                op2 = row2.operator("lumiflow.download_zip", text="Download from GitHub", icon='URL')
                op2.download_url = download_url
                op2.new_version = new_version

            # Warning message
            col.separator(factor=0.3)
            warning_row = col.row()
            warning_row.label(text="🔁 Reload Blender after update")

    def draw_donate_section(self, context, layout):
        """Draw donation information section"""
        wm = context.window_manager

        # Separator for visual clarity
        layout.separator()

        # Donate section box
        donate_box = layout.box()

        # Header
        header_row = donate_box.row()
        header_row.label(text="Support LumiFlow", icon='FUND')

        # Content box
        content_box = donate_box.box()
        col = content_box.column(align=True)

        # Message
        col.label(text="LumiFlow is free and open-source")
        col.label(text="Your support helps development")
        col.separator(factor=0.5)

        # Donation links
        col.label(text="Support via:", icon='HEART')

        # Patreon
        row = col.row()
        row.scale_y = 1.3
        op = row.operator("wm.url_open", text="Patreon")
        op.url = "https://patreon.com/LumiFlow"

        # Ko-fi
        row = col.row()
        row.scale_y = 1.3
        op = row.operator("wm.url_open", text="Ko-fi")
        op.url = "https://ko-fi.com/lumiflow"

        col.separator(factor=0.3)
        col.label(text="Thank you for your support! ❤️",)



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
