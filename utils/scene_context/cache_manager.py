"""Simple caching utilities for SceneAnalyzer results."""

from dataclasses import dataclass
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene_analyzer import SceneContext


@dataclass(frozen=True)
class CacheKey:
    frame: int
    selection_hash: str
    level: str
    overrides: str = ""


class AnalysisCache:
    """In-memory cache for SceneContext keyed by frame, selection, and level."""

    def __init__(self, max_size: int = 10) -> None:
        self._max_size = max_size
        self._cache: Dict[CacheKey, "SceneContext"] = {}

    def get(self, key: CacheKey) -> Optional["SceneContext"]:
        return self._cache.get(key)

    def put(self, key: CacheKey, context: "SceneContext") -> None:
        if len(self._cache) >= self._max_size and self._cache:
            # Evict oldest entry by frame as a simple heuristic
            oldest_key = min(self._cache.keys(), key=lambda k: k.frame)
            self._cache.pop(oldest_key, None)
        self._cache[key] = context

    def invalidate(self) -> None:
        self._cache.clear()


__all__ = ["CacheKey", "AnalysisCache"]
