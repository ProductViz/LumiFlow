STUDIO_JEWELRY_TEMPLATES = {

    "jewelry_macro": {
        "id": "jewelry_macro",
        "name": "Jewelry Macro",
        "category": "Studio & Commercial",
        "description": "Specialized macro lighting for jewelry photography with maximum detail and sparkle",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Top Macro Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "intensity": 180,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Left Side Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 30,
                        "distance": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 135,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.174533,
                    "spot_blend": 0.05
                }
            },
            {
                "name": "Right Side Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 30,
                        "distance": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 90,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.174533,
                    "spot_blend": 0.05
                }
            },
            {
                "name": "Backlight Sparkle",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 45,
                        "distance": 0.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 80,
                    "color": (1.0, 1.0, 0.9),
                    "spot_size": 0.087266,
                    "spot_blend": 0.02
                }
            }
        ],
        "settings": {
            "base_distance": 1.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"macro_detail": True, "sparkle_enhancement": 1.5},
            "diamond": {"brilliance_boost": True, "fire_enhancement": 1.3},
            "gold": {"warm_luster": True, "texture_definition": 1.2},
            "silver": {"cool_reflection": True, "scratch_reveal": 1.1}
        },
        "camera_preferences": {
            "angle": "macro_top",
            "height": "macro_overhead",
            "focal_length": 100,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.1,
            "highlights": -0.05,
            "clarity": 0.5,
            "color_balance": "neutral"
        }
    },

    "jewelry_black_bg_dramatic": {
        "id": "jewelry_black_bg_dramatic",
        "name": "Jewelry Black Background Dramatic",
        "category": "Studio & Commercial",
        "description": "Dramatic jewelry lighting on black background with strong rims and controlled key",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Soft Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 45,
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.1,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rim Left",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -120,
                        "elevation": 35,
                        "distance": 1.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 220,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Rim Right",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 35,
                        "distance": 1.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Background Halo",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": -0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "size_y": 1.0,
                    "intensity": 40,
                    "color": (0.1, 0.1, 0.1),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"sparkle_enhancement": 1.3, "edge_definition": 1.3},
            "jewelry": {"facet_definition": 1.3, "black_bg_protection": True}
        },
        "camera_preferences": {
            "angle": "jewelry_hero",
            "height": "slightly_above",
            "focal_length": 85,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": 0.0,
            "highlights": -0.15,
            "clarity": 0.4,
            "color_balance": "neutral"
        }
    },

    "jewelry_high_key_white_catalog": {
        "id": "jewelry_high_key_white_catalog",
        "name": "Jewelry High-Key White Catalog",
        "category": "Studio & Commercial",
        "description": "High-key white background lighting for jewelry catalog with clean reflections and readable stones",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Front Soft Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 25,
                        "elevation": 35,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.3,
                    "intensity": 220,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Fill Left",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -70,
                        "elevation": 30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.1,
                    "intensity": 160,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Fill Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 80,
                        "elevation": 30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.1,
                    "intensity": 150,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Top Softbox",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.2,
                    "intensity": 190,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Background White",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 210,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.9,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_reduction": 0.9, "even_illumination": True},
            "jewelry": {"facet_readability": 1.2, "metal_hotspot_control": 1.2}
        },
        "camera_preferences": {
            "angle": "jewelry_catalog",
            "height": "slightly_above",
            "focal_length": 85,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.35,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "jewelry_gradient_luxury": {
        "id": "jewelry_gradient_luxury",
        "name": "Jewelry Gradient Luxury",
        "category": "Studio & Commercial",
        "description": "Luxury jewelry lighting with colored gradient background and controlled sparkle",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Hero Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 30,
                        "distance": 1.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.1,
                    "intensity": 210,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 25,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.0,
                    "intensity": 130,
                    "color": (0.96, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Gradient Top",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": 0.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.2,
                    "intensity": 60,
                    "color": (0.25, 0.16, 0.45),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Gradient Bottom",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": -0.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.2,
                    "intensity": 35,
                    "color": (0.05, 0.04, 0.12),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Sparkle Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 10,
                        "elevation": 45,
                        "distance": 1.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 120,
                    "color": (1.0, 1.0, 0.95),
                    "spot_size": 0.261799,
                    "spot_blend": 0.1
                }
            }
        ],
        "settings": {
            "base_distance": 1.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"sparkle_enhancement": 1.2},
            "jewelry": {"facet_definition": 1.3, "color_gem_pop": 1.2}
        },
        "camera_preferences": {
            "angle": "jewelry_hero",
            "height": "slightly_above",
            "focal_length": 90,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.15,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.3,
            "color_balance": "cool_luxury"
        }
    },

    "jewelry_dark_reflective_base": {
        "id": "jewelry_dark_reflective_base",
        "name": "Jewelry Dark Reflective Base",
        "category": "Studio & Commercial",
        "description": "Jewelry lighting on a dark reflective base with controlled strip highlights and reflections",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Strip Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 35,
                        "distance": 1.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 0.4,
                    "intensity": 220,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 30,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 0.4,
                    "intensity": 170,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Back Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 170,
                        "elevation": 30,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 160,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Reflective Floor Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -0.4
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 90,
                    "color": (0.04, 0.05, 0.06),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"reflection_control": 1.3},
            "jewelry": {"reflection_symmetry": 1.2, "black_base_protection": True}
        },
        "camera_preferences": {
            "angle": "jewelry_reflective_base",
            "height": "slightly_above",
            "focal_length": 80,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.25,
            "shadows": 0.2,
            "highlights": -0.15,
            "clarity": 0.35,
            "color_balance": "cool"
        }
    },

    "jewelry_ring_topdown_tray": {
        "id": "jewelry_ring_topdown_tray",
        "name": "Jewelry Ring Top-Down Tray",
        "category": "Studio & Commercial",
        "description": "Top-down lighting for multiple rings or earrings on a tray with soft overhead and side accents",
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
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.6,
                    "intensity": 220,
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
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 0.8,
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
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 0.8,
                    "intensity": 130,
                    "color": (1.0, 0.99, 0.98),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.1,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"flatlay_evenness": 1.1},
            "jewelry": {"facet_readability": 1.2, "tray_texture_control": 1.1}
        },
        "camera_preferences": {
            "angle": "flatlay_top",
            "height": "macro_overhead",
            "focal_length": 60,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.05,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.25,
            "color_balance": "neutral"
        }
    },

    "jewelry_earring_hanging_display": {
        "id": "jewelry_earring_hanging_display",
        "name": "Jewelry Earring Hanging Display",
        "category": "Studio & Commercial",
        "description": "Lighting for hanging earrings or pendants with strong vertical highlights and soft background",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Narrow Top Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 60,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.7,
                    "size_y": 1.2,
                    "intensity": 210,
                    "color": (1.0, 0.98, 0.96),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Rim Left",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -110,
                        "elevation": 25,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 170,
                    "color": (0.95, 0.98, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Side Rim Right",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 110,
                        "elevation": 25,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 160,
                    "color": (0.95, 0.98, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Background Soft",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.0,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.6,
                    "intensity": 110,
                    "color": (0.95, 0.96, 0.99),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.9,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"sparkle_enhancement": 1.2},
            "jewelry": {"vertical_highlight": 1.3, "chain_detail": 1.2}
        },
        "camera_preferences": {
            "angle": "jewelry_hanging",
            "height": "slightly_above",
            "focal_length": 80,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.15,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    }
}
