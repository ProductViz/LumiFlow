"""
Icon Manager Module
Manages PNG icons for overlay keymap display.
"""
import bpy
import gpu
import os
from gpu_extras.batch import batch_for_shader
from typing import Dict, Optional, Tuple


class IconManager:
    """Manages loading, caching, and drawing of PNG icons for overlay keymaps."""
    
    def __init__(self):
        self.icons: Dict[str, bpy.types.Image] = {}
        self.textures: Dict[str, gpu.types.GPUTexture] = {}
        self.icon_dimensions: Dict[str, Dict[str, int]] = {}  # Store original dimensions
        self.icon_size: int = 14
        self.icon_spacing: int = 1  # Spacing between icons
        self._load_icons()
    
    def _load_icons(self):
        """Load all available icons from assets directory."""
        try:
            # Get addon directory
            addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icons_dir = os.path.join(addon_dir, "assets", "icons")
            
            # Check if icons directory exists
            if not os.path.exists(icons_dir):
                return
            
            # List all files in icons directory
            try:
                icon_files = os.listdir(icons_dir)
            except Exception as e:
                pass
            
            # Define icon mappings
            icon_mappings = {
                # Modifier keys
                'ctrl': 'key_ctrl.png',
                'shift': 'key_shift.png',
                'alt': 'key_alt.png',
                # Mouse buttons
                'lmb_drag': 'lmb_drag.png',
                'mmb_drag': 'mmb_drag.png',
                'rmb_drag': 'rmb_drag.png',
                # Letter keys
                'a': 'key_a.png',
                'x': 'key_x.png',
                'c': 'key_c.png',
                'v': 'key_v.png',
                'd': 'key_d.png',
                # Special keys
                'space': 'key_space.png',
                'enter': 'key_enter.png',
                'tab': 'key_tab.png',
                'esc': 'key_esc.png',
                'delete': 'key_delete.png',
            }
            
            # Load icons
            for icon_name, filename in icon_mappings.items():
                icon_path = os.path.join(icons_dir, filename)
                
                if os.path.exists(icon_path):
                    try:
                        # Load image
                        image = bpy.data.images.load(icon_path, check_existing=True)
                        self.icons[icon_name] = image
                        
                        # Create GPU texture with error handling
                        try:
                            texture = gpu.texture.from_image(image)
                            self.textures[icon_name] = texture
                                
                        except Exception as tex_error:
                            continue
                        
                        # Store original dimensions for aspect ratio calculation
                        if hasattr(image, 'size') and len(image.size) == 2:
                            self.icon_dimensions[icon_name] = {
                                'width': image.size[0],
                                'height': image.size[1]
                            }
                        else:
                            # Fallback to standard size
                            self.icon_dimensions[icon_name] = {
                                'width': self.icon_size,
                                'height': self.icon_size
                            }
                    except Exception as e:
                        pass
                else:
                    pass
                    
        except Exception as e:
            pass
    
    def get_icon_size(self) -> int:
        """Get the default icon size."""
        return self.icon_size
    
    def draw_icon(self, icon_name: str, x: int, y: int, size: Optional[int] = None):
        """Draw a single icon at the specified position."""
        if icon_name not in self.textures:
            return
        
        # Get texture first
        texture = self.textures[icon_name]
        
        # Get shader - using Blender's built-in IMAGE shader
        shader = gpu.shader.from_builtin('IMAGE')
        
        icon_size = size or self.icon_size
        
        # Calculate proportional dimensions based on aspect ratio
        if icon_name in self.icon_dimensions:
            orig_width = self.icon_dimensions[icon_name]['width']
            orig_height = self.icon_dimensions[icon_name]['height']
            
            if orig_width > 0 and orig_height > 0:
                # Calculate aspect ratio
                aspect_ratio = orig_width / orig_height
                
                # Calculate dimensions maintaining aspect ratio
                # CONSISTENT HEIGHT: All icons have the same height, width is adjusted
                draw_height = icon_size  # All icons have the same height
                draw_width = int(icon_size * aspect_ratio)  # Width adjusted by aspect ratio
                
                # Optional: Limit maximum width for very wide icons
                max_width = icon_size * 2  # Maximum 2x the height
                if draw_width > max_width:
                    draw_width = max_width
                    
            else:
                # Fallback to square if invalid dimensions
                draw_width = icon_size
                draw_height = icon_size
        else:
            # Fallback to square if no dimension data
            draw_width = icon_size
            draw_height = icon_size
        
        # Define vertices for the icon rectangle - using Blender's standard clockwise order
        # Based on Blender's official documentation: ((100, 100), (200, 100), (200, 200), (100, 200))
        pos = (
            (x, y),                           # bottom-left
            (x + draw_width, y),               # bottom-right
            (x + draw_width, y + draw_height), # top-right
            (x, y + draw_height)              # top-left
        )
        
        # Use Blender's standard texture coordinates from official documentation
        # Based on Blender example: ((0, 0), (1, 0), (1, 1), (0, 1))
        texCoord = (
            (0, 0),  # bottom-left
            (1, 0),  # bottom-right
            (1, 1),  # top-right
            (0, 1)   # top-left
        )
        
        # Create batch for drawing
        batch = batch_for_shader(
            shader,
            'TRI_FAN',
            {
                "pos": pos,
                "texCoord": texCoord,
            },
        )
        
        # Enable alpha blending for transparent icons
        gpu.state.blend_set('ALPHA')
        
        # Draw the icon - following Blender's official example
        shader.bind()
        shader.uniform_sampler("image", texture)
        batch.draw(shader)
        
        # Restore blend state
        gpu.state.blend_set('NONE')
    
    def draw_keymap_icons(self, keymap_text: str, start_x: int, start_y: int) -> int:
        """
        Draw icons for a keymap string and return the total width used.
        
        Args:
            keymap_text: String like "Ctrl + Shift + MMB Drag"
            start_x: Starting X position
            start_y: Starting Y position
            
        Returns:
            Total width used by icons and spacing
        """
        # Processing keymap text for icons
        
        if not keymap_text:
            return 0
        
        current_x = start_x
        icon_spacing = 4
        plus_spacing = 8
        
        # Parse keymap text and draw corresponding icons
        parts = keymap_text.split('+')
        # Split keymap text into parts
        
        valid_parts = []
        for i, part in enumerate(parts):
            part = part.strip()
            # Processing keymap part
            
            # Skip empty parts
            if not part:
                # Skipping empty part
                continue
                
            # Check if this is a valid keymap part (not just "Drag" text)
            part_lower = part.lower()
            # Skip only if it's exactly "drag" or ends with " drag" (with space)
            if part_lower == 'drag' or part_lower.endswith(' drag'):
                # Skipping drag part
                continue
            # Don't skip LMB_Drag, MMB_Drag, RMB_Drag - these are valid mouse button icons
            elif part_lower in ['lmb_drag', 'mmb_drag', 'rmb_drag']:
                # Valid mouse button drag
                pass
            # Skip other drag variations that aren't mouse buttons
            elif '_drag' in part_lower and part_lower not in ['lmb_drag', 'mmb_drag', 'rmb_drag']:
                # Skipping non-mouse drag part
                continue
                
            valid_parts.append(part)
            # Valid keymap part
        
        # Valid parts to process
        
        for i, part in enumerate(valid_parts):
            
            # Determine which icon to draw
            icon_name = None
            part_lower = part.lower()
            
            # Modifier keys
            if 'ctrl' in part_lower:
                icon_name = 'ctrl'
            elif 'shift' in part_lower:
                icon_name = 'shift'
            elif 'alt' in part_lower:
                icon_name = 'alt'
            # Mouse buttons - support both old and new formats
            elif part_lower in ['lmb', 'lmb_drag']:
                icon_name = 'lmb_drag'
            elif part_lower in ['mmb', 'mmb_drag']:
                icon_name = 'mmb_drag'
            elif part_lower in ['rmb', 'rmb_drag']:
                icon_name = 'rmb_drag'
            # Letter keys
            elif part_lower in ['a', 'x', 'c', 'v', 'd']:
                icon_name = part_lower
            # Special keys
            elif 'space' in part_lower:
                icon_name = 'space'
            elif 'enter' in part_lower:
                icon_name = 'enter'
            elif 'tab' in part_lower:
                icon_name = 'tab'
            elif 'esc' in part_lower:
                icon_name = 'esc'
            elif 'delete' in part_lower:
                icon_name = 'delete'
            
            # Part mapped to icon
            
            # Draw icon if found
            if icon_name:
                # Drawing icon at calculated position
                self.draw_icon(icon_name, current_x, start_y)
                
                # Get actual width of this icon
                actual_width = self.get_icon_width(icon_name)
                current_x += actual_width + icon_spacing
                # Icon width calculated and position updated
                
                # Add spacing between icons instead of drawing + sign
                if i < len(valid_parts) - 1:
                    # Just add configurable spacing
                    current_x += self.icon_spacing
        
        return current_x - start_x
    
    def get_icon_width(self, icon_name: str, size: Optional[int] = None) -> int:
        """Get the actual width of an icon based on its aspect ratio."""
        icon_size = size or self.icon_size
        
        if icon_name in self.icon_dimensions:
            orig_width = self.icon_dimensions[icon_name]['width']
            orig_height = self.icon_dimensions[icon_name]['height']
            
            if orig_width > 0 and orig_height > 0:
                aspect_ratio = orig_width / orig_height
                # CONSISTENT HEIGHT: All icons have the same height, width is adjusted
                draw_width = int(icon_size * aspect_ratio)  # Width adjusted by aspect ratio
                
                # Optional: Limit maximum width for very wide icons
                max_width = icon_size * 2  # Maximum 2x the height
                if draw_width > max_width:
                    draw_width = max_width
                    
                return draw_width
        
        return icon_size  # Fallback
    
    def get_icon_size(self) -> int:
        """Get the current icon size."""
        return self.icon_size
    
    def set_icon_size(self, size: int):
        """Set the icon size."""
        self.icon_size = max(12, min(32, size))  # Clamp between 12 and 32 pixels
    
    def cleanup(self):
        """Clean up GPU textures and other resources."""
        for texture in self.textures.values():
            try:
                texture.free()
            except:
                pass
        
        self.icons.clear()
        self.textures.clear()


# Global icon manager instance
_icon_manager: Optional[IconManager] = None


def get_icon_manager() -> IconManager:
    """Get the global icon manager instance."""
    global _icon_manager
    if _icon_manager is None:
        _icon_manager = IconManager()
    return _icon_manager


def cleanup_icon_manager():
    """Clean up the global icon manager."""
    global _icon_manager
    if _icon_manager is not None:
        _icon_manager.cleanup()
        _icon_manager = None

