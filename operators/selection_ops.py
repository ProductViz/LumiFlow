"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
# # Import modul utama Blender
import bpy
from ..utils.common import lumi_is_addon_enabled, lumi_get_light_collection 

# # Definisi class untuk Operator
class LUMI_OT_select_light(bpy.types.Operator):
    bl_idname = "lumi.select_light"
    bl_label = "Pilih Lampu"
    # # Definisi property Blender
    light_name: bpy.props.StringProperty()

    @classmethod
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        return lumi_is_addon_enabled()

    # # Method utama eksekusi operator
    def execute(self, context):
        if not lumi_is_addon_enabled():
            # # Batalkan operasi
            return {'CANCELLED'}
        # # Akses data objek Blender
        obj = bpy.data.objects.get(self.light_name)
        if not obj:
            # # Batalkan operasi
            return {'CANCELLED'}
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        mesh_name = obj.get("target_face_object")
        if mesh_name:
            # # Akses data objek Blender
            mesh_obj = bpy.data.objects.get(mesh_name)
            if mesh_obj and mesh_obj.type == 'MESH':
                context.scene.light_target = mesh_obj
       
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}

# # Definisi class untuk Operator
class LUMI_OT_delete_light(bpy.types.Operator):
    bl_idname = "lumi.delete_light"
    bl_label = "Hapus Lampu"
    # # Definisi property Blender
    light_name: bpy.props.StringProperty()

    @classmethod
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        return lumi_is_addon_enabled()

    # # Method utama eksekusi operator
    def execute(self, context):
        if not lumi_is_addon_enabled():
            # # Batalkan operasi
            return {'CANCELLED'}
        # # Akses data objek Blender
        obj = bpy.data.objects.get(self.light_name)
        if obj:
            # # Akses data objek Blender
            bpy.data.objects.remove(obj, do_unlink=True)
        # Trigger redraw area jika memungkinkan
        area = getattr(context, 'area', None)
        if area:
            area.tag_redraw()
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}


# # Definisi class untuk Operator
class LUMI_OT_delete_collection(bpy.types.Operator):
    bl_idname = "lumi.delete_collection"
    bl_label = "Delete Collection"
    bl_description = "Delete selected collection and optionally its contents"
    bl_options = {'REGISTER', 'UNDO'}

    # Property untuk konfirmasi
    confirm: bpy.props.BoolProperty(
        name="Confirm",
        description="Confirm deletion",
        default=False
    )
    
    # Property untuk menentukan apakah objek dalam collection juga dihapus
    delete_objects: bpy.props.BoolProperty(
        name="Delete Objects",
        description="Also delete objects within the collection",
        default=False
    )

    @classmethod
    # # Method untuk menentukan kapan operator/panel aktif
    def poll(cls, context):
        return lumi_is_addon_enabled() and context.collection is not None

    def invoke(self, context, event):
        # Show confirmation dialog
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        if collection:
            layout.label(text=f"Delete collection '{collection.name}'?")
            layout.prop(self, "delete_objects")
        
    # # Method utama eksekusi operator
    def execute(self, context):
        if not lumi_is_addon_enabled():
            # # Batalkan operasi
            return {'CANCELLED'}
            
        collection = context.collection
        if not collection:
            self.report({'WARNING'}, "No collection selected")
            # # Batalkan operasi
            return {'CANCELLED'}
            
        # Don't delete master collection or scene collection
        if collection.name in ["Master Collection", "Scene Collection"]:
            self.report({'WARNING'}, "Cannot delete master collection")
            # # Batalkan operasi
            return {'CANCELLED'}
            
        collection_name = collection.name
        
        try:
            # If delete_objects is True, remove all objects in collection
            if self.delete_objects:
                objects_to_remove = list(collection.objects)
                for obj in objects_to_remove:
                    # # Akses data objek Blender
                    bpy.data.objects.remove(obj, do_unlink=True)
            else:
                # Move objects to parent collection or scene collection
                parent_collection = None
                for parent in bpy.data.collections:
                    if collection in parent.children.values():
                        parent_collection = parent
                        break
                
                if not parent_collection:
                    parent_collection = context.scene.collection
                    
                # Move objects to parent collection
                objects_to_move = list(collection.objects)
                for obj in objects_to_move:
                    collection.objects.unlink(obj)
                    parent_collection.objects.link(obj)
            
            # Remove collection
            bpy.data.collections.remove(collection)
            self.report({'INFO'}, f"Deleted collection '{collection_name}'")
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to delete collection: {str(e)}")
            # # Batalkan operasi
            return {'CANCELLED'}
        
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}


# # Definisi class untuk Operator
class LUMI_OT_cycle_lights_modal(bpy.types.Operator):
    """Operator modal untuk cycling lampu dengan menekan dan menahan tombol D"""
    bl_idname = "lumi.cycle_lights_modal"
    bl_label = "Cycle Lights Modal"
    bl_description = "Hold D and scroll to cycle through lights"
    bl_options = {'REGISTER'}
    
    # # Method utama untuk modal operator
    def modal(self, context, event):
        """Fungsi modal yang menangani event saat operator aktif"""
        # Validate modal context
        if not self.validate_modal_context(context):
            # # Batalkan operasi
            return {'CANCELLED'}
        
        # Cycle lampu dengan scroll wheel sambil D ditekan
        # # Periksa jenis event (mouse, keyboard, dll)
        # Cancel modal if Ctrl, Alt, or Shift is pressed
        if event.type in {'LEFT_CTRL', 'RIGHT_CTRL', 'LEFT_ALT', 'RIGHT_ALT', 'LEFT_SHIFT', 'RIGHT_SHIFT'} and event.value == 'PRESS':
            try:
                self.cleanup_modal(context)
            except Exception:
                pass
            self.report({'INFO'}, "Light cycling cancelled (modifier pressed)")
            return {'CANCELLED'}
        # D key cycles forward
        if event.type == 'D' and event.value == 'PRESS':
            self.cycle_to_next_light(context, direction=1)
            return {'RUNNING_MODAL'}

        # Scroll wheel cycles too
        if event.type == 'WHEELUPMOUSE':
            self.cycle_to_next_light(context, direction=1)
            return {'RUNNING_MODAL'}
        elif event.type == 'WHEELDOWNMOUSE':
            self.cycle_to_next_light(context, direction=-1)
            return {'RUNNING_MODAL'}
        
        # Handle ESC sebagai jalan keluar alternatif
        # # Periksa jenis event (mouse, keyboard, dll)
        if event.type == 'ESC':
            self.cleanup_modal(context)
            self.report({'INFO'}, "Light cycling cancelled")
            # # Batalkan operasi
            return {'CANCELLED'}
        
        # Biarkan event lain lewat tanpa diganggu
        return {'PASS_THROUGH'}
    
    def validate_modal_context(self, context):
        """Validate context for modal operations"""
        if not context or not context.scene:
            self.report({'ERROR'}, "Invalid context")
            return False
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, "LumiFlow addon is not active")
            return False
        if not hasattr(context, 'area') or context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "Not in 3D View")
            return False
        return True
    
    def cleanup_modal(self, context):
        """Clean up modal state"""
        # # Coba eksekusi kode dengan error handling
        try:
            # Reset instance variables if they exist
            if hasattr(self, '_current_light_index'):
                self._current_light_index = -1
            if hasattr(self, '_lights_cache'):
                self._lights_cache = []
        # # Tangani error jika terjadi
        except Exception as e:
            print(f"Error during modal cleanup: {str(e)}")
    
    def cancel(self, context):
        """Cancel method for modal operator cleanup"""
        # # Coba eksekusi kode dengan error handling
        try:
            self.cleanup_modal(context)
        # # Tangani error jika terjadi
        except Exception as e:
            print(f"Error in cancel cleanup: {str(e)}")
        return None
    
    # # Method dipanggil saat operator dimulai
    def invoke(self, context, event):
        """Fungsi yang dipanggil saat operator dimulai"""
        
        # Initialize instance variables
        self._current_light_index = -1
        self._lights_cache = []
        
        # Validate initial context
        if not self.validate_modal_context(context):
            # # Batalkan operasi
            return {'CANCELLED'}
            
        # Initialize lights cache for better performance
        self.refresh_lights_cache(context)
        if not self._lights_cache:
            self.report({'WARNING'}, "No lights found in LumiFlow collection")
            # # Batalkan operasi
            return {'CANCELLED'}
        
        # Inisialisasi index lampu yang sedang aktif
        self._current_light_index = self.get_current_light_index(context)
        
        # Mulai modal handler
        context.window_manager.modal_handler_add(self)
        
        self.report({'INFO'}, "Light cycling active - hold D and scroll to cycle lights")
        # # Tetap jalankan modal operator
        return {'RUNNING_MODAL'}
    
    def refresh_lights_cache(self, context):
        """Refresh the cached lights list"""
        # Initialize if not exists
        if not hasattr(self, '_lights_cache'):
            self._lights_cache = []
        else:
            self._lights_cache.clear()
            
        light_collection = lumi_get_light_collection(context.scene)
        if light_collection:
            # # Periksa apakah objek adalah lampu
            lights = [obj for obj in light_collection.objects if obj.type == 'LIGHT']
            # Urutkan lampu berdasarkan nama untuk konsistensi
            self._lights_cache = sorted(lights, key=lambda x: x.name)
    
    def cycle_to_next_light(self, context, direction=1):
        """Fungsi untuk berpindah ke lampu berikutnya atau sebelumnya"""
        
        # Validate context
        if not self.validate_modal_context(context):
            return
        
        # Refresh lights if cache is empty or not exists
        if not hasattr(self, '_lights_cache') or not self._lights_cache:
            self.refresh_lights_cache(context)
        
        if not self._lights_cache:
            self.report({'WARNING'}, "No lights found in LumiFlow collection")
            return
        
        # Initialize current index if not exists
        if not hasattr(self, '_current_light_index'):
            self._current_light_index = -1
        
        # Handle solo mode cycling differently
        if is_quick_solo_active():
            # In solo mode, cycle through all lights and transfer solo status
            # Hitung index lampu berikutnya
            if self._current_light_index == -1:
                # Jika belum ada lampu terpilih, mulai dari awal atau akhir
                self._current_light_index = 0 if direction > 0 else len(self._lights_cache) - 1
            else:
                # Pindah ke index berikutnya dengan wrapping (kembali ke awal/akhir)
                self._current_light_index = (self._current_light_index + direction) % len(self._lights_cache)
            
            # Pilih lampu target
            target_light = self._lights_cache[self._current_light_index]
            
            # Validate light still exists
            if target_light.name not in bpy.data.objects:
                self.refresh_lights_cache(context)
                self.report({'WARNING'}, "Light was deleted, refreshing list")
                return
            
            # Transfer solo status to the new light and select it
            self._transfer_solo_status(context, target_light)
            
            return
        
        # Hitung index lampu berikutnya (normal mode)
        if self._current_light_index == -1:
            # Jika belum ada lampu terpilih, mulai dari awal atau akhir
            self._current_light_index = 0 if direction > 0 else len(self._lights_cache) - 1
        else:
            # Pindah ke index berikutnya dengan wrapping (kembali ke awal/akhir)
            self._current_light_index = (self._current_light_index + direction) % len(self._lights_cache)
        
        # Pilih lampu target (hanya selection, tanpa mengubah view)
        target_light = self._lights_cache[self._current_light_index]
        
        # Validate light still exists
        # # Akses data objek Blender
        if target_light.name not in bpy.data.objects:
            self.refresh_lights_cache(context)
            self.report({'WARNING'}, "Light was deleted, refreshing list")
            return
        
        # Select the light (normal mode) or transfer solo status (solo mode)
        if is_quick_solo_active():
            # Solo mode: transfer solo status to the new light
            self._transfer_solo_status(context, target_light)
        else:
            # Normal mode: just select the light
            self.select_light_only(context, target_light)
        
        # Tampilkan info di status bar
        if is_quick_solo_active():
            self.report({'INFO'}, f"Solo: {target_light.name}")
        else:
            self.report({'INFO'}, f"{target_light.name} ({self._current_light_index + 1}/{len(self._lights_cache)})")
    
    def get_current_light_index(self, context):
        """Fungsi untuk mendapatkan index lampu yang sedang dipilih saat ini"""
        
        if not hasattr(self, '_lights_cache') or not self._lights_cache:
            return -1
        
        # Cari lampu yang sedang aktif saat ini
        active_obj = context.active_object
        # # Periksa apakah objek adalah lampu
        if active_obj and active_obj.type == 'LIGHT' and active_obj in self._lights_cache:
            return self._lights_cache.index(active_obj)
        
        # Return -1 jika tidak ada lampu yang dipilih
        return -1
    
    def _transfer_solo_status(self, context, new_solo_light):
        """Transfer solo status from current solo light to new solo light"""
        global _QUICK_SOLO_STATE, _QUICK_SOLO_ACTIVE
        
        if not _QUICK_SOLO_ACTIVE:
            return
        
        light_collection = lumi_get_light_collection(context.scene)
        if not light_collection:
            return
        
        # Hide all lights except the new solo light
        for obj in light_collection.objects:
            if obj.type == 'LIGHT':
                if obj == new_solo_light:
                    # Make new solo light visible
                    obj.hide_viewport = False
                    obj.hide_render = False
                else:
                    # Hide all other lights
                    obj.hide_viewport = True
                    obj.hide_render = True
        
        # Select and activate the new solo light
        self.select_light_only(context, new_solo_light)
    
    def select_light_only(self, context, light_obj):
        """Fungsi untuk memilih lampu tanpa mengubah view kamera"""
        # # Coba eksekusi kode dengan error handling
        try:
            # Batalkan semua seleksi yang ada
            bpy.ops.object.select_all(action='DESELECT')
            
            # Pilih dan aktifkan lampu target (tanpa view changes)
            light_obj.select_set(True)
            context.view_layer.objects.active = light_obj
            
            # Force viewport update
            if context.area:
                context.area.tag_redraw()
                
        # # Tangani error jika terjadi
        except Exception as e:
            self.report({'WARNING'}, f"Failed to select light: {str(e)}")
            print(f"Light selection error: {str(e)}")


# # Global state untuk Quick Solo Light
_QUICK_SOLO_STATE = {}
_QUICK_SOLO_ACTIVE = False


# # Definisi class untuk Operator Quick Solo Light
class LUMI_OT_quick_solo_light(bpy.types.Operator):
    """Operator untuk mengaktifkan/menonaktifkan solo mode untuk lampu yang dipilih"""
    bl_idname = "lumi.quick_solo_light"
    bl_label = "Quick Solo Light"
    bl_description = "Toggle solo mode for selected light (Ctrl+Shift+D)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Periksa apakah operator dapat dijalankan"""
        # Pastikan addon aktif dan ada lampu yang dipilih
        if not lumi_is_addon_enabled():
            return False

        # Periksa apakah ada objek aktif yang merupakan lampu
        active_obj = context.active_object
        return active_obj and active_obj.type == 'LIGHT'

    def execute(self, context):
        """Method utama eksekusi operator"""
        global _QUICK_SOLO_STATE, _QUICK_SOLO_ACTIVE

        try:
            active_light = context.active_object

            if not active_light or active_light.type != 'LIGHT':
                self.report({'WARNING'}, "No light selected")
                return {'CANCELLED'}

            # Toggle solo mode using global state
            if _QUICK_SOLO_ACTIVE:
                self.disable_solo_mode(context)
                self.report({'INFO'}, f"Solo mode disabled")
            else:
                self.enable_solo_mode(context, active_light)
                self.report({'INFO'}, f"Solo: {active_light.name}")

            # Force viewport update
            if context.area:
                context.area.tag_redraw()

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Solo operation failed: {str(e)}")
            return {'CANCELLED'}

    def enable_solo_mode(self, context, solo_light):
        """Aktifkan solo mode untuk lampu yang dipilih"""
        global _QUICK_SOLO_STATE, _QUICK_SOLO_ACTIVE

        # Simpan state semua lampu sebelum solo
        _QUICK_SOLO_STATE.clear()
        light_collection = lumi_get_light_collection(context.scene)

        if not light_collection:
            self.report({'WARNING'}, "LumiFlow light collection not found")
            return

        # Simpan visibility state semua lampu dan hide semua kecuali yang di-solo
        for obj in light_collection.objects:
            if obj.type == 'LIGHT':
                # Simpan state asli
                _QUICK_SOLO_STATE[obj.name] = {
                    'hide_viewport': obj.hide_viewport,
                    'hide_render': obj.hide_render
                }

                # Hide semua lampu kecuali yang di-solo
                if obj != solo_light:
                    obj.hide_viewport = True
                    obj.hide_render = True
                else:
                    # Pastikan solo light visible
                    obj.hide_viewport = False
                    obj.hide_render = False

        _QUICK_SOLO_ACTIVE = True

    def disable_solo_mode(self, context):
        """Nonaktifkan solo mode dan restore semua lampu"""
        global _QUICK_SOLO_STATE, _QUICK_SOLO_ACTIVE

        light_collection = lumi_get_light_collection(context.scene)

        if not light_collection:
            return

        # Restore state semua lampu
        for obj in light_collection.objects:
            if obj.type == 'LIGHT' and obj.name in _QUICK_SOLO_STATE:
                state = _QUICK_SOLO_STATE[obj.name]
                obj.hide_viewport = state['hide_viewport']
                obj.hide_render = state['hide_render']

        _QUICK_SOLO_STATE.clear()
        _QUICK_SOLO_ACTIVE = False

    @classmethod
    def is_solo_active(cls):
        """Periksa apakah solo mode sedang aktif"""
        global _QUICK_SOLO_ACTIVE
        return _QUICK_SOLO_ACTIVE

    @classmethod
    def get_solo_light_name(cls):
        """Dapatkan nama lampu yang sedang di-solo"""
        global _QUICK_SOLO_ACTIVE
        if _QUICK_SOLO_ACTIVE:
            # Cari lampu yang tidak di-hide
            light_collection = lumi_get_light_collection(bpy.context.scene)
            if light_collection:
                for obj in light_collection.objects:
                    if obj.type == 'LIGHT' and not obj.hide_viewport:
                        return obj.name
        return None


def cleanup_quick_solo_state():
    """Cleanup function untuk reset Quick Solo state saat unregister"""
    global _QUICK_SOLO_STATE, _QUICK_SOLO_ACTIVE
    _QUICK_SOLO_STATE.clear()
    _QUICK_SOLO_ACTIVE = False


def is_quick_solo_active():
    """Helper function to check if Quick Solo mode is active"""
    global _QUICK_SOLO_ACTIVE
    return _QUICK_SOLO_ACTIVE


def get_quick_solo_light_name():
    """Helper function to get the name of currently solo light"""
    global _QUICK_SOLO_ACTIVE
    if _QUICK_SOLO_ACTIVE:
        light_collection = lumi_get_light_collection(bpy.context.scene)
        if light_collection:
            for obj in light_collection.objects:
                if obj.type == 'LIGHT' and not obj.hide_viewport:
                    return obj.name
    return None


def cleanup_camera_light_state():
    """Cleanup function untuk reset Camera Light state saat unregister"""
    try:
        # Import and cleanup directly without global variable manipulation
        from ..core.camera_manager import CameraLightManager
        
        # Create a temporary manager for cleanup
        temp_manager = CameraLightManager()
        temp_manager.cleanup_system(bpy.context)
        
        # Reset the global instance by directly accessing the module
        import sys
        if 'LumiFlow.core.camera_manager' in sys.modules:
            module = sys.modules['LumiFlow.core.camera_manager']
            if hasattr(module, '_camera_light_manager_instance'):
                module._camera_light_manager_instance = None
    except Exception:
        pass
