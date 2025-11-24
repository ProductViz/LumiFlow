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
    },

    "golden_hour_environment": {
        "id": "golden_hour_environment",
        "name": "Golden Hour Environment",
        "category": "Environment & Realistic",
        "description": "Warm low-angle golden hour sun with cool sky fill for outdoor scenes and products",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Golden Sun Key",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 15,
                        "distance": 10.0
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (-0.4, 0, 0.6)
                    }
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 5.0,
                    "color": (1.0, 0.78, 0.55),
                    "shape": "DISK"
                }
            },
            {
                "name": "Sky Dome",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 8.0
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (-1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 10.0,
                    "size_y": 8.0,
                    "intensity": 160,
                    "color": (0.82, 0.88, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Warm Bounce",
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
                    "size": 8.0,
                    "size_y": 6.0,
                    "intensity": 70,
                    "color": (0.98, 0.87, 0.68),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 8.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"warm_highlights": True, "soft_shadows": 1.1},
            "metal": {"reflection_control": 1.1},
            "fabric": {"texture_clarity": 1.1},
            "skin": {"warm_tones": 1.2}
        },
        "camera_preferences": {
            "angle": "golden_hour_three_quarter",
            "height": "slightly_above",
            "focal_length": 50,
            "distance": "natural_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.15,
            "color_balance": "warm"
        }
    },

    "interior_window_soft": {
        "id": "interior_window_soft",
        "name": "Interior Window Soft",
        "category": "Environment & Realistic",
        "description": "Soft interior daylight from a large window with gentle fill and background separation",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Window Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 35,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 3.0,
                    "intensity": 220,
                    "color": (0.96, 0.96, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Interior Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 25,
                        "distance": 5.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 150,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Background Accent",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 7.0,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 2.5,
                    "intensity": 160,
                    "color": (0.95, 0.95, 0.98),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 6.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"soft_lighting": True, "texture_visibility": 1.1},
            "furniture": {"wood_grain": 1.1, "fabric_detail": 1.1},
            "skin": {"natural_softness": 1.2}
        },
        "camera_preferences": {
            "angle": "interior_lifestyle",
            "height": "slightly_above",
            "focal_length": 35,
            "distance": "natural_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.25,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    }

}
