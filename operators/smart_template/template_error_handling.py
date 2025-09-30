# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Template Error Handling
Error handling and recovery utilities for template operations.
"""

import bpy
import time
import traceback
from typing import List, Dict, Tuple, Optional, Any
from contextlib import contextmanager


class TemplateError(Exception):
    """Base exception for template system"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        self.message = message
        self.error_code = error_code or "TEMPLATE_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class TemplateNotFoundError(TemplateError):
    """Template ID not found"""
    
    def __init__(self, template_id: str, available_templates: List[str] = None):
        message = f"Template '{template_id}' not found"
        details = {
            "template_id": template_id,
            "available_templates": available_templates or []
        }
        super().__init__(message, "TEMPLATE_NOT_FOUND", details)


class InvalidTemplateError(TemplateError):
    """Template data corrupted or invalid"""
    
    def __init__(self, template_id: str, validation_errors: List[str] = None):
        message = f"Template '{template_id}' is invalid or corrupted"
        details = {
            "template_id": template_id,
            "validation_errors": validation_errors or []
        }
        super().__init__(message, "INVALID_TEMPLATE", details)


class SceneValidationError(TemplateError):
    """Scene doesn't meet requirements"""
    
    def __init__(self, validation_errors: List[str], warnings: List[str] = None):
        message = "Scene validation failed"
        details = {
            "errors": validation_errors,
            "warnings": warnings or []
        }
        super().__init__(message, "SCENE_VALIDATION_ERROR", details)


class TemplateOperationError(TemplateError):
    """Error during template operation"""
    
    def __init__(self, operation: str, original_exception: Exception = None):
        message = f"Template operation '{operation}' failed"
        details = {
            "operation": operation,
            "original_exception": str(original_exception) if original_exception else None
        }
        super().__init__(message, "OPERATION_ERROR", details)


class TemplateResourceError(TemplateError):
    """Resource-related error (memory, file access, etc.)"""
    
    def __init__(self, resource_type: str, details: str):
        message = f"Resource error: {resource_type} - {details}"
        super().__init__(message, "RESOURCE_ERROR", {"resource_type": resource_type, "details": details})


# ===== ERROR MESSAGES CATALOG =====

ERROR_MESSAGES = {
    # Selection errors
    "no_selection": "Please select at least one mesh object to light",
    "invalid_selection": "Selected objects must be mesh objects",
    "empty_selection": "Selection contains no valid mesh objects",
    
    # Template errors
    "template_not_found": "Template '{}' not found. Check template library or reinstall addon.",
    "invalid_template": "Template data is corrupted. Please update addon or report issue.",
    "template_load_failed": "Failed to load template '{}'. File may be corrupted.",
    "template_save_failed": "Cannot save template. Check file permissions and disk space.",
    
    # Scene errors
    "no_camera": "This template requires an active camera. Please add and select a camera.",
    "no_objects": "No objects in scene to analyze for lighting setup.",
    "scene_too_complex": "Scene is too complex ({} objects). Consider simplifying.",
    "large_scale_warning": "Large scene scale detected. Lights may appear too small.",
    
    # Resource errors
    "permission_denied": "Cannot access file system. Check folder permissions.",
    "out_of_memory": "Not enough memory to complete operation. Close other applications.",
    "disk_space_low": "Insufficient disk space to save template files.",
    
    # Operation errors
    "light_creation_failed": "Failed to create light '{}'. Check scene limits.",
    "collection_error": "Cannot access LumiFlow collection. Check addon installation.",
    "viewport_error": "Viewport update failed. Scene may be corrupted.",
    "analysis_failed": "Subject analysis failed. Try selecting different objects.",
    
    # System errors
    "addon_not_enabled": "LumiFlow addon is not properly enabled. Check preferences.",
    "blender_version": "This feature requires Blender {} or newer.",
    "context_invalid": "Invalid Blender context. Try operation in 3D viewport.",
    "mode_not_supported": "This operation is not supported in current mode.",
}

SOLUTION_SUGGESTIONS = {
    "no_selection": "Select one or more mesh objects in the 3D viewport before applying template.",
    "template_not_found": "Check if template exists in library. Try refreshing template list or reinstalling addon.",
    "invalid_template": "Delete corrupted template and reinstall addon, or report bug to developer.",
    "no_camera": "Add a camera to scene: Shift+A > Camera, then select it as active camera.",
    "permission_denied": "Run Blender as administrator or check folder permissions.",
    "out_of_memory": "Close other applications, reduce scene complexity, or restart Blender.",
    "light_creation_failed": "Check scene object limit (1000 objects max). Delete unused objects.",
    "collection_error": "Reinstall LumiFlow addon or reset addon preferences.",
    "analysis_failed": "Ensure objects have valid geometry and materials.",
}


# ===== VALIDATION FUNCTIONS =====

def validate_scene_for_template(context: bpy.types.Context, template: Dict) -> Tuple[List[str], List[str]]:
    """Validate scene before applying template"""
    
    errors = []
    warnings = []
    
    try:
        # Check context validity
        if not context:
            errors.append("Invalid Blender context")
            return errors, warnings
        
        if not context.scene:
            errors.append("No active scene")
            return errors, warnings
        
        # Check selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            warnings.append("No objects selected")
        
        mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH']
        if not mesh_objects:
            errors.append("invalid_selection")
        
        # Check scene scale
        try:
            scale = context.scene.unit_settings.scale_length
            if scale > 100:
                warnings.append("large_scale_warning")
            elif scale < 0.001:
                warnings.append("Scene scale very small, lights may be too large")
        except AttributeError:
            pass  # Unit settings not available in older versions
        
        # Check existing lights
        existing_lights = [o for o in context.scene.objects if o.type == 'LIGHT']
        if len(existing_lights) > 20:
            warnings.append(f"{len(existing_lights)} lights already in scene - performance may be affected")
        
        # Check object limit
        total_objects = len(context.scene.objects)
        if total_objects > 800:
            warnings.append(f"Scene has {total_objects} objects - approaching Blender limits")
        elif total_objects > 1000:
            errors.append("scene_too_complex")
        
        # Template-specific checks
        if template:
            if template.get("requires_camera") and not context.scene.camera:
                errors.append("no_camera")
            
            if template.get("requires_world") and not context.scene.world:
                errors.append("No world settings available for template")
            
            # Check template complexity
            light_count = len(template.get("lights", []))
            if light_count > 15:
                warnings.append(f"Template creates {light_count} lights - may impact performance")
        
        # Check addon state
        from ...utils.common import lumi_is_addon_enabled
        if not lumi_is_addon_enabled():
            errors.append("addon_not_enabled")
        
        # Check Blender version for advanced features
        if bpy.app.version < (3, 0, 0):
            warnings.append("Some features may not work properly in Blender versions older than 3.0")
        
    except Exception as e:
        errors.append(f"Validation failed: {str(e)}")
    
    return errors, warnings

def validate_template_data(template: Dict) -> Tuple[bool, List[str]]:
    """Validate template data structure"""
    
    errors = []
    
    if not isinstance(template, dict):
        errors.append("Template must be a dictionary")
        return False, errors
    
    # Required fields
    required_fields = ["id", "name", "category", "lights"]
    for field in required_fields:
        if field not in template:
            errors.append(f"Missing required field: {field}")
    
    # Validate lights array
    if "lights" in template:
        lights = template["lights"]
        if not isinstance(lights, list):
            errors.append("Lights must be an array")
        else:
            for i, light in enumerate(lights):
                if not isinstance(light, dict):
                    errors.append(f"Light {i}: must be an object")
                    continue
                
                # Required light fields
                light_required = ["name", "type", "position", "properties"]
                for field in light_required:
                    if field not in light:
                        errors.append(f"Light {i}: missing field '{field}'")
                
                # Validate light type
                if "type" in light and light["type"] not in ["AREA", "SPOT", "POINT", "SUN"]:
                    errors.append(f"Light {i}: invalid type '{light['type']}'")
                
                # Validate position
                if "position" in light:
                    pos = light["position"]
                    if not isinstance(pos, dict):
                        errors.append(f"Light {i}: position must be an object")
                    elif "method" not in pos:
                        errors.append(f"Light {i}: position missing method")
    
    return len(errors) == 0, errors

def validate_blender_context(context: bpy.types.Context) -> Tuple[bool, List[str]]:
    """Validate Blender context for template operations"""
    
    errors = []
    
    if not context:
        errors.append("context_invalid")
        return False, errors
    
    # Check we're in the right space
    if hasattr(context, 'space_data') and context.space_data:
        if context.space_data.type != 'VIEW_3D':
            errors.append("Operation must be performed in 3D Viewport")
    
    # Check we're in object mode
    if context.mode != 'OBJECT':
        errors.append("mode_not_supported")
    
    # Check scene exists
    if not context.scene:
        errors.append("No active scene")
    
    return len(errors) == 0, errors

def report_errors(operator: bpy.types.Operator, errors: List[str], warnings: List[str]) -> bool:
    """Report errors and warnings to user with solutions"""
    
    # Critical errors - prevent operation
    if errors:
        error_messages = []
        solution_messages = []
        
        for error in errors:
            # Get user-friendly message
            message = ERROR_MESSAGES.get(error, error)
            error_messages.append(f"â€¢ {message}")
            
            # Get solution suggestion
            solution = SOLUTION_SUGGESTIONS.get(error)
            if solution:
                solution_messages.append(f"â†’ {solution}")
        
        # Report error
        error_text = "Cannot apply template:\n" + "\n".join(error_messages)
        if solution_messages:
            error_text += "\n\nSolutions:\n" + "\n".join(solution_messages)
        
        operator.report({'ERROR'}, error_text)
        return False
    
    # Warnings - show but allow operation to continue
    if warnings:
        for warning in warnings:
            warning_message = ERROR_MESSAGES.get(warning, warning)
            operator.report({'WARNING'}, warning_message)
    
    return True


def report_exception(operator: bpy.types.Operator, exception: Exception, operation: str = "operation"):
    """Report exception with context and debugging info"""
    
    if isinstance(exception, TemplateError):
        # Our custom errors - user-friendly reporting
        message = f"{operation.title()} failed: {exception.message}"
        
        # Add details if available
        if exception.details:
            if "suggestions" in exception.details:
                message += "\n\nSuggestions:\n" + "\n".join(f"â€¢ {s}" for s in exception.details["suggestions"])
        
        operator.report({'ERROR'}, message)
    else:
        
        operator.report({'ERROR'}, f"{operation.title()} failed: {str(exception)}")
        
        
        pass




class TemplateOperationStack:
    """Track operations for undo/recovery"""
    
    def __init__(self):
        self.operations = []
        self.created_objects = []
        self.modified_objects = {}  # object: original_data
        self.created_collections = []
        self.start_time = time.time()
    
    def push_object_creation(self, objects: List[bpy.types.Object]):
        """Track created objects"""
        self.operations.append(("create_objects", objects))
        self.created_objects.extend(objects)
    
    def push_object_modification(self, obj: bpy.types.Object, original_data: Dict):
        """Track object modification"""
        if obj not in self.modified_objects:
            self.modified_objects[obj] = original_data
        self.operations.append(("modify_object", obj))
    
    def push_collection_creation(self, collection: bpy.types.Collection):
        """Track created collections"""
        self.operations.append(("create_collection", collection))
        self.created_collections.append(collection)
    
    def rollback(self):
        """Undo all operations"""
        try:
            # Process operations in reverse order
            for operation_type, data in reversed(self.operations):
                try:
                    if operation_type == "create_objects":
                        for obj in data:
                            if obj and obj.name in bpy.data.objects:
                                bpy.data.objects.remove(obj, do_unlink=True)
                    
                    elif operation_type == "modify_object":
                        obj = data
                        if obj and obj.name in bpy.data.objects:
                            original = self.modified_objects.get(obj, {})
                            # Restore original properties
                            for prop, value in original.items():
                                if hasattr(obj, prop):
                                    setattr(obj, prop, value)
                    
                    elif operation_type == "create_collection":
                        collection = data
                        if collection and collection.name in bpy.data.collections:
                            bpy.data.collections.remove(collection)
                
                except Exception as e:
                    pass
            
            # Clear tracking
            self.operations.clear()
            self.created_objects.clear()
            self.modified_objects.clear()
            self.created_collections.clear()
            
            pass
            
        except Exception as e:
            pass


# ===== SAFE OPERATION DECORATORS =====

def safe_template_operation(operation_name: str):
    """Decorator for safe template operations with automatic error handling"""
    
    def decorator(func):
        def wrapper(self, context, *args, **kwargs):
            # Create operation stack for rollback
            operation_stack = TemplateOperationStack()
            
            try:
                # Validate context first
                context_valid, context_errors = validate_blender_context(context)
                if not context_valid:
                    report_errors(self, context_errors, [])
                    return {'CANCELLED'}
                
                # Execute the operation
                result = func(self, context, operation_stack, *args, **kwargs)
                
                # Operation succeeded
                return result
                
            except TemplateError as e:
                # Our custom errors - user-friendly handling
                operation_stack.rollback()
                report_exception(self, e, operation_name)
                return {'CANCELLED'}
                
            except Exception as e:
                # System errors - rollback and report
                operation_stack.rollback()
                report_exception(self, e, operation_name)
                return {'CANCELLED'}
        
        return wrapper
    return decorator


@contextmanager
def safe_template_context(operator: bpy.types.Operator, operation: str):
    """Context manager for safe template operations"""
    
    operation_stack = TemplateOperationStack()
    
    try:
        yield operation_stack
        # If we get here, operation succeeded
        
    except TemplateError as e:
        operation_stack.rollback()
        report_exception(operator, e, operation)
        raise
        
    except Exception as e:
        operation_stack.rollback()
        report_exception(operator, e, operation)
        raise TemplateOperationError(operation, e)


# ===== UTILITY FUNCTIONS =====

def get_template_error_context() -> Dict[str, Any]:
    """Get current context information for error reporting"""
    
    context_info = {
        "timestamp": time.time(),
        "blender_version": bpy.app.version_string,
        "addon_version": "1.0.0",  # Should come from addon metadata
    }
    
    try:
        context = bpy.context
        if context:
            context_info.update({
                "mode": context.mode,
                "selected_objects": len(context.selected_objects),
                "scene_objects": len(context.scene.objects) if context.scene else 0,
                "active_object": context.active_object.name if context.active_object else None,
            })
    except:
        pass
    
    return context_info


def log_template_error(error: Exception, context_info: Dict = None):
    """Log detailed error information for debugging"""
    
    log_entry = {
        "timestamp": time.time(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context_info or get_template_error_context(),
        "traceback": traceback.format_exc()
    }
    
    pass


# ===== INITIALIZATION =====

def initialize_error_handling():
    """Initialize error handling system"""
    
    pass
    
   
    pass


def cleanup_error_handling():
    """Cleanup error handling resources"""
    
    pass

