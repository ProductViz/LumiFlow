"""
Mesh Overlay Module
Contains mesh stroke and object outline functions.
"""

import bpy
import bmesh
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from .config import OverlayConfig

def _draw_scene_object_strokes_if_no_lights():
    """Draw scene object outlines when viewport shading is RENDERED and there are no lights using OverlayConfig."""
    context = bpy.context
    region = context.region
    rv3d = context.region_data
    
    if not region or not rv3d:
        return
    
    # Check if viewport is in RENDERED shading
    if context.space_data.shading.type != 'RENDERED':
        return
    
    # Check if there are any lights in the scene
    light_objects = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
    if light_objects:
        return
    
    # Get stroke color from config
    stroke_color = OverlayConfig.get_color('mesh_stroke', (0.8, 0.8, 0.8, 0.5))
    
    # Collect all mesh objects
    mesh_objects = [obj for obj in context.visible_objects if obj.type == 'MESH']
    
    if not mesh_objects:
        return
    
    # Prepare to collect stroke lines
    lines = []
    
    # Process each mesh object
    for obj in mesh_objects:
        if not obj.data or not obj.data.polygons:
            continue
        
        # Create evaluated mesh for deformed objects
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        
        # Create bmesh from evaluated mesh
        bm = bmesh.new()
        try:
            bm.from_mesh(eval_obj.data)
            
            # Get world matrix
            mw = eval_obj.matrix_world
            
            # Get view direction for silhouette detection
            view_direction = rv3d.view_matrix.to_3x3() @ Vector((0, 0, 1))
            view_direction = view_direction.normalized()
            
            # Find silhouette edges (edges between front and back faces)
            for edge in bm.edges:
                if len(edge.link_faces) == 2:
                    # Get the two faces connected by this edge
                    face1, face2 = edge.link_faces
                    
                    # Get face normals in world space
                    normal1 = mw @ face1.normal
                    normal2 = mw @ face2.normal
                    normal1 = normal1.normalized()
                    normal2 = normal2.normalized()
                    
                    # Check if faces are oriented differently relative to view
                    dot1 = normal1.dot(view_direction)
                    dot2 = normal2.dot(view_direction)
                    
                    # If one faces camera and other faces away, it's a silhouette edge
                    if (dot1 > 0) != (dot2 > 0):
                        v1 = mw @ edge.verts[0].co
                        v2 = mw @ edge.verts[1].co
                        lines.extend([v1, v2])
        finally:
            bm.free()
            eval_obj.to_mesh_clear()

    if lines:
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        shader.bind()
        shader.uniform_float("color", stroke_color)
        batch = batch_for_shader(shader, 'LINES', {"pos": lines})
        batch.draw(shader)

