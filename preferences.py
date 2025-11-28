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

from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    CollectionProperty,
    IntProperty,
)

logger = logging.getLogger(__name__)

SHORTCUT_KEY_ITEMS = [
    # Alphabet keys A–Z
    ('A', "A", ""),
    ('B', "B", ""),
    ('C', "C", ""),
    ('D', "D", ""),
    ('E', "E", ""),
    ('F', "F", ""),
    ('G', "G", ""),
    ('H', "H", ""),
    ('I', "I", ""),
    ('J', "J", ""),
    ('K', "K", ""),
    ('L', "L", ""),
    ('M', "M", ""),
    ('N', "N", ""),
    ('O', "O", ""),
    ('P', "P", ""),
    ('Q', "Q", ""),
    ('R', "R", ""),
    ('S', "S", ""),
    ('T', "T", ""),
    ('U', "U", ""),
    ('V', "V", ""),
    ('W', "W", ""),
    ('X', "X", ""),
    ('Y', "Y", ""),
    ('Z', "Z", ""),

    # Mouse buttons
    ('LEFTMOUSE', "Left Mouse", ""),
    ('RIGHTMOUSE', "Right Mouse", ""),
    ('MIDDLEMOUSE', "Middle Mouse", ""),
]


class LumiFlowShortcutItem(bpy.types.PropertyGroup):
    """Single LumiFlow shortcut configuration item."""

    action_id: StringProperty(name="Action ID", default="")
    label: StringProperty(name="Label", default="")
    description: StringProperty(name="Description", default="")
    operator: StringProperty(name="Operator", default="")

    key_type: EnumProperty(
        name="Key",
        items=SHORTCUT_KEY_ITEMS,
        default='A',
    )

    key_value: EnumProperty(
        name="Event",
        items=[
            ('PRESS', "Press", ""),
            ('RELEASE', "Release", ""),
        ],
        default='PRESS',
    )

    ctrl: BoolProperty(name="Ctrl", default=False)
    shift: BoolProperty(name="Shift", default=False)
    alt: BoolProperty(name="Alt", default=False)

    active: BoolProperty(name="Active", default=True)


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

    # Shortcut configuration collection
    shortcuts: CollectionProperty(type=LumiFlowShortcutItem)
    shortcuts_index: IntProperty(default=0)

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
        # SHORTCUT SETTINGS
        # =====================================================================

        try:
            from .shortcuts_config import ensure_default_shortcuts
            ensure_default_shortcuts(self)
        except Exception:
            pass

        shortcut_box = layout.box()
        shortcut_col = shortcut_box.column(align=True)
        shortcut_col.label(text="Shortcut Settings", icon='EVENT_A')

        # Guard against missing 'shortcuts' attribute if preferences were
        # registered before the CollectionProperty was available.
        if hasattr(self, "shortcuts"):
            # Header row: Action / Shortcut
            header_row = shortcut_col.row(align=True)
            header_split = header_row.split(factor=0.45, align=True)
            header_left = header_split.row(align=True)
            header_left.label(text="Action")
            header_right = header_split.row(align=True)
            header_right.label(text="Shortcut")

            for item in self.shortcuts:
                row = shortcut_col.row(align=True)
                split = row.split(factor=0.45, align=True)

                # Left column: action label only
                left = split.row(align=True)
                left.label(text=item.label or item.action_id)

                # Right column: key/event + modifiers in a single row
                right = split.row(align=True)
                right.prop(item, "key_type", text="")
                right.prop(item, "key_value", text="")
                right.prop(item, "ctrl", text="Ctrl")
                right.prop(item, "shift", text="Shift")
                right.prop(item, "alt", text="Alt")

            # Small spacer before footer buttons
            shortcut_col.separator()

            # Footer buttons: Apply / Reset
            footer = shortcut_col.row(align=True)
            footer.operator("lumiflow.apply_shortcuts", text="Apply Shortcuts", icon='CHECKMARK')
            footer.operator("lumiflow.reset_shortcuts", text="Reset to Default", icon='LOOP_BACK')
        else:
            info_row = shortcut_col.row()
            info_row.label(text="Shortcut system not initialized (restart Blender or re-enable addon).", icon='ERROR')


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
__all__ = ['LumiFlowAddonPreferences', 'LumiFlowShortcutItem']