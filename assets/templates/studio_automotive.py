STUDIO_AUTOMOTIVE_TEMPLATES = {

    "automotive_showroom_soft": {
        "id": "automotive_showroom_soft",
        "name": "Automotive Showroom Soft",
        "category": "Studio & Commercial",
        "description": "Soft showroom-style lighting for automotive product visualization with clean reflections",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Key Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 35,
                        "distance": 6.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 2.0,
                    "intensity": 450,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Roof Fill",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 300,
                    "color": (0.96, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Rim",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -110,
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
                    "size_y": 1.5,
                    "intensity": 260,
                    "color": (0.95, 0.97, 1.0),
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
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 3.0,
                    "intensity": 260,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 6.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"reflection_control": 1.1, "panel_highlight_smoothness": 1.2},
            "automotive": {"paint_reflection": 1.2, "window_clarity": 1.1}
        },
        "camera_preferences": {
            "angle": "automotive_showroom",
            "height": "slightly_above",
            "focal_length": 70,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "automotive_showroom_contrast_strips": {
        "id": "automotive_showroom_contrast_strips",
        "name": "Automotive Showroom Contrast Strips",
        "category": "Studio & Commercial",
        "description": "Higher-contrast showroom lighting with defined strip reflections for glossy car paint",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Primary Strip Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 30,
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 1.2,
                    "intensity": 520,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposing Strip Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -40,
                        "elevation": 28,
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.5,
                    "size_y": 1.2,
                    "intensity": 420,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Roof Soft Fill",
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
                    "size": 7.0,
                    "size_y": 4.0,
                    "intensity": 260,
                    "color": (0.97, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Panel",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 12.0,
                        "z": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 10.0,
                    "size_y": 3.0,
                    "intensity": 300,
                    "color": (0.98, 0.98, 0.99),
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
            "default": {"strip_reflection_contrast": 1.3},
            "automotive": {"panel_highlight_definition": 1.3, "color_accuracy": 1.1}
        },
        "camera_preferences": {
            "angle": "automotive_showroom",
            "height": "slightly_above",
            "focal_length": 80,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.15,
            "highlights": -0.15,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "automotive_studio_black_rim": {
        "id": "automotive_studio_black_rim",
        "name": "Automotive Studio Black Rim",
        "category": "Studio & Commercial",
        "description": "Low-key black-background studio lighting with strong rim and hood highlights",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Side Rim Left",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -130,
                        "elevation": 25,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 420,
                    "color": (1.0, 0.97, 0.9),
                    "spot_size": 0.55,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Side Rim Right",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 130,
                        "elevation": 25,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 380,
                    "color": (0.98, 0.98, 1.0),
                    "spot_size": 0.55,
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Hood Accent Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 10,
                        "elevation": 35,
                        "distance": 7.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 1.0,
                    "intensity": 320,
                    "color": (1.0, 0.97, 0.92),
                    "shape": "RECTANGLE"
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
                        "distance": 9.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 2.0,
                    "intensity": 90,
                    "color": (0.4, 0.45, 0.6),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Floor Glow",
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
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 120,
                    "color": (0.05, 0.06, 0.08),
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
            "default": {"silhouette_emphasis": 1.3},
            "automotive": {"paint_reflection": 1.3, "black_bg_protection": True}
        },
        "camera_preferences": {
            "angle": "automotive_low_hero",
            "height": "low",
            "focal_length": 90,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": 0.0,
            "highlights": -0.2,
            "clarity": 0.35,
            "color_balance": "cool"
        }
    },

    "automotive_overhead_strip_stage": {
        "id": "automotive_overhead_strip_stage",
        "name": "Automotive Overhead Strip Stage",
        "category": "Studio & Commercial",
        "description": "Overhead strip lighting for stage-like presentation with strong roof and hood reflections",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Central Overhead Strip",
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
                    "size": 8.0,
                    "size_y": 2.0,
                    "intensity": 420,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Front Accent Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 5,
                        "elevation": 20,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 1.5,
                    "intensity": 260,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rear Accent Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 20,
                        "distance": 8.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 1.5,
                    "intensity": 220,
                    "color": (0.96, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Stage Background",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 14.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 12.0,
                    "size_y": 4.0,
                    "intensity": 300,
                    "color": (0.1, 0.1, 0.12),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 9.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"roof_reflection_control": 1.2},
            "automotive": {"panel_highlight_smoothness": 1.3, "glass_clarity": 1.1}
        },
        "camera_preferences": {
            "angle": "automotive_top_three_quarter",
            "height": "slightly_above",
            "focal_length": 60,
            "distance": "product_wide"
        },
        "post_processing": {
            "contrast": 1.15,
            "shadows": 0.15,
            "highlights": -0.1,
            "clarity": 0.25,
            "color_balance": "neutral"
        }
    },

    "automotive_detail_wheel_macro": {
        "id": "automotive_detail_wheel_macro",
        "name": "Automotive Detail Wheel Macro",
        "category": "Studio & Commercial",
        "description": "Macro lighting for wheels, rims, and brake calipers with controlled metal highlights",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Rim Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 35,
                        "elevation": 25,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.4,
                    "intensity": 260,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Opposite Edge Strip",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -35,
                        "elevation": 20,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.8,
                    "size_y": 1.2,
                    "intensity": 190,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Brake Caliper Spot",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 15,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 180,
                    "color": (1.0, 0.95, 0.9),
                    "spot_size": 0.35,
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
            "default": {"macro_detail": 1.3},
            "automotive": {"metallic_edge_definition": 1.4, "brake_color_pop": 1.2}
        },
        "camera_preferences": {
            "angle": "macro_wheel",
            "height": "macro_overhead",
            "focal_length": 80,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.25,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.4,
            "color_balance": "neutral"
        }
    },

    "automotive_detail_interior_cockpit": {
        "id": "automotive_detail_interior_cockpit",
        "name": "Automotive Interior Cockpit Detail",
        "category": "Studio & Commercial",
        "description": "Focused interior cockpit lighting for steering wheel, dashboard, and materials",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Dashboard Key",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -20,
                        "elevation": 25,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.4,
                    "size_y": 1.0,
                    "intensity": 220,
                    "color": (1.0, 0.98, 0.96),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Steering Wheel Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 40,
                        "elevation": 20,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 190,
                    "color": (1.0, 0.97, 0.9),
                    "spot_size": 0.35,
                    "spot_blend": 0.25
                }
            },
            {
                "name": "Ambient Interior Glow",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": -1.5,
                        "z": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 1.5,
                    "intensity": 120,
                    "color": (0.85, 0.9, 1.0),
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
            "default": {"interior_detail": 1.3},
            "automotive": {"leather_definition": 1.3, "brushed_metal_emphasis": 1.2}
        },
        "camera_preferences": {
            "angle": "interior_cockpit",
            "height": "slightly_above",
            "focal_length": 35,
            "distance": "macro_close"
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
