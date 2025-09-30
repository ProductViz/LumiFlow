"""
Linking Operations
Operators for light linking and group management functionality.
"""
import bpy
from bpy.props import CollectionProperty, StringProperty, BoolProperty
from mathutils import Vector
from ..utils import lumi_is_addon_enabled, lumi_get_light_collection

LUMIFLOW_COLLECTION_NAME = "LumiFlow Lights"
DEFAULT_GROUP_NAME = "Default"

# Track dynamically created menu classes for cleanup
_dynamic_menu_classes = []

# Scene attribute keys for recursion flags (avoid stale globals across reload)
_FLAG_UPDATING = "_lumi_updating_light_links"
_FLAG_GROUP_UPDATE = "_lumi_group_update_in_progress"

def light_item_marked_update(self, context):
    """Handle per-light checkbox changes; guard against recursion using
    scene-scoped flags stored on the active scene object."""
    scene = getattr(context, "scene", None) or bpy.context.scene

    # If any update is already in progress on this scene, skip to avoid recursion.
    if scene.get(_FLAG_UPDATING, False):
        return

    # Mark both flags so any other handlers or sync functions know this
    # is a programmatic/update-in-progress operation and should early-return.
    scene[_FLAG_UPDATING] = True
    scene[_FLAG_GROUP_UPDATE] = True
    
    try:
        scene = context.scene
        light_name = self.name
        lamp = bpy.data.objects.get(light_name)
        if not lamp or lamp.type != 'LIGHT':
            return

        # Determine receivers: use current object group if available, else all MESH
        receivers = []
        idx = getattr(scene, "lumi_object_groups_index", -1)
        
        if idx >= 0 and idx < len(scene.lumi_object_groups):
            grp = scene.lumi_object_groups[idx]
            for it in grp.objects:
                o = bpy.data.objects.get(it.name)
                if o and o.type == 'MESH':
                    receivers.append(o)
        else:
            receivers = [o for o in bpy.data.objects if o.type == 'MESH']

        if not receivers:
            return

        # Determine link_action from the checkbox value
        do_include = bool(self.marked)

        # Save selection/active
        original_active = context.view_layer.objects.active
        original_selected = list(context.selected_objects)

        try:
            bpy.ops.object.select_all(action='DESELECT')
            for o in receivers:
                o.select_set(True)
            lamp.select_set(True)
            context.view_layer.objects.active = lamp

            if do_include:
                bpy.ops.object.light_linking_receivers_link(link_state='INCLUDE')
            else:
                bpy.ops.object.light_linking_receivers_link(link_state='EXCLUDE')

            # Update internal link-status table for current group -> light
            links = scene.lumi_object_group_link_status
            grp_name = scene.lumi_object_groups[idx].name if (idx >= 0 and idx < len(scene.lumi_object_groups)) else ""
            # remove existing
            to_remove = [i for i,l in enumerate(links) if l.object_group_name == grp_name and l.light_name == light_name]
            for i in reversed(to_remove):
                links.remove(i)
            entry = links.add()
            entry.object_group_name = grp_name
            entry.light_name = light_name
            # Set link status
            entry.is_linked = bool(do_include)

        except Exception as e:
            pass

        finally:
            # restore selection
            bpy.ops.object.select_all(action='DESELECT')
            for o in original_selected:
                try: o.select_set(True)
                except Exception: pass
            context.view_layer.objects.active = original_active

            redraw_3d_areas()
            
    finally:
        scene[_FLAG_UPDATING] = False
        scene[_FLAG_GROUP_UPDATE] = False

class LUMI_ObjectGroupLinkStatus(bpy.types.PropertyGroup):    
    object_group_name: StringProperty()
    light_name: StringProperty()
    # Link status property
    is_linked: BoolProperty(default=False)

class LUMI_ObjectItem(bpy.types.PropertyGroup):
    name: StringProperty()
    
    def update_object_selected(self, context):
        """Update object selection in viewport when checkbox changes"""
        # # Access Blender object data
        obj = bpy.data.objects.get(self.name)
        if obj:
            try:
                obj.select_set(self.selected)
                # Update active object if this is the only selected object
                if self.selected and len([o for o in bpy.context.selected_objects]) == 1:
                    bpy.context.view_layer.objects.active = obj
            except (AttributeError, RuntimeError):
                # Ignore context errors during batch operations
                pass
    
    selected: BoolProperty(
        name="Selected",
        description="Object selected in viewport",
        default=False,
        update=update_object_selected
    )

class LUMI_ObjectGroup(bpy.types.PropertyGroup):
    name: StringProperty()
    objects: CollectionProperty(type=LUMI_ObjectItem)
    show_objects: BoolProperty(
        name="Show Objects",
        description="Show/hide objects in this group",
        default=False
    )

class LUMI_LightItem(bpy.types.PropertyGroup):
    name: StringProperty()
    marked: BoolProperty(default=False, update=light_item_marked_update)

class LUMI_LightGroup(bpy.types.PropertyGroup):
    name: StringProperty()
    lights: CollectionProperty(type=LUMI_LightItem)
    show_objects: BoolProperty(
        name="Show Lights",
        description="Show/hide lights in this group",
        default=True
    )

    def get_is_marked(self):
        """Get marked status - read-only property for display"""
        return all(item.marked for item in self.lights) and len(self.lights) > 0

    def set_is_marked(self, value):
        """Set marked status for linking - optimized for read-only groups"""
        # Use scene attributes for flags to avoid stale module globals on reload
        scene = bpy.context.scene

        # Prevent recursion when updating individual lights
        if getattr(scene, _FLAG_UPDATING, False):
            return

        scene[_FLAG_UPDATING] = True
        scene[_FLAG_GROUP_UPDATE] = True  # Mark this as a group update
        try:
            for item in self.lights:
                item.marked = value
        finally:
            scene[_FLAG_UPDATING] = False
            scene[_FLAG_GROUP_UPDATE] = False

    is_marked: BoolProperty(
        name="Link to Current Object Group",
        description="Link this light group to currently selected object group",
        get=get_is_marked,
        set=set_is_marked
    )

class LUMI_UnGroupedLightItem(bpy.types.PropertyGroup):
    name: StringProperty()
    # Marked status for light linking
    marked: BoolProperty(default=False, update=light_item_marked_update)

def get_valid_mesh_objects():
    return [obj for obj in bpy.data.objects if obj.type == 'MESH']

def get_valid_light_objects(context):
    """Get all light objects in LumiFlow collection and its children"""
    lights = []
    root_collection = lumi_get_light_collection(context.scene)
    
    # Get lights directly in root collection
    for obj in root_collection.objects:
        # Check if object is a light
        if obj.type == 'LIGHT':
            lights.append(obj)
    
    # Get lights in sub-collections
    for sub_col in root_collection.children:
        for obj in sub_col.objects:
            # Check if object is a light
            if obj.type == 'LIGHT':
                lights.append(obj)
    
    return lights

def redraw_3d_areas():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()


def get_light_groups_from_collections(context):
    root_collection = lumi_get_light_collection(context.scene)
    return [col for col in root_collection.children]

def get_default_lights(context):
    root_collection = lumi_get_light_collection(context.scene)
    default_lights = []
    
    sub_collection_objects = set()
    for sub_collection in root_collection.children:
        sub_collection_objects.update(obj.name for obj in sub_collection.objects)
    
    for obj in root_collection.objects:
        # Check if object is a light
        if obj.type == 'LIGHT' and obj.name not in sub_collection_objects:
            default_lights.append(obj)
    
    return default_lights

def get_grouped_object_names(exclude_default=True):
    grouped_names = set()
    for group in bpy.context.scene.lumi_object_groups:
        if exclude_default and group.name == DEFAULT_GROUP_NAME:
            continue
        grouped_names.update(item.name for item in group.objects)
    return grouped_names

def get_grouped_light_names(context):
    root_collection = lumi_get_light_collection(context.scene)
    grouped_names = set()
    for group in root_collection.children:
        grouped_names.update(obj.name for obj in group.objects)
    return grouped_names

def sync_light_groups_with_collections(scene):
    """Optimized sync for read-only light groups - only updates display data"""
    # Store current marked states before clearing
    marked_dict = {}
    for group in scene.lumi_light_groups:
        for item in group.lights:
            marked_dict[item.name] = item.marked

    scene.lumi_light_groups.clear()
    
    # Prevent recursion when setting marked states - this is system sync, not user action
    scene[_FLAG_UPDATING] = True
    scene[_FLAG_GROUP_UPDATE] = True  # Mark as system update
    try:
        # Optimized: Only create groups for display, don't modify collections
        root_collection = lumi_get_light_collection(scene)
        
        # Default group - all lights in root collection
        all_lights_in_root = [obj for obj in root_collection.objects if obj.type == 'LIGHT']
        
        if all_lights_in_root:
            default_group = scene.lumi_light_groups.add()
            default_group.name = DEFAULT_GROUP_NAME
            default_group.show_objects = True
            
            # Add lights to display group
            for light in all_lights_in_root:
                light_item = default_group.lights.add()
                light_item.name = light.name
                light_item.marked = marked_dict.get(light.name, False)
        
        # Sub-collection groups - read-only display
        for collection in root_collection.children:
            group = scene.lumi_light_groups.add()
            group.name = collection.name
            group.show_objects = True
            
            for obj in collection.objects:
                if obj.type == 'LIGHT':
                    light_item = group.lights.add()
                    light_item.name = obj.name
                    light_item.marked = marked_dict.get(obj.name, False)
    finally:
        scene[_FLAG_UPDATING] = False
        scene[_FLAG_GROUP_UPDATE] = False

def ensure_default_object_group(scene):
    default_group = next((g for g in scene.lumi_object_groups if g.name == DEFAULT_GROUP_NAME), None)
    if not default_group:
        default_group = scene.lumi_object_groups.add()
        default_group.name = DEFAULT_GROUP_NAME
    
    default_group.objects.clear()
    grouped_names = get_grouped_object_names(exclude_default=True)
    
    for obj in get_valid_mesh_objects():
        if obj.name not in grouped_names:
            obj_item = default_group.objects.add()
            obj_item.name = obj.name

def get_object_current_group(scene, object_name):
    """Get group where object currently belongs, return None if not found"""
    for group in scene.lumi_object_groups:
        for item in group.objects:
            if item.name == object_name:
                return group
    return None

def check_objects_in_groups(scene, object_names):
    """Check which objects are already in groups and return mapping object_name -> group_name"""
    object_to_group = {}
    for group in scene.lumi_object_groups:
        for item in group.objects:
            if item.name in object_names:
                object_to_group[item.name] = group.name
    return object_to_group

def remove_objects_from_all_groups(scene, object_names, exclude_group=None):
    """Remove objects from all groups except exclude_group"""
    removed_count = 0
    for group in scene.lumi_object_groups:
        if exclude_group and group == exclude_group:
            continue
            
        items_to_remove = []
        for i, item in enumerate(group.objects):
            if item.name in object_names:
                items_to_remove.append(i)
                removed_count += 1
        
        # Remove from back to avoid index issues
        for i in reversed(items_to_remove):
            group.objects.remove(i)
    
    return removed_count

def sync_ungrouped_lights(scene):
    """Optimized sync for ungrouped lights - read-only display"""
    # Use scene-scoped flags (avoid module-level globals)
    
    # Create context object for function calls
    context = bpy.context
    
    grouped_names = get_grouped_light_names(context)
    marked_dict = {item.name: item.marked for item in scene.lumi_un_grouped_lights}
    valid_light_objects = get_valid_light_objects(context)
    valid_lights = {obj.name for obj in valid_light_objects if obj.name not in grouped_names}
    
    ungrouped_lights = scene.lumi_un_grouped_lights
    ungrouped_lights.clear()
    
    # Prevent recursion when setting marked states - mark as a system/group update
    scene[_FLAG_UPDATING] = True
    scene[_FLAG_GROUP_UPDATE] = True
    try:
        for name in valid_lights:
            item = ungrouped_lights.add()
            item.name = name
            item.marked = marked_dict.get(name, False)
    finally:
        scene[_FLAG_UPDATING] = False
        scene[_FLAG_GROUP_UPDATE] = False

def sync_marked_with_links(scene):
    """Essential function for syncing marked states with link status"""
    # Use scene-scoped flags
    
    obj_groups = scene.lumi_object_groups
    obj_index = scene.lumi_object_groups_index
    
    if obj_index < 0 or obj_index >= len(obj_groups):
        return
        
    current_obj_group = obj_groups[obj_index]
    links = scene.lumi_object_group_link_status
    
    # Prevent recursion when syncing marked states - mark as a system/group update
    scene[_FLAG_UPDATING] = True
    scene[_FLAG_GROUP_UPDATE] = True
    try:
        for group in scene.lumi_light_groups:
            for item in group.lights:
                link_status = next((l for l in links 
                    if l.object_group_name == current_obj_group.name and l.light_name == item.name), None)
                item.marked = link_status.is_linked if link_status else False
    finally:
        scene[_FLAG_UPDATING] = False
        scene[_FLAG_GROUP_UPDATE] = False

def object_group_index_update(self, context):
    """Essential handler for object group selection changes"""
    sync_marked_with_links(context.scene)
    redraw_3d_areas()

def lumi_light_groups_update_handler(scene, depsgraph):
    """
    Optimized handler for light group updates in read-only mode
    - Only syncs display data when collections change
    - Minimal processing for performance
    """
    try:
        # Only sync if there are actual changes to avoid unnecessary updates
        if hasattr(scene, 'lumi_light_groups'):
            sync_light_groups_with_collections(scene)
            sync_ungrouped_lights(scene)
    except (AttributeError, RuntimeError):
        # Ignore context errors during batch operations
        pass

def depsgraph_update_default_group(scene, depsgraph=None):
    """
    Handler for updating default object groups when scene changes
    - Ensures default group is maintained when objects are added/removed
    - Compatible with both depsgraph_update_post and load_post handlers
    """
    try:
        if hasattr(scene, 'lumi_object_groups'):
            ensure_default_object_group(scene)
            # Also sync light groups to stay consistent
            sync_light_groups_with_collections(scene)
            sync_ungrouped_lights(scene)
    except (AttributeError, RuntimeError):
        # Ignore context errors during batch operations
        pass

def ensure_default_light_group(scene):
    """Simplified: Just sync display groups with collections"""
    sync_light_groups_with_collections(scene)

class LUMI_UL_object_groups(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Add property to UI
        layout.prop(item, "name", text="", emboss=False, icon='GROUP')

    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        default_indices = [i for i, item in enumerate(items) if item.name == DEFAULT_GROUP_NAME]
        other_indices = [i for i, item in enumerate(items) if item.name != DEFAULT_GROUP_NAME]
        indices = default_indices + other_indices
        filter_flags = [self.bitflag_filter_item] * len(items)
        return filter_flags, indices

class LUMI_UL_objects_in_group(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = bpy.data.objects.get(item.name)
        if obj and obj.type == 'MESH':
            # Create horizontal UI row
            row = layout.row(align=True)
            row.prop(item, "selected", text="")
            op = row.operator("lumi.select_object_from_group", 
                            text=item.name, icon='OUTLINER_OB_MESH', emboss=False)
            op.object_name = item.name
        else:
            layout.label(text=f"{item.name} (missing)", icon='ERROR')
    
    def filter_items(self, context, data, propname):
        items = getattr(data, propname)
        filtered = []
        indices = list(range(len(items)))
        
        for item in items:
            obj = bpy.data.objects.get(item.name)
            if obj and obj.type == 'MESH':
                filtered.append(self.bitflag_filter_item)
            else:
                filtered.append(0)
        
        return filtered, indices

class LUMI_UL_light_groups(bpy.types.UIList):
    """Optimized UIList for read-only light groups"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False, icon='LIGHT')

class LUMI_UL_lights_in_group(bpy.types.UIList):
    """Optimized UIList for lights in read-only groups"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        light_obj = bpy.data.objects.get(item.name)
        if light_obj and light_obj.type == 'LIGHT':
            row = layout.row(align=True)
            # Only show checkbox for linking, no selection controls
            row.prop(item, "marked", text="")
            row.label(text=item.name, icon='OUTLINER_OB_LIGHT')
        else:
            layout.label(text=f"{item.name} (missing)", icon='ERROR')

class LUMI_OT_add_group(bpy.types.Operator):
    bl_idname = "lumi.add_group"
    bl_label = "Add Object Group"
    bl_options = {'REGISTER', 'UNDO'}
    # Property for group name
    group_name: StringProperty(
        name="Group Name",
        description="Name for the new object group",
        default="New Group"
    )
    
    # Property to show warning if objects are already in other groups
    show_warning: BoolProperty(default=False)
    warning_message: StringProperty(default="")
    conflicted_objects: StringProperty(default="")

    def invoke(self, context, event):
        # Set default name based on existing group count
        scene = context.scene
        self.group_name = f"Group {len(scene.lumi_object_groups) + 1}"
        
        # Check selected objects and detect conflicts
        self._check_object_conflicts(context)
        
        return context.window_manager.invoke_props_dialog(self, width=300)

    def _check_object_conflicts(self, context):
        """Check if selected objects are already in other groups"""
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            self.show_warning = False
            return
            
        # Use utility function to check conflicts
        selected_names = [obj.name for obj in selected_meshes]
        object_to_group_map = check_objects_in_groups(context.scene, selected_names)
        
        # Filter out Default group - no warning needed for objects in Default group
        filtered_conflicts = {}
        for obj_name, group_name in object_to_group_map.items():
            if group_name != DEFAULT_GROUP_NAME:
                filtered_conflicts[obj_name] = group_name
        
        if filtered_conflicts:
            self.show_warning = True
            conflicted_objects = []
            
            for obj_name, group_name in filtered_conflicts.items():
                conflicted_objects.append(f"• {obj_name} (in '{group_name}')")
            
            self.conflicted_objects = "\n".join(conflicted_objects)
            count = len(conflicted_objects)
            self.warning_message = f"{count} object{'s' if count > 1 else ''} already in other group{'s' if count > 1 else ''}:"
        else:
            self.show_warning = False

    def draw(self, context):
        layout = self.layout
        
        # Input group name
        layout.prop(self, "group_name")
        
        # Show warning if there are conflicts
        if self.show_warning:
            layout.separator()
            
            # Warning message without alert
            warning_row = layout.row()
            warning_row.label(text=self.warning_message, icon='ERROR')
            
            # List objects in separate box with indent
            objects_box = layout.box()
            objects_col = objects_box.column()
            for line in self.conflicted_objects.split('\n'):
                if line.strip():
                    indent_row = objects_col.row()
                    indent_row.separator(factor=2)  # Indent to the right
                    indent_row.label(text=line)
            
            # Brief info
            layout.label(text="Objects will be moved to new group.")
            
            layout.separator()

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        
        # Validate group name is not empty
        if not self.group_name.strip():
            self.report({'ERROR'}, "Group name cannot be empty")
            return {'CANCELLED'}
        
        # Check if name already exists (except Default)
        existing_names = [group.name for group in scene.lumi_object_groups]
        if self.group_name in existing_names:
            self.report({'ERROR'}, f"Group name '{self.group_name}' already exists")
            return {'CANCELLED'}
        
        # Check and add selected mesh objects to new group
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            # Create empty group
            group = scene.lumi_object_groups.add()
            group.name = self.group_name.strip()
            scene.lumi_object_groups_index = len(scene.lumi_object_groups) - 1
            self.report({'INFO'}, f"Created empty group '{group.name}'")
            return {'FINISHED'}
        
        # Remove objects from other groups if any (one object = one group implementation)
        selected_names = [obj.name for obj in selected_meshes]
        removed_count = remove_objects_from_all_groups(scene, selected_names)
        
        # Create new group
        group = scene.lumi_object_groups.add()
        group.name = self.group_name.strip()
        scene.lumi_object_groups_index = len(scene.lumi_object_groups) - 1
        
        # Add objects to new group
        added_count = 0
        for obj in selected_meshes:
            obj_item = group.objects.add()
            obj_item.name = obj.name
            added_count += 1
        
        # Update default group to exclude objects already added to new group
        ensure_default_object_group(scene)
        redraw_3d_areas()
        
        # Generate result report
        if removed_count > 0:
            self.report({'INFO'}, f"Created group '{group.name}' with {added_count} object(s). Moved {removed_count} object(s) from other groups.")
        else:
            self.report({'INFO'}, f"Created group '{group.name}' with {added_count} selected object(s)")
        
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_remove_group(bpy.types.Operator):
    bl_idname = "lumi.remove_group"
    bl_label = "Remove Object Group"
    bl_options = {'INTERNAL'}

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        index = scene.lumi_object_groups_index
        
        if index >= 0 and index < len(scene.lumi_object_groups):
            group = scene.lumi_object_groups[index]
            if group.name == DEFAULT_GROUP_NAME:
                self.report({'WARNING'}, "Default group cannot be deleted.")
                # Cancel operation
                return {'CANCELLED'}
            
            # Get objects in group to be deleted
            objects_in_group = []
            for item in group.objects:
                obj = bpy.data.objects.get(item.name)
                if obj and obj.type == 'MESH':
                    objects_in_group.append(obj)
            
            # Save original selection state
            original_active = context.view_layer.objects.active
            original_selected = list(context.selected_objects)
            
            # Remove linking from all marked lights
            unlinked_count = 0
            
            # Collect all marked lights first
            marked_lights = []
            
            # Search in light groups
            for light_group in scene.lumi_light_groups:
                for light_item in light_group.lights:
                    if light_item.marked:
                        light_obj = bpy.data.objects.get(light_item.name)
                        if light_obj and light_obj.type == 'LIGHT':
                            marked_lights.append(light_obj)
            
            # Search in ungrouped lights
            for ungrouped_light in scene.lumi_un_grouped_lights:
                if ungrouped_light.marked:
                    light_obj = bpy.data.objects.get(ungrouped_light.name)
                    if light_obj and light_obj.type == 'LIGHT':
                        marked_lights.append(light_obj)
            
            # Process unlink for each marked light
            try:
                for light_obj in marked_lights:
                    if objects_in_group:  # Ensure there are objects in group
                        try:
                            # Use direct collection manipulation approach like reference function
                            # Light Linking collection name
                            link_coll_name = f"Light Linking for {light_obj.name}"
                            link_collection = bpy.data.collections.get(link_coll_name)
                            
                            if not link_collection:
                                print(f"❌ Light Linking collection '{link_coll_name}' not found. Skipping.")
                                continue
                            
                           # # Check if object is a light from Light Linking Collection
                            objects_removed = 0
                            for obj in objects_in_group:
                                # Use object name for checking and unlinking
                                if obj.name in [o.name for o in link_collection.objects]:
                                    link_collection.objects.unlink(obj)
                                    objects_removed += 1
                                    print(f"✅ Object '{obj.name}' removed from '{link_coll_name}'.")
                                else:
                                    print(f"ℹ Object '{obj.name}' not in '{link_coll_name}'.")
                            
                            if objects_removed > 0:
                                unlinked_count += 1
                                print(f"Successfully unlinked {light_obj.name} from {objects_removed} object(s)")
                            
                        except Exception as e:
                            self.report({'WARNING'}, f"Failed to unlink {light_obj.name}: {e}")
                            print(f"Error unlinking {light_obj.name}: {e}")
                                
            finally:
                # Restore original selection
                bpy.ops.object.select_all(action='DESELECT')
                for obj in original_selected:
                    if obj and obj.name in bpy.data.objects:
                        obj.select_set(True)
                if original_active and original_active.name in bpy.data.objects:
                    context.view_layer.objects.active = original_active
            
            # Remove internal link status for this group
            links = scene.lumi_object_group_link_status
            old_links = [i for i, l in enumerate(links) if l.object_group_name == group.name]
            for i in reversed(old_links):
                links.remove(i)
            
            # Remove group
            scene.lumi_object_groups.remove(index)
            scene.lumi_object_groups_index = max(0, index - 1)
            
            # Update default group
            ensure_default_object_group(scene)
            redraw_3d_areas()
            
            if unlinked_count > 0:
                self.report({'INFO'}, f"Removed group '{group.name}' and unlinked {unlinked_count} marked light(s)")
            else:
                self.report({'INFO'}, f"Removed group '{group.name}'")

        return {'FINISHED'}

class LUMI_OT_add_object_to_group(bpy.types.Operator):
    bl_idname = "lumi.add_object_to_group"
    bl_label = "Add Selected Objects to Group"
    bl_options = {'INTERNAL'}
    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        obj_groups = scene.lumi_object_groups
        obj_index = scene.lumi_object_groups_index
        
        if obj_index < 0 or obj_index >= len(obj_groups):
            self.report({'WARNING'}, "No object group selected.")
            # Cancel operation
            return {'CANCELLED'}
            
        obj_group = obj_groups[obj_index]
        # Get selected objects in scene
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected.")
            # Cancel operation
            return {'CANCELLED'}
        
        # Implementation of one object = one group: remove from other groups first
        selected_names = [obj.name for obj in selected_meshes]
        removed_count = remove_objects_from_all_groups(scene, selected_names, exclude_group=obj_group)
        
        # Add objects to target group
        existing_names = {item.name for item in obj_group.objects}
        added_count = 0
        
        for obj in selected_meshes:
            if obj.name not in existing_names:
                obj_item = obj_group.objects.add()
                obj_item.name = obj.name
                added_count += 1

        ensure_default_object_group(scene)
        redraw_3d_areas()
        
        # Generate result report
        if removed_count > 0:
            self.report({'INFO'}, f"Added {added_count} object(s) to {obj_group.name}. Moved {removed_count} object(s) from other groups.")
        else:
            message = f"Added {added_count} object(s) to {obj_group.name}" if added_count > 0 else \
                      "No new objects added (already in group)"
            self.report({'INFO'}, message)
        
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_remove_object_from_group(bpy.types.Operator):
    bl_idname = "lumi.remove_object_from_group"
    bl_label = "Remove Object from Group"
    bl_options = {'INTERNAL'}
    
    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        obj_index = scene.lumi_object_groups_index
        
        if obj_index < 0 or obj_index >= len(scene.lumi_object_groups):
            # Cancel operation
            return {'CANCELLED'}
            
        obj_group = scene.lumi_object_groups[obj_index]
        to_remove = [i for i, item in enumerate(obj_group.objects) if item.selected]
        
        for i in reversed(to_remove):
            obj_group.objects.remove(i)
            
        self.report({'INFO'}, f"Removed {len(to_remove)} checked object(s)")
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_sync_object_selection(bpy.types.Operator):
    """Synchronize checkbox states with viewport selection"""
    bl_idname = "lumi.sync_object_selection"
    bl_label = "Sync Selection"
    bl_options = {'INTERNAL'}

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        selected_objects = set(obj.name for obj in context.selected_objects if obj.type == 'MESH')
        
        # Update all object groups
        for group in scene.lumi_object_groups:
            for item in group.objects:
                try:
                    # Update checkbox to match viewport selection
                    current_state = item.name in selected_objects
                    item.selected = current_state
                except AttributeError:
                    # Skip items that don't have the selected property
                    continue
                
        self.report({'INFO'}, "Selection synchronized")
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_select_object_from_group(bpy.types.Operator):
    bl_idname = "lumi.select_object_from_group"
    bl_label = "Select Object"
    bl_options = {'INTERNAL'}
    
    object_name: StringProperty()
    
    # # Main method for operator execution
    def execute(self, context):
        # # Access Blender object data
        obj = bpy.data.objects.get(self.object_name)
        if obj:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            self.report({'INFO'}, f"Selected {self.object_name}")
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_toggle_select_all_objects_in_group(bpy.types.Operator):
    bl_idname = "lumi.toggle_select_all_objects_in_group"
    bl_label = "Toggle Select All Objects"
    bl_options = {'INTERNAL'}

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        obj_index = scene.lumi_object_groups_index
        
        if obj_index < 0 or obj_index >= len(scene.lumi_object_groups):
            # Cancel operation
            return {'CANCELLED'}
            
        obj_group = scene.lumi_object_groups[obj_index]
        all_selected = all(item.selected for item in obj_group.objects)
        
        for item in obj_group.objects:
            item.selected = not all_selected
            
        # Complete operation successfully
        return {'FINISHED'}

# ============================================================================
# OPERATORS - Light Groups
# ============================================================================

# # DEPRECATED: Light groups are now read-only, managed through collections only
# This operator is kept for compatibility but disabled
class LUMI_OT_add_light_group(bpy.types.Operator):
    bl_idname = "lumi.add_light_group"
    bl_label = "Add Light Group (Disabled)"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        self.report({'INFO'}, "Light groups are now read-only. Manage lights through collections.")
        return {'CANCELLED'}

# # DEPRECATED: Light groups are now read-only, managed through collections only
class LUMI_OT_remove_light_group(bpy.types.Operator):
    bl_idname = "lumi.remove_light_group"
    bl_label = "Remove Light Group (Disabled)"
    bl_options = {'INTERNAL'}

    group_name: StringProperty()

    def execute(self, context):
        self.report({'INFO'}, "Light groups are now read-only. Manage lights through collections.")
        return {'CANCELLED'}

# # DEPRECATED: Light groups are now read-only, managed through collections only
class LUMI_OT_add_light_to_group(bpy.types.Operator):
    bl_idname = "lumi.add_light_to_group"
    bl_label = "Add Light to Group (Disabled)"
    bl_options = {'INTERNAL'}
    
    group_name: StringProperty()

    def execute(self, context):
        self.report({'INFO'}, "Light groups are now read-only. Manage lights through collections.")
        return {'CANCELLED'}

# # DEPRECATED: Light groups are now read-only, managed through collections only
class LUMI_OT_remove_light_from_group(bpy.types.Operator):
    bl_idname = "lumi.remove_light_from_group"
    bl_label = "Remove Light from Group (Disabled)"
    bl_options = {'INTERNAL'}

    group_name: StringProperty()
    light_name: StringProperty()

    def execute(self, context):
        self.report({'INFO'}, "Light groups are now read-only. Manage lights through collections.")
        return {'CANCELLED'}

# Class definition for Operator
class LUMI_OT_select_un_grouped_light(bpy.types.Operator):
    bl_idname = "lumi.select_un_grouped_light"
    bl_label = "Select/Deselect Light"
    bl_options = {'INTERNAL'}

    light_name: StringProperty()

    # # Main method for operator execution
    def execute(self, context):
        # # Access Blender object data
        obj = bpy.data.objects.get(self.light_name)
        # # Check if object is a light
        if obj and obj.type == 'LIGHT':
            new_state = not obj.select_get()
            obj.select_set(new_state)
            if new_state:
                context.view_layer.objects.active = obj
        # Report the result
        self.report({'INFO'}, f"{'Selected' if new_state else 'Unselected'} {self.light_name}")
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_select_light_from_group(bpy.types.Operator):
    bl_idname = "lumi.select_light_from_group"
    bl_label = "Select Light"
    bl_options = {'INTERNAL'}

    light_name: StringProperty()

    # # Main method for operator execution
    def execute(self, context):
        # # Access Blender object data
        light_obj = bpy.data.objects.get(self.light_name)
        # # Check if object is a light
        if light_obj and light_obj.type == 'LIGHT':
            new_state = not light_obj.select_get()
            light_obj.select_set(new_state)
            if new_state:
                context.view_layer.objects.active = light_obj
            self.report({'INFO'}, f"{'Selected' if new_state else 'Unselected'} {self.light_name}")
        # Complete operation successfully
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_toggle_select_all_lights_in_group(bpy.types.Operator):
    bl_idname = "lumi.toggle_select_all_lights_in_group"
    bl_label = "Toggle Select All Lights"
    bl_options = {'INTERNAL'}

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        light_index = scene.lumi_light_groups_index
        
        if light_index < 0 or light_index >= len(scene.lumi_light_groups):
            # Cancel operation
            return {'CANCELLED'}
            
        light_group = scene.lumi_light_groups[light_index]
        all_selected = all(item.selected for item in light_group.lights)
        
        for item in light_group.lights:
            item.selected = not all_selected
            
        # Complete operation successfully
        return {'FINISHED'}

# ============================================================================
# LIGHT LINKING OPERATOR
# ============================================================================
class LUMI_MT_group_actions(bpy.types.Menu):
    bl_label = "Group Actions"
    bl_idname = "LUMI_MT_group_actions"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        group_name = scene.get("lumi_temp_group_name", "")
        if not group_name:
            layout.label(text="(no group)", icon='ERROR')
            return        
        col = layout.column(align=True)
        op_inc = col.operator("lumi.update_light_linking", text="Include")
        op_inc.group_name = group_name
        op_inc.force_state = 'INCLUDE'
        op_exc = col.operator("lumi.update_light_linking", text="Exclude")
        op_exc.group_name = group_name
        op_exc.force_state = 'EXCLUDE'

# Class definition for Operator
class LUMI_OT_update_light_linking(bpy.types.Operator):
    bl_idname = "lumi.update_light_linking"
    bl_label = "Update Object Group Linking"
    bl_options = {'INTERNAL'}

    # Property to specify which group to process (optional - falls back to scene index)
    group_name: StringProperty(
        name="Group Name",
        description="Name of the group to process",
        default=""
    )

    # new: allow forcing action from menu (INCLUDE / EXCLUDE / "" for toggle)
    force_state: StringProperty(
        name="Force State",
        description="Force include/exclude (INCLUDE/EXCLUDE) or empty for toggle",
        default=""
    )
# ...existing code...
    def execute(self, context):
        scene = context.scene
        obj_groups = scene.lumi_object_groups

        # Determine current_obj_group:
        current_obj_group = None
        # Priority: if operator is called from menu with group_name, use that
        if getattr(self, "group_name", ""):
            current_obj_group = next((g for g in obj_groups if g.name == self.group_name), None)
            if not current_obj_group:
                self.report({'WARNING'}, f"Object group '{self.group_name}' not found")
                return {'CANCELLED'}
        else:
            # fallback to index selected on scene
            idx = getattr(scene, "lumi_object_groups_index", -1)
            if idx >= 0 and idx < len(obj_groups):
                current_obj_group = obj_groups[idx]
            else:
                self.report({'WARNING'}, "No object group selected")
                return {'CANCELLED'}

        # Get receiver objects from current group
        receiver_objects = []
        for item in current_obj_group.objects:
            obj = bpy.data.objects.get(item.name)
            if obj and obj.type == 'MESH':
                receiver_objects.append(obj)

        if not receiver_objects:
            self.report({'WARNING'}, "No valid mesh objects found in the group.")
            return {'CANCELLED'}

        # Get selected lights from viewport (not marked lights)
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']

        if not selected_lights:
            self.report({'WARNING'}, "No lights selected in viewport.")
            return {'CANCELLED'}

        # Check existing links BEFORE clearing to determine toggle state
        links = scene.lumi_object_group_link_status
        selected_light_names = {light.name for light in selected_lights}

        # Store existing link states for toggle logic
        existing_link_states = {}
        for light in selected_lights:
            existing_link = next((l for l in links
                                if l.object_group_name == current_obj_group.name and l.light_name == light.name), None)
            existing_link_states[light.name] = existing_link.is_linked if existing_link else False

        # Now clear old links for this group, but only for selected lights
        old_links = [i for i, l in enumerate(links)
                    if l.object_group_name == current_obj_group.name and l.light_name in selected_light_names]
        for i in reversed(old_links):
            links.remove(i)

        # Save selection state
        original_active = context.view_layer.objects.active
        original_selected = list(context.selected_objects)

        updated_count = 0

        try:
            # Process each selected light with ALL objects in the group
            for light_obj in selected_lights:
                # FORCE via menu property takes precedence
                if self.force_state == 'INCLUDE':
                    link_state = 'INCLUDE'
                    is_linked = True
                    action_text = "Linked"
                elif self.force_state == 'EXCLUDE':
                    link_state = 'EXCLUDE'
                    is_linked = False
                    action_text = "Excluded"
                else:
                    # Toggle logic based on stored existing state
                    was_linked = existing_link_states.get(light_obj.name, False)
                    if was_linked:
                        link_state = 'EXCLUDE'
                        is_linked = False
                        action_text = "Excluded"
                    else:
                        link_state = 'INCLUDE'
                        is_linked = True
                        action_text = "Linked"

                # Add/Update internal links for tracking
                link = links.add()
                link.object_group_name = current_obj_group.name
                link.light_name = light_obj.name
                link.is_linked = is_linked

                # Clear selection first
                bpy.ops.object.select_all(action='DESELECT')

                # Select ALL receiver objects in the group
                for obj in receiver_objects:
                    obj.select_set(True)

                # Select the light and make it active
                light_obj.select_set(True)
                context.view_layer.objects.active = light_obj

                try:
                    bpy.ops.object.light_linking_receivers_link(link_state=link_state)
                    updated_count += 1
                    print(f"✅ {action_text} {light_obj.name} {'to' if is_linked else 'from'} {len(receiver_objects)} objects in group '{current_obj_group.name}'")
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to {action_text.lower()} {light_obj.name}: {e}")
                    print(f"❌ Error {action_text.lower()} {light_obj.name}: {e}")

        finally:
            # Restore selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                if obj and obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                context.view_layer.objects.active = original_active

        self.report({'INFO'}, f"Toggled {updated_count} selected lights with ALL {len(receiver_objects)} objects in group '{current_obj_group.name}'")
        return {'FINISHED'}

# Class definition for Operator
class LUMI_OT_quick_link_to_target(bpy.types.Operator): 
    """Quick Link: Select light/mesh, press keymap - if light: toggle linking mode, if mesh: show group menu"""
    bl_idname = "lumi.quick_link_to_target"
    bl_label = "Quick Link to Target Object"
    bl_options = {'REGISTER', 'UNDO'}

    target_object_name: StringProperty(default="")
    selected_lights: CollectionProperty(type=bpy.types.PropertyGroup)
    
    @classmethod
    def poll(cls, context):
        return lumi_is_addon_enabled()

    def invoke(self, context, event):
        """Start operation based on selected object type"""
        
        # 1. Check if LumiFlow addon is enabled
        if not lumi_is_addon_enabled():
            self.report({'ERROR'}, "LumiFlow addon is not enabled")
            return {'CANCELLED'}
        
        # 2. Check what is selected
        selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        # 3. Ensure only one type of object is selected (not both)
        if selected_lights and selected_meshes:
            self.report({'WARNING'}, "Please select only lights OR mesh objects, not both")
            return {'CANCELLED'}
        
        # 4. If lights are selected, enter modal mode directly
        if selected_lights:
            # Store selected lights for modal mode
            self.selected_lights.clear()
            for light in selected_lights:
                item = self.selected_lights.add()
                item.name = light.name
            
            # Start modal for target selection
            context.window_manager.modal_handler_add(self)
            self.report({'INFO'}, f"Quick Link Mode Active: Click mesh objects to toggle linking for {len(selected_lights)} light(s). Press X to exit, ESC to cancel.")
            return {'RUNNING_MODAL'}
        
        # 5. If meshes are selected, show group menu for meshes
        elif selected_meshes:
            return self.show_object_group_menu(context)
        else:
            self.report({'WARNING'}, "Select lights for linking mode or mesh objects for group assignment")
            return {'CANCELLED'}
    
    def show_object_group_menu(self, context):
        """Show menu to select object group"""
        def draw_menu(self, context):
            layout = self.layout
            scene = context.scene
            
            # Option 1: Create new group
            # Use INVOKE_DEFAULT to force dialog to appear
            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("lumi.add_group", text="Create New Group", icon='ADD')
            
            # Separator
            layout.separator()
            
            # Option 2: Add to existing groups (exclude default)
            existing_groups = [group for group in scene.lumi_object_groups 
                             if group.name != DEFAULT_GROUP_NAME]
            
            if existing_groups:
                layout.separator()
                for group in existing_groups:
                    row = layout.row()
                    row.operator("lumi.add_object_to_group", text=f"• {group.name}", icon='GROUP')
            else:
                layout.label(text="No existing groups available", icon='INFO')
        
        # Show popup menu
        context.window_manager.popup_menu(draw_menu, title="Add Objects to Group", icon='GROUP')
        return {'FINISHED'}
    
    def show_object_light_menu(self, context):
        """Show menu to select object group"""
        def draw_menu(menu_self, context):
            layout = menu_self.layout
            scene = context.scene

            existing_groups = [group for group in scene.lumi_object_groups
                                if group.name != DEFAULT_GROUP_NAME]

            if existing_groups:
                layout.separator()
                for group in existing_groups:
                    # Determine if the group contains any valid mesh objects
                    has_mesh = False
                    for item in group.objects:
                        obj = bpy.data.objects.get(item.name)
                        if obj and obj.type == 'MESH':
                            has_mesh = True
                            break

                    col = layout.column(align=True)
                    if not has_mesh:
                        col.enabled = False

                    # Create unique menu class for each group to avoid race condition
                    menu_id = f"LUMI_MT_group_actions_{group.name.replace(' ', '_')}"
                    
                    # Create menu class dynamically for this specific group
                    if not hasattr(bpy.types, menu_id):
                        # Create new menu class with captured group name
                        group_name_captured = group.name  # Capture current value
                        
                        def create_menu_class(captured_name):
                            class DynamicGroupMenu(bpy.types.Menu):
                                bl_label = "Group Actions"
                                bl_idname = menu_id
                                
                                def draw(self, context):
                                    layout = self.layout
                                    col = layout.column(align=True)
                                    op_inc = col.operator("lumi.update_light_linking", text="Include")
                                    op_inc.group_name = captured_name
                                    op_inc.force_state = 'INCLUDE'
                                    op_exc = col.operator("lumi.update_light_linking", text="Exclude")
                                    op_exc.group_name = captured_name
                                    op_exc.force_state = 'EXCLUDE'
                            return DynamicGroupMenu
                        
                        # Register the new menu class and track it
                        menu_class = create_menu_class(group_name_captured)
                        bpy.utils.register_class(menu_class)
                        _dynamic_menu_classes.append(menu_class)
                    
                    # Use the unique menu for this group
                    col.menu(menu_id, text=f"{group.name}", icon='GROUP')

            else:
                layout.label(text="No existing groups available", icon='INFO')

        context.window_manager.popup_menu(draw_menu, title="Select Reciver Group")
        return {'FINISHED'}


    def modal(self, context, event):
        """Handle mouse click for target selection"""
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get object under mouse
            target_obj = self.get_object_under_mouse(context, event)
            
            if target_obj and target_obj.type == 'MESH':
                self.target_object_name = target_obj.name
                result = self.execute_quick_link(context)
                # Don't return FINISHED - keep modal active for more clicks
                self.report({'INFO'}, f"Quick Link applied to '{target_obj.name}'. Click another object or press X to exit.")
                return {'RUNNING_MODAL'}
            else:
                self.report({'WARNING'}, "Click on a mesh object to create/toggle linking")
                return {'RUNNING_MODAL'}
            
        elif event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            # Right click works without needing to be on mesh object
            return self.show_object_light_menu(context)
        
        elif event.type == 'ESC' and event.value == 'PRESS':
            self.report({'INFO'}, "Quick link mode cancelled")
            return {'CANCELLED'}
        elif event.type == 'X' and event.value == 'RELEASE':
            self.report({'INFO'}, "Quick link mode exited")
            return {'FINISHED'}
            
        return {'RUNNING_MODAL'}

    def get_object_under_mouse(self, context, event):
        """Get object under mouse cursor"""
        # Convert mouse coordinates to region coordinates
        coord = (event.mouse_region_x, event.mouse_region_y)
        
        # Perform ray casting
        try:
            # Get 3D viewport region
            region = None
            region_3d = None
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for reg in area.regions:
                        if reg.type == 'WINDOW':
                            region = reg
                            for space in area.spaces:
                                if space.type == 'VIEW_3D':
                                    region_3d = space.region_3d
                                    break
                            break
                    break
            
            if not region or not region_3d:
                return None
                
            # Get mouse position in 3D space
            from bpy_extras import view3d_utils
            
            # Get ray direction and origin
            view_vector = view3d_utils.region_2d_to_vector_3d(region, region_3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, region_3d, coord)
            
            # Perform ray cast
            depsgraph = context.evaluated_depsgraph_get()
            result, location, normal, index, obj, matrix = context.scene.ray_cast(depsgraph, ray_origin, view_vector)
            
            return obj if result else None
            
        except Exception as e:
            print(f"Ray casting error: {e}")
            # Fallback: return active object if it's a mesh
            if context.active_object and context.active_object.type == 'MESH':
                return context.active_object
            return None
    
    def execute_quick_link(self, context):
        """Execute the quick linking process"""
        if not self.target_object_name:
            return {'CANCELLED'}
            
        scene = context.scene
        target_obj_name = self.target_object_name
        
        # 1. Check/Create object group with target object name
        target_group = None
        group_index = -1
        
        # Find existing group with same name
        for i, group in enumerate(scene.lumi_object_groups):
            if group.name == target_obj_name:
                target_group = group
                group_index = i
                break
        
        # Create new group if not found
        if not target_group:
            # Ensure object is removed from any existing group first
            remove_objects_from_all_groups(scene, [target_obj_name])

            target_group = scene.lumi_object_groups.add()
            target_group.name = target_obj_name
            group_index = len(scene.lumi_object_groups) - 1

            # Add target object to the new group
            obj_item = target_group.objects.add()
            obj_item.name = target_obj_name

            self.report({'INFO'}, f"Created new group '{target_obj_name}'")
        else:
            # Check if target object is in the group
            existing_names = {item.name for item in target_group.objects}
            if target_obj_name not in existing_names:
                # Remove object from other groups (exclude this target group)
                remove_objects_from_all_groups(scene, [target_obj_name], exclude_group=target_group)

                obj_item = target_group.objects.add()
                obj_item.name = target_obj_name
        
        # Set as current group
        scene.lumi_object_groups_index = group_index
        
        # 2. Toggle mark status for selected lights
        toggled_lights = []
        
        for light_info in self.selected_lights:
            light_name = light_info.name
            found = False
            
            # Find light in light groups and toggle marked status
            for light_group in scene.lumi_light_groups:
                for light_item in light_group.lights:
                    if light_item.name == light_name:
                        # Toggle marked status
                        light_item.marked = not light_item.marked
                        status = "linked" if light_item.marked else "excluded"
                        toggled_lights.append(f"{light_name} ({status})")
                        found = True
                        break
                if found:
                    break
        
        if not toggled_lights:
            self.report({'WARNING'}, "No lights found in light groups")
            return {'CANCELLED'}
        
        # 3. Update light linking only for selected lights
        receiver_objects = []
        for item in target_group.objects:
            obj = bpy.data.objects.get(item.name)
            if obj and obj.type == 'MESH':
                receiver_objects.append(obj)

        if not receiver_objects:
            self.report({'WARNING'}, "No valid mesh objects found in the group.")
            return {'CANCELLED'}

        # Clear old links for this group, but only for selected lights
        links = scene.lumi_object_group_link_status
        selected_light_names = {light_info.name for light_info in self.selected_lights}
        old_links = [i for i, l in enumerate(links) 
                    if l.object_group_name == target_group.name and l.light_name in selected_light_names]
        for i in reversed(old_links):
            links.remove(i)

        # Save selection state
        original_active = context.view_layer.objects.active
        original_selected = list(context.selected_objects)

        updated_count = 0

        try:
            # Process only lights that are in selected_lights
            for light_info in self.selected_lights:
                light_name = light_info.name
                light_obj = bpy.data.objects.get(light_name)
                
                if not light_obj or light_obj.type != 'LIGHT':
                    continue

                # Find marked status from light groups
                light_marked = False
                for light_group in scene.lumi_light_groups:
                    for light_item in light_group.lights:
                        if light_item.name == light_name:
                            light_marked = light_item.marked
                            break
                    if light_marked:
                        break

                link_state = 'INCLUDE' if light_marked else 'EXCLUDE'

                # Add to internal links if marked
                if light_marked:
                    link = links.add()
                    link.object_group_name = target_group.name
                    link.light_name = light_name
                    link.is_linked = True

                # Perform linking/unlinking for this light
                bpy.ops.object.select_all(action='DESELECT')

                for obj in receiver_objects:
                    obj.select_set(True)

                light_obj.select_set(True)
                context.view_layer.objects.active = light_obj

                try:
                    bpy.ops.object.light_linking_receivers_link(link_state=link_state)
                    updated_count += 1
                except Exception as e:
                    self.report({'WARNING'}, f"Failed {link_state} {light_obj.name}: {e}")

        finally:
            # Restore selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                if obj and obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                context.view_layer.objects.active = original_active

        # Update default group to exclude objects now in custom groups
        ensure_default_object_group(scene)
        redraw_3d_areas()

        # Report results
        light_list = ", ".join(toggled_lights)
        self.report({'INFO'}, f"Quick Link: {light_list} → '{target_obj_name}' group")
        
        return {'FINISHED'}

    def execute(self, context):
        """Direct execution (fallback)"""
        if not self.target_object_name:
            self.report({'WARNING'}, "Use Ctrl+Shift+Z to start quick link mode")
            return {'CANCELLED'}
        return self.execute_quick_link(context)   

# Class definition for Operator
class LUMI_OT_clear_light_linking(bpy.types.Operator):
    bl_idname = "lumi.clear_light_linking"
    bl_label = "Clear All Light Linking"
    bl_options = {'INTERNAL'}

    # # Main method for operator execution
    def execute(self, context):
        scene = context.scene
        links = scene.lumi_object_group_link_status
        links.clear()
        self.report({'INFO'}, "All light linking cleared.")
        # Complete operation successfully
        return {'FINISHED'}



def draw_advanced_linking_ui(layout, context):
    """
    Optimized light linking UI for read-only light groups
    - Light groups are now managed through collections only
    - UI focuses on linking display and control, not group management
    """
    scene = context.scene
    
    # Direct display without header and dropdown
    content_box = layout.box()
    try:
        # Split into logical sections
        _draw_receiver_groups(content_box, scene)
        content_box.separator()
        _draw_emitter_section(content_box, scene)
        
    except (AttributeError, RuntimeError):
        content_box.label(text="Error accessing linking data", icon='ERROR')

def _draw_receiver_groups(layout, scene):
    """Receiver groups with improved error handling - optimized for read-only"""
    box = layout.box()
    box.label(text="Receiver Groups", icon='GROUP')
    
    try:
        # Check if properties exist and initialize if needed
        if not hasattr(scene, 'lumi_object_groups'):
            box.label(text="Object groups not available", icon='INFO')
            return
        
        # Ensure index exists    
        if not hasattr(scene, 'lumi_object_groups_index'):
            box.label(text="Object groups index not available", icon='INFO')
            return
        
        # Create horizontal layout: list on left, buttons on right
        row = box.row()
        
        # Left side - template list
        list_col = row.column()
        if len(scene.lumi_object_groups) > 0:
            if LUMI_UL_object_groups is not None:
                list_col.template_list(
                    "LUMI_UL_object_groups", "",
                    scene, "lumi_object_groups",
                    scene, "lumi_object_groups_index",
                    rows=3
                )
            else:
                # Fallback display if UIList class is not available
                for i, group in enumerate(scene.lumi_object_groups):
                    row_item = list_col.row()
                    if i == scene.lumi_object_groups_index:
                        row_item.alert = True
                    row_item.label(text=group.name, icon='GROUP')
        else:
            list_col.label(text="No object groups", icon='INFO')
        
        # Right side - action buttons
        btn_col = row.column(align=True)
        btn_col.operator_context = 'INVOKE_DEFAULT'
        btn_col.operator("lumi.add_group", text="", icon='ADD')
        btn_col.operator("lumi.remove_group", text="", icon='REMOVE')
        
        # Show/hide toggle
        if hasattr(scene, 'lumi_show_objects_in_group'):
            btn_col.prop(scene, "lumi_show_objects_in_group", text="", 
                       icon='HIDE_OFF' if scene.lumi_show_objects_in_group else 'HIDE_ON')
            
            if scene.lumi_show_objects_in_group and len(scene.lumi_object_groups) > 0:
                _draw_objects_in_group(layout, scene)
        else:
            btn_col.label(text="", icon='HIDE_ON')
            
    except (AttributeError, RuntimeError) as e:
        box.label(text="Error accessing receiver groups", icon='ERROR')
        box.label(text=f"Details: {str(e)[:50]}...", icon='INFO')

def _draw_objects_in_group(layout, scene):
    """Objects in selected group"""
    try:
        group_count = len(scene.lumi_object_groups)
        if scene.lumi_object_groups_index < 0 or scene.lumi_object_groups_index >= group_count:
            return
            
        current_group = scene.lumi_object_groups[scene.lumi_object_groups_index]
        box = layout.box()
        
        if current_group.name == DEFAULT_GROUP_NAME:
            _draw_default_group_objects(box, current_group)
        else:
            _draw_custom_group_objects(box, current_group)
            
    except (AttributeError, RuntimeError, IndexError):
        layout.label(text="Error displaying group objects", icon='ERROR')

def _draw_default_group_objects(box, group):
    """Default group object display"""
    try:
        split = box.split(factor=0.85)
        col_list = split.column(align=True)
        col_btn = split.column(align=True)
        
        col_list.label(text=f"Objects in: {group.name}")
        
        if group.objects:
            for item in group.objects:
                obj = bpy.data.objects.get(item.name)
                icon = 'OUTLINER_OB_MESH' if obj and obj.type == 'MESH' else 'ERROR'
                row = col_list.row(align=True)
                row.prop(item, "selected", text="")
                row.label(text=item.name, icon=icon)
        else:
            col_list.label(text="(Empty)", icon='INFO')
        
        btn_row = col_btn.row(align=True)
        btn_row.alignment = 'RIGHT'
        btn_row.operator("lumi.toggle_select_all_objects_in_group", 
                       text="", icon='RESTRICT_SELECT_OFF')
                       
    except (AttributeError, RuntimeError):
        box.label(text="Error accessing group objects", icon='ERROR')

def _draw_custom_group_objects(box, group):
    """Custom group object display"""
    try:
        split = box.split(factor=0.85)
        col_list = split.column(align=True)
        col_btn = split.column(align=True)

        col_list.label(text=f"Objects in: {group.name}")

        if group.objects:
            for item in group.objects:
                obj = bpy.data.objects.get(item.name)
                icon = 'OUTLINER_OB_MESH' if obj and obj.type == 'MESH' else 'ERROR'
                row = col_list.row(align=True)
                
                # Simple checkbox without highlight
                row.prop(item, "selected", text="")
                
                # Object name without highlight
                row.label(text=item.name, icon=icon)
                
        else:
            col_list.label(text="Select objects → click +")
        # Action buttons
        group_buttons = [
            ("lumi.add_object_to_group", 'ADD', "Add selected objects"),
            ("lumi.remove_object_from_group", 'REMOVE', "Remove selected objects"),
            ("lumi.toggle_select_all_objects_in_group", 'RESTRICT_SELECT_OFF', "Toggle select all")
        ]
        
        for op_name, icon, tooltip in group_buttons:
            btn_row = col_btn.row(align=True)
            btn_row.alignment = 'RIGHT'
            op = btn_row.operator(op_name, text="", icon=icon)
            # Add tooltips if operator supports it
            
    except (AttributeError, RuntimeError):
        box.label(text="Error accessing group objects", icon='ERROR')

def _draw_emitter_section(layout, scene):
    """
    Optimized emitter section for read-only light groups
    - Removed group management buttons since groups are read-only
    - Focus on display and linking controls only
    """
    try:
        box = layout.box()
        header_row = box.row(align=True)
        header_row.label(text="Light Emitters (Read-Only Groups)", icon='LIGHT')

        col = box.column(align=True)

        # Draw custom light groups first
        custom_groups = [g for g in scene.lumi_light_groups if g.name != DEFAULT_GROUP_NAME]
        for group in custom_groups:
            _draw_light_group_readonly(col, group, scene)
            col.separator(factor=0.5)

        # Draw default group last
        default_group = next((g for g in scene.lumi_light_groups 
                            if g.name == DEFAULT_GROUP_NAME), None)
        if default_group:
            if custom_groups:  # Add separator if there are custom groups
                col.separator()
            _draw_default_light_group_readonly(col, default_group)
            
    except (AttributeError, RuntimeError):
        box.label(text="Error accessing light groups", icon='ERROR')

def _draw_light_group_readonly(col, group, scene):
    """
    Optimized light group display for read-only groups
    - Removed management buttons (add, delete, etc.)
    - Only shows linking controls and group info
    """
    try:
        # Group header - simplified for read-only
        row = col.row(align=True)
        row.prop(group, "is_marked", text="")
        row.label(text=f"{group.name} (Collection)", icon='OUTLINER_COLLECTION')
        
        # Toggle visibility only (no management buttons)
        show_btn = row.operator("wm.context_toggle", text="", 
                              icon='HIDE_OFF' if group.show_objects else 'HIDE_ON')
        group_index = next(i for i, g in enumerate(scene.lumi_light_groups) 
                         if g.name == group.name)
        show_btn.data_path = f'scene.lumi_light_groups[{group_index}].show_objects'

        # Show lights in group if expanded - read-only
        if group.show_objects:
            for light_item in group.lights:
                _draw_light_in_group_readonly(col, light_item)
                
    except (AttributeError, RuntimeError):
        pass

def _draw_light_in_group_readonly(col, light_item):
    """
    Optimized light display for read-only groups
    - Removed remove button since groups are managed through collections
    - Only shows linking checkbox and light info
    """
    row = col.row(align=True)
    row.separator(factor=4)  # Indent
    
    row.prop(light_item, "marked", text="")
    
    icon = 'OUTLINER_OB_LIGHT' if light_item.marked else 'LIGHT'
    row.label(text=light_item.name, icon=icon)
    
    # Info: Light is managed through collections
    row.label(text="", icon='INFO')

def _draw_default_light_group_readonly(col, default_group):
    """
    Optimized default light group for read-only system
    - Simplified display focusing on linking only
    """
    try:
        if not default_group.lights:
            col.label(text="No lights available", icon='INFO')
            return
            
        for light_item in default_group.lights:
            row = col.row(align=True)
            row.prop(light_item, "marked", text="")
            
            light_obj = bpy.data.objects.get(light_item.name) 
            is_selected = light_obj and light_obj.select_get()
            label_icon = 'OUTLINER_OB_LIGHT' if is_selected else 'LIGHT'
            
            row.label(text=light_item.name, icon=label_icon)
            
    except (AttributeError, RuntimeError):
        pass

# DEPRECATED: Original functions kept for compatibility but not used in read-only mode
def _draw_light_group(col, group, scene):
    """DEPRECATED: Original light group display with management buttons"""
    pass

def _draw_light_in_group(col, light_item, group_name):
    """DEPRECATED: Original light display with remove button"""
    pass

def _draw_default_light_group(col, default_group):
    """DEPRECATED: Original default group display"""
    pass

def cleanup_dynamic_menu_classes():
    """Clean up dynamically created menu classes"""
    global _dynamic_menu_classes
    for menu_class in _dynamic_menu_classes:
        try:
            bpy.utils.unregister_class(menu_class)
        except:
            pass  # Ignore if already unregistered
    _dynamic_menu_classes.clear()