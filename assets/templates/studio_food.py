STUDIO_FOOD_TEMPLATES = {

    "food_high_key_clean": {
        "id": "food_high_key_clean",
        "name": "Food High-Key Clean Studio",
        "category": "Studio & Commercial",
        "description": "High-key clean lighting for food photography with soft shadows and bright background",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 40,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.4,
                    "intensity": 220,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Fill Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 30,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "size_y": 1.5,
                    "intensity": 150,
                    "color": (0.97, 0.99, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Background Light",
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
                    "size": 2.5,
                    "size_y": 2.0,
                    "intensity": 160,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"food_texture": True, "color_freshness": 1.2}
        },
        "camera_preferences": {
            "angle": "food_standard",
            "height": "slightly_above",
            "focal_length": 50,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.3,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "warm"
        }
    },

    "food_rustic_side_soft": {
        "id": "food_rustic_side_soft",
        "name": "Food Rustic Side Soft",
        "category": "Studio & Commercial",
        "description": "Rustic side-lit setup for food with soft shadows and warm tones, ideal for wooden tabletops",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Side Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.2,
                    "intensity": 210,
                    "color": (1.0, 0.96, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 25,
                        "distance": 2.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.4,
                    "intensity": 120,
                    "color": (0.97, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Tint",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": 0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.4,
                    "size_y": 1.6,
                    "intensity": 80,
                    "color": (0.55, 0.4, 0.3),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"food_texture": 1.2, "shadows_softness": 1.1}
        },
        "camera_preferences": {
            "angle": "food_45_side",
            "height": "slightly_above",
            "focal_length": 50,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.35,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "warm"
        }
    },

    "food_window_directional": {
        "id": "food_window_directional",
        "name": "Food Window Directional",
        "category": "Studio & Commercial",
        "description": "Natural window-style directional light for food, mimicking side window daylight",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Window Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -70,
                        "elevation": 35,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.8,
                    "intensity": 220,
                    "color": (1.0, 0.98, 0.96),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Bounce Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 40,
                        "elevation": 20,
                        "distance": 2.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.4,
                    "intensity": 120,
                    "color": (0.97, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Soft",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.2,
                        "z": 0.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.4,
                    "size_y": 1.6,
                    "intensity": 90,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.4,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"food_texture": 1.2, "color_freshness": 1.2}
        },
        "camera_preferences": {
            "angle": "food_window",
            "height": "slightly_above",
            "focal_length": 50,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.05,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "neutral_warm"
        }
    },

    "food_flatlay_brunch_overhead": {
        "id": "food_flatlay_brunch_overhead",
        "name": "Food Flatlay Brunch Overhead",
        "category": "Studio & Commercial",
        "description": "Soft overhead flatlay lighting for brunch-style compositions with props and multiple plates",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Overhead Softbox",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 85,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.2,
                    "size_y": 2.0,
                    "intensity": 230,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Left Edge Rake",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -80,
                        "elevation": 25,
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.0,
                    "intensity": 140,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Right Edge Rake",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 80,
                        "elevation": 25,
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.0,
                    "intensity": 130,
                    "color": (1.0, 0.99, 0.98),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.3,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"flatlay_evenness": 1.1, "food_texture": 1.15}
        },
        "camera_preferences": {
            "angle": "flatlay_top",
            "height": "macro_overhead",
            "focal_length": 45,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.18,
            "color_balance": "neutral_warm"
        }
    },

    "food_hero_45_contrast": {
        "id": "food_hero_45_contrast",
        "name": "Food Hero 45 Contrast",
        "category": "Studio & Commercial",
        "description": "Hero 3/4 view lighting for burgers, pizzas, and plated dishes with stronger directional contrast",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Hero Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 35,
                        "distance": 2.1
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.3,
                    "intensity": 240,
                    "color": (1.0, 0.98, 0.94),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Controlled Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 25,
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.2,
                    "intensity": 130,
                    "color": (0.97, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Gradient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.4,
                        "z": 0.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.2,
                    "size_y": 1.6,
                    "intensity": 90,
                    "color": (0.2, 0.16, 0.13),
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
            "default": {"food_texture": 1.25, "highlight_crispness": 1.1}
        },
        "camera_preferences": {
            "angle": "food_hero_45",
            "height": "slightly_above",
            "focal_length": 60,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.35,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    },

    "food_macro_texture_detail": {
        "id": "food_macro_texture_detail",
        "name": "Food Macro Texture Detail",
        "category": "Studio & Commercial",
        "description": "Macro lighting for food texture details like crumbs, grill marks, and surface gloss",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Raking Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 25,
                        "elevation": 15,
                        "distance": 1.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.0,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 20,
                        "distance": 1.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.1,
                    "intensity": 120,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Overhead",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 1.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.0,
                    "intensity": 110,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.4,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"food_texture": 1.4, "microcontrast": 1.3}
        },
        "camera_preferences": {
            "angle": "macro_top",
            "height": "macro_overhead",
            "focal_length": 80,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.35,
            "color_balance": "neutral_warm"
        }
    }
}

