# -*- coding: utf-8 -*-
"""
LumiFlow Dramatic & Cinematic Templates
Lighting setups for dramatic and cinematic photography
"""

# Dramatic & Cinematic Templates Collection
DRAMATIC_CINEMATIC_TEMPLATES = {
    "film_noir_classic": {
        "id": "film_noir_classic",
        "name": "Film Noir Classic",
        "category": "Dramatic & Cinematic",
        "description": "Classic film noir lighting with strong contrasts and dramatic shadows",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Key Hard Light",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 60,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 800,
                    "color": (1.0, 0.95, 0.85),
                    "angle": 0.1
                }
            },
            {
                "name": "Venetian Blind Effect",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 30,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 400,
                    "color": (0.9, 0.9, 0.95),
                    "spot_size": 1.2,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Rim Separation",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 45,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (1.0, 0.92, 0.8),
                    "spot_size": 0.8,
                    "spot_blend": 0.3
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "dark_dramatic"
        },
        "material_adaptations": {
            "skin": {"contrast_enhancement": 1.4, "shadow_depth": 1.3},
            "fabric": {"texture_drama": 1.2, "shadow_definition": 1.4}
        },
        "camera_preferences": {
            "angle": "dramatic_low",
            "height": "slightly_below",
            "focal_length": 85,
            "distance": "medium_dramatic"
        },
        "post_processing": {
            "contrast": 1.8,
            "shadows": -0.3,
            "highlights": -0.4,
            "clarity": 0.3,
            "color_balance": "cool_shadows"
        }
    },

    "golden_hour_cinematic": {
        "id": "golden_hour_cinematic",
        "name": "Golden Hour Cinematic",
        "category": "Dramatic & Cinematic",
        "description": "Warm cinematic lighting mimicking golden hour with soft directional light",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Golden Key",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 15,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 600,
                    "color": (1.0, 0.8, 0.6),
                    "angle": 0.2
                }
            },
            {
                "name": "Atmosphere Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 25,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "intensity": 150,
                    "color": (1.0, 0.85, 0.7),
                    "shape": "DISK"
                }
            },
            {
                "name": "Backlight Glow",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 20,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 200,
                    "color": (1.0, 0.75, 0.5),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "warm_cinematic"
        },
        "material_adaptations": {
            "skin": {"golden_glow": True, "warm_tones": 1.3},
            "landscape": {"atmospheric_perspective": True, "golden_enhancement": 1.2}
        },
        "camera_preferences": {
            "angle": "cinematic_wide",
            "height": "eye_level",
            "focal_length": 35,
            "distance": "cinematic_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.2,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "warm_golden"
        }
    },

    "thriller_suspense": {
        "id": "thriller_suspense",
        "name": "Thriller Suspense",
        "category": "Dramatic & Cinematic",
        "description": "Mysterious lighting with sharp contrasts and strategic shadows for suspense",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Interrogation Key",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 70,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 1000,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.6,
                    "spot_blend": 0.05
                }
            },
            {
                "name": "Shadow Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 20,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (0.8, 0.85, 1.0),
                    "spot_size": 1.0,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Background Mystery",
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
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 50,
                    "color": (0.7, 0.8, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "suspenseful_dark"
        },
        "material_adaptations": {
            "skin": {"dramatic_contrast": 1.5, "mystery_shadows": True},
            "fabric": {"texture_emphasis": 1.3, "shadow_play": 1.4}
        },
        "camera_preferences": {
            "angle": "thriller_low",
            "height": "slightly_below",
            "focal_length": 50,
            "distance": "close_dramatic"
        },
        "post_processing": {
            "contrast": 2.0,
            "shadows": -0.5,
            "highlights": -0.3,
            "clarity": 0.4,
            "color_balance": "cool_blue"
        }
    },

    "romantic_drama": {
        "id": "romantic_drama",
        "name": "Romantic Drama",
        "category": "Dramatic & Cinematic",
        "description": "Soft, dreamy lighting with warm tones for romantic dramatic scenes",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Romantic Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 35,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "intensity": 250,
                    "color": (1.0, 0.9, 0.8),
                    "shape": "DISK"
                }
            },
            {
                "name": "Dreamy Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 25,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 120,
                    "color": (1.0, 0.85, 0.75),
                    "shape": "DISK"
                }
            },
            {
                "name": "Hair Glow",
                "type": "AREA",
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
                    "offset": (0, 0, 0.5)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 180,
                    "color": (1.0, 0.8, 0.6),
                    "shape": "DISK"
                }
            },
            {
                "name": "Ambient Romance",
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
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 60,
                    "color": (1.0, 0.88, 0.78),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.8,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "romantic_soft"
        },
        "material_adaptations": {
            "skin": {"soft_glow": True, "romantic_tones": 1.2},
            "fabric": {"soft_textures": True, "warm_enhancement": 1.1}
        },
        "camera_preferences": {
            "angle": "romantic_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "intimate_close"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": 0.1,
            "clarity": -0.1,
            "color_balance": "warm_romantic"
        }
    },

    "action_hero": {
        "id": "action_hero",
        "name": "Action Hero",
        "category": "Dramatic & Cinematic",
        "description": "Dynamic lighting with strong directional light and dramatic rim lighting for action scenes",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Hero Key",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 45,
                        "distance": 6.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 900,
                    "color": (1.0, 0.95, 0.9),
                    "angle": 0.15
                }
            },
            {
                "name": "Dynamic Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 60,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 600,
                    "color": (1.0, 0.9, 0.8),
                    "spot_size": 1.0,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Power Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 30,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 200,
                    "color": (0.9, 0.95, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Environment Accent",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 5.0,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 5.0,
                    "intensity": 100,
                    "color": (0.85, 0.9, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "dynamic_powerful"
        },
        "material_adaptations": {
            "skin": {"heroic_definition": True, "muscular_emphasis": 1.2},
            "metal": {"dynamic_reflections": True, "power_highlights": 1.3},
            "fabric": {"action_textures": True, "movement_definition": 1.2}
        },
        "camera_preferences": {
            "angle": "heroic_low",
            "height": "slightly_below",
            "focal_length": 35,
            "distance": "action_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.1,
            "highlights": -0.1,
            "clarity": 0.25,
            "color_balance": "neutral_powerful"
        }
    },

    "horror_gothic": {
        "id": "horror_gothic",
        "name": "Horror Gothic",
        "category": "Dramatic & Cinematic",
        "description": "Dark, eerie lighting with minimal fill for horror and gothic atmospheres",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Eerie Underlight",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -60,
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 400,
                    "color": (0.7, 0.8, 1.0),
                    "spot_size": 1.2,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Side Shadow",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 15,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (0.6, 0.7, 1.0),
                    "spot_size": 0.8,
                    "spot_blend": 0.5
                }
            },
            {
                "name": "Atmospheric Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 6.0,
                    "intensity": 30,
                    "color": (0.5, 0.6, 0.9),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "dark_gothic"
        },
        "material_adaptations": {
            "skin": {"pallor_enhancement": True, "shadow_emphasis": 1.5},
            "fabric": {"gothic_textures": True, "darkness_adaptation": 1.3}
        },
        "camera_preferences": {
            "angle": "gothic_dramatic",
            "height": "below_subject",
            "focal_length": 50,
            "distance": "close_menacing"
        },
        "post_processing": {
            "contrast": 2.2,
            "shadows": -0.7,
            "highlights": -0.5,
            "clarity": 0.3,
            "color_balance": "cold_gothic"
        }
    },

    "sci_fi_futuristic": {
        "id": "sci_fi_futuristic",
        "name": "Sci-Fi Futuristic",
        "category": "Dramatic & Cinematic",
        "description": "Cool-toned futuristic lighting with neon accents and technological atmosphere",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Tech Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 45,
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
                    "intensity": 350,
                    "color": (0.8, 0.9, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Neon Accent Blue",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 20,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (0.3, 0.6, 1.0),
                    "spot_size": 0.9,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Neon Accent Cyan",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 30,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 180,
                    "color": (0.2, 0.8, 1.0),
                    "spot_size": 1.1,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Environment Tech",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.5,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 80,
                    "color": (0.6, 0.8, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "futuristic_tech"
        },
        "material_adaptations": {
            "skin": {"tech_enhancement": True, "futuristic_tones": 1.2},
            "metal": {"tech_reflections": True, "neon_highlights": 1.3},
            "plastic": {"tech_surfaces": True, "neon_glow": 1.2}
        },
        "camera_preferences": {
            "angle": "futuristic_standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "sci_fi_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.1,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "cool_futuristic"
        }
    },

    "western_dramatic": {
        "id": "western_dramatic",
        "name": "Western Dramatic",
        "category": "Dramatic & Cinematic",
        "description": "Harsh directional lighting with warm tones for western and desert dramatic scenes",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Desert Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 30,
                        "distance": 10.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 1200,
                    "color": (1.0, 0.85, 0.7),
                    "angle": 0.1
                }
            },
            {
                "name": "Dust Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 20,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "intensity": 100,
                    "color": (1.0, 0.9, 0.8),
                    "shape": "DISK"
                }
            },
            {
                "name": "Silhouette Rim",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 10,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 800,
                    "color": (1.0, 0.8, 0.6),
                    "angle": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 5.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "western_harsh"
        },
        "material_adaptations": {
            "skin": {"weathered_tones": True, "harsh_shadows": 1.3},
            "leather": {"worn_textures": True, "dust_accumulation": 1.2},
            "metal": {"sun_bleached": True, "heat_reflections": 1.1}
        },
        "camera_preferences": {
            "angle": "western_low",
            "height": "ground_level",
            "focal_length": 35,
            "distance": "western_wide"
        },
        "post_processing": {
            "contrast": 1.6,
            "shadows": -0.2,
            "highlights": -0.3,
            "clarity": 0.3,
            "color_balance": "warm_desert"
        }
    },

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
                "name": "Edge Definition",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 15,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (0.90, 0.95, 1.0),
                    "spot_size": 0.4,
                    "spot_blend": 0.1
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"contrast_enhancement": 1.5, "edge_sharpness": True},
            "skin": {"dramatic_modeling": True, "shadow_definition": 1.3},
            "fabric": {"texture_contrast": True, "fold_drama": 1.4}
        },
        "camera_preferences": {
            "angle": "split_dramatic",
            "height": "subject_level",
            "focal_length": 85,
            "distance": "dramatic_medium"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": -0.2,
            "highlights": -0.1,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "film_noir_shadows": {
        "id": "film_noir_shadows",
        "name": "Film Noir Shadows",
        "category": "Dramatic & Cinematic",
        "description": "Classic film noir lighting with harsh shadows and venetian blind patterns",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Noir Key Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 35,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 800,
                    "color": (0.98, 0.95, 0.88),
                    "spot_size": 0.6,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Shadow Pattern",
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
                    "color": (0.92, 0.90, 0.85),
                    "spot_size": 1.2,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Cool Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 20,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 250,
                    "color": (0.85, 0.88, 0.95),
                    "spot_size": 0.4,
                    "spot_blend": 0.25
                }
            },
            {
                "name": "Atmosphere",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
                        "z": -1.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "intensity": 30,
                    "color": (0.70, 0.75, 0.85),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 2.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_drama": 1.6, "pattern_definition": True},
            "fabric": {"noir_texture": True, "shadow_play": 1.3},
            "metal": {"harsh_reflections": True, "contrast_edges": 1.4}
        },
        "camera_preferences": {
            "angle": "noir_dramatic",
            "height": "slightly_below",
            "focal_length": 50,
            "distance": "noir_medium"
        },
        "post_processing": {
            "contrast": 1.6,
            "shadows": -0.4,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "cool"
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
    }
}

# Export untuk template system
__all__ = ['DRAMATIC_CINEMATIC_TEMPLATES']
