# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

# -*- coding: utf-8 -*-
"""
LumiFlow Studio & Commercial Templates
Professional lighting setups for studio and commercial photography
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
                "name": "Fill Card",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -25,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 2.8,
                    "intensity": 100,
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
                        "azimuth": 0,
                        "elevation": 70,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0.3)
                },
                "properties": {
                    "intensity": 200,
                    "color": (1.0, 0.95, 0.9),
                    "spot_size": 0.8,
                    "spot_blend": 0.3
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
                    "size": 5.0,
                    "size_y": 3.5,
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
            "skin": {"flattering_tones": True, "smooth_rendering": True},
            "fabric": {"texture_detail": 1.1, "color_richness": 1.2},
            "jewelry": {"sparkle_control": True, "highlight_management": 0.9}
        },
        "camera_preferences": {
            "angle": "portrait_standard",
            "height": "eye_level",
            "focal_length": 85,
            "distance": "portrait_medium"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.2,
            "color_balance": "warm"
        }
    },

    "loop_portrait": {
        "id": "loop_portrait",
        "name": "Loop Portrait",
        "category": "Studio & Commercial",
        "description": "Classic loop lighting pattern for standard portrait photography",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Key Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 35,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "size_y": 3.2,
                    "intensity": 300,
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
                        "azimuth": -45,
                        "elevation": 25,
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
                "name": "Background Light",
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
                    "size": 4.0,
                    "size_y": 3.0,
                    "intensity": 80,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 2.8,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "skin": {"natural_tones": True, "soft_shadows": True},
            "fabric": {"texture_clarity": True, "color_accuracy": 1.1}
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
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "box_lighting_360": {
        "id": "box_lighting_360",
        "name": "Box Lighting 360Â°",
        "category": "Studio & Commercial",
        "description": "Even 360-degree lighting for products requiring uniform illumination from all angles",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Front Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
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
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Left Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
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
                    "intensity": 180,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Right Light",
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
                    "size": 3.0,
                    "intensity": 180,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Back Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 180,
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
                    "intensity": 160,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Top Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 80,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "intensity": 150,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Bottom Fill",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -45,
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
                    "intensity": 80,
                    "color": (0.98, 0.98, 1.0),
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
            "default": {"uniform_illumination": True, "shadow_minimization": 0.9},
            "metal": {"reflection_control": True, "even_highlights": True},
            "glass": {"transparency_clarity": True, "refraction_balance": 1.1}
        },
        "camera_preferences": {
            "angle": "product_360",
            "height": "product_level",
            "focal_length": 50,
            "distance": "product_standard"
        },
        "post_processing": {
            "contrast": 0.95,
            "shadows": 0.4,
            "highlights": -0.2,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    },

    "studio_sweep": {
        "id": "studio_sweep",
        "name": "Studio Sweep",
        "category": "Studio & Commercial",
        "description": "Smooth gradient background lighting with seamless backdrop illumination",
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
                        "elevation": 35,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.2,
                    "intensity": 250,
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
                        "azimuth": -30,
                        "elevation": 25,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.5,
                    "size_y": 4.5,
                    "intensity": 120,
                    "color": (0.98, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Top",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 4.0,
                        "z": 2.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, -1.0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.5,
                    "intensity": 200,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Bottom",
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
                    "target": "background",
                    "offset": (0, 0, -0.5)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.5,
                    "intensity": 100,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Sweep Gradient",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 2.0,
                        "z": -2.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 45, 0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 5.0,
                    "intensity": 80,
                    "color": (0.98, 0.99, 1.0),
                    "shape": "RECTANGLE"
                }
            }
        ],
        "settings": {
            "base_distance": 3.2,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "default": {"background_separation": True, "smooth_falloff": 1.2},
            "reflective": {"background_control": True, "clean_reflections": 0.9}
        },
        "camera_preferences": {
            "angle": "studio_standard",
            "height": "product_level",
            "focal_length": 50,
            "distance": "medium_wide"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.05,
            "color_balance": "neutral"
        }
    },

    "full_body_fashion": {
        "id": "full_body_fashion",
        "name": "Full Body Fashion",
        "category": "Studio & Commercial",
        "description": "Even full-body lighting setup for fashion catalog and modeling photography",
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
                        "distance": 4.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.0,
                    "size_y": 5.5,
                    "intensity": 300,
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
                        "azimuth": -45,
                        "elevation": 30,
                        "distance": 4.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 4.5,
                    "size_y": 6.0,
                    "intensity": 150,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Body Light Left",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -90,
                        "elevation": 10,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, -0.5, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 100,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Body Light Right",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 10,
                        "distance": 3.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, -0.5, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 4.0,
                    "intensity": 100,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Strip",
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
                    "size_y": 4.5,
                    "intensity": 120,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Hair Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": 70,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0.8)
                },
                "properties": {
                    "intensity": 180,
                    "color": (1.0, 0.95, 0.9),
                    "spot_size": 1.0,
                    "spot_blend": 0.2
                }
            }
        ],
        "settings": {
            "base_distance": 4.0,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "fabric": {"texture_detail": 1.1, "color_accuracy": 1.2, "wrinkle_definition": True},
            "skin": {"natural_tones": True, "full_body_evenness": True},
            "accessories": {"detail_clarity": True, "material_distinction": 1.1}
        },
        "camera_preferences": {
            "angle": "fashion_standard",
            "height": "chest_level",
            "focal_length": 85,
            "distance": "full_body"
        },
        "post_processing": {
            "contrast": 1.1,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.15,
            "color_balance": "neutral"
        }
    },

    "food_menu_shot": {
        "id": "food_menu_shot",
        "name": "Food Menu Shot",
        "category": "Studio & Commercial",
        "description": "Clean and bright lighting setup for food photography and menu items",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Food Light",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 45,
                        "elevation": 60,
                        "distance": 2.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 2.8,
                    "intensity": 400,
                    "color": (1.0, 0.98, 0.94),
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
                        "elevation": 45,
                        "distance": 2.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.5,
                    "intensity": 200,
                    "color": (0.95, 0.98, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Side Accent",
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
                    "size": 1.5,
                    "size_y": 2.2,
                    "intensity": 150,
                    "color": (1.0, 0.96, 0.92),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Background Clean",
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
                    "size": 4.0,
                    "size_y": 3.0,
                    "intensity": 100,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Texture Detail",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 15,
                        "distance": 1.8
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 120,
                    "color": (1.0, 0.94, 0.88),
                    "spot_size": 1.2,
                    "spot_blend": 0.4
                }
            }
        ],
        "settings": {
            "base_distance": 2.2,
            "auto_scale": True,
            "preserve_existing": False
        },
        "material_adaptations": {
            "food": {"appetite_appeal": True, "texture_enhancement": 1.3, "color_vibrancy": 1.2},
            "liquid": {"clarity_control": True, "surface_tension": 1.1},
            "ceramic": {"clean_appearance": True, "subtle_reflections": 0.8}
        },
        "camera_preferences": {
            "angle": "food_overhead",
            "height": "table_above",
            "focal_length": 50,
            "distance": "food_close"
        },
        "post_processing": {
            "contrast": 1.2,
            "shadows": 0.3,
            "highlights": -0.1,
            "clarity": 0.25,
            "color_balance": "warm"
        }
    },

    "jewelry_focus": {
        "id": "jewelry_focus",
        "name": "Jewelry Focus",
        "category": "Studio & Commercial",
        "description": "Specialized lighting for jewelry with enhanced sparkle and detail definition",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Main Brilliance",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 30,
                        "elevation": 45,
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 1.5,
                    "intensity": 500,
                    "color": (1.0, 1.0, 1.0),
                    "shape": "SQUARE"
                }
            },
            {
                "name": "Sparkle Accent",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -45,
                        "elevation": 60,
                        "distance": 1.2
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 300,
                    "color": (1.0, 0.98, 0.96),
                    "spot_size": 0.5,
                    "spot_blend": 0.1
                }
            },
            {
                "name": "Side Definition",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 120,
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
                    "size_y": 1.8,
                    "intensity": 200,
                    "color": (0.98, 1.0, 0.98),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Facet Light",
                "type": "SPOT",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 90,
                        "elevation": 15,
                        "distance": 1.5
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "intensity": 250,
                    "color": (1.0, 0.99, 0.97),
                    "spot_size": 0.7,
                    "spot_blend": 0.2
                }
            },
            {
                "name": "Background Soft",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": 0,
                        "y": 2.5,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 3.0,
                    "size_y": 2.0,
                    "intensity": 80,
                    "color": (0.95, 0.97, 1.0),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Reflection Card",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": 0,
                        "elevation": -30,
                        "distance": 1.0
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
                    "color": (1.0, 1.0, 1.0),
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
            "diamond": {"brilliant_cut_enhancement": True, "fire_dispersion": 1.5},
            "gold": {"warm_reflections": True, "polish_definition": 1.3},
            "silver": {"cool_reflections": True, "mirror_finish": 1.2},
            "gemstone": {"color_saturation": 1.4, "clarity_boost": 1.3},
            "pearl": {"lustre_enhancement": True, "surface_smoothness": 1.2}
        },
        "camera_preferences": {
            "angle": "jewelry_macro",
            "height": "jewelry_level",
            "focal_length": 100,
            "distance": "macro_close"
        },
        "post_processing": {
            "contrast": 1.3,
            "shadows": 0.1,
            "highlights": -0.05,
            "clarity": 0.3,
            "color_balance": "neutral"
        }
    },

    "gradient_background_elegant": {
        "id": "gradient_background_elegant",
        "name": "Gradient Background Elegant",
        "category": "Dramatic & Cinematic",
        "description": "Smooth elegant gradient background lighting for modern sophisticated looks",
        "author": "LumiFlow",
        "version": "1.0",
        "lights": [
            {
                "name": "Subject Key",
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
                    "size": 2.5,
                    "intensity": 300,
                    "color": (1.0, 0.98, 0.95),
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
                        "z": 2.5
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, -1.0)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 5.0,
                    "intensity": 180,
                    "color": (0.95, 0.97, 1.0),
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
                        "z": -2.0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 0, -0.3)
                },
                "properties": {
                    "size": 8.0,
                    "size_y": 5.0,
                    "intensity": 60,
                    "color": (0.85, 0.90, 0.98),
                    "shape": "RECTANGLE"
                }
            },
            {
                "name": "Side Accent",
                "type": "AREA",
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": -60,
                        "elevation": 25,
                        "distance": 3.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": (0, 0, 0)
                },
                "properties": {
                    "size": 2.0,
                    "size_y": 1.2,
                    "intensity": 120,
                    "color": (0.92, 0.95, 1.0),
                    "shape": "ELLIPSE"
                }
            },
            {
                "name": "Edge Softness",
                "type": "AREA",
                "position": {
                    "method": "cartesian",
                    "params": {
                        "x": -3.0,
                        "y": 4.0,
                        "z": 0
                    }
                },
                "rotation": {
                    "target": "background",
                    "offset": (0, 30, 0)
                },
                "properties": {
                    "size": 6.0,
                    "size_y": 4.0,
                    "intensity": 80,
                    "color": (0.90, 0.93, 0.98),
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
            "default": {"smooth_transitions": True, "elegant_finish": 1.1},
            "reflective": {"gradient_reflections": True, "clean_highlights": 0.9},
            "matte": {"gradient_separation": True, "soft_contrast": 0.8}
        },
        "camera_preferences": {
            "angle": "elegant_standard",
            "height": "subject_level",
            "focal_length": 85,
            "distance": "elegant_medium"
        },
        "post_processing": {
            "contrast": 1.0,
            "shadows": 0.2,
            "highlights": -0.1,
            "clarity": 0.1,
            "color_balance": "neutral"
        }
    }
}

# Export untuk template system
__all__ = ['STUDIO_COMMERCIAL_TEMPLATES']

