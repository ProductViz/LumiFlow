# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Mode Manager
Centralized mode management system for all overlay modules.
Provides single source of truth for mode definitions, availability, and handling.
"""

import bpy
import math
from typing import Dict, List, Tuple, Optional, Union
from .color import lumi_rgb_to_kelvin


class ModeManager:
    """
    Centralized mode management system for LumiFlow overlay modules.
    Handles mode definitions, availability checking, and property access.
    """
    
    # =====================================================================
    # CENTRALIZED MODE DEFINITIONS
    # =====================================================================
    
    # Mode definitions with unified structure
    MODES = {
        'DISTANCE': {
            'display_name': 'Distance',
            'modifier': 'Ctrl',
            'description': 'Light distance from pivot point',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_distance(light),
                'formatter': lambda value: f"{value:.2f}m",
                'unit': 'm'
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            }
        },
        'POWER': {
            'display_name': 'Power',
            'modifier': 'Shift',
            'description': 'Light energy/power',
            'properties': {
                'getter': lambda light, ctx: getattr(light.data, 'energy', 0),
                'formatter': lambda value: f"{value:.1f}W",
                'unit': 'W'
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            }
        },
        'SCALE': {
            'display_name': 'Scale',
            'modifier': 'Alt',
            'description': 'Light size/radius (multi-property handler)',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_scale_value(light),
                'formatter': lambda value: f"{value:.2f}m",
                'unit': 'm'
            },
            'availability': {
                'POINT': True,    # Controls shadow_soft_size
                'SPOT': True,     # Controls shadow_soft_size
                'AREA': True,     # Controls size/size_y
                'DEFAULT': False
            },
            'dynamic_labels': {
                'POINT': 'Radius',
                'SPOT': 'Radius', 
                'AREA': 'Size'
            }
        },
        'ANGLE': {
            'display_name': 'Angle',
            'modifier': 'Ctrl+Shift',
            'description': 'Light angle/spot size/spread (multi-property handler)',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_angle_value(light),
                'formatter': lambda value: f"{value:.1f}Â°",
                'unit': 'Â°'
            },
            'availability': {
                'SUN': True,      # Controls angle
                'SPOT': True,     # Controls spot_size
                'AREA': True,     # Controls spread
                'DEFAULT': False
            },
            'dynamic_labels': {
                'SUN': 'Angle',
                'SPOT': 'Spot Size',
                'AREA': 'Spread'
            }
        },
        'BLEND': {
            'display_name': 'Blend',
            'modifier': 'Shift+Alt',
            'description': 'Spot light blend factor',
            'properties': {
                'getter': lambda light, ctx: getattr(light.data, 'spot_blend', 0),
                'formatter': lambda value: f"{value:.2f}",
                'unit': ''
            },
            'availability': {
                'SPOT': True,      # Controls spot_blend
                'DEFAULT': False
            }
        },
        'TEMPERATURE': {
            'display_name': 'Temperature',
            'modifier': 'Ctrl+Alt',
            'description': 'Color temperature',
            'properties': {
                'getter': lambda light, ctx: lumi_rgb_to_kelvin(*light.data.color) if hasattr(light.data, 'color') else 5500,
                'formatter': lambda value: f"{int(value)}K",
                'unit': 'K'
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            }
        },
        # =====================================================================
        # POSITIONING MODES
        # =====================================================================
        'HIGHLIGHT': {
            'display_name': 'Highlight',
            'modifier': 'Ctrl',
            'description': 'Highlight positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'highlight'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'highlight'
        },
        'NORMAL': {
            'display_name': 'Normal',
            'modifier': 'Shift',
            'description': 'Normal positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'normal'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'normal'
        },
        'ORBIT': {
            'display_name': 'Orbit',
            'modifier': 'Alt',
            'description': 'Orbit positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'orbit'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'orbit'
        },
        'TARGET': {
            'display_name': 'Target',
            'modifier': 'Ctrl+Alt',
            'description': 'Target positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'target'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'target'
        },
        'FREE': {
            'display_name': 'Free',
            'modifier': 'Ctrl+Shift',
            'description': 'Free positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'free'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'free'
        },
        'MOVE': {
            'display_name': 'Move',
            'modifier': 'Shift+Alt',
            'description': 'Move positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'move'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {
                'POINT': True,
                'SUN': True,
                'SPOT': True,
                'AREA': True,
                'DEFAULT': True
            },
            'is_positioning': True,
            'positioning_type': 'move'
        }
    }
    
    # =====================================================================
    # STATIC HELPER METHODS
    # =====================================================================
    
    @staticmethod
    def _get_distance(light_obj: bpy.types.Object) -> float:
        """Get distance from light to pivot point."""
        from ..utils.light import lumi_get_light_pivot
        if "Lumi_pivot_world" in light_obj:
            return (light_obj.location - lumi_get_light_pivot(light_obj)).length
        return 0.0
    
    @staticmethod
    def _get_scale_value(light_obj: bpy.types.Object) -> float:
        """Get scale value based on light type."""
        data = light_obj.data
        light_type = data.type
        
        if light_type in {'POINT', 'SPOT'}:
            return getattr(data, 'shadow_soft_size', 0)
        elif light_type == 'AREA':
            shape = getattr(data, 'shape', 'SQUARE')
            size_x = getattr(data, 'size', 0.0)
            size_y = getattr(data, 'size_y', size_x)
            
            # For rectangle/ellipse with different sizes, return average
            if shape in {'RECTANGLE', 'ELLIPSE'} and abs(size_x - size_y) > 0.001:
                return (size_x + size_y) / 2
            else:
                return size_x
        return 0.0
    
    @staticmethod
    def _get_angle_value(light_obj: bpy.types.Object) -> float:
        """Get angle value based on light type."""
        data = light_obj.data
        light_type = data.type
        
        if light_type == 'SUN':
            return getattr(data, 'angle', 0.0)
        elif light_type == 'SPOT':
            return getattr(data, 'spot_size', 0.0) * 180.0 / math.pi  # Convert radians to degrees
        elif light_type == 'AREA':
            return getattr(data, 'spread', 0.0)
        else:
            return 0.0
    
    @staticmethod
    def _get_positioning_status(light_obj: bpy.types.Object, positioning_type: str) -> bool:
        """Get positioning mode status for a light.
        
        Args:
            light_obj: Blender light object
            positioning_type: Positioning mode type (highlight, normal, orbit, target, free, move)
            
        Returns:
            bool: True if positioning mode is active for this light
        """
        try:
            from ..core.state import get_state
            state = get_state()
            
            # Map positioning types to modal state names
            state_mapping = {
                'highlight': 'highlight',
                'normal': 'align',  # Normal positioning uses 'align' state
                'orbit': 'rotate',  # Orbit positioning uses 'rotate' state
                'target': 'target',
                'free': 'free',
                'move': 'move'
            }
            
            modal_state = state_mapping.get(positioning_type)
            if modal_state:
                return state.get_modal_state(modal_state)
            
            return False
        except Exception as e:
            print(f"âš ï¸  LumiFlow: Error getting positioning status: {e}")
            return False
    
    @classmethod
    def get_active_positioning_mode(cls, context: bpy.types.Context) -> Optional[str]:
        """Get the currently active positioning mode.
        
        Args:
            context: Blender context
            
        Returns:
            str: Active positioning mode name or None if none active
        """
        try:
            from ..core.state import get_state
            state = get_state()
            
            # Check all positioning modal states
            positioning_states = {
                'highlight': 'HIGHLIGHT',
                'align': 'NORMAL',      # Normal positioning
                'rotate': 'ORBIT',      # Orbit positioning
                'target': 'TARGET',
                'free': 'FREE',
                'move': 'MOVE'
            }
            
            for modal_state, mode_name in positioning_states.items():
                if state.get_modal_state(modal_state):
                    return mode_name
            
            return None
        except Exception as e:
            print(f"âš ï¸  LumiFlow: Error getting active positioning mode: {e}")
            return None
    
    @classmethod
    def is_positioning_mode(cls, mode_name: str) -> bool:
        """Check if a mode is a positioning mode.
        
        Args:
            mode_name: Mode name (uppercase)
            
        Returns:
            bool: True if mode is a positioning mode
        """
        mode_config = cls.MODES.get(mode_name, {})
        return mode_config.get('is_positioning', False)
    
    @classmethod
    def get_positioning_modes(cls) -> List[str]:
        """Get list of all positioning mode names.
        
        Returns:
            List of positioning mode names (uppercase)
        """
        return [
            mode_name for mode_name, config in cls.MODES.items()
            if config.get('is_positioning', False)
        ]
    
    @classmethod
    def get_smart_control_modes(cls) -> List[str]:
        """Get list of all smart control mode names (non-positioning).
        
        Returns:
            List of smart control mode names (uppercase)
        """
        return [
            mode_name for mode_name, config in cls.MODES.items()
            if not config.get('is_positioning', False)
        ]
    # =====================================================================
    
    @classmethod
    def get_available_modes(cls, light_type: str) -> List[str]:
        """
        Get list of available mode names for a light type.
        
        Args:
            light_type: Light type (POINT, SUN, SPOT, AREA)
            
        Returns:
            List of available mode names (uppercase)
        """
        available = []
        for mode_name, mode_config in cls.MODES.items():
            if cls.is_mode_available(mode_name, light_type):
                available.append(mode_name)
        return available
    
    @classmethod
    def is_mode_available(cls, mode_name: str, light_type: str) -> bool:
        """
        Check if a mode is available for a specific light type.
        
        Args:
            mode_name: Mode name (uppercase)
            light_type: Light type (POINT, SUN, SPOT, AREA)
            
        Returns:
            True if mode is available
        """
        mode_config = cls.MODES.get(mode_name)
        if not mode_config:
            return False
        
        availability = mode_config['availability']
        return availability.get(light_type, availability.get('DEFAULT', False))
    
    @classmethod
    def get_mode_display_name(cls, mode_name: str, light_type: str) -> str:
        """
        Get display name for a mode, with dynamic labels for multi-property modes.
        
        Args:
            mode_name: Mode name (uppercase)
            light_type: Light type (POINT, SUN, SPOT, AREA)
            
        Returns:
            Display name for the mode
        """
        mode_config = cls.MODES.get(mode_name)
        if not mode_config:
            return mode_name.title()
        
        # Check for dynamic labels first
        dynamic_labels = mode_config.get('dynamic_labels', {})
        if light_type in dynamic_labels:
            return dynamic_labels[light_type]
        
        return mode_config['display_name']
    
    @classmethod
    def get_mode_modifier(cls, mode_name: str) -> str:
        """
        Get keyboard modifier for a mode.
        
        Args:
            mode_name: Mode name (uppercase)
            
        Returns:
            Keyboard modifier string
        """
        mode_config = cls.MODES.get(mode_name, {})
        return mode_config.get('modifier', 'Ctrl/Shift/Alt')
    
    @classmethod
    def get_mode_info(cls, mode_name: str, light_obj: bpy.types.Object, context: bpy.types.Context) -> Tuple[str, str, bool]:
        """
        Get comprehensive mode information for display.
        
        Args:
            mode_name: Mode name (uppercase)
            light_obj: Blender light object
            context: Blender context
            
        Returns:
            Tuple of (label, formatted_value, is_available)
        """
        light_type = light_obj.data.type
        
        # Check availability
        if not cls.is_mode_available(mode_name, light_type):
            error_msg = f"âŒ {mode_name.title()} mode not available for {light_type} lights"
            return None, error_msg, False
        
        # Get mode configuration
        mode_config = cls.MODES.get(mode_name)
        if not mode_config:
            return mode_name.title(), "N/A", True
        
        # Get display label
        label = cls.get_mode_display_name(mode_name, light_type)
        
        # Get and format value
        try:
            getter = mode_config['properties']['getter']
            formatter = mode_config['properties']['formatter']
            
            raw_value = getter(light_obj, context)
            formatted_value = formatter(raw_value)
            
            return label, formatted_value, True
            
        except Exception as e:
            return label, "Error", False
    
    @classmethod
    def get_all_modes_info(cls, light_obj: bpy.types.Object, context: bpy.types.Context) -> List[Tuple[str, str]]:
        """
        Get information for all available smart control modes for a light.
        Excludes positioning modes - only shows Distance, Power, Scale, etc.
        
        Args:
            light_obj: Blender light object
            context: Blender context
            
        Returns:
            List of (label, formatted_value) tuples for available smart control modes
        """
        available_modes = []
        light_type = light_obj.data.type
        
        # Only iterate through smart control modes, exclude positioning modes
        for mode_name in cls.get_smart_control_modes():
            label, value, is_available = cls.get_mode_info(mode_name, light_obj, context)
            if is_available and value != "N/A" and not value.startswith("âŒ"):
                available_modes.append((label, value))
        
        return available_modes
    
    @classmethod
    def get_mode_tips(cls, light_type: str) -> List[str]:
        """
        Get formatted mode tips for display in overlay.
        
        Args:
            light_type: Light type (POINT, SUN, SPOT, AREA)
            
        Returns:
            List of formatted tip strings
        """
        tips = []
        
        for mode_name in cls.get_available_modes(light_type):
            display_name = cls.get_mode_display_name(mode_name, light_type)
            modifier = cls.get_mode_modifier(mode_name)
            
            # Use different action text for positioning modes vs smart control modes
            if cls.is_positioning_mode(mode_name):
                action_text = "LMB drag"
            else:
                action_text = "MMB Drag"
            
            tips.append(f"â€¢ {display_name} ({modifier} + {action_text})")
        
        return tips
    
    @classmethod
    def get_mode_property_details(cls, mode_name: str, light_type: str) -> Dict:
        """
        Get detailed property information for a mode.
        
        Args:
            mode_name: Mode name (uppercase)
            light_type: Light type (POINT, SUN, SPOT, AREA)
            
        Returns:
            Dictionary with property details
        """
        if not cls.is_mode_available(mode_name, light_type):
            return {}
        
        mode_config = cls.MODES.get(mode_name, {})
        return {
            'mode_name': mode_name,
            'display_name': cls.get_mode_display_name(mode_name, light_type),
            'modifier': cls.get_mode_modifier(mode_name),
            'description': mode_config.get('description', ''),
            'unit': mode_config.get('properties', {}).get('unit', ''),
            'is_multi_property': 'dynamic_labels' in mode_config
        }


# =====================================================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY
# =====================================================================

def get_available_modes(light_type: str) -> List[str]:
    """Backward compatibility function."""
    return ModeManager.get_available_modes(light_type)

def is_mode_available(mode_name: str, light_type: str) -> bool:
    """Backward compatibility function."""
    return ModeManager.is_mode_available(mode_name, light_type)

def get_mode_label_for_light_type(mode_name: str, light_type: str) -> str:
    """Backward compatibility function."""
    return ModeManager.get_mode_display_name(mode_name, light_type)

def get_smart_control_mode_info(mode_name: str, light_obj: bpy.types.Object, context: bpy.types.Context) -> Tuple[str, str, bool]:
    """Backward compatibility function."""
    return ModeManager.get_mode_info(mode_name, light_obj, context)

def get_all_available_modes_info(light_obj: bpy.types.Object, context: bpy.types.Context) -> List[Tuple[str, str]]:
    """Backward compatibility function."""
    return ModeManager.get_all_modes_info(light_obj, context)

def handle_all_smart_control_modes(mode_name: str, light_obj: bpy.types.Object, context: bpy.types.Context) -> str:
    """Backward compatibility function."""
    label, value, is_available = ModeManager.get_mode_info(mode_name, light_obj, context)
    if is_available:
        return f"{label}: {value}"
    else:
        return value  # Return error message


# =====================================================================
# POSITIONING MODE CONVENIENCE FUNCTIONS
# =====================================================================

def get_active_positioning_mode(context: bpy.types.Context) -> Optional[str]:
    """Get the currently active positioning mode.
    
    Args:
        context: Blender context
        
    Returns:
        str: Active positioning mode name or None if none active
    """
    return ModeManager.get_active_positioning_mode(context)

def is_positioning_mode(mode_name: str) -> bool:
    """Check if a mode is a positioning mode.
    
    Args:
        mode_name: Mode name (uppercase)
        
    Returns:
        bool: True if mode is a positioning mode
    """
    return ModeManager.is_positioning_mode(mode_name)

def get_positioning_modes() -> List[str]:
    """Get list of all positioning mode names.
    
    Returns:
        List of positioning mode names (uppercase)
    """
    return ModeManager.get_positioning_modes()

def get_smart_control_modes() -> List[str]:
    """Get list of all smart control mode names (non-positioning).
    
    Returns:
        List of smart control mode names (uppercase)
    """
    return ModeManager.get_smart_control_modes()

def get_positioning_mode_status(light_obj: bpy.types.Object, positioning_type: str) -> bool:
    """Get positioning mode status for a light.
    
    Args:
        light_obj: Blender light object
        positioning_type: Positioning mode type (highlight, normal, orbit, target, free, move)
        
    Returns:
        bool: True if positioning mode is active for this light
    """
    return ModeManager._get_positioning_status(light_obj, positioning_type)

