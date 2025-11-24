# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Menu Operations
Operators for menu functionality including smart light operations and template management.
"""
import bpy
from mathutils import Vector
from ..utils.common import lumi_is_addon_enabled
from ..utils.operators import lumi_raycast_at_mouse
from ..utils.color import lumi_apply_kelvin_to_lights
from ..core.assign_manager import assign_light_to_active_camera

# Import advanced subject detection for AI analysis
from .smart_template.template_analyzer import analyze_subject, AdvancedSubjectClassifier


def safe_ui_label(layout, text, icon='NONE'):
    """Safely add a label to layout, ensuring text is always a string"""
    try:
        if text is None:
            safe_text = ""
        else:
                safe_text = str(text).strip()

        if len(safe_text) > 120:
            safe_text = safe_text[:117] + "..."

        safe_text = safe_text.replace('\n', ' ').replace('\r', ' ')
        if not safe_text:
            safe_text = "N/A"

        safe_icons = {
            'NONE', 'INFO', 'ERROR', 'LIGHT', 'CHECKMARK', 'REMOVE', 'X',
            'LIGHT_SUN', 'LIGHT_DATA', 'SOLO_ON', 'PLUS', 'PREFERENCES',
            'FILE_REFRESH', 'ZOOM_SELECTED', 'ZOOM_ALL', 'MODIFIER_DATA'
        }

        safe_icon = str(icon) if icon else 'NONE'
        if safe_icon not in safe_icons:
            safe_icon = 'INFO'

        if safe_icon and safe_icon != 'NONE':
            layout.label(text=safe_text, icon=safe_icon)
        else:
            layout.label(text=safe_text)

    except Exception as e:
        pass
        return

class LUMI_OT_smart_light_pie_call(bpy.types.Operator):
    bl_idname = "lumi.smart_light_pie_call"
    bl_label = "Smart Light Pie Menu"
    bl_description = "Open Smart Light Pie Menu with shortcut (Ctrl+Shift+A)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        mouse_pos = (event.mouse_region_x, event.mouse_region_y)
        hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, mouse_pos)
        if not hit_obj or hit_obj.type != 'MESH':
            self.report({'WARNING'}, 'Point mouse to mesh object to add light!')
            return {'CANCELLED'}

        scene = context.scene
        scene.lumi_temp_hit_obj = hit_obj
        scene.lumi_temp_hit_location = tuple(hit_location)
        scene.lumi_temp_hit_normal = tuple(hit_normal)
        scene.lumi_temp_hit_index = hit_index

        bpy.ops.wm.call_menu(name="LUMI_MT_add_light_pie")
        return {'FINISHED'}

    def execute(self, context):
        return self.invoke(context, None)

class LUMI_OT_add_smart_light(bpy.types.Operator):
    bl_idname = "lumi.add_smart_light"
    bl_label = "Add Smart Light"
    bl_description = "Add light with automatic positioning on object surface"
    bl_options = {'REGISTER', 'UNDO'}

    light_type : bpy.props.StringProperty()
    mouse_position : bpy.props.IntVectorProperty(size=2)
    use_stored_target : bpy.props.BoolProperty(default=False)
    use_raycast_target : bpy.props.BoolProperty(default=False)
    setup_type : bpy.props.StringProperty(default="")
    area_shape : bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}
        
        scene = context.scene

        # If operator is configured to use stored target but no valid data exists,
        # fall back to raycast from current mouse position (for keymap usage).
        if self.use_stored_target:
            hit_obj = getattr(scene, 'lumi_temp_hit_obj', None)
            hit_location = getattr(scene, 'lumi_temp_hit_location', None)
            hit_normal = getattr(scene, 'lumi_temp_hit_normal', None)
            if hit_obj is None or hit_location is None or hit_normal is None:
                self.use_stored_target = False

        if not self.use_stored_target and event:
            self.mouse_position = (event.mouse_region_x, event.mouse_region_y)

        return self.execute(context)

    def execute(self, context):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        scene = context.scene

        if self.use_stored_target:
            hit_obj = getattr(scene, 'lumi_temp_hit_obj', None)
            hit_location = getattr(scene, 'lumi_temp_hit_location', None)
            hit_normal = getattr(scene, 'lumi_temp_hit_normal', None)
            hit_index = getattr(scene, 'lumi_temp_hit_index', None)
            if hit_obj is None or hit_location is None or hit_normal is None:
                self.report({'ERROR'}, 'Target data not found!')
                return {'CANCELLED'}
            hit_location = Vector(hit_location)
            hit_normal = Vector(hit_normal)
            self.clear_temp_data(scene)
        else:
            hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, self.mouse_position)
            if not hit_obj or hit_obj.type != 'MESH':
                self.report({'WARNING'}, 'Point mouse to mesh object to add light!')
                return {'CANCELLED'}

        from ..utils.light import create_smart_light
        from ..utils.smart_calc import get_smart_light_parameters
        light_type_str = str(self.light_type)
        light_obj = create_smart_light(context, light_type_str, hit_location, hit_normal, hit_obj)
        
        if self.area_shape and light_obj and light_obj.data.type == 'AREA':
            area_shape_str = str(self.area_shape).upper()
            
            # Get smart parameters to preserve calculated scale values
            smart_params = get_smart_light_parameters(context, hit_obj, hit_location, hit_normal, light_type_str)
            scale_params = smart_params['scale']
            calculated_size = scale_params.get('size', 1.0)
            calculated_size_y = scale_params.get('size_y', 1.2)
            
            if area_shape_str == "SQUARE":
                light_obj.data.shape = 'SQUARE'
                light_obj.data.size = calculated_size
            elif area_shape_str == "RECTANGLE":
                light_obj.data.shape = 'RECTANGLE'
                light_obj.data.size = calculated_size
                light_obj.data.size_y = calculated_size_y
            elif area_shape_str == "DISK":
                light_obj.data.shape = 'DISK'
                light_obj.data.size = calculated_size
            elif area_shape_str == "ELLIPSE":
                light_obj.data.shape = 'ELLIPSE'
                light_obj.data.size = calculated_size
                light_obj.data.size_y = calculated_size_y
            
            shape_names = {
                "SQUARE": "Square",
                "RECTANGLE": "Rectangle", 
                "DISK": "Disk",
                "ELLIPSE": "Ellipse"
            }
            shape_name = shape_names.get(area_shape_str, area_shape_str)
            light_obj.name = f"{shape_name} Area Light"
            light_obj.data.name = f"{shape_name} Area Data"
        
        assign_light_to_active_camera(light_obj)

        # Apply light linking EXCLUDE to all objects marked as exclude quick add
        try:
            scene_ll = scene

            # Kumpulkan semua mesh dengan flag exclude
            exclude_targets = [obj for obj in scene_ll.objects
                              if obj.type == 'MESH' and bool(getattr(obj, 'lumi_exclude_quick_add', False))]

            if light_obj and light_obj.type == 'LIGHT' and exclude_targets:
                linked = False

                # 1) Coba pakai API scene.light_linking jika tersedia (Blender 4.x)
                if hasattr(scene_ll, 'light_linking') and scene_ll.light_linking:
                    try:
                        for obj in exclude_targets:
                            try:
                                scene_ll.light_linking.link_new(light_obj, obj, 'EXCLUDE')
                            except Exception:
                                # Jika satu objek gagal, lanjut ke yang lain
                                pass
                        linked = True
                    except Exception:
                        linked = False

                # 2) Fallback: gunakan operator light_linking_receivers_link (Blender 3.6)
                if not linked:
                    try:
                        import bpy

                        original_selection = list(context.selected_objects)
                        original_active = context.view_layer.objects.active

                        bpy.ops.object.select_all(action='DESELECT')
                        light_obj.select_set(True)
                        context.view_layer.objects.active = light_obj

                        for obj in exclude_targets:
                            try:
                                obj.select_set(True)
                            except Exception:
                                pass

                        if hasattr(bpy.ops.object, 'light_linking_receivers_link'):
                            try:
                                bpy.ops.object.light_linking_receivers_link(link_state='EXCLUDE')
                            except Exception:
                                pass

                        # Kembalikan seleksi awal
                        bpy.ops.object.select_all(action='DESELECT')
                        for obj in original_selection:
                            try:
                                obj.select_set(True)
                            except Exception:
                                pass
                        try:
                            context.view_layer.objects.active = original_active
                        except Exception:
                            pass
                    except Exception:
                        # Jika fallback juga gagal, lanjut tanpa mengganggu alur utama
                        pass
        except Exception:
            # Jika light linking tidak tersedia atau gagal, lanjut tanpa mengganggu alur utama
            pass

        scene.light_target = hit_obj
        scene.light_target_face_location = tuple(hit_location)
        
        if self.area_shape:
            shape_display = str(self.area_shape).title()
            self.report({'INFO'}, f'{shape_display} Area light successfully added to {hit_obj.name}')
        else:
            self.report({'INFO'}, f'{light_type_str.title()} light successfully added to {hit_obj.name}')
        
        return {'FINISHED'}

    def clear_temp_data(self, scene):
        """Clear temporary hit data on the scene safely.

        In Blender 5.0, Scene properties like lumi_temp_* are defined as
        RNA properties, not plain ID properties. Using ``del scene[attr]``
        can raise ``KeyError: 'property not found in group'`` when the
        underlying ID property entry does not exist. To avoid this, we
        reset each property to a safe default value instead of deleting
        it from the ID property group.
        """
        temp_defaults = {
            'lumi_temp_hit_obj': None,
            'lumi_temp_hit_location': (0.0, 0.0, 0.0),
            'lumi_temp_hit_normal': (0.0, 0.0, 1.0),
            'lumi_temp_hit_index': 0,
        }

        for attr, default in temp_defaults.items():
            if hasattr(scene, attr):
                try:
                    setattr(scene, attr, default)
                except Exception:
                    # Failsafe: ignore reset errors to avoid interrupting the operator
                    pass


def get_favorite_templates(self, context):
    """Return top 5 most used templates for quick access"""
    try:
        from ..operators.smart_template.template_library import list_templates, get_template_categories, get_studio_commercial_templates, get_dramatic_cinematic_templates
        
        studio_templates = get_studio_commercial_templates()
        dramatic_templates = get_dramatic_cinematic_templates()
        
        favorites = []
        
        priority_studio = ["three_point_setup", "high_key_ecommerce", "clamshell_beauty", "butterfly_glamor"]
        for template_id in priority_studio:
            if template_id in studio_templates:
                template = studio_templates[template_id]
                template_name = template.get("name", "Unknown Template")
                favorites.append((template_id, template_name, f"Apply {template_name}"))
        
        priority_dramatic = ["rembrandt_dramatic", "hero_shot_premium", "low_key_dramatic"]
        for template_id in priority_dramatic:
            if template_id in dramatic_templates:
                template = dramatic_templates[template_id]
                template_name = template.get("name", "Unknown Template")
                favorites.append((template_id, template_name, f"Apply {template_name}"))
        
        if not favorites:
            favorites.append(("none", "No Templates", "No templates available"))
            
        return favorites[:5]
        
    except ImportError:
        return [("none", "Templates Not Available", "Template system not loaded")]
    except Exception as e:
        return [("error", "Error Loading Templates", f"Error: {str(e)}")]


# === NEW TEMPLATE CATEGORY OPERATORS ===

class LUMI_OT_studio_commercial_menu(bpy.types.Operator):
    """Studio & Commercial Templates Menu"""
    bl_idname = "lumi.studio_commercial_menu"
    bl_label = "Studio & Commercial Templates"
    bl_description = "Show Studio & Commercial lighting templates"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="LUMI_MT_template_studio_commercial")
        return {'FINISHED'}


class LUMI_OT_dramatic_cinematic_menu(bpy.types.Operator):
    """Dramatic & Cinematic Templates Menu"""
    bl_idname = "lumi.dramatic_cinematic_menu"
    bl_label = "Dramatic & Cinematic Templates"
    bl_description = "Show Dramatic & Cinematic lighting templates"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="LUMI_MT_template_dramatic_cinematic")
        return {'FINISHED'}


class LUMI_OT_environment_realistic_menu(bpy.types.Operator):
    """Environment & Realistic Templates Menu"""
    bl_idname = "lumi.environment_realistic_menu"
    bl_label = "Environment & Realistic Templates"
    bl_description = "Show Environment & Realistic lighting templates"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="LUMI_MT_template_environment_realistic")
        return {'FINISHED'}


class LUMI_OT_utilities_single_lights_menu(bpy.types.Operator):
    """Utilities & Single Lights Templates Menu"""
    bl_idname = "lumi.utilities_single_lights_menu"
    bl_label = "Utilities & Single Lights Templates"
    bl_description = "Show Utilities & Single Lights templates"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="LUMI_MT_template_utilities_single")
        return {'FINISHED'}


class LUMI_OT_template_category_browser(bpy.types.Operator):
    """Template Category Browser"""
    bl_idname = "lumi.template_category_browser"
    bl_label = "Template Category Browser"
    bl_description = "Browse templates by category with search and filter"
    bl_options = {'REGISTER', 'UNDO'}
    
    category_filter: bpy.props.EnumProperty(
        name="Category",
        description="Filter templates by category",
        items=[
            ('ALL', 'All Categories', 'Show all templates'),
            ('Studio & Commercial', 'Studio & Commercial', 'Professional studio lighting'),
            ('Dramatic & Cinematic', 'Dramatic & Cinematic', 'Dramatic and cinematic lighting'),
            ('Environment & Realistic', 'Environment & Realistic', 'Natural environment lighting'),
            ('Utilities & Single Lights', 'Utilities & Single Lights', 'Single light utilities'),
        ],
        default='ALL'
    )
    
    search_text: bpy.props.StringProperty(
        name="Search",
        description="Search templates by name",
        default=""
    )
    
    selected_template: bpy.props.StringProperty(
        name="Selected Template",
        description="Template to apply",
        default=""
    )
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        if not self.selected_template:
            self.report({'WARNING'}, 'No template selected')
            return {'CANCELLED'}
        
        if not context.selected_objects:
            self.report({'WARNING'}, 'Please select an object to light')
            return {'CANCELLED'}
        
        try:
            bpy.ops.lumi.apply_lighting_template(
                template_id=self.selected_template,
                auto_scale=True,
                use_camera_relative=True
            )
            
            from .smart_template.template_library import get_template
            template = get_template(self.selected_template)
            template_name = template.get('name', self.selected_template) if template else self.selected_template
            
            self.report({'INFO'}, f"Applied template: {template_name}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply template: {str(e)}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="LumiFlow Template Browser", icon='LIGHT')
        
        row = layout.row()
        row.prop(self, "category_filter", text="Category")
        row.prop(self, "search_text", text="Search", icon='VIEWZOOM')
        
        layout.separator()
        
        try:
            from .smart_template.template_library import BUILTIN_TEMPLATES
            
            filtered_templates = []
            search_lower = self.search_text.lower()
            
            for template_id, template in BUILTIN_TEMPLATES.items():
                if self.category_filter != 'ALL':
                    if template.get('category') != self.category_filter:
                        continue
                
                if search_lower:
                    template_name = template.get('name', '').lower()
                    template_desc = template.get('description', '').lower()
                    if search_lower not in template_name and search_lower not in template_desc:
                        continue
                
                filtered_templates.append((template_id, template))
            
            if not filtered_templates:
                layout.label(text="No templates found", icon='INFO')
                return
            
            filtered_templates.sort(key=lambda x: x[1].get('name', ''))
            
            box = layout.box()
            box.label(text=f"Templates ({len(filtered_templates)} found):")
            
            for template_id, template in filtered_templates[:10]:
                row = box.row()
                
                op = row.operator("lumi.template_category_browser", 
                                text=template.get('name', template_id), 
                                icon='LIGHT_DATA')
                op.selected_template = template_id
                op.category_filter = self.category_filter
                op.search_text = self.search_text
                
                category = template.get('category', 'Unknown')
                category_icons = {
                    'Studio & Commercial': 'LIGHT_AREA',
                    'Dramatic & Cinematic': 'CAMERA_DATA',
                    'Environment & Realistic': 'WORLD',
                    'Utilities & Single Lights': 'LIGHT_SUN'
                }
                icon = category_icons.get(category, 'LIGHT')
                row.label(text="", icon=icon)
                
                light_count = len(template.get('lights', []))
                row.label(text=f"{light_count}L")
            
            if len(filtered_templates) > 10:
                layout.label(text=f"... and {len(filtered_templates) - 10} more templates")
        
        except Exception as e:
            layout.label(text=f"Error loading templates: {str(e)}", icon='ERROR')

# --- NEW SMART TEMPLATE LIGHT PIE OPERATORS ---

class LUMI_OT_smart_template_light_pie_call(bpy.types.Operator):
    """Call Smart Template Light Pie Menu"""
    bl_idname = "lumi.smart_template_light_pie_call"
    bl_label = "Smart Template Light Pie"
    bl_description = "Open Smart Template Light Pie Menu for professional lighting setup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and 
                context.selected_objects and 
                any(obj.type == 'MESH' for obj in context.selected_objects))

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        if context.selected_objects:
            mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            if mesh_objects:
                target_obj = mesh_objects[0]
                scene = context.scene
                scene.lumi_temp_hit_obj = target_obj
                
                target_location = target_obj.location.copy()
                scene.lumi_temp_hit_location = tuple(target_location)
                
                target_normal = Vector((0, 0, 1))
                scene.lumi_temp_hit_normal = tuple(target_normal)
                scene.lumi_temp_hit_index = 0
            else:
                self.report({'WARNING'}, 'Please select a mesh object to use as lighting target')
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, 'Please select a mesh object to use as lighting target')
            return {'CANCELLED'}

        bpy.ops.wm.call_menu_pie(name="LUMI_MT_smart_template_light_pie")
        return {'FINISHED'}

    def execute(self, context):
        return self.invoke(context, None)

class LUMI_OT_template_favorites(bpy.types.Operator):
    """Template Favorites Menu"""
    bl_idname = "lumi.template_favorites"
    bl_label = "Template Favorites"
    bl_description = "Access favorite lighting templates quickly"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def execute(self, context):
        self.draw_favorites_menu(context)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Favorite Templates", icon='SOLO_ON')
        
        favorite_templates = [
            ("three_point_setup", "Three-Point Setup"),
            ("high_key_ecommerce", "High-Key E-commerce"), 
            ("low_key_dramatic", "Low-Key Dramatic"),
            ("key_light_only", "Key Light Only"),
            ("fill_light_only", "Fill Light Only"),
            ("rim_light_only", "Rim Light Only"),
            ("hero_shot_premium", "Hero Shot Premium"),
            ("clamshell_beauty", "Clamshell Beauty"),
        ]
        
        col = layout.column()
        for template_id, template_name in favorite_templates:
            row = col.row()
            op = row.operator("lumi.apply_lighting_template", text=template_name, icon='LIGHT_DATA')
            op.template_id = template_id
            op.auto_scale = True
            op.use_camera_relative = True
            
            row.operator("lumi.toggle_template_favorite", text="", icon='SOLO_ON').template_id = template_id
class LUMI_OT_template_menu_call(bpy.types.Operator):
    """Call Template Menu"""
    bl_idname = "lumi.template_menu_call"
    bl_label = "Template Menu"
    bl_description = "Open LumiFlow Template Menu for lighting templates"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        scene = context.scene
        
        if context.selected_objects:
            mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            
            if mesh_objects:
                mouse_pos = (event.mouse_region_x, event.mouse_region_y)
                hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, mouse_pos)
                
                if hit_obj and hit_obj.type == 'MESH':
                    scene.lumi_temp_hit_obj = hit_obj
                    scene.lumi_temp_hit_location = tuple(hit_location)
                    scene.lumi_temp_hit_normal = tuple(hit_normal)
                    scene.lumi_temp_hit_index = hit_index
                else:
                    scene.lumi_temp_hit_obj = None
                    scene.lumi_temp_hit_location = (0.0, 0.0, 0.0)
                    scene.lumi_temp_hit_normal = (0.0, 0.0, 1.0)
                    scene.lumi_temp_hit_index = 0
                    
                target_obj = mesh_objects[0]
                scene.lumi_temp_selected_obj = target_obj
                scene.lumi_temp_selected_location = tuple(target_obj.location.copy())
                scene.lumi_temp_selected_normal = (0.0, 0.0, 1.0)
                scene.lumi_temp_selected_index = 0
            else:
                scene.lumi_temp_selected_obj = None
                scene.lumi_temp_selected_location = (0.0, 0.0, 0.0)
                scene.lumi_temp_selected_normal = (0.0, 0.0, 1.0)
                scene.lumi_temp_selected_index = 0
                
                mouse_pos = (event.mouse_region_x, event.mouse_region_y)
                hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, mouse_pos)
                
                if not hit_obj or hit_obj.type != 'MESH':
                    scene.lumi_temp_hit_obj = None
                    scene.lumi_temp_hit_location = (0.0, 0.0, 0.0)
                    scene.lumi_temp_hit_normal = (0.0, 0.0, 1.0)
                    scene.lumi_temp_hit_index = 0
                else:
                    scene.lumi_temp_hit_obj = hit_obj
                    scene.lumi_temp_hit_location = tuple(hit_location)
                    scene.lumi_temp_hit_normal = tuple(hit_normal)
                    scene.lumi_temp_hit_index = hit_index
        else:
            scene.lumi_temp_selected_obj = None
            scene.lumi_temp_selected_location = (0.0, 0.0, 0.0)
            scene.lumi_temp_selected_normal = (0.0, 0.0, 1.0)
            scene.lumi_temp_selected_index = 0
            
            mouse_pos = (event.mouse_region_x, event.mouse_region_y)
            hit_obj, hit_location, hit_normal, hit_index = lumi_raycast_at_mouse(context, mouse_pos)
            
            if not hit_obj or hit_obj.type != 'MESH':
                scene.lumi_temp_hit_obj = None
                scene.lumi_temp_hit_location = (0.0, 0.0, 0.0)
                scene.lumi_temp_hit_normal = (0.0, 0.0, 1.0)
                scene.lumi_temp_hit_index = 0
            else:
                scene.lumi_temp_hit_obj = hit_obj
                scene.lumi_temp_hit_location = tuple(hit_location)
                scene.lumi_temp_hit_normal = tuple(hit_normal)
                scene.lumi_temp_hit_index = hit_index

        try:
            bpy.ops.wm.call_menu(name="LUMI_MT_template_menu")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open template menu: {str(e)}")
            return {'CANCELLED'}
    
    def execute(self, context):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        scene = context.scene
        if context.selected_objects:
            mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            if mesh_objects:
                target_obj = mesh_objects[0]
                scene.lumi_temp_hit_obj = target_obj
                
                target_location = target_obj.location.copy()
                scene.lumi_temp_hit_location = tuple(target_location)
                
                target_normal = Vector((0, 0, 1))
                scene.lumi_temp_hit_normal = tuple(target_normal)
                scene.lumi_temp_hit_index = 0
            else:
                scene.lumi_temp_hit_obj = None
                scene.lumi_temp_hit_location = (0.0, 0.0, 0.0)
                scene.lumi_temp_hit_normal = (0.0, 0.0, 1.0)
                scene.lumi_temp_hit_index = 0
        else:
            scene.lumi_temp_hit_obj = None
            scene.lumi_temp_hit_location = (0.0, 0.0, 0.0)
            scene.lumi_temp_hit_normal = (0.0, 0.0, 1.0)
            scene.lumi_temp_hit_index = 0

        try:
            bpy.ops.wm.call_menu(name="LUMI_MT_template_menu")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open template menu: {str(e)}")
            return {'CANCELLED'}

class LUMI_OT_flip_menu_call(bpy.types.Operator):
    """Call Light Flip Menu"""
    bl_idname = "lumi.flip_menu_call"
    bl_label = "Light Flip Menu"
    bl_description = "Open LumiFlow Light Flip Menu for flip operations"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        try:
            bpy.ops.wm.call_menu(name="LUMIFLOW_MT_light_flip_menu")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open flip menu: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_scale_axis_menu_call(bpy.types.Operator):
    """Quick Scale Axis Menu"""
    bl_idname = "lumi.scale_axis_menu_call"
    bl_label = "Scale Axis Menu"
    bl_description = "Quickly change scale axis for Area lights (Rectangle/Ellipse)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Operator is only available when LumiFlow is enabled
        return lumi_is_addon_enabled()

    def _can_use_custom_axis(self, context):
        """Check if selection contains an Area light with Rectangle/Ellipse shape"""
        try:
            selected_lights = [obj for obj in getattr(context, "selected_objects", []) if obj.type == 'LIGHT']
        except Exception:
            return False

        for light in selected_lights:
            data = getattr(light, "data", None)
            if getattr(data, "type", None) == 'AREA':
                shape = getattr(data, 'shape', 'SQUARE')
                if shape in {'RECTANGLE', 'ELLIPSE'}:
                    return True

        return False

    def invoke(self, context, event):
        scene = getattr(context, 'scene', None)
        if scene is None:
            return {'CANCELLED'}

        # Require Smart Control mode and Scale Axis property for consistency
        smart_control_mode_enabled = getattr(scene, 'lumi_smart_control_mode_enabled', True)
        if not smart_control_mode_enabled or not hasattr(scene, 'lumi_scale_axis'):
            self.report({'INFO'}, "Scale Axis menu is available only when Smart Control mode is enabled")
            return {'CANCELLED'}

        if not self._can_use_custom_axis(context):
            # Match existing behavior in smart_ops for axis limitations
            self.report({'INFO'}, "Axis change only available for Area lights with Rectangle/Ellipse shape")
            return {'CANCELLED'}

        def draw_scale_axis_menu(menu, ctx):
            layout = menu.layout
            scn = getattr(ctx, 'scene', None)
            if scn is None or not hasattr(scn, 'lumi_scale_axis'):
                return

            col = layout.column(align=True)
            # Vertical layout: one button per row (XY, X, Y)
            for axis_id in ('XY', 'X', 'Y'):
                row = col.row(align=True)
                row.prop_enum(scn, "lumi_scale_axis", axis_id)

        try:
            context.window_manager.popup_menu(draw_scale_axis_menu, title="Scale Axis", icon='ORIENTATION_LOCAL')
        except Exception:
            return {'CANCELLED'}

        return {'FINISHED'}

class LUMI_OT_set_light_assignment_mode(bpy.types.Operator):
    """Set Light Assignment Mode"""
    bl_idname = "lumi.set_light_assignment_mode"
    bl_label = "Set Light Assignment Mode"
    bl_description = "Set whether new lights are assigned globally (Scene) or to active camera only"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(
        name="Assignment Mode",
        description="Light assignment mode",
        items=[
            ('SCENE', "Scene", "New lights are visible to all cameras (global)"),
            ('CAMERA', "Camera", "New lights are only visible to the active camera")
        ],
        default='CAMERA'
    )

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def execute(self, context):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        if self.mode == 'CAMERA':
            # Check if any cameras exist in the scene
            cameras = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
            if not cameras:
                self.report({'WARNING'}, 'No cameras found in scene. Cannot switch to Camera mode.')
                return {'CANCELLED'}

        scene = context.scene
        scene.lumi_light_assignment_mode = self.mode

        if self.mode == 'SCENE':
            self.report({'INFO'}, "Light assignment mode set to: Scene (global lights)")
        else:
            self.report({'INFO'}, "Light assignment mode set to: Camera (camera-specific lights)")

        return {'FINISHED'}

class LUMI_OT_quick_assign_light(bpy.types.Operator):
    """Quick Assign Light to Scene/Camera"""
    bl_idname = "lumi.quick_assign_light"
    bl_label = "Quick Assign Light"
    bl_description = "Quick assign selected light to scene or specific camera"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.selected_objects and
                any(obj.type == 'LIGHT' for obj in context.selected_objects))

    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}

        # Check if exactly one light is selected
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        if len(selected_lights) != 1:
            self.report({'WARNING'}, 'Please select exactly one light')
            return {'CANCELLED'}

        self.selected_light = selected_lights[0]

        # Show assignment menu
        context.window_manager.popup_menu(self.draw_assignment_menu, title="Assign Light To", icon='LIGHT')
        return {'FINISHED'}

    def draw_assignment_menu(self, menu, context):
        layout = menu.layout

        # Scene assignment
        op = layout.operator("lumi.assign_light_to_target", text="Scene (Global)", icon='WORLD')
        op.light_name = self.selected_light.name
        op.target_type = 'SCENE'

        layout.separator()

        # Camera assignments
        cameras = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
        if cameras:
            for camera in cameras:
                op = layout.operator("lumi.assign_light_to_target", text=f"Camera: {camera.name}", icon='CAMERA_DATA')
                op.light_name = self.selected_light.name
                op.target_type = 'CAMERA'
                op.camera_name = camera.name
        else:
            layout.label(text="No cameras found", icon='ERROR')

class LUMI_OT_assign_light_to_target(bpy.types.Operator):
    """Assign Light to Target"""
    bl_idname = "lumi.assign_light_to_target"
    bl_label = "Assign Light to Target"
    bl_options = {'INTERNAL'}

    light_name: bpy.props.StringProperty()
    target_type: bpy.props.StringProperty()  # 'SCENE' or 'CAMERA'
    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        from ..core.assign_manager import get_assign_light_manager

        manager = get_camera_light_manager()

        if self.target_type == 'SCENE':
            # Assign to scene (global)
            manager.assign_light_to_camera("SCENE", self.light_name)
            self.report({'INFO'}, f"Assigned '{self.light_name}' to Scene")
        elif self.target_type == 'CAMERA':
            # Assign to specific camera
            manager.assign_light_to_camera(self.camera_name, self.light_name)
            self.report({'INFO'}, f"Assigned '{self.light_name}' to Camera '{self.camera_name}'")

        # Update visibility
        if context.scene.camera:
            manager.update_light_visibility_for_camera(context, context.scene.camera.name)

        return {'FINISHED'}

