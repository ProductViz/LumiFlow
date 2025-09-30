# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Template Operators
Operators for template management and browser functionality.
"""

import bpy
from bpy.props import StringProperty

class LUMI_OT_toggle_template_favorite(bpy.types.Operator):
    """Toggle template favorite status"""
    bl_idname = "lumi.toggle_template_favorite"
    bl_label = "Toggle Template Favorite"
    bl_description = "Add/remove template from favorites"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    template_id: StringProperty(
        name="Template ID",
        description="Template to toggle favorite",
        default="",
        options={'SKIP_SAVE'}
    )
    
    def execute(self, context):
        if not self.template_id:
            self.report({'ERROR'}, "No template ID provided")
            return {'CANCELLED'}
            
        scene = context.scene
        favorites = getattr(scene, 'lumi_template_favorites', '')
        
        if favorites.strip():
            fav_list = [f.strip() for f in favorites.split(',') if f.strip()]
        else:
            fav_list = []
        
        if self.template_id in fav_list:
            fav_list.remove(self.template_id)
            self.report({'INFO'}, f"Removed '{self.template_id}' from favorites")
        else:
            fav_list.append(self.template_id)
            self.report({'INFO'}, f"Added '{self.template_id}' to favorites")
        
        scene.lumi_template_favorites = ','.join(fav_list)
        
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'UI':
                        region.tag_redraw()
                        
        return {'FINISHED'}


class LUMI_OT_set_template_category(bpy.types.Operator):
    """Set template category filter"""
    bl_idname = "lumi.set_template_category"
    bl_label = "Set Template Category"
    bl_description = "Filter templates by category"
    bl_options = {'REGISTER'}
    
    category: StringProperty(
        name="Category",
        description="Template category to filter",
        default="ALL"
    )
    
    def execute(self, context):
        context.scene.lumi_template_category = self.category
        return {'FINISHED'}


class LUMI_OT_save_lighting_template(bpy.types.Operator):
    """Save current lighting setup as template"""
    bl_idname = "lumi.save_lighting_template"
    bl_label = "Save Current as Template"
    bl_description = "Save current lighting setup as new template"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Template saving not yet implemented")
        return {'FINISHED'}


class LUMI_OT_apply_template_direct(bpy.types.Operator):
    """Apply template directly without dialog"""
    bl_idname = "lumi.apply_template_direct"
    bl_label = "Apply Template Direct"
    bl_description = "Apply lighting template directly without dialog"
    bl_options = {'REGISTER', 'UNDO'}
    
    template_id: StringProperty(
        name="Template ID",
        description="Template to apply",
        default=""
    )
    
    auto_scale: bpy.props.BoolProperty(
        name="Auto Scale",
        description="Automatically scale lights to subject size",
        default=True
    )

    intensity_multiplier: bpy.props.FloatProperty(
        name="Intensity Multiplier",
        description="Global intensity multiplier for all lights",
        default=1.0,
        min=0.1,
        max=10.0
    )

    size_multiplier: bpy.props.FloatProperty(
        name="Size Multiplier", 
        description="Global size multiplier for area lights",
        default=1.0,
        min=0.1,
        max=5.0
    )

    use_camera_relative: bpy.props.BoolProperty(
        name="Camera Relative",
        description="Position lights relative to camera view",
        default=True
    )

    preserve_existing: bpy.props.BoolProperty(
        name="Preserve Existing Lights",
        description="Keep existing lights in scene. If unchecked, removes lights based on current assignment mode: SCENE mode removes G_* lights, CAMERA mode removes C_XX_* lights for active camera",
        default=False
    )

    manual_distance: bpy.props.FloatProperty(
        name="Manual Distance",
        description="Override automatic distance calculation",
        default=0.0,
        min=0.0,
        max=50.0
    )

    use_material_adaptation: bpy.props.BoolProperty(
        name="Material Adaptation",
        description="Adjust lighting based on material analysis",
        default=True
    )
    
    def execute(self, context):
        """Execute template application directly"""
        result = bpy.ops.lumi.apply_lighting_template(
            'EXEC_DEFAULT',
            template_id=self.template_id,
            auto_scale=self.auto_scale,
            intensity_multiplier=self.intensity_multiplier,
            size_multiplier=self.size_multiplier,
            use_camera_relative=self.use_camera_relative,
            preserve_existing=self.preserve_existing,
            manual_distance=self.manual_distance,
            use_material_adaptation=self.use_material_adaptation
        )
        
        return result


class LUMI_OT_apply_template_default(bpy.types.Operator):
    """Apply template using addon default parameters (no user properties)"""
    bl_idname = "lumi.apply_template_default"
    bl_label = "Apply Template (Default)"
    bl_description = "Apply lighting template using default parameters"
    bl_options = {'REGISTER', 'UNDO'}

    template_id: StringProperty(
        name="Template ID",
        description="Template to apply",
        default=""
    )

    def execute(self, context):
        result = bpy.ops.lumi.apply_lighting_template(
            'EXEC_DEFAULT',
            template_id=self.template_id,
            auto_scale=True,
            intensity_multiplier=1.0,
            size_multiplier=1.0,
            use_camera_relative=True,
            preserve_existing=True
        )
        return result


class LUMI_OT_apply_template(bpy.types.Operator):
    """Apply template operator"""
    bl_idname = "lumi.apply_template"
    bl_label = "Apply Template"
    bl_description = "Apply lighting template"
    bl_options = {'REGISTER', 'UNDO'}
    
    template_id: StringProperty(
        name="Template ID",
        description="Template to apply",
        default=""
    )
    
    def execute(self, context):
        result = bpy.ops.lumi.apply_lighting_template(
            'EXEC_DEFAULT',
            template_id=self.template_id
        )
        return result


class LUMI_OT_show_all_templates(bpy.types.Operator):
    """Show all templates operator"""
    bl_idname = "lumi.show_all_templates"
    bl_label = "Show All Templates"
    bl_description = "Open full template browser in popup"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
        
    def draw(self, context):
        """Draw full template browser popup"""
        layout = self.layout
        scene = context.scene
        
        header = layout.row()
        header.label(text=" All Lighting Templates", icon='LIGHT')
        
        try:
            from .smart_template.template_library import BUILTIN_TEMPLATES
            
            category_filter = getattr(scene, 'lumi_template_category', 'ALL')
            
            if category_filter == 'ALL':
                template_ids = sorted(BUILTIN_TEMPLATES.keys())
                templates = [BUILTIN_TEMPLATES[tid] for tid in template_ids]
            else:
                templates = []
                for template_id, template in sorted(BUILTIN_TEMPLATES.items()):
                    if template.get('category', '').lower() == category_filter.lower():
                        templates.append(template)
                    
            if templates:
                self._draw_list_view(layout, templates, context)
            else:
                layout.label(text="No templates found", icon='INFO')
                
        except Exception as e:
            layout.label(text="Error loading templates", icon='ERROR')
            layout.label(text=str(e)[:50] + "...")   
    
    
    def _draw_list_view(self, layout, templates, context):
        """Draw templates in list layout grouped by category"""
        scene = context.scene
        favorites_str = getattr(scene, 'lumi_template_favorites', '')
        favorites = [f.strip() for f in favorites_str.split(',') if f.strip()]
        
        categories = {}
        for i, template in enumerate(templates):
            template_id = template.get('id', f'template_{i}')
            if not template_id or template_id == 'unknown':
                template_id = f'template_{i}'
            
            category = template.get('category', 'other').title()
            if category not in categories:
                categories[category] = []
            categories[category].append((template_id, template))
        
        for category_name in sorted(categories.keys()):
            category_templates = categories[category_name]
            
            header_row = layout.row()
            header_row.label(text=category_name)
            col = layout.column(align=True)
            
            for template_id, template in category_templates:
                template_name = template.get('name', template_id.replace('_', ' ').title())
                light_count = len(template.get('lights', []))
                
                row = col.row(align=True)
                
                row.label(text="ðŸ’¡", icon='NONE')
                
                name_col = row.column()
                name_col.scale_x = 2.0
                name_col.label(text=template_name)
                
                count_col = row.column()
                count_col.scale_x = 0.5
                count_col.label(text=f"{light_count}L")
                
                is_favorite = template_id in favorites
                star_icon = 'SOLO_ON' if is_favorite else 'SOLO_OFF'
                star_op = row.operator("lumi.toggle_template_favorite", text="", icon=star_icon)
                star_op.template_id = template_id
                
                if context.selected_objects:
                    apply_op = row.operator("lumi.apply_lighting_template", text="Apply")
                    apply_op.template_id = template_id
    

__all__ = [
    'LUMI_OT_toggle_template_favorite',
    'LUMI_OT_set_template_category', 
    'LUMI_OT_save_lighting_template',
    'LUMI_OT_apply_template_direct',
    'LUMI_OT_apply_template_default',
    'LUMI_OT_apply_template',
    'LUMI_OT_show_all_templates'
]

