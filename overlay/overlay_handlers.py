"""
Overlay Handlers Module
Contains draw handler management and scene update functions.
"""

import bpy
from .config import overlay_manager

# Global handlers (deprecated - using overlay_manager now)
_lumi_draw_handler = None
_lumi_overlay_draw_handler = None
_lumi_stroke_overlay_handler = None
_lumi_tips_overlay_handler = None
_lumi_cursor_overlay_handler = None

_overlay_needs_reinit = True
_overlay_reinit_count = 0

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _safe_remove_handler(handler_var):
    """Safely remove a draw handler."""
    if handler_var is not None:
        bpy.types.SpaceView3D.draw_handler_remove(handler_var, 'WINDOW')
        return None
    return handler_var

def _safe_add_handler(func, mode):
    """Safely add a draw handler."""
    return bpy.types.SpaceView3D.draw_handler_add(func, (), 'WINDOW', mode)

# ============================================================================
# DRAW HANDLERS - Refactored to use DrawHandler class
# ============================================================================

def lumi_enable_draw_handler(): 
    """Enable light lines drawing handler using DrawHandler."""
    global _lumi_draw_handler
    if _lumi_draw_handler is None:
        _lumi_draw_handler = overlay_manager.register_handler(
            'light_lines', lumi_draw_light_lines, 'POST_VIEW'
        )
        _lumi_draw_handler.enable()
    else:
        _lumi_draw_handler.enable()

def lumi_disable_draw_handler():
    """Disable light lines drawing handler."""
    global _lumi_draw_handler
    if _lumi_draw_handler:
        _lumi_draw_handler.disable()
        _lumi_draw_handler = None

def lumi_enable_overlay_draw_handler():
    """Enable overlay info drawing handler using DrawHandler."""
    global _lumi_overlay_draw_handler
    if _lumi_overlay_draw_handler is None:
        _lumi_overlay_draw_handler = overlay_manager.register_handler(
            'overlay_info', draw_overlay_info, 'POST_PIXEL'
        )
        _lumi_overlay_draw_handler.enable()
    else:
        _lumi_overlay_draw_handler.enable()

def lumi_disable_overlay_draw_handler():
    """Disable overlay info drawing handler."""
    global _lumi_overlay_draw_handler
    if _lumi_overlay_draw_handler:
        _lumi_overlay_draw_handler.disable()
        _lumi_overlay_draw_handler = None


def lumi_enable_stroke_overlay_handler():
    """Enable stroke overlay drawing handler using DrawHandler."""
    global _lumi_stroke_overlay_handler
    if _lumi_stroke_overlay_handler is None:
        _lumi_stroke_overlay_handler = overlay_manager.register_handler(
            'stroke_overlay', lumi_draw_stroke_overlay, 'POST_VIEW'
        )
        _lumi_stroke_overlay_handler.enable()
    else:
        _lumi_stroke_overlay_handler.enable()

def lumi_disable_stroke_overlay_handler():
    """Disable stroke overlay drawing handler."""
    global _lumi_stroke_overlay_handler
    if _lumi_stroke_overlay_handler is not None:
        _lumi_stroke_overlay_handler.disable()

def lumi_enable_tips_overlay_handler():
    """Enable tips overlay drawing handler using DrawHandler."""
    global _lumi_tips_overlay_handler
    if _lumi_tips_overlay_handler is None:
        _lumi_tips_overlay_handler = overlay_manager.register_handler(
            'tips_overlay', lumi_draw_tips_overlay, 'POST_PIXEL'
        )
        _lumi_tips_overlay_handler.enable()
    else:
        _lumi_tips_overlay_handler.enable()

def lumi_disable_tips_overlay_handler():
    """Disable tips overlay drawing handler."""
    global _lumi_tips_overlay_handler
    if _lumi_tips_overlay_handler is not None:
        _lumi_tips_overlay_handler.disable()

def lumi_enable_cursor_overlay_handler():
    """Enable cursor overlay drawing handler using DrawHandler."""
    global _lumi_cursor_overlay_handler
    if _lumi_cursor_overlay_handler is None:
        _lumi_cursor_overlay_handler = overlay_manager.register_handler(
            'cursor_overlay', lumi_draw_cursor_overlay, 'POST_PIXEL'
        )
        _lumi_cursor_overlay_handler.enable()
    else:
        _lumi_cursor_overlay_handler.enable()

def lumi_disable_cursor_overlay_handler():
    """Disable cursor overlay drawing handler."""
    global _lumi_cursor_overlay_handler
    if _lumi_cursor_overlay_handler is not None:
        _lumi_cursor_overlay_handler.disable()

# ============================================================================
# SCENE UPDATE HANDLERS
# ============================================================================
def debug_overlay_status():
    """Debug function to check overlay status"""
    pass

def lumi_scene_update_handler(scene, depsgraph):
    """Main scene update handler for managing all drawing handlers."""
    global _overlay_needs_reinit, _overlay_reinit_count
    
    from ..utils import lumi_is_addon_enabled
    if not lumi_is_addon_enabled():
        lumi_disable_draw_handler()
        lumi_disable_overlay_draw_handler()
        lumi_disable_stroke_overlay_handler()
        lumi_disable_tips_overlay_handler()
        lumi_disable_cursor_overlay_handler()
        return
    
    if _overlay_needs_reinit:
        _overlay_reinit_count += 1
        if _overlay_reinit_count > 5:
            _overlay_needs_reinit = False
            _overlay_reinit_count = 0
            return
        
        lumi_enable_draw_handler()
        lumi_enable_overlay_draw_handler()
        lumi_enable_stroke_overlay_handler()
        lumi_enable_tips_overlay_handler()
        lumi_enable_cursor_overlay_handler()
        
        _overlay_needs_reinit = False
        _overlay_reinit_count = 0
        return
    
    
    selected_lights = [obj for obj in scene.objects if obj.select_get() and obj.type == 'LIGHT']
    if selected_lights:
        lumi_enable_draw_handler()
        lumi_enable_overlay_draw_handler()
    else:
        lumi_enable_draw_handler()
        lumi_enable_overlay_draw_handler()
    
    lumi_enable_tips_overlay_handler()
    lumi_enable_cursor_overlay_handler()
    
    
    if scene.render.engine == 'CYCLES' or scene.render.engine == 'EEVEE':
        light_objects = [obj for obj in scene.objects if obj.type == 'LIGHT']
        if not light_objects:
            lumi_enable_stroke_overlay_handler()
        else:
            lumi_disable_stroke_overlay_handler()
    else:
        lumi_disable_stroke_overlay_handler()

# Import functions from other modules for handler compatibility
from .overlay_light import lumi_draw_light_lines
from .overlay_info import draw_overlay_info
from .overlay_mesh import _draw_scene_object_strokes_if_no_lights
from .overlay_tips import draw_overlay_tips
from .overlay_cursor import draw_overlay_cursor

def lumi_draw_stroke_overlay():
    """Wrapper function for stroke overlay drawing."""
    _draw_scene_object_strokes_if_no_lights()

def lumi_draw_tips_overlay():
    """Wrapper function for tips overlay drawing."""
    draw_overlay_tips()

def lumi_draw_cursor_overlay():
    """Wrapper function for cursor overlay drawing."""
    draw_overlay_cursor()

