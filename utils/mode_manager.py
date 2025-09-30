# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Mode Manager
Centralized mode management system for all overlay modules.
Provides single source of truth for mode definitions, availability, and handling.
"""

import bpy
import math
from typing import Dict, List, Tuple, Optional, Union
from .color import lumi_rgb_to_kelvin


class ModeManager:
    """Centralized mode management for smart controls and positioning."""
    
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
                'formatter': lambda value: f"{value:.1f}°",
                'unit': '°'
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
    }
    
    # Positioning modes - generated using helper
    MODES.update({
        'HIGHLIGHT': {
            'display_name': 'Highlight', 'modifier': 'Ctrl',
            'description': 'Highlight positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'highlight'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'highlight'
        },
        'NORMAL': {
            'display_name': 'Normal', 'modifier': 'Shift',
            'description': 'Normal positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'normal'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'normal'
        },
        'ORBIT': {
            'display_name': 'Orbit', 'modifier': 'Alt',
            'description': 'Orbit positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'orbit'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'orbit'
        },
        'TARGET': {
            'display_name': 'Target', 'modifier': 'Ctrl+Alt',
            'description': 'Target positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'target'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'target'
        },
        'FREE': {
            'display_name': 'Free', 'modifier': 'Ctrl+Shift',
            'description': 'Free positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'free'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'free'
        },
        'MOVE': {
            'display_name': 'Move', 'modifier': 'Shift+Alt',
            'description': 'Move positioning mode',
            'properties': {
                'getter': lambda light, ctx: ModeManager._get_positioning_status(light, 'move'),
                'formatter': lambda value: "Active" if value else "Inactive",
                'unit': ''
            },
            'availability': {'POINT': True, 'SUN': True, 'SPOT': True, 'AREA': True, 'DEFAULT': True},
            'is_positioning': True, 'positioning_type': 'move'
        }
    })
    
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
            return getattr(data, 'angle', 0.0) * 180.0 / math.pi
        elif light_type == 'SPOT':
            return getattr(data, 'spot_size', 0.0) * 180.0 / math.pi
        elif light_type == 'AREA':
            return getattr(data, 'spread', 0.0) * 180.0
        return 0.0
    
    @staticmethod
    def _get_positioning_status(light_obj: bpy.types.Object, positioning_type: str) -> bool:
        """Get positioning mode status for a light."""
        from ..core.state import get_state
        state = get_state()
        
        state_mapping = {
            'highlight': 'highlight',
            'normal': 'align',
            'orbit': 'rotate',
            'target': 'target',
            'free': 'free',
            'move': 'move'
        }
        
        modal_state = state_mapping.get(positioning_type)
        return state.get_modal_state(modal_state) if modal_state else False
    
    @classmethod
    def get_active_positioning_mode(cls, context: bpy.types.Context) -> Optional[str]:
        """Get the currently active positioning mode."""
        from ..core.state import get_state
        state = get_state()
        
        positioning_states = {
            'highlight': 'HIGHLIGHT',
            'align': 'NORMAL',
            'rotate': 'ORBIT',
            'target': 'TARGET',
            'free': 'FREE',
            'move': 'MOVE'
        }
        
        for modal_state, mode_name in positioning_states.items():
            if state.get_modal_state(modal_state):
                return mode_name
        
        return None
    
    @classmethod
    def is_positioning_mode(cls, mode_name: str) -> bool:
        """Check if a mode is a positioning mode."""
        return cls.MODES.get(mode_name, {}).get('is_positioning', False)
    
    @classmethod
    def get_positioning_modes(cls) -> List[str]:
        """Get list of all positioning mode names."""
        return [name for name, cfg in cls.MODES.items() if cfg.get('is_positioning', False)]
    
    @classmethod
    def get_smart_control_modes(cls) -> List[str]:
        """Get list of all smart control mode names (non-positioning)."""
        return [name for name, cfg in cls.MODES.items() if not cfg.get('is_positioning', False)]
    # =====================================================================
    
    @classmethod
    def get_available_modes(cls, light_type: str) -> List[str]:
        """Get list of available mode names for a light type."""
        return [name for name in cls.MODES if cls.is_mode_available(name, light_type)]
    
    @classmethod
    def is_mode_available(cls, mode_name: str, light_type: str) -> bool:
        """Check if a mode is available for a specific light type."""
        if mode_name not in cls.MODES:
            return False
        availability = cls.MODES[mode_name]['availability']
        return availability.get(light_type, availability.get('DEFAULT', False))
    
    @classmethod
    def get_mode_display_name(cls, mode_name: str, light_type: str) -> str:
        """Get display name for a mode, with dynamic labels for multi-property modes."""
        if mode_name not in cls.MODES:
            return mode_name.title()
        
        mode_config = cls.MODES[mode_name]
        dynamic_labels = mode_config.get('dynamic_labels', {})
        return dynamic_labels.get(light_type, mode_config['display_name'])
    
    @classmethod
    def get_mode_modifier(cls, mode_name: str) -> str:
        """Get keyboard modifier for a mode."""
        return cls.MODES.get(mode_name, {}).get('modifier', 'Ctrl/Shift/Alt')
    
    @classmethod
    def get_mode_info(cls, mode_name: str, light_obj: bpy.types.Object, context: bpy.types.Context) -> Tuple[str, str, bool]:
        """Get comprehensive mode information for display."""
        light_type = light_obj.data.type
        
        if not cls.is_mode_available(mode_name, light_type):
            error_msg = f"âœ {mode_name.title()} mode not available for {light_type} lights"
            return None, error_msg, False
        
        if mode_name not in cls.MODES:
            return mode_name.title(), "N/A", True
        
        mode_config = cls.MODES[mode_name]
        label = cls.get_mode_display_name(mode_name, light_type)
        
        try:
            getter = mode_config['properties']['getter']
            formatter = mode_config['properties']['formatter']
            raw_value = getter(light_obj, context)
            formatted_value = formatter(raw_value)
            return label, formatted_value, True
        except:
            return label, "Error", False
    
    @classmethod
    def get_all_modes_info(cls, light_obj: bpy.types.Object, context: bpy.types.Context) -> List[Tuple[str, str]]:
        """Get information for all available smart control modes for a light."""
        result = []
        for mode_name in cls.get_smart_control_modes():
            label, value, is_available = cls.get_mode_info(mode_name, light_obj, context)
            if is_available and value not in ("N/A", "") and not value.startswith("âœ"):
                result.append((label, value))
        return result


# Exported symbols
__all__ = ['ModeManager']
