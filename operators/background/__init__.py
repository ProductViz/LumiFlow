# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

"""
Background System Module
Provides background creation and lighting for studio photography workflows.
Separated from lighting templates - accessible via Ctrl+Shift+B.

Phase 1: Basic background creation and presets
Phase 2: Layer interaction, light linking, awareness system
"""

from .background_generator import (
    create_seamless_background,
    create_flat_backdrop,
    create_ground_plane,
    BackgroundType,
    get_existing_backgrounds,
    remove_background,
)

from .background_presets import (
    BACKGROUND_PRESETS,
    BACKGROUND_LIGHTING_PRESETS,
    get_background_preset,
    get_lighting_preset,
    get_recommended_lighting,
)

from .background_ops import (
    LUMI_OT_background_menu_call,
    LUMI_OT_apply_background,
    LUMI_OT_remove_background,
)

# Phase 2: Light linking and awareness
from .light_linking import (
    is_light_linking_available,
    apply_layer_isolation,
    clear_light_linking,
    categorize_scene_lights,
    get_background_objects,
    get_product_objects,
    LUMI_OT_apply_layer_isolation,
    LUMI_OT_clear_layer_isolation,
)

from .background_awareness import (
    analyze_background,
    analyze_product,
    get_smart_suggestions,
    should_suggest_background,
    should_suggest_isolation,
    get_recommended_lighting_for_background,
    BackgroundAnalysis,
    ProductAnalysis,
)

__all__ = [
    # Generator
    'create_seamless_background',
    'create_flat_backdrop',
    'create_ground_plane',
    'BackgroundType',
    'get_existing_backgrounds',
    'remove_background',
    
    # Presets
    'BACKGROUND_PRESETS',
    'BACKGROUND_LIGHTING_PRESETS',
    'get_background_preset',
    'get_lighting_preset',
    'get_recommended_lighting',
    
    # Operators
    'LUMI_OT_background_menu_call',
    'LUMI_OT_apply_background',
    'LUMI_OT_remove_background',
    
    # Light Linking (Phase 2)
    'is_light_linking_available',
    'apply_layer_isolation',
    'clear_light_linking',
    'categorize_scene_lights',
    'get_background_objects',
    'get_product_objects',
    'LUMI_OT_apply_layer_isolation',
    'LUMI_OT_clear_layer_isolation',
    
    # Awareness (Phase 2)
    'analyze_background',
    'analyze_product',
    'get_smart_suggestions',
    'should_suggest_background',
    'should_suggest_isolation',
    'get_recommended_lighting_for_background',
    'BackgroundAnalysis',
    'ProductAnalysis',
]
