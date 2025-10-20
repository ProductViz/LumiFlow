# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Environment & Realistic Templates
Natural lighting templates for outdoor scenes, architectural photography, and realistic environments
"""

# Environment & Realistic Templates Collection
ENVIRONMENT_REALISTIC_TEMPLATES = {
    "overcast_day": {
        "id": "overcast_day",
        "name": "Overcast Day",
        "category": "Environment & Realistic",
        "description": "Soft, even overcast lighting with natural cloud diffusion",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Overcast Sky",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 6.0
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (-1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 8.0,
                    "intensity": 200,
                    "color": (0.92, 0.95, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Cloud Diffusion",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 70,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (-1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 140,
                    "color": (0.88, 0.92, 0.98),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Ambient Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 45,
                        "distance": 4.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "intensity": 100,
                    "color": (0.90, 0.94, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Ground Reflection",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -1.0
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 50,
                    "color": (0.85, 0.88, 0.95),
                    "shape": "ELLIPSE"
                }
            }
        ],
        "settings": {
            "base_distance": 5.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"soft_lighting": True, "even_illumination": 1.1},
            "skin": {"natural_softness": True, "even_tones": 1.2},
            "fabric": {"texture_clarity": True, "color_accuracy": 1.1},
            "metal": {"soft_reflections": True, "subdued_highlights": 0.8}
        },
        "camera_preferences": {
            "angle": "natural_standard",
            "height": "natural_level",
            "focal_length": 50,
            "distance": "natural_medium"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.05,
            "color_balance": "cool"
        }
    }

}
