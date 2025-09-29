bl_info = {
    "name": "LumiFlow",
    "author": "Burhanuddin",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > LumiFlow",
    "description": "Smart lighting tools for Blender",
    "category": "Lighting",
}

import bpy
import importlib
import sys

# Import modules
from . import base_modal
from . import registration

# Development mode - reload modules when script reloads
if "bpy" in locals():
    try:
        # Get addon name for finding all related modules
        addon_name = __name__.split('.')[0]
        
        # Reload all addon modules with error handling
        modules_to_reload = []
        for name, module in sys.modules.items():
            if name.startswith(addon_name + '.') and name != __name__:
                modules_to_reload.append((name, module))
        
        # Sort modules to reload dependencies first (deeper modules first)
        modules_to_reload.sort(key=lambda x: x[0].count('.'), reverse=True)
        
        for name, module in modules_to_reload:
            try:
                importlib.reload(module)
            except ImportError:
                # Continue with other modules
                pass
            except Exception:
                pass
        
        # Reload base modules after others
        try:
            importlib.reload(base_modal)
        except Exception:
            pass
        
        try:
            importlib.reload(registration)
        except Exception:
            pass
            
    except Exception:
        pass

# Import BaseModalOperator to make it available for other modules
from .base_modal import BaseModalOperator

def register():
    """Register LumiFlow addon with error handling"""
    try:
        registration.register()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise  # Re-raise to ensure Blender knows registration failed

def unregister():
    """Unregister LumiFlow addon with error handling"""
    try:
        registration.unregister()
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Don't re-raise during unregister to avoid Blender issues

# Development helper operators
class LUMIFLOW_OT_reload_addon(bpy.types.Operator):
    """Reload LumiFlow addon for development"""
    bl_idname = "lumiflow.reload_addon"
    bl_label = "Reload LumiFlow"
    bl_description = "Reload the LumiFlow addon (development only)"
    
    def execute(self, context):
        try:
            # Check for running modal operators first
            running_modals = self.get_running_modal_operators()
            if running_modals:
                self.report({'WARNING'}, f"Stop running modal operators first: {', '.join(running_modals)}")
                return {'CANCELLED'}
            
            # Unregister current addon
            unregister()
            
            # Reload scripts
            bpy.ops.script.reload()
            
            # Re-register addon
            register()
            
            self.report({'INFO'}, "LumiFlow reloaded successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to reload: {e}")
            return {'CANCELLED'}
    
    def get_running_modal_operators(self):
        """Check for running modal operators from this addon"""
        running = []
        addon_name = __name__.split('.')[0].upper()
        
        # Check window manager for modal handlers
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if hasattr(area, 'spaces'):
                    for space in area.spaces:
                        # Check if any modal operators are running
                        # This is a simplified check - you might need to adapt based on your specific operators
                        pass
        
        # Alternative: Check for specific operator classes
        for attr_name in dir(bpy.types):
            if attr_name.startswith(addon_name) and 'OT_' in attr_name:
                try:
                    op_class = getattr(bpy.types, attr_name)
                    if hasattr(op_class, '_running_modal') and op_class._running_modal:
                        running.append(attr_name)
                except:
                    pass
        
        return running

class LUMIFLOW_OT_stop_all_modals(bpy.types.Operator):
    """Stop all running LumiFlow modal operators"""
    bl_idname = "lumiflow.stop_all_modals"
    bl_label = "Stop All LumiFlow Modals"
    bl_description = "Force stop all running modal operators from LumiFlow"
    
    def execute(self, context):
        try:
            stopped_count = 0
            addon_name = __name__.split('.')[0].upper()
            
            # Force cleanup using BaseModalOperator
            from .base_modal import BaseModalOperator
            
            # Get all registered operator classes that inherit from BaseModalOperator
            for attr_name in dir(bpy.types):
                if attr_name.startswith(addon_name) and 'OT_' in attr_name:
                    try:
                        op_class = getattr(bpy.types, attr_name)
                        # Check if it's likely a modal operator class
                        if (hasattr(op_class, '_modal_instances') or 
                            hasattr(op_class, '_running_modal')):
                            # Force cleanup
                            if hasattr(op_class, 'cleanup_all_modals'):
                                op_class.cleanup_all_modals()
                                stopped_count += 1
                            elif hasattr(op_class, '_modal_instances'):
                                # Manual cleanup
                                instances = getattr(op_class, '_modal_instances', set()).copy()
                                for instance in instances:
                                    if hasattr(instance, 'cleanup'):
                                        instance.cleanup(context)
                                op_class._modal_instances.clear()
                                op_class._running_modal = False
                                stopped_count += 1
                    except Exception as e:
                        print(f"Error stopping modal {attr_name}: {e}")
            
            # Also try to send ESC events to cancel any remaining modals
            self.send_escape_events(context)
            
            self.report({'INFO'}, f"Attempted to stop {stopped_count} modal operator classes")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to stop modals: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def send_escape_events(self, context):
        """Send ESC events to try canceling remaining modals"""
        try:
            # This is a fallback method - send ESC key events
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        # Override context and try to send escape
                        with context.temp_override(window=window, area=area):
                            try:
                                # Create a fake ESC event to trigger modal cancellation
                                # This is hacky but sometimes necessary
                                pass  # We'll rely on the cleanup methods above
                            except:
                                pass
        except Exception as e:
            print(f"Error sending escape events: {e}")

class LUMIFLOW_OT_dev_panel(bpy.types.Panel):
    """Development panel for LumiFlow"""
    bl_label = "LumiFlow Dev"
    bl_idname = "LUMIFLOW_PT_dev_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LumiFlow"
    bl_order = 999  # Put at bottom
    
    @classmethod
    def poll(cls, context):
        # Only show in development (when Developer Extras is enabled)
        return context.preferences.view.show_developer_ui
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="Development Tools:", icon='TOOL_SETTINGS')
        col.operator("lumiflow.stop_all_modals", icon='X')
        col.operator("lumiflow.reload_addon", icon='FILE_REFRESH')

# Register development operators only in development
def register_dev_operators():
    """Register development-only operators"""
    dev_classes = [
        LUMIFLOW_OT_reload_addon,
        LUMIFLOW_OT_stop_all_modals,
        LUMIFLOW_OT_dev_panel
    ]
    
    for cls in dev_classes:
        if not hasattr(bpy.types, cls.bl_idname.replace('.', '_').upper()):
            try:
                bpy.utils.register_class(cls)
            except Exception as e:
                print(f"Failed to register dev class {cls}: {e}")

def unregister_dev_operators():
    """Unregister development operators"""
    dev_classes = [
        LUMIFLOW_OT_reload_addon,
        LUMIFLOW_OT_stop_all_modals,
        LUMIFLOW_OT_dev_panel
    ]
    
    for cls in reversed(dev_classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister dev class {cls}: {e}")

if __name__ == "__main__":
    register()
    register_dev_operators()
else:
    # Only register dev operators in development mode
    register_dev_operators()