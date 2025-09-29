import bpy

class BaseModalOperator:
    """Base class untuk modal operator dengan fungsionalitas bersama"""
    
    # Variabel untuk fungsionalitas modal inti
    _dragging = False
    _original_positions = {}
    _original_rotations = {}
    _original_pivots = {}

    def __init__(self):
        # Inisialisasi status running modal
        self._is_running = False

    def store_original_positions(self, context):
        """Simpan posisi asli untuk fungsi undo"""
        # Bersihkan data posisi sebelumnya
        self._original_positions.clear()
        self._original_rotations.clear()
        self._original_pivots.clear()
        
        # Simpan posisi, rotasi, dan pivot untuk setiap lampu yang dipilih
        # # Ambil objek yang dipilih dalam scene
        for light in context.selected_objects:
            if light.type == 'LIGHT':
                # Simpan posisi asli
                self._original_positions[light.name] = light.location.copy()
                # Simpan rotasi asli
                self._original_rotations[light.name] = light.rotation_euler.copy()
                # Simpan pivot asli jika ada
                if "Lumi_pivot_world" in light:
                    self._original_pivots[light.name] = tuple(light["Lumi_pivot_world"])
                else:
                    self._original_pivots[light.name] = None

    def restore_original_positions(self, context):
        """Kembalikan lampu ke posisi aslinya"""
        # Iterasi semua lampu yang dipilih
        # # Ambil objek yang dipilih dalam scene
        for light in context.selected_objects:
            if light.type == 'LIGHT' and light.name in self._original_positions:
                # Kembalikan posisi asli
                light.location = self._original_positions[light.name]
                # Kembalikan rotasi asli jika ada
                if light.name in self._original_rotations:
                    light.rotation_euler = self._original_rotations[light.name]
                # Kembalikan pivot asli jika ada
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
        # # Periksa jenis event (mouse, keyboard, dll)
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            if self._original_positions:
                self.restore_original_positions(context)
                self.clear_undo_data()
                if hasattr(self, 'report'):
                    self.report({'INFO'}, "Position restored")
            return True
        return False   

    # # Method dipanggil saat operator dimulai
    def invoke(self, context, event):
        """Base invoke method for modal operators"""
        if hasattr(self, 'bl_idname') and context.area.type == 'VIEW_3D':
            self._is_running = True
            
            # Store original positions for undo
            self.store_original_positions(context)
            
            # Add modal handler
            context.window_manager.modal_handler_add(self)
            # # Tetap jalankan modal operator
            return {'RUNNING_MODAL'}
        else:
            if hasattr(self, 'report'):
                self.report({'WARNING'}, "View3D not found, cannot run operator")
            # # Batalkan operasi
            return {'CANCELLED'}

    # # Method utama untuk modal operator
    def modal(self, context, event):
        """Base modal method - override this in subclasses"""
        
        # Handle undo first
        if self.handle_undo(context, event):
            # # Tetap jalankan modal operator
            return {'RUNNING_MODAL'}
        
        # ESC to cancel
        # # Periksa jenis event (mouse, keyboard, dll)
        if event.type == 'ESC':
            return self.cancel(context)
        
        # Pass through by default
        return {'PASS_THROUGH'}

    def cancel(self, context):
        """Cancel the modal operator"""
        self.cleanup(context)
        # # Batalkan operasi
        return {'CANCELLED'}

    def finish(self, context):
        """Finish the modal operator successfully"""
        self.cleanup(context)
        # # Selesaikan operasi dengan sukses
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
            # Ensure tracking attributes exist
            if not hasattr(cls, '_modal_instances'):
                cls._modal_instances = set()
            if not hasattr(cls, '_running_modal'):
                cls._running_modal = False
            cls._modal_instances.discard(self)
            # Update class tracking
            if not cls._modal_instances:
                cls._running_modal = False
            pass

    @classmethod
    def cleanup_all_modals(cls):
        """Force cleanup all modal instances of this class"""
        # Ensure tracking attributes exist
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