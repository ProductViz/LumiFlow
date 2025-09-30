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
    
    # Startup tips settings
    show_tips_on_start: bpy.props.BoolProperty(
        name="Show Tips on Startup",
        default=True,
        description="Show helpful tips when Blender starts."
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
    
    overlay_font_scale: bpy.props.FloatProperty(
        name="Font Scale",
        default=1.0,
        min=0.3,
        max=3.0,
        step=0.1,
        precision=1,
        description="Scale factor for overlay text font size (0.3x to 3.0x). Perfect for HD, 2K, 4K displays."
    )
    overlay_line_spacing: bpy.props.FloatProperty(
        name="Line Spacing",
        default=1.0,
        min=0.5,
        max=2.5,
        step=0.1,
        precision=1,
        description="Multiplier for line spacing between overlay text lines. Higher values = more spacing."
    )
    
    # =====================================================================
    # THEME AND COLOR CUSTOMIZATION
    # =====================================================================
    
    theme_preset: bpy.props.EnumProperty(
        name="Color Theme",
        items=[
            ('DEFAULT', "Default", "LumiFlow default blue/orange theme"),
            ('DARK', "High Contrast Dark", "High contrast dark theme for dark environments"),
            ('LIGHT', "Light Theme", "Light theme for bright workspaces"),
            ('WARM', "Warm", "Warm orange/red theme"),
            ('COOL', "Cool", "Cool blue/cyan theme"),
            ('MINIMAL', "Minimal", "Minimal grayscale theme"),
            ('NEON', "Neon", "Bright neon colors for dark environments"),
            ('CUSTOM', "Custom", "Use custom colors defined below")
        ],
        default='DEFAULT',
        description="Quick color theme presets. Select 'Custom' to use your own colors."
    )
    
    use_custom_colors: bpy.props.BoolProperty(
        name="Use Custom Colors",
        default=False,
        description="Override theme presets with custom colors below."
    )
    
    # Primary colors
    header_color: bpy.props.FloatVectorProperty(
        name="Header Color",
        subtype='COLOR',
        size=4,
        default=(0.2, 0.7, 1.0, 1.0),
        min=0.0,
        max=1.0,
        description="Color for section headers and main titles."
    )
    highlight_color: bpy.props.FloatVectorProperty(
        name="Highlight Color",
        subtype='COLOR',
        size=4,
        default=(1.0, 0.85, 0.2, 1.0),
        min=0.0,
        max=1.0,
        description="Color for active/highlighted values and important information."
    )
    normal_text_color: bpy.props.FloatVectorProperty(
        name="Normal Text",
        subtype='COLOR',
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        description="Color for standard text and labels."
    )
    secondary_text_color: bpy.props.FloatVectorProperty(
        name="Secondary Text",
        subtype='COLOR',
        size=4,
        default=(0.85, 0.85, 0.85, 1.0),
        min=0.0,
        max=1.0,
        description="Color for secondary information and descriptions."
    )
    dim_text_color: bpy.props.FloatVectorProperty(
        name="Dim Text",
        subtype='COLOR',
        size=4,
        default=(0.6, 0.6, 0.6, 1.0),
        min=0.0,
        description="Color for less important text and subtle information."
    )
    
    # Smart overlay colors
    smart_text_color: bpy.props.FloatVectorProperty(
        name="Smart Text",
        subtype='COLOR',
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        description="Color for smart overlay text."
    )
    smart_value_color: bpy.props.FloatVectorProperty(
        name="Smart Value",
        subtype='COLOR',
        size=4,
        default=(1.0, 1.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
        description="Color for smart overlay values."
    )
    
    # =====================================================================
    # OVERLAY POSITIONING & LAYOUT
    # =====================================================================
    
    info_panel_position: bpy.props.EnumProperty(
        name="Info Panel Position",
        items=[
            ('BOTTOM_RIGHT', "Bottom Right", "Position info panel at bottom right (default)"),
            ('BOTTOM_LEFT', "Bottom Left", "Position info panel at bottom left"),
            ('TOP_RIGHT', "Top Right", "Position info panel at top right"),
            ('TOP_LEFT', "Top Left", "Position info panel at top left")
        ],
        default='BOTTOM_RIGHT',
        description="Position of the light information panel."
    )
    tips_panel_position: bpy.props.EnumProperty(
        name="Tips Panel Position",
        items=[
            ('BOTTOM_LEFT', "Bottom Left", "Position tips panel at bottom left (default)"),
            ('BOTTOM_RIGHT', "Bottom Right", "Position tips panel at bottom right"),
            ('TOP_LEFT', "Top Left", "Position tips panel at top left"),
            ('TOP_RIGHT', "Top Right", "Position tips panel at top right")
        ],
        default='BOTTOM_LEFT',
        description="Position of the tips/help panel."
    )
    
    overlay_opacity: bpy.props.FloatProperty(
        name="Overlay Opacity",
        default=1.0,
        min=0.1,
        max=1.0,
        step=0.1,
        precision=1,
        description="Overall opacity/transparency of all overlay elements."
    )
    
    info_panel_margin_x: bpy.props.IntProperty(
        name="Info Panel Margin X",
        default=20,
        min=0,
        max=200,
        description="Horizontal margin/offset for info panel from edge of viewport."
    )
    info_panel_margin_y: bpy.props.IntProperty(
        name="Info Panel Margin Y",
        default=20,
        min=0,
        max=200,
        description="Vertical margin/offset for info panel from edge of viewport."
    )
    tips_panel_margin_x: bpy.props.IntProperty(
        name="Tips Panel Margin X",
        default=20,
        min=0,
        max=200,
        description="Horizontal margin/offset for tips panel from edge of viewport."
    )
    tips_panel_margin_y: bpy.props.IntProperty(
        name="Tips Panel Margin Y",
        default=20,
        min=0,
        max=200,
        description="Vertical margin/offset for tips panel from edge of viewport."
    )
    
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
        col.prop(self, "show_tips_on_start")
        
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
        col.label(text="Font Scale (Perfect for HD, 2K, 4K displays):")
        col.prop(self, "overlay_font_scale", slider=True)
        
        col.separator(factor=0.5)
        col.label(text="Line Spacing:")
        col.prop(self, "overlay_line_spacing", slider=True)
        
        # =====================================================================
        # THEME & COLOR SETTINGS
        # =====================================================================
        
        box = layout.box()
        box.label(text="🎨 Theme & Colors", icon='COLOR')
        
        col = box.column(align=True)
        col.prop(self, "theme_preset")
        
        if self.theme_preset == 'CUSTOM':
            col.separator()
            col.prop(self, "use_custom_colors")
            
            if self.use_custom_colors:
                # Color customization
                color_box = box.box()
                color_box.label(text="Custom Colors", icon='COLORSET_01_VEC')
                
                color_col = color_box.column(align=True)
                color_col.prop(self, "header_color")
                color_col.prop(self, "highlight_color")
                color_col.prop(self, "normal_text_color")
                color_col.prop(self, "secondary_text_color")
                color_col.prop(self, "dim_text_color")
                
                color_col.separator()
                color_col.label(text="Smart Overlay Colors:")
                color_col.prop(self, "smart_text_color")
                color_col.prop(self, "smart_value_color")
        
        # =====================================================================
        # LAYOUT & POSITIONING
        # =====================================================================
        
        box = layout.box()
        box.label(text="📐 Layout & Positioning", icon='OBJECT_ORIGIN')
        
        # Position settings
        pos_row = box.row(align=True)
        pos_col1 = pos_row.column(align=True)
        pos_col1.label(text="Panel Positions:")
        pos_col1.prop(self, "info_panel_position", text="Info Panel")
        pos_col1.prop(self, "tips_panel_position", text="Tips Panel")
        
        pos_col2 = pos_row.column(align=True)
        pos_col2.label(text="Margins:")
        margins_row1 = pos_col2.row(align=True)
        margins_row1.prop(self, "info_panel_margin_x", text="Info X")
        margins_row1.prop(self, "info_panel_margin_y", text="Y")
        margins_row2 = pos_col2.row(align=True)
        margins_row2.prop(self, "tips_panel_margin_x", text="Tips X")
        margins_row2.prop(self, "tips_panel_margin_y", text="Y")
        # Opacity
        box.separator()
        box.prop(self, "overlay_opacity", slider=True)
        
        # =====================================================================
        # PREVIEW & HELP
        # =====================================================================
        
        info_box = layout.box()
        info_col = info_box.column()
        info_col.label(text="💡 Tips:", icon='QUESTION')
        info_col.label(text="• Font Scale: Adjust for your screen resolution (0.5x for large screens, 2.0x+ for small/high-DPI)")
        info_col.label(text="• Themes: Auto-adapt will adjust colors based on Blender's light/dark theme")
        info_col.label(text="• Changes take effect immediately in the 3D viewport")


# Export for registration
__all__ = ['LumiFlowAddonPreferences']

