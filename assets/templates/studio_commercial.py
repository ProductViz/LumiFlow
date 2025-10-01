# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Studio Commercial Templates
Professional lighting templates for studio photography, commercial work, and product photography.
"""

# Studio & Commercial Templates Collection
STUDIO_COMMERCIAL_TEMPLATES = {
    "three_point_setup": {
        "id": "three_point_setup",
        "name": "Three-Point Setup",
        "category": "Studio & Commercial",
        "description": "Classic three-point studio lighting with key, fill, and rim for professional results",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
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
                    "intensity": 300,
                    "color": (1.0, 1.0, 1.0),
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
                        "distance": 3.5
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
                    "color": (0.95, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rim Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 60,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 250,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.785398,
                    "spot_blend": 0.15
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"surface_detail": 1.0, "reflection_balance": 0.8}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.1,
            "highlights": -0.05,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

        "high_key_ecommerce": {
        "id": "high_key_ecommerce",
        "name": "High-Key E-commerce",
        "category": "Studio & Commercial", 
        "description": "Bright, clean high-key lighting with minimal shadows for e-commerce product shots",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 45,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 5.0,
                    "intensity": 400,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Fill Light Left",
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
                    "size": 3.5,
                    "size_y": 4.5,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Fill Light Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
                        "elevation": 30,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject", 
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 4.5,
                    "intensity": 180,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Light",
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
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 150,
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
            "default": {"brightness_boost": 1.2, "shadow_reduction": 0.8}
        },
        "camera_preferences": {
            "angle": "product_standard",
            "height": "slightly_above", 
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },
    "clamshell_beauty": {
        "id": "clamshell_beauty",
        "name": "Clamshell Beauty",
        "category": "Studio & Commercial",
        "description": "Professional clamshell setup with wraparound soft lighting for beauty and jewelry photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Top Beauty Light",
                "type": "AREA",
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
                    "size": 3.5,
                    "size_y": 2.5,
                    "intensity": 200,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Bottom Fill Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -45,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 2.5,
                    "intensity": 80,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Accent Left",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 15,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 60,
                    "color": (0.98, 1.0, 0.98),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Side Accent Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 15,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "intensity": 60,
                    "color": (1.0, 0.98, 0.98),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Background Softbox",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 3.5,
                        "z": 0.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 3.5,
                    "intensity": 40,
                    "color": (1.0, 1.0, 1.0),
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
            "glass": {"crystal_clarity": True, "soft_reflection": 0.9},
            "metal": {"polished_finish": True, "even_highlights": True},
            "jewelry": {"brilliant_sparkle": True, "facet_definition": 1.2},
            "cosmetics": {"skin_flattering": True, "color_accuracy": 1.1}
        },
        "camera_preferences": {
            "angle": "beauty_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "beauty_close"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.4,
            "highlights": -0.15,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "butterfly_glamor": {
        "id": "butterfly_glamor",
        "name": "Butterfly Glamor",
        "category": "Studio & Commercial",
        "description": "Classic butterfly/paramount lighting for glamorous portrait and beauty shots",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Beauty Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 45,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "intensity": 350,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "DISK"
                }
            },
            {
                "name": "Fill Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -30,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "intensity": 100,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Hair Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 60,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 0.95, 0.85),
                    "spot_size": 0.523599,
                    "spot_blend": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 2.2,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"glamor_boost": True, "skin_softening": 0.8}
        },
        "camera_preferences": {
            "angle": "beauty_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "beauty_close"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    },

    "product_hero_shot": {
        "id": "product_hero_shot",
        "name": "Product Hero Shot",
        "category": "Studio & Commercial",
        "description": "Dramatic product lighting with gradient background for hero shots and advertising",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Product Light",
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
                    "size_y": 4.0,
                    "intensity": 450,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Rim Light Top",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 75,
                        "distance": 2.0
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
                    "spot_blend": 0.15
                }
            },
            {
                "name": "Gradient Background",
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
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 6.0,
                    "intensity": 100,
                    "color": (0.2, 0.3, 0.8),
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
            "default": {"product_highlight": True, "edge_definition": 1.2}
        },
        "camera_preferences": {
            "angle": "product_hero",
            "height": "slightly_above",
            "focal_length": 100,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.1,
            "highlights": -0.05,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "softbox_portrait": {
        "id": "softbox_portrait",
        "name": "Softbox Portrait",
        "category": "Studio & Commercial",
        "description": "Classic softbox lighting setup for natural-looking portrait photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Softbox",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 40,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 2.0,
                    "intensity": 400,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Fill Softbox",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 25,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.5,
                    "intensity": 150,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Hair Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 160,
                        "elevation": 55,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 120,
                    "color": (1.0, 0.95, 0.85),
                    "spot_size": 0.523599,
                    "spot_blend": 0.25
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"natural_skin": True, "soft_transition": 0.9}
        },
        "camera_preferences": {
            "angle": "portrait_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.15,
            "highlights": -0.08,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "ring_light_beauty": {
        "id": "ring_light_beauty",
        "name": "Ring Light Beauty",
        "category": "Studio & Commercial",
        "description": "Modern ring light setup for beauty, fashion, and social media photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Ring Light Main",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0.5,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 350,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "DISK"
                }
            },
            {
                "name": "Soft Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -20,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "intensity": 80,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "DISK"
                }
            },
            {
                "name": "Background Glow",
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
                    "size": 5.0,
                    "intensity": 60,
                    "color": (0.8, 0.85, 1.0),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 1.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"ring_light_effect": True, "catchlight_enhancement": 1.2}
        },
        "camera_preferences": {
            "angle": "beauty_closeup",
            "height": "eye_level",
            "focal_length": 100,
            "distance": "beauty_very_close"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.15,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "catalog_product": {
        "id": "catalog_product",
        "name": "Catalog Product",
        "category": "Studio & Commercial",
        "description": "Clean, even lighting for product catalog photography with consistent results",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Left Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 30,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 250,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Right Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 30,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 250,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Top Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 75,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 2.5,
                    "intensity": 150,
                    "color": (1.0, 1.0, 1.0),
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
                        "y": 4.0,
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
                    "intensity": 100,
                    "color": (1.0, 1.0, 1.0),
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
            "default": {"even_illumination": True, "minimal_shadows": 0.7}
        },
        "camera_preferences": {
            "angle": "product_catalog",
            "height": "slightly_above",
            "focal_length": 50,
            "distance": "product_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.4,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "beauty_dish_glamor": {
        "id": "beauty_dish_glamor",
        "name": "Beauty Dish Glamor",
        "category": "Studio & Commercial",
        "description": "Beauty dish lighting for dramatic yet flattering portrait and fashion photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Beauty Dish Main",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 35,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 500,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "DISK"
                }
            },
            {
                "name": "Grid Spot",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 45,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 100,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.349066,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Hair Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
                        "elevation": 60,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 0.95, 0.85),
                    "spot_size": 0.523599,
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
            "default": {"beauty_dish_character": True, "dramatic_flair": 1.1}
        },
        "camera_preferences": {
            "angle": "portrait_dramatic",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.1,
            "highlights": -0.05,
            "clarity": 0.3,
            "color_balance": "warm"
        }
    },

    "fashion_editorial": {
        "id": "fashion_editorial",
        "name": "Fashion Editorial",
        "category": "Studio & Commercial",
        "description": "High-fashion editorial lighting with dramatic shadows and highlights",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Fashion Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 40,
                        "distance": 2.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 6.0,
                    "intensity": 600,
                    "color": (1.0, 0.98, 0.95),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Dramatic Fill",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -120,
                        "elevation": 20,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 80,
                    "color": (0.8, 0.85, 1.0),
                    "spot_size": 1.0472,
                    "spot_blend": 0.3
                }
            },
            {
                "name": "Edge Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 50,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 200,
                    "color": (1.0, 0.95, 0.85),
                    "spot_size": 0.349066,
                    "spot_blend": 0.1
                }
            }
        ],
        "settings": {
            "base_distance": 2.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"editorial_style": True, "high_contrast": 1.3}
        },
        "camera_preferences": {
            "angle": "fashion_editorial",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "fashion_medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": 0.05,
            "highlights": 0.0,
            "clarity": 0.4,
            "color_balance": "dramatic"
        }
    },

    "loop_portrait": {
        "id": "loop_portrait",
        "name": "Loop Portrait",
        "category": "Studio & Commercial",
        "description": "Classic loop lighting setup for portrait photography with characteristic nose shadow",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
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
                    "size_y": 3.0,
                    "intensity": 350,
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
                        "azimuth": -30,
                        "elevation": 10,
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
                    "intensity": 120,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Hair Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 150,
                        "elevation": 50,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 0.95, 0.85),
                    "spot_size": 0.523599,
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
            "default": {"portrait_character": True, "loop_shadow": 0.8}
        },
        "camera_preferences": {
            "angle": "portrait_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.15,
            "highlights": -0.08,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "jewelry_macro": {
        "id": "jewelry_macro",
        "name": "Jewelry Macro",
        "category": "Studio & Commercial",
        "description": "Specialized macro lighting for jewelry photography with maximum detail and sparkle",
        "author": "LumiFlow",
        "version": "1.0",
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
                    "size": 1.0,
                    "intensity": 200,
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
                        "distance": 1.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
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
                        "distance": 1.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
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
                        "distance": 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 100,
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
    }
}

