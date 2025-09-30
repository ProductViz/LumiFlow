"""
Core Module
Contains core functionality for state management and global variables used throughout LumiFlow.
"""
from .state import get_state, LumiFlowState
from .globals import (
    get_scroll_control_enabled,
    get_scroll_operator_instance,
    get_last_selected_lights,
    get_rotate_modal_active,
    get_target_modal_active,
    get_align_modal_active,
    get_highlight_modal_active
)

__all__ = [
    'get_state', 
    'LumiFlowState',
    'get_scroll_control_enabled',
    'get_scroll_operator_instance',
    'get_last_selected_lights',
    'get_rotate_modal_active',
    'get_target_modal_active',
    'get_align_modal_active',
    'get_highlight_modal_active'
]
