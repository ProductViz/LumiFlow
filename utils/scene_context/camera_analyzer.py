"""
CameraAnalyzer - Centralized camera analysis.
Menggantikan logic dari:
- obstruction_detector._analyze_camera()
- scene_analysis.get_camera_frustum_planes()
- template_analyzer.calculate_camera_relation() (partial)
"""

import bpy
import math
from typing import List, Optional
from dataclasses import dataclass
from mathutils import Vector, Matrix


@dataclass
class FrustumPlane:
    """Single frustum plane."""
    normal: Vector
    point: Vector
    type: str  # 'near', 'far', 'left', 'right', 'top', 'bottom'


@dataclass
class CameraData:
    """Complete camera information."""
    location: Vector
    forward: Vector
    up: Vector
    right: Vector
    fov: float
    near_clip: float
    far_clip: float
    matrix: Matrix
    frustum_planes: List[FrustumPlane]
    type: str  # 'PERSP' or 'ORTHO'


class CameraAnalyzer:
    """Centralized camera analysis."""

    def __init__(self, context: bpy.types.Context):
        self.context = context

    def analyze(self, camera: bpy.types.Object) -> CameraData:
        """
        Complete camera analysis.

        Args:
            camera: Camera object

        Returns:
            CameraData with all information
        """
        if not camera or camera.type != 'CAMERA':
            return None

        matrix = camera.matrix_world.copy()

        return CameraData(
            location=matrix.translation.copy(),
            forward=self._get_forward(matrix),
            up=self._get_up(matrix),
            right=self._get_right(matrix),
            fov=self._get_fov(camera),
            near_clip=camera.data.clip_start,
            far_clip=camera.data.clip_end,
            matrix=matrix,
            frustum_planes=self._calculate_frustum_planes(camera, matrix),
            type=camera.data.type
        )

    def is_in_frustum(self, obj: bpy.types.Object,
                     camera_data: CameraData) -> bool:
        """Check if object is in camera frustum."""
        if not obj.bound_box:
            return False

        # Get world bbox corners
        bbox_corners = [obj.matrix_world @ Vector(corner)
                       for corner in obj.bound_box]

        # Check against all frustum planes
        for plane in camera_data.frustum_planes:
            all_outside = True
            for corner in bbox_corners:
                distance = (corner - plane.point).dot(plane.normal)
                if distance >= 0:
                    all_outside = False
                    break

            if all_outside:
                return False  # Object outside this plane

        return True  # Object in frustum

    def _get_forward(self, matrix: Matrix) -> Vector:
        """Get camera forward direction (looks down -Z)."""
        forward_vec = matrix.to_3x3() @ Vector((0, 0, -1))
        return forward_vec.normalized()

    def _get_up(self, matrix: Matrix) -> Vector:
        """Get camera up direction (+Y)."""
        up_vec = matrix.to_3x3() @ Vector((0, 1, 0))
        return up_vec.normalized()

    def _get_right(self, matrix: Matrix) -> Vector:
        """Get camera right direction (+X)."""
        right_vec = matrix.to_3x3() @ Vector((1, 0, 0))
        return right_vec.normalized()

    def _get_fov(self, camera: bpy.types.Object) -> float:
        """Get camera field of view in radians."""
        if camera.data.type == 'PERSP':
            return camera.data.angle
        else:
            return math.radians(60)  # Default for ortho

    def _calculate_frustum_planes(self, camera: bpy.types.Object,
                                  matrix: Matrix) -> List[FrustumPlane]:
        """Calculate 6 frustum planes."""
        planes = []

        cam_pos = matrix.translation
        cam_forward = self._get_forward(matrix)
        cam_up = self._get_up(matrix)
        cam_right = self._get_right(matrix)

        # Near plane
        near_center = cam_pos + cam_forward * camera.data.clip_start
        planes.append(FrustumPlane(cam_forward, near_center, 'near'))

        # Far plane
        far_center = cam_pos + cam_forward * camera.data.clip_end
        planes.append(FrustumPlane(-cam_forward, far_center, 'far'))

        if camera.data.type == 'PERSP':
            # Perspective frustum
            fov = camera.data.angle
            aspect = self.context.scene.render.pixel_aspect_x / \
                    self.context.scene.render.pixel_aspect_y

            half_fov_h = fov / 2
            half_fov_v = math.atan(math.tan(half_fov_h) / aspect)

            # Left/Right/Top/Bottom planes (simplified)
            # Full implementation would calculate exact normals
            planes.append(FrustumPlane(cam_right, cam_pos, 'left'))
            planes.append(FrustumPlane(-cam_right, cam_pos, 'right'))
            planes.append(FrustumPlane(-cam_up, cam_pos, 'top'))
            planes.append(FrustumPlane(cam_up, cam_pos, 'bottom'))
        else:
            # Orthographic frustum
            ortho_scale = camera.data.ortho_scale
            half_scale = ortho_scale / 2

            planes.append(FrustumPlane(cam_right,
                         cam_pos - cam_right * half_scale, 'left'))
            planes.append(FrustumPlane(-cam_right,
                         cam_pos + cam_right * half_scale, 'right'))
            planes.append(FrustumPlane(-cam_up,
                         cam_pos + cam_up * half_scale, 'top'))
            planes.append(FrustumPlane(cam_up,
                         cam_pos - cam_up * half_scale, 'bottom'))

        return planes


__all__ = ['CameraAnalyzer', 'CameraData', 'FrustumPlane']