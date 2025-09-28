"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

For licensing inquiries: asqa3d@gmail.com
"""

# Import state management for backward compatibility
from .state import get_state
import warnings

# Legacy accessors (deprecated, will be removed in v2.0)
# These functions are kept for backward compatibility only
def get_scroll_control_enabled():
    """Deprecated: Use get_state().scroll_control_enabled"""
    warnings.warn(
        "get_scroll_control_enabled() is deprecated and will be removed in v2.0. "
        "Use get_state().scroll_control_enabled instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().scroll_control_enabled

def get_scroll_operator_instance():
    """Deprecated: Use get_state().modal_operators['scroll']"""
    warnings.warn(
        "get_scroll_operator_instance() is deprecated and will be removed in v2.0. "
        "Use get_state().modal_operators['scroll'] instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().modal_operators.get('scroll')

def get_last_selected_lights():
    """Deprecated: Use get_state().last_selected_lights"""
    warnings.warn(
        "get_last_selected_lights() is deprecated and will be removed in v2.0. "
        "Use get_state().last_selected_lights instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().last_selected_lights

def get_rotate_modal_active():
    """Deprecated: Use get_state().modal_states['rotate']"""
    warnings.warn(
        "get_rotate_modal_active() is deprecated and will be removed in v2.0. "
        "Use get_state().modal_states['rotate'] instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().modal_states.get('rotate', False)

def get_target_modal_active():
    """Deprecated: Use get_state().modal_states['target']"""
    warnings.warn(
        "get_target_modal_active() is deprecated and will be removed in v2.0. "
        "Use get_state().modal_states['target'] instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().modal_states.get('target', False)

def get_align_modal_active():
    """Deprecated: Use get_state().modal_states['align']"""
    warnings.warn(
        "get_align_modal_active() is deprecated and will be removed in v2.0. "
        "Use get_state().modal_states['align'] instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().modal_states.get('align', False)

def get_highlight_modal_active():
    """Deprecated: Use get_state().modal_states['highlight']"""
    warnings.warn(
        "get_highlight_modal_active() is deprecated and will be removed in v2.0. "
        "Use get_state().modal_states['highlight'] instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_state().modal_states.get('highlight', False)

# TODO: Remove all legacy accessors in v2.0

