

# Import positioning-specific utilities
from .utils import *

# Import semua positioning operators (updated after refactoring)
from .highlight_ops import LUMI_OT_highlight_positioning
from .normal_ops import LUMI_OT_normal_positioning
from .target_ops import LUMI_OT_target_positioning
from .orbit_ops import LUMI_OT_orbit_positioning, LUMI_OT_orbit_angles
from .free_ops import LUMI_OT_free_positioning
from .move import LUMI_OT_move_positioning

# Import flip operators
from .flip_ops import (
    LUMI_OT_flip_to_camera_front,
    LUMI_OT_flip_to_camera_back,
    LUMI_OT_flip_to_camera_along,
    LUMI_OT_flip_across_pivot,
    LUMI_OT_flip_horizontal,
    LUMI_OT_flip_vertical,
    LUMI_OT_flip_180_degrees
)

# Import __all__ from utils
from .utils import __all__ as utils_all

# Export semua positioning components
__all__ = [
    # Positioning utilities
    *utils_all,
    
    # Highlight operators
    'LUMI_OT_highlight_positioning',
    
    # Normal operators (dulu align)
    'LUMI_OT_normal_positioning',
    
    # Target operators
    'LUMI_OT_target_positioning',
    
    # Orbit operators (dulu rotate)
    'LUMI_OT_orbit_positioning',
    'LUMI_OT_orbit_angles',
    
    # Free positioning operators
    'LUMI_OT_free_positioning',
    
    # Move positioning operators
    'LUMI_OT_move_positioning',
    
    # Flip operators
    'LUMI_OT_flip_to_camera_front',
    'LUMI_OT_flip_to_camera_back',
    'LUMI_OT_flip_to_camera_along',
    'LUMI_OT_flip_across_pivot',
    'LUMI_OT_flip_horizontal',
    'LUMI_OT_flip_vertical',
    'LUMI_OT_flip_180_degrees'
]


def register():
    """Register all positioning operators"""
    try:
        # Register all positioning operators
        bpy.utils.register_class(LUMI_OT_highlight_positioning)
        bpy.utils.register_class(LUMI_OT_normal_positioning)
        bpy.utils.register_class(LUMI_OT_orbit_positioning)
        bpy.utils.register_class(LUMI_OT_target_positioning)
        bpy.utils.register_class(LUMI_OT_free_positioning)
        bpy.utils.register_class(LUMI_OT_move_positioning)
        
        # Register orbit angles operator (unchanged)
        bpy.utils.register_class(LUMI_OT_orbit_angles)
        
        # Register flip operators
        bpy.utils.register_class(LUMI_OT_flip_to_camera_front)
        bpy.utils.register_class(LUMI_OT_flip_to_camera_back)
        bpy.utils.register_class(LUMI_OT_flip_to_camera_along)
        bpy.utils.register_class(LUMI_OT_flip_across_pivot)
        bpy.utils.register_class(LUMI_OT_flip_horizontal)
        bpy.utils.register_class(LUMI_OT_flip_vertical)
        
        pass
        
    except Exception as e:
        pass


def unregister():
    """Unregister all positioning operators"""
    try:
        # Unregister all positioning operators
        bpy.utils.unregister_class(LUMI_OT_highlight_positioning)
        bpy.utils.unregister_class(LUMI_OT_normal_positioning)
        bpy.utils.unregister_class(LUMI_OT_orbit_positioning)
        bpy.utils.unregister_class(LUMI_OT_target_positioning)
        bpy.utils.unregister_class(LUMI_OT_free_positioning)
        bpy.utils.unregister_class(LUMI_OT_move_positioning)
        
        # Unregister orbit angles operator (unchanged)
        bpy.utils.unregister_class(LUMI_OT_orbit_angles)
        
        # Unregister flip operators
        bpy.utils.unregister_class(LUMI_OT_flip_to_camera_front)
        bpy.utils.unregister_class(LUMI_OT_flip_to_camera_back)
        bpy.utils.unregister_class(LUMI_OT_flip_to_camera_along)
        bpy.utils.unregister_class(LUMI_OT_flip_across_pivot)
        bpy.utils.unregister_class(LUMI_OT_flip_horizontal)
        bpy.utils.unregister_class(LUMI_OT_flip_vertical)
        
        pass
        
    except Exception as e:
        pass



