# Shortcut configuration and defaults for LumiFlow

import bpy

# Logical action IDs
ACTION_ID_TEMPLATE_MENU = "TEMPLATE_MENU"
ACTION_ID_FLIP_MENU = "FLIP_MENU"
ACTION_ID_QUICK_LINK = "QUICK_LINK"
ACTION_ID_QUICK_ASSIGN = "QUICK_ASSIGN"
ACTION_ID_CYCLE_LIGHTS = "CYCLE_LIGHTS"
ACTION_ID_SOLO_LIGHT = "SOLO_LIGHT"
ACTION_ID_SCALE_AXIS_MENU = "SCALE_AXIS_MENU"
ACTION_ID_TOGGLE_POSITIONING_MODE = "TOGGLE_POSITIONING_MODE"
ACTION_ID_TOGGLE_SMART_MODE = "TOGGLE_SMART_MODE"
ACTION_ID_SELECT_ALL_LIGHTS = "SELECT_ALL_LIGHTS"
ACTION_ID_TOGGLE_ADDON = "TOGGLE_ADDON"

STANDARD_ACTION_IDS = {
    ACTION_ID_TEMPLATE_MENU,
    ACTION_ID_FLIP_MENU,
    ACTION_ID_QUICK_LINK,
    ACTION_ID_QUICK_ASSIGN,
    ACTION_ID_CYCLE_LIGHTS,
    ACTION_ID_SOLO_LIGHT,
    ACTION_ID_SCALE_AXIS_MENU,
    ACTION_ID_TOGGLE_POSITIONING_MODE,
    ACTION_ID_TOGGLE_SMART_MODE,
    ACTION_ID_SELECT_ALL_LIGHTS,
}

TOGGLE_ACTION_ID = ACTION_ID_TOGGLE_ADDON


DEFAULT_SHORTCUTS = [
    {
        "action_id": ACTION_ID_TEMPLATE_MENU,
        "label": "Template Menu",
        "description": "Open LumiFlow template menu",
        "operator": "lumi.template_menu_call",
        "key_type": "A",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": True,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_FLIP_MENU,
        "label": "Flip Menu",
        "description": "Open LumiFlow flip menu",
        "operator": "lumi.flip_menu_call",
        "key_type": "C",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": True,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_QUICK_LINK,
        "label": "Quick Link to Target",
        "description": "Quick link selected light(s) to target object",
        "operator": "lumi.quick_link_to_target",
        "key_type": "X",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": True,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_QUICK_ASSIGN,
        "label": "Quick Assign Light",
        "description": "Quick assign light to active object or camera",
        "operator": "lumi.quick_assign_light",
        "key_type": "Q",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": True,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_SCALE_AXIS_MENU,
        "label": "Scale Axis Menu",
        "description": "Open LumiFlow scale axis menu",
        "operator": "lumi.scale_axis_menu_call",
        "key_type": "Q",
        "key_value": "PRESS",
        "ctrl": False,
        "shift": False,
        "alt": True,
    },
    {
        "action_id": ACTION_ID_CYCLE_LIGHTS,
        "label": "Cycle Lights",
        "description": "Cycle through scene lights",
        "operator": "lumi.cycle_lights_modal",
        "key_type": "D",
        "key_value": "PRESS",
        "ctrl": False,
        "shift": False,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_SELECT_ALL_LIGHTS,
        "label": "Select All Lights",
        "description": "Select all LumiFlow lights in the scene",
        "operator": "lumi.select_all_lights",
        "key_type": "D",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": False,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_SOLO_LIGHT,
        "label": "Quick Solo Light",
        "description": "Solo active light",
        "operator": "lumi.quick_solo_light",
        "key_type": "D",
        "key_value": "PRESS",
        "ctrl": True,
        "shift": True,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_TOGGLE_POSITIONING_MODE,
        "label": "Toggle Positioning Mode",
        "description": "Toggle LumiFlow positioning mode",
        "operator": "lumi.toggle_positioning_mode",
        "key_type": "P",
        "key_value": "PRESS",
        "ctrl": False,
        "shift": False,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_TOGGLE_SMART_MODE,
        "label": "Toggle Smart Control Mode",
        "description": "Toggle LumiFlow smart control mode",
        "operator": "lumi.toggle_smart_control_mode",
        "key_type": "F",
        "key_value": "PRESS",
        "ctrl": False,
        "shift": False,
        "alt": False,
    },
    {
        "action_id": ACTION_ID_TOGGLE_ADDON,
        "label": "Toggle LumiFlow Addon",
        "description": "Enable/disable LumiFlow addon",
        "operator": "lumi.toggle_addon",
        "key_type": "L",
        "key_value": "PRESS",
        "ctrl": False,
        "shift": False,
        "alt": False,
    },
]


def _apply_default_to_item(item, data):
    item.action_id = data.get("action_id", "")
    item.label = data.get("label", "")
    item.description = data.get("description", "")
    item.operator = data.get("operator", "")
    item.key_type = data.get("key_type", "A")
    item.key_value = data.get("key_value", "PRESS")
    item.ctrl = bool(data.get("ctrl", False))
    item.shift = bool(data.get("shift", False))
    item.alt = bool(data.get("alt", False))
    item.active = True


def ensure_default_shortcuts(prefs):
    """Ensure prefs.shortcuts contains at least the default actions.

    - If collection empty: populate with all DEFAULT_SHORTCUTS.
    - If some items exist: append only missing action_ids.
    """
    if not hasattr(prefs, "shortcuts"):
        return

    shortcuts = prefs.shortcuts

    if len(shortcuts) == 0:
        for data in DEFAULT_SHORTCUTS:
            item = shortcuts.add()
            _apply_default_to_item(item, data)
        return

    existing_ids = {item.action_id for item in shortcuts}
    for data in DEFAULT_SHORTCUTS:
        if data["action_id"] not in existing_ids:
            item = shortcuts.add()
            _apply_default_to_item(item, data)


def reset_shortcuts_to_default(prefs):
    """Reset all shortcuts in prefs to DEFAULT_SHORTCUTS."""
    if not hasattr(prefs, "shortcuts"):
        return

    prefs.shortcuts.clear()
    ensure_default_shortcuts(prefs)


def iter_standard_shortcuts(prefs):
    """Yield active shortcut items for standard actions (excluding toggle addon)."""
    if not hasattr(prefs, "shortcuts"):
        return []

    result = []
    for item in prefs.shortcuts:
        if not getattr(item, "active", True):
            continue
        if item.action_id in STANDARD_ACTION_IDS:
            result.append(item)
    return result


def get_toggle_addon_shortcut(prefs):
    """Get active shortcut item for toggle addon, or None."""
    if not hasattr(prefs, "shortcuts"):
        return None

    for item in prefs.shortcuts:
        if item.action_id == TOGGLE_ACTION_ID and getattr(item, "active", True):
            return item
    return None


__all__ = [
    "ACTION_ID_TEMPLATE_MENU",
    "ACTION_ID_FLIP_MENU",
    "ACTION_ID_QUICK_LINK",
    "ACTION_ID_QUICK_ASSIGN",
    "ACTION_ID_CYCLE_LIGHTS",
    "ACTION_ID_SOLO_LIGHT",
    "ACTION_ID_SCALE_AXIS_MENU",
    "ACTION_ID_TOGGLE_POSITIONING_MODE",
    "ACTION_ID_TOGGLE_SMART_MODE",
    "ACTION_ID_SELECT_ALL_LIGHTS",
    "ACTION_ID_TOGGLE_ADDON",
    "STANDARD_ACTION_IDS",
    "TOGGLE_ACTION_ID",
    "DEFAULT_SHORTCUTS",
    "ensure_default_shortcuts",
    "reset_shortcuts_to_default",
    "iter_standard_shortcuts",
    "get_toggle_addon_shortcut",
]
