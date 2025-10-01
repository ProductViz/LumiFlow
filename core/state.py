# SPDX-License-Identifier: GPL-3.0-or-later
#
# LumiFlow - Smart lighting tools for Blender
# Copyright (C) 2024 LumiFlow Developer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Core State Module
Central state management system for LumiFlow with singleton pattern implementation.
Manages addon state, selected objects, and modal operators.
"""
import bpy
from mathutils import Vector
from typing import Dict, Any, List

class LumiFlowState:
    """State management for LumiFlow addon"""

    def __init__(self):
        # Modal operators state
        self.modal_operators = {}
        
        # Draw handlers
        self.draw_handlers = {}
        
        # Temporary data storage
        self.temp_data = {}
        
        # Control states
        self.scroll_control_enabled = False
        self.last_selected_lights = set()
        
        # Modal states (mapped from old global variables)
        self.modal_states = {
            'rotate': False,      # _rotate_modal_active (ORBIT positioning)
            'target': False,      # _target_modal_active  (TARGET positioning)
            'align': False,       # _align_modal_active   (NORMAL positioning)
            'highlight': False,   # _highlight_modal_active (HIGHLIGHT positioning)
            'free': False,        # Free positioning mode
            'move': False,        # Move positioning mode
        }
        
        # Obstruction detection state
        self.obstruction_detection = {
            'enabled': True,
            'fallback_strategy': 'ADJUST_POSITION',
            'show_warnings': True,
            'detected_obstructions': [],
            'adjusted_lights': [],
            'skipped_lights': []
        }

    def register_modal(self, operator_id, instance):
        """Register active modal operator"""
        self.modal_operators[operator_id] = instance

    def unregister_modal(self, operator_id):
        """Unregister modal operator"""
        if operator_id in self.modal_operators:
            del self.modal_operators[operator_id]

    def set_modal_state(self, modal_type, active):
        """Set modal state for specific type"""
        if modal_type in self.modal_states:
            self.modal_states[modal_type] = active

    def get_modal_state(self, modal_type):
        """Get modal state for specific type"""
        return self.modal_states.get(modal_type, False)

    def register_draw_handler(self, handler_id, handler):
        """Register draw handler"""
        self.draw_handlers[handler_id] = handler

    def unregister_draw_handler(self, handler_id):
        """Unregister draw handler"""
        if handler_id in self.draw_handlers:
            del self.draw_handlers[handler_id]

    def cleanup(self):
        """Clean up all state"""
        # Clean up modal operators
        self.modal_operators.clear()
        
        # Clean up draw handlers - PROPERLY unregister from Blender
        try:
            from ..overlay.config import overlay_manager
            overlay_manager.disable_all_handlers()
            overlay_manager.handlers.clear()
        except Exception as e:
            pass
        
        self.draw_handlers.clear()
        
        # Clean up temporary data
        self.temp_data.clear()
        self.scroll_control_enabled = False
        self.last_selected_lights.clear()
        
        # Reset all modal states
        for key in self.modal_states:
            self.modal_states[key] = False
        
        # Reset obstruction detection state
        self.obstruction_detection = {
            'enabled': True,
            'fallback_strategy': 'ADJUST_POSITION',
            'show_warnings': True,
            'detected_obstructions': [],
            'adjusted_lights': [],
            'skipped_lights': []
        }
    
    def set_obstruction_detection_enabled(self, enabled: bool):
        """Set obstruction detection enabled state"""
        self.obstruction_detection['enabled'] = enabled
    
    def set_obstruction_fallback_strategy(self, strategy: str):
        """Set obstruction fallback strategy"""
        if strategy in ['ADJUST_POSITION', 'SKIP_LIGHT', 'WARN_ONLY']:
            self.obstruction_detection['fallback_strategy'] = strategy
    
    def set_obstruction_show_warnings(self, show_warnings: bool):
        """Set whether to show obstruction warnings"""
        self.obstruction_detection['show_warnings'] = show_warnings
    
    def add_detected_obstruction(self, light_name: str, hit_object: str, hit_location: Vector):
        """Add detected obstruction to state"""
        self.obstruction_detection['detected_obstructions'].append({
            'light_name': light_name,
            'hit_object': hit_object,
            'hit_location': hit_location,
            'timestamp': bpy.context.scene.frame_current if hasattr(bpy.context, 'scene') else 0
        })
    
    def add_adjusted_light(self, light_name: str, original_position: Vector, new_position: Vector):
        """Add adjusted light to state"""
        self.obstruction_detection['adjusted_lights'].append({
            'light_name': light_name,
            'original_position': original_position,
            'new_position': new_position,
            'timestamp': bpy.context.scene.frame_current if hasattr(bpy.context, 'scene') else 0
        })
    
    def add_skipped_light(self, light_name: str, reason: str):
        """Add skipped light to state"""
        self.obstruction_detection['skipped_lights'].append({
            'light_name': light_name,
            'reason': reason,
            'timestamp': bpy.context.scene.frame_current if hasattr(bpy.context, 'scene') else 0
        })
    
    def get_obstruction_detection_state(self) -> Dict[str, Any]:
        """Get current obstruction detection state"""
        return self.obstruction_detection.copy()
    
    def clear_obstruction_detection_history(self):
        """Clear obstruction detection history"""
        self.obstruction_detection['detected_obstructions'].clear()
        self.obstruction_detection['adjusted_lights'].clear()
        self.obstruction_detection['skipped_lights'].clear()

# Singleton instance
_state = LumiFlowState()

def get_state():
    """Get LumiFlow state instance"""
    return _state
