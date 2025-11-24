STUDIO_APPAREL_TEMPLATES = {

    "apparel_flat_even": {
        "id": "apparel_flat_even",
        "name": "Apparel Flat Catalog Even",
        "category": "Studio & Commercial",
        "description": "Even catalog lighting for apparel with flat-lay or front view and minimal shadows",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Top Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
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
                    "intensity": 180,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Side Left",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 30,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.6,
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 30,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.6,
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Fill",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
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
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
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
            "default": {"even_illumination": True, "texture_visibility": 1.2},
            "fabric": {"wrinkle_definition": 1.1, "color_accuracy": 1.1}
        },
        "camera_preferences": {
            "angle": "catalog_front",
            "height": "subject_level",
            "focal_length": 50,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "apparel_ecommerce_front_white": {
        "id": "apparel_ecommerce_front_white",
        "name": "Apparel E-commerce Front White",
        "category": "Studio & Commercial",
        "description": "High-key front e-commerce lighting for apparel on mannequin or model against white background",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Front Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 10,
                        "elevation": 35,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 2.4,
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
                        "azimuth": -70,
                        "elevation": 25,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 2.0,
                    "intensity": 180,
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
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 2.0,
                    "intensity": 160,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Top Softener",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.5,
                    "intensity": 140,
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
                        "y": 5.0,
                        "z": 0
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
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"even_illumination": True, "wrinkle_reduction": 0.9},
            "fabric": {"color_accuracy": 1.1, "texture_visibility": 1.0}
        },
        "camera_preferences": {
            "angle": "catalog_front",
            "height": "subject_level",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.2,
            "highlights": -0.15,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "apparel_mannequin_45_key": {
        "id": "apparel_mannequin_45_key",
        "name": "Apparel Mannequin 45° Key",
        "category": "Studio & Commercial",
        "description": "Dimensional 45° key lighting for apparel on mannequin with gentle shadow shaping",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "45 Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 40,
                        "elevation": 30,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 2.0,
                    "intensity": 230,
                    "color": (1.0, 0.99, 0.97),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -50,
                        "elevation": 25,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.8,
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rim Back",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 35,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.6,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Backdrop Gradient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 5.0,
                        "z": 0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 90,
                    "color": (0.92, 0.94, 0.98),
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
            "default": {"shoulder_shape_emphasis": 1.1},
            "fabric": {"texture_visibility": 1.15, "wrinkle_definition": 1.1}
        },
        "camera_preferences": {
            "angle": "three_quarter",
            "height": "subject_level",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.05,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "apparel_fashion_lowkey": {
        "id": "apparel_fashion_lowkey",
        "name": "Apparel Fashion Low-Key",
        "category": "Studio & Commercial",
        "description": "Low-key fashion lighting for apparel with strong shape and rim separation",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Narrow Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 25,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.6,
                    "intensity": 260,
                    "color": (1.0, 0.96, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Kicker",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -120,
                        "elevation": 20,
                        "distance": 3.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 190,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.55,
                    "spot_blend": 0.25
                }
            },
            {
                "name": "Hair / Shoulder Rim",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 35,
                        "distance": 3.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 210,
                    "color": (1.0, 0.95, 0.9),
                    "spot_size": 0.5,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Minimal Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -20,
                        "elevation": 15,
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.8,
                    "intensity": 40,
                    "color": (0.7, 0.8, 0.9),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"silhouette_emphasis": 1.2},
            "fabric": {"texture_visibility": 1.1, "black_level_protection": True}
        },
        "camera_preferences": {
            "angle": "fashion_three_quarter",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.0,
            "highlights": -0.2,
            "clarity": 0.25,
            "color_balance": "cool"
        }
    },

    "apparel_lifestyle_soft_window": {
        "id": "apparel_lifestyle_soft_window",
        "name": "Apparel Lifestyle Soft Window",
        "category": "Studio & Commercial",
        "description": "Soft lifestyle-style lighting for apparel simulating large window key and gentle fill",
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
                        "elevation": 30,
                        "distance": 4.0
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
                    "color": (0.98, 0.95, 0.9),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Interior Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 50,
                        "elevation": 20,
                        "distance": 4.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.5,
                    "intensity": 130,
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
                    "intensity": 160,
                    "color": (0.96, 0.96, 0.98),
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
                    "intensity": 90,
                    "color": (0.98, 0.97, 0.95),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 4.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"lifestyle_softness": 1.2},
            "fabric": {"texture_visibility": 1.1, "warmth": 1.1}
        },
        "camera_preferences": {
            "angle": "lifestyle_three_quarter",
            "height": "slightly_above",
            "focal_length": 50,
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

    "apparel_fabric_detail_macro": {
        "id": "apparel_fabric_detail_macro",
        "name": "Apparel Fabric Detail Macro",
        "category": "Studio & Commercial",
        "description": "Macro lighting for apparel fabric details, seams, and texture with raking light",
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
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.2,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Fill Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 20,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.6,
                    "size_y": 1.4,
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
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
                        "distance": 1.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.2,
                    "intensity": 110,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.6,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"texture_visibility": 1.4},
            "fabric": {"seam_definition": 1.4, "weave_visibility": 1.5}
        },
        "camera_preferences": {
            "angle": "macro_top",
            "height": "macro_overhead",
            "focal_length": 100,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.35,
            "color_balance": "neutral"
        }
    }
}

