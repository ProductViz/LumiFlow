# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

import bpy
import os
import shutil
import requests
import zipfile
import tempfile
import json
import logging
import webbrowser
from pathlib import Path

logger = logging.getLogger(__name__)

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
        # Remove any suffix like -beta, -alpha
        version_str = version_str.split('-')[0]
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

            self.report({'INFO'}, "Checking for updates...")
            response = requests.get(ADDON_API_URL, timeout=10)

            if response.status_code != 200:
                context.window_manager.lumiflow_update_info = "ERROR|Failed to check updates. Please try again later."
                self.report({'WARNING'}, "Failed to connect to GitHub")
                return {'CANCELLED'}

            data = response.json()
            latest_version_str = data.get("tag_name", "v0.0.0")
            latest_version = parse_version(latest_version_str)
            
            # ✅ PERUBAHAN: Ambil dari assets, bukan zipball_url
            assets = data.get("assets", [])
            download_url = ""
            
            # Cari asset dengan nama LumiFlow-{tag_name}.zip
            expected_filename = f"LumiFlow-{latest_version_str}.zip"
            logger.info(f"Looking for asset: {expected_filename}")
            
            for asset in assets:
                asset_name = asset.get("name", "")
                if asset_name == expected_filename:
                    download_url = asset.get("browser_download_url", "")
                    logger.info(f"Found matching asset: {asset_name}")
                    break
            
            # Fallback 1: Cari asset yang mengandung "LumiFlow" dan ".zip"
            if not download_url:
                logger.warning(f"Exact match not found, searching for LumiFlow*.zip")
                for asset in assets:
                    asset_name = asset.get("name", "")
                    if "LumiFlow" in asset_name and asset_name.endswith(".zip"):
                        download_url = asset.get("browser_download_url", "")
                        logger.info(f"Found fallback asset: {asset_name}")
                        break
            
            # Fallback 2: Ambil asset pertama jika tidak ada yang cocok
            if not download_url and assets:
                download_url = assets[0].get("browser_download_url", "")
                logger.warning(f"Using first asset: {assets[0].get('name')}")
            
            # Fallback 3: Gunakan zipball_url (backward compatibility)
            if not download_url:
                download_url = data.get("zipball_url", "")
                logger.warning("No assets found, falling back to zipball_url")

            if not download_url:
                context.window_manager.lumiflow_update_info = "ERROR|No download URL found in release"
                self.report({'ERROR'}, "No download URL found")
                return {'CANCELLED'}

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
            logger.exception("Error checking updates")
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
        backup_dir = None

        try:
            current_version = get_current_version()
            current_version_str = f"v{current_version[0]}.{current_version[1]}.{current_version[2]}"

            # ============================================================
            # STEP 1: Download ZIP
            # ============================================================
            self.report({'INFO'}, f"Downloading LumiFlow {self.new_version}...")
            logger.info(f"Download URL: {self.download_url}")

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

            logger.info(f"Download complete: {zip_path}")

            # ============================================================
            # STEP 2: Validate ZIP
            # ============================================================
            self.report({'INFO'}, "Validating download...")
            
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Test ZIP integrity
                    bad_file = zip_ref.testzip()
                    if bad_file:
                        raise Exception(f"Corrupted file in ZIP: {bad_file}")
                    
                    # Check if __init__.py exists
                    file_list = zip_ref.namelist()
                    has_init = any("__init__.py" in f for f in file_list)
                    if not has_init:
                        raise Exception("Invalid addon ZIP: missing __init__.py")
                    
                    logger.info("ZIP validation passed")
            except zipfile.BadZipFile:
                raise Exception("Invalid or corrupted ZIP file")

            # ============================================================
            # STEP 3: Extract ZIP
            # ============================================================
            self.report({'INFO'}, "Extracting files...")
            extract_dir = temp_dir / "extracted"

            if extract_dir.exists():
                shutil.rmtree(extract_dir, ignore_errors=True)

            extract_dir.mkdir()

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            logger.info(f"Extracted to: {extract_dir}")

            # ============================================================
            # STEP 4: Find addon folder
            # ============================================================
            extracted_folders = list(extract_dir.iterdir())
            if not extracted_folders:
                raise Exception("Extracted archive is empty")

            addon_source = None

            # ✅ PERUBAHAN: Deteksi struktur ZIP yang lebih robust
            
            # Scenario 1: ZIP berisi LumiFlow/ langsung (dari asset)
            if len(extracted_folders) == 1 and extracted_folders[0].name == "LumiFlow":
                addon_source = extracted_folders[0]
                logger.info(f"Found addon source (direct): {addon_source}")
            
            # Scenario 2: ZIP berisi multiple folders, cari LumiFlow
            elif len(extracted_folders) > 1:
                for folder in extracted_folders:
                    if folder.is_dir() and folder.name == "LumiFlow":
                        addon_source = folder
                        logger.info(f"Found addon source (multiple): {addon_source}")
                        break
            
            # Scenario 3: ZIP berisi folder repo (dari zipball)
            if not addon_source:
                repo_folder = extracted_folders[0]
                logger.info(f"Checking repo folder: {repo_folder}")
                
                # Cari folder LumiFlow di dalam repo folder
                for item in repo_folder.iterdir():
                    if item.is_dir() and item.name == "LumiFlow":
                        addon_source = item
                        logger.info(f"Found addon source (repo subfolder): {addon_source}")
                        break
                    elif item.is_file() and item.name == "__init__.py":
                        # Addon root adalah repo folder itu sendiri
                        addon_source = repo_folder
                        logger.info(f"Found addon source (repo root): {addon_source}")
                        break

            if not addon_source:
                raise Exception("Could not find LumiFlow addon in the archive")

            # Verify __init__.py exists
            init_file = addon_source / "__init__.py"
            if not init_file.exists():
                raise Exception(f"Invalid addon structure: {addon_source} missing __init__.py")

            logger.info(f"Addon source validated: {addon_source}")

            # ============================================================
            # STEP 5: Get addon installation path
            # ============================================================
            addon_paths = bpy.utils.script_paths(subdir="addons")
            if not addon_paths:
                raise Exception("Could not find Blender addons directory")

            # Use user addons directory (first in list)
            user_addons_dir = Path(addon_paths[0])
            addon_dest = user_addons_dir / "LumiFlow"

            logger.info(f"Addon destination: {addon_dest}")

            # ============================================================
            # STEP 5.5: Backup existing addon
            # ============================================================
            if addon_dest.exists():
                self.report({'INFO'}, "Creating backup...")
                backup_dir = user_addons_dir / f"LumiFlow_backup_{current_version_str}"
                
                # Hapus backup lama jika ada
                if backup_dir.exists():
                    shutil.rmtree(backup_dir, ignore_errors=True)
                
                # Copy addon saat ini ke backup
                shutil.copytree(addon_dest, backup_dir)
                logger.info(f"Backup created: {backup_dir}")
                self.report({'INFO'}, "Backup created")

            # ============================================================
            # STEP 6: Install new version (overwrite old files)
            # ============================================================
            self.report({'INFO'}, "Installing new version...")
            
            # Simply copy over - let shutil handle overwriting
            shutil.copytree(addon_source, addon_dest, dirs_exist_ok=True)
            logger.info("Installation complete")

            # ============================================================
            # STEP 7: Cleanup temp directory and backup
            # ============================================================
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Delete backup after successful update
            if backup_dir and backup_dir.exists():
                try:
                    shutil.rmtree(backup_dir, ignore_errors=True)
                    logger.info(f"Backup deleted: {backup_dir}")
                except Exception as e:
                    logger.warning(f"Failed to delete backup: {e}")

            # Set SUCCESS status to show restart message
            context.window_manager.lumiflow_update_info = f"SUCCESS|{self.new_version}"

            self.report({'INFO'}, f"✓ Successfully updated to {self.new_version}!")
            self.report({'INFO'}, "Please restart Blender to complete the update")

            return {'FINISHED'}

        except Exception as e:
            error_msg = str(e)
            self.report({'ERROR'}, f"Update failed: {error_msg}")
            logger.exception("Update failed")
            
            # ============================================================
            # ROLLBACK: Restore backup if update failed
            # ============================================================
            if backup_dir and backup_dir.exists() and addon_dest:
                try:
                    self.report({'INFO'}, "Rolling back to previous version...")
                    
                    # Remove failed update
                    if addon_dest.exists():
                        shutil.rmtree(addon_dest, ignore_errors=True)
                    
                    # Restore backup
                    shutil.copytree(backup_dir, addon_dest)
                    
                    self.report({'INFO'}, "Rollback successful")
                    logger.info("Rollback successful")
                except Exception as rollback_error:
                    self.report({'ERROR'}, f"Rollback failed: {str(rollback_error)}")
                    logger.exception("Rollback failed")
            
            # Cleanup temp files on failure
            if temp_dir and temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception as cleanup_error:
                    logger.warning(f"Failed to cleanup temp files: {cleanup_error}")

            return {'CANCELLED'}


class LUMI_OT_download_zip(bpy.types.Operator):
    """Open GitHub Release page to download ZIP manually"""
    bl_idname = "lumiflow.download_zip"
    bl_label = "Download from GitHub"
    bl_description = "Open GitHub Release page in browser to download ZIP file manually"

    download_url: bpy.props.StringProperty()
    new_version: bpy.props.StringProperty()

    def execute(self, context):
        try:
            # Convert download URL to release page URL
            # From: https://github.com/ProductViz/LumiFlow/releases/download/v1.0.0/LumiFlow-v1.0.0.zip
            # To:   https://github.com/ProductViz/LumiFlow/releases/tag/v1.0.0
            
            if "github.com" in self.download_url and "/releases/download/" in self.download_url:
                # Extract version tag from download URL
                parts = self.download_url.split("/releases/download/")
                if len(parts) == 2:
                    repo_part = parts[0]  # https://github.com/ProductViz/LumiFlow
                    version_and_file = parts[1]  # v1.0.0/LumiFlow-v1.0.0.zip
                    version_tag = version_and_file.split("/")[0]  # v1.0.0
                    
                    # Construct release page URL
                    release_url = f"{repo_part}/releases/tag/{version_tag}"
                else:
                    # Fallback: use generic releases page
                    release_url = "https://github.com/ProductViz/LumiFlow/releases/latest"
            else:
                # Fallback: use generic releases page
                release_url = "https://github.com/ProductViz/LumiFlow/releases/latest"
            
            logger.info(f"Opening release page: {release_url}")
            
            # Open in default browser
            webbrowser.open(release_url)
            
            self.report({'INFO'}, f"Opening GitHub Release page for {self.new_version}")
            self.report({'INFO'}, "Download the ZIP file and install manually via Blender Preferences")
            
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = str(e)
            self.report({'ERROR'}, f"Failed to open browser: {error_msg}")
            logger.exception("Failed to open browser")
            return {'CANCELLED'}


class LUMI_OT_toggle_overlay_info(bpy.types.Operator):
    bl_idname = "lumi.toggle_overlay_info"
    bl_label = "Toggle Overlay Info"
    bl_description = "Toggle light info overlay visibility (D)"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

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

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        scene = context.scene
        scene.lumi_show_overlay_tips = not scene.lumi_show_overlay_tips
        return {'FINISHED'}


class LUMI_OT_toggle_donate_panel(bpy.types.Operator):
    """Toggle donate panel visibility"""
    bl_idname = "lumi.toggle_donate_panel"
    bl_label = "Toggle Donate Panel"
    bl_description = "Show/hide the donation panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        scene.show_donate_panel = not scene.show_donate_panel

        # Close update panel if donate panel is opened
        if scene.show_donate_panel and scene.show_update_panel:
            scene.show_update_panel = False

        return {'FINISHED'}


class LUMI_OT_toggle_positioning_mode(bpy.types.Operator):
    """Toggle positioning mode on/off"""
    bl_idname = "lumi.toggle_positioning_mode"
    bl_label = "Toggle Positioning Mode"
    bl_description = "Toggle positioning mode on/off (P)"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        scene = context.scene
        scene.lumi_positioning_mode_enabled = not scene.lumi_positioning_mode_enabled
        status = "ENABLED" if scene.lumi_positioning_mode_enabled else "DISABLED"
        self.report({'INFO'}, f"Positioning Mode {status}")
        return {'FINISHED'}


class LUMI_OT_toggle_smart_control_mode(bpy.types.Operator):
    """Toggle smart control mode on/off"""
    bl_idname = "lumi.toggle_smart_control_mode"
    bl_label = "Toggle Smart Control Mode"
    bl_description = "Toggle smart control mode on/off (F)"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        scene = context.scene
        scene.lumi_smart_control_mode_enabled = not scene.lumi_smart_control_mode_enabled
        status = "ENABLED" if scene.lumi_smart_control_mode_enabled else "DISABLED"
        self.report({'INFO'}, f"Smart Control Mode {status}")
        return {'FINISHED'}


class LUMI_OT_toggle_addon(bpy.types.Operator):
    """Toggle LumiFlow addon on/off"""
    bl_idname = "lumi.toggle_addon"
    bl_label = "Toggle LumiFlow Addon"
    bl_description = "Toggle LumiFlow addon on/off (D)"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        # Toggle addon can always be called, regardless of addon state
        return True

    def execute(self, context):
        scene = context.scene
        scene.lumi_enabled = not scene.lumi_enabled
        status = "ENABLED" if scene.lumi_enabled else "DISABLED"
        self.report({'INFO'}, f"LumiFlow {status}")
        return {'FINISHED'}


class LUMI_OT_apply_shortcuts(bpy.types.Operator):
    """Apply LumiFlow shortcut changes from Addon Preferences"""
    bl_idname = "lumiflow.apply_shortcuts"
    bl_label = "Apply LumiFlow Shortcuts"
    bl_description = "Rebuild LumiFlow keymaps using current shortcut preferences"
    bl_options = {'REGISTER'}

    # Summary text shown in confirmation dialog when there are conflicts
    conflict_summary: bpy.props.StringProperty(
        name="Conflict Summary",
        description="Summary of LumiFlow shortcut conflicts with Blender defaults",
        default="",
        options={'SKIP_SAVE'},
    )

    # ----------------------------
    # Conflict detection helpers
    # ----------------------------
    @staticmethod
    def _collect_lumiflow_bindings(prefs):
        """Collect active LumiFlow shortcut bindings from preferences.

        Returns a dict mapping (type, value, ctrl, shift, alt) -> list of
        (operator, label, action_id).
        """
        bindings = {}

        try:
            from ..shortcuts_config import iter_standard_shortcuts, get_toggle_addon_shortcut
        except Exception:
            return bindings

        # Standard actions
        for item in iter_standard_shortcuts(prefs):
            op = getattr(item, "operator", "")
            if not op:
                continue
            combo = (
                getattr(item, "key_type", "A"),
                getattr(item, "key_value", "PRESS"),
                bool(getattr(item, "ctrl", False)),
                bool(getattr(item, "shift", False)),
                bool(getattr(item, "alt", False)),
            )
            label = getattr(item, "label", "") or getattr(item, "action_id", op)
            action_id = getattr(item, "action_id", "")
            bindings.setdefault(combo, []).append((op, label, action_id))

        # Toggle addon shortcut (not part of STANDARD_ACTION_IDS)
        try:
            toggle_item = get_toggle_addon_shortcut(prefs)
        except Exception:
            toggle_item = None

        if toggle_item is not None and getattr(toggle_item, "operator", ""):
            combo = (
                getattr(toggle_item, "key_type", "L"),
                getattr(toggle_item, "key_value", "PRESS"),
                bool(getattr(toggle_item, "ctrl", False)),
                bool(getattr(toggle_item, "shift", False)),
                bool(getattr(toggle_item, "alt", False)),
            )
            label = getattr(toggle_item, "label", "") or getattr(toggle_item, "action_id", toggle_item.operator)
            action_id = getattr(toggle_item, "action_id", "")
            bindings.setdefault(combo, []).append((toggle_item.operator, label, action_id))

        return bindings

    @staticmethod
    def _format_combo(key_type, key_value, ctrl, shift, alt):
        parts = []
        if ctrl:
            parts.append("Ctrl")
        if shift:
            parts.append("Shift")
        if alt:
            parts.append("Alt")
        parts.append(key_type)
        combo = "+".join(parts)
        if key_value and key_value != "PRESS":
            combo += f" ({key_value})"
        return combo

    @classmethod
    def _detect_conflicts(cls, context, prefs):
        """Detect internal LumiFlow and Blender default conflicts.

        Returns (lumi_conflicts, blender_conflicts).
        - lumi_conflicts: dict combo -> list of (op, label, action_id) with length > 1
        - blender_conflicts: list of dicts with keys:
            combo, combo_str, lumi_label, lumi_op, km_name, bl_op
        """
        bindings = cls._collect_lumiflow_bindings(prefs)

        # Internal LumiFlow conflicts: same combo used by multiple actions
        lumi_conflicts = {
            combo: entries for combo, entries in bindings.items() if len(entries) > 1
        }

        blender_conflicts = []

        wm = getattr(context, "window_manager", None)
        if wm is None:
            return lumi_conflicts, blender_conflicts

        kc_default = getattr(wm, "keyconfigs", None)
        if kc_default is None or not getattr(kc_default, "default", None):
            return lumi_conflicts, blender_conflicts

        kc_default = kc_default.default

        target_names = {"3D View", "Object Mode"}

        # Scan Blender default keymaps for 3D View / Object Mode
        try:
            for km in kc_default.keymaps:
                if km.space_type != 'VIEW_3D':
                    continue
                if km.name not in target_names:
                    continue

                for kmi in km.keymap_items:
                    if not getattr(kmi, "active", True):
                        continue

                    combo = (
                        getattr(kmi, "type", ""),
                        getattr(kmi, "value", "PRESS"),
                        bool(getattr(kmi, "ctrl", False)),
                        bool(getattr(kmi, "shift", False)),
                        bool(getattr(kmi, "alt", False)),
                    )

                    if combo in bindings:
                        key_type, key_value, ctrl, shift, alt = combo
                        combo_str = cls._format_combo(key_type, key_value, ctrl, shift, alt)
                        for op, label, _action_id in bindings[combo]:
                            blender_conflicts.append({
                                "combo": combo,
                                "combo_str": combo_str,
                                "lumi_label": label,
                                "lumi_op": op,
                                "km_name": km.name,
                                "bl_op": getattr(kmi, "idname", ""),
                            })
        except Exception:
            # If anything goes wrong here, just fail open without blocking apply
            return lumi_conflicts, []

        return lumi_conflicts, blender_conflicts

    # ----------------------------
    # Operator UI / lifecycle
    # ----------------------------
    def invoke(self, context, event):
        try:
            from ..utils.common import get_addon_preferences
            from ..shortcuts_config import ensure_default_shortcuts

            prefs = get_addon_preferences()
            if prefs is None:
                self.report({'WARNING'}, "LumiFlow preferences not available")
                return {'CANCELLED'}

            # Ensure preferences contain default shortcuts before conflict check
            try:
                ensure_default_shortcuts(prefs)
            except Exception:
                pass

            lumi_conflicts, blender_conflicts = self._detect_conflicts(context, prefs)

            # Hard block: internal LumiFlow conflicts
            if lumi_conflicts:
                msgs = []
                for combo, entries in lumi_conflicts.items():
                    key_type, key_value, ctrl, shift, alt = combo
                    combo_str = self._format_combo(key_type, key_value, ctrl, shift, alt)
                    labels = {label for _op, label, _aid in entries}
                    msgs.append(f"{combo_str}: " + ", ".join(sorted(labels)))

                joined = "; ".join(msgs)
                self.report({'ERROR'}, f"LumiFlow shortcut conflict: {joined}")
                return {'CANCELLED'}

            # Soft block: conflicts with Blender defaults -> ask confirmation
            if blender_conflicts:
                lines = []
                for c in blender_conflicts[:8]:  # limit lines for dialog
                    lines.append(
                        f"{c['combo_str']}: {c['lumi_label']} (LumiFlow) vs {c['km_name']} → {c['bl_op']}"
                    )
                if len(blender_conflicts) > 8:
                    lines.append(f"(+ {len(blender_conflicts) - 8} more conflicts)")

                self.conflict_summary = "\n".join(lines)
                return context.window_manager.invoke_props_dialog(self, width=520)

            # No conflicts: apply directly
            return self.execute(context)

        except Exception as e:
            self.report({'ERROR'}, f"Failed to analyze shortcuts: {e}")
            return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout
        if self.conflict_summary:
            col = layout.column(align=True)
            col.label(text="Some LumiFlow shortcuts conflict with Blender defaults:", icon='ERROR')
            for line in self.conflict_summary.split("\n"):
                col.label(text=line)
            col.separator()
            col.label(text="Apply anyway and override these Blender shortcuts?", icon='QUESTION')

    def execute(self, context):
        try:
            from ..utils.common import get_addon_preferences
            from .. import registration

            prefs = get_addon_preferences()
            if prefs is None:
                self.report({'WARNING'}, "LumiFlow preferences not available")
                return {'CANCELLED'}

            # Ensure preferences contain default shortcuts before rebuild
            try:
                from ..shortcuts_config import ensure_default_shortcuts
                ensure_default_shortcuts(prefs)
            except Exception:
                pass

            # Rebuild keymaps: clear existing then register again
            try:
                registration.unregister_keymaps()
            except Exception:
                pass

            try:
                registration.register_keymaps()
            except Exception as e:
                self.report({'ERROR'}, f"Failed to register keymaps: {e}")
                return {'CANCELLED'}

            # Ensure toggle keymap is still present
            try:
                registration.ensure_toggle_addon_keymap()
            except Exception:
                pass

            self.report({'INFO'}, "LumiFlow shortcuts applied")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply shortcuts: {e}")
            return {'CANCELLED'}


class LUMI_OT_reset_shortcuts(bpy.types.Operator):
    """Reset LumiFlow shortcuts to default values"""
    bl_idname = "lumiflow.reset_shortcuts"
    bl_label = "Reset LumiFlow Shortcuts"
    bl_description = "Reset LumiFlow shortcuts in Addon Preferences to defaults and rebuild keymaps"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            from ..utils.common import get_addon_preferences
            from ..shortcuts_config import reset_shortcuts_to_default
            from .. import registration

            prefs = get_addon_preferences()
            if prefs is None:
                self.report({'WARNING'}, "LumiFlow preferences not available")
                return {'CANCELLED'}

            # Reset preferences to default shortcuts
            try:
                reset_shortcuts_to_default(prefs)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to reset shortcuts: {e}")
                return {'CANCELLED'}

            # Rebuild keymaps using the apply operator logic
            try:
                registration.unregister_keymaps()
            except Exception:
                pass

            try:
                registration.register_keymaps()
            except Exception as e:
                self.report({'ERROR'}, f"Failed to register keymaps after reset: {e}")
                return {'CANCELLED'}

            try:
                registration.ensure_toggle_addon_keymap()
            except Exception:
                pass

            self.report({'INFO'}, "LumiFlow shortcuts reset to defaults")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to reset shortcuts: {e}")
            return {'CANCELLED'}


class LUMI_OT_toggle_viewport_overlay(bpy.types.Operator):
    """Toggle overlay visibility for specific viewport"""
    bl_idname = "lumi.toggle_viewport_overlay"
    bl_label = "Toggle Viewport Overlay"
    bl_description = "Toggle overlay visibility for current viewport"
    bl_options = {'REGISTER'}

    overlay_type: bpy.props.StringProperty(
        name="Overlay Type",
        description="Type of overlay to toggle",
        default=""
    )

    viewport_id: bpy.props.StringProperty(
        name="Viewport ID",
        description="ID of the viewport to toggle overlay for",
        default=""
    )

    @classmethod
    def description(cls, context, properties):
        overlay_type = getattr(properties, "overlay_type", "")

        if overlay_type == "overlay_tips":
            return "Show overlay tips"
        if overlay_type == "overlay_info":
            return "Show overlay info"

        return cls.bl_description

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        if not self.overlay_type:
            self.report({'ERROR'}, "No overlay type specified")
            return {'CANCELLED'}

        # Import here to avoid circular imports
        from ..ui.overlay.config import viewport_overlay_manager

        # Get current viewport context
        current_viewport_id = viewport_overlay_manager.get_viewport_id(context)

        # Use provided viewport_id if available, otherwise use current
        target_viewport_id = self.viewport_id or current_viewport_id

        if target_viewport_id is None:
            self.report({'ERROR'}, "No viewport context available")
            return {'CANCELLED'}

        # Toggle the overlay state for this viewport
        current_state = viewport_overlay_manager.get_overlay_state(context, self.overlay_type)
        new_state = not current_state

        viewport_overlay_manager.set_overlay_state(context, self.overlay_type, new_state)

        # Force redraw of all 3D viewports to update the overlay
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

        status = "ENABLED" if new_state else "DISABLED"
        return {'FINISHED'}


class LUMI_OT_clean_viewport(bpy.types.Operator):
    """Toggle overlay elements for clean viewport"""
    bl_idname = "lumi.clean_viewport"
    bl_label = "Clean Viewport"
    bl_description = "Toggle overlay elements visibility for a clean viewport view"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        try:
            space_data = context.space_data
            
            # Check if we're in a 3D viewport
            if space_data.type != 'VIEW_3D':
                self.report({'WARNING'}, "Must be in 3D viewport")
                return {'CANCELLED'}
            
            # Import viewport overlay manager
            from ..ui.overlay.config import viewport_overlay_manager
            
            # Get current viewport state
            current_state = viewport_overlay_manager.get_overlay_state(context, 'clean_viewport')
            
            # Toggle state
            if not current_state:
                # Save current overlay states for this viewport
                viewport_overlay_manager.save_viewport_overlay_states(context, space_data)
                
                # Hide overlay elements
                space_data.overlay.show_ortho_grid = False
                space_data.overlay.show_floor = False
                space_data.overlay.show_axis_x = False
                space_data.overlay.show_axis_y = False
                space_data.overlay.show_cursor = False
                space_data.overlay.show_annotation = False
                space_data.overlay.show_text = False
                space_data.overlay.show_bones = False
                space_data.overlay.show_motion_paths = False
                space_data.overlay.show_object_origins = False
                space_data.overlay.show_extras = False
                space_data.overlay.show_relationship_lines = False
                space_data.overlay.show_outline_selected = True  # Keep outline selected
                space_data.overlay.show_viewer_attribute = False
                space_data.show_reconstruction = False
                space_data.show_gizmo = False
                
                # Set viewport state to active
                viewport_overlay_manager.set_overlay_state(context, 'clean_viewport', True)
                self.report({'INFO'}, "Viewport overlays hidden")
            else:
                # Get saved states for this viewport (for tracking purposes)
                viewport_id = viewport_overlay_manager.get_viewport_id(context)
                saved_states = viewport_overlay_manager.saved_overlay_states.get(viewport_id, {})
                
                # Invert: all false values become true (and true stays true)
                # Result: enable all overlays for this specific viewport
                space_data.overlay.show_ortho_grid = True
                space_data.overlay.show_floor = True
                space_data.overlay.show_axis_x = True
                space_data.overlay.show_axis_y = True
                space_data.overlay.show_cursor = True
                space_data.overlay.show_annotation = True
                space_data.overlay.show_text = True
                space_data.overlay.show_bones = True
                space_data.overlay.show_motion_paths = True
                space_data.overlay.show_object_origins = True
                space_data.overlay.show_extras = True
                space_data.overlay.show_relationship_lines = True
                space_data.overlay.show_outline_selected = True
                space_data.overlay.show_viewer_attribute = True
                space_data.show_reconstruction = True
                space_data.show_gizmo = True
                
                # Set viewport state to inactive
                viewport_overlay_manager.set_overlay_state(context, 'clean_viewport', False)
                self.report({'INFO'}, "Viewport overlays inverted (false→true)")
            
            # Force redraw
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to toggle viewport: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_open_user_guide(bpy.types.Operator):
    """Open LumiFlow User Manual on GitHub"""
    bl_idname = "lumi.open_user_guide"
    bl_label = "Open User Guide"
    bl_description = "Open the complete LumiFlow User Manual on GitHub in your default web browser"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        try:
            # GitHub URL for user manual
            manual_url = "https://github.com/ProductViz/LumiFlow/blob/main/user_manual/00_INDEX.md"
            
            # Open in default browser
            webbrowser.open(manual_url)
            
            self.report({'INFO'}, "User guide opened in browser")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open user guide: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_open_community_discord(bpy.types.Operator):
    """Open LumiFlow community Discord"""
    bl_idname = "lumi.open_community_discord"
    bl_label = "Community"
    bl_description = "LumiFlow community Discord"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        try:
            # Discord invite URL for LumiFlow community
            discord_url = "https://discord.gg/Akav3KCRut"

            # Open in default browser
            webbrowser.open(discord_url)

            self.report({'INFO'}, "Community Discord opened in browser")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to open community Discord: {str(e)}")
            return {'CANCELLED'}


class LUMI_OT_clear_quick_exclude(bpy.types.Operator):
    """Clear Quick Smart Add exclude flags from all mesh objects in the scene"""
    bl_idname = "lumi.clear_quick_exclude"
    bl_label = "Clear Quick Exclude"
    bl_description = "Clear Quick Smart Add exclude flags from all mesh objects in the current scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        scene = context.scene
        cleared = 0

        for obj in scene.objects:
            try:
                if obj.type == 'MESH' and getattr(obj, "lumi_exclude_quick_add", False):
                    obj.lumi_exclude_quick_add = False
                    cleared += 1
            except Exception:
                # Ignore per-object errors so the rest can still be processed
                continue

        if cleared:
            self.report({'INFO'}, f"Cleared Quick Smart Add exclude on {cleared} mesh object(s)")
        else:
            self.report({'INFO'}, "No mesh objects had Quick Smart Add exclude enabled")

        return {'FINISHED'}


class LUMI_OT_clear_quick_exclude_single(bpy.types.Operator):
    """Remove one object from Quick Smart Add exclude list"""
    bl_idname = "lumi.clear_quick_exclude_single"
    bl_label = "Remove from Quick Exclude"
    bl_description = "Remove this object from the Quick Smart Add exclude"
    bl_options = {'REGISTER', 'UNDO'}

    object_name: bpy.props.StringProperty(name="Object Name", default="")

    @classmethod
    def poll(cls, context):
        from ..utils import lumi_is_addon_enabled
        return lumi_is_addon_enabled()

    def execute(self, context):
        scene = context.scene

        if not self.object_name:
            self.report({'WARNING'}, "No object specified")
            return {'CANCELLED'}

        obj = scene.objects.get(self.object_name)
        if obj is None:
            self.report({'WARNING'}, "Object not found in scene")
            return {'CANCELLED'}

        try:
            if obj.type == 'MESH' and getattr(obj, "lumi_exclude_quick_add", False):
                obj.lumi_exclude_quick_add = False
                self.report({'INFO'}, f"Removed Quick Smart Add exclude from {obj.name}")
            else:
                self.report({'INFO'}, "Object is not excluded or not a mesh")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to clear Quick Exclude for {obj.name}: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}