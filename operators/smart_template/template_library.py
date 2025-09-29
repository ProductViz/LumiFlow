"""
Template Library Module
Comprehensive lighting template definitions with mathematically precise positioning.
"""

import math
from typing import Dict, List, Optional, Tuple, Any

try:
    from ...templates.studio_commercial import STUDIO_COMMERCIAL_TEMPLATES
    from ...templates.dramatic_cinematic import DRAMATIC_CINEMATIC_TEMPLATES
    from ...templates.environment_realistic import ENVIRONMENT_REALISTIC_TEMPLATES
    from ...templates.utilities_single_lights import UTILITIES_SINGLE_LIGHTS_TEMPLATES
    from ...templates import ALL_TEMPLATES
    
    TEMPLATES_IMPORTED = True
except ImportError as e:
    # Fallback for direct execution or development
    TEMPLATES_IMPORTED = False

TEMPLATE_SCHEMA = {
    "id": str,
    "name": str,
    "category": str,  # portrait/product/fashion/automotive
    "description": str,
    "author": str,
    "version": str,
    "lights": [
        {
            "name": str,
            "type": str,  # AREA, SPOT, POINT, SUN
            "position": {
                "method": str,  # "spherical", "cartesian", "relative"
                "params": dict  # method-specific parameters
            },
            "rotation": {
                "target": str,  # "subject", "camera", "world"
                "offset": tuple  # (x, y, z) in radians
            },
            "properties": {
                "size": float,
                "intensity": float,
                "color": tuple,  # (r, g, b) or temperature
                "shape": str   # For area lights
            }
        }
    ],
    "settings": {
        "base_distance": float,  # Reference distance for scaling
        "auto_scale": bool,
        "preserve_existing": bool
    }
}

BUILTIN_TEMPLATES = {}

if TEMPLATES_IMPORTED:
    BUILTIN_TEMPLATES.update(STUDIO_COMMERCIAL_TEMPLATES)
    BUILTIN_TEMPLATES.update(DRAMATIC_CINEMATIC_TEMPLATES) 
    BUILTIN_TEMPLATES.update(ENVIRONMENT_REALISTIC_TEMPLATES)
    BUILTIN_TEMPLATES.update(UTILITIES_SINGLE_LIGHTS_TEMPLATES)
    
    total_templates = len(STUDIO_COMMERCIAL_TEMPLATES) + len(DRAMATIC_CINEMATIC_TEMPLATES) + len(ENVIRONMENT_REALISTIC_TEMPLATES) + len(UTILITIES_SINGLE_LIGHTS_TEMPLATES)
else:
    BUILTIN_TEMPLATES = {
        "default_portrait": {
            "id": "default_portrait",
            "name": "Default Portrait",
            "category": "Studio & Commercial", 
            "description": "Basic portrait lighting setup",
            "author": "LumiFlow",
            "version": "1.0",
            "lights": [
                {
                    "name": "Key Light",
                    "type": "AREA",
                    "position": {
                        "method": "spherical",
                        "params": {"azimuth": 45, "elevation": 45, "distance": 3.0}
                    },
                    "rotation": {"target": "subject", "offset": (0, 0, 0)},
                    "properties": {
                        "size": 2.0, "intensity": 300, "color": (1.0, 1.0, 1.0), "shape": "RECTANGLE"
                    }
                }
            ],
            "settings": {"base_distance": 3.0, "auto_scale": True, "preserve_existing": False},
            "material_adaptations": {"default": {"primary_illumination": True}},
            "camera_preferences": {
                "angle": "standard", "height": "subject_level", "focal_length": 85, "distance": "medium"
            },
            "post_processing": {
                "contrast": 1.1, "shadows": 0.0, "highlights": -0.1, "clarity": 0.1, "color_balance": "neutral"
            }
        }
    }

def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """Get template by ID."""
    try:
        return BUILTIN_TEMPLATES.get(template_id)
    except Exception as e:
        pass
        return None


def list_templates(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List available templates, optionally filtered by category."""
    try:
        templates = []
        
        for template_id, template in BUILTIN_TEMPLATES.items():
            if category and template.get('category') != category:
                continue
            
            template_copy = template.copy()
            template_copy['template_id'] = template_id
            templates.append(template_copy)
        
        return templates
        
    except Exception as e:
        pass
        return []


def validate_template(template: Dict[str, Any]) -> bool:
    """Validate template structure against schema."""
    try:
        required_keys = ['id', 'name', 'category', 'description', 'lights', 'settings']
        for key in required_keys:
            if key not in template:
                return False
        
        lights = template.get('lights', [])
        if not isinstance(lights, list) or len(lights) == 0:
            return False
        
        for light in lights:
            if not isinstance(light, dict):
                return False
            
            light_required = ['name', 'type', 'position', 'rotation', 'properties']
            for light_key in light_required:
                if light_key not in light:
                    return False
            
            valid_types = ['AREA', 'SPOT', 'POINT', 'SUN']
            if light.get('type') not in valid_types:
                return False
            
            position = light.get('position', {})
            valid_methods = ['spherical', 'cartesian', 'relative']
            if position.get('method') not in valid_methods:
                return False
        
        settings = template.get('settings', {})
        if not isinstance(settings, dict):
            return False
        
        settings_required = ['base_distance', 'auto_scale', 'preserve_existing']
        for setting_key in settings_required:
            if setting_key not in settings:
                return False
        
        return True
        
    except Exception as e:
        pass
        return False


def get_template_categories() -> List[str]:
    """Get all available template categories."""
    try:
        categories = set()
        for template in BUILTIN_TEMPLATES.values():
            categories.add(template.get('category', 'unknown'))
        return sorted(list(categories))
    except Exception as e:
        pass
        return []


def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all templates in a specific category."""
    return list_templates(category=category)


def get_template_names() -> List[str]:
    """Get list of all template IDs."""
    try:
        return list(BUILTIN_TEMPLATES.keys())
    except Exception as e:
        pass
        return []


def get_template_count() -> int:
    """Get total number of templates."""
    return len(BUILTIN_TEMPLATES)


def get_studio_commercial_templates() -> Dict[str, Dict[str, Any]]:
    """Get all Studio & Commercial lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'Studio & Commercial'}


def get_dramatic_cinematic_templates() -> Dict[str, Dict[str, Any]]:
    """Get all Dramatic & Cinematic lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'Dramatic & Cinematic'}


def get_environment_realistic_templates() -> Dict[str, Dict[str, Any]]:
    """Get all Environment & Realistic lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'Environment & Realistic'}


def get_utilities_single_lights_templates() -> Dict[str, Dict[str, Any]]:
    """Get all Utilities & Single Lights templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'Utilities & Single Lights'}


def get_architecture_templates() -> Dict[str, Dict[str, Any]]:
    """Get all architecture lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'architecture'}


def get_food_photography_templates() -> Dict[str, Dict[str, Any]]:
    """Get all food photography lighting templates.""" 
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'food'}


def get_nature_landscape_templates() -> Dict[str, Dict[str, Any]]:
    """Get all nature and landscape lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'nature'}


def get_jewelry_luxury_templates() -> Dict[str, Dict[str, Any]]:
    """Get all jewelry and luxury product lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'jewelry'}


def get_cinematic_moods_templates() -> Dict[str, Dict[str, Any]]:
    """Get all cinematic moods lighting templates."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == 'cinematic'}


def get_templates_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """Get templates filtered by category."""
    return {k: v for k, v in BUILTIN_TEMPLATES.items() if v.get('category') == category}


def search_templates(query: str) -> List[Dict[str, Any]]:
    """Search templates by name or description."""
    try:
        results = []
        query_lower = query.lower()
        
        for template_id, template in BUILTIN_TEMPLATES.items():
            name = template.get('name', '').lower()
            description = template.get('description', '').lower()
            category = template.get('category', '').lower()
            
            if query_lower in name or query_lower in description or query_lower in category:
                template_copy = template.copy()
                template_copy['template_id'] = template_id
                results.append(template_copy)
        
        return results
        
    except Exception as e:
        pass
        return []

