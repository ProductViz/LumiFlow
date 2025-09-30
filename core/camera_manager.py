# SPDX-License-Identifier: GPL-3.0-or-later
#
# LumiFlow - Smart lighting tools for Blender
# Copyright (C) 2024 LumiFlow Developer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Camera Manager Module
Manages camera-light relationships and visibility control for LumiFlow.
Provides singleton pattern implementation for camera-based light management.
"""
import bpy
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# Global singleton instance
_camera_light_manager_instance = None

def get_camera_light_manager():
    """Get singleton instance of CameraLightManager"""
    global _camera_light_manager_instance
    if _camera_light_manager_instance is None:
        _camera_light_manager_instance = CameraLightManager()
    return _camera_light_manager_instance

class CameraLightManager:
    """Manager for camera-based light visibility system"""
    
    def __init__(self):
        self.camera_light_assignments = defaultdict(list)  # {camera_name: [light_names]}
        self.original_light_states = {}  # Backup original state of all lights
        self.active_camera_name = None  # Track currently active camera
        self.is_initialized = False
    
    def initialize_system(self, context):
        """Initialize camera-light system when addon is enabled"""
        if self.is_initialized:
            return
            
        print("\n=== CAMERA LIGHT SYSTEM INITIALIZING ===")
        
        # CONTEXT VALIDATION: Ensure context is valid and has scene
        if not self._is_context_valid(context):
            print("⚠️  Context not ready, scheduling delayed initialization")
            self._schedule_delayed_initialization()
            return
        
        # Backup original state of all lights
        self.backup_original_light_states(context)
        
        # Load camera-light assignments using naming system
        success = self._load_assignments_from_properties()
        
        if success:
            print("✅ Camera-light assignments loaded successfully")
        else:
            print("⚠️  No camera-light assignments found (this is normal if no lights with naming convention exist)")
        
        # Set initial active camera
        if context.scene.camera:
            self.active_camera_name = context.scene.camera.name
            print(f"Active camera set to: {self.active_camera_name}")
        else:
            print("No active camera found")
        
        # Update visibility for active camera
        if self.active_camera_name:
            self.update_light_visibility_for_camera(context, self.active_camera_name)
        
        # Register scene update handler
        self.register_scene_update_handler()
        
        self.is_initialized = True
        print("=== CAMERA LIGHT SYSTEM INITIALIZED ===")
    
    
    def cleanup_system(self, context):
        """Cleanup camera-light system when addon is disabled"""
        if not self.is_initialized:
            return
            
        print("\n=== CAMERA LIGHT SYSTEM CLEANING UP ===")
        
        # Restore original state of all lights
        self.restore_original_light_states(context)
        
        # Unregister scene update handler
        self.unregister_scene_update_handler()
        
        # Reset state (preserve camera_light_assignments as user data)
        self.active_camera_name = None
        # self.camera_light_assignments.clear()  # Don't clear user assignments!
        self.original_light_states.clear()
        self.is_initialized = False
        
        print("=== CAMERA LIGHT SYSTEM CLEANED UP ===")
    
    def backup_original_light_states(self, context):
        """Backup original state of all lights in scene"""
        self.original_light_states.clear()
        
        for obj in context.scene.objects:
            if obj.type == 'LIGHT':
                self.original_light_states[obj.name] = {
                    'hide_viewport': obj.hide_viewport,
                    'hide_render': obj.hide_render
                }
    
    def restore_original_light_states(self, context):
        """Restore original state of all lights"""
        for obj in context.scene.objects:
            if obj.type == 'LIGHT' and obj.name in self.original_light_states:
                original_state = self.original_light_states[obj.name]
                obj.hide_viewport = original_state['hide_viewport']
                obj.hide_render = original_state['hide_render']
    
    def assign_light_to_camera(self, camera_name: str, light_name: str):
        """Assign light to specific camera"""
        # Add to memory cache
        if light_name not in self.camera_light_assignments[camera_name]:
            self.camera_light_assignments[camera_name].append(light_name)
            print(f"Assigned light '{light_name}' to camera '{camera_name}'")
        else:
            print(f"Light '{light_name}' already assigned to camera '{camera_name}'")
        
        # Save to persistent Blender properties
        self._save_assignments_to_properties()
    
    def remove_light_from_camera(self, camera_name: str, light_name: str):
        """Remove light from specific camera"""
        if camera_name in self.camera_light_assignments:
            if light_name in self.camera_light_assignments[camera_name]:
                self.camera_light_assignments[camera_name].remove(light_name)
        
        # Save to persistent Blender properties
        self._save_assignments_to_properties()
    
    def get_camera_assigned_lights(self, camera_name: str) -> List[str]:
        """Get list of lights assigned to camera"""
        # First try to load from persistent properties if memory cache is empty
        if not self.camera_light_assignments.get(camera_name):
            self._load_assignments_from_properties()
        return self.camera_light_assignments.get(camera_name, [])
    
    def update_light_visibility_for_camera(self, context, camera_name: str):
        """Update light visibility for specific camera"""
        if not camera_name:
            return
            
        print(f"\n=== UPDATING LIGHT VISIBILITY FOR CAMERA ===")
        print(f"Camera: {camera_name}")
        
        # Get all lights in scene
        all_lights = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
        
        # Get lights assigned to this camera
        assigned_lights = self.get_camera_assigned_lights(camera_name)
        
        print(f"Total lights in scene: {len(all_lights)}")
        print(f"Lights assigned to camera '{camera_name}': {assigned_lights}")
        
        for light in all_lights:
            if light.name in assigned_lights:
                # Show assigned lights
                light.hide_viewport = False
                light.hide_render = False
                print(f"SHOWING: {light.name} (assigned to camera)")
            else:
                # Hide unassigned lights
                light.hide_viewport = True
                light.hide_render = True
                print(f"HIDING: {light.name} (not assigned to camera)")
        
        print("=== LIGHT VISIBILITY UPDATE COMPLETE ===")
    
    def check_camera_change(self, context):
        """Check if active camera changed and update visibility"""
        if not context.scene.camera:
            return
            
        current_camera_name = context.scene.camera.name
        
        if current_camera_name != self.active_camera_name:
            print(f"\n=== CAMERA CHANGE DETECTED ===")
            print(f"Previous camera: {self.active_camera_name}")
            print(f"New camera: {current_camera_name}")
            
            # Update active camera
            self.active_camera_name = current_camera_name
            
            # NO AUTO-ASSIGNMENT - only update visibility for existing assignments
            # Auto-assignment only happens during light creation, not camera switches
            
            # Update visibility for new camera
            self.update_light_visibility_for_camera(context, current_camera_name)
            
            # Force viewport update
            if context.area:
                context.area.tag_redraw()
                
            print(f"Camera changed to: {current_camera_name}")
            print("=== CAMERA CHANGE HANDLED ===")
    
    def register_scene_update_handler(self):
        """Register scene update handler for camera change detection"""
        # Remove existing handler if any
        self.unregister_scene_update_handler()
        
        # Add new handler
        if on_scene_update not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(on_scene_update)
    
    def unregister_scene_update_handler(self):
        """Unregister scene update handler"""
        if on_scene_update in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(on_scene_update)
    
    def _is_context_valid(self, context):
        """Validate context to ensure scene access"""
        try:
            # Check if context exists and has scene
            if context is None:
                return False
            
            # Check if context has scene attribute
            if not hasattr(context, 'scene'):
                return False
            
            # Check if scene is valid
            if context.scene is None:
                return False
            
            # Check if this is _RestrictContext (problematic)
            context_type = type(context).__name__
            if context_type == '_RestrictContext':
                return False
            
            # Check if can access scene objects
            try:
                _ = context.scene.objects
                return True
            except (AttributeError, RuntimeError):
                return False
                
        except Exception:
            return False
    
    def _schedule_delayed_initialization(self):
        """Schedule delayed initialization using Blender timer"""
        try:
            # Remove existing timer if any
            if hasattr(bpy.app, 'timers') and hasattr(self, '_delayed_init_timer'):
                if self._delayed_init_timer in bpy.app.timers:
                    bpy.app.timers.remove(self._delayed_init_timer)
            
            # Schedule new timer
            self._delayed_init_timer = bpy.app.timers.register(
                self._delayed_initialize,
                first_interval=0.5  # Wait 0.5 seconds
            )
            print("📅 Delayed initialization scheduled in 0.5 seconds")
            
        except Exception as e:
            print(f"❌ Failed to schedule delayed initialization: {e}")
    
    def _delayed_initialize(self):
        """Delayed initialization called by timer"""
        try:
            context = bpy.context
            if self._is_context_valid(context):
                self.initialize_system(context)
        except Exception as e:
            print(f"❌ Delayed initialization failed: {e}")
        finally:
            # Remove timer reference if completed
            if hasattr(self, '_delayed_init_timer'):
                delattr(self, '_delayed_init_timer')
        
        return None  # Remove timer
    
    def _save_assignments_to_properties(self):
        """Save camera-light assignments using naming system (no PropertyGroup needed)"""
        try:
            # With naming system, assignments are stored directly in Blender object names
            # No need to save to PropertyGroup because assignments are detected automatically
            # from light name prefixes (C_XX_ for specific camera, G_ for global)
            
            print(f"💾 Assignments are stored in light names using naming convention")
            print(f"💾 Total cameras with assignments: {len(self.camera_light_assignments)}")
            
            # Debug: Print current assignments
            if self.camera_light_assignments:
                print("🔍 Current assignments (stored in light names):")
                for camera, lights in self.camera_light_assignments.items():
                    print(f"  - {camera}: {lights}")
            else:
                print("⚠️  No assignments to save")
            
            # Nothing needs to be saved to PropertyGroup because the system already uses
            # persistent naming convention in Blender objects
            print("✅ Naming convention system - no PropertyGroup saving needed")
            
        except Exception as e:
            print(f"⚠️  Failed to save assignments (naming convention): {e}")
            import traceback
            traceback.print_exc()
    
    def _load_assignments_from_properties(self):
        """Load camera-light assignments from Blender properties using naming system"""
        try:
            scene = bpy.context.scene
            loaded_count = 0
            
            print(f"📖 Loading assignments using naming system")
            
            # Clear existing assignments
            self.camera_light_assignments.clear()
            
            # Get all cameras in scene
            cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
            print(f"📖 Found {len(cameras)} cameras in scene")
            
            # Get all lights in scene
            lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
            print(f"📖 Found {len(lights)} lights in scene")
            
            # Detect assignments based on naming system
            for camera in cameras:
                camera_name = camera.name
                print(f"📖 Checking assignments for camera: {camera_name}")
                
                # Extract camera number from name
                camera_num = self._extract_camera_number(camera_name)
                if camera_num:
                    # Find lights with prefix C_{camera_num}_
                    assigned_lights = []
                    for light in lights:
                        if light.name.startswith(f"C_{camera_num}_"):
                            assigned_lights.append(light.name)
                    
                    if assigned_lights:
                        self.camera_light_assignments[camera_name] = assigned_lights
                        loaded_count += 1
                        print(f"  ✅ Found {len(assigned_lights)} lights for {camera_name}: {assigned_lights}")
                    else:
                        print(f"  📖 No lights found for {camera_name}")
                else:
                    print(f"  📖 Could not extract camera number from: {camera_name}")
            
            # Also check global lights (prefix G_)
            global_lights = []
            for light in lights:
                if light.name.startswith("G_"):
                    global_lights.append(light.name)
            
            if global_lights:
                # Add global lights to all cameras
                for camera_name in self.camera_light_assignments:
                    self.camera_light_assignments[camera_name].extend(global_lights)
                
                print(f"  ✅ Added {len(global_lights)} global lights to all cameras")
            
            print(f"📊 Memory cache now contains {len(self.camera_light_assignments)} cameras")
            
            # Debug: Print loaded assignments
            if self.camera_light_assignments:
                print("🔍 Current assignments in memory:")
                for camera, lights in self.camera_light_assignments.items():
                    print(f"  - {camera}: {lights}")
            else:
                print("⚠️  No assignments loaded")
            
            return loaded_count > 0
                    
        except Exception as e:
            print(f"⚠️  Failed to load assignments from naming system: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _extract_camera_number(self, camera_name):
        """Extract camera number from camera name"""
        try:
            # Handle format Camera.001, Camera.002, etc.
            if camera_name.endswith('.001'):
                return '01'
            elif camera_name.endswith('.002'):
                return '02'
            elif camera_name.endswith('.003'):
                return '03'
            elif camera_name.endswith('.004'):
                return '04'
            elif camera_name.endswith('.005'):
                return '05'
            elif camera_name.endswith('.006'):
                return '06'
            elif camera_name.endswith('.007'):
                return '07'
            elif camera_name.endswith('.008'):
                return '08'
            elif camera_name.endswith('.009'):
                return '09'
            elif camera_name == 'Camera':
                return '00'
            else:
                # Extract number from camera name
                match = re.search(r'\d+', camera_name)
                return match.group(0).zfill(2) if match else None
        except Exception as e:
            print(f"Error extracting camera number from {camera_name}: {e}")
            return None
    

# Global handler function
def on_scene_update(depsgraph):
    """Handler for depsgraph update events"""
    try:
        # Get manager instance
        manager = get_camera_light_manager()
        
        # Check camera change
        if manager.is_initialized:
            manager.check_camera_change(bpy.context)
    except Exception:
        # Silently fail to avoid breaking Blender
        pass

# Helper function for automatic light assignment
def generate_organized_light_name(base_name: str, assignment_mode: str, camera_name: str = None) -> str:
    """Generate organized light name with prefix based on assignment mode"""
    try:
        # Remove existing prefixes if any
        clean_name = base_name
        for prefix in ['G_', 'C_00', 'C_01', 'C_02', 'C_03', 'C_04', 'C_05', 'C_06', 'C_07', 'C_08', 'C_09']:
            if clean_name.startswith(prefix):
                clean_name = clean_name[len(prefix):].lstrip('_')
                break
        
        if assignment_mode == 'SCENE':
            # Global mode: Add G_ prefix
            return f"G_{clean_name}"
        else:  # CAMERA mode
            # Camera mode: Add C_XX prefix based on camera
            if camera_name:
                # Extract camera number or use camera name
                if camera_name.endswith('.001'):
                    camera_num = '01'
                elif camera_name.endswith('.002'):
                    camera_num = '02'
                elif camera_name.endswith('.003'):
                    camera_num = '03'
                elif camera_name.endswith('.004'):
                    camera_num = '04'
                elif camera_name.endswith('.005'):
                    camera_num = '05'
                elif camera_name.endswith('.006'):
                    camera_num = '06'
                elif camera_name.endswith('.007'):
                    camera_num = '07'
                elif camera_name.endswith('.008'):
                    camera_num = '08'
                elif camera_name.endswith('.009'):
                    camera_num = '09'
                elif camera_name == 'Camera':
                    camera_num = '00'
                else:
                    # Extract number from camera name or use default
                    match = re.search(r'\d+', camera_name)
                    camera_num = match.group(0).zfill(2) if match else '00'
                
                return f"C_{camera_num}_{clean_name}"
            else:
                # No camera specified, use default
                return f"C_00_{clean_name}"
    except Exception as e:
        print(f"Error generating organized light name: {e}")
        return base_name  # Fallback to original name

def assign_light_to_active_camera(light_obj):
    """Assign new light to active camera or all cameras depending on mode"""
    try:
        context = bpy.context
        
        # Validate context before accessing scene
        if context is None or not hasattr(context, 'scene') or context.scene is None:
            print("⚠️  Cannot assign light to camera: Context not available")
            return
        
        scene = context.scene
        assignment_mode = getattr(scene, 'lumi_light_assignment_mode', 'SCENE')
        
        manager = get_camera_light_manager()
        
        # Generate organized name and rename the light
        original_name = light_obj.name
        if assignment_mode == 'SCENE':
            organized_name = generate_organized_light_name(original_name, 'SCENE')
        else:
            active_camera = scene.camera
            camera_name = active_camera.name if active_camera else None
            organized_name = generate_organized_light_name(original_name, 'CAMERA', camera_name)
        
        # Rename the light if name is different
        if organized_name != original_name:
            # Check if name already exists, add suffix if needed
            final_name = organized_name
            counter = 1
            while final_name in bpy.data.objects:
                final_name = f"{organized_name}.{counter:03d}"
                counter += 1
            
            light_obj.name = final_name
            print(f"Renamed light: '{original_name}' → '{light_obj.name}'")
        
        print(f"\n=== ASSIGNING LIGHT (Mode: {assignment_mode}) ===")
        print(f"Light: {light_obj.name}")
        
        if assignment_mode == 'SCENE':
            # Scene mode: Assign to all cameras
            all_cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
            
            if all_cameras:
                print(f"Assigning to all cameras ({len(all_cameras)} cameras)")
                for camera in all_cameras:
                    manager.assign_light_to_camera(camera.name, light_obj.name)
                    print(f"  - Assigned to camera: {camera.name}")
                
                # Update visibility for all cameras
                for camera in all_cameras:
                    manager.update_light_visibility_for_camera(context, camera.name)
                
                print(f"Light '{light_obj.name}' assigned to all cameras (global)")
            else:
                print(f"⚠️  No cameras found in scene")
                
        else:  # CAMERA mode
            # Camera mode: Assign only to active camera
            active_camera = scene.camera
            
            if active_camera:
                print(f"Assigning to active camera only")
                print(f"Camera: {active_camera.name}")
                
                manager.assign_light_to_camera(active_camera.name, light_obj.name)
                
                # Update visibility immediately (system always active)
                manager.update_light_visibility_for_camera(context, active_camera.name)
                
                print(f"Light '{light_obj.name}' assigned to camera '{active_camera.name}' (camera-specific)")
            else:
                print(f"⚠️  No active camera found for light assignment")
        
        # Force viewport update
        if context.area:
            context.area.tag_redraw()
            
    except Exception as e:
        print(f"❌ Failed to assign light to camera: {e}")