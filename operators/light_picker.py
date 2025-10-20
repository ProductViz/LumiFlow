# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Light Picker System
Automatic light selection system that works even when overlay extras are disabled.
This system automatically intercepts clicks and detects if you're clicking on a light,
providing the same natural feel as when extras are enabled.
"""

import bpy
from mathutils import Vector
from bpy_extras.view3d_utils import location_3d_to_region_2d, region_2d_to_origin_3d, region_2d_to_vector_3d
from ..utils import lumi_is_addon_enabled
from ..utils.common import lumi_get_light_collection
from ..utils.light import lumi_calculate_light_target_position
import logging

logger = logging.getLogger(__name__)

# Global state for automatic light picking
_auto_picker_active = False


class LUMI_OT_auto_light_picker(bpy.types.Operator):
    """Automatic light picker that runs in background"""
    bl_idname = "lumi.auto_light_picker"
    bl_label = "LumiFlow Auto Light Picker"
    bl_description = "Automatically detect clicks on lights (always active when LumiFlow enabled)"
    bl_options = {'INTERNAL'}
    
    # Class variables for modal state
    _is_running = False
    _instance = None
    
    # Pick radius in pixels
    pick_radius: bpy.props.IntProperty(
        name="Pick Radius",
        description="Radius in pixels for detecting light clicks",
        default=25,
        min=10,
        max=100
    )
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be invoked"""
        return (lumi_is_addon_enabled() and 
                context.area and 
                context.area.type == 'VIEW_3D' and
                context.region and
                context.space_data and
                not cls._is_running)
    
    def invoke(self, context, event):
        """Start automatic light picker (runs in background)"""
        # Check if already running
        if LUMI_OT_auto_light_picker._is_running:
            return {'CANCELLED'}
        
        # Set running state
        LUMI_OT_auto_light_picker._is_running = True
        LUMI_OT_auto_light_picker._instance = self
        
        # Add modal handler to WINDOW_MANAGER (not just one area)
        context.window_manager.modal_handler_add(self)
        
        logger.info("LumiFlow Auto Light Picker: Active (Multi-Viewport)")
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        """Handle mouse events for automatic light picking"""
        # Stop if addon disabled
        if not lumi_is_addon_enabled():
            return self.cancel(context)
        
        # Only intercept left mouse press in 3D viewport
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get the actual viewport context where the click happened
            viewport_context = self._get_viewport_context_from_event(context, event)
            
            if viewport_context is None:
                # Not in a 3D viewport, pass through
                return {'PASS_THROUGH'}
            
            # Try to pick a light at mouse position using correct viewport context
            picked_light = self.pick_light_at_mouse(viewport_context, event)
            
            if picked_light:
                # Deselect all objects first (unless Shift is held for multi-select)
                if not event.shift:
                    bpy.ops.object.select_all(action='DESELECT')
                
                # Select the picked light
                picked_light.select_set(True)
                context.view_layer.objects.active = picked_light
                
                # Force viewport redraw
                if viewport_context.area:
                    viewport_context.area.tag_redraw()
                
                # Consume the event - don't pass through
                return {'RUNNING_MODAL'}
            else:
                # No light found - let Blender handle the click normally
                return {'PASS_THROUGH'}
        
        # Pass through all other events
        return {'PASS_THROUGH'}
    
    def _get_viewport_context_from_event(self, context, event):
        """Get the correct viewport context from mouse position.
        This is crucial for multi-viewport support."""
        # Find which area/region the mouse is in
        mouse_x = event.mouse_x
        mouse_y = event.mouse_y
        
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    # Check if mouse is within this area's bounds
                    if (area.x <= mouse_x < area.x + area.width and
                        area.y <= mouse_y < area.y + area.height):
                        
                        # Find the correct region within this area
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                # Create a context override for this specific viewport
                                override = context.copy()
                                override['area'] = area
                                override['region'] = region
                                override['space_data'] = area.spaces.active
                                
                                # Return a simple context object
                                class ViewportContext:
                                    def __init__(self, area, region, space_data, scene, view_layer):
                                        self.area = area
                                        self.region = region
                                        self.space_data = space_data
                                        self.scene = scene
                                        self.view_layer = view_layer
                                
                                return ViewportContext(
                                    area, region, area.spaces.active,
                                    context.scene, context.view_layer
                                )
        
        return None
    
    def pick_light_at_mouse(self, context, event):
        """
        Pick a light at the mouse position using 2D screen space detection.
        Checks both light position and target sign position.
        Returns the closest light within pick_radius, or None if no light is found.
        """
        # Get viewport context
        region = context.region
        rv3d = context.space_data.region_3d
        
        if not region or not rv3d:
            return None
        
        # Convert mouse position from window coordinates to region coordinates
        # This is crucial for multi-viewport support
        mouse_x = event.mouse_x - region.x
        mouse_y = event.mouse_y - region.y
        mouse_pos = Vector((mouse_x, mouse_y))
        
        # Get all lights from LumiFlow collection
        scene = context.scene
        light_collection = lumi_get_light_collection(scene)
        
        if not light_collection:
            return None
        
        all_lights = [obj for obj in light_collection.objects if obj.type == 'LIGHT']
        
        if not all_lights:
            return None
        
        # Find the closest light within pick radius
        closest_light = None
        closest_distance = float('inf')
        
        for light in all_lights:
            # Check 1: Light position
            light_pos_2d = location_3d_to_region_2d(region, rv3d, light.location)
            if light_pos_2d is not None:
                distance = (light_pos_2d - mouse_pos).length
                if distance < self.pick_radius and distance < closest_distance:
                    closest_distance = distance
                    closest_light = light
            
            # Check 2: Target sign position
            target_pos = lumi_calculate_light_target_position(light, scene)
            target_pos_2d = location_3d_to_region_2d(region, rv3d, target_pos)
            if target_pos_2d is not None:
                distance = (target_pos_2d - mouse_pos).length
                if distance < self.pick_radius and distance < closest_distance:
                    closest_distance = distance
                    closest_light = light
        
        return closest_light
    
    def cancel(self, context):
        """Cancel the operator"""
        LUMI_OT_auto_light_picker._is_running = False
        LUMI_OT_auto_light_picker._instance = None
        logger.info("LumiFlow Auto Light Picker: Stopped")
        return {'CANCELLED'}
    
    @classmethod
    def is_picker_running(cls):
        """Check if auto picker is currently running"""
        return cls._is_running
    
    @classmethod
    def stop_picker(cls):
        """Stop the auto picker"""
        if cls._instance:
            cls._instance.cancel(bpy.context)
            cls._instance = None


def pick_light_at_position(context, mouse_x, mouse_y, pick_radius=20):
    """
    Utility function to pick a light at a specific 2D position.
    Checks both light position and target sign position.
    Can be used by other operators or systems.
    
    Args:
        context: Blender context
        mouse_x: Mouse X position in region coordinates
        mouse_y: Mouse Y position in region coordinates
        pick_radius: Radius in pixels for detection
    
    Returns:
        The closest light object within pick_radius, or None
    """
    region = context.region
    rv3d = context.space_data.region_3d
    
    if not region or not rv3d:
        return None
    
    mouse_pos = Vector((mouse_x, mouse_y))
    
    # Get all lights from LumiFlow collection
    scene = context.scene
    light_collection = lumi_get_light_collection(scene)
    
    if not light_collection:
        return None
    
    all_lights = [obj for obj in light_collection.objects if obj.type == 'LIGHT']
    
    if not all_lights:
        return None
    
    # Find the closest light within pick radius
    closest_light = None
    closest_distance = float('inf')
    
    for light in all_lights:
        # Check 1: Light position
        light_pos_2d = location_3d_to_region_2d(region, rv3d, light.location)
        if light_pos_2d is not None:
            distance = (light_pos_2d - mouse_pos).length
            if distance < pick_radius and distance < closest_distance:
                closest_distance = distance
                closest_light = light
        
        # Check 2: Target sign position
        target_pos = lumi_calculate_light_target_position(light, scene)
        target_pos_2d = location_3d_to_region_2d(region, rv3d, target_pos)
        if target_pos_2d is not None:
            distance = (target_pos_2d - mouse_pos).length
            if distance < pick_radius and distance < closest_distance:
                closest_distance = distance
                closest_light = light
    
    return closest_light


def start_auto_picker():
    """Start the automatic light picker if not already running"""
    if not LUMI_OT_auto_light_picker.is_picker_running():
        try:
            bpy.ops.lumi.auto_light_picker('INVOKE_DEFAULT')
            logger.info("Auto light picker started")
        except Exception as e:
            logger.error(f"Failed to start auto light picker: {e}")


def stop_auto_picker():
    """Stop the automatic light picker"""
    LUMI_OT_auto_light_picker.stop_picker()


def register():
    """Register the light picker operator"""
    bpy.utils.register_class(LUMI_OT_auto_light_picker)


def unregister():
    """Unregister the light picker operator"""
    stop_auto_picker()
    bpy.utils.unregister_class(LUMI_OT_auto_light_picker)
