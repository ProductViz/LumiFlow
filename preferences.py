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
Addon Preferences
Contains the addon preferences class with all UI customization options.
"""
# # Import modul utama Blender
import bpy


class LumiFlowAddonPreferences(bpy.types.AddonPreferences):
    """Addon preferences for LumiFlow, allowing users to customize keymaps and UI options."""
    bl_idname = __package__ or "LumiFlow"

    # Custom shortcut settings
    enable_custom_shortcuts: bpy.props.BoolProperty(
        name="Enable Custom Shortcuts",
        default=True,
        description="Allow custom keymap overrides for LumiFlow operators."
    )
    
    
    # Development panel settings
    show_dev_panel: bpy.props.BoolProperty(
        name="Show Development Panel",
        default=False,
        description="Show the development panel for addon debugging and reloading (requires Developer Extras enabled)"
    )
    
    # =====================================================================
    # OVERLAY TEXT CUSTOMIZATION
    # =====================================================================
    
    overlay_display_scale: bpy.props.FloatProperty(
        name="Display Scale",
        default=1.0,
        min=0.3,
        max=3.0,
        step=0.1,
        precision=1,
        description="Combined scale factor for font size and line spacing (0.3x to 3.0x). Perfect for HD, 2K, 4K displays."
    )

    @property
    def overlay_font_scale(self):
        """Get font scale (same as display scale)."""
        return self.overlay_display_scale

    @property
    def overlay_line_spacing(self):
        """Get line spacing (proportional to display scale)."""
        return self.overlay_display_scale
    
    
    
    def force_viewport_redraw(self):
        """Force redraw of all 3D viewports to show theme changes."""
        try:
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        except:
            pass

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        
        # Header
        header = layout.row()
        header.label(text="🎨 LumiFlow Overlay Customization", icon='PREFERENCES')
        
        # =====================================================================
        # GENERAL SETTINGS
        # =====================================================================
        
        box = layout.box()
        box.label(text="General Settings", icon='SETTINGS')
        
        col = box.column()
        col.prop(self, "enable_custom_shortcuts")
        
        # Development tools
        col.separator()
        dev_row = col.row()
        dev_row.prop(self, "show_dev_panel")
        if not context.preferences.view.show_developer_ui:
            dev_row = col.row()
            dev_row.alert = True
            dev_row.label(text="⚠️ Enable 'Developer Extras' in Preferences > Interface", icon='ERROR')
        
        # =====================================================================
        # DISPLAY & FONT SETTINGS
        # =====================================================================
        
        box = layout.box()
        box.label(text="📱 Display & Font Settings", icon='FONTPREVIEW')
        
        col = box.column(align=True)
        col.label(text="Display Scale (Font & Spacing):")
        col.prop(self, "overlay_display_scale", slider=True)
        
        
        
        # =====================================================================
        # PREVIEW & HELP
        # =====================================================================
        
        info_box = layout.box()
        info_col = info_box.column()
        info_col.label(text="💡 Tips:", icon='QUESTION')
        info_col.label(text="• Display Scale: Adjust for your screen resolution (0.3x for large screens, 2.0x+ for small/high-DPI)")
        info_col.label(text="• Controls both font size and line spacing proportionally")
        info_col.label(text="• Changes take effect immediately in the 3D viewport")


# Export for registration
__all__ = ['LumiFlowAddonPreferences']

