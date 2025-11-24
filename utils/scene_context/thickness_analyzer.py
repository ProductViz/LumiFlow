"""
ThicknessAnalyzer - Wrapper untuk legacy get_object_thickness_analysis
agar bisa dipakai lewat SceneAnalyzer / SceneContext.
"""

import bpy
from dataclasses import dataclass
from typing import Dict, List, Optional

from mathutils import Vector

from ..scene_analysis import get_object_thickness_analysis


@dataclass
class ObjectThicknessData:
    """Thickness data untuk satu objek."""
    object_name: str
    average_thickness: float
    min_thickness: float
    max_thickness: float
    method: str


@dataclass
class ThicknessData:
    """Ringkasan thickness untuk sekumpulan objek."""
    objects: Dict[str, ObjectThicknessData]
    average_thickness: float
    min_thickness: float
    max_thickness: float
    objects_analyzed: int


class ThicknessAnalyzer:
    """Adapter tipis di atas legacy get_object_thickness_analysis."""

    def __init__(self, context: bpy.types.Context):
        self.context = context

    def analyze(self,
                target_objects: List[bpy.types.Object],
                sample_points: int = 3) -> ThicknessData:
        """Analisis thickness untuk daftar objek menggunakan fungsi legacy.

        Untuk saat ini, ini hanyalah wrapper sehingga logika lama tetap terpakai
        sambil output-nya dibungkus dalam dataclass yang rapi.
        """
        if not target_objects:
            return self._empty()

        try:
            legacy_result = get_object_thickness_analysis(
                self.context,
                target_objects,
                self.context.scene.camera,
                sample_points=sample_points,
            )
        except Exception:
            # Jika analisis gagal, kembalikan nilai default aman
            return self._empty()

        raw_data = legacy_result.get("thickness_data") or {}
        objects: Dict[str, ObjectThicknessData] = {}

        for name, entry in raw_data.items():
            avg = float(entry.get("average_thickness", 0.0))
            min_t = float(entry.get("min_thickness", 0.0))
            max_t = float(entry.get("max_thickness", 0.0))
            method = str(entry.get("method", ""))

            objects[name] = ObjectThicknessData(
                object_name=name,
                average_thickness=avg,
                min_thickness=min_t,
                max_thickness=max_t,
                method=method,
            )

        objects_analyzed = int(legacy_result.get("objects_analyzed", len(objects)))

        if not objects:
            # Hindari nilai inf dari struktur legacy jika tidak ada data
            return ThicknessData(
                objects={},
                average_thickness=0.0,
                min_thickness=0.0,
                max_thickness=0.0,
                objects_analyzed=0,
            )

        avg_all = float(legacy_result.get("average_thickness", 0.0))
        min_all = float(legacy_result.get("min_thickness", 0.0))
        max_all = float(legacy_result.get("max_thickness", 0.0))

        # Legacy bisa menyimpan min_thickness sebagai inf saat tidak ada data; 
        # amankan dengan fallback sederhana.
        if objects_analyzed <= 0 or not (min_all >= 0.0):
            # Re-hitung min/max dari per-objek jika perlu
            mins = [o.min_thickness for o in objects.values()]
            maxs = [o.max_thickness for o in objects.values()]
            min_all = min(mins) if mins else 0.0
            max_all = max(maxs) if maxs else 0.0

        return ThicknessData(
            objects=objects,
            average_thickness=avg_all,
            min_thickness=min_all,
            max_thickness=max_all,
            objects_analyzed=objects_analyzed,
        )

    def _empty(self) -> ThicknessData:
        """Helper untuk mengembalikan hasil kosong yang aman."""
        return ThicknessData(
            objects={},
            average_thickness=0.0,
            min_thickness=0.0,
            max_thickness=0.0,
            objects_analyzed=0,
        )


__all__ = ["ThicknessAnalyzer", "ThicknessData", "ObjectThicknessData"]
