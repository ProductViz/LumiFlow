# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
"""
LumiFlow Positioning Utilities
Contains specialized utilities only used within positioning operators.
"""

# # Import modul utama Blender
import bpy
from mathutils import Vector

# Import state management
from ...core.state import get_state
from ...utils import lumi_is_addon_enabled


def lumi_disable_all_positioning_ops(scene: bpy.types.Scene):
    """Disable all positioning modal operators - positioning-specific utility."""
    state = get_state()
    state.set_modal_state('highlight', False)
    state.set_modal_state('align', False)
    state.set_modal_state('rotate', False)
    state.set_modal_state('target', False)
    state.set_modal_state('free', False)
    state.set_modal_state('move', False)


def lumi_is_valid_positioning_context(context: bpy.types.Context, check_event=False, check_mode=None, required_mode=None) -> bool:
    """Centralized validation for all positioning operations
    
    Args:
        context: Blender context
        check_event: Whether to check for event presence
        check_mode: Whether to check positioning mode
        required_mode: Specific mode to check against
    
    Returns:
        bool: True if context is valid
    """
    # Basic context validation
    if not context or not context.scene:
        return False
    
    # Event validation (for modal operations)
    if check_event and not hasattr(context, 'event'):
        return False
    
    # Addon validation
    if not lumi_is_addon_enabled():
        return False
    
    # Mode validation
    if check_mode and required_mode:
        if context.scene.light_props.positioning_mode != required_mode:
            return False
    return True


def lumi_get_active_power_value(context: bpy.types.Context) -> float:
    """Get the active power value - simplified since sensitivity settings are removed."""
    # Return a reasonable default power value for smart sensitivity system
    return 10.0


def validate_positioning_target(obj: bpy.types.Object) -> bool:
    """Validate if object is suitable for positioning target - positioning-specific validation."""
    if not obj or obj.type not in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
        return False
    
    # Check if object has geometry
    # # Coba eksekusi kode dengan error handling
    try:
        if obj.type == 'MESH' and obj.data:
            return len(obj.data.vertices) > 0
        return True
    except:
        return False


def lumi_handle_modal_error(operator, context, error: Exception, operation_name: str) -> set:
    """Centralized error handling for modal operators
    
    Args:
        operator: The operator instance
        context: Blender context
        error: The exception that occurred
        operation_name: Name of the operation for error message
    
    Returns:
        set: Blender operator return set
    """
    operator.report({'ERROR'}, f"{operation_name} error: {error}")
    return {'CANCELLED'}


def lumi_handle_positioning_error(operator, context, error: Exception, operation_name: str) -> None:
    """Handle positioning update errors without breaking modal operation
    
    Args:
        operator: The operator instance
        context: Blender context
        error: The exception that occurred
        operation_name: Name of the operation for error message
    """
    # Only report critical errors, ignore minor ones
    if "out of" in str(error).lower() or "index" in str(error).lower():
        operator.report({'WARNING'}, f"{operation_name} warning: {error}")
    # Silent handling for minor errors


def detect_positioning_mode(event: bpy.types.Event) -> str:
    """Detect positioning mode based on modifier keys
    
    Args:
        event: Blender event object
        
    Returns:
        str: Mode name (HIGHLIGHT, NORMAL, ORBIT, TARGET, FREE, MOVE) or None
    """
    if event.ctrl and not event.shift and not event.alt:
        return 'HIGHLIGHT'
    elif not event.ctrl and event.shift and not event.alt:
        return 'NORMAL'
    elif not event.ctrl and not event.shift and event.alt:
        return 'ORBIT'
    elif event.ctrl and not event.shift and event.alt:
        return 'TARGET'
    elif event.ctrl and event.shift and not event.alt:
        return 'FREE'
    elif not event.ctrl and event.shift and event.alt:
        return 'MOVE'
    else:
        return None


def get_modifier_keys_for_mode(mode: str) -> str:
    """Get modifier keys description for a given mode
    
    Args:
        mode: Mode name
        
    Returns:
        str: Modifier keys description
    """
    modifier_map = {
        'HIGHLIGHT': 'Ctrl',
        'NORMAL': 'Shift',
        'ORBIT': 'Alt',
        'TARGET': 'Ctrl+Alt',
        'FREE': 'Ctrl+Shift',
        'MOVE': 'Shift+Alt'
    }
    return modifier_map.get(mode, '')


# Export positioning-specific utilities
__all__ = [
    'lumi_disable_all_positioning_ops',
    'lumi_get_active_power_value',
    'validate_positioning_target',
    'lumi_handle_modal_error',
    'lumi_handle_positioning_error',
    'detect_positioning_mode',
    'get_modifier_keys_for_mode'
]


