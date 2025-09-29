"""
Property Utilities
Contains property update callbacks and related utility functions.
"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, StringProperty

# Import state management
from ..core.state import get_state

# Import utility functions
from .common import (
    lumi_is_addon_enabled,
    lumi_get_light_collection, 
    lumi_reset_highlight,
    lumi_move_to_collection,
    lumi_safe_context_override,
    lumi_get_object_bounds,
    lumi_sample_object_material,
    get_addon_path
)


# Property Group class definition
class LightPositioningProperties(PropertyGroup):
    """Properties for light positioning modes."""
    positioning_mode: EnumProperty(
        name="Positioning Mode",
        items=[
            ('HIGHLIGHT', 'Highlight', ''),
            ('NORMAL', 'Normal', ''),
            ('TARGET', 'Target', ''),
            ('ORBIT', 'Orbit', ''),
            ('FREE', 'Free', ''),
            ('MOVE', 'Move', ''),
            ('DISABLE', 'Disable', '')
        ],
        default='DISABLE'
    )


class ProfessionalLightingProperties(PropertyGroup):
    """Properties for professional lighting techniques."""
    # Color harmony settings
    harmony_type: EnumProperty(
        name="Harmony Type",
        items=[
            ('complementary', "Complementary", "Opposite colors on color wheel"),
            ('triadic', "Triadic", "Three colors equally spaced"),
            ('analogous', "Analogous", "Adjacent colors on color wheel"),
            ('split_complementary', "Split Complementary", "Base complement split into two"),
            ('tetradic', "Tetradic", "Rectangle on color wheel"),
            ('monochromatic', "Monochromatic", "Same hue, different saturation/brightness")
        ],
        default='complementary'
    )
    
    base_hue: bpy.props.FloatProperty(
        name="Base Hue",
        description="Base hue for color harmony (0-360 degrees)",
        default=60.0,
        min=0.0,
        max=360.0
    )
    
    saturation: bpy.props.FloatProperty(
        name="Saturation", 
        description="Color saturation intensity",
        default=0.8,
        min=0.0,
        max=1.0
    )
    
    # Cinematic mood settings
    mood_type: EnumProperty(
        name="Mood Type",
        items=[
            ('dramatic', "Dramatic", "High contrast dramatic lighting"),
            ('romantic', "Romantic", "Soft warm romantic lighting"),
            ('horror', "Horror", "Dark suspenseful horror lighting"),
            ('sci_fi', "Sci-Fi", "Cool futuristic sci-fi lighting"),
            ('film_noir', "Film Noir", "Classic black and white film lighting"),
            ('natural', "Natural", "Natural daylight lighting"),
            ('golden_hour', "Golden Hour", "Warm golden hour lighting"),
            ('blue_hour', "Blue Hour", "Cool blue hour lighting"),
            ('cyberpunk', "Cyberpunk", "Neon cyberpunk lighting"),
            ('vintage', "Vintage", "Warm vintage film lighting")
        ],
        default='dramatic'
    )
    
    # Time of day settings
    time_of_day: EnumProperty(
        name="Time of Day",
        items=[
            ('dawn', "Dawn", "Early morning dawn lighting"),
            ('morning', "Morning", "Bright morning lighting"), 
            ('midday', "Midday", "Harsh midday sun lighting"),
            ('afternoon', "Afternoon", "Warm afternoon lighting"),
            ('golden_hour', "Golden Hour", "Golden hour photography lighting"),
            ('sunset', "Sunset", "Warm sunset lighting"),
            ('twilight', "Twilight", "Soft twilight lighting"),
            ('night', "Night", "Dark night lighting"),
            ('blue_hour', "Blue Hour", "Blue hour photography lighting")
        ],
        default='golden_hour'
    )
    
    # Advanced shadow settings
    penumbra_factor: bpy.props.FloatProperty(
        name="Penumbra Factor",
        description="Soft shadow penumbra intensity", 
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    contact_shadow: bpy.props.FloatProperty(
        name="Contact Shadow Strength",
        description="Contact shadow intensity",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    shadow_density: bpy.props.FloatProperty(
        name="Shadow Density",
        description="Overall shadow density",
        default=1.0,
        min=0.0,
        max=2.0
    )
    
    negative_fill: bpy.props.FloatProperty(
        name="Negative Fill",
        description="Negative fill simulation strength",
        default=0.2,
        min=0.0,
        max=1.0
    )
    
    use_material_shadows: bpy.props.BoolProperty(
        name="Material Based Shadows",
        description="Adjust shadows based on material properties",
        default=True
    )
    
    # Professional techniques
    artistic_override: bpy.props.FloatProperty(
        name="Artistic Override",
        description="Blend between realistic (0) and artistic (1) lighting",
        default=0.3,
        min=0.0,
        max=1.0
    )
    
    # Volumetric effects
    haze_density: bpy.props.FloatProperty(
        name="Haze Density",
        description="Atmospheric haze density",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    fog_absorption: bpy.props.FloatProperty(
        name="Fog Absorption",
        description="Fog absorption strength",
        default=0.8,
        min=0.0,
        max=1.0
    )
    
    scattering: bpy.props.FloatProperty(
        name="Scattering Anisotropy",
        description="Light scattering direction (-1 to 1)",
        default=0.0,
        min=-1.0,
        max=1.0
    )
    
    godrays_strength: bpy.props.FloatProperty(
        name="God Rays Strength",
        description="God rays intensity",
        default=0.5,
        min=0.0,
        max=2.0
    )


def lumi_enabled_update(self, context: bpy.types.Context):
    """Update callback when addon is enabled/disabled."""
    state = get_state()
    scene = context.scene  # Define scene variable for both cases
    
    if self.lumi_enabled:
        state.scroll_control_enabled = True
        # Close other panels when enabled
        scene.lumi_light_linking_expanded = False
        scene.lumi_color_enabled = False
        # Addon enabled - activating features
        
        # Force scene update to trigger overlay activation
        # This ensures all handlers are activated through the proper scene update mechanism
        try:
            # Tag scene for update to trigger lumi_scene_update_handler
            if hasattr(bpy.context, 'scene') and bpy.context.scene:
                bpy.context.scene.update_tag()
                # Scene tagged for update to activate overlays
                
            # Also call scene update handler directly as backup
            # This ensures overlays are activated immediately
            from ..overlay import lumi_scene_update_handler
            if hasattr(bpy.context, 'scene') and bpy.context.scene:
                # Create a dummy depsgraph for the call
                lumi_scene_update_handler(bpy.context.scene, bpy.context.evaluated_depsgraph_get())
                # Scene update handler called directly
                
            # Initialize Camera Light system when addon is enabled
            try:
                from ..core.camera_manager import get_camera_light_manager
                camera_manager = get_camera_light_manager()
                
                # Try to initialize with available context
                # CameraLightManager already has internal context validation
                camera_manager.initialize_system(context)
                print("🔧 Camera Light System initialization triggered")
                
            except Exception as e:
                # If failed, try delayed initialization through manager
                try:
                    from ..core.camera_manager import get_camera_light_manager
                    camera_manager = get_camera_light_manager()
                    camera_manager._schedule_delayed_initialization()
                    print("📅 Camera Light System delayed initialization scheduled")
                except Exception as e2:
                    print(f"❌ Camera Light System initialization failed: {e2}")
                
        except Exception as e:
            # Error in overlay activation - pass silently
            pass
    else:
        # Proper cleanup when disabled
        # Addon disabled - cleaning up
        state.scroll_control_enabled = False
        scene.lumi_scroll_control_enabled = False
        
        # Clean up overlay handlers
        try:
            from ..overlay import (
                lumi_disable_draw_handler,
                lumi_disable_overlay_draw_handler,
                lumi_disable_stroke_overlay_handler,
                lumi_disable_tips_overlay_handler,
                lumi_disable_cursor_overlay_handler
            )
            lumi_disable_draw_handler()
            lumi_disable_overlay_draw_handler()
            lumi_disable_stroke_overlay_handler()
            lumi_disable_tips_overlay_handler()
            lumi_disable_cursor_overlay_handler()
            
            # Cleanup Camera Light system when addon is disabled
            try:
                from ..core.camera_manager import get_camera_light_manager
                camera_manager = get_camera_light_manager()
                camera_manager.cleanup_system(context)
                print("🔧 Camera Light System cleanup completed")
            except Exception as e:
                print(f"❌ Camera Light System cleanup failed: {e}")
            
        except Exception as e:
            print(f"LumiFlow: Error in overlay cleanup: {e}")

def lumi_overlay_update(self, context: bpy.types.Context):
    """Update callback when overlay info property changes."""
    # Force redraw of all 3D viewports
    try:
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        status = "enabled" if self.lumi_overlay_info_enabled else "disabled"
    except Exception:
        pass


def lumi_color_enabled_update(self, context: bpy.types.Context):
    """Update callback for Color Controls - mutual exclusion with Light Linking Manager."""
    try:
        # If Color Controls expanded, Light Linking Manager must collapse
        if self.lumi_color_enabled:
            self.lumi_light_linking_expanded = False
    except Exception as e:
        pass


def lumi_light_linking_expanded_update(self, context: bpy.types.Context):
    """Update callback for Light Linking Manager - mutual exclusion with Color Controls."""
    try:
        # If Light Linking Manager expanded, Color Controls must collapse
        if self.lumi_light_linking_expanded:
            self.lumi_color_enabled = False
    except Exception as e:
        pass


# =====================================================================
# ACCORDION BEHAVIOR FUNCTIONS
# =====================================================================

def accordion_update_handler(property_name, context):
    """Generic accordion handler that closes all other sections when one opens."""
    all_sections = [
        "lumi_color_controls_expanded",
        "lumi_light_mixer_expanded", 
        "lumi_template_settings_expanded",
        "lumi_template_browser_expanded",
        "lumi_light_linking_expanded",
        "lumi_scroll_settings_expanded"
    ]
    scene = context.scene
    # Only close others if current section is being opened
    if getattr(scene, property_name, False):
        for section in all_sections:
            if section != property_name and hasattr(scene, section):
                setattr(scene, section, False)


class LightControlProperties(PropertyGroup):
    """Centralized properties for light control operators."""
    # Distance control
    distance: bpy.props.FloatProperty(
        name="Distance from Target",
        description="Distance of light from target/pivot",
        default=5.0,
        min=0.1,
        max=20.0,
        unit='LENGTH'
    )
    
    # Power control
    power: bpy.props.FloatProperty(
        name="Light Power",
        description="Light energy/power",
        default=1.0,
        min=0.001,
        max=1000.0
    )
    
    # Scale/Size controls
    scale: bpy.props.FloatProperty(
        name="Light Size",
        description="Light size/radius",
        default=1.0,
        min=0.01,
        max=100.0,
        unit='LENGTH'
    )
    
    # Area light size controls
    scale_x: bpy.props.FloatProperty(
        name="Size X",
        description="Area light size X (width)",
        default=1.0,
        min=0.01,
        max=100.0,
        unit='LENGTH'
    )
    
    scale_y: bpy.props.FloatProperty(
        name="Size Y",
        description="Area light size Y (height)",
        default=1.0,
        min=0.01,
        max=100.0,
        unit='LENGTH'
    )
    
    # Temperature control
    temperature: bpy.props.FloatProperty(
        name="Color Temperature",
        description="Color temperature in Kelvin",
        default=6500,
        min=800,
        max=20000
    )
    
    # Angle control (for spot size, sun angle, etc.)
    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Light angle / spot size / sun angle",
        default=0.0,
        min=0.0,
        max=3.1415926
    )
    
    # Blend control (spot blend/falloff)
    blend: bpy.props.FloatProperty(
        name="Blend",
        description="Spot blend / falloff",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    # Spread control (area light spread)
    spread: bpy.props.FloatProperty(
        name="Spread",
        description="Area light spread (0..1)",
        default=0.0,
        min=0.0,
        max=1.0
    )
    
    # Mode selection
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('DISTANCE', 'Distance', 'Distance mode'),
            ('POWER', 'Power', 'Power mode'),
            ('SCALE', 'Scale', 'Scale mode'),
            ('ANGLE', 'Angle', 'Angle mode'),
            ('SPOT_SIZE', 'Spot Size', 'Spot size mode'),
            ('TEMPERATURE', 'Temperature', 'Temperature mode'),
            ('BLEND', 'Blend', 'Blend mode'),
        ],
        default='POWER'
    )


# Individual update functions for each accordion section
def lumi_color_controls_expanded_update(self, context):
    """Update callback for Color Controls accordion."""
    accordion_update_handler("lumi_color_controls_expanded", context)


def lumi_light_mixer_expanded_update(self, context):
    """Update callback for Light Mixer accordion."""
    accordion_update_handler("lumi_light_mixer_expanded", context)


def lumi_template_settings_expanded_update(self, context):
    """Update callback for Template Settings accordion."""
    accordion_update_handler("lumi_template_settings_expanded", context)


def lumi_template_browser_expanded_update(self, context):
    """Update callback for Template Browser accordion."""
    accordion_update_handler("lumi_template_browser_expanded", context)




def lumi_light_linking_expanded_accordion_update(self, context):
    """Update callback for Light Linking accordion."""
    accordion_update_handler("lumi_light_linking_expanded", context)


def lumi_scroll_settings_expanded_update(self, context):
    """Update callback for Scroll Settings accordion."""
    accordion_update_handler("lumi_scroll_settings_expanded", context)


# Export all property utilities
__all__ = [
    'LightPositioningProperties',
    'LightControlProperties',
    'ProfessionalLightingProperties',
    'lumi_enabled_update',
    'lumi_overlay_update', 
    'lumi_color_enabled_update',
    'lumi_light_linking_expanded_update',
    'accordion_update_handler',
    'lumi_color_controls_expanded_update',
    'lumi_light_mixer_expanded_update',
    'lumi_template_settings_expanded_update',
    'lumi_template_browser_expanded_update',
    'lumi_light_linking_expanded_accordion_update',
    'lumi_scroll_settings_expanded_update'
]

