# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer


import bpy
try:
    import requests
except ImportError:
    requests = None
import json
import tempfile
import zipfile
import shutil
import os
from pathlib import Path

# Konfigurasi GitHub
GITHUB_REPO = "ProductViz/LumiFlow"
ADDON_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_current_version():
    """Get current addon version from bl_info"""
    from .. import bl_info
    return bl_info["version"]

def parse_version(version_str):
    """Convert version string to tuple (1, 2, 3)"""
    try:
        version_str = version_str.lstrip('v')
        return tuple(map(int, version_str.split('.')))
    except Exception:
        return (0, 0, 0)


class LUMI_OT_check_update(bpy.types.Operator):
    """Check for LumiFlow addon updates from GitHub"""
    bl_idname = "lumiflow.check_update"
    bl_label = "Check Update"
    bl_description = "Check if a newer version of LumiFlow is available on GitHub"

    def execute(self, context):
        if requests is None:
            context.window_manager.lumiflow_update_info = "ERROR|Requests module not available. Please install requests library."
            self.report({'ERROR'}, "Requests module not available")
            return {'CANCELLED'}

        try:
            current_version = get_current_version()
            current_version_str = f"v{current_version[0]}.{current_version[1]}.{current_version[2]}"

            response = requests.get(ADDON_API_URL, timeout=10)

            if response.status_code != 200:
                context.window_manager.lumiflow_update_info = "ERROR|Failed to check updates. Please try again later."
                self.report({'WARNING'}, "Failed to connect to GitHub")
                return {'CANCELLED'}

            data = response.json()
            latest_version_str = data.get("tag_name", "v0.0.0")
            latest_version = parse_version(latest_version_str)
            download_url = data.get("zipball_url", "")

            wm = context.window_manager

            if latest_version > current_version:
                wm.lumiflow_update_info = f"UPDATE|{latest_version_str}|{download_url}"
                self.report({'INFO'}, f"New version available: {latest_version_str}")
            else:
                wm.lumiflow_update_info = f"UPTODATE|{current_version_str}"
                self.report({'INFO'}, f"You're using the latest version: {current_version_str}")

            return {'FINISHED'}

        except requests.exceptions.RequestException as e:
            context.window_manager.lumiflow_update_info = "ERROR|Network error. Check your internet connection."
            self.report({'ERROR'}, f"Network error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            context.window_manager.lumiflow_update_info = f"ERROR|{str(e)}"
            self.report({'ERROR'}, f"Error checking updates: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_update_addon(bpy.types.Operator):
    """Download and install the latest version of LumiFlow"""
    bl_idname = "lumiflow.update_addon"
    bl_label = "Update Now"
    bl_description = "Download and install the latest version from GitHub"

    download_url: bpy.props.StringProperty()
    new_version: bpy.props.StringProperty()

    def execute(self, context):
        if requests is None:
            self.report({'ERROR'}, "Requests module not available")
            return {'CANCELLED'}

        if not self.download_url:
            self.report({'ERROR'}, "No download URL provided")
            return {'CANCELLED'}

        temp_dir = None
        addon_dest = None

        try:
            # ============================================================
            # STEP 1: Download ZIP
            # ============================================================
            self.report({'INFO'}, f"Downloading LumiFlow {self.new_version}...")

            temp_dir = Path(tempfile.gettempdir()) / "lumiflow_update"

            # Clean temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

            temp_dir.mkdir(exist_ok=True)

            zip_path = temp_dir / f"lumiflow_{self.new_version}.zip"

            response = requests.get(self.download_url, timeout=30, stream=True)
            if response.status_code != 200:
                raise Exception(f"Failed to download: HTTP {response.status_code}")

            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # ============================================================
            # STEP 2: Extract ZIP
            # ============================================================
            self.report({'INFO'}, "Extracting files...")
            extract_dir = temp_dir / "extracted"

            if extract_dir.exists():
                shutil.rmtree(extract_dir, ignore_errors=True)

            extract_dir.mkdir()

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # ============================================================
            # STEP 3: Find addon folder
            # ============================================================
            extracted_folders = list(extract_dir.iterdir())
            if not extracted_folders:
                raise Exception("Extracted archive is empty")

            # The first folder should be the repo folder
            repo_folder = extracted_folders[0]
            addon_source = None

            # Look for LumiFlow folder or __init__.py with bl_info
            for item in repo_folder.iterdir():
                if item.is_dir() and item.name == "LumiFlow":
                    addon_source = item
                    break
                elif item.is_file() and item.name == "__init__.py":
                    # Addon root is the repo folder itself
                    addon_source = repo_folder
                    break

            if not addon_source:
                raise Exception("Could not find LumiFlow addon in the archive")

            # ============================================================
            # STEP 4: Get addon installation path
            # ============================================================
            addon_paths = bpy.utils.script_paths(subdir="addons")
            if not addon_paths:
                raise Exception("Could not find Blender addons directory")

            # Use user addons directory (first in list)
            user_addons_dir = Path(addon_paths[0])
            addon_dest = user_addons_dir / "LumiFlow"

            # ============================================================
            # STEP 5: Copy new version (overwrite old files)
            # ============================================================
            self.report({'INFO'}, "Installing new version...")
            
            # Simply copy over - let shutil handle overwriting
            shutil.copytree(addon_source, addon_dest, dirs_exist_ok=True)

            # ============================================================
            # STEP 6: Cleanup temp directory
            # ============================================================
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

            # Clear update info
            context.window_manager.lumiflow_update_info = ""
            context.scene.show_update_panel = False

            self.report({'INFO'}, f"✓ Successfully updated to {self.new_version}!")
            self.report({'INFO'}, "Please restart Blender to complete the update")

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Update failed: {str(e)}")
            
            # Cleanup temp files on failure
            if temp_dir and temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except:
                    pass

            return {'CANCELLED'}


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