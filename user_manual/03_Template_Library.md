# Part 3: Template Library (40+ Templates)

**LumiFlow User Manual - Part 3 of 5**

---

## Table of Contents

- [Template System Overview](#template-system-overview)
- [Studio & Commercial Templates](#studio--commercial-templates-12)
- [Dramatic & Cinematic Templates](#dramatic--cinematic-templates-10)
- [Environment & Realistic Templates](#environment--realistic-templates-12)
- [Utilities & Single Lights](#utilities--single-lights-6)
- [How to Apply Templates](#how-to-apply-templates)
- [Template Customization](#template-customization)

---

## Template System Overview

### What Are Templates?

Templates are pre-configured professional lighting setups that can be applied to your scene in one click. Each template includes:

- **Multiple lights** positioned professionally
- **Optimized properties** (power, size, color)
- **Intelligent positioning** based on your subject
- **Industry-standard configurations** used by professionals

### Template Categories

LumiFlow currently includes **15 templates** organized into 4 categories:

| Category | Templates | Best For |
|----------|-----------|----------|
| **Studio & Commercial** | 6 | Product photography, portraits, e-commerce |
| **Dramatic & Cinematic** | 1 | Film, storytelling, dramatic moods |
| **Environment & Realistic** | 1 | Outdoor scenes, natural lighting |
| **Utilities & Single Lights** | 7 | Building blocks, custom setups |

### Template Dialog Options

When applying any template, you'll see a dialog with options:

**Camera Relative**
- ✅ Checked: Position lights relative to camera view
- ⬜ Unchecked: Position lights relative to subject
- *Note: Only shown if cameras exist in scene*

**Preserve Existing Lights**
- ✅ Checked: Keeps existing lights in scene
- ⬜ Unchecked (Default): Removes existing lights based on assignment mode before applying template
  - In SCENE mode: removes lights with `G_` prefix (global lights)
  - In CAMERA mode: removes lights with `C_XX_` prefix matching active camera

**Material Adaptation**
- ✅ Checked (Default): Analyzes materials and adjusts lighting automatically
- ⬜ Unchecked: Uses default template lighting without material adjustments

**Auto-Scale**
- ✅ Enabled by default: Automatically adjusts light distance and size based on scene bounds
- Light distances scale with object size for consistent results

**Recommendation:** For first-time use, use default settings (Preserve Existing unchecked to replace old lights).

---

## Complete Template Library

LumiFlow currently includes **15 professional lighting templates** organized into 4 categories.

### Studio & Commercial Templates (6)

Professional lighting for product photography, portraits, and commercial work.

| # | Template Name | Lights | Best For |
|---|--------------|--------|----------|
| 1 | Three-Point Setup | 3 | Standard portrait, interview, professional look |
| 2 | High-Key E-commerce | 4 | Bright product shots with white background |
| 3 | Clamshell Beauty | 5 | Beauty shots, jewelry, high-end products |
| 4 | Product Hero Shot | 3 | Dramatic product advertising |
| 5 | Catalog Product | 4 | Clean catalog photography |
| 6 | Jewelry Macro | 4 | Macro jewelry photography with sparkle |

*More studio templates coming in future updates*

### Dramatic & Cinematic Templates (1)

Professional storytelling lighting for film, video, and dramatic scenes.

| # | Template Name | Lights | Best For |
|---|--------------|--------|----------|
| 1 | Dramatic Portrait | 4 | Intense characters, powerful mood, cinematic scenes |

*More dramatic templates coming in future updates*

### Environment & Realistic Templates (1)

Natural lighting simulation for outdoor and realistic indoor scenes.

| # | Template Name | Lights | Best For |
|---|--------------|--------|----------|
| 1 | Overcast Day | 4 | Soft cloudy day lighting, natural outdoor scenes |

*More environment templates coming in future updates*

### Utilities & Single Lights (7)

Building blocks for custom lighting setups - applied instantly without dialog.

| # | Template Name | Lights | Use Case |
|---|--------------|--------|----------|
| 1 | Key Light Only | 1 | Main illumination, starting point |
| 2 | Fill Light Only | 1 | Shadow softening, secondary light |
| 3 | Rim Light Only | 1 | Edge definition, separation |
| 4 | Backlight Only | 1 | Silhouettes, dramatic backlighting |
| 5 | Top-Down Light | 1 | Flat lay, overhead product shots |
| 6 | Single Sun | 1 | Natural outdoor sun simulation |
| 7 | Single Spot | 1 | Focused accent lighting |

**Note:** Template configurations (light positions, intensities, colors) are optimized based on industry standards and include automatic material adaptation. Use templates as professional starting points, then customize to your specific needs.

---

## How to Apply Templates

### Basic Application

1. **Select Subject**
   - Click on object(s) you want to light
   - Multiple objects can be selected

2. **Choose Template**
   - Click template button in panel
   - Or browse template categories

3. **Configure Dialog** (for non-utility templates)
   - Review options (Camera Relative, Preserve Existing, Material Adaptation)
   - Use defaults for first-time: Preserve Existing unchecked to replace old lights
   - Click OK

4. **Lights Created**
   - Check Outliner for new lights
   - View in camera mode (`Numpad 0`)
   - Switch to Material Preview (`Z` key → Material Preview)

### Advanced Options

**Multiple Objects:**
- Select all objects before applying template
- Template calculates bounds of all objects
- Lights position based on group center

**Camera-Relative Positioning:**
- Toggle "Camera Relative" to position lights based on camera view
- When disabled, lights position relative to subject center
- Useful for matching lighting to specific camera angles

**Preserve Mode:**
- Check "Preserve Existing Lights"
- Template adds to existing setup
- Good for layering multiple templates

---

## Template Customization

### After Applying a Template

Templates are just starting points - customize freely!

**1. Reposition Lights**
- Use positioning modes (Highlight, Normal, Target, etc.)
- Manually move lights with `G` key
- Use Orbit mode to rotate around subject

**2. Adjust Properties**
- Use Smart Controls (`MMB` drag)
- Modify power, distance, temperature
- Change light size and softness

**3. Add/Remove Lights**
- Add more lights with `Ctrl+Shift+A`
- Delete unwanted lights (`X` key)
- Duplicate lights (`Shift+D`)

**4. Color Grading**
- Use Temperature control for subtle color shifts
- Or manually set RGB color in light properties
- Mix warm and cool for visual interest

**5. Light Linking**
- Use `Ctrl+Shift+X` to link lights to specific objects
- Create groups for complex scenes
- Selective lighting control

### Saving Custom Templates

Unfortunately, saving custom templates as new presets is not yet available in v1.0.0.

**Workaround:**
- Save different .blend files as your template library
- Append lights from other .blend files (`File > Append`)
- Use Blender's Asset Browser (Blender 3.0+)

---

## Template Usage Tips

### Choosing the Right Template
- Match template category to your subject and mood
- Studio templates: portraits, products, commercial work
- Dramatic templates: storytelling, film, emotional scenes
- Environment templates: outdoor/indoor realistic lighting
- Utility templates: building blocks for custom setups

### Best Practices
- Start with defaults, customize after application
- Use "Preserve Existing" to layer multiple templates
- Utilities/Single Lights apply instantly without dialog
- Templates auto-scale to scene size for consistent results
- Experiment freely - templates are non-destructive
- Study professional positioning after applying templates

---

## Next Steps

**Excellent!** You now know the template system and how to use it effectively!

### Continue to Part 4

In **Part 4: Advanced Features**, you'll master:
- 6 Positioning Modes in detail
- 6 Smart Control types
- Camera Assignment System workflows
- Light Linking advanced techniques
- Flip Operations

👉 **[Continue to Part 4 →](04_Advanced_Features.md)**

---

## Quick Links

- [← Back to Part 2](02_Getting_Started_Core_Features.md)
- [Back to Index](00_INDEX.md)
- [Part 4: Advanced Features →](04_Advanced_Features.md)

---

**Master the Templates!** 🎨✨
