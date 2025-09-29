# -*- coding: utf-8 -*-
"""
LumiFlow Temperature Presets Module
Contains predefined temperature values for different lighting conditions.
"""

# Temperature presets in Kelvin
TEMPERATURE_PRESETS = {
    'candle': 1900,
    'tungsten': 2700,
    'warm_white': 3200,
    'daylight': 5500,
    'overcast': 6500,
    'shade': 7500,
    'blue_sky': 10000
}

# Export presets
__all__ = ['TEMPERATURE_PRESETS']


