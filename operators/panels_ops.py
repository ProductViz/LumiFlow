import bpy
from ..utils.common import lumi_is_addon_enabled

class LUMI_OT_toggle_overlay_info(bpy.types.Operator):
    bl_idname = "lumi.toggle_overlay_info"
    bl_label = "Toggle Overlay Info"
    bl_description = "Toggle light info overlay visibility (D)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        scene.lumi_show_overlay_info = not scene.lumi_show_overlay_info
        return {'FINISHED'}

class LUMI_OT_toggle_overlay_tips(bpy.types.Operator):
    """Toggle overlay tips visibility"""
    bl_idname = "lumi.toggle_overlay_tips"
    bl_label = "Toggle Overlay Tips"
    bl_description = "Toggle tips overlay visibility (T)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        scene.lumi_show_overlay_tips = not scene.lumi_show_overlay_tips
        return {'FINISHED'}

class LUMI_OT_toggle_addon(bpy.types.Operator):
    """Toggle LumiFlow addon on/off"""
    bl_idname = "lumi.toggle_addon"
    bl_label = "Toggle LumiFlow Addon"
    bl_description = "Toggle LumiFlow addon on/off (D)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        scene.lumi_enabled = not scene.lumi_enabled
        status = "ENABLED" if scene.lumi_enabled else "DISABLED"
        self.report({'INFO'}, f"LumiFlow {status}")
        return {'FINISHED'}
