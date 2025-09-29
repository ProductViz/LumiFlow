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
        self.icon_dimensions: Dict[str, Dict[str, int]] = {}
        self.icon_size: int = 14
        self.icon_spacing: int = 1
        self._load_icons()
    
    def _load_icons(self):
        """Load all available icons from assets directory."""
        try:
            addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icons_dir = os.path.join(addon_dir, "assets", "icons")
            
            if not os.path.exists(icons_dir):
                return
            
            try:
                icon_files = os.listdir(icons_dir)
            except Exception:
                pass
            
            icon_mappings = {
                'ctrl': 'key_ctrl.png',
                'shift': 'key_shift.png',
                'alt': 'key_alt.png',
                'lmb_drag': 'lmb_drag.png',
                'mmb_drag': 'mmb_drag.png',
                'rmb_drag': 'rmb_drag.png',
                'a': 'key_a.png',
                'x': 'key_x.png',
                'c': 'key_c.png',
                'v': 'key_v.png',
                'd': 'key_d.png',
                'space': 'key_space.png',
                'enter': 'key_enter.png',
                'tab': 'key_tab.png',
                'esc': 'key_esc.png',
                'delete': 'key_delete.png',
            }
            
            for icon_name, filename in icon_mappings.items():
                icon_path = os.path.join(icons_dir, filename)
                
                if os.path.exists(icon_path):
                    try:
                        image = bpy.data.images.load(icon_path, check_existing=True)
                        self.icons[icon_name] = image
                        
                        try:
                            texture = gpu.texture.from_image(image)
                            self.textures[icon_name] = texture
                        except Exception:
                            continue
                        
                        if hasattr(image, 'size') and len(image.size) == 2:
                            self.icon_dimensions[icon_name] = {
                                'width': image.size[0],
                                'height': image.size[1]
                            }
                        else:
                            self.icon_dimensions[icon_name] = {
                                'width': self.icon_size,
                                'height': self.icon_size
                            }
                    except Exception:
                        pass
                else:
                    pass
                    
        except Exception:
            pass
    
    def get_icon_size(self) -> int:
        """Get the default icon size."""
        return self.icon_size
    
    def draw_icon(self, icon_name: str, x: int, y: int, size: Optional[int] = None):
        if icon_name not in self.textures:
            return
        
        texture = self.textures[icon_name]
        shader = gpu.shader.from_builtin('IMAGE')
        
        icon_size = size or self.icon_size
        
        if icon_name in self.icon_dimensions:
            orig_width = self.icon_dimensions[icon_name]['width']
            orig_height = self.icon_dimensions[icon_name]['height']
            
            if orig_width > 0 and orig_height > 0:
                aspect_ratio = orig_width / orig_height
                draw_height = icon_size
                draw_width = int(icon_size * aspect_ratio)
                
                max_width = icon_size * 2
                if draw_width > max_width:
                    draw_width = max_width
            else:
                draw_width = icon_size
                draw_height = icon_size
        else:
            draw_width = icon_size
            draw_height = icon_size
        
        pos = (
            (x, y),
            (x + draw_width, y),
            (x + draw_width, y + draw_height),
            (x, y + draw_height)
        )
        
        texCoord = (
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        )
        
        batch = batch_for_shader(
            shader,
            'TRI_FAN',
            {
                "pos": pos,
                "texCoord": texCoord,
            },
        )
        
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_sampler("image", texture)
        batch.draw(shader)
        
        gpu.state.blend_set('NONE')
    
    def draw_keymap_icons(self, keymap_text: str, start_x: int, start_y: int) -> int:
        """
        Draw icons for a keymap string and return the total width used.
{{ ... }}
        Args:
            keymap_text: String like "Ctrl + Shift + MMB Drag"
            start_x: Starting X position
            start_y: Starting Y position
            
        Returns:
            Total width used by icons and spacing
        """
        if not keymap_text:
            return 0
        
        current_x = start_x
        icon_spacing = 4
        plus_spacing = 8
        
        parts = keymap_text.split('+')
        
        valid_parts = []
        for i, part in enumerate(parts):
            part = part.strip()
            
            if not part:
                continue
                
            part_lower = part.lower()
            if part_lower == 'drag' or part_lower.endswith(' drag'):
                continue
            elif part_lower in ['lmb_drag', 'mmb_drag', 'rmb_drag']:
                pass
            elif '_drag' in part_lower and part_lower not in ['lmb_drag', 'mmb_drag', 'rmb_drag']:
                continue
                
            valid_parts.append(part)
        
        for i, part in enumerate(valid_parts):
            icon_name = None
            part_lower = part.lower()
            
            if 'ctrl' in part_lower:
                icon_name = 'ctrl'
            elif 'shift' in part_lower:
                icon_name = 'shift'
            elif 'alt' in part_lower:
                icon_name = 'alt'
            elif part_lower in ['lmb', 'lmb_drag']:
                icon_name = 'lmb_drag'
            elif part_lower in ['mmb', 'mmb_drag']:
                icon_name = 'mmb_drag'
            elif part_lower in ['rmb', 'rmb_drag']:
                icon_name = 'rmb_drag'
            elif part_lower in ['a', 'x', 'c', 'v', 'd']:
                icon_name = part_lower
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
            
            if icon_name:
                self.draw_icon(icon_name, current_x, start_y)
                
                actual_width = self.get_icon_width(icon_name)
                current_x += actual_width + icon_spacing
                
                if i < len(valid_parts) - 1:
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
                draw_width = int(icon_size * aspect_ratio)
                
                max_width = icon_size * 2
                if draw_width > max_width:
                    draw_width = max_width
                    
                return draw_width
        
        return icon_size  # Fallback
    
    def get_icon_size(self) -> int:
        """Get the current icon size."""
        return self.icon_size
    
    def set_icon_size(self, size: int):
        """Set the icon size."""
        self.icon_size = max(12, min(32, size))
    
    def cleanup(self):
        """Clean up GPU textures and other resources."""
        for texture in self.textures.values():
            try:
                texture.free()
            except Exception:
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

