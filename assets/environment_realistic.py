# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

# -*- coding: utf-8 -*-
"""
LumiFlow Environment & Realistic Templates
Natural and environmental lighting setups for realistic scenes
"""

# Environment & Realistic Templates Collection
ENVIRONMENT_REALISTIC_TEMPLATES = {
    "natural_daylight": {
        "id": "natural_daylight",
        "name": "Natural Daylight",
        "category": "Environment & Realistic",
        "description": "Realistic daylight simulation with sky dome and sun for natural outdoor lighting",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Sun Light",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 45,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 500,
                    "color": (1.0, 0.95, 0.9),
                    "angle": 0.5
                }
            },
            {
                "name": "Sky Dome",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 90,
                        "distance": 10.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "intensity": 150,
                    "color": (0.8, 0.9, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Ground Bounce",
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
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 15.0,
                    "intensity": 80,
                    "color": (0.9, 0.9, 0.85),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 8.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "natural_bright"
        },
        "material_adaptations": {
            "landscape": {"natural_colors": True, "realistic_shadows": 1.0},
            "architecture": {"daylight_response": True, "material_accuracy": 1.1},
            "vegetation": {"photosynthetic_glow": True, "natural_subsurface": 1.2}
        },
        "camera_preferences": {
            "angle": "natural_standard",
            "height": "human_perspective",
            "focal_length": 50,
            "distance": "realistic_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "natural_daylight"
        }
    },

    "overcast_soft": {
        "id": "overcast_soft",
        "name": "Overcast Soft",
        "category": "Environment & Realistic",
        "description": "Soft, even lighting simulating overcast sky conditions with minimal shadows",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Overcast Sky",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 12.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "intensity": 300,
                    "color": (0.9, 0.92, 0.95),
                    "shape": "DISK"
                }
            },
            {
                "name": "Ambient Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 60,
                        "distance": 10.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "intensity": 200,
                    "color": (0.88, 0.9, 0.93),
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
                        "z": -1.5
                    }
                },
                "rotation": {
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 18.0,
                    "intensity": 100,
                    "color": (0.85, 0.87, 0.9),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 10.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "soft_neutral"
        },
        "material_adaptations": {
            "default": {"soft_shadows": True, "even_illumination": 1.1},
            "fabric": {"texture_visibility": 1.0, "color_accuracy": 1.1},
            "portrait": {"flattering_skin": True, "soft_features": 1.1}
        },
        "camera_preferences": {
            "angle": "natural_standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "comfortable_medium"
        },
        "post_processing": {
            "contrast": 0.8,
            "shadows": 0.4,
            "highlights": -0.2,
            "clarity": 0.0,
            "color_balance": "neutral_cool"
        }
    },

    "window_light_portrait": {
        "id": "window_light_portrait",
        "name": "Window Light Portrait",
        "category": "Environment & Realistic",
        "description": "Natural window lighting with soft directional light and bounce fill",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Window Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -3.0,
                        "y": 0,
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 3.0,
                    "intensity": 400,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Wall Bounce",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 1.5,
                        "y": 0,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 120,
                    "color": (0.92, 0.94, 0.96),
                    "shape": "RECTANGLE"
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
                        "z": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 60,
                    "color": (0.9, 0.92, 0.94),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "natural_intimate"
        },
        "material_adaptations": {
            "skin": {"natural_tones": True, "soft_shadows": True},
            "fabric": {"texture_clarity": True, "natural_colors": 1.1},
            "wood": {"natural_grain": True, "warm_tones": 1.1}
        },
        "camera_preferences": {
            "angle": "portrait_natural",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "natural_window"
        }
    },

    "forest_dappled": {
        "id": "forest_dappled",
        "name": "Forest Dappled",
        "category": "Environment & Realistic",
        "description": "Dappled forest lighting with sun rays filtering through leaves",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Filtered Sunbeam 1",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
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
                    "spot_size": 0.8,
                    "spot_blend": 0.4
                }
            },
            {
                "name": "Filtered Sunbeam 2",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 45,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0.5, 0, 0)
                },
                "properties": {
                    "intensity": 600,
                    "color": (1.0, 0.93, 0.8),
                    "spot_size": 1.0,
                    "spot_blend": 0.5
                }
            },
            {
                "name": "Green Ambient",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 70,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 15.0,
                    "intensity": 150,
                    "color": (0.7, 0.9, 0.8),
                    "shape": "DISK"
                }
            },
            {
                "name": "Forest Floor",
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
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 12.0,
                    "intensity": 80,
                    "color": (0.8, 0.75, 0.65),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 5.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "natural_forest"
        },
        "material_adaptations": {
            "vegetation": {"subsurface_glow": True, "forest_colors": 1.2},
            "wood": {"natural_patina": True, "forest_weathering": 1.1},
            "fabric": {"nature_adaptation": True, "organic_tones": 1.1}
        },
        "camera_preferences": {
            "angle": "nature_standard",
            "height": "ground_level",
            "focal_length": 35,
            "distance": "environment_wide"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.2,
            "clarity": 0.15,
            "color_balance": "natural_green"
        }
    },

    "beach_sunset": {
        "id": "beach_sunset",
        "name": "Beach Sunset",
        "category": "Environment & Realistic",
        "description": "Warm sunset lighting with ocean reflection and atmospheric glow",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Setting Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 5,
                        "distance": 20.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 600,
                    "color": (1.0, 0.7, 0.5),
                    "angle": 0.8
                }
            },
            {
                "name": "Ocean Reflection",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 8.0,
                        "z": -0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 20.0,
                    "size_y": 10.0,
                    "intensity": 200,
                    "color": (1.0, 0.8, 0.6),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Sky Glow",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 30,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "intensity": 300,
                    "color": (1.0, 0.8, 0.7),
                    "shape": "DISK"
                }
            },
            {
                "name": "Sand Reflection",
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
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 15.0,
                    "intensity": 120,
                    "color": (1.0, 0.9, 0.8),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 8.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "warm_romantic"
        },
        "material_adaptations": {
            "water": {"sunset_reflection": True, "wave_sparkle": 1.3},
            "sand": {"warm_glow": True, "texture_definition": 1.1},
            "skin": {"golden_tan": True, "sunset_warmth": 1.2}
        },
        "camera_preferences": {
            "angle": "sunset_standard",
            "height": "beach_level",
            "focal_length": 35,
            "distance": "romantic_wide"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "warm_sunset"
        }
    },

    "indoor_ambient": {
        "id": "indoor_ambient",
        "name": "Indoor Ambient",
        "category": "Environment & Realistic",
        "description": "Realistic indoor lighting with mixed artificial and natural light sources",
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
                        "z": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 200,
                    "color": (1.0, 0.95, 0.85),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Window Ambient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -2.5,
                        "y": 0,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "size_y": 2.5,
                    "intensity": 300,
                    "color": (0.9, 0.95, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Table Lamp",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 1.5,
                        "y": -1.0,
                        "z": 0.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "intensity": 150,
                    "color": (1.0, 0.9, 0.75),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Wall Bounce",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 2.0,
                        "y": 0,
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 3.5,
                    "intensity": 80,
                    "color": (0.95, 0.95, 0.9),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "cozy_indoor"
        },
        "material_adaptations": {
            "wood": {"warm_tones": True, "furniture_glow": 1.1},
            "fabric": {"indoor_textures": True, "comfort_colors": 1.1},
            "metal": {"indoor_reflections": True, "warm_highlights": 1.0}
        },
        "camera_preferences": {
            "angle": "indoor_standard",
            "height": "sitting_level",
            "focal_length": 50,
            "distance": "comfortable_close"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.4,
            "highlights": -0.1,
            "clarity": 0.05,
            "color_balance": "warm_indoor"
        }
    },

    "mountain_vista": {
        "id": "mountain_vista",
        "name": "Mountain Vista",
        "category": "Environment & Realistic",
        "description": "Alpine lighting with clear atmosphere and mountain peak illumination",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Alpine Sun",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 40,
                        "distance": 25.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 700,
                    "color": (1.0, 0.98, 0.95),
                    "angle": 0.3
                }
            },
            {
                "name": "Sky Dome",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 85,
                        "distance": 20.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 40.0,
                    "intensity": 200,
                    "color": (0.7, 0.85, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Snow Reflection",
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
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 30.0,
                    "intensity": 150,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Atmospheric Scatter",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 20,
                        "distance": 15.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 25.0,
                    "intensity": 100,
                    "color": (0.8, 0.9, 1.0),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 15.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "crisp_alpine"
        },
        "material_adaptations": {
            "snow": {"brilliant_white": True, "sparkle_enhancement": 1.3},
            "rock": {"alpine_textures": True, "weather_effects": 1.1},
            "vegetation": {"high_altitude_adaptation": True, "crisp_colors": 1.2}
        },
        "camera_preferences": {
            "angle": "vista_wide",
            "height": "mountain_level",
            "focal_length": 24,
            "distance": "landscape_far"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.1,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "crisp_mountain"
        }
    },

    "urban_street": {
        "id": "urban_street",
        "name": "Urban Street",
        "category": "Environment & Realistic",
        "description": "Mixed urban lighting with street lights, neon signs, and ambient city glow",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Street Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -2.0,
                        "y": -1.0,
                        "z": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "intensity": 300,
                    "color": (1.0, 0.9, 0.7),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Neon Sign Blue",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 1.5,
                        "y": 2.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.5,
                    "intensity": 150,
                    "color": (0.3, 0.6, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Neon Sign Red",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 2.5,
                        "y": 1.5,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.6,
                    "size_y": 1.2,
                    "intensity": 120,
                    "color": (1.0, 0.2, 0.3),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Building Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 5.0,
                        "z": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 6.0,
                    "intensity": 80,
                    "color": (0.9, 0.85, 0.7),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Pavement Reflection",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -0.5
                    }
                },
                "rotation": {
                    "target": "upward",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 10.0,
                    "intensity": 60,
                    "color": (0.8, 0.8, 0.75),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False,
            "mood": "urban_night"
        },
        "material_adaptations": {
            "concrete": {"urban_wear": True, "wet_reflections": 1.1},
            "metal": {"neon_reflections": True, "urban_patina": 1.2},
            "glass": {"city_reflections": True, "neon_glow": 1.1}
        },
        "camera_preferences": {
            "angle": "street_level",
            "height": "pedestrian_view",
            "focal_length": 35,
            "distance": "urban_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.2,
            "highlights": -0.2,
            "clarity": 0.15,
            "color_balance": "urban_mixed"
        }
    }
}

# Export untuk template system
__all__ = ['ENVIRONMENT_REALISTIC_TEMPLATES']

