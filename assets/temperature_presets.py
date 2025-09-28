# LumiFlow - Smart lighting tools for Blender
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 LumiFlow Developer

# -*- coding: utf-8 -*-
"""
LumiFlow - Smart Lighting Tools for Blender
Copyright (C) 2024 Burhanuddin. All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
modification, distribution, or use of this software, via any medium,
is strictly prohibited.

For licensing inquiries: asqa3d@gmail.com
"""
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


