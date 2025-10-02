"""
LumiFlow Overlay Configuration
Centralized configuration for overlay system including colors, positions, and settings.
"""

from typing import Dict, Tuple, Any
from mathutils import Vector
import bpy


class OverlayConfig:
    """Centralized configuration for LumiFlow overlay system."""
    
    # Default colors for overlay elements
    DEFAULT_COLORS = {
        'header': (0.0, 0.608, 1.0, 1.0),  # #009bff
        'text': (1.0, 1.0, 1.0, 1.0),
        'highlight': (0.945, 0.941, 0.000, 1.0),  # #f1f000
        'normal': (1.0, 1.0, 1.0, 1.0),
        'secondary': (0.75, 0.75, 0.75, 1.0),
        'dim': (0.6, 0.6, 0.6, 1.0),
        'scroll_text': (1.0, 1.0, 1.0, 1.0),
        'scroll_value': (1.0, 1.0, 0.0, 1.0),
        'error': (1.0, 0.4, 0.4, 1.0)
    }
    
    # Default positions for overlay panels
    DEFAULT_POSITIONS = {
        'info': (10, 10),  # Will be positioned on right side
        'tips': (10, 200)  # Will be positioned on left side
    }
    
    # Light visualization colors
    LIGHT_COLORS = {
        'point': (1.0, 0.5, 0.2, 1.0),
        'spot': (1.0, 0.5, 0.2, 1.0),
        'sun': (1.0, 1.0, 0.0, 1.0),
        'area': (0.2, 1.0, 0.5, 1.0),
        'target': (1.0, 1.0, 1.0, 1.0),
        'selected': (0.0, 0.608, 1.0, 1.0)  # #009bff - same as header
    }
    
    # Drawing settings
    DRAWING_SETTINGS = {
        'circle_segments': 32,
        'line_width': 1,
        'font_size_default': 13,
        'font_size_tips': 12,
        'line_height_default': 18,
        'line_spacing_multiplier': 1.3,
        'tips_spacing_multiplier': 1.2,
        'value_offset_default': 100,
        'value_offset_tips': 100
    }
    
    # Light visualization settings
    LIGHT_SETTINGS = {
        'point_radius': 0.1,
        'spot_radius': 0.1,
        'sun_size': 0.2,
        'area_size': 0.5,
        'target_size': 0.05,
        'plus_sign_size': 0.1
    }
    
    @classmethod
    def get_color(cls, color_name: str, fallback: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)) -> Tuple[float, float, float, float]:
        """Get a color by name with fallback."""
        return cls.DEFAULT_COLORS.get(color_name, fallback)
    
    @classmethod
    def get_light_color(cls, light_type: str, fallback: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)) -> Tuple[float, float, float, float]:
        """Get light visualization color by type."""
        return cls.LIGHT_COLORS.get(light_type.lower(), fallback)
    
    @classmethod
    def get_position(cls, panel_name: str, fallback: Tuple[int, int] = (10, 10)) -> Tuple[int, int]:
        """Get default position for a panel."""
        return cls.DEFAULT_POSITIONS.get(panel_name, fallback)
    
    @classmethod
    def get_drawing_setting(cls, setting_name: str, fallback: Any = None) -> Any:
        """Get a drawing setting by name."""
        return cls.DRAWING_SETTINGS.get(setting_name, fallback)
    
    @classmethod
    def get_light_setting(cls, setting_name: str, fallback: Any = None) -> Any:
        """Get a light visualization setting by name."""
        return cls.LIGHT_SETTINGS.get(setting_name, fallback)
    
    @classmethod
    def get_all_colors(cls) -> Dict[str, Tuple[float, float, float, float]]:
        """Get all default colors."""
        return cls.DEFAULT_COLORS.copy()
    
    @classmethod
    def get_all_light_colors(cls) -> Dict[str, Tuple[float, float, float, float]]:
        """Get all light visualization colors."""
        return cls.LIGHT_COLORS.copy()
    
    @classmethod
    def get_preset_colors(cls, preset_name: str) -> Dict[str, Tuple[float, float, float, float]]:
        """Get color preset by name."""
        presets = {
            'DEFAULT': {
                'header': (0.2, 0.7, 1.0, 1.0),
                'text': (1.0, 1.0, 1.0, 1.0),
                'highlight': (1.0, 0.85, 0.2, 1.0),
                'normal': (1.0, 1.0, 1.0, 1.0),
                'secondary': (0.75, 0.75, 0.75, 1.0),
                'dim': (0.6, 0.6, 0.6, 1.0),
                'scroll_text': (1.0, 1.0, 1.0, 1.0),
                'scroll_value': (1.0, 1.0, 0.0, 1.0)
            },
            'DARK': {
                'header': (0.1, 0.5, 0.8, 1.0),
                'text': (0.9, 0.9, 0.9, 1.0),
                'highlight': (0.9, 0.7, 0.1, 1.0),
                'normal': (0.9, 0.9, 0.9, 1.0),
                'secondary': (0.6, 0.6, 0.6, 1.0),
                'dim': (0.4, 0.4, 0.4, 1.0),
                'scroll_text': (0.9, 0.9, 0.9, 1.0),
                'scroll_value': (0.9, 0.9, 0.0, 1.0)
            },
            'LIGHT': {
                'header': (0.3, 0.6, 0.9, 1.0),
                'text': (0.1, 0.1, 0.1, 1.0),
                'highlight': (0.8, 0.6, 0.1, 1.0),
                'normal': (0.1, 0.1, 0.1, 1.0),
                'secondary': (0.3, 0.3, 0.3, 1.0),
                'dim': (0.5, 0.5, 0.5, 1.0),
                'scroll_text': (0.1, 0.1, 0.1, 1.0),
                'scroll_value': (0.8, 0.8, 0.0, 1.0)
            },
            'HIGH_CONTRAST': {
                'header': (0.0, 1.0, 1.0, 1.0),
                'text': (1.0, 1.0, 1.0, 1.0),
                'highlight': (1.0, 1.0, 0.0, 1.0),
                'normal': (1.0, 1.0, 1.0, 1.0),
                'secondary': (0.8, 0.8, 0.8, 1.0),
                'dim': (0.5, 0.5, 0.5, 1.0),
                'scroll_text': (1.0, 1.0, 1.0, 1.0),
                'scroll_value': (1.0, 1.0, 0.0, 1.0)
            }
        }
        return presets.get(preset_name.upper(), presets['DEFAULT'])


class DrawHandler:
    """Base class for managing Blender draw handlers."""
    
    def __init__(self, draw_func: callable, handler_type: str = 'POST_PIXEL'):
        """
        Initialize draw handler.
        
        Args:
            draw_func: Function to be called for drawing
            handler_type: Type of handler ('POST_PIXEL', 'POST_VIEW', 'PRE_VIEW', etc.)
        """
        self.draw_func = draw_func
        self.handler_type = handler_type
        self.handler = None
        self.is_enabled = False
    
    def enable(self) -> bool:
        """
        Enable the draw handler.
        
        Returns:
            bool: True if successfully enabled, False otherwise
        """
        if self.is_enabled:
            return True
        
        try:
            self.handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_func, (), 'WINDOW', self.handler_type
            )
            self.is_enabled = True
            
            # Tag redraw if region is available
            if hasattr(bpy.context, 'region') and bpy.context.region is not None:
                bpy.context.region.tag_redraw()
            
            return True
        except Exception as e:
            print(f"Error enabling draw handler: {e}")
            return False
    
    def disable(self) -> bool:
        """
        Disable the draw handler.
        
        Returns:
            bool: True if successfully disabled, False otherwise
        """
        if not self.is_enabled or self.handler is None:
            return True
        
        try:
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            self.handler = None
            self.is_enabled = False
            return True
        except Exception as e:
            print(f"Error disabling draw handler: {e}")
            return False
    
    def toggle(self) -> bool:
        """
        Toggle the draw handler on/off.
        
        Returns:
            bool: New state (True if enabled, False if disabled)
        """
        if self.is_enabled:
            self.disable()
            return False
        else:
            return self.enable()
    
    def is_active(self) -> bool:
        """Check if the handler is currently active."""
        return self.is_enabled and self.handler is not None


class OverlayManager:
    """Manager class for handling multiple overlay handlers."""
    
    def __init__(self):
        self.handlers = {}
    
    def register_handler(self, name: str, draw_func: callable, handler_type: str = 'POST_PIXEL') -> DrawHandler:
        """
        Register a new draw handler.
        
        Args:
            name: Unique name for the handler
            draw_func: Function to be called for drawing
            handler_type: Type of handler ('POST_PIXEL', 'POST_VIEW', etc.)
        
        Returns:
            DrawHandler: The created handler instance
        """
        if name in self.handlers:
            print(f"Handler '{name}' already exists. Cleaning up old handler...")
            old_handler = self.handlers[name]
            old_handler.disable()  # Properly disable old handler
        
        handler = DrawHandler(draw_func, handler_type)
        self.handlers[name] = handler
        return handler
    
    def get_handler(self, name: str) -> DrawHandler:
        """Get a registered handler by name."""
        return self.handlers.get(name)
    
    def enable_handler(self, name: str) -> bool:
        """Enable a specific handler by name."""
        handler = self.get_handler(name)
        if handler:
            return handler.enable()
        return False
    
    def disable_handler(self, name: str) -> bool:
        """Disable a specific handler by name."""
        handler = self.get_handler(name)
        if handler:
            return handler.disable()
        return False
    
    def enable_all_handlers(self) -> None:
        """Enable all registered handlers."""
        for handler in self.handlers.values():
            handler.enable()
    
    def disable_all_handlers(self) -> None:
        """Disable all registered handlers."""
        for handler in self.handlers.values():
            handler.disable()
    
    def cleanup(self) -> None:
        """Clean up all handlers."""
        self.disable_all_handlers()
        self.handlers.clear()


# Global overlay manager instance
overlay_manager = OverlayManager()
