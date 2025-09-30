# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Dramatic Cinematic Templates
Mood-enhancing lighting templates for dramatic portraits, cinematic scenes, and artistic photography.
"""

# Dramatic & Cinematic Templates Collection
DRAMATIC_CINEMATIC_TEMPLATES = {
    "low_key_dramatic": {
        "id": "low_key_dramatic",
        "name": "Low-Key Dramatic",
        "category": "Dramatic & Cinematic",
        "description": "Dark, moody lighting with selective illumination for mysterious and dramatic effects",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Dramatic Key",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 45,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 400,
                    "color": (1.0, 0.92, 0.80),
                    "spot_size": 0.7,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Shadow Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -120,
                        "elevation": 15,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 4.0,
                    "intensity": 30,
                    "color": (0.70, 0.80, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Rim Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 180,
                    "color": (0.85, 0.90, 1.0),
                    "spot_size": 0.5,
                    "spot_blend": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_depth": 1.5, "contrast_boost": 1.3},
            "metal": {"dramatic_reflections": True, "edge_definition": 1.4},
            "fabric": {"texture_depth": 1.2, "shadow_detail": True}
        },
        "camera_preferences": {
            "angle": "dramatic_low",
            "height": "subject_level",
            "focal_length": 85,
            "distance": "dramatic_close"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": -0.3,
            "highlights": -0.2,
            "clarity": 0.25,
            "color_balance": "warm"
        }
    },

    "hero_shot_premium": {
        "id": "hero_shot_premium",
        "name": "Hero Shot Premium",
        "category": "Dramatic & Cinematic",
        "description": "Premium product hero lighting with dramatic key light and elegant rim lighting",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Hero Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 55,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 500,
                    "color": (1.0, 0.98, 0.94),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Premium Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 25,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (1.0, 0.95, 0.88),
                    "spot_size": 0.6,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Luxury Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 20,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.2,
                    "intensity": 80,
                    "color": (0.92, 0.96, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Background Gradient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, -0.5)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 120,
                    "color": (0.95, 0.97, 1.0),
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
            "luxury": {"premium_finish": True, "highlight_control": 1.2},
            "metal": {"polished_perfection": True, "reflection_quality": 1.3},
            "glass": {"crystal_clarity": True, "premium_sparkle": 1.4},
            "leather": {"rich_texture": True, "depth_enhancement": 1.2}
        },
        "camera_preferences": {
            "angle": "hero_standard",
            "height": "slightly_above",
            "focal_length": 85,
            "distance": "hero_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.1,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "rembrandt_dramatic": {
        "id": "rembrandt_dramatic",
        "name": "Rembrandt Dramatic",
        "category": "Dramatic & Cinematic",
        "description": "Classic Rembrandt lighting with enhanced drama for cinematic portrait effects",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Rembrandt Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 45,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 400,
                    "color": (1.0, 0.94, 0.85),
                    "shape": "SQUARE"
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
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 3.5,
                    "intensity": 60,
                    "color": (0.85, 0.90, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Hair Separation",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 60,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0.3)
                },
                "properties": {
                    "intensity": 200,
                    "color": (1.0, 0.92, 0.82),
                    "spot_size": 0.8,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Background Mood",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.5,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 40,
                    "color": (0.80, 0.85, 0.95),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 2.2,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "skin": {"dramatic_tones": True, "shadow_character": 1.3},
            "fabric": {"texture_drama": True, "fold_definition": 1.2},
            "jewelry": {"selective_sparkle": True, "mood_reflection": 0.8}
        },
        "camera_preferences": {
            "angle": "portrait_dramatic",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.05,
            "highlights": -0.15,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    },

    "split_lighting_contrast": {
        "id": "split_lighting_contrast",
        "name": "Split Lighting Contrast",
        "category": "Dramatic & Cinematic",
        "description": "Sharp split lighting creating dramatic half-light, half-shadow effects",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Side Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 0,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 0.8,
                    "intensity": 600,
                    "color": (1.0, 0.95, 0.88),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Minimal Opposite",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 0,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 3.2,
                    "intensity": 20,
                    "color": (0.75, 0.85, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Top Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 60,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 0.98, 0.95),
                    "spot_size": 0.5,
                    "spot_blend": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"high_contrast": True, "dramatic_split": 1.4}
        },
        "camera_preferences": {
            "angle": "dramatic_side",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": -0.2,
            "highlights": -0.1,
            "clarity": 0.3,
            "color_balance": "dramatic"
        }
    },

    "noir_mystery": {
        "id": "noir_mystery",
        "name": "Noir Mystery",
        "category": "Dramatic & Cinematic",
        "description": "Classic film noir lighting with deep shadows and strategic highlights",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Noir Key",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 75,
                        "elevation": 35,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 350,
                    "color": (1.0, 0.90, 0.75),
                    "spot_size": 0.6,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Venetian Blind",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -2.0,
                        "y": 1.5,
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.3,
                    "size_y": 3.0,
                    "intensity": 100,
                    "color": (1.0, 0.85, 0.70),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Smoke Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 10,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 25,
                    "color": (0.60, 0.70, 0.85),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 2.2,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"noir_atmosphere": True, "shadow_mystery": 1.5}
        },
        "camera_preferences": {
            "angle": "noir_dutch",
            "height": "low_angle",
            "focal_length": 50,
            "distance": "noir_close"
        },
        "post_processing": {
            "contrast": 1.6,
            "shadows": -0.4,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "monochrome"
        }
    },

    "cinematic_wide": {
        "id": "cinematic_wide",
        "name": "Cinematic Wide",
        "category": "Dramatic & Cinematic",
        "description": "Cinematic lighting for wide shots with atmospheric depth and mood",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Moon Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 40,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "intensity": 200,
                    "color": (0.85, 0.90, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Practical Fill",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -1.5,
                        "y": 0.5,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.5,
                    "intensity": 80,
                    "color": (1.0, 0.95, 0.85),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Atmosphere Back",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 20,
                        "distance": 6.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 120,
                    "color": (0.70, 0.80, 0.95),
                    "spot_size": 1.2,
                    "spot_blend": 0.5
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"cinematic_depth": True, "atmospheric_mood": 1.2}
        },
        "camera_preferences": {
            "angle": "cinematic_wide",
            "height": "eye_level",
            "focal_length": 35,
            "distance": "cinematic_far"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.1,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "cool"
        }
    },

    "dramatic_silhouette": {
        "id": "dramatic_silhouette",
        "name": "Dramatic Silhouette",
        "category": "Dramatic & Cinematic",
        "description": "Backlighting creating powerful silhouette effects against bright backgrounds",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Backlight Rim",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 800,
                    "color": (1.0, 0.95, 0.85),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Blast",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 5.0,
                        "z": -1.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 10.0,
                    "size_y": 8.0,
                    "intensity": 400,
                    "color": (1.0, 0.98, 0.90),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Floor Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": -2.0,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 150,
                    "color": (1.0, 0.90, 0.75),
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
            "default": {"silhouette_effect": True, "rim_enhancement": 1.5}
        },
        "camera_preferences": {
            "angle": "silhouette_backlit",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "silhouette_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": -0.5,
            "highlights": 0.2,
            "clarity": 0.1,
            "color_balance": "warm"
        }
    },

    "horror_atmosphere": {
        "id": "horror_atmosphere",
        "name": "Horror Atmosphere",
        "category": "Dramatic & Cinematic",
        "description": "Tense horror lighting with unsettling shadows and strategic highlights",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Unsettling Key",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 20,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 180,
                    "color": (0.85, 0.70, 0.60),
                    "spot_size": 0.8,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Practical Evil",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 1.5,
                        "y": 0.0,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.3,
                    "intensity": 60,
                    "color": (1.0, 0.60, 0.40),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Moonlight Chill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 60,
                        "distance": 6.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 40,
                    "color": (0.60, 0.70, 0.85),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"horror_mood": True, "unsettling_shadows": 1.3}
        },
        "camera_preferences": {
            "angle": "horror_dutch",
            "height": "low_angle",
            "focal_length": 28,
            "distance": "horror_close"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": -0.3,
            "highlights": -0.3,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    }
}

