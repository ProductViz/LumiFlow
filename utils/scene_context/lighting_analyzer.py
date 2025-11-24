"""
LightingAnalyzer - Analisis ringkas semua LIGHT + HDRI di scene
untuk dipakai oleh SceneAnalyzer / SceneContext.
"""

import bpy
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

from mathutils import Vector

from .camera_analyzer import CameraData


@dataclass
class LightingData:
    """Ringkasan lighting di scene."""
    # Inventaris lampu
    point_lights: List[bpy.types.Object]
    spot_lights: List[bpy.types.Object]
    area_lights: List[bpy.types.Object]
    sun_lights: List[bpy.types.Object]

    # HDRI / World
    has_hdri: bool
    hdri_strength: float
    world_color: Tuple[float, float, float]

    # Statistik global
    total_light_count: int
    average_energy: float
    ambient_level: float

    # Peran semantik (heuristik)
    key_light_candidates: List[bpy.types.Object]
    fill_light_candidates: List[bpy.types.Object]
    rim_light_candidates: List[bpy.types.Object]


class LightingAnalyzer:
    """Analisis lighting di scene (lampu + HDRI)."""

    def __init__(self, context: bpy.types.Context):
        self.context = context

    def analyze(
        self,
        camera_data: Optional[CameraData] = None,
        product_center: Optional[Vector] = None,
    ) -> LightingData:
        """Analisis utama lighting.

        Args:
            camera_data: Opsional, dipakai untuk klasifikasi key/fill/rim.
            product_center: Opsional, center produk (mis. bounds.center).
        """
        scene = self.context.scene

        point_lights: List[bpy.types.Object] = []
        spot_lights: List[bpy.types.Object] = []
        area_lights: List[bpy.types.Object] = []
        sun_lights: List[bpy.types.Object] = []
        all_lights: List[bpy.types.Object] = []

        for obj in scene.objects:
            if obj.type != "LIGHT" or not getattr(obj, "data", None):
                continue
            all_lights.append(obj)
            light_type = obj.data.type
            if light_type == "POINT":
                point_lights.append(obj)
            elif light_type == "SPOT":
                spot_lights.append(obj)
            elif light_type == "AREA":
                area_lights.append(obj)
            elif light_type == "SUN":
                sun_lights.append(obj)

        total_light_count = len(all_lights)
        energies = [float(getattr(obj.data, "energy", 0.0)) for obj in all_lights]
        total_energy = sum(energies)
        average_energy = total_energy / total_light_count if total_light_count > 0 else 0.0

        has_hdri, hdri_strength, world_color = self._detect_hdri()
        ambient_level = self._estimate_ambient_level(total_energy, hdri_strength)

        key_lights, fill_lights, rim_lights = self._classify_light_roles(
            all_lights, camera_data, product_center
        )

        return LightingData(
            point_lights=point_lights,
            spot_lights=spot_lights,
            area_lights=area_lights,
            sun_lights=sun_lights,
            has_hdri=has_hdri,
            hdri_strength=hdri_strength,
            world_color=world_color,
            total_light_count=total_light_count,
            average_energy=average_energy,
            ambient_level=ambient_level,
            key_light_candidates=key_lights,
            fill_light_candidates=fill_lights,
            rim_light_candidates=rim_lights,
        )

    def _detect_hdri(self) -> Tuple[bool, float, Tuple[float, float, float]]:
        """Deteksi HDRI/world sederhana dari World node tree."""
        scene = self.context.scene
        world = scene.world

        has_hdri = False
        hdri_strength = 0.0
        world_color = (0.0, 0.0, 0.0)

        if not world:
            return has_hdri, hdri_strength, world_color

        # Fallback warna world
        try:
            col = getattr(world, "color", None)
            if col is not None:
                world_color = (float(col[0]), float(col[1]), float(col[2]))
        except Exception:
            pass

        node_tree = getattr(world, "node_tree", None)
        if not node_tree:
            return has_hdri, hdri_strength, world_color

        try:
            for node in node_tree.nodes:
                if node.type == "TEX_ENVIRONMENT":
                    has_hdri = True
                if node.type == "BACKGROUND":
                    # Strength
                    try:
                        strength_socket = node.inputs.get("Strength")
                        if strength_socket is not None:
                            hdri_strength = float(strength_socket.default_value)
                    except Exception:
                        pass

                    # Warna (kalau tidak linked)
                    color_socket = node.inputs.get("Color")
                    if color_socket is not None and not color_socket.is_linked:
                        try:
                            col = color_socket.default_value
                            world_color = (float(col[0]), float(col[1]), float(col[2]))
                        except Exception:
                            pass
        except Exception:
            # Kalau gagal parsing node, pakai fallback awal
            pass

        return has_hdri, hdri_strength, world_color

    def _estimate_ambient_level(self, total_energy: float, hdri_strength: float) -> float:
        """Estimasi kasar level ambient berdasarkan total energi + HDRI strength."""
        if total_energy <= 0.0 and hdri_strength <= 0.0:
            return 0.0

        # Heuristik sederhana: skala kecil dari total energi + kontribusi HDRI.
        return total_energy * 0.1 + hdri_strength

    def _classify_light_roles(
        self,
        lights: List[bpy.types.Object],
        camera_data: Optional[CameraData],
        product_center: Optional[Vector],
    ) -> Tuple[List[bpy.types.Object], List[bpy.types.Object], List[bpy.types.Object]]:
        """Heuristik sederhana untuk membagi lampu jadi key / fill / rim.

        - Tanpa camera/product_center: lampu paling terang = key, sisanya = fill.
        - Dengan camera/product_center: gunakan arah relatif terhadap product & kamera.
        """
        if not lights:
            return [], [], []

        # Fallback: tidak ada info kamera/produk
        if camera_data is None or product_center is None:
            sorted_lights = sorted(
                lights, key=lambda l: float(getattr(l.data, "energy", 0.0)), reverse=True
            )
            key = sorted_lights[:1]
            fill = sorted_lights[1:]
            return key, fill, []

        key: List[bpy.types.Object] = []
        fill: List[bpy.types.Object] = []
        rim: List[bpy.types.Object] = []

        cam_pos = camera_data.location
        to_product = (product_center - cam_pos)
        if to_product.length == 0:
            to_product = camera_data.forward.copy()
        else:
            to_product.normalize()

        for light in lights:
            try:
                light_pos = light.matrix_world.translation
            except Exception:
                fill.append(light)
                continue

            to_light_vec = light_pos - product_center
            if to_light_vec.length == 0:
                fill.append(light)
                continue
            to_light_dir = to_light_vec.normalized()

            # Dot terhadap arah kamera→produk: >0 artinya relatif searah (depan), <0 artinya belakang.
            dot_cam = to_light_dir.dot(to_product)

            if dot_cam > 0.3:
                key.append(light)
            elif dot_cam < -0.3:
                rim.append(light)
            else:
                fill.append(light)

        # Kalau tidak ada key yang terdeteksi, fallback ke lampu paling terang
        if not key and lights:
            brightest = max(lights, key=lambda l: float(getattr(l.data, "energy", 0.0)))
            key.append(brightest)
            if brightest in fill:
                fill.remove(brightest)

        return key, fill, rim


__all__ = ["LightingAnalyzer", "LightingData"]
