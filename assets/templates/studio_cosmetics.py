STUDIO_COSMETICS_TEMPLATES = {

    "cosmetics_soft_gradient": {
        "id": "cosmetics_soft_gradient",
        "name": "Cosmetics Soft Gradient",
        "category": "Studio & Commercial",
        "description": "Soft beauty lighting for cosmetics with gentle gradient background and subtle rim",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Beauty Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 40,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.3,
                    "intensity": 200,
                    "color": (1.0, 0.98, 0.97),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 20,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.6,
                    "intensity": 120,
                    "color": (0.97, 0.99, 1.0),
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
                        "y": 4.0,
                        "z": 0.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.4,
                    "intensity": 80,
                    "color": (0.95, 0.8, 0.9),
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
                        "y": 4.0,
                        "z": -0.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.4,
                    "intensity": 40,
                    "color": (0.4, 0.2, 0.35),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Rim",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 35,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.6,
                    "size_y": 0.8,
                    "intensity": 80,
                    "color": (1.0, 0.96, 0.95),
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
            "default": {"skin_flattering": True, "color_accuracy": 1.1},
            "cosmetics": {"label_readability": 1.2, "bottle_glow": True}
        },
        "camera_preferences": {
            "angle": "beauty_product",
            "height": "slightly_above",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.2,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "cosmetics_high_key_white": {
        "id": "cosmetics_high_key_white",
        "name": "Cosmetics High-Key White",
        "category": "Studio & Commercial",
        "description": "High-key white background lighting for cosmetics with clean labels and soft shadows",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Front Soft Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 15,
                        "elevation": 35,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.8,
                    "intensity": 260,
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
                        "azimuth": -60,
                        "elevation": 30,
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.3,
                    "size_y": 1.5,
                    "intensity": 190,
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
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.3,
                    "size_y": 1.5,
                    "intensity": 170,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Top Beauty",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 75,
                        "distance": 2.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.6,
                    "intensity": 180,
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
                        "y": 3.5,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.6,
                    "size_y": 2.0,
                    "intensity": 230,
                    "color": (1.0, 1.0, 1.0),
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
            "default": {"shadow_reduction": 0.85, "even_illumination": True},
            "cosmetics": {"label_readability": 1.25, "bottle_glow": 1.1}
        },
        "camera_preferences": {
            "angle": "product_standard",
            "height": "slightly_above",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.25,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "cosmetics_luxury_black_rim": {
        "id": "cosmetics_luxury_black_rim",
        "name": "Cosmetics Luxury Black Rim",
        "category": "Studio & Commercial",
        "description": "Low-key luxury lighting for cosmetics on black background with strong rim and bottle glow",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Narrow Warm Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 25,
                        "distance": 2.4
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.3,
                    "intensity": 230,
                    "color": (1.0, 0.96, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Cool Rim Back",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -145,
                        "elevation": 30,
                        "distance": 2.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 210,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.4,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Soft Side Accent",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 20,
                        "distance": 2.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 120,
                    "color": (0.95, 0.96, 1.0),
                    "shape": "RECTANGLE"
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
                    "size": 1.6,
                    "size_y": 1.0,
                    "intensity": 45,
                    "color": (0.08, 0.08, 0.1),
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
            "default": {"silhouette_emphasis": 1.2},
            "cosmetics": {"glass_edge_glow": 1.3, "metallic_cap_pop": 1.2}
        },
        "camera_preferences": {
            "angle": "beauty_product",
            "height": "slightly_above",
            "focal_length": 85,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.0,
            "highlights": -0.2,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "cosmetics_clamshell_color_contrast": {
        "id": "cosmetics_clamshell_color_contrast",
        "name": "Cosmetics Clamshell Color Contrast",
        "category": "Studio & Commercial",
        "description": "Clamshell-style beauty lighting for cosmetics with warm key and cool fill for color contrast",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Warm Top Beauty",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 50,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 210,
                    "color": (1.0, 0.92, 0.85),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Cool Bottom Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -40,
                        "distance": 1.9
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 80,
                    "color": (0.85, 0.92, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Accent Left",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -70,
                        "elevation": 20,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.7,
                    "size_y": 0.9,
                    "intensity": 90,
                    "color": (0.98, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Side Accent Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 70,
                        "elevation": 20,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.7,
                    "size_y": 0.9,
                    "intensity": 90,
                    "color": (1.0, 0.96, 0.95),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"beauty_color_contrast": 1.1},
            "cosmetics": {"label_readability": 1.2, "bottle_glow": 1.15}
        },
        "camera_preferences": {
            "angle": "beauty_product",
            "height": "slightly_above",
            "focal_length": 80,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.2,
            "color_balance": "color_contrast"
        }
    },

    "cosmetics_flatlay_soft_overhead": {
        "id": "cosmetics_flatlay_soft_overhead",
        "name": "Cosmetics Flatlay Soft Overhead",
        "category": "Studio & Commercial",
        "description": "Soft overhead lighting for cosmetics flat-lay compositions with gentle directional texture",
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
                    "size_y": 1.8,
                    "intensity": 220,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
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
                        "distance": 2.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.0,
                    "intensity": 130,
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
                        "distance": 2.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.0,
                    "intensity": 130,
                    "color": (1.0, 0.99, 0.98),
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
            "default": {"flatlay_evenness": 1.1},
            "cosmetics": {"texture_visibility": 1.15, "packaging_edges": 1.1}
        },
        "camera_preferences": {
            "angle": "flatlay_top",
            "height": "macro_overhead",
            "focal_length": 50,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.18,
            "color_balance": "neutral"
        }
    },

    "cosmetics_texture_macro_smear": {
        "id": "cosmetics_texture_macro_smear",
        "name": "Cosmetics Texture Macro Smear",
        "category": "Studio & Commercial",
        "description": "Macro lighting for lipstick or foundation smears with raking light to emphasize texture",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Raking Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 20,
                        "elevation": 15,
                        "distance": 1.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.7,
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
                        "azimuth": -35,
                        "elevation": 20,
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
            "default": {"texture_visibility": 1.4},
            "cosmetics": {"smear_relief": 1.4, "pigment_saturation": 1.2}
        },
        "camera_preferences": {
            "angle": "macro_top",
            "height": "macro_overhead",
            "focal_length": 90,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.25,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.35,
            "color_balance": "neutral"
        }
    }
}

