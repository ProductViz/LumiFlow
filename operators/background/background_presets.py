# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Background Presets
Defines presets for background types and their associated lighting configurations.
"""

from typing import Dict, Any, List, Tuple, Optional


# Background type presets
BACKGROUND_PRESETS: Dict[str, Dict[str, Any]] = {
    "white_seamless": {
        "id": "white_seamless",
        "name": "White Seamless",
        "description": "Classic white cyclorama for clean product shots",
        "type": "seamless",
        "color": (1.0, 1.0, 1.0),
        "default_lighting": "even_fill_high",
        "recommended_isolation": True,
        "icon": "MESH_PLANE",
    },
    
    "black_seamless": {
        "id": "black_seamless",
        "name": "Black Seamless",
        "description": "Black cyclorama for dramatic product shots",
        "type": "seamless",
        "color": (0.02, 0.02, 0.02),
        "default_lighting": "none",
        "recommended_isolation": True,
        "icon": "MESH_PLANE",
    },
    
    "gray_seamless": {
        "id": "gray_seamless",
        "name": "Gray Seamless",
        "description": "Neutral gray cyclorama for versatile lighting",
        "type": "seamless",
        "color": (0.5, 0.5, 0.5),
        "default_lighting": "even_fill_medium",
        "recommended_isolation": True,
        "icon": "MESH_PLANE",
    },
    
    "colored_solid": {
        "id": "colored_solid",
        "name": "Colored Solid",
        "description": "Solid color backdrop - customize color",
        "type": "seamless",
        "color": (0.2, 0.4, 0.8),  # Default blue, user can change
        "default_lighting": "even_fill_medium",
        "recommended_isolation": True,
        "icon": "COLOR",
    },
    
    "flat_white": {
        "id": "flat_white",
        "name": "Flat White Backdrop",
        "description": "Simple vertical white backdrop",
        "type": "backdrop",
        "color": (1.0, 1.0, 1.0),
        "default_lighting": "even_fill_high",
        "recommended_isolation": True,
        "icon": "MESH_PLANE",
    },
    
    "flat_black": {
        "id": "flat_black",
        "name": "Flat Black Backdrop",
        "description": "Simple vertical black backdrop",
        "type": "backdrop",
        "color": (0.02, 0.02, 0.02),
        "default_lighting": "none",
        "recommended_isolation": True,
        "icon": "MESH_PLANE",
    },
    
    "ground_white": {
        "id": "ground_white",
        "name": "White Ground Plane",
        "description": "White ground plane only",
        "type": "ground",
        "color": (1.0, 1.0, 1.0),
        "default_lighting": "ground_fill",
        "recommended_isolation": False,
        "icon": "MESH_GRID",
    },
    
    "ground_reflective": {
        "id": "ground_reflective",
        "name": "Reflective Ground",
        "description": "Reflective ground plane for product reflections",
        "type": "ground",
        "color": (0.1, 0.1, 0.1),
        "reflective": True,
        "default_lighting": "none",
        "recommended_isolation": False,
        "icon": "MESH_GRID",
    },
}


# Background lighting presets
BACKGROUND_LIGHTING_PRESETS: Dict[str, Dict[str, Any]] = {
    "none": {
        "id": "none",
        "name": "No Background Lighting",
        "description": "No dedicated background lights",
        "lights": [],
    },
    
    "even_fill_high": {
        "id": "even_fill_high",
        "name": "Even Fill (High)",
        "description": "Bright, even illumination for white backgrounds",
        "lights": [
            {
                "name": "BG Fill Top",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.5, 2.0)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 3.0,
                    "size_y": 2.0,
                    "energy": 300,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
            {
                "name": "BG Fill Bottom",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.3, -0.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 4.0,
                    "size_y": 2.0,
                    "energy": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "even_fill_medium": {
        "id": "even_fill_medium",
        "name": "Even Fill (Medium)",
        "description": "Medium intensity even illumination",
        "lights": [
            {
                "name": "BG Fill",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.5, 1.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 3.0,
                    "size_y": 2.0,
                    "energy": 150,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "gradient_top_down": {
        "id": "gradient_top_down",
        "name": "Gradient Top-Down",
        "description": "Brighter at top, darker at bottom",
        "lights": [
            {
                "name": "BG Gradient Top",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.3, 2.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 4.0,
                    "size_y": 1.5,
                    "energy": 400,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
            {
                "name": "BG Gradient Mid",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.3, 0.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 3.0,
                    "size_y": 1.0,
                    "energy": 100,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "gradient_bottom_up": {
        "id": "gradient_bottom_up",
        "name": "Gradient Bottom-Up",
        "description": "Brighter at bottom, darker at top",
        "lights": [
            {
                "name": "BG Gradient Bottom",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.3, -0.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 4.0,
                    "size_y": 1.5,
                    "energy": 400,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
            {
                "name": "BG Gradient Top",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.3, 2.0)},
                "rotation": {"target": "background"},
                "properties": {
                    "size": 3.0,
                    "size_y": 1.0,
                    "energy": 80,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "accent_spots": {
        "id": "accent_spots",
        "name": "Accent Spots",
        "description": "Spot lights for dramatic background accents",
        "lights": [
            {
                "name": "BG Accent Left",
                "type": "SPOT",
                "position": {"method": "relative_to_bg", "offset": (-2.0, -1.0, 1.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "energy": 500,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.8,
                    "spot_blend": 0.5,
                },
            },
            {
                "name": "BG Accent Right",
                "type": "SPOT",
                "position": {"method": "relative_to_bg", "offset": (2.0, -1.0, 1.5)},
                "rotation": {"target": "background"},
                "properties": {
                    "energy": 500,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.8,
                    "spot_blend": 0.5,
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "dramatic_side": {
        "id": "dramatic_side",
        "name": "Dramatic Side",
        "description": "Strong side lighting for textured backgrounds",
        "lights": [
            {
                "name": "BG Side Light",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (-3.0, 0, 1.0)},
                "rotation": {"target": "background", "offset": (0, 0.5, 0)},
                "properties": {
                    "size": 1.0,
                    "size_y": 3.0,
                    "energy": 300,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "ground_fill": {
        "id": "ground_fill",
        "name": "Ground Fill",
        "description": "Lighting for ground plane",
        "lights": [
            {
                "name": "Ground Fill",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, -2.0, 3.0)},
                "rotation": {"target": "ground"},
                "properties": {
                    "size": 4.0,
                    "size_y": 4.0,
                    "energy": 150,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE",
                },
            },
        ],
        "light_linking": {
            "mode": "include_background_only",
        },
    },
    
    "rim_accent": {
        "id": "rim_accent",
        "name": "Rim Accent",
        "description": "Subtle rim lighting that also affects product edges",
        "lights": [
            {
                "name": "BG Rim",
                "type": "AREA",
                "position": {"method": "relative_to_bg", "offset": (0, 0.2, 1.0)},
                "rotation": {"target": "camera"},
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "energy": 100,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE",
                },
            },
        ],
        "light_linking": {
            "mode": "natural",  # Affects both background and product
        },
    },
}


# Layer interaction modes
INTERACTION_MODES: Dict[str, Dict[str, Any]] = {
    "natural": {
        "id": "natural",
        "name": "Natural",
        "description": "Lights affect both product and background naturally",
        "product_lights_exclude_bg": False,
        "bg_lights_exclude_product": False,
    },
    
    "isolated": {
        "id": "isolated",
        "name": "Isolated",
        "description": "Full separation using light linking",
        "product_lights_exclude_bg": True,
        "bg_lights_exclude_product": True,
    },
    
    "hybrid": {
        "id": "hybrid",
        "name": "Hybrid",
        "description": "Configurable per-light interaction",
        "product_lights_exclude_bg": True,
        "bg_lights_exclude_product": True,
        "allow_rim_spill": True,
    },
}


def get_background_preset(preset_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a background preset by ID.
    
    Args:
        preset_id: Preset identifier
    
    Returns:
        Preset dictionary or None if not found
    """
    return BACKGROUND_PRESETS.get(preset_id)


def get_lighting_preset(preset_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a lighting preset by ID.
    
    Args:
        preset_id: Preset identifier
    
    Returns:
        Preset dictionary or None if not found
    """
    return BACKGROUND_LIGHTING_PRESETS.get(preset_id)


def get_recommended_lighting(bg_preset_id: str) -> str:
    """
    Get recommended lighting preset for a background type.
    
    Args:
        bg_preset_id: Background preset ID
    
    Returns:
        Recommended lighting preset ID
    """
    preset = get_background_preset(bg_preset_id)
    if preset:
        return preset.get("default_lighting", "none")
    return "none"


def get_all_background_presets() -> List[Tuple[str, str, str]]:
    """
    Get all background presets as enum items.
    
    Returns:
        List of (id, name, description) tuples
    """
    items = []
    for preset_id, preset in BACKGROUND_PRESETS.items():
        items.append((
            preset_id,
            preset["name"],
            preset["description"]
        ))
    return items


def get_all_lighting_presets() -> List[Tuple[str, str, str]]:
    """
    Get all lighting presets as enum items.
    
    Returns:
        List of (id, name, description) tuples
    """
    items = []
    for preset_id, preset in BACKGROUND_LIGHTING_PRESETS.items():
        items.append((
            preset_id,
            preset["name"],
            preset["description"]
        ))
    return items
