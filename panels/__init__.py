"""
Panels Module
Contains all panel classes for the LumiFlow Blender addon UI.
"""

import bpy
import inspect
from . import main_panel

# Import all panels for external access
from .main_panel import (
    LUMI_PT_light_control,
)

# Template browser module removed
template_browser_available = False

# Automatically collect all panel classes from main_panel.py that are subclasses of bpy.types.Panel
panel_classes = [
    cls for name, cls in inspect.getmembers(main_panel, inspect.isclass)
    if issubclass(cls, bpy.types.Panel)
]

# Template settings and browser modules removed
template_settings_classes = []
template_browser_classes = []

all_classes = panel_classes + template_settings_classes + template_browser_classes

__all__ = [cls.__name__ for cls in all_classes]

def register():
    """Register all panel classes to Blender."""
    for cls in all_classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {e}")

def unregister():
    """Unregister all panel classes from Blender."""
    for cls in reversed(all_classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {e}")
