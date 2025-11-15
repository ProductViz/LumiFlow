STUDIO_ELECTRONICS_TEMPLATES = {

    "electronics_lowkey_rim": {
        "id": "electronics_lowkey_rim",
        "name": "Electronics Low-Key Rim",
        "category": "Studio & Commercial",
        "description": "Low-key dramatic lighting for electronics with strong rim edges and subtle front key",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Rim Left",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -120,
                        "elevation": 30,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 250,
                    "color": (0.8, 0.9, 1.0),
                    "spot_size": 0.523599,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Rim Right",
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
                    "intensity": 220,
                    "color": (0.8, 0.9, 1.0),
                    "spot_size": 0.523599,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Soft Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 20,
                        "elevation": 20,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 70,
                    "color": (0.9, 0.95, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Glow",
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
                    "size": 1.8,
                    "size_y": 1.2,
                    "intensity": 40,
                    "color": (0.05, 0.08, 0.15),
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
            "default": {"edge_definition": 1.3, "reflection_control": 1.1},
            "electronics": {"screen_glow": True, "logo_highlight": 1.2}
        },
        "camera_preferences": {
            "angle": "tech_hero",
            "height": "slightly_above",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.0,
            "highlights": -0.15,
            "clarity": 0.3,
            "color_balance": "cool"
        }
    },

    "electronics_high_key_white": {
        "id": "electronics_high_key_white",
        "name": "Electronics High-Key White",
        "category": "Studio & Commercial",
        "description": "High-key white background lighting for electronics with clean edges and readable interfaces",
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
                        "elevation": 35,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
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
                        "azimuth": -70,
                        "elevation": 30,
                        "distance": 2.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.3,
                    "size_y": 1.5,
                    "intensity": 200,
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
                        "azimuth": 90,
                        "elevation": 30,
                        "distance": 2.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.3,
                    "size_y": 1.5,
                    "intensity": 180,
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
                        "distance": 2.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.8,
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
                        "y": 3.8,
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
            "base_distance": 2.6,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_reduction": 0.85, "even_illumination": True},
            "electronics": {"screen_reflection_control": 1.1, "logo_readability": 1.2}
        },
        "camera_preferences": {
            "angle": "product_standard",
            "height": "slightly_above",
            "focal_length": 60,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.25,
            "highlights": -0.2,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "electronics_gradient_hero": {
        "id": "electronics_gradient_hero",
        "name": "Electronics Gradient Hero",
        "category": "Studio & Commercial",
        "description": "Hero lighting for electronics with colored gradient background and strong front definition",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Front Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 30,
                        "distance": 2.3
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.4,
                    "intensity": 260,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 25,
                        "distance": 2.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.6,
                    "intensity": 140,
                    "color": (0.95, 0.98, 1.0),
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
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 60,
                    "color": (0.15, 0.2, 0.5),
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
                        "z": -0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.5,
                    "intensity": 35,
                    "color": (0.02, 0.04, 0.1),
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
            "default": {"edge_definition": 1.2},
            "electronics": {"screen_glow": 1.2, "logo_highlight": 1.2}
        },
        "camera_preferences": {
            "angle": "tech_hero",
            "height": "slightly_above",
            "focal_length": 80,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.15,
            "highlights": -0.15,
            "clarity": 0.25,
            "color_balance": "cool"
        }
    },

    "electronics_darkroom_screen_glow": {
        "id": "electronics_darkroom_screen_glow",
        "name": "Electronics Dark Room Screen Glow",
        "category": "Studio & Commercial",
        "description": "Low ambient dark-room lighting emphasizing device screen glow and silhouettes",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Soft Key From Screen",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 10,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.8,
                    "size_y": 1.0,
                    "intensity": 140,
                    "color": (0.8, 0.9, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rim Back",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 160,
                        "elevation": 25,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 170,
                    "color": (0.9, 0.95, 1.0),
                    "spot_size": 0.45,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Ambient Fill Low",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 15,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 1.8,
                    "intensity": 50,
                    "color": (0.1, 0.12, 0.18),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.2,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.2,
                    "size_y": 1.6,
                    "intensity": 45,
                    "color": (0.03, 0.04, 0.08),
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
            "default": {"silhouette_emphasis": 1.2},
            "electronics": {"screen_glow": 1.4, "logo_highlight": 1.2}
        },
        "camera_preferences": {
            "angle": "tech_hero",
            "height": "slightly_above",
            "focal_length": 70,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.0,
            "highlights": -0.2,
            "clarity": 0.3,
            "color_balance": "cool"
        }
    },

    "electronics_desk_topdown_soft": {
        "id": "electronics_desk_topdown_soft",
        "name": "Electronics Desk Top-Down Soft",
        "category": "Studio & Commercial",
        "description": "Soft top-down lighting for desk setups with laptops, keyboards, and accessories",
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
                        "distance": 2.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.4,
                    "size_y": 2.0,
                    "intensity": 260,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Keyboard Edge Rake",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -70,
                        "elevation": 25,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.0,
                    "intensity": 160,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Mouse Edge Rake",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 70,
                        "elevation": 25,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.6,
                    "size_y": 1.0,
                    "intensity": 150,
                    "color": (1.0, 0.99, 0.98),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.6,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"flatlay_evenness": 1.1},
            "electronics": {"keycap_readability": 1.2, "surface_reflection_control": 1.1}
        },
        "camera_preferences": {
            "angle": "desk_topdown",
            "height": "macro_overhead",
            "focal_length": 45,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.05,
            "shadows": 0.25,
            "highlights": -0.15,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "electronics_macro_port_detail": {
        "id": "electronics_macro_port_detail",
        "name": "Electronics Macro Port Detail",
        "category": "Studio & Commercial",
        "description": "Macro lighting for ports, buttons, and texture details on electronics",
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
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.0,
                    "intensity": 210,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Edge Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -35,
                        "elevation": 20,
                        "distance": 1.6
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.1,
                    "intensity": 130,
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
                        "distance": 1.7
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.0,
                    "intensity": 120,
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
            "electronics": {"port_edge_definition": 1.4, "logo_microcontrast": 1.3}
        },
        "camera_preferences": {
            "angle": "macro_side",
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

