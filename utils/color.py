"""
Color Utilities
Contains all color-related utility functions: HSV/RGB conversions, Kelvin temperature, etc.
"""

import math
import bpy


def lumi_rgb_to_hsv(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert RGB values to HSV."""
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    v = max_val
    s = 0 if max_val == 0 else diff / max_val
    
    if diff == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360
    
    return h, s, v


def lumi_hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    """Convert HSV values to RGB."""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return r + m, g + m, b + m


def lumi_kelvin_to_rgb(kelvin: float) -> tuple[float, float, float]:
    """Convert color temperature in Kelvin to RGB values."""
    kelvin = max(1000, min(20000, kelvin))
    temp = kelvin / 100.0
    
    # Calculate red
    if temp <= 66:
        red = 255
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = max(0, min(255, red))
    
    # Calculate green
    if temp <= 66:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
    else:
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
    green = max(0, min(255, green))
    
    # Calculate blue
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = temp - 10
        blue = 138.5177312231 * math.log(blue) - 305.0447927307
        blue = max(0, min(255, blue))
    
    return (red / 255.0, green / 255.0, blue / 255.0)


def lumi_rgb_to_kelvin(r: float, g: float, b: float) -> float:
    """Convert RGB color values back to approximate Kelvin temperature."""
    # Convert to 0-255 range
    r_255 = max(0, min(255, r * 255))
    g_255 = max(0, min(255, g * 255))
    b_255 = max(0, min(255, b * 255))
    
    # Handle pure white case first
    if r_255 == 255 and g_255 == 255 and b_255 == 255:
        return 6500  # Pure white = daylight white
    
    # Handle near-white cases (high values across all channels)
    if r_255 > 240 and g_255 > 240 and b_255 > 240:
        # Very light colors, closer to daylight
        return 6000 + ((r_255 + g_255 + b_255) / 765.0) * 1000
    
    # Calculate color temperature based on red/blue ratio
    # This is the key indicator for warm vs cool colors
    if r_255 > b_255:
        # Warm color (more red than blue) - lower kelvin
        red_blue_ratio = r_255 / max(b_255, 1)  # Avoid division by zero
        
        if red_blue_ratio > 1.5:
            # Very warm (reddish/orange)
            kelvin = 2000 + (g_255 / 255.0) * 1500
        elif red_blue_ratio > 1.2:
            # Warm (yellowish)
            kelvin = 3000 + (g_255 / 255.0) * 1000
        else:
            # Slightly warm
            kelvin = 4000 + (g_255 / 255.0) * 1000
    else:
        # Cool color (more blue than red) - higher kelvin
        blue_red_ratio = b_255 / max(r_255, 1)  # Avoid division by zero
        
        if blue_red_ratio > 1.5:
            # Very cool (bluish)
            kelvin = 8000 + ((blue_red_ratio - 1.5) * 2000)
        elif blue_red_ratio > 1.2:
            # Cool (bluish-white)
            kelvin = 6500 + ((blue_red_ratio - 1.2) * 3000)
        else:
            # Slightly cool
            kelvin = 5000 + ((blue_red_ratio - 1.0) * 3000)
    
    # Fine-tune based on green channel (green affects perceived warmth)
    green_factor = g_255 / 255.0
    if r_255 > b_255:
        # For warm colors, more green = slightly higher kelvin
        kelvin += green_factor * 200
    else:
        # For cool colors, more green = slightly lower kelvin
        kelvin -= green_factor * 200
    
    # Clamp to valid range
    return max(1000, min(20000, kelvin))


def lumi_apply_kelvin_to_lights(context: bpy.types.Context, kelvin: float):
    """Apply Kelvin temperature color to selected lights."""
    # # Ambil objek yang dipilih dalam scene
    selected_lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
    if selected_lights:
        rgb = lumi_kelvin_to_rgb(kelvin)
        for light in selected_lights:
            light.data.color = rgb


# Export all color utilities
__all__ = [
    'lumi_rgb_to_hsv',
    'lumi_hsv_to_rgb', 
    'lumi_kelvin_to_rgb',
    'lumi_rgb_to_kelvin',
    'lumi_apply_kelvin_to_lights'
]


