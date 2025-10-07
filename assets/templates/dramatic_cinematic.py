# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Dramatic Cinematic Templates
Mood-enhancing lighting templates for dramatic portraits, cinematic scenes, and artistic photography.
"""

# Dramatic & Cinematic Templates Collection
DRAMATIC_CINEMATIC_TEMPLATES = {
    "dramatic_portrait": {
        "id": "dramatic_portrait",
        "name": "Dramatic Portrait",
        "category": "Dramatic & Cinematic",
        "description": "Cinematic portrait lighting with strong key light, deep shadows, and atmospheric mood",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Dramatic Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 30,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.2,
                    "intensity": 140,
                    "color": (1.0, 0.95, 0.85),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Atmospheric Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 45,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 90,
                    "color": (1.0, 0.90, 0.75),
                    "spot_size": 0.8,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Subtle Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 15,
                        "distance": 4.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 0.8,
                    "intensity": 30,
                    "color": (0.85, 0.90, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Background Separation",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.5,
                        "z": 0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 45,
                    "color": (0.3, 0.4, 0.6),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "skin": {"dramatic_modeling": True, "shadow_depth": 1.3},
            "fabric": {"texture_emphasis": True, "dramatic_folds": 1.2},
            "hair": {"volume_definition": True, "rim_highlight": 1.4}
        },
        "camera_preferences": {
            "angle": "dramatic_portrait",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.0,
            "highlights": -0.2,
            "clarity": 0.3,
            "color_balance": "warm"
        }
    }
}

