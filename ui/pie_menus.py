# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Pie Menus Module
Contains all pie menu classes for the LumiFlow Blender addon UI.
"""
import bpy

from ..utils import lumi_is_addon_enabled

class LUMI_MT_add_light_pie(bpy.types.Menu):
    """Vertical menu for adding smart lights"""
    bl_label = "Add Smart Light"
    bl_idname = "LUMI_MT_add_light_pie"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have stored hit data from operator call
        scene = context.scene
        hit_obj = getattr(scene, 'lumi_temp_hit_obj', None)
        hit_location = getattr(scene, 'lumi_temp_hit_location', None)
        has_hit_data = (hit_obj is not None and hit_location is not None and 
                       hit_obj.type == 'MESH' and lumi_is_addon_enabled())

        # Note: Gray out logic moved to main menu (LUMI_MT_template_menu)

        if not has_hit_data:
            # No hit data - show instruction based on selection
            selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            has_selected_mesh = len(selected_mesh_objects) > 0

            if has_selected_mesh:
                layout.label(text="Hover selected mesh to add light", icon='INFO')
            else:
                layout.label(text="Hover mesh to add light", icon='INFO')
        else:
            # Has hit data - show the menu
            op = layout.operator("lumi.add_smart_light", text="Sun Light", icon='LIGHT_SUN')
            op.light_type = "SUN"
            op.use_stored_target = True
            
            op = layout.operator("lumi.add_smart_light", text="Point Light", icon='LIGHT_POINT')
            op.light_type = "POINT"
            op.use_stored_target = True
            
            op = layout.operator("lumi.add_smart_light", text="Spot Light", icon='LIGHT_SPOT')
            op.light_type = "SPOT"
            op.use_stored_target = True
            
                        
            layout.separator()
            
            # Area Light Shapes
            layout.label(text="Area Light Shapes", icon='MESH_GRID')
            
            op = layout.operator("lumi.add_smart_light", text="Square Area", icon='MESH_PLANE')
            op.light_type = "AREA"
            op.area_shape = "SQUARE"
            op.use_stored_target = True
            
            op = layout.operator("lumi.add_smart_light", text="Rectangle Area", icon='MESH_PLANE')
            op.light_type = "AREA"
            op.area_shape = "RECTANGLE"
            op.use_stored_target = True
            
            op = layout.operator("lumi.add_smart_light", text="Disk Area", icon='MESH_CIRCLE')
            op.light_type = "AREA"
            op.area_shape = "DISK"
            op.use_stored_target = True
            
            op = layout.operator("lumi.add_smart_light", text="Ellipse Area", icon='MESH_CIRCLE')
            op.light_type = "AREA"
            op.area_shape = "ELLIPSE"
            op.use_stored_target = True
        
             
class LUMI_MT_smart_template_light_pie(bpy.types.Menu):
    """Smart Template Light Pie Menu for professional lighting setup"""
    bl_label = "Smart Template Light"
    bl_idname = "LUMI_MT_smart_template_light_pie"
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        # North - Key Light
        op = pie.operator("lumi.apply_template_default", text="Key Light", icon='LIGHT_SUN')
        op.template_id = "key_light_only"
        
        # South - Fill Light
        pie.operator("lumi.analyze_subject_advanced", text="AI Analyze", icon='MODIFIER_DATA')
        
        # South-East - Template Browser
        pie.menu("LUMI_MT_template_menu", text="Templates", icon='OUTLINER_COLLECTION')       
        
        # West - Back Light
        op = pie.operator("lumi.apply_template_default", text="Back Light", icon='LIGHT_POINT')
        op.template_id = "backlight_only"
        
        # North-East - Top Down Light
        op = pie.operator("lumi.apply_template_default", text="Top-Down Light", icon='LIGHT_DATA')
        op.template_id = "top_down_light"
        
        # North-West - AI Analyze            
        op = pie.operator("lumi.apply_template_default", text="Fill Light", icon='LIGHT_AREA')
        op.template_id = "fill_light_only" 
                
         # East - Rim Light
        op = pie.operator("lumi.apply_template_default", text="Rim Light", icon='LIGHT_SPOT')
        op.template_id = "rim_light_only"

        # South-West - Favorites
        pie.menu("LUMI_MT_template_favorites", text="Favorites", icon='SOLO_ON')


# --- NEW TEMPLATE CATEGORY MENUS ---

class LUMI_MT_template_studio_commercial(bpy.types.Menu):
    """Studio & Commercial lighting templates submenu"""
    bl_label = "Studio & Commercial"
    bl_idname = "LUMI_MT_template_studio_commercial"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have stored selected object data
        scene = context.scene
        selected_obj = getattr(scene, 'lumi_temp_selected_obj', None)
        has_selected_data = (selected_obj is not None and 
                           selected_obj.type == 'MESH' and 
                           lumi_is_addon_enabled())

        # Note: Gray out logic moved to main menu (LUMI_MT_template_menu)

        if not has_selected_data:
            # No selected object data - show instruction
            layout.label(text="Select mesh object to apply template", icon='INFO')
        else:
            # Has selected object data - show the menu
            try:
                from ..operators.smart_template.template_library import get_studio_commercial_templates
                studio_templates = get_studio_commercial_templates()

                if studio_templates:
                    # Display available studio & commercial templates
                    for template_id, template in studio_templates.items():
                        template_name = template.get('name', template_id.replace('_', ' ').title())
                        op = layout.operator("lumi.apply_lighting_template", text=template_name, icon='LIGHT_DATA')
                        op.template_id = template_id
                        op.auto_scale = True
                        op.use_camera_relative = True
                else:
                    layout.label(text="No Studio & Commercial templates available", icon='INFO')

            except Exception as e:
                layout.label(text=f"Error loading templates: {str(e)[:30]}...", icon='ERROR')


class LUMI_MT_template_dramatic_cinematic(bpy.types.Menu):
    """Dramatic & Cinematic lighting templates submenu"""
    bl_label = "Dramatic & Cinematic"
    bl_idname = "LUMI_MT_template_dramatic_cinematic"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have stored selected object data
        scene = context.scene
        selected_obj = getattr(scene, 'lumi_temp_selected_obj', None)
        has_selected_data = (selected_obj is not None and 
                           selected_obj.type == 'MESH' and 
                           lumi_is_addon_enabled())

        # Note: Gray out logic moved to main menu (LUMI_MT_template_menu)

        if not has_selected_data:
            # No selected object data - show instruction
            layout.label(text="Select mesh object to apply template", icon='INFO')
        else:
            # Has selected object data - show the menu
            try:
                from ..operators.smart_template.template_library import get_dramatic_cinematic_templates
                dramatic_templates = get_dramatic_cinematic_templates()

                if dramatic_templates:
                    # Display available dramatic & cinematic templates
                    for template_id, template in dramatic_templates.items():
                        template_name = template.get('name', template_id.replace('_', ' ').title())
                        op = layout.operator("lumi.apply_lighting_template", text=template_name, icon='LIGHT_DATA')
                        op.template_id = template_id
                        op.auto_scale = True
                        op.use_camera_relative = True
                else:
                    layout.label(text="No Dramatic & Cinematic templates available", icon='INFO')

            except Exception as e:
                layout.label(text=f"Error loading templates: {str(e)[:30]}...", icon='ERROR')


class LUMI_MT_template_environment_realistic(bpy.types.Menu):
    """Environment & Realistic lighting templates submenu"""
    bl_label = "Environment & Realistic"
    bl_idname = "LUMI_MT_template_environment_realistic"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have stored selected object data
        scene = context.scene
        selected_obj = getattr(scene, 'lumi_temp_selected_obj', None)
        has_selected_data = (selected_obj is not None and 
                           selected_obj.type == 'MESH' and 
                           lumi_is_addon_enabled())

        # Note: Gray out logic moved to main menu (LUMI_MT_template_menu)

        if not has_selected_data:
            # No selected object data - show instruction
            layout.label(text="Select mesh object to apply template", icon='INFO')
        else:
            # Has selected object data - show the menu
            try:
                from ..operators.smart_template.template_library import get_environment_realistic_templates
                environment_templates = get_environment_realistic_templates()

                if environment_templates:
                    # Display available environment & realistic templates
                    for template_id, template in environment_templates.items():
                        template_name = template.get('name', template_id.replace('_', ' ').title())
                        op = layout.operator("lumi.apply_lighting_template", text=template_name, icon='LIGHT_DATA')
                        op.template_id = template_id
                        op.auto_scale = True
                        op.use_camera_relative = True
                else:
                    layout.label(text="No Environment & Realistic templates available", icon='INFO')

            except Exception as e:
                layout.label(text=f"Error loading templates: {str(e)[:30]}...", icon='ERROR')


class LUMI_MT_template_utilities_single(bpy.types.Menu):
    """Utilities & Single Lights templates submenu"""
    bl_label = "Utilities & Single Lights"
    bl_idname = "LUMI_MT_template_utilities_single"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have stored selected object data
        scene = context.scene
        selected_obj = getattr(scene, 'lumi_temp_selected_obj', None)
        has_selected_data = (selected_obj is not None and 
                           selected_obj.type == 'MESH' and 
                           lumi_is_addon_enabled())

        # Note: Gray out logic moved to main menu (LUMI_MT_template_menu)

        if not has_selected_data:
            # No selected object data - show instruction
            layout.label(text="Select mesh object to apply template", icon='INFO')
        else:
            # Has selected object data - show the menu
            try:
                from ..operators.smart_template.template_library import get_utilities_single_lights_templates
                utilities_templates = get_utilities_single_lights_templates()

                if utilities_templates:
                    # Display available utilities & single lights templates
                    for template_id, template in utilities_templates.items():
                        template_name = template.get('name', template_id.replace('_', ' ').title())
                        op = layout.operator("lumi.apply_template_default", text=template_name, icon='LIGHT_DATA')
                        op.template_id = template_id
                else:
                    layout.label(text="No Utilities & Single Lights templates available", icon='INFO')

            except Exception as e:
                layout.label(text=f"Error loading templates: {str(e)[:30]}...", icon='ERROR')


class LUMI_MT_template_favorites(bpy.types.Menu):
    """Template Favorites Menu"""
    bl_label = "Template Favorites"
    bl_idname = "LUMI_MT_template_favorites"

    @classmethod
    def poll(cls, context):
        """Check if addon is enabled"""
        return lumi_is_addon_enabled()

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        favorites = getattr(scene, 'lumi_template_favorites', '')
        
        # Convert to list, handle empty string
        if favorites.strip():
            fav_list = [f.strip() for f in favorites.split(',') if f.strip()]
        else:
            fav_list = []
        
        # Import template library to get template info
        from ..assets.templates import ALL_TEMPLATES
        
        if not fav_list:
            # No favorites - show message
            layout.label(text="No Favorites Yet", icon='SOLO_OFF')
            layout.separator()
            layout.operator("lumi.show_all_templates", text="Browse Templates", icon='OUTLINER_COLLECTION')
        else:
            # Show favorite templates vertically
            layout.label(text="Your Favorite Templates:", icon='SOLO_ON')
            layout.separator()
            
            for template_id in fav_list:
                # Find template info
                template_info = ALL_TEMPLATES.get(template_id)
                if template_id:
                    op = layout.operator("lumi.apply_lighting_template", 
                                    text=template_id, 
                                    icon='LIGHT_DATA')
                    op.template_id = template_id
                    op.auto_scale = True
                    op.use_camera_relative = True
                else:
                    # Template not found in library
                    layout.label(text=f"Missing: {template_id}", icon='ERROR')
            
            layout.separator()
            layout.operator("lumi.show_all_templates", text="Browse More Templates", icon='OUTLINER_COLLECTION')

class LUMI_MT_template_menu(bpy.types.Menu):
    """Main template selection menu"""
    bl_label = "Lighting Templates"
    bl_idname = "LUMI_MT_template_menu"
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def draw(self, context):
        layout = self.layout

        # Check if we have stored hit data from operator call
        scene = context.scene
        hit_obj = getattr(scene, 'lumi_temp_hit_obj', None)
        hit_location = getattr(scene, 'lumi_temp_hit_location', None)
        has_hit_data = hit_obj is not None and hit_location is not None

        # Check if there are mesh objects selected
        selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        has_selected_mesh = len(selected_mesh_objects) > 0

        # For Default Lights: validate hit data AND hit must be on selected mesh
        hit_on_selected_mesh = False
        if has_hit_data and has_selected_mesh and hit_obj:
            # Check if hit object is one of the selected mesh objects
            hit_on_selected_mesh = hit_obj in selected_mesh_objects

        #Single light - Default Lights (validate hit data AND hit on selected mesh)
        default_layout = layout.row()
        default_layout.enabled = has_hit_data and (not has_selected_mesh or hit_on_selected_mesh) and lumi_is_addon_enabled()
        default_layout.menu("LUMI_MT_add_light_pie", text="Default Light", icon='LIGHT_AREA')

        #Template single light - Utilities (validate selection only)
        utilities_layout = layout.row()
        utilities_layout.enabled = has_selected_mesh and lumi_is_addon_enabled()
        utilities_layout.menu("LUMI_MT_template_utilities_single", text="Utilities & Single Lights", icon='LIGHT_SUN')

        layout.separator()

        # Template menus (validate selection only)
        studio_layout = layout.row()
        studio_layout.enabled = has_selected_mesh and lumi_is_addon_enabled()
        studio_layout.menu("LUMI_MT_template_studio_commercial", text="Studio & Commercial", icon='LIGHT_AREA')

        dramatic_layout = layout.row()
        dramatic_layout.enabled = has_selected_mesh and lumi_is_addon_enabled()
        dramatic_layout.menu("LUMI_MT_template_dramatic_cinematic", text="Dramatic & Cinematic", icon='CAMERA_DATA')

        realistic_layout = layout.row()
        realistic_layout.enabled = has_selected_mesh and lumi_is_addon_enabled()
        realistic_layout.menu("LUMI_MT_template_environment_realistic", text="Environment & Realistic", icon='WORLD')
       


# --- FLIP TO CAMERA SUBMENU ---
class LUMIFLOW_MT_flip_to_camera(bpy.types.Menu):
    """Flip to Camera Operations Submenu"""
    bl_label = "Flip to Camera"
    bl_idname = "LUMIFLOW_MT_flip_to_camera"

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def draw(self, context):
        layout = self.layout

        # Three camera flip modes
        layout.operator("lumiflow.flip_to_camera_front",
                       text="Front (Behind Target)",
                       icon='CAMERA_DATA')

        layout.operator("lumiflow.flip_to_camera_back",
                       text="Back (Co-located)",
                       icon='CAMERA_DATA')

        layout.operator("lumiflow.flip_to_camera_along",
                       text="Along (Parallel)",
                       icon='CAMERA_DATA')


# --- LIGHT FLIP ---
class LUMIFLOW_MT_light_flip_menu(bpy.types.Menu):
    """Light Flip Operations Menu"""
    bl_label = "Light Flip Operations"
    bl_idname = "LUMIFLOW_MT_light_flip_menu"

    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def draw(self, context):
        layout = self.layout

        # Main flip operations
        layout.menu("LUMIFLOW_MT_flip_to_camera",
                   text="To Camera",
                   icon='CAMERA_DATA')

        layout.separator()

        # Directional flips
        layout.operator("lumiflow.flip_horizontal",
                       text="Flip Horizontal",
                       icon='ARROW_LEFTRIGHT')

        layout.operator("lumiflow.flip_vertical",
                       text="Flip Vertical",
                       icon='SORT_ASC')

        layout.separator()

        # Directional flips
        layout.operator("lumiflow.flip_180_degrees",
                       text="Flip 180Â° (Z-Axis)",
                       icon='LOOP_BACK')

        layout.separator()

        # Advanced flips
        layout.operator("lumiflow.flip_across_pivot",
                       text="Flip Across Pivot",
                       icon='PIVOT_BOUNDBOX')

