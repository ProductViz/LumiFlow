# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Background Operators
Main operators for the background system (Ctrl+Shift+B).
"""

import bpy
import math
from bpy.props import (
    StringProperty, BoolProperty, FloatProperty, 
    EnumProperty, FloatVectorProperty, IntProperty
)
from mathutils import Vector
from typing import List, Optional, Set

from ...utils.common import lumi_is_addon_enabled, lumi_get_light_collection


def get_background_type_items(self, context):
    """Dynamic enum items for background types."""
    from .background_presets import BACKGROUND_PRESETS
    
    items = []
    for preset_id, preset in BACKGROUND_PRESETS.items():
        icon = preset.get("icon", "MESH_PLANE")
        items.append((
            preset_id,
            preset["name"],
            preset["description"],
            icon,
            len(items)
        ))
    
    # Add "Use Existing" option
    items.append((
        "use_existing",
        "Use Existing",
        "Use existing background objects in scene",
        "SCENE_DATA",
        len(items)
    ))
    
    return items


def get_lighting_preset_items(self, context):
    """Dynamic enum items for lighting presets."""
    from .background_presets import BACKGROUND_LIGHTING_PRESETS
    
    items = []
    for preset_id, preset in BACKGROUND_LIGHTING_PRESETS.items():
        items.append((
            preset_id,
            preset["name"],
            preset["description"],
            'LIGHT',
            len(items)
        ))
    
    return items


class LUMI_OT_background_menu_call(bpy.types.Operator):
    """Open Background System Dialog (Ctrl+Shift+B)"""
    bl_idname = "lumi.background_menu_call"
    bl_label = "LumiFlow Background System"
    bl_description = "Open Background System dialog to create backgrounds with integrated lighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def invoke(self, context, event):
        if not lumi_is_addon_enabled():
            self.report({'WARNING'}, 'LumiFlow is not active!')
            return {'CANCELLED'}
        
        # Open the apply background dialog
        return bpy.ops.lumi.apply_background('INVOKE_DEFAULT')


class LUMI_OT_apply_background(bpy.types.Operator):
    """Apply background with lighting to scene"""
    bl_idname = "lumi.apply_background"
    bl_label = "Apply Background"
    bl_description = "Create background and apply lighting preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Background type
    background_type: EnumProperty(
        name="Background Type",
        description="Type of background to create",
        items=get_background_type_items,
        default=0,
    )
    
    # Custom color for colored backgrounds
    background_color: FloatVectorProperty(
        name="Background Color",
        description="Color for the background",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0),
    )
    
    # Lighting preset
    add_lighting: BoolProperty(
        name="Add Background Lighting",
        description="Add dedicated lighting for the background",
        default=True,
    )
    
    lighting_preset: EnumProperty(
        name="Lighting Preset",
        description="Lighting preset for the background",
        items=get_lighting_preset_items,
        default=0,
    )
    
    # Layer Interaction settings
    show_layer_interaction: BoolProperty(
        name="Show Layer Interaction",
        description="Show advanced layer interaction settings",
        default=False,
    )
    
    interaction_mode: EnumProperty(
        name="Interaction Mode",
        description="How lights interact between product and background",
        items=[
            ('natural', "Natural", "Lights affect both product and background", 'LIGHT_SUN', 0),
            ('isolated', "Isolated", "Full separation using light linking", 'UNLINKED', 1),
            ('hybrid', "Hybrid", "Configurable per-light interaction", 'PREFERENCES', 2),
        ],
        default='natural',
    )
    
    # Isolation settings
    product_lights_exclude_bg: BoolProperty(
        name="Product Lights Exclude Background",
        description="Product lights will not affect the background",
        default=True,
    )
    
    bg_lights_exclude_product: BoolProperty(
        name="Background Lights Exclude Product",
        description="Background lights will not affect the product",
        default=True,
    )
    
    allow_rim_spill: BoolProperty(
        name="Allow Rim Spill",
        description="Allow background lights to create subtle rim on product",
        default=False,
    )
    
    # Intensity balance
    product_intensity: FloatProperty(
        name="Product Layer Intensity",
        description="Intensity multiplier for product lights",
        min=0.0,
        max=2.0,
        default=1.0,
        subtype='FACTOR',
    )
    
    bg_intensity: FloatProperty(
        name="Background Layer Intensity",
        description="Intensity multiplier for background lights",
        min=0.0,
        max=2.0,
        default=1.0,
        subtype='FACTOR',
    )
    
    # Scale factor
    scale_factor: FloatProperty(
        name="Scale Factor",
        description="How much larger the background should be relative to product",
        min=1.5,
        max=10.0,
        default=3.0,
    )
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def invoke(self, context, event):
        # Analyze existing scene state
        self._analyze_scene(context)
        
        # Set default lighting based on background type
        self.update_default_lighting()
        
        # Show dialog
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def _analyze_scene(self, context):
        """Analyze scene for existing lights and backgrounds."""
        try:
            from .background_awareness import analyze_background, analyze_product
            
            self._bg_analysis = analyze_background(context)
            self._product_analysis = analyze_product(context)
            
            # Auto-suggest isolation if product lights exist
            if self._product_analysis.has_product_lights:
                self.interaction_mode = 'isolated'
                self.show_layer_interaction = True
        except Exception:
            self._bg_analysis = None
            self._product_analysis = None
    
    def update_default_lighting(self):
        """Update default lighting preset based on background type."""
        from .background_presets import get_recommended_lighting
        
        recommended = get_recommended_lighting(self.background_type)
        if recommended:
            self.lighting_preset = recommended
    
    def draw(self, context):
        layout = self.layout
        
        # Smart Suggestions (Phase 2)
        self._draw_smart_suggestions(layout, context)
        
        # Background Type Section
        box = layout.box()
        box.label(text="Background Type", icon='MESH_PLANE')
        box.prop(self, "background_type", text="")
        
        # Show color picker for colored backgrounds
        if self.background_type == "colored_solid":
            box.prop(self, "background_color", text="Color")
        
        box.prop(self, "scale_factor", text="Scale")
        
        # Lighting Section
        box = layout.box()
        row = box.row()
        row.prop(self, "add_lighting", text="Add Background Lighting", icon='LIGHT')
        
        if self.add_lighting:
            box.prop(self, "lighting_preset", text="Preset")
            box.prop(self, "bg_intensity", text="Intensity", slider=True)
        
        # Layer Interaction Section (collapsible)
        box = layout.box()
        row = box.row()
        row.prop(
            self, "show_layer_interaction",
            icon='TRIA_DOWN' if self.show_layer_interaction else 'TRIA_RIGHT',
            text="Layer Interaction (Intermediate/Advanced)",
            emboss=False,
        )
        
        if self.show_layer_interaction:
            col = box.column(align=True)
            col.label(text="Interaction Mode:")
            col.prop(self, "interaction_mode", text="")
            
            if self.interaction_mode in ('isolated', 'hybrid'):
                col.separator()
                col.label(text="Light Linking Settings:")
                col.prop(self, "product_lights_exclude_bg")
                col.prop(self, "bg_lights_exclude_product")
                
                if self.interaction_mode == 'hybrid':
                    col.prop(self, "allow_rim_spill")
            
            col.separator()
            col.label(text="Intensity Balance:")
            col.prop(self, "product_intensity", text="Product Layer", slider=True)
    
    def _draw_smart_suggestions(self, layout, context):
        """Draw smart suggestions based on scene analysis."""
        bg_analysis = getattr(self, '_bg_analysis', None)
        product_analysis = getattr(self, '_product_analysis', None)
        
        if not bg_analysis and not product_analysis:
            return
        
        has_suggestions = False
        
        # Check for existing background
        if bg_analysis and bg_analysis.has_background:
            box = layout.box()
            box.alert = True
            row = box.row()
            row.label(text="Existing background detected", icon='INFO')
            row = box.row()
            row.label(text=f"Type: {bg_analysis.background_type}")
            if bg_analysis.has_background_lights:
                row = box.row()
                row.label(text=f"Has {len(bg_analysis.background_lights)} BG lights")
            has_suggestions = True
        
        # Check for existing product lights
        if product_analysis and product_analysis.has_product_lights:
            if not has_suggestions:
                box = layout.box()
            else:
                box = layout.box()
            
            light_count = len(product_analysis.product_lights)
            row = box.row()
            row.label(text=f"{light_count} product lights detected", icon='LIGHT')
            row = box.row()
            row.label(text="Isolation mode recommended", icon='CHECKMARK')
            has_suggestions = True
        
        # Show suggestions from analysis
        if bg_analysis and bg_analysis.suggestions:
            box = layout.box()
            box.label(text="Suggestions:", icon='INFO')
            for suggestion in bg_analysis.suggestions[:3]:  # Max 3 suggestions
                row = box.row()
                row.scale_y = 0.8
                row.label(text=f"• {suggestion}")
        
        if has_suggestions:
            layout.separator()
    
    def execute(self, context):
        from .background_generator import (
            create_seamless_background,
            create_flat_backdrop,
            create_ground_plane,
            get_existing_backgrounds,
        )
        from .background_presets import get_background_preset, get_lighting_preset
        
        # Get preset info
        bg_preset = get_background_preset(self.background_type)
        
        # Create or use existing background
        bg_object = None
        
        if self.background_type == "use_existing":
            # Find existing backgrounds
            existing = get_existing_backgrounds(context)
            if existing:
                bg_object = existing[0]
                self.report({'INFO'}, f"Using existing background: {bg_object.name}")
            else:
                self.report({'WARNING'}, "No existing background found")
                return {'CANCELLED'}
        else:
            # Determine color
            if self.background_type == "colored_solid":
                color = tuple(self.background_color)
            elif bg_preset:
                color = bg_preset.get("color", (1.0, 1.0, 1.0))
            else:
                color = (1.0, 1.0, 1.0)
            
            # Create background based on type
            bg_type = bg_preset.get("type", "seamless") if bg_preset else "seamless"
            
            if bg_type == "seamless":
                bg_object = create_seamless_background(
                    context,
                    color=color,
                    name=f"LumiFlow_{bg_preset['name'].replace(' ', '_')}",
                    scale_factor=self.scale_factor,
                )
            elif bg_type == "backdrop":
                bg_object = create_flat_backdrop(
                    context,
                    color=color,
                    name=f"LumiFlow_{bg_preset['name'].replace(' ', '_')}",
                    scale_factor=self.scale_factor,
                )
            elif bg_type == "ground":
                reflective = bg_preset.get("reflective", False)
                bg_object = create_ground_plane(
                    context,
                    color=color,
                    name=f"LumiFlow_{bg_preset['name'].replace(' ', '_')}",
                    scale_factor=self.scale_factor,
                    reflective=reflective,
                )
            
            self.report({'INFO'}, f"Created background: {bg_object.name}")
        
        # Create background lighting if enabled
        if self.add_lighting and self.lighting_preset != "none":
            bg_lights = self.create_background_lights(context, bg_object)
            
            if bg_lights:
                self.report({'INFO'}, f"Created {len(bg_lights)} background lights")
                
                # Apply light linking if isolation mode
                if self.interaction_mode in ('isolated', 'hybrid'):
                    self.apply_light_linking(context, bg_object, bg_lights)
        
        # Apply intensity adjustments
        if self.product_intensity != 1.0:
            self.adjust_product_lights_intensity(context)
        
        return {'FINISHED'}
    
    def create_background_lights(self, context, bg_object) -> List[bpy.types.Object]:
        """Create background lights based on preset."""
        from .background_presets import get_lighting_preset
        
        preset = get_lighting_preset(self.lighting_preset)
        if not preset or not preset.get("lights"):
            return []
        
        created_lights = []
        light_collection = lumi_get_light_collection(context)
        
        for light_def in preset["lights"]:
            # Create light
            light_data = bpy.data.lights.new(
                name=light_def["name"],
                type=light_def["type"]
            )
            
            # Set properties
            props = light_def.get("properties", {})
            light_data.energy = props.get("energy", 100) * self.bg_intensity
            light_data.color = props.get("color", (1.0, 1.0, 1.0))
            
            if light_def["type"] == "AREA":
                light_data.shape = props.get("shape", "RECTANGLE")
                light_data.size = props.get("size", 1.0)
                if hasattr(light_data, "size_y"):
                    light_data.size_y = props.get("size_y", light_data.size)
            
            elif light_def["type"] == "SPOT":
                light_data.spot_size = props.get("spot_size", 0.785)
                light_data.spot_blend = props.get("spot_blend", 0.15)
            
            # Create object
            light_obj = bpy.data.objects.new(light_def["name"], light_data)
            
            # Calculate position
            position = self.calculate_light_position(
                light_def.get("position", {}),
                bg_object,
                context
            )
            light_obj.location = position
            
            # Calculate rotation
            self.orient_light_to_target(light_obj, bg_object, light_def.get("rotation", {}))
            
            # Link to collection
            if light_collection:
                light_collection.objects.link(light_obj)
            else:
                context.collection.objects.link(light_obj)
            
            # Mark as background light
            light_obj["lumiflow_bg_light"] = True
            light_obj["lumiflow_layer"] = "background"
            
            created_lights.append(light_obj)
        
        return created_lights
    
    def calculate_light_position(self, pos_def, bg_object, context) -> Vector:
        """Calculate light position based on definition."""
        method = pos_def.get("method", "relative_to_bg")
        offset = Vector(pos_def.get("offset", (0, 0, 0)))
        
        if method == "relative_to_bg" and bg_object:
            # Position relative to background center
            bg_center = bg_object.location
            return bg_center + offset
        
        return offset
    
    def orient_light_to_target(self, light_obj, bg_object, rot_def):
        """Orient light to face target."""
        target = rot_def.get("target", "background")
        
        if target == "background" and bg_object:
            # Point at background center
            direction = bg_object.location - light_obj.location
            if direction.length > 0:
                light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        elif target == "ground" and bg_object:
            # Point downward at ground
            light_obj.rotation_euler = (math.radians(90), 0, 0)
        
        elif target == "camera":
            # Point toward camera
            camera = context.scene.camera
            if camera:
                direction = camera.location - light_obj.location
                if direction.length > 0:
                    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    def apply_light_linking(self, context, bg_object, bg_lights):
        """Apply light linking for isolation mode."""
        # Get product objects (selected objects that are not background)
        product_objects = [
            obj for obj in context.selected_objects
            if obj.type == 'MESH' and not obj.get("lumiflow_background")
        ]
        
        if not product_objects:
            return
        
        # Get existing product lights
        product_lights = self.get_product_lights(context)
        
        # Apply light linking
        # Note: This uses Blender 4.0+ light linking API
        try:
            # For background lights - exclude product
            if self.bg_lights_exclude_product:
                for light in bg_lights:
                    if hasattr(light, "light_linking"):
                        # Set to include only background
                        light.light_linking.receiver_collection = None
                        # Create blocker collection for product
                        blocker_name = f"{light.name}_blocker"
                        if blocker_name not in bpy.data.collections:
                            blocker_coll = bpy.data.collections.new(blocker_name)
                            for obj in product_objects:
                                if obj.name not in blocker_coll.objects:
                                    blocker_coll.objects.link(obj)
                            light.light_linking.blocker_collection = blocker_coll
            
            # For product lights - exclude background
            if self.product_lights_exclude_bg and product_lights:
                for light in product_lights:
                    if hasattr(light, "light_linking"):
                        blocker_name = f"{light.name}_bg_blocker"
                        if blocker_name not in bpy.data.collections:
                            blocker_coll = bpy.data.collections.new(blocker_name)
                            if bg_object.name not in blocker_coll.objects:
                                blocker_coll.objects.link(bg_object)
                            light.light_linking.blocker_collection = blocker_coll
        
        except AttributeError:
            # Light linking not available in this Blender version
            self.report({'INFO'}, "Light linking requires Blender 4.0+")
    
    def get_product_lights(self, context) -> List[bpy.types.Object]:
        """Get existing product lights (Layer 1)."""
        lights = []
        light_collection = lumi_get_light_collection(context)
        
        if light_collection:
            for obj in light_collection.objects:
                if obj.type == 'LIGHT' and not obj.get("lumiflow_bg_light"):
                    lights.append(obj)
        
        return lights
    
    def adjust_product_lights_intensity(self, context):
        """Adjust intensity of product lights."""
        product_lights = self.get_product_lights(context)
        
        for light in product_lights:
            if light.data:
                light.data.energy *= self.product_intensity


class LUMI_OT_remove_background(bpy.types.Operator):
    """Remove LumiFlow background from scene"""
    bl_idname = "lumi.remove_background"
    bl_label = "Remove Background"
    bl_description = "Remove LumiFlow background and its lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    remove_lights: BoolProperty(
        name="Remove Background Lights",
        description="Also remove background lights",
        default=True,
    )
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "remove_lights")
    
    def execute(self, context):
        from .background_generator import get_existing_backgrounds, remove_background
        
        backgrounds = get_existing_backgrounds(context)
        
        if not backgrounds:
            self.report({'WARNING'}, "No LumiFlow backgrounds found")
            return {'CANCELLED'}
        
        removed_count = 0
        
        # Remove background lights if requested
        if self.remove_lights:
            for obj in list(context.scene.objects):
                if obj.type == 'LIGHT' and obj.get("lumiflow_bg_light"):
                    bpy.data.objects.remove(obj)
                    removed_count += 1
        
        # Remove backgrounds
        for bg in backgrounds:
            remove_background(bg)
            removed_count += 1
        
        self.report({'INFO'}, f"Removed {removed_count} objects")
        return {'FINISHED'}


# Registration
classes = [
    LUMI_OT_background_menu_call,
    LUMI_OT_apply_background,
    LUMI_OT_remove_background,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
