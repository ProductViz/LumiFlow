

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import math
from mathutils import Vector, Color
from typing import List, Tuple, Optional, Dict
from bpy_extras import view3d_utils

from .config import OverlayConfig
from ..core.camera_light_manager import get_camera_light_manager
from ..core.visibility_controller import get_visibility_controller
from ..utils import lumi_is_addon_enabled


class CameraSpecificOverlay:
    """Handles camera-specific light relationship visualizations."""
    
    def __init__(self):
        self._enabled = False
        self._last_camera = None
        self._camera_light_connections = {}
        self._connection_colors = {}
        self._color_index = 0
        
    def enable(self):
        """Enable camera-specific overlay."""
        self._enabled = True
        self._generate_connection_colors()
        
    def disable(self):
        """Disable camera-specific overlay."""
        self._enabled = False
        self._camera_light_connections.clear()
        self._connection_colors.clear()
        self._last_camera = None
        
    def is_enabled(self) -> bool:
        """Check if overlay is enabled."""
        return self._enabled
        
    def _generate_connection_colors(self):
        """Generate distinct colors for camera-light connections."""
        colors = [
            Color((1.0, 0.3, 0.3)),  # Red
            Color((0.3, 1.0, 0.3)),  # Green
            Color((0.3, 0.3, 1.0)),  # Blue
            Color((1.0, 1.0, 0.3)),  # Yellow
            Color((1.0, 0.3, 1.0)),  # Magenta
            Color((0.3, 1.0, 1.0)),  # Cyan
            Color((1.0, 0.6, 0.3)),  # Orange
            Color((0.6, 0.3, 1.0)),  # Purple
            Color((0.3, 1.0, 0.6)),  # Spring Green
            Color((1.0, 0.3, 0.6)),  # Rose
        ]
        
        self._connection_colors = {}
        self._color_index = 0
        
    def _get_camera_color(self, camera_name: str) -> Color:
        """Get a consistent color for a camera."""
        if camera_name not in self._connection_colors:
            if self._color_index < len(self._connection_colors):
                self._connection_colors[camera_name] = self._connection_colors[self._color_index]
            else:
                # Generate random color if we run out of predefined colors
                import random
                self._connection_colors[camera_name] = Color((
                    random.random(), random.random(), random.random()
                ))
            self._color_index += 1
            
        return self._connection_colors[camera_name]
        
    def _update_camera_light_connections(self, context):
        """Update camera-light connection data."""
        if not lumi_is_addon_enabled():
            return
            
        scene = context.scene
        camera_specific_props = getattr(scene, 'lumi_camera_specific_props', None)
        
        if not camera_specific_props or not camera_specific_props.camera_specific_lights_enabled:
            self._camera_light_connections.clear()
            return
            
        # Get camera light manager
        camera_light_manager = get_camera_light_manager()
        
        # Clear previous connections
        self._camera_light_connections.clear()
        
        # Get all cameras and their assigned lights
        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
        
        for camera in cameras:
            assigned_lights = camera_light_manager.get_camera_assigned_lights(camera)
            if assigned_lights:
                self._camera_light_connections[camera.name] = assigned_lights
                
    def _draw_camera_light_connection(self, camera_pos: Vector, light_pos: Vector, 
                                     color: Color, region, rv3d, batch_lines: List):
        """Draw a connection line between camera and light."""
        # Convert 3D positions to 2D screen coordinates
        camera_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, camera_pos)
        light_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, light_pos)
        
        if camera_2d and light_2d:
            # Only draw if both points are visible
            batch_lines.extend([
                (camera_pos, color),
                (light_pos, color)
            ])
            
    def _draw_camera_indicator(self, camera: bpy.types.Object, region, rv3d, batch_shapes: List):
        """Draw a special indicator for cameras with assigned lights."""
        camera_pos = camera.matrix_world.translation
        camera_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, camera_pos)
        
        if camera_2d:
            # Draw a small circle around the camera
            color = self._get_camera_color(camera.name)
            radius = 0.2  # World space radius
            
            # Create circle points
            circle_points = []
            segments = 16
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                
                # Create offset in camera's local space
                offset = camera.matrix_world @ Vector((x, y, 0))
                point = camera_pos + (offset - camera_pos)
                circle_points.append((point, color))
                
            # Add circle lines
            for i in range(len(circle_points)):
                batch_shapes.extend([
                    circle_points[i],
                    circle_points[(i + 1) % len(circle_points)]
                ])
                
    def _draw_light_indicator(self, light: bpy.types.Object, assigned_cameras: List[str], 
                             region, rv3d, batch_shapes: List):
        """Draw indicators for lights assigned to cameras."""
        light_pos = light.matrix_world.translation
        light_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, light_pos)
        
        if light_2d:
            # Draw small indicators for each assigned camera
            indicator_count = len(assigned_cameras)
            for i, camera_name in enumerate(assigned_cameras):
                color = self._get_camera_color(camera_name)
                
                # Position indicators around the light
                angle = 2 * math.pi * i / indicator_count
                offset_distance = 0.15
                
                # Calculate offset position
                offset_x = math.cos(angle) * offset_distance
                offset_y = math.sin(angle) * offset_distance
                
                # Create indicator position
                indicator_pos = light_pos + Vector((offset_x, offset_y, 0))
                
                # Draw small square indicator
                size = 0.05
                square_points = [
                    (indicator_pos + Vector((-size, -size, 0)), color),
                    (indicator_pos + Vector((size, -size, 0)), color),
                    (indicator_pos + Vector((size, size, 0)), color),
                    (indicator_pos + Vector((-size, size, 0)), color),
                    (indicator_pos + Vector((-size, -size, 0)), color)
                ]
                
                for j in range(len(square_points) - 1):
                    batch_shapes.extend([
                        square_points[j],
                        square_points[j + 1]
                    ])
                    
    def _draw_active_camera_highlight(self, context, region, rv3d, batch_shapes: List):
        """Draw highlight for active camera."""
        scene = context.scene
        if not scene.camera:
            return
            
        camera_pos = scene.camera.matrix_world.translation
        camera_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, camera_pos)
        
        if camera_2d:
            # Draw pulsing circle for active camera
            import time
            pulse = abs(math.sin(time.time() * 3))  # 3 Hz pulse
            
            color = Color((1.0, 1.0, 0.0))  # Yellow for active camera
            radius = 0.3 + pulse * 0.1  # Pulsing radius
            
            # Create circle points
            circle_points = []
            segments = 24
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                
                # Create offset in camera's local space
                offset = scene.camera.matrix_world @ Vector((x, y, 0))
                point = camera_pos + (offset - camera_pos)
                circle_points.append((point, color))
                
            # Add circle lines
            for i in range(len(circle_points)):
                batch_shapes.extend([
                    circle_points[i],
                    circle_points[(i + 1) % len(circle_points)]
                ])
                
    def draw_camera_specific_overlay(self, context):
        """Main drawing function for camera-specific overlay."""
        if not self._enabled or not lumi_is_addon_enabled():
            return
            
        scene = context.scene
        camera_specific_props = getattr(scene, 'lumi_camera_specific_props', None)
        
        if not camera_specific_props or not camera_specific_props.camera_specific_lights_enabled:
            return
            
        # Get drawing context
        region = context.region
        rv3d = context.region_data
        
        if not region or not rv3d:
            return
            
        # Update connections if camera changed
        if scene.camera != self._last_camera:
            self._update_camera_light_connections(context)
            self._last_camera = scene.camera
            
        # Initialize batch lists
        batch_lines = []
        batch_shapes = []
        
        # Draw camera-light connections
        for camera_name, lights in self._camera_light_connections.items():
            camera_obj = scene.objects.get(camera_name)
            if not camera_obj:
                continue
                
            camera_pos = camera_obj.matrix_world.translation
            camera_color = self._get_camera_color(camera_name)
            
            for light in lights:
                light_pos = light.matrix_world.translation
                self._draw_camera_light_connection(
                    camera_pos, light_pos, camera_color, region, rv3d, batch_lines
                )
                
        # Draw camera indicators
        for camera_name in self._camera_light_connections.keys():
            camera_obj = scene.objects.get(camera_name)
            if camera_obj:
                self._draw_camera_indicator(camera_obj, region, rv3d, batch_shapes)
                
        # Draw light indicators
        for light in context.scene.objects:
            if light.type == 'LIGHT':
                assigned_cameras = []
                for camera_name, lights in self._camera_light_connections.items():
                    if light in lights:
                        assigned_cameras.append(camera_name)
                        
                if assigned_cameras:
                    self._draw_light_indicator(light, assigned_cameras, region, rv3d, batch_shapes)
                    
        # Draw active camera highlight
        self._draw_active_camera_highlight(context, region, rv3d, batch_shapes)
        
        # Render the batches
        if batch_lines:
            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            batch = batch_for_shader(shader, 'LINES', {
                'pos': [point for point, color in batch_lines],
                'color': [color for point, color in batch_lines]
            })
            shader.bind()
            batch.draw(shader)
            
        if batch_shapes:
            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            batch = batch_for_shader(shader, 'LINES', {
                'pos': [point for point, color in batch_shapes],
                'color': [color for point, color in batch_shapes]
            })
            shader.bind()
            batch.draw(shader)


# Global instance
_camera_specific_overlay = None


def get_camera_specific_overlay() -> CameraSpecificOverlay:
    """Get the global camera-specific overlay instance."""
    global _camera_specific_overlay
    if _camera_specific_overlay is None:
        _camera_specific_overlay = CameraSpecificOverlay()
    return _camera_specific_overlay


def draw_camera_specific_overlay(context):
    """Wrapper function for drawing camera-specific overlay."""
    overlay = get_camera_specific_overlay()
    overlay.draw_camera_specific_overlay(context)


def enable_camera_specific_overlay():
    """Enable camera-specific overlay."""
    overlay = get_camera_specific_overlay()
    overlay.enable()


def disable_camera_specific_overlay():
    """Disable camera-specific overlay."""
    overlay = get_camera_specific_overlay()
    overlay.disable()


def is_camera_specific_overlay_enabled() -> bool:
    """Check if camera-specific overlay is enabled."""
    overlay = get_camera_specific_overlay()
    return overlay.is_enabled()

