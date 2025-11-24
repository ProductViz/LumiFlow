# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Template Intelligence Utilities

This module provides loading helpers for research-driven template metadata
and lookup tables defined in data/research_lookup_tables.json.

It is intentionally lightweight in v1.1.0: only loading, validation,
and simple access helpers. Scoring and recommendation logic lives in
TemplateRecommender (see roadmap docs 02_1_TEMPLATE_RECOMMENDER_DAN_PRODUCT_CLASSIFIER).
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict


def _get_default_lookup_structure() -> Dict[str, Any]:
    """Return an empty but structurally valid lookup table dict.

    Used as a safe fallback when file is missing or invalid so that
    callers can still operate without crashing.
    """

    return {
        "templates": [],
        "product_to_template_prior": [],
        "audit_targets": {},
        "material_profiles": [],
        "mood_profiles": [],
    }


_LOOKUP_CACHE: Dict[str, Any] | None = None


def load_research_lookup_tables(path: str = "data/research_lookup_tables.json") -> Dict[str, Any]:
    """Load research-driven template metadata and lookup tables.

    This helper is designed to be robust against missing files or
    partially filled JSON structures. It enforces only the minimal
    guarantees required by v1.1.0 (presence of top-level keys), and
    fills optional sections with sensible defaults when absent.

    Parameters
    ----------
    path: str
        Relative or absolute path to the lookup JSON file.

    Returns
    -------
    Dict[str, Any]
        Dictionary with at least the keys:
        - templates: list
        - product_to_template_prior: list
        - audit_targets: dict
        - material_profiles: list
        - mood_profiles: list
    """

    try:
        # Resolve relative path against addon root (LumiFlow package)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        abs_path = path
        if not os.path.isabs(abs_path):
            abs_path = os.path.join(base_dir, path)

        if not os.path.exists(abs_path):
            return _get_default_lookup_structure()

        with open(abs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure minimal structure and fill defaults for optional sections
        if not isinstance(data, dict):
            return _get_default_lookup_structure()

        templates = data.get("templates")
        product_priors = data.get("product_to_template_prior")
        audit_targets = data.get("audit_targets")
        material_profiles = data.get("material_profiles")
        mood_profiles = data.get("mood_profiles")

        result: Dict[str, Any] = {
            "templates": templates if isinstance(templates, list) else [],
            "product_to_template_prior": (
                product_priors if isinstance(product_priors, list) else []
            ),
            "audit_targets": audit_targets if isinstance(audit_targets, dict) else {},
            "material_profiles": (
                material_profiles if isinstance(material_profiles, list) else []
            ),
            "mood_profiles": mood_profiles if isinstance(mood_profiles, list) else [],
        }

        return result

    except Exception:
        # Any parsing or IO error falls back to an empty-but-valid structure
        return _get_default_lookup_structure()


def get_research_lookup_tables(path: str = "data/research_lookup_tables.json") -> Dict[str, Any]:
    """Cached accessor for research lookup tables.

    This avoids re-reading the JSON file on every call. It is safe to use
    from performance-sensitive paths like template application.
    """

    global _LOOKUP_CACHE
    if _LOOKUP_CACHE is None:
        _LOOKUP_CACHE = load_research_lookup_tables(path)
    return _LOOKUP_CACHE


def get_research_template_entry(template_id: str, path: str = "data/research_lookup_tables.json") -> Dict[str, Any]:
    """Return the research metadata entry for a given template_id, if any.

    If no matching entry is found, an empty dict is returned.
    """

    tables = get_research_lookup_tables(path)
    templates = tables.get("templates", []) or []
    for entry in templates:
        try:
            if entry.get("id") == template_id:
                return entry
        except Exception:
            continue
    return {}


__all__ = [
    "load_research_lookup_tables",
    "get_research_lookup_tables",
    "get_research_template_entry",
]
