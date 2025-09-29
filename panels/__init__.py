"""
LumiFlow Panels Module
Contains all panel classes for the LumiFlow Blender addon UI.
"""

# # Import modul utama Blender
import bpy
import inspect
# # Import dari modul lokal addon
from . import main_panel

# Import semua panel untuk external access
from .main_panel import (
    LUMI_PT_light_control,
)

# Template browser module removed
template_browser_available = False

# Otomatis kumpulkan semua kelas panel dari main_panel.py yang merupakan subclass dari bpy.types.Panel
panel_classes = [
    cls for name, cls in inspect.getmembers(main_panel, inspect.isclass)
    if issubclass(cls, bpy.types.Panel)
]

# Template settings and browser modules removed
template_settings_classes = []
template_browser_classes = []

# Gabungkan semua kelas
all_classes = panel_classes + template_settings_classes + template_browser_classes

# Export untuk backward compatibility
__all__ = [cls.__name__ for cls in all_classes]

# # Fungsi untuk mendaftarkan class ke Blender
def register():
    for cls in all_classes:
        # # Coba eksekusi kode dengan error handling
        try:
            # # Daftarkan class ke sistem Blender
            bpy.utils.register_class(cls)
        # # Tangani error jika terjadi
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {e}")

# # Fungsi untuk membatalkan pendaftaran class
def unregister():
    for cls in reversed(all_classes):
        # # Coba eksekusi kode dengan error handling
        try:
            # # Batalkan pendaftaran class
            bpy.utils.unregister_class(cls)
        # # Tangani error jika terjadi
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {e}")
