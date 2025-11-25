# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Light Linking Utilities
Provides light linking functionality for Blender 4.0+ to separate
product and background lighting layers.
"""

import bpy
from typing import List, Optional, Set, Dict, Any


def is_light_linking_available() -> bool:
    """Check if light linking is available in current Blender version."""
    # Light linking was introduced in Blender 4.0
    return bpy.app.version >= (4, 0, 0)


def get_or_create_collection(name: str) -> bpy.types.Collection:
    """Get existing collection or create new one."""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    return bpy.data.collections.new(name)


def add_objects_to_collection(
    collection: bpy.types.Collection,
    objects: List[bpy.types.Object]
) -> None:
    """Add objects to collection if not already present."""
    for obj in objects:
        if obj.name not in collection.objects:
            try:
                collection.objects.link(obj)
            except RuntimeError:
                # Object already in collection
                pass


def remove_objects_from_collection(
    collection: bpy.types.Collection,
    objects: List[bpy.types.Object]
) -> None:
    """Remove objects from collection."""
    for obj in objects:
        if obj.name in collection.objects:
            try:
                collection.objects.unlink(obj)
            except RuntimeError:
                pass


def setup_light_linking_blocker(
    light: bpy.types.Object,
    blocked_objects: List[bpy.types.Object],
    collection_suffix: str = "_blocker"
) -> Optional[bpy.types.Collection]:
    """
    Setup light linking to block light from affecting certain objects.
    
    Args:
        light: Light object to configure
        blocked_objects: Objects that should not receive light
        collection_suffix: Suffix for blocker collection name
    
    Returns:
        Created blocker collection or None if not available
    """
    if not is_light_linking_available():
        return None
    
    if not hasattr(light, "light_linking"):
        return None
    
    if not blocked_objects:
        return None
    
    # Create blocker collection
    blocker_name = f"{light.name}{collection_suffix}"
    blocker_coll = get_or_create_collection(blocker_name)
    
    # Add blocked objects
    add_objects_to_collection(blocker_coll, blocked_objects)
    
    # Assign to light
    try:
        light.light_linking.blocker_collection = blocker_coll
    except Exception:
        return None
    
    return blocker_coll


def setup_light_linking_receiver(
    light: bpy.types.Object,
    receiver_objects: List[bpy.types.Object],
    collection_suffix: str = "_receiver"
) -> Optional[bpy.types.Collection]:
    """
    Setup light linking to only affect certain objects.
    
    Args:
        light: Light object to configure
        receiver_objects: Objects that should receive light (exclusive)
        collection_suffix: Suffix for receiver collection name
    
    Returns:
        Created receiver collection or None if not available
    """
    if not is_light_linking_available():
        return None
    
    if not hasattr(light, "light_linking"):
        return None
    
    if not receiver_objects:
        return None
    
    # Create receiver collection
    receiver_name = f"{light.name}{collection_suffix}"
    receiver_coll = get_or_create_collection(receiver_name)
    
    # Add receiver objects
    add_objects_to_collection(receiver_coll, receiver_objects)
    
    # Assign to light
    try:
        light.light_linking.receiver_collection = receiver_coll
    except Exception:
        return None
    
    return receiver_coll


def clear_light_linking(light: bpy.types.Object) -> None:
    """Clear all light linking from a light."""
    if not is_light_linking_available():
        return
    
    if not hasattr(light, "light_linking"):
        return
    
    try:
        # Clear collections
        if light.light_linking.blocker_collection:
            coll_name = light.light_linking.blocker_collection.name
            light.light_linking.blocker_collection = None
            # Remove empty collection
            if coll_name in bpy.data.collections:
                coll = bpy.data.collections[coll_name]
                if len(coll.objects) == 0:
                    bpy.data.collections.remove(coll)
        
        if light.light_linking.receiver_collection:
            coll_name = light.light_linking.receiver_collection.name
            light.light_linking.receiver_collection = None
            if coll_name in bpy.data.collections:
                coll = bpy.data.collections[coll_name]
                if len(coll.objects) == 0:
                    bpy.data.collections.remove(coll)
    except Exception:
        pass


def apply_layer_isolation(
    context,
    product_lights: List[bpy.types.Object],
    background_lights: List[bpy.types.Object],
    product_objects: List[bpy.types.Object],
    background_objects: List[bpy.types.Object],
    mode: str = "isolated",
    allow_rim_spill: bool = False
) -> Dict[str, Any]:
    """
    Apply layer isolation between product and background.
    
    Args:
        context: Blender context
        product_lights: Lights in product layer
        background_lights: Lights in background layer
        product_objects: Product mesh objects
        background_objects: Background mesh objects
        mode: 'natural', 'isolated', or 'hybrid'
        allow_rim_spill: Allow BG lights to create rim on product (hybrid mode)
    
    Returns:
        Dictionary with results and any warnings
    """
    result = {
        "success": True,
        "warnings": [],
        "product_lights_configured": 0,
        "background_lights_configured": 0,
    }
    
    if not is_light_linking_available():
        result["success"] = False
        result["warnings"].append("Light linking requires Blender 4.0+")
        return result
    
    if mode == "natural":
        # Natural mode - clear any existing light linking
        for light in product_lights + background_lights:
            clear_light_linking(light)
        return result
    
    # Isolated or Hybrid mode
    # Product lights should not affect background
    for light in product_lights:
        blocker = setup_light_linking_blocker(
            light, 
            background_objects,
            "_bg_blocker"
        )
        if blocker:
            result["product_lights_configured"] += 1
    
    # Background lights should not affect product (unless rim spill allowed)
    for light in background_lights:
        if mode == "hybrid" and allow_rim_spill:
            # In hybrid mode with rim spill, check if this is a rim light
            if "rim" in light.name.lower() or "accent" in light.name.lower():
                # Allow this light to affect product
                continue
        
        blocker = setup_light_linking_blocker(
            light,
            product_objects,
            "_product_blocker"
        )
        if blocker:
            result["background_lights_configured"] += 1
    
    return result


def get_light_layer(light: bpy.types.Object) -> str:
    """
    Determine which layer a light belongs to.
    
    Returns:
        'product', 'background', 'ambient', or 'unknown'
    """
    # Check custom property first
    layer = light.get("lumiflow_layer")
    if layer:
        return layer
    
    # Check if it's a background light
    if light.get("lumiflow_bg_light"):
        return "background"
    
    # Infer from name
    name_lower = light.name.lower()
    
    if any(kw in name_lower for kw in ["bg", "background", "backdrop"]):
        return "background"
    
    if any(kw in name_lower for kw in ["ambient", "world", "env"]):
        return "ambient"
    
    if any(kw in name_lower for kw in ["key", "fill", "rim", "product", "main"]):
        return "product"
    
    return "unknown"


def categorize_scene_lights(context) -> Dict[str, List[bpy.types.Object]]:
    """
    Categorize all lights in scene by layer.
    
    Returns:
        Dictionary with 'product', 'background', 'ambient', 'unknown' keys
    """
    categories = {
        "product": [],
        "background": [],
        "ambient": [],
        "unknown": [],
    }
    
    for obj in context.scene.objects:
        if obj.type == 'LIGHT':
            layer = get_light_layer(obj)
            categories[layer].append(obj)
    
    return categories


def get_background_objects(context) -> List[bpy.types.Object]:
    """Get all background objects in scene."""
    backgrounds = []
    for obj in context.scene.objects:
        if obj.type == 'MESH':
            # Check custom property
            if obj.get("lumiflow_background"):
                backgrounds.append(obj)
                continue
            
            # Check name patterns
            name_lower = obj.name.lower()
            if any(kw in name_lower for kw in ["background", "backdrop", "cyclorama", "seamless"]):
                backgrounds.append(obj)
    
    return backgrounds


def get_product_objects(context) -> List[bpy.types.Object]:
    """Get product objects (selected meshes that are not backgrounds)."""
    backgrounds = set(get_background_objects(context))
    products = []
    
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj not in backgrounds:
            products.append(obj)
    
    # If nothing selected, try to find non-background meshes
    if not products:
        for obj in context.scene.objects:
            if obj.type == 'MESH' and obj not in backgrounds:
                # Skip very large objects (likely environment)
                dims = obj.dimensions
                if max(dims) < 50:  # Reasonable product size
                    products.append(obj)
    
    return products


class LUMI_OT_apply_layer_isolation(bpy.types.Operator):
    """Apply light linking isolation between layers"""
    bl_idname = "lumi.apply_layer_isolation"
    bl_label = "Apply Layer Isolation"
    bl_description = "Apply light linking to separate product and background lighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('natural', "Natural", "No isolation - lights affect everything"),
            ('isolated', "Isolated", "Full separation between layers"),
            ('hybrid', "Hybrid", "Separation with rim spill allowed"),
        ],
        default='isolated',
    )
    
    @classmethod
    def poll(cls, context):
        return is_light_linking_available()
    
    def execute(self, context):
        # Get objects and lights
        product_objects = get_product_objects(context)
        background_objects = get_background_objects(context)
        light_categories = categorize_scene_lights(context)
        
        if not product_objects:
            self.report({'WARNING'}, "No product objects found")
            return {'CANCELLED'}
        
        if not background_objects:
            self.report({'WARNING'}, "No background objects found")
            return {'CANCELLED'}
        
        # Apply isolation
        result = apply_layer_isolation(
            context,
            product_lights=light_categories["product"],
            background_lights=light_categories["background"],
            product_objects=product_objects,
            background_objects=background_objects,
            mode=self.mode,
            allow_rim_spill=(self.mode == 'hybrid'),
        )
        
        if result["warnings"]:
            for warning in result["warnings"]:
                self.report({'WARNING'}, warning)
        
        total = result["product_lights_configured"] + result["background_lights_configured"]
        self.report({'INFO'}, f"Configured {total} lights for {self.mode} mode")
        
        return {'FINISHED'}


class LUMI_OT_clear_layer_isolation(bpy.types.Operator):
    """Clear all light linking isolation"""
    bl_idname = "lumi.clear_layer_isolation"
    bl_label = "Clear Layer Isolation"
    bl_description = "Remove all light linking from scene lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return is_light_linking_available()
    
    def execute(self, context):
        count = 0
        for obj in context.scene.objects:
            if obj.type == 'LIGHT':
                clear_light_linking(obj)
                count += 1
        
        self.report({'INFO'}, f"Cleared light linking from {count} lights")
        return {'FINISHED'}


# Registration
classes = [
    LUMI_OT_apply_layer_isolation,
    LUMI_OT_clear_layer_isolation,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
