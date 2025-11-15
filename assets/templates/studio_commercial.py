# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Studio Commercial Templates
Professional lighting templates for studio photography, commercial work, and product photography.
"""

try:
    from .studio_jewelry import STUDIO_JEWELRY_TEMPLATES
    from .studio_food import STUDIO_FOOD_TEMPLATES
    from .studio_cosmetics import STUDIO_COSMETICS_TEMPLATES
    from .studio_electronics import STUDIO_ELECTRONICS_TEMPLATES
    from .studio_apparel import STUDIO_APPAREL_TEMPLATES
    from .studio_furniture import STUDIO_FURNITURE_TEMPLATES
    from .studio_automotive import STUDIO_AUTOMOTIVE_TEMPLATES
    _PRODUCT_TEMPLATES_IMPORTED = True
except ImportError:
    _PRODUCT_TEMPLATES_IMPORTED = False

# Studio & Commercial Templates Collection
STUDIO_COMMERCIAL_TEMPLATES = {
    "three_point_setup": {
        "id": "three_point_setup",
        "name": "Three-Point Setup",
        "category": "Studio & Commercial",
        "description": "Classic three-point studio lighting with key, fill, and rim for professional results",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
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
                    "size_y": 1.2,
                    "intensity": 200,
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
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "size_y": 1.5,
                    "intensity": 100,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Rim Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 135,
                        "elevation": 55,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 150,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.698132,
                    "spot_blend": 0.15
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
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
        "version": "1.1",
        "lights": [
            {
                "name": "Main Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 40,
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.2,
                    "size_y": 1.4,
                    "intensity": 180,
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
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 160,
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
                        "distance": 2.2
                    }
                },
                "rotation": {
                    "target": "subject", 
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 160,
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
                        "y": 3.5,
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
                    "intensity": 120,
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
        "description": "Professional clamshell lighting for beauty, jewelry, and high-end product shots",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Top Beauty Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 50,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.9,
                    "size_y": 1.2,
                    "intensity": 180,
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
                    "size": 0.9,
                    "size_y": 1.2,
                    "intensity": 60,
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
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.5,
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
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 0.5,
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
                    "size": 1.0,
                    "size_y": 0.7,
                    "intensity": 20,
                    "color": (1.0, 1.0, 1.0),
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


    "product_hero_shot": {
        "id": "product_hero_shot",
        "name": "Product Hero Shot",
        "category": "Studio & Commercial",
        "description": "Dramatic product lighting with gradient background for hero shots and advertising",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Main Product Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 35,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 250,
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
                        "azimuth": 135,
                        "elevation": 60,
                        "distance": 1.8
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
                    "size": 1.6,
                    "size_y": 1.2,
                    "intensity": 30,
                    "color": (0.2, 0.3, 0.8),
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



    "catalog_product": {
        "id": "catalog_product",
        "name": "Catalog Product",
        "category": "Studio & Commercial",
        "description": "Clean, even lighting for product catalog photography with consistent results",
        "author": "LumiFlow",
        "version": "1.1",
        "lights": [
            {
                "name": "Left Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 35,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.0,
                    "size_y": 1.2,
                    "intensity": 200,
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
                        "elevation": 35,
                        "distance": 2.5
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
                    "size": 0.8,
                    "size_y": 0.8,
                    "intensity": 100,
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
                        "y": 3.5,
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
                    "intensity": 80,
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
    }
}

# Rebuild STUDIO_COMMERCIAL_TEMPLATES as generic + product-specific aggregator
_GENERIC_TEMPLATE_KEYS = (
    "three_point_setup",
    "high_key_ecommerce",
    "clamshell_beauty",
    "product_hero_shot",
    "catalog_product",
)

_GENERIC_STUDIO_COMMERCIAL_TEMPLATES = {
    key: STUDIO_COMMERCIAL_TEMPLATES[key]
    for key in _GENERIC_TEMPLATE_KEYS
    if key in STUDIO_COMMERCIAL_TEMPLATES
}

STUDIO_COMMERCIAL_TEMPLATES = {}
STUDIO_COMMERCIAL_TEMPLATES.update(_GENERIC_STUDIO_COMMERCIAL_TEMPLATES)

if _PRODUCT_TEMPLATES_IMPORTED:
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_JEWELRY_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_FOOD_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_COSMETICS_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_ELECTRONICS_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_APPAREL_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_FURNITURE_TEMPLATES)
    STUDIO_COMMERCIAL_TEMPLATES.update(STUDIO_AUTOMOTIVE_TEMPLATES)
