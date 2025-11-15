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
import logging

logger = logging.getLogger(__name__)

class LumiFlowAddonPreferences(bpy.types.AddonPreferences):
    """Addon preferences for LumiFlow, allowing users to customize keymaps and UI options."""
    bl_idname = __package__ or "LumiFlow"

    
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
    
    overlay_keymap_display_mode: bpy.props.EnumProperty(
        name="Keymap Display Mode",
        description="Choose how keyboard shortcuts are displayed in overlay tips",
        items=[
            ('ICONS', "Icons", "Display keyboard shortcuts as visual icons (recommended for better readability)", 'IMAGE_DATA', 0),
            ('TEXT', "Text", "Display keyboard shortcuts as plain text", 'FONT_DATA', 1),
        ],
        default='ICONS',
        update=lambda self, context: self.force_viewport_redraw()
    )

    # Studio & Commercial template category visibility
    studio_commercial_show_apparel: bpy.props.BoolProperty(
        name="Apparel",
        description="Show apparel-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_automotive: bpy.props.BoolProperty(
        name="Automotive",
        description="Show automotive-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_cosmetics: bpy.props.BoolProperty(
        name="Cosmetics",
        description="Show cosmetics-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_electronics: bpy.props.BoolProperty(
        name="Electronics",
        description="Show electronics-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_food: bpy.props.BoolProperty(
        name="Food",
        description="Show food-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_furniture: bpy.props.BoolProperty(
        name="Furniture",
        description="Show furniture-specific Studio & Commercial templates",
        default=True,
    )

    studio_commercial_show_jewelry: bpy.props.BoolProperty(
        name="Jewelry",
        description="Show jewelry-specific Studio & Commercial templates",
        default=True,
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
        except Exception as e:
            logger.debug(f"Cannot redraw viewports: {e}")

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        
        # Header
        header = layout.row()
        header.label(text="LumiFlow Overlay Customization", icon='PREFERENCES')
        
        
        # =====================================================================
        # DISPLAY & FONT SETTINGS
        # =====================================================================
        
        box = layout.box()
        
        col = box.column(align=True)
        
        # Display Scale - Label and slider in one row with wider slider
        split = col.split(factor=0.40, align=True)
        split.label(text="Display Scale:")
        row = split.row(align=True)
        row.prop(self, "overlay_display_scale", slider=True, text="")
        
        col.separator()
        
        # =====================================================================
        # KEYMAP DISPLAY MODE
        # =====================================================================
        
        # Keymap Display Mode - Label and buttons in one row
        split = col.split(factor=0.60, align=True)
        split.label(text="Keymap Display:")
        row = split.row(align=True)
        row.prop(self, "overlay_keymap_display_mode", expand=True)
        
        
        
        # =====================================================================
        # STUDIO & COMMERCIAL TEMPLATE CATEGORIES
        # =====================================================================
        
        box_sc = layout.box()
        col_sc = box_sc.column(align=True)
        col_sc.label(text="Studio & Commercial Categories")

        split_sc = col_sc.split(factor=0.5, align=True)
        col_left = split_sc.column(align=True)
        col_right = split_sc.column(align=True)

        # Left column (4 items)
        col_left.prop(self, "studio_commercial_show_apparel")
        col_left.prop(self, "studio_commercial_show_automotive")
        col_left.prop(self, "studio_commercial_show_cosmetics")
        col_left.prop(self, "studio_commercial_show_electronics")

        # Right column (3 items)
        col_right.prop(self, "studio_commercial_show_food")
        col_right.prop(self, "studio_commercial_show_furniture")
        col_right.prop(self, "studio_commercial_show_jewelry")

        # =====================================================================
        # PREVIEW & HELP
        # =====================================================================
        
        info_box = layout.box()
        info_col = info_box.column()
        info_col.label(text="💡 Tips:", icon='QUESTION')
        info_col.label(text="• Display Scale: Adjust for your screen resolution (0.3x for large screens, 2.0x+ for small/high-DPI)")
        info_col.label(text="• Controls both font size and line spacing proportionally")
        info_col.label(text="• Keymap Display: Icons mode shows visual keyboard icons, Text mode shows plain text shortcuts")
        info_col.label(text="• Changes take effect immediately in the 3D viewport")


# Export for registration
__all__ = ['LumiFlowAddonPreferences']