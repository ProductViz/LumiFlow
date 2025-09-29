import bpy
import gpu
import bmesh
from gpu_extras.batch import batch_for_shader
import blf
import math
from mathutils import Vector, Quaternion
from typing import List, Tuple, Optional
from bpy_extras import view3d_utils

from .config import OverlayConfig
from ..utils import lumi_get_light_pivot, lumi_get_viewport_camera_position

# ============================================================================
# LIGHT VISUALIZATION FUNCTIONS
# ============================================================================

def draw_point_light_circle(center_world: Vector, radius: float, region=None, rv3d=None, batch_shapes=None):
    """Draw circle for POINT light that matches Blender's default overlay size.
    The circle maintains consistent world-space size relative to viewport zoom."""
    # Get view rotation matrix to orient circle towards camera
    view_rot = rv3d.view_matrix.to_3x3().inverted()
    x_axis = view_rot @ Vector((1, 0, 0))
    y_axis = view_rot @ Vector((0, 1, 0))
    
    main_points = []
    for i in range(32):
        angle = 2 * math.pi * i / 32
        offset_x = math.cos(angle) * radius
        offset_y = math.sin(angle) * radius
        world_offset = x_axis * offset_x + y_axis * offset_y
        point = center_world + world_offset
        main_points.append(point)
    
    # Draw the main circle
    for i in range(len(main_points)):
        batch_shapes.extend([main_points[i], main_points[(i + 1) % len(main_points)]])
    
    # Draw small center circle (screen space - constant size like Blender)
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, center_world)
    if screen_pos:
        # Fixed screen radius for center circle (like Blender default)
        screen_radius = 3.0  # pixels - stays same size regardless of zoom
        center_points = []
        for i in range(12):  # Less segments for small circle
            angle = 2 * math.pi * i / 12
            offset = Vector((math.cos(angle), math.sin(angle))) * screen_radius
            screen = screen_pos + offset
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen)
            ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen)
            depth = (center_world - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
            point = ray_origin + ray_dir * depth
            center_points.append(point)
        
        # Draw the small center circle
        for i in range(len(center_points)):
            batch_shapes.extend([center_points[i], center_points[(i + 1) % len(center_points)]])

def draw_viewport_facing_circle(center_world: Vector, radius: float, cam_pos: Vector, region, rv3d, batch_shapes):
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, center_world)
    if not screen_pos:
        return
        
    scale_factor = 10000
    points = []
    for i in range(24):
        angle = 2 * math.pi * i / 24
        offset = Vector((math.cos(angle), math.sin(angle))) * (radius * scale_factor)
        screen = screen_pos + offset
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen)
        ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen)
        depth = (center_world - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        point = ray_origin + ray_dir * depth
        points.append(point)
        
    for i in range(len(points)):
        batch_shapes.extend([points[i], points[(i + 1) % len(points)]])

def draw_screen_aligned_circle(center_world: Vector, radius: float = 0.00001, color: tuple = (1, 0.5, 0.2, 1), region=None, rv3d=None, batch_shapes=None):
    """Draw screen-aligned circle using OverlayConfig."""
    # Get default color from config if not specified
    if color == (1, 0.5, 0.2, 1):
        color = OverlayConfig.get_color('screen_aligned_circle', (1, 0.5, 0.2, 1))
    
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, center_world)
    if not screen_pos:
        return
        
    scale_factor = 10000
    points = []
    for i in range(24):
        angle = 2 * math.pi * i / 24
        offset = Vector((math.cos(angle), math.sin(angle))) * (radius * scale_factor)
        screen = screen_pos + offset
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen)
        ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen)
        depth = (center_world - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        point = ray_origin + ray_dir * depth
        points.append(point)
        
    for i in range(0, len(points), 2):
        if i + 1 < len(points):
            batch_shapes.extend([points[i], points[i + 1]])

def draw_sun_icon(center: Vector, region=None, rv3d=None, batch_shapes=None):
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, center)
    if not screen_pos:
        return
        
    scale_factor = 10000
    radius = 0.001
    
    points = []
    for i in range(32):
        angle = 2 * math.pi * i / 32
        offset = Vector((math.cos(angle), math.sin(angle))) * (radius * scale_factor)
        screen = screen_pos + offset
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen)
        ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen)
        depth = (center - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        point = ray_origin + ray_dir * depth
        points.append(point)
        
    for i in range(len(points)):
        batch_shapes.extend([points[i], points[(i + 1) % len(points)]])

    for i in range(8):
        angle = 2 * math.pi * i / 8
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        offset_inner = Vector((cos_a, sin_a)) * (1.2 * radius * scale_factor)
        offset_outer = Vector((cos_a, sin_a)) * (1.6 * radius * scale_factor)

        ray_origin_inner = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen_pos + offset_inner)
        ray_dir_inner = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen_pos + offset_inner)
        depth_inner = (center - ray_origin_inner).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        point_inner = ray_origin_inner + ray_dir_inner * depth_inner
        
        ray_origin_outer = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen_pos + offset_outer)
        ray_dir_outer = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen_pos + offset_outer)
        depth_outer = (center - ray_origin_outer).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        point_outer = ray_origin_outer + ray_dir_outer * depth_outer
        batch_shapes.extend([point_inner, point_outer])

def draw_circle(center: Vector, normal: Vector, radius: float, segments: int = 32, color: tuple = (1, 1, 0, 1), basis_x: Vector = None, basis_y: Vector = None, batch_shapes=None):
    """Draw a circle with customizable parameters using OverlayConfig."""
    if batch_shapes is None:
        return
        
    # Get segments from config if not specified
    if segments == 32:
        segments = OverlayConfig.get_drawing_setting('circle_segments', 32)
    
    # Get default color from config if not specified
    if color == (1, 1, 0, 1):
        color = OverlayConfig.get_color('circle_default', (1, 1, 0, 1))
    
    # Create basis vectors if not provided
    if basis_x is None or basis_y is None:
        # Create arbitrary perpendicular vectors
        if abs(normal.z) < 0.9:
            basis_x = normal.cross(Vector((0, 0, 1))).normalized()
        else:
            basis_x = normal.cross(Vector((1, 0, 0))).normalized()
        basis_y = normal.cross(basis_x).normalized()
    
    # Create circle vertices
    vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pos = center + basis_x * x + basis_y * y
        vertices.append(pos)
    
    # Add to batch if provided
    if batch_shapes is not None:
        for i in range(segments):
            batch_shapes.extend([vertices[i], vertices[(i + 1) % segments]])

def draw_area_overlay(light, target_pos: Vector, batch_shapes=None):
    light_matrix = light.matrix_world
    local_x = light_matrix.col[0].to_3d().normalized()  # X axis lampu (size)
    local_y = light_matrix.col[1].to_3d().normalized()  # Y axis lampu (size_y)
    local_z = light_matrix.col[2].to_3d().normalized()  # Z axis lampu (arah sinar = -Z)
    
    x_axis = local_x
    y_axis = local_y
    
    shape = light.data.shape
    size_x = light.data.size
    size_y = getattr(light.data, "size_y", size_x)
    hx = size_x / 2
    
    if shape in {'SQUARE', 'DISK'}:
        hy = hx  # Force square/circular shape
    else:
        hy = size_y / 2
    
    if shape in {'SQUARE', 'RECTANGLE', 'ELLIPSE'}:
        if shape == 'ELLIPSE':
            segments = 32
            points = []
            for i in range(segments + 1):
                angle = 2 * math.pi * i / segments
                point = light.location + (math.cos(angle) * hx * x_axis + math.sin(angle) * hy * y_axis)
                points.append(point)
            for i in range(segments):
                batch_shapes.extend([points[i], points[i + 1]])
        else:
            corners = [
                light.location + x_axis * hx + y_axis * hy,
                light.location - x_axis * hx + y_axis * hy,
                light.location - x_axis * hx - y_axis * hy,
                light.location + x_axis * hx - y_axis * hy,
            ]
            for i in range(4):
                batch_shapes.extend([corners[i], corners[(i + 1) % 4]])
    elif shape == 'DISK':
        # Untuk DISK, gunakan normal dari -Z axis lampu  
        # Draw circle directly into batch_shapes untuk konsistensi
        segments = 32
        angle_step = 2 * math.pi / segments
        points = []
        for i in range(segments):
            angle = angle_step * i
            point = light.location + hx * (math.cos(angle) * x_axis + math.sin(angle) * y_axis)
            points.append(point)
        for i in range(segments):
            p1 = points[i]
            p2 = points[(i + 1) % segments]
            batch_shapes.extend([p1, p2])
    else:
        # Fallback: draw as square for unknown shapes
        corners = [
            light.location + x_axis * hx + y_axis * hy,
            light.location - x_axis * hx + y_axis * hy,
            light.location - x_axis * hx - y_axis * hy,
            light.location + x_axis * hx - y_axis * hy,
        ]
        for i in range(4):
            batch_shapes.extend([corners[i], corners[(i + 1) % 4]])

def draw_spot_light_circle(center_world: Vector, radius: float, region=None, rv3d=None, batch_shapes=None):
    """Draw circle for SPOT light that matches Blender's default overlay size.
    Similar to POINT light but for SPOT light at the source."""
    # Get view rotation matrix to orient circle towards camera
    view_rot = rv3d.view_matrix.to_3x3().inverted()
    x_axis = view_rot @ Vector((1, 0, 0))
    y_axis = view_rot @ Vector((0, 1, 0))
    
    # Draw main circle based on shadow_soft_size (world space)
    world_radius = max(0.05, radius)  # minimum radius for visibility
    segments = 32
    
    # Main circle points (world space - changes with zoom)
    main_points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        offset_x = math.cos(angle) * world_radius
        offset_y = math.sin(angle) * world_radius
        world_offset = x_axis * offset_x + y_axis * offset_y
        point = center_world + world_offset
        main_points.append(point)
    
    # Draw the main circle
    for i in range(len(main_points)):
        batch_shapes.extend([main_points[i], main_points[(i + 1) % len(main_points)]])
    
    # Draw small center circle (screen space - constant size like Blender)
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, center_world)
    if screen_pos:
        # Fixed screen radius for center circle (like Blender default)
        screen_radius = 3.0  # pixels - stays same size regardless of zoom
        center_points = []
        for i in range(12):  # Less segments for small circle
            angle = 2 * math.pi * i / 12
            offset = Vector((math.cos(angle), math.sin(angle))) * screen_radius
            screen = screen_pos + offset
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen)
            ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen)
            depth = (center_world - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
            point = ray_origin + ray_dir * depth
            center_points.append(point)
        
        # Draw the small center circle
        for i in range(len(center_points)):
            batch_shapes.extend([center_points[i], center_points[(i + 1) % len(center_points)]])
    else:
        # Fallback: draw very small world-space circle if screen conversion fails
        center_radius = 0.01
        center_points = []
        for i in range(12):
            angle = 2 * math.pi * i / 12
            offset_x = math.cos(angle) * center_radius
            offset_y = math.sin(angle) * center_radius
            world_offset = x_axis * offset_x + y_axis * offset_y
            point = center_world + world_offset
            center_points.append(point)
        
        for i in range(len(center_points)):
            batch_shapes.extend([center_points[i], center_points[(i + 1) % len(center_points)]])

def draw_spot_cone(light, target_pos: Vector, cam_pos: Vector, region=None, rv3d=None, batch_lines=None, batch_shapes=None):
    direction = (target_pos - light.location).normalized()
    angle = light.data.spot_size
    blend = light.data.spot_blend
    distance = 5.0
    cone_base = light.location + direction * distance
    cone_radius = math.tan(angle / 2) * distance
    blend_radius = cone_radius * (1 - blend)

    draw_spot_light_circle(light.location, light.data.shadow_soft_size, region=region, rv3d=rv3d, batch_shapes=batch_shapes)
    draw_circle(cone_base, direction, cone_radius, batch_shapes=batch_shapes)
    
    # Get blend color from config
    blend_color = OverlayConfig.get_color('spot_blend', (0.5, 0.8, 1, 1))
    draw_circle(cone_base, direction, blend_radius, color=blend_color, batch_shapes=batch_shapes)

    batch_lines.extend([light.location, cone_base])

    # Arah kamera dalam world space (negatif Z)
    view_dir = rv3d.view_rotation @ Vector((0, 0, -1))
    
   # Proyeksikan arah kamera ke bidang tegak lurus arah lampu
    proj = view_dir - direction * view_dir.dot(direction)
    if proj.length < 1e-6:
        proj = direction.orthogonal()
    else:
        proj.normalize()

    # Dot product: seberapa sejajar arah lampu dengan kamera
    dot_dir = direction.dot(view_dir)
    abs_dot = abs(dot_dir)

    # Cek apakah light berhadapan langsung dengan kamera (dot product mendekati -1)
    facing_threshold = 0.75  # threshold untuk light berhadapan dengan kamera
    if dot_dir < -facing_threshold:
        return  # tidak menggambar garis cone jika light berhadapan dengan kamera

    # Ambang sejajar: jika kamera hampir sejajar dengan arah lampu, sudut cone menyempit
    threshold = 0.7
    max_angle = math.pi / 2  # sudut maksimal (36 derajat)
    min_angle = 0  # sudut minimal agar tidak benar-benar menutup

    # Interpolasi sudut offset berdasarkan seberapa sejajar
    if abs_dot > threshold:
        # Semakin sejajar, sudut makin kecil
        t = (abs_dot - threshold) / (1 - threshold)
        t = min(max(t, 0.0), 1.0)
        angle_offset = (1 - t) * max_angle + t * min_angle
    else:
        angle_offset = max_angle

    if angle_offset < 1:
        q1 = Quaternion(direction, angle_offset)
        q2 = Quaternion(direction, -angle_offset)
    else:
        q1 = Quaternion(direction, -max_angle)
        q2 = Quaternion(direction, max_angle)

    edge1 = cone_base + (q1 @ proj) * cone_radius
    edge2 = cone_base + (q2 @ proj) * cone_radius

    edge_distance = (edge1 - edge2).length
    if edge_distance < 2.0:  # tidak digambar jika terlalu sempit
        return

    # Tambahkan garis cone
    batch_shapes.extend([light.location, edge1])
    batch_shapes.extend([light.location, edge2])

def draw_sign(location: Vector, size: float = 0.1, color: tuple = (1, 1, 1, 1), region=None, rv3d=None, batch_lines=None):
    """Draw sign indicator at target position using OverlayConfig."""
    if batch_lines is None:
        return
    
    # Get default size from config if not specified
    if size == 0.1:
        size = OverlayConfig.get_light_setting('plus_sign_size', 0.1)
    
    # Get default color from config if not specified
    if color == (1, 1, 1, 1):
        color = OverlayConfig.get_color('plus_sign', (1, 1, 1, 1))
    
    # Create screen-aligned plus sign
    screen_pos = view3d_utils.location_3d_to_region_2d(region, rv3d, location)
    if not screen_pos:
        return
    
    # Create plus sign in screen space
    half_size = size * 150  # Scale for screen visibility
    screen_points = [
        screen_pos + Vector((-half_size, 0)),      # Left
        screen_pos + Vector((half_size, 0)),       # Right
        screen_pos + Vector((0, -half_size)),      # Bottom
        screen_pos + Vector((0, half_size))        # Top
    ]
    
    # Convert screen points back to world space at the depth of original location
    world_points = []
    for screen_point in screen_points:
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen_point)
        ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen_point)
        depth = (location - ray_origin).dot(rv3d.view_rotation @ Vector((0, 0, -1)))
        world_point = ray_origin + ray_dir * depth
        world_points.append(world_point)
    
    # Add horizontal line (left to right)
    batch_lines.extend([world_points[0], world_points[1]])
    # Add vertical line (bottom to top)
    batch_lines.extend([world_points[2], world_points[3]])

# calculate_target_position moved to utils/light.py as lumi_calculate_light_target_position

def draw_light_visualization(light, target_pos: Vector, cam_pos: Vector, region=None, rv3d=None, batch_lines=None, batch_shapes=None):
    """Draw visualization for a single light based on its type using OverlayConfig."""
    # Get target size from config
    target_size = OverlayConfig.get_light_setting('target_size', 0.05)
    draw_sign(target_pos, size=target_size, region=region, rv3d=rv3d, batch_lines=batch_lines)
    batch_lines.extend([light.location, target_pos])
    ltype = light.data.type

    if ltype == 'POINT':
        point_radius = OverlayConfig.get_light_setting('point_radius', 0.1)
        draw_point_light_circle(light.location, light.data.shadow_soft_size, region, rv3d, batch_shapes)

    elif ltype == 'SUN':
        sun_size = OverlayConfig.get_light_setting('sun_size', 0.2)
        draw_sun_icon(light.location, region=region, rv3d=rv3d, batch_shapes=batch_shapes)

    elif ltype == 'SPOT':
        spot_radius = OverlayConfig.get_light_setting('spot_radius', 0.1)
        draw_spot_cone(light, target_pos, cam_pos, region=region, rv3d=rv3d, batch_lines=batch_lines, batch_shapes=batch_shapes)

    elif ltype == 'AREA':
        area_size = OverlayConfig.get_light_setting('area_size', 0.5)
        draw_area_overlay(light, target_pos, batch_shapes=batch_shapes)
        draw_screen_aligned_circle(light.location, radius=0.001, region=region, rv3d=rv3d, batch_shapes=batch_shapes)

def render_batches(shader, batch_lines, batch_shapes):
    """Render the accumulated line and shape batches."""
    if batch_lines:
        shader.bind()
        shader.uniform_float("color", OverlayConfig.get_color('highlight'))
        batch = batch_for_shader(shader, 'LINES', {"pos": batch_lines})
        batch.draw(shader)

    if batch_shapes:
        shader.bind()
        shader.uniform_float("color", OverlayConfig.get_light_color('selected'))
        batch = batch_for_shader(shader, 'LINES', {"pos": batch_shapes})
        batch.draw(shader)

def initialize_drawing_context():
    """Initialize drawing context including region, shader, and batch arrays."""
    region = bpy.context.region
    rv3d = bpy.context.region_data
    if not region or not rv3d:
        return None, None, None, None, None, None
    
    context = bpy.context
    scene = context.scene
    # # Ambil objek yang dipilih dalam scene
    selected_objects = context.selected_objects
    # # Periksa apakah objek adalah lampu
    lights = [obj for obj in selected_objects if obj.type == 'LIGHT']
    if not lights:
        return None, None, None, None, None, None
    
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch_lines = []
    batch_shapes = []
    cam_pos = lumi_get_viewport_camera_position(rv3d)
    
    return region, rv3d, scene, lights, shader, batch_lines, batch_shapes, cam_pos

# ============================================================================
# LIGHT LINES AND VISUALIZATION
# ============================================================================

def lumi_draw_light_lines():
    """Draw light visualization lines, shapes, and indicators using OverlayConfig."""
    context = bpy.context
    region = context.region
    rv3d = context.region_data
    
    if not region or not rv3d:
        return
    
    scene = context.scene
    
    # Get selected lights - don't return early if none selected
    selected_objects = context.selected_objects
    lights = [obj for obj in selected_objects if obj.type == 'LIGHT']
    
    # Initialize drawing components
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch_lines = []
    batch_shapes = []
    cam_pos = lumi_get_viewport_camera_position(rv3d)

    # Main light drawing logic - only if lights are selected
    for light in lights:
        # Calculate target position for light
        from ..utils.light import lumi_calculate_light_target_position
        target_pos = lumi_calculate_light_target_position(light, scene)
        
        # Draw visualization for this light
        draw_light_visualization(light, target_pos, cam_pos, region, rv3d, batch_lines, batch_shapes)

    # Render all accumulated batches
    render_batches(shader, batch_lines, batch_shapes)

