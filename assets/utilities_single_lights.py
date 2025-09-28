# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

# -*- coding: utf-8 -*-
"""
LumiFlow Utilities & Single Lights Templates
Simple and utility lighting setups for quick illumination
"""

# Utilities & Single Lights Templates Collection
UTILITIES_SINGLE_LIGHTS_TEMPLATES = {
    "key_light_only": {
        "id": "key_light_only",
        "name": "Key Light Only",
        "category": "Utilities & Single Lights",
        "description": "Simple single key light for basic subject illumination",
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
                    "size": 2.0,
                    "intensity": 300,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"basic_illumination": True}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.0,
            "highlights": 0.0,
            "clarity": 0.0,
            "color_balance": "neutral"
        }
    },

    "fill_light_only": {
        "id": "fill_light_only",
        "name": "Fill Light Only",
        "category": "Utilities & Single Lights",
        "description": "Soft fill light for shadow reduction and gentle illumination",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Fill Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -30,
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
                    "intensity": 200,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.5,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"shadow_fill": True, "gentle_illumination": 1.0}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": 0.0,
            "clarity": 0.0,
            "color_balance": "neutral"
        }
    },

    "rim_light_only": {
        "id": "rim_light_only",
        "name": "Rim Light Only",
        "category": "Utilities & Single Lights",
        "description": "Strong rim light for subject separation and edge definition",
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
                    "intensity": 400,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.8,
                    "spot_blend": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 2.5,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"edge_definition": True, "separation_enhancement": 1.2}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.0,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "hair_light_special": {
        "id": "hair_light_special",
        "name": "Hair Light Special",
        "category": "Utilities & Single Lights",
        "description": "Specialized hair light for portrait enhancement and hair separation",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Hair Light",
                "type": "SPOT",
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
                    "offset": (0, 0, 0.5)
                },
                "properties": {
                    "intensity": 250,
                    "color": (1.0, 0.95, 0.9),
                    "spot_size": 1.0,
                    "spot_blend": 0.3
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "hair": {"strand_definition": True, "highlight_enhancement": 1.3},
            "fabric": {"texture_accent": True}
        },
        "camera_preferences": {
            "angle": "portrait_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.0,
            "highlights": -0.05,
            "clarity": 0.1,
            "color_balance": "warm"
        }
    },

    "background_wash": {
        "id": "background_wash",
        "name": "Background Wash",
        "category": "Utilities & Single Lights",
        "description": "Even background illumination for clean backdrop lighting",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
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
                    "target": "background",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 5.0,
                    "size_y": 4.0,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "backdrop": {"even_illumination": True, "clean_appearance": 1.1}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.0,
            "color_balance": "neutral"
        }
    },

    "top_down_light": {
        "id": "top_down_light",
        "name": "Top-Down Light",
        "category": "Utilities & Single Lights",
        "description": "Overhead lighting for flat lay photography and top-down shots",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Overhead Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 400,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"even_coverage": True, "flat_illumination": 1.0}
        },
        "camera_preferences": {
            "angle": "top_down",
            "height": "overhead",
            "focal_length": 50,
            "distance": "flat_lay"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "side_light_drama": {
        "id": "side_light_drama",
        "name": "Side Light Drama",
        "category": "Utilities & Single Lights",
        "description": "Strong side lighting for dramatic shadows and texture emphasis",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Side Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 30,
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
                    "intensity": 500,
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
            "default": {"texture_emphasis": 1.3, "dramatic_shadows": True}
        },
        "camera_preferences": {
            "angle": "dramatic_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.4,
            "shadows": -0.2,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "neutral"
        }
    },

    "under_light_eerie": {
        "id": "under_light_eerie",
        "name": "Under Light Eerie",
        "category": "Utilities & Single Lights",
        "description": "Upward lighting from below for dramatic and eerie effects",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Under Light",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 0,
                        "z": -1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "intensity": 350,
                    "color": (0.9, 0.95, 1.0),
                    "shape": "SQUARE"
                }
            }
        ],
        "settings": {
            "base_distance": 1.5,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"eerie_lighting": True, "upward_shadows": 1.2}
        },
        "camera_preferences": {
            "angle": "dramatic_low",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "close"
        },
        "post_processing": {
            "contrast": 1.5,
            "shadows": -0.3,
            "highlights": -0.2,
            "clarity": 0.2,
            "color_balance": "cool"
        }
    },

    "bounce_card_soft": {
        "id": "bounce_card_soft",
        "name": "Bounce Card Soft",
        "category": "Utilities & Single Lights",
        "description": "Soft bounce card lighting for gentle fill and natural reflections",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Bounce Card",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 20,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.5,
                    "intensity": 150,
                    "color": (0.98, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"soft_fill": True, "natural_reflection": 1.0}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_close"
        },
        "post_processing": {
            "contrast": 0.9,
            "shadows": 0.4,
            "highlights": 0.0,
            "clarity": 0.0,
            "color_balance": "neutral"
        }
    },

    "spot_accent": {
        "id": "spot_accent",
        "name": "Spot Accent",
        "category": "Utilities & Single Lights",
        "description": "Focused spot light for highlighting specific details or areas",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Spot Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 60,
                        "elevation": 45,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (1.0, 1.0, 1.0),
                    "spot_size": 0.5,
                    "spot_blend": 0.1
                }
            }
        ],
        "settings": {
            "base_distance": 2.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"detail_highlight": True, "focused_illumination": 1.2}
        },
        "camera_preferences": {
            "angle": "detail_focus",
            "height": "eye_level",
            "focal_length": 100,
            "distance": "close_detail"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.0,
            "highlights": -0.1,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "ambient_base": {
        "id": "ambient_base",
        "name": "Ambient Base",
        "category": "Utilities & Single Lights",
        "description": "Basic ambient lighting for overall scene illumination and base exposure",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Ambient Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 60,
                        "distance": 5.0
                    }
                },
                "rotation": {
                    "target": "scene_center",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 8.0,
                    "intensity": 150,
                    "color": (0.95, 0.95, 1.0),
                    "shape": "DISK"
                }
            }
        ],
        "settings": {
            "base_distance": 5.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"base_illumination": True, "ambient_exposure": 1.0}
        },
        "camera_preferences": {
            "angle": "standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 0.8,
            "shadows": 0.5,
            "highlights": 0.0,
            "clarity": 0.0,
            "color_balance": "neutral"
        }
    },

    "color_gel_accent": {
        "id": "color_gel_accent",
        "name": "Color Gel Accent",
        "category": "Utilities & Single Lights",
        "description": "Colored accent light for mood enhancement and creative color effects",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Color Accent",
                "type": "SPOT",
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
                    "intensity": 200,
                    "color": (0.2, 0.6, 1.0),
                    "spot_size": 1.2,
                    "spot_blend": 0.4
                }
            }
        ],
        "settings": {
            "base_distance": 3.0,
            "auto_scale": True,
            "preserve_existing": True
        },
        "material_adaptations": {
            "default": {"color_enhancement": True, "mood_lighting": 1.1}
        },
        "camera_preferences": {
            "angle": "creative_standard",
            "height": "eye_level",
            "focal_length": 50,
            "distance": "medium"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.1,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "creative"
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
                    "shape": "SQUARE"
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
    }
}

# Export untuk template system
__all__ = ['UTILITIES_SINGLE_LIGHTS_TEMPLATES']

