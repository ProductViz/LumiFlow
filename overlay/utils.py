"""
Overlay Utilities
Utility functions for overlay drawing, text rendering, and theme management.
"""
# # Import modul utama Blender
import bpy
import blf
import math
from typing import List, Tuple

# Import GPU modules for drawing
import gpu
from gpu_extras.batch import batch_for_shader

# Import konfigurasi terpusat
from .config import OverlayConfig

# Global font ID
_FONT_ID = 0

def _calculate_font_size(scaled_font_size, spacing):
    """Calculate font size based on spacing multiplier."""
    if spacing >= 2.0:
        return int(scaled_font_size * 1.5)
    elif spacing >= 1.8:
        return int(scaled_font_size * 1.3)
    elif spacing >= 1.7:
        return int(scaled_font_size * 1.25)
    elif spacing >= 1.6:
        return int(scaled_font_size * 1.2)
    elif spacing >= 1.5:
        return int(scaled_font_size * 1.1)
    else:
        return scaled_font_size

def _get_font_scale_from_spacing(spacing):
    """Get font scale multiplier from spacing for backward compatibility."""
    if spacing >= 2.0:
        return 1.5
    elif spacing >= 1.8:
        return 1.3
    elif spacing >= 1.7:
        return 1.25
    elif spacing >= 1.6:
        return 1.2
    elif spacing >= 1.5:
        return 1.1
    else:
        return 1.0

def get_text_settings(context: bpy.types.Context) -> Tuple[float, float]:
    """Get font scale and line spacing."""
    ui_scale = context.preferences.view.ui_scale
    addon_prefs = context.preferences.addons.get(__package__.split('.')[0] or "LumiFlow")
    
    if addon_prefs and hasattr(addon_prefs.preferences, 'overlay_font_scale'):
        prefs = addon_prefs.preferences
        font_scale = ui_scale * getattr(prefs, 'overlay_font_scale', 1.0)
        line_spacing = getattr(prefs, 'overlay_line_spacing', 1.0)
    else:
        font_scale = ui_scale
        line_spacing = 1.0
        
    return font_scale, line_spacing

def get_config_colors(context: bpy.types.Context) -> dict:
    """Get colors directly from OverlayConfig without any overrides."""
    return OverlayConfig.get_all_colors()

def get_overlay_positions(context: bpy.types.Context, region) -> tuple:
    """Get overlay panel positions dengan konfigurasi yang sederhana."""
    addon_prefs = context.preferences.addons.get(__package__.split('.')[0] or "LumiFlow")
    if addon_prefs and hasattr(addon_prefs.preferences, 'info_panel_position'):
        prefs = addon_prefs.preferences
        
        # Helper function to calculate x position
        def calc_x_position(is_on_right, panel_width):
            margin = getattr(prefs, 'info_panel_margin_x', 20)
            return (region.width - panel_width - margin) if is_on_right else margin
        
        # Get position settings
        info_on_right = getattr(prefs, 'info_panel_position', 'BOTTOM_RIGHT') in ['BOTTOM_RIGHT', 'TOP_RIGHT']
        tips_on_right = getattr(prefs, 'tips_panel_position', 'BOTTOM_LEFT') in ['BOTTOM_RIGHT', 'TOP_RIGHT']
        
        # Calculate positions using helper function
        margin = getattr(prefs, 'info_panel_margin_x', 20)
        info_x = calc_x_position(info_on_right, 250)
        tips_x = calc_x_position(tips_on_right, 300)
        
        # Y positions
        info_y = margin
        tips_y = margin + 20
        
        return (info_x, info_y), (tips_x, tips_y)
    
    # Use default positions from centralized config
    default_info = OverlayConfig.get_position('info', (region.width - 270, 20))
    default_tips = OverlayConfig.get_position('tips', (20, 20))
    
    # Adjust info position based on region width if needed
    if default_info[0] > region.width - 50:
        info_pos = (region.width - 270, default_info[1])
    else:
        info_pos = default_info
    
    return info_pos, default_tips

def draw_text(
    lines: List[Tuple[str, str, Tuple[float, float, float, float]]],
    position: Tuple[int, int],
    font_scale: float = 1.0,
    line_spacing: float = 1.0,
    font_id: int = 0,
    is_tips: bool = False,
    alignment: str = 'left'  # 'left' or 'right'
) -> None:
    """
    Fungsi tunggal untuk menggambar teks, menggantikan draw_overlay_text dan draw_overlay_tips.
    Menggunakan konfigurasi terpusat dari OverlayConfig.
    
    Args:
        lines: List of tuples dengan format:
               - Legacy: (label, value, color) atau (label, value, color, spacing)
               - New: (label, value, color, spacing_before, spacing_after) atau 
                     (label, value, color, spacing_before, spacing_after, font_scale)
        position: (x, y) starting position
        font_scale: Font size multiplier
        line_spacing: Line spacing multiplier
        font_id: Font ID to use
        is_tips: If True, uses tips styling (smaller font, different spacing)
        alignment: Text alignment ('left' or 'right')
    """
    # Get drawing settings from centralized config
    base_font_size = OverlayConfig.get_drawing_setting(
        'font_size_tips' if is_tips else 'font_size_default'
    )
    base_line_height = OverlayConfig.get_drawing_setting('line_height_default')
    
    # Apply scaling
    spacing_multiplier = OverlayConfig.get_drawing_setting(
        'tips_spacing_multiplier' if is_tips else 'line_spacing_multiplier'
    )
    scaled_font_size = int(base_font_size * font_scale)
    scaled_line_height = int(base_line_height * line_spacing * spacing_multiplier)
    
    # Set font size
    blf.size(font_id, scaled_font_size)
    
    x, y = position
    x_value_offset = OverlayConfig.get_drawing_setting(
        'value_offset_tips' if is_tips else 'value_offset_default'
    )
    
    # Pass 1: collect row spacings and font sizes
    row_spacings = []
    row_font_scales = []
    
    for entry in lines:
        # Parse tuple dengan dukungan backward compatibility
        if len(entry) == 3:
            # Format lama: (label, value, color)
            label, value, color = entry
            spacing_before = 1.0
            spacing_after = 1.0
            font_scale_multiplier = 1.0
        elif len(entry) == 4:
            # Format lama dengan spacing: (label, value, color, spacing)
            label, value, color, spacing = entry
            spacing_before = spacing
            spacing_after = spacing
            # Untuk backward compatibility, gunakan logika font size lama
            font_scale_multiplier = _get_font_scale_from_spacing(spacing)
        elif len(entry) == 5:
            # Format baru: (label, value, color, spacing_before, column_offset)
            label, value, color, spacing_before, column_offset = entry
            font_scale_multiplier = 1.0
        elif len(entry) == 6:
            # Format baru dengan font scale: (label, value, color, spacing_before, column_offset, font_scale)
            label, value, color, spacing_before, column_offset, font_scale_multiplier = entry
        else:
            # Fallback untuk format tidak dikenal
            label, value, color = entry[:3]
            spacing_before = 1.0
            spacing_after = 1.0
            font_scale_multiplier = 1.0
        
        label_lines = label.splitlines()
        value_lines = value.splitlines() if value else []
        
        # Spacing sebelum baris pertama
        row_spacings.append(spacing_before)
        row_font_scales.append(font_scale_multiplier)
        
        # Spacing untuk baris label tambahan (jika multi-line)
        for _ in label_lines[1:]:
            row_spacings.append(0.5)  # Spacing kecil untuk baris lanjutan
            row_font_scales.append(font_scale_multiplier)
        
        # Spacing untuk baris value tambahan (jika multi-line)
        if value_lines:
            for _ in value_lines[1:]:  # Skip first value line (drawn with label)
                row_spacings.append(0.5)  # Spacing kecil untuk baris lanjutan
                row_font_scales.append(font_scale_multiplier)
        
        # Spacing setelah baris terakhir (untuk jarak ke entry berikutnya)
        # Gunakan spacing_before sebagai spacing_after untuk backward compatibility
        row_spacings.append(spacing_before)
        row_font_scales.append(1.0)  # Font scale tidak penting untuk spacing saja
    
    # Pass 2: draw text
    row_idx = 0
    for entry in lines:
        # Parse tuple dengan dukungan backward compatibility
        if len(entry) == 3:
            label, value, color = entry
            font_scale_multiplier = 1.0
            column_offset = None  # Use default offset
        elif len(entry) == 4:
            label, value, color, spacing = entry
            font_scale_multiplier = _get_font_scale_from_spacing(spacing)
            column_offset = None  # Use default offset
        elif len(entry) == 5:
            # Format baru: (label, value, color, spacing_before, column_offset)
            label, value, color, spacing_before, column_offset = entry
            font_scale_multiplier = 1.0
        elif len(entry) == 6:
            # Format baru dengan font scale: (label, value, color, spacing_before, column_offset, font_scale)
            label, value, color, spacing_before, column_offset, font_scale_multiplier = entry
        else:
            label, value, color = entry[:3]
            font_scale_multiplier = 1.0
            column_offset = None  # Use default offset
        
        label_lines = label.splitlines()
        value_lines = value.splitlines() if value else []
        
        for l_idx, line in enumerate(label_lines):
            # Calculate y position
            y_offset = sum(row_spacings[row_idx:]) * scaled_line_height
            current_y = y + y_offset
            
            # Set font size berdasarkan font_scale_multiplier (bukan spacing)
            current_font_size = int(scaled_font_size * row_font_scales[row_idx])
            blf.size(font_id, current_font_size)
            
            # Calculate text width for alignment
            text_width = blf.dimensions(font_id, line)[0]
            
            # Set position based on alignment
            if alignment == 'right':
                draw_x = x - text_width
            else:
                draw_x = x
                
            blf.position(font_id, draw_x, current_y, 0)
            blf.color(font_id, *color)
            blf.draw(font_id, line)
            
            if value and l_idx == 0 and value_lines:
                # Set font size untuk value (gunakan font scale yang sama dengan label)
                current_font_size = int(scaled_font_size * row_font_scales[row_idx])
                blf.size(font_id, current_font_size)
                
                # Check if value contains keymap shortcuts (for icons)
                value_text = value_lines[0]
                # Processing value text for keymap icons
                if ":" in value_text and is_tips:
                    # Split value into description and keymap
                    parts = value_text.split(":", 1)
                    description = parts[0].strip()
                    keymap_text = parts[1].strip() if len(parts) > 1 else ""
                    # Split into description and keymap
                    
                    # Calculate value text width for alignment
                    desc_width = blf.dimensions(font_id, description)[0]
                    
                    # Set value position based on alignment
                    if alignment == 'right':
                        # For right alignment, value goes to the left of label
                        value_x = draw_x - desc_width - int(5 * font_scale)  # 5px spacing
                    else:
                        # For left alignment, value goes to the right of label
                        # Use column_offset if provided, otherwise use default calculation
                        if column_offset is not None:
                            # Direct column offset control
                            value_x = x + int(column_offset * font_scale)
                        else:
                            # Default behavior with configurable offset
                            adjusted_offset = int(x_value_offset * font_scale * 0.75)  # Use 75% of original offset
                            value_x = x + adjusted_offset
                        
                    blf.position(font_id, value_x, current_y, 0)
                    blf.draw(font_id, description)
                    
                    # Draw icons for keymap if available
                    if keymap_text:
                        try:
                            # Lazy import to avoid circular dependencies
                            from .icon_manager import get_icon_manager
                            icon_manager = get_icon_manager()
                            
                            # Calculate icon position
                            icon_x = value_x + desc_width + 5
                            icon_size = icon_manager.get_icon_size()
                            # Align icon with text baseline - raise icons to match text alignment
                            # Use a portion of current font size for better vertical alignment
                            vertical_offset = int(current_font_size * 0.9)  # Raise by 30% of font size
                            icon_y = current_y - icon_size + vertical_offset
                            
                            # About to draw icons for keymap
                            # Icon position calculated
                            # Icon size set
                            # Current font size set
                            
                            # Draw keymap icons
                            icons_width = icon_manager.draw_keymap_icons(keymap_text, icon_x, icon_y)
                            # Icons drawn with total width
                            
                            # Draw remaining text (only parts that don't have icons)
                            # Get the parsed parts from icon manager to know what was drawn as icons
                            remaining_text = keymap_text
                            
                            # Remove all parts that have icons: modifiers, mouse buttons, and letter keys
                            # This list should match what icon_manager.draw_keymap_icons can handle
                            icon_parts = ['Ctrl', 'Shift', 'Alt', 'LMB_Drag', 'MMB_Drag', 'RMB_Drag', 'A', 'C', 'X', 'V', 'D']
                            
                            # Remove each icon part and any associated + signs
                            for part in icon_parts:
                                # Remove the part itself
                                remaining_text = remaining_text.replace(part, '')
                                
                            # Remove + signs and clean up
                            remaining_text = remaining_text.replace('+', '')
                            
                            # Strip any remaining whitespace
                            remaining_text = remaining_text.strip()
                            
                            if remaining_text:
                                text_x = icon_x + icons_width + 5
                                blf.position(font_id, text_x, current_y, 0)
                                blf.draw(font_id, remaining_text)
                        except Exception as e:
                            # Fallback to regular text if icon manager fails
                            print(f"Icon manager error: {e}")
                            fallback_x = value_x + desc_width + 5
                            blf.position(font_id, fallback_x, current_y, 0)
                            blf.draw(font_id, keymap_text)
                else:
                    # Regular value text (no icons)
                    value_width = blf.dimensions(font_id, value_text)[0]
                    
                    # Set value position based on alignment
                    if alignment == 'right':
                        # For right alignment, value goes to the left of label
                        value_x = draw_x - value_width - int(5 * font_scale)  # 5px spacing
                    else:
                        # For left alignment, value goes to the right of label
                        value_x = x + int(x_value_offset * font_scale)
                        
                    blf.position(font_id, value_x, current_y, 0)
                    blf.draw(font_id, value_text)
            row_idx += 1
        
        if value and len(value_lines) > 1:
            for v_idx in range(1, len(value_lines)):
                # Calculate y position for multiline values
                y_offset = sum(row_spacings[row_idx+1:]) * scaled_line_height
                current_y = y + y_offset
                
                # Set font size untuk multi-line value
                current_font_size = int(scaled_font_size * row_font_scales[row_idx])
                blf.size(font_id, current_font_size)
                
                # Calculate value text width for alignment
                value_width = blf.dimensions(font_id, value_lines[v_idx])[0]
                
                # Set value position based on alignment
                if alignment == 'right':
                    # For right alignment, multiline values align to the right
                    value_x = x - value_width
                else:
                    # For left alignment, multiline values align with first value
                    value_x = x + int(x_value_offset * font_scale)
                    
                blf.position(font_id, value_x, current_y, 0)
                blf.color(font_id, *color)
                blf.draw(font_id, value_lines[v_idx])
                row_idx += 1
        
        # Skip spacing_after row (ini hanya untuk spacing, bukan untuk drawing)
        row_idx += 1

# get_info_lines() moved to overlay_info.py - only used by overlay_info module


# Mode management functions moved to utils.mode_manager for centralized system
# Import from there: from ..utils.mode_manager import ModeManager

