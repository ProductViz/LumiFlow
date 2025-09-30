# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Common Utilities
Contains frequently used functions across various modules (operators, panels, menus, draw).
"""

import bpy
from mathutils import Vector

def lumi_is_addon_enabled() -> bool:
    """Check if LumiFlow addon is enabled - used in all modules."""
    try:
        return bpy.context.scene.get("lumi_enabled", False)
    except Exception:
        return False


def lumi_get_light_collection(scene=None) -> bpy.types.Collection:
    """
    Get or create LumiFlow light collection per scene.
    
    Args:
        scene: Target scene, defaults to current scene
    
    Returns:
        Collection specific to that scene
    """
    if scene is None:
        scene = bpy.context.scene
    
    if not scene:
        return None
    
    # Use naming convention: LumiFlow_Lights_[SceneName]
    col_name = f"LumiFlow_Lights_{scene.name}"
    
    # Check if collection already exists
    if col_name in bpy.data.collections:
        collection = bpy.data.collections[col_name]
        # Ensure collection is linked to this scene
        if collection.name not in scene.collection.children:
            scene.collection.children.link(collection)
        return collection
    
    # Create new collection for this scene
    try:
        collection = bpy.data.collections.new(col_name)
        scene.collection.children.link(collection)
        return collection
    except Exception:
        return None


def cleanup_lumiflow_collections():
    """
    Remove collections for scenes that no longer exist.
    Called during addon register/unregister.
    Uses timer to delay execution if data is not available during registration.
    """
    try:
        # Check if bpy.data is accessible and has scenes
        if hasattr(bpy.data, 'scenes') and bpy.data.scenes:
            _perform_cleanup_lumiflow_collections()
        else:
            # Schedule cleanup for later using timer
            _schedule_cleanup_lumiflow_collections()
    except AttributeError:
        # Schedule cleanup for later using timer
        _schedule_cleanup_lumiflow_collections()


def _perform_cleanup_lumiflow_collections():
    """
    Internal function to perform the actual cleanup.
    Called when bpy.data is accessible.
    """
    try:
        existing_scenes = {scene.name for scene in bpy.data.scenes}
        
        for collection in bpy.data.collections:
            if collection.name.startswith("LumiFlow_Lights_"):
                scene_name = collection.name.replace("LumiFlow_Lights_", "")
                if scene_name not in existing_scenes:
                    try:
                        bpy.data.collections.remove(collection)
                    except Exception:
                        pass  # Ignore errors during cleanup
    except Exception:
        pass  # Ignore all errors during cleanup


def _schedule_cleanup_lumiflow_collections():
    """
    Schedule cleanup using timer for execution when Blender is ready.
    """
    try:
        # Use a small delay to ensure Blender is fully initialized
        bpy.app.timers.register(
            _cleanup_timer_callback,
            first_interval=0.5
        )
    except Exception:
        pass  # Ignore timer registration errors


def _cleanup_timer_callback():
    """
    Timer callback for delayed cleanup.
    """
    try:
        _perform_cleanup_lumiflow_collections()
    except Exception:
        pass
    return None  # Don't repeat the timer


def lumi_reset_highlight(scene: bpy.types.Scene):
    """Reset all highlight status flags and force viewport redraw - used by several positioning operators."""
    scene.lumi_status_hue_active = False
    scene.lumi_status_saturation_active = False
    scene.lumi_status_distance_active = False
    scene.lumi_status_power_active = False
    scene.lumi_status_scale_active = False
    scene.lumi_status_temperature_active = False
    scene.lumi_status_angle_active = False
    
    if bpy is not None:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()


def lumi_move_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection):
    """Move an object to a specific collection - used by light creation operations."""
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)


def lumi_safe_context_override(context: bpy.types.Context, operation_func) -> bool:
    """Safely override context for operations - used by multiple operators."""
    try:
        # Blender 4.x: use temp_override if available
        if hasattr(context, 'temp_override'):
            if context.area and context.area.type == 'VIEW_3D':
                override_context = {
                    'area': context.area,
                    'region': context.region,
                    'space_data': context.space_data
                }
                with context.temp_override(**override_context):
                    return operation_func()
        # Blender 3.6: run directly
        return operation_func()
    except Exception:
        try:
            return operation_func()
        except Exception:
            return False


def lumi_get_object_bounds(obj: bpy.types.Object) -> dict:
    """Get single object bounds - used by template analyzer."""
    try:
        if not obj or obj.type != 'MESH':
            return {
                "min": Vector(),
                "max": Vector(),
                "center": Vector(),
                "dimensions": Vector((1.0, 1.0, 1.0)),
                "diagonal": 1.0,
                "radius": 0.5
            }
        
        # Get world-space bounding box
        bbox_corners = [Vector(corner) @ obj.matrix_world for corner in obj.bound_box]
        
        min_coord = Vector(bbox_corners[0])
        max_coord = Vector(bbox_corners[0])
        
        for corner in bbox_corners:
            for i in range(3):
                min_coord[i] = min(min_coord[i], corner[i])
                max_coord[i] = max(max_coord[i], corner[i])
        
        center = (min_coord + max_coord) * 0.5
        dimensions = max_coord - min_coord
        diagonal = dimensions.length
        radius = diagonal * 0.5
        
        return {
            "min": min_coord,
            "max": max_coord,
            "center": center,
            "dimensions": dimensions,
            "diagonal": diagonal,
            "radius": radius
        }
        
    except Exception:
        return {
            "min": Vector(),
            "max": Vector(),
            "center": Vector(),
            "dimensions": Vector((1.0, 1.0, 1.0)),
            "diagonal": 1.0,
            "radius": 0.5
        }


def lumi_sample_object_material(obj: bpy.types.Object) -> dict:
    """Sample dominant material from object - used by template analyzer."""
    try:
        if not obj or not obj.data or not hasattr(obj.data, 'materials'):
            return {
                "dominant_type": "dielectric",
                "has_emission": False,
                "average_roughness": 0.5,
                "transparency": 0.0
            }
        
        materials = [slot.material for slot in obj.material_slots if slot.material]
        
        if not materials:
            return {
                "dominant_type": "dielectric", 
                "has_emission": False,
                "average_roughness": 0.5,
                "transparency": 0.0
            }
        
        # Simple material analysis (can be enhanced later)
        return {
            "dominant_type": "dielectric", 
            "has_emission": False,
            "average_roughness": 0.5,
            "transparency": 0.0
        }
        
    except Exception:
        return {
            "dominant_type": "dielectric", 
            "has_emission": False,
            "average_roughness": 0.5,
            "transparency": 0.0
        }


def get_addon_path() -> str:
    """Get the LumiFlow addon directory path"""
    import os
    return os.path.dirname(os.path.dirname(__file__))


# Export common utilities
__all__ = [
    'lumi_is_addon_enabled',
    'lumi_get_light_collection', 
    'cleanup_lumiflow_collections',
    'lumi_reset_highlight',
    'lumi_move_to_collection',
    'lumi_safe_context_override',
    'lumi_get_object_bounds',
    'lumi_sample_object_material',
    'get_addon_path'
]

