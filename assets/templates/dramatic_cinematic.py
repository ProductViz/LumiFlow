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
        "version": "1.1",
        "lights": [
            {
                "name": "Dramatic Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 30,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.4,
                    "intensity": 240,
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
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 160,
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
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.0,
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
            "base_distance": 2.2,
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
    },

    "cinematic_color_contrast": {
        "id": "cinematic_color_contrast",
        "name": "Cinematic Color Contrast",
        "category": "Dramatic & Cinematic",
        "description": "Cinematic blue-orange color contrast lighting for portraits and fashion",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Warm Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 25,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.5,
                    "intensity": 230,
                    "color": (1.0, 0.88, 0.72),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Cool Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -80,
                        "elevation": 20,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.2,
                    "intensity": 80,
                    "color": (0.68, 0.8, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Back Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 140,
                        "elevation": 35,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.7,
                    "spot_blend": 0.25
                }
            },
            {
                "name": "Background Wash",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
                        "z": 0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.0,
                    "intensity": 70,
                    "color": (0.18, 0.25, 0.4),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "skin": {"color_contrast_enhancement": 1.1, "shadow_depth": 1.2},
            "fabric": {"texture_emphasis": 1.2, "saturation_boost": 1.1},
            "hair": {"rim_highlight": 1.3}
        },
        "camera_preferences": {
            "angle": "cinematic_three_quarter",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.05,
            "highlights": -0.15,
            "clarity": 0.25,
            "color_balance": "blue_orange"
        }
    },

    "lowkey_silhouette": {
        "id": "lowkey_silhouette",
        "name": "Low-Key Silhouette",
        "category": "Dramatic & Cinematic",
        "description": "Backlit low-key silhouette lighting with strong edge rim",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Back Sun",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 10,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 260,
                    "color": (1.0, 0.9, 0.8),
                    "spot_size": 0.5,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Rim Left",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -135,
                        "elevation": 20,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (0.95, 0.95, 1.0),
                    "spot_size": 0.6,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Rim Right",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 20,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 180,
                    "color": (0.9, 0.9, 1.0),
                    "spot_size": 0.6,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Minimal Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 15,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "size_y": 1.2,
                    "intensity": 25,
                    "color": (0.6, 0.7, 0.9),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "skin": {"silhouette_emphasis": 1.3, "shadow_depth": 1.4},
            "fabric": {"edge_definition": 1.3},
            "hair": {"back_rim_priority": 1.4}
        },
        "camera_preferences": {
            "angle": "silhouette_profile",
            "height": "eye_level",
            "focal_length": 70,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.6,
            "shadows": 0.0,
            "highlights": -0.3,
            "clarity": 0.35,
            "color_balance": "cool"
        }
    }
}

