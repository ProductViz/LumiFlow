"""Template System - Core business logic for template application."""

import bpy
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..operators.smart_template.template_library import get_template
from ..utils.scene_context import SceneContext


@dataclass
class ValidationResult:
    """Validation result container."""
    valid: bool
    errors: List[str]
    warnings: List[str]

    @staticmethod
    def success() -> 'ValidationResult':
        return ValidationResult(True, [], [])

    @staticmethod
    def failure(error: str) -> 'ValidationResult':
        return ValidationResult(False, [error], [])


class TemplateSystem:
    """Core template application business logic."""

    def __init__(self):
        self.current_template = None

    def validate_template(self, template_id: str) -> ValidationResult:
        """Validate template exists and has correct structure."""
        template = get_template(template_id)

        if not template:
            return ValidationResult.failure(f"Template '{template_id}' not found")

        if 'lights' not in template:
            return ValidationResult.failure("Template missing 'lights' definition")

        if not isinstance(template['lights'], list) or len(template['lights']) == 0:
            return ValidationResult.failure("Template has no lights defined")

        self.current_template = template
        return ValidationResult.success()

    def validate_scene(self, context: bpy.types.Context,
                      selected_objects: List[bpy.types.Object]) -> ValidationResult:
        """Validate scene state for template application."""
        errors = []
        warnings = []

        if not selected_objects:
            errors.append("No objects selected")

        if not context.scene.camera:
            warnings.append("No camera in scene")

        if context.mode != 'OBJECT':
            errors.append("Must be in Object Mode")

        if errors:
            return ValidationResult(False, errors, warnings)
        return ValidationResult(True, [], warnings)

    def get_template_metadata(self, template_id: str) -> Dict[str, Any]:
        """Get template metadata."""
        template = get_template(template_id)
        if not template:
            return {}

        return {
            'id': template_id,
            'name': template.get('name', template_id),
            'description': template.get('description', ''),
            'category': template.get('category', 'general'),
            'light_count': len(template.get('lights', []))
        }


__all__ = ['TemplateSystem', 'ValidationResult']