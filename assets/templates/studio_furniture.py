STUDIO_FURNITURE_TEMPLATES = {

    "furniture_lifestyle_soft": {
        "id": "furniture_lifestyle_soft",
        "name": "Furniture Lifestyle Soft",
        "category": "Studio & Commercial",
        "description": "Soft lifestyle-style lighting for furniture with window key and gentle background separation",
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
                        "distance": 4.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 260,
                    "color": (0.98, 0.95, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Fill Opposite",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 25,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.5,
                    "intensity": 180,
                    "color": (0.97, 0.98, 1.0),
                    "shape": "RECTANGLE"
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
                    "intensity": 200,
                    "color": (0.95, 0.95, 0.95),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Floor Bounce",
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
                    "method": "euler",
                    "params": {
                        "euler": (1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.0,
                    "intensity": 120,
                    "color": (0.98, 0.97, 0.95),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 5.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"texture_visibility": 1.2, "shadow_softness": 1.1},
            "furniture": {"fabric_detail": 1.2, "wood_grain": 1.1}
        },
        "camera_preferences": {
            "angle": "furniture_lifestyle",
            "height": "slightly_above",
            "focal_length": 35,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.15,
            "color_balance": "warm"
        }
    },

    "furniture_showroom_white": {
        "id": "furniture_showroom_white",
        "name": "Furniture Showroom White",
        "category": "Studio & Commercial",
        "description": "High-key white showroom lighting for furniture with even illumination and clean background",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Front Soft Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 20,
                        "elevation": 30,
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 3.0,
                    "intensity": 360,
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
                        "elevation": 25,
                        "distance": 7.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 3.0,
                    "intensity": 260,
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
                        "elevation": 25,
                        "distance": 7.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 3.0,
                    "intensity": 240,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Roof Softbox",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 9.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 260,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Wall",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 10.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 10.0,
                    "size_y": 4.0,
                    "intensity": 320,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 7.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_reduction": 0.9, "even_illumination": True},
            "furniture": {"fabric_detail": 1.1, "wood_grain": 1.1}
        },
        "camera_preferences": {
            "angle": "furniture_showroom",
            "height": "slightly_above",
            "focal_length": 35,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.3,
            "highlights": -0.2,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "furniture_catalog_three_quarter": {
        "id": "furniture_catalog_three_quarter",
        "name": "Furniture Catalog Three-Quarter",
        "category": "Studio & Commercial",
        "description": "Three-quarter catalog lighting for furniture with controlled contrast and subtle background gradient",
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
                        "distance": 6.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 2.8,
                    "intensity": 320,
                    "color": (1.0, 0.98, 0.95),
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
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 220,
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
                        "y": 9.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 9.0,
                    "size_y": 4.0,
                    "intensity": 240,
                    "color": (0.92, 0.92, 0.94),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 7.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"texture_visibility": 1.2},
            "furniture": {"fabric_detail": 1.2, "wood_grain": 1.15}
        },
        "camera_preferences": {
            "angle": "furniture_hero_45",
            "height": "slightly_above",
            "focal_length": 45,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.05,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.2,
            "color_balance": "neutral_warm"
        }
    },

    "furniture_corner_moody": {
        "id": "furniture_corner_moody",
        "name": "Furniture Corner Moody",
        "category": "Studio & Commercial",
        "description": "Moody corner lighting for furniture with stronger shadows and accent wall illumination",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Corner Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 30,
                        "distance": 6.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 320,
                    "color": (0.98, 0.95, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Low Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 50,
                        "elevation": 20,
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.0,
                    "intensity": 140,
                    "color": (0.92, 0.94, 0.98),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Corner Wall Accent",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -3.5,
                        "y": 7.5,
                        "z": 2.5
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
                    "color": (0.16, 0.18, 0.22),
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
                        "y": 0,
                        "z": -0.6
                    }
                },
                "rotation": {
                    "method": "euler",
                    "params": {
                        "euler": (1.57, 0, 0)
                    }
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 3.0,
                    "intensity": 120,
                    "color": (0.12, 0.12, 0.14),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 7.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_depth": 1.2},
            "furniture": {"fabric_depth": 1.2, "wood_contrast": 1.2}
        },
        "camera_preferences": {
            "angle": "furniture_corner",
            "height": "slightly_above",
            "focal_length": 40,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.2,
            "highlights": -0.15,
            "clarity": 0.25,
            "color_balance": "cool_neutral"
        }
    },

    "furniture_topdown_layout": {
        "id": "furniture_topdown_layout",
        "name": "Furniture Top-Down Layout",
        "category": "Studio & Commercial",
        "description": "Top-down lighting for furniture layout shots such as rugs, coffee tables, and seating plans",
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
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 6.0,
                    "intensity": 360,
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
                        "elevation": 30,
                        "distance": 8.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 3.0,
                    "intensity": 220,
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
                        "elevation": 30,
                        "distance": 8.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 3.0,
                    "intensity": 210,
                    "color": (1.0, 0.99, 0.98),
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
            "default": {"flatlay_evenness": 1.1},
            "furniture": {"rug_texture": 1.3, "wood_surface_readability": 1.2}
        },
        "camera_preferences": {
            "angle": "furniture_topdown",
            "height": "macro_overhead",
            "focal_length": 35,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "furniture_detail_material_macro": {
        "id": "furniture_detail_material_macro",
        "name": "Furniture Detail Material Macro",
        "category": "Studio & Commercial",
        "description": "Macro lighting for furniture material details like stitching, wood grain, and hardware",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Raking Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 15,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 260,
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
                        "distance": 2.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.6,
                    "intensity": 170,
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
                        "distance": 2.8
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
            "base_distance": 2.7,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"texture_visibility": 1.4},
            "furniture": {"stitching_detail": 1.4, "wood_microcontrast": 1.3, "hardware_specular": 1.2}
        },
        "camera_preferences": {
            "angle": "macro_side",
            "height": "macro_overhead",
            "focal_length": 80,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.35,
            "color_balance": "neutral"
        }
    }
}
