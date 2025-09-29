import bpy

class BaseModalOperator:
    """Base class for modal operators with shared functionality"""
    
    # Variables for core modal functionality
    _dragging = False
    _original_positions = {}
    _original_rotations = {}
    _original_pivots = {}

    def __init__(self):
        self._is_running = False

    def store_original_positions(self, context):
        """Store original positions for undo functionality"""
        self._original_positions.clear()
        self._original_rotations.clear()
        self._original_pivots.clear()
        
        # Store position, rotation, and pivot for each selected light
        for light in context.selected_objects:
            if light.type == 'LIGHT':
                self._original_positions[light.name] = light.location.copy()
                self._original_rotations[light.name] = light.rotation_euler.copy()
                if "Lumi_pivot_world" in light:
                    self._original_pivots[light.name] = tuple(light["Lumi_pivot_world"])
                else:
                    self._original_pivots[light.name] = None

    def restore_original_positions(self, context):
        """Restore lights to their original positions"""
        for light in context.selected_objects:
            if light.type == 'LIGHT' and light.name in self._original_positions:
                light.location = self._original_positions[light.name]
                if light.name in self._original_rotations:
                    light.rotation_euler = self._original_rotations[light.name]
                if light.name in self._original_pivots:
                    pivot = self._original_pivots[light.name]
                    if pivot is not None:
                        light["Lumi_pivot_world"] = pivot
                    elif "Lumi_pivot_world" in light:
                        del light["Lumi_pivot_world"]

    def clear_undo_data(self):
        """Clear stored position data"""
        self._original_positions.clear()
        self._original_rotations.clear()
        self._original_pivots.clear()

    def handle_undo(self, context, event):
        """Handle undo with right mouse click"""
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            if self._original_positions:
                self.restore_original_positions(context)
                self.clear_undo_data()
                if hasattr(self, 'report'):
                    self.report({'INFO'}, "Position restored")
            return True
        return False   

    def invoke(self, context, event):
        """Base invoke method for modal operators"""
        if hasattr(self, 'bl_idname') and context.area.type == 'VIEW_3D':
            self._is_running = True
            
            # Store original positions for undo
            self.store_original_positions(context)
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            if hasattr(self, 'report'):
                self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def modal(self, context, event):
        
        if self.handle_undo(context, event):
            return {'RUNNING_MODAL'}
        
        if event.type == 'ESC':
            return self.cancel(context)
        
        return {'PASS_THROUGH'}

    def cancel(self, context):
        """Cancel the modal operator"""
        self.cleanup(context)
        return {'CANCELLED'}

    def finish(self, context):
        """Finish the modal operator successfully"""
        self.cleanup(context)
        return {'FINISHED'}
    
    def cleanup(self, context):
        """Clean up operator state"""
        self._dragging = False
        self.clear_undo_data()
    
    # Development helpers for modal tracking
    def cleanup_modal(self):
        """Clean up modal operator state for development"""
        if getattr(self, '_is_running', False):
            self._is_running = False
            cls = self.__class__
            if not hasattr(cls, '_modal_instances'):
                cls._modal_instances = set()
            if not hasattr(cls, '_running_modal'):
                cls._running_modal = False
            cls._modal_instances.discard(self)
            if not cls._modal_instances:
                cls._running_modal = False
            pass

    @classmethod
    def cleanup_all_modals(cls):
        """Force cleanup all modal instances of this class"""
        if not hasattr(cls, '_modal_instances'):
            cls._modal_instances = set()
        if not hasattr(cls, '_running_modal'):
            cls._running_modal = False

        instances_copy = cls._modal_instances.copy()
        for instance in instances_copy:
            if hasattr(instance, 'cleanup'):
                instance.cleanup(None)
        cls._running_modal = False
        cls._modal_instances.clear()

    @classmethod
    def is_modal_running(cls):
        """Check if any modal of this class is running"""
        return bool(getattr(cls, '_running_modal', False)) and len(getattr(cls, '_modal_instances', set())) > 0