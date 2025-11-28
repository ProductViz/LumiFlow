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
LumiFlow Addon Main Module
Main entry point for the LumiFlow Blender addon with addon metadata and module imports.
"""
bl_info = {
    "name": "LumiFlow",
    "author": "Burhanuddin",
    "version": (1, 2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > LumiFlow",
    "description": "Smart lighting tools for Blender",
    "category": "Lighting",
}

import bpy
import importlib
import sys

# Import addon modules
from . import base_modal
from . import registration

# Development mode - reload modules when script reloads
if "bpy" in locals():
    try:
        addon_name = __name__.split('.')[0]
        
        modules_to_reload = []
        for name, module in sys.modules.items():
            if name.startswith(addon_name + '.') and name != __name__:
                modules_to_reload.append((name, module))
        
        modules_to_reload.sort(key=lambda x: x[0].count('.'), reverse=True)
        
        for name, module in modules_to_reload:
            try:
                importlib.reload(module)
            except ImportError:
                pass
            except Exception:
                pass
        
        try:
            importlib.reload(base_modal)
        except Exception:
            pass
        
        try:
            importlib.reload(registration)
        except Exception:
            pass
            
    except Exception:
        pass

# Export BaseModalOperator for use by other modules
from .base_modal import BaseModalOperator

def register():
    """Register LumiFlow addon with error handling"""
    try:
        registration.register()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise  # Re-raise to ensure Blender knows registration failed

def unregister():
    """Unregister LumiFlow addon with error handling"""
    try:
        registration.unregister()
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Don't re-raise during unregister to avoid Blender issues

if __name__ == "__main__":
    register()
