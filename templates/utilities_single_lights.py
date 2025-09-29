"""
Utilities Single Lights Templates
Single light templates for testing, utilities, and specialized lighting scenarios.
"""

# Utilities & Single Lights Templates Collection
UTILITIES_SINGLE_LIGHTS_TEMPLATES = {
    "key_light_only": {
        "id": "key_light_only",
        "name": "Key Light Only",
        "category": "Utilities & Single Lights",
        "description": "Single key light for primary illumination and testing",
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
                    "intensity": 300,
                    "color": (1.0, 0.95, 0.9),
                    "shape": "SQUARE"  # Professional key light softbox proportion
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"primary_illumination": True, "shadow_definition": 1.2}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "subject_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.0,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "warm"
        }
    },

    "fill_light_only": {
        "id": "fill_light_only",
        "name": "Fill Light Only",
        "category": "Utilities & Single Lights",
        "description": "Single fill light for shadow softening and secondary illumination",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
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
                    "size": 3.5,
                    "size_y": 2.5,
                    "intensity": 120,
                    "color": (0.9, 0.95, 1.0),
                    "shape": "ELLIPSE"  # Large soft fill light diffusion pattern
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"shadow_softening": True, "gentle_fill": 1.1}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "subject_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": -0.05,
            "clarity": 0.05,
            "color_balance": "cool"
        }
    },

    "rim_light_only": {
        "id": "rim_light_only",
        "name": "Rim Light Only",
        "category": "Utilities & Single Lights",
        "description": "Single rim light for edge definition and subject separation",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
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
                    "color": (1.0, 0.98, 0.95),
                    "spot_size": 0.785398,
                    "spot_blend": 0.15
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"edge_definition": True, "subject_separation": 1.3}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "subject_level",
            "focal_length": 85,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": -0.1,
            "highlights": 0.1,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "backlight_only": {
        "id": "backlight_only",
        "name": "Backlight Only",
        "category": "Utilities & Single Lights",
        "description": "Single backlight for silhouette effects and dramatic lighting",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Backlight",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
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
                    "intensity": 400,
                    "color": (1.0, 0.98, 0.94),
                    "shape": "SQUARE"  # Professional backlight panel
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"silhouette_effect": True, "dramatic_backlight": 1.4}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "subject_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": -0.3,
            "highlights": 0.2,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "top_down_light": {
        "id": "top_down_light",
        "name": "Top-Down Light",
        "category": "Utilities & Single Lights",
        "description": "Single overhead light for flat lay and product photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Top Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 90,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 350,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "DISK"  # Natural overhead light dispersion for flat lay
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"even_illumination": True, "minimal_shadows": 1.1}
        },
        "camera_preferences": {
            "angle": "top_down",
            "height": "overhead",
            "focal_length": 50,
            "distance": "top_down_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.4,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "single_sun": {
        "id": "single_sun",
        "name": "Single Sun",
        "category": "Utilities & Single Lights",
        "description": "Single sun light for natural outdoor lighting simulation",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Sun Light",
                "type": "SUN",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
                        "elevation": 45,
                        "distance": 100
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 5.0,
                    "color": (1.0, 0.95, 0.85),
                    "size": 1.0,
                    "angle": 0.53
                }
            }
        ],
        "settings": {
            "base_distance": 100.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"natural_sunlight": True, "sharp_shadows": 1.3}
        },
        "camera_preferences": {
            "angle": "natural_outdoor",
            "height": "subject_level",
            "focal_length": 50,
            "distance": "outdoor_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": -0.1,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    },

    "single_spot": {
        "id": "single_spot",
        "name": "Single Spot",
        "category": "Utilities & Single Lights",
        "description": "Single focused spot light for dramatic highlighting and accent lighting",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Spot Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 45,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 500,
                    "color": (1.0, 0.98, 0.95),
                    "spot_size": 0.785398,
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
            "default": {"focused_highlight": True, "dramatic_accent": 1.4}
        },
        "camera_preferences": {
            "angle": "dramatic_standard",
            "height": "subject_level",
            "focal_length": 85,
            "distance": "dramatic_medium"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": -0.2,
            "highlights": 0.1,
            "clarity": 0.25,
            "color_balance": "neutral"
        }
    }

}

