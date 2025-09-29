"""
LumiFlow Smart Template Module
Advanced lighting template system for intelligent light placement and configuration.
"""

# Import all smart_template modules
from .lighting_templates import (
    LUMI_OT_apply_lighting_template,
    LUMI_OT_preview_template,
    LUMI_OT_preview_lighting_template,
    LUMI_OT_save_custom_template,
    LUMI_OT_manage_custom_templates,
    LUMI_OT_save_lighting_template,
)
from .template_analyzer import (
    analyze_subject,
    detect_subject_type,
    SubjectAnalysis,
)
from .template_library import (
    BUILTIN_TEMPLATES,
    get_template,
    list_templates,
    validate_template,
    get_studio_commercial_templates,
    get_dramatic_cinematic_templates,
    get_environment_realistic_templates,
    get_utilities_single_lights_templates,
)

# Import error handling system
from .template_error_handling import (
    initialize_error_handling,
    cleanup_error_handling,
    TemplateError,
    TemplateNotFoundError,
    InvalidTemplateError,
    SceneValidationError
)


# Import template operators
from .template_ops import (
    LUMI_OT_toggle_template_favorite,
    LUMI_OT_set_template_category,
    LUMI_OT_save_lighting_template,
    LUMI_OT_apply_template_direct,
    LUMI_OT_apply_template_default,
    LUMI_OT_apply_template,
    LUMI_OT_show_all_templates,
)

# Export for registration
__all__ = [
    'LUMI_OT_apply_lighting_template',
    'LUMI_OT_preview_template',
    'LUMI_OT_preview_lighting_template',
    'LUMI_OT_save_custom_template',
    'LUMI_OT_manage_custom_templates',
    'LUMI_OT_save_lighting_template',
    'analyze_subject',
    'detect_subject_type',
    'SubjectAnalysis',
    'BUILTIN_TEMPLATES',
    'get_template',
    'list_templates',
    'validate_template',
    'get_studio_commercial_templates',
    'get_dramatic_cinematic_templates', 
    'get_environment_realistic_templates',
    'get_utilities_single_lights_templates',
    # Error handling system
    'initialize_error_handling',
    'cleanup_error_handling',
    'TemplateError',
    'TemplateNotFoundError',
    'InvalidTemplateError',
    'SceneValidationError',
    # Template operators
    'LUMI_OT_toggle_template_favorite',
    'LUMI_OT_set_template_category',
    'LUMI_OT_save_lighting_template',
    'LUMI_OT_apply_template_direct',
    'LUMI_OT_apply_template_default',
    'LUMI_OT_apply_template',
    'LUMI_OT_show_all_templates',
]

