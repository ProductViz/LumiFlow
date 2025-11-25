# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Background Generator
Creates various types of studio backgrounds (seamless, flat, ground plane).
"""

import bpy
import bmesh
import math
from mathutils import Vector
from enum import Enum
from typing import Optional, Tuple, List


class BackgroundType(Enum):
    """Types of studio backgrounds."""
    WHITE_SEAMLESS = "white_seamless"
    BLACK_SEAMLESS = "black_seamless"
    COLORED_SOLID = "colored_solid"
    GRADIENT = "gradient"
    TEXTURED = "textured"
    USE_EXISTING = "use_existing"


def get_product_bounds(context) -> Tuple[Vector, Vector, float]:
    """
    Calculate bounds of selected product objects.
    
    Returns:
        Tuple of (center, dimensions, max_dimension)
    """
    selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
    
    if not selected:
        # Default bounds if nothing selected
        return Vector((0, 0, 0)), Vector((2, 2, 2)), 2.0
    
    # Calculate combined bounding box
    min_co = Vector((float('inf'), float('inf'), float('inf')))
    max_co = Vector((float('-inf'), float('-inf'), float('-inf')))
    
    for obj in selected:
        # Get world-space bounding box corners
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        for corner in bbox_corners:
            min_co.x = min(min_co.x, corner.x)
            min_co.y = min(min_co.y, corner.y)
            min_co.z = min(min_co.z, corner.z)
            max_co.x = max(max_co.x, corner.x)
            max_co.y = max(max_co.y, corner.y)
            max_co.z = max(max_co.z, corner.z)
    
    center = (min_co + max_co) / 2
    dimensions = max_co - min_co
    max_dim = max(dimensions.x, dimensions.y, dimensions.z)
    
    return center, dimensions, max_dim


def create_seamless_background(
    context,
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    name: str = "LumiFlow_Background",
    scale_factor: float = 3.0,
    curve_segments: int = 16,
    curve_radius: float = 0.5,
) -> bpy.types.Object:
    """
    Create a seamless cyclorama-style background.
    
    Args:
        context: Blender context
        color: RGB color tuple (0-1 range)
        name: Name for the background object
        scale_factor: How much larger than product (multiplier)
        curve_segments: Number of segments for the curved section
        curve_radius: Radius of the curve (as fraction of height)
    
    Returns:
        Created background object
    """
    center, dimensions, max_dim = get_product_bounds(context)
    
    # Calculate background size
    width = max(dimensions.x, dimensions.y) * scale_factor
    height = dimensions.z * scale_factor
    depth = max(dimensions.x, dimensions.y) * scale_factor * 0.8
    
    # Minimum sizes
    width = max(width, 4.0)
    height = max(height, 3.0)
    depth = max(depth, 3.0)
    
    # Create mesh
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    
    # Link to scene
    context.collection.objects.link(obj)
    
    # Create geometry with bmesh
    bm = bmesh.new()
    
    # Calculate curve parameters
    curve_r = height * curve_radius
    
    # Create vertices for seamless background
    # Ground plane vertices
    verts = []
    
    # Front edge (at camera side)
    front_y = center.y - depth / 2
    back_y = center.y + depth / 2
    
    half_width = width / 2
    
    # Ground plane (flat section)
    ground_z = center.z - dimensions.z / 2 - 0.01  # Slightly below product
    
    # Create ground vertices
    v_front_left = bm.verts.new((-half_width, front_y, ground_z))
    v_front_right = bm.verts.new((half_width, front_y, ground_z))
    
    # Curve start point
    curve_start_y = back_y - curve_r
    v_curve_start_left = bm.verts.new((-half_width, curve_start_y, ground_z))
    v_curve_start_right = bm.verts.new((half_width, curve_start_y, ground_z))
    
    # Create ground face
    bm.faces.new([v_front_left, v_front_right, v_curve_start_right, v_curve_start_left])
    
    # Create curved section
    prev_left = v_curve_start_left
    prev_right = v_curve_start_right
    
    for i in range(1, curve_segments + 1):
        angle = (math.pi / 2) * (i / curve_segments)
        
        # Calculate position on curve
        y_offset = curve_r * math.sin(angle)
        z_offset = curve_r * (1 - math.cos(angle))
        
        y = curve_start_y + y_offset
        z = ground_z + z_offset
        
        v_left = bm.verts.new((-half_width, y, z))
        v_right = bm.verts.new((half_width, y, z))
        
        # Create face
        bm.faces.new([prev_left, prev_right, v_right, v_left])
        
        prev_left = v_left
        prev_right = v_right
    
    # Create wall section (vertical)
    wall_top_z = ground_z + curve_r + height
    v_top_left = bm.verts.new((-half_width, back_y, wall_top_z))
    v_top_right = bm.verts.new((half_width, back_y, wall_top_z))
    
    # Wall face
    bm.faces.new([prev_left, prev_right, v_top_right, v_top_left])
    
    # Recalculate normals
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # Write to mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Position object
    obj.location = Vector((center.x, 0, 0))
    
    # Create and assign material
    mat = create_background_material(name + "_Material", color)
    obj.data.materials.append(mat)
    
    # Mark as background for LumiFlow detection
    obj["lumiflow_background"] = True
    obj["lumiflow_bg_type"] = "seamless"
    
    # Add to LumiFlow collection if exists
    add_to_lumiflow_collection(context, obj, "Backgrounds")
    
    return obj


def create_flat_backdrop(
    context,
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    name: str = "LumiFlow_Backdrop",
    scale_factor: float = 3.0,
) -> bpy.types.Object:
    """
    Create a simple flat backdrop (vertical plane).
    
    Args:
        context: Blender context
        color: RGB color tuple
        name: Name for the backdrop
        scale_factor: Size multiplier
    
    Returns:
        Created backdrop object
    """
    center, dimensions, max_dim = get_product_bounds(context)
    
    # Calculate size
    width = max(dimensions.x, dimensions.y) * scale_factor
    height = dimensions.z * scale_factor
    
    width = max(width, 4.0)
    height = max(height, 3.0)
    
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    obj = context.active_object
    obj.name = name
    obj.data.name = name
    
    # Scale and rotate to be vertical
    obj.scale = (width, height, 1)
    obj.rotation_euler = (math.pi / 2, 0, 0)
    
    # Position behind product
    obj.location = Vector((
        center.x,
        center.y + max(dimensions.y, dimensions.x) * 1.5,
        center.z + dimensions.z / 4
    ))
    
    # Apply transforms
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Create and assign material
    mat = create_background_material(name + "_Material", color)
    obj.data.materials.append(mat)
    
    # Mark as background
    obj["lumiflow_background"] = True
    obj["lumiflow_bg_type"] = "backdrop"
    
    add_to_lumiflow_collection(context, obj, "Backgrounds")
    
    return obj


def create_ground_plane(
    context,
    color: Tuple[float, float, float] = (0.8, 0.8, 0.8),
    name: str = "LumiFlow_Ground",
    scale_factor: float = 4.0,
    reflective: bool = False,
) -> bpy.types.Object:
    """
    Create a ground plane.
    
    Args:
        context: Blender context
        color: RGB color tuple
        name: Name for the ground plane
        scale_factor: Size multiplier
        reflective: Whether to make it reflective
    
    Returns:
        Created ground plane object
    """
    center, dimensions, max_dim = get_product_bounds(context)
    
    # Calculate size
    size = max(dimensions.x, dimensions.y) * scale_factor
    size = max(size, 5.0)
    
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    obj = context.active_object
    obj.name = name
    obj.data.name = name
    
    # Position at bottom of product
    obj.location = Vector((
        center.x,
        center.y,
        center.z - dimensions.z / 2 - 0.01
    ))
    
    # Create material
    if reflective:
        mat = create_reflective_material(name + "_Material", color)
    else:
        mat = create_background_material(name + "_Material", color)
    
    obj.data.materials.append(mat)
    
    # Mark as background
    obj["lumiflow_background"] = True
    obj["lumiflow_bg_type"] = "ground"
    
    add_to_lumiflow_collection(context, obj, "Backgrounds")
    
    return obj


def create_background_material(
    name: str,
    color: Tuple[float, float, float],
    roughness: float = 1.0,
) -> bpy.types.Material:
    """
    Create a simple diffuse material for backgrounds.
    
    Args:
        name: Material name
        color: RGB color
        roughness: Surface roughness (1.0 = fully diffuse)
    
    Returns:
        Created material
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Specular IOR Level'].default_value = 0.0
    
    # Connect
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat


def create_reflective_material(
    name: str,
    color: Tuple[float, float, float],
    roughness: float = 0.1,
) -> bpy.types.Material:
    """
    Create a reflective material for ground planes.
    
    Args:
        name: Material name
        color: RGB color
        roughness: Surface roughness
    
    Returns:
        Created material
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat


def create_gradient_material(
    name: str,
    color_top: Tuple[float, float, float],
    color_bottom: Tuple[float, float, float],
) -> bpy.types.Material:
    """
    Create a gradient material.
    
    Args:
        name: Material name
        color_top: Top color RGB
        color_bottom: Bottom color RGB
    
    Returns:
        Created material
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Roughness'].default_value = 1.0
    bsdf.inputs['Specular IOR Level'].default_value = 0.0
    
    # Color ramp for gradient
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (0, 0)
    ramp.color_ramp.elements[0].color = (*color_bottom, 1.0)
    ramp.color_ramp.elements[1].color = (*color_top, 1.0)
    
    # Texture coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)
    
    # Separate XYZ to get Z (vertical)
    separate = nodes.new('ShaderNodeSeparateXYZ')
    separate.location = (-200, 0)
    
    # Connect
    links.new(tex_coord.outputs['Generated'], separate.inputs['Vector'])
    links.new(separate.outputs['Z'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat


def add_to_lumiflow_collection(
    context,
    obj: bpy.types.Object,
    subcollection_name: str = "Backgrounds"
) -> None:
    """
    Add object to LumiFlow collection structure.
    
    Args:
        context: Blender context
        obj: Object to add
        subcollection_name: Name of subcollection
    """
    # Find or create LumiFlow collection
    lumiflow_coll = None
    for coll in bpy.data.collections:
        if coll.name.startswith("LumiFlow"):
            lumiflow_coll = coll
            break
    
    if not lumiflow_coll:
        lumiflow_coll = bpy.data.collections.new("LumiFlow")
        context.scene.collection.children.link(lumiflow_coll)
    
    # Find or create subcollection
    bg_coll = None
    for child in lumiflow_coll.children:
        if child.name == subcollection_name:
            bg_coll = child
            break
    
    if not bg_coll:
        bg_coll = bpy.data.collections.new(subcollection_name)
        lumiflow_coll.children.link(bg_coll)
    
    # Unlink from current collections and link to background collection
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    bg_coll.objects.link(obj)


def get_existing_backgrounds(context) -> List[bpy.types.Object]:
    """
    Get all existing LumiFlow background objects in scene.
    
    Returns:
        List of background objects
    """
    backgrounds = []
    for obj in context.scene.objects:
        if obj.get("lumiflow_background"):
            backgrounds.append(obj)
    return backgrounds


def remove_background(obj: bpy.types.Object) -> None:
    """
    Remove a background object and its material.
    
    Args:
        obj: Background object to remove
    """
    # Remove materials
    for mat in obj.data.materials:
        if mat and mat.users == 1:
            bpy.data.materials.remove(mat)
    
    # Remove mesh data
    mesh = obj.data
    bpy.data.objects.remove(obj)
    
    if mesh and mesh.users == 0:
        bpy.data.meshes.remove(mesh)
