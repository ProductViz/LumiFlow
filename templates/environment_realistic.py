# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
LumiFlow Environment & Realistic Templates
Natural lighting templates for outdoor scenes, architectural photography, and realistic environments
"""

# Environment & Realistic Templates Collection
ENVIRONMENT_REALISTIC_TEMPLATES = {
    "golden_hour_sun": {
        "id": "golden_hour_sun",
        "name": "Golden Hour Sun",
        "category": "Environment & Realistic",
        "description": "Warm golden hour sunlight for natural outdoor photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Golden Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 12,
                        "distance": 100
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 4.5,
                    "color": (1.0, 0.82, 0.55),
                    "size": 1.0,
                    "angle": 0.53
                }
            },
            {
                "name": "Sky Ambient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 30
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 50.0,
                    "intensity": 150,
                    "color": (1.0, 0.9, 0.7),
                    "shape": "DISK"  # Natural sky dome shape for golden hour
                }
            },
            {
                "name": "Ground Bounce",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": -10,
                        "distance": 20.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "size_y": 15.0,
                    "intensity": 80,
                    "color": (0.9, 0.8, 0.6),
                    "shape": "ELLIPSE"  # Natural ground reflection pattern
                }
            },
            {
                "name": "Atmospheric Haze",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 25,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 12.0,
                    "intensity": 60,
                    "color": (1.0, 0.85, 0.65),
                    "shape": "DISK"  # Soft circular atmospheric effect
                }
            }
        ],
        "settings": {
            "base_distance": 25.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"golden_warmth": True, "soft_shadows": 1.2},
            "skin": {"golden_glow": True, "natural_warmth": 1.3},
            "fabric": {"warm_textures": True, "golden_tint": 1.1},
            "metal": {"warm_reflections": True, "golden_highlights": 1.2}
        },
        "camera_preferences": {
            "angle": "natural_outdoor",
            "height": "golden_hour_level",
            "focal_length": 85,
            "distance": "natural_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.1,
            "warmth": 0.3,
            "color_balance": "warm"
        }
    },

    "overcast_day": {
        "id": "overcast_day",
        "name": "Overcast Day",
        "category": "Environment & Realistic",
        "description": "Soft, even overcast lighting with natural cloud diffusion",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Overcast Sky",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 40
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 80.0,
                    "intensity": 350,
                    "color": (0.92, 0.95, 1.0),
                    "shape": "DISK"  # Soft overcast dome for natural sky diffusion
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
                        "distance": 30.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 40.0,
                    "size_y": 25.0,
                    "intensity": 200,
                    "color": (0.88, 0.92, 0.98),
                    "shape": "ELLIPSE"  # Natural cloud formation shape
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
                        "distance": 25.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 30.0,
                    "intensity": 120,
                    "color": (0.90, 0.94, 1.0),
                    "shape": "DISK"  # Natural ambient light dispersion
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
                        "z": -2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 40.0,
                    "size_y": 25.0,
                    "intensity": 60,
                    "color": (0.85, 0.88, 0.95),
                    "shape": "ELLIPSE"  # Natural ground reflection pattern
                }
            }
        ],
        "settings": {
            "base_distance": 30.0,
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

    "direct_midday_sun": {
        "id": "direct_midday_sun",
        "name": "Direct Midday Sun",
        "category": "Environment & Realistic",
        "description": "Harsh direct sunlight with strong shadows for midday photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Midday Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 85,
                        "distance": 100
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 8.0,
                    "color": (1.0, 1.0, 0.95),
                    "size": 0.8,
                    "angle": 0.53
                }
            },
            {
                "name": "Sky Blue",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 50
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 60.0,
                    "intensity": 100,
                    "color": (0.6, 0.8, 1.0),
                    "shape": "DISK"  # Natural sky dome for clear day
                }
            },
            {
                "name": "Shadow Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 15,
                        "distance": 30.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "size_y": 12.0,
                    "intensity": 40,
                    "color": (0.7, 0.8, 0.95),
                    "shape": "ELLIPSE"  # Natural shadow fill from environment
                }
            },
            {
                "name": "Ground Glare",
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
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 35.0,
                    "intensity": 120,
                    "color": (0.95, 0.95, 0.9),
                    "shape": "DISK"  # Natural ground glare pattern
                }
            }
        ],
        "settings": {
            "base_distance": 35.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"harsh_shadows": True, "high_contrast": 1.4},
            "skin": {"shadow_definition": True, "harsh_modeling": 1.3},
            "fabric": {"texture_sharpness": True, "shadow_detail": 1.2},
            "metal": {"sharp_reflections": True, "glare_control": 0.9}
        },
        "camera_preferences": {
            "angle": "midday_standard",
            "height": "natural_level",
            "focal_length": 35,
            "distance": "harsh_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": -0.2,
            "highlights": -0.3,
            "clarity": 0.25,
            "color_balance": "neutral"
        }
    },

    "forest_dappled_light": {
        "id": "forest_dappled_light",
        "name": "Forest Dappled Light",
        "category": "Environment & Realistic",
        "description": "Natural forest lighting with dappled sunlight filtering through leaves",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Filtered Sunlight",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 65,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 600,
                    "color": (1.0, 0.92, 0.75),
                    "spot_size": 1.5,
                    "spot_blend": 0.6
                }
            },
            {
                "name": "Canopy Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 12.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "size_y": 15.0,
                    "intensity": 200,
                    "color": (0.75, 0.85, 0.65),
                    "shape": "ELLIPSE"  # Irregular canopy light pattern through leaves
                }
            },
            {
                "name": "Forest Floor Bounce",
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
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "intensity": 60,
                    "color": (0.6, 0.7, 0.5),
                    "shape": "DISK"  # Natural forest floor reflection
                }
            },
            {
                "name": "Side Dapple",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 45,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (0.9, 0.85, 0.7),
                    "spot_size": 1.0,
                    "spot_blend": 0.5
                }
            },
            {
                "name": "Ambient Green",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 30,
                        "distance": 12.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 15.0,
                    "size_y": 9.0,
                    "intensity": 80,
                    "color": (0.65, 0.8, 0.6),
                    "shape": "ELLIPSE"  # Soft forest ambient light
                }
            }
        ],
        "settings": {
            "base_distance": 12.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"dappled_shadows": True, "natural_variation": 1.2},
            "skin": {"forest_tones": True, "natural_modeling": 1.1},
            "fabric": {"organic_textures": True, "green_cast": 0.9},
            "wood": {"natural_harmony": True, "bark_detail": 1.3}
        },
        "camera_preferences": {
            "angle": "forest_natural",
            "height": "ground_level",
            "focal_length": 85,
            "distance": "forest_close"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.1,
            "highlights": -0.2,
            "clarity": 0.15,
            "color_balance": "slightly_green"
        }
    },

    "moonlight_night": {
        "id": "moonlight_night",
        "name": "Moonlight Night",
        "category": "Environment & Realistic",
        "description": "Soft blue moonlight for natural night photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Moonlight",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 45,
                        "distance": 50.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "intensity": 120,
                    "color": (0.6, 0.7, 0.9),
                    "shape": "DISK"  # Natural moon disc shape
                }
            },
            {
                "name": "Night Sky",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 40
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 60.0,
                    "intensity": 25,
                    "color": (0.2, 0.3, 0.5),
                    "shape": "DISK"  # Natural night sky dome
                }
            },
            {
                "name": "Star Reflection",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 70,
                        "distance": 30.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "size_y": 12.0,
                    "intensity": 15,
                    "color": (0.5, 0.6, 0.8),
                    "shape": "ELLIPSE"  # Scattered starlight pattern
                }
            },
            {
                "name": "Ground Dim",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 30.0,
                    "size_y": 18.0,
                    "intensity": 20,
                    "color": (0.4, 0.5, 0.7),
                    "shape": "ELLIPSE"  # Natural ground reflection at night
                }
            }
        ],
        "settings": {
            "base_distance": 35.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"night_mood": True, "blue_cast": 1.2},
            "skin": {"moonlit_pallor": True, "cool_tones": 1.3},
            "fabric": {"night_textures": True, "muted_colors": 0.8},
            "metal": {"moonlight_reflections": True, "subdued_shine": 0.7}
        },
        "camera_preferences": {
            "angle": "night_standard",
            "height": "natural_level",
            "focal_length": 50,
            "distance": "night_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": -0.1,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "cool"
        }
    },

    "interior_daylight": {
        "id": "interior_daylight",
        "name": "Interior Daylight",
        "category": "Environment & Realistic",
        "description": "Natural daylight streaming through windows for interior photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Window",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 30,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "intensity": 400,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "SQUARE"  # Realistic window frame proportion
                }
            },
            {
                "name": "Window Bounce",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 15,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 2.5,
                    "intensity": 120,
                    "color": (0.92, 0.95, 1.0),
                    "shape": "ELLIPSE"  # Wall reflection pattern
                }
            },
            {
                "name": "Ceiling Reflection",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "intensity": 80,
                    "color": (0.90, 0.93, 0.98),
                    "shape": "DISK"  # Natural ceiling light dispersion
                }
            },
            {
                "name": "Wall Bounce",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 10,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 3.0,
                    "intensity": 60,
                    "color": (0.88, 0.91, 0.96),
                    "shape": "ELLIPSE"  # Natural wall reflection pattern
                }
            }
        ],
        "settings": {
            "base_distance": 4.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"natural_interior": True, "window_light": 1.1},
            "fabric": {"interior_textures": True, "natural_colors": 1.2},
            "wood": {"warm_wood_tones": True, "interior_glow": 1.1},
            "glass": {"window_clarity": True, "natural_transparency": 1.0}
        },
        "camera_preferences": {
            "angle": "interior_standard",
            "height": "room_level",
            "focal_length": 35,
            "distance": "interior_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.2,
            "highlights": -0.15,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "interior_night": {
        "id": "interior_night",
        "name": "Interior Night",
        "category": "Environment & Realistic",
        "description": "Warm artificial interior lighting for cozy evening atmospheres",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Ceiling Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 300,
                    "color": (1.0, 0.88, 0.7),
                    "shape": "DISK"  # Typical ceiling fixture shape
                }
            },
            {
                "name": "Table Lamp",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 25,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 0.8,
                    "intensity": 250,
                    "color": (1.0, 0.85, 0.65),
                    "shape": "ELLIPSE"  # Typical lampshade shape
                }
            },
            {
                "name": "Floor Lamp",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 35,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 200,
                    "color": (1.0, 0.90, 0.75),
                    "shape": "DISK"  # Typical floor lamp diffuser
                }
            },
            {
                "name": "Wall Sconce",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 20,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 0.5,
                    "intensity": 150,
                    "color": (1.0, 0.92, 0.8),
                    "shape": "ELLIPSE"  # Wall sconce diffuser shape
                }
            },
            {
                "name": "Ambient Glow",
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
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "intensity": 40,
                    "color": (0.9, 0.8, 0.6),
                    "shape": "DISK"  # Natural ambient floor reflection
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"cozy_warmth": True, "interior_ambience": 1.2},
            "fabric": {"warm_textures": True, "cozy_feel": 1.3},
            "wood": {"rich_wood_tones": True, "warm_glow": 1.2},
            "metal": {"warm_reflections": True, "soft_highlights": 0.9}
        },
        "camera_preferences": {
            "angle": "interior_cozy",
            "height": "living_level",
            "focal_length": 35,
            "distance": "interior_intimate"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.15,
            "highlights": -0.1,
            "warmth": 0.3,
            "color_balance": "warm"
        }
    },

    "architectural_facade": {
        "id": "architectural_facade",
        "name": "Architectural Facade",
        "category": "Environment & Realistic",
        "description": "Professional architectural facade lighting for building photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Key Architectural",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 30,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 12.0,
                    "intensity": 400,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "SQUARE"  # Professional architectural panel shape
                }
            },
            {
                "name": "Fill Facade",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 25,
                        "distance": 18.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 10.0,
                    "size_y": 6.0,
                    "intensity": 200,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "ELLIPSE"  # Architectural fill light pattern
                }
            },
            {
                "name": "Detail Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 15,
                        "distance": 12.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (1.0, 0.96, 0.92),
                    "spot_size": 1.5,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Sky Background",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 20.0,
                        "z": 15.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 30.0,
                    "intensity": 80,
                    "color": (0.7, 0.8, 1.0),
                    "shape": "DISK"  # Natural sky background
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
                        "z": -3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "size_y": 15.0,
                    "intensity": 60,
                    "color": (0.85, 0.88, 0.92),
                    "shape": "ELLIPSE"  # Natural architectural ground reflection
                }
            }
        ],
        "settings": {
            "base_distance": 15.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "concrete": {"architectural_texture": True, "surface_detail": 1.2},
            "glass": {"building_clarity": True, "reflection_control": 1.1},
            "metal": {"architectural_finish": True, "modern_highlights": 1.3},
            "stone": {"natural_texture": True, "weathering_detail": 1.2}
        },
        "camera_preferences": {
            "angle": "architectural_standard",
            "height": "building_level",
            "focal_length": 24,
            "distance": "architectural_wide"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.1,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "sunny_road_automotive": {
        "id": "sunny_road_automotive",
        "name": "Sunny Road Automotive",
        "category": "Environment & Realistic",
        "description": "Natural outdoor automotive lighting on sunny roads",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Sunny Road Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 40,
                        "distance": 100
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 6.0,
                    "color": (1.0, 0.95, 0.88),
                    "size": 1.0,
                    "angle": 0.53
                }
            },
            {
                "name": "Road Reflection",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 30.0,
                    "size_y": 18.0,
                    "intensity": 180,
                    "color": (0.9, 0.92, 0.95),
                    "shape": "ELLIPSE"  # Natural road reflection pattern
                }
            },
            {
                "name": "Sky Fill",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 40
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 50.0,
                    "intensity": 120,
                    "color": (0.75, 0.85, 1.0),
                    "shape": "DISK"  # Natural sky dome fill
                }
            },
            {
                "name": "Environment Bounce",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 15,
                        "distance": 20.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 15.0,
                    "size_y": 9.0,
                    "intensity": 100,
                    "color": (0.85, 0.88, 0.9),
                    "shape": "ELLIPSE"  # Natural environment reflection
                }
            },
            {
                "name": "Horizon Glow",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 5,
                        "distance": 50.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 40.0,
                    "size_y": 25.0,
                    "intensity": 80,
                    "color": (0.95, 0.9, 0.8),
                    "shape": "ELLIPSE"  # Natural horizon glow pattern
                }
            }
        ],
        "settings": {
            "base_distance": 25.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "automotive_paint": {"road_reflections": True, "natural_shine": 1.2},
            "chrome": {"outdoor_brightness": True, "sky_reflections": 1.3},
            "glass": {"road_clarity": True, "environment_reflection": 1.1},
            "tire": {"road_texture": True, "asphalt_interaction": 1.2},
            "metal": {"outdoor_finish": True, "natural_patina": 1.1}
        },
        "camera_preferences": {
            "angle": "automotive_outdoor",
            "height": "road_level",
            "focal_length": 35,
            "distance": "automotive_scenic"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.1,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "slightly_warm"
        }
    }

}

