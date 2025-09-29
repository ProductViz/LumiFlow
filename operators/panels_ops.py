
import bpy
from ..utils.common import lumi_is_addon_enabled

# # Definisi class untuk Operator
class LUMI_OT_toggle_overlay_info(bpy.types.Operator):
    """Operator untuk mengaktifkan/menonaktifkan overlay info lampu"""
    bl_idname = "lumi.toggle_overlay_info"
    bl_label = "Toggle Overlay Info"
    bl_description = "Toggle light info overlay visibility (D)"
    bl_options = {'REGISTER'}

    # # Method utama eksekusi operator
    def execute(self, context):
        scene = context.scene
        scene.lumi_show_overlay_info = not scene.lumi_show_overlay_info
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}

# # Definisi class untuk Operator
class LUMI_OT_toggle_overlay_tips(bpy.types.Operator):
    """Operator untuk mengaktifkan/menonaktifkan overlay tips"""
    bl_idname = "lumi.toggle_overlay_tips"
    bl_label = "Toggle Overlay Tips"
    bl_description = "Toggle tips overlay visibility (T)"
    bl_options = {'REGISTER'}

    # # Method utama eksekusi operator
    def execute(self, context):
        scene = context.scene
        scene.lumi_show_overlay_tips = not scene.lumi_show_overlay_tips
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}

# # Definisi class untuk Operator
class LUMI_OT_toggle_addon(bpy.types.Operator):
    """Operator untuk mengaktifkan/menonaktifkan addon LumiFlow"""
    bl_idname = "lumi.toggle_addon"
    bl_label = "Toggle LumiFlow Addon"
    bl_description = "Toggle LumiFlow addon on/off (D)"
    bl_options = {'REGISTER'}

    # # Method utama eksekusi operator
    def execute(self, context):
        scene = context.scene
        scene.lumi_enabled = not scene.lumi_enabled
        status = "ENABLED" if scene.lumi_enabled else "DISABLED"
        self.report({'INFO'}, f"LumiFlow {status}")
        # # Selesaikan operasi dengan sukses
        return {'FINISHED'}




