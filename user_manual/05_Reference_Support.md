# Part 5: Reference & Support

**LumiFlow User Manual - Part 5 of 5**

---

## Table of Contents

- [Complete Keyboard Shortcuts](#complete-keyboard-shortcuts)
- [Tips & Best Practices](#tips--best-practices)
- [Common Workflows by Use Case](#common-workflows-by-use-case)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Performance Optimization](#performance-optimization)
- [Community & Support](#community--support)

---

## Complete Keyboard Shortcuts

### Primary Shortcuts

| Shortcut | Function | Context |
|----------|----------|---------|
| **L** | Enable/Disable LumiFlow | Global |
| **P** | Toggle Positioning Mode | When LumiFlow enabled |
| **F** | Toggle Smart Control Mode | When LumiFlow enabled |
| **D** | Cycle Through Lights | Anytime |
| **Ctrl+Shift+A** | Template Menu (Add Light) | LumiFlow enabled |
| **Ctrl+Shift+C** | Flip Operations Menu | Lights selected |
| **Ctrl+Shift+X** | Quick Link to Objects | Light + objects selected |
| **Ctrl+Shift+D** | Solo Active Light | Light selected |

### Positioning Mode Shortcuts

**Note:** Positioning mode must be enabled (P key)

| Shortcut | Positioning Mode | Description |
|----------|------------------|-------------|
| **Ctrl + LMB Drag** | Highlight | Position at specular highlight |
| **Shift + LMB Drag** | Normal | Align perpendicular to surface |
| **Alt + LMB Drag** | Orbit | Rotate around pivot point |
| **Ctrl+Alt + LMB Drag** | Target | Point at selected objects |
| **Ctrl+Shift + LMB Drag** | Free | Manual XYZ coordinate input |
| **Shift+Alt + LMB Drag** | Move | Interactive drag positioning |

### Smart Control Shortcuts (MMB)

**Note:** Smart Control mode must be enabled (F key)

| Shortcut | Control Mode | Range |
|----------|--------------|-------|
| **Ctrl + MMB Drag** | Distance | 0.1m - 100m |
| **Shift + MMB Drag** | Power | 1W - 10,000W |
| **Alt + MMB Drag** | Scale | 0.01m - 50m |
| **Ctrl+Shift + MMB Drag** | Angle | 0° - 180° (Spot lights) |
| **Ctrl+Alt + MMB Drag** | Temperature | 1000K - 12,000K |
| **Shift+Alt + MMB Drag** | Blend | 0.0 - 1.0 (Shadow softness) |

### Mouse Controls

| Action | Function | Context |
|--------|----------|---------|
| **MMB + Drag** | Smart Control (adjust properties) | Light selected, Smart Control enabled |
| **LMB + Drag** | Positioning Mode | Positioning mode active |
| **RMB Click** | Select light/object | Viewport |
| **Scroll Wheel** | Zoom in/out | Viewport |

### Blender Standard Shortcuts (Related)

| Shortcut | Function |
|----------|----------|
| **N** | Toggle Sidebar (access LumiFlow panel) |
| **Numpad 0** | Camera View |
| **Numpad 7** | Top View |
| **Numpad 1** | Front View |
| **Numpad 3** | Side View |
| **Z** | Shading Menu (Material Preview/Rendered) |
| **F12** | Render |
| **Shift+A** | Add Object Menu |
| **X** | Delete |
| **G** | Move/Grab |
| **R** | Rotate |
| **S** | Scale |
| **Ctrl+Z** | Undo |
| **Ctrl+Shift+Z** | Redo |
| **A** | Select All |
| **Alt+A** | Deselect All |

---

## Tips & Best Practices

### General Lighting Principles

**Three-Point Lighting Basics:**
1. **Key Light** - Main light source (brightest)
2. **Fill Light** - Softens shadows (1/2 to 1/4 of key)
3. **Rim/Back Light** - Separates from background

**Light Ratios:**
- **1:1 Ratio** - Flat, even lighting (corporate, clean)
- **2:1 Ratio** - Subtle dimension (standard portrait)
- **4:1 Ratio** - Strong dimension (dramatic portrait)
- **8:1 Ratio** - Very dramatic (film noir)

**Color Temperature Rules:**
- Mix warm and cool for visual interest
- Warm = inviting, cozy, nostalgic
- Cool = clinical, modern, futuristic
- Neutral = professional, trustworthy

### LumiFlow Workflow Best Practices

**Start with Templates:**
- Don't start from scratch
- Templates teach professional techniques
- Customize after understanding the setup

**Layer Your Lighting:**
1. Apply base template
2. Test render
3. Adjust main lights (key, fill)
4. Add accent lights if needed
5. Fine-tune with Smart Controls

**Use Assignment Modes Wisely:**
- **SCENE Mode:** Simple projects, single camera
- **CAMERA Mode:** Multi-angle, professional setups
- Mix both: Global environment + per-camera keys

**Positioning Strategy:**
1. **Template** - Automatic base positioning
2. **Move Mode** - Rough visual adjustment
3. **Specific Mode** - Precise placement (Highlight, Target)
4. **Smart Controls** - Final fine-tuning

### Performance Tips

**For Large Scenes:**
- Enable LOD system in overlay settings
- Reduce icon scale
- Use Solo Light when adjusting individual lights
- Disable mesh outlines if slow

**For Rendering:**
- Use appropriate light sizes (larger = slower)
- Optimize blend values (higher = slower)
- Consider light count (40+ lights = slow)
- Use light linking to reduce calculations

**Viewport Performance:**
- Material Preview faster than Rendered
- Solid mode fastest for positioning
- Hide lights when not adjusting
- Use camera clipping for large scenes

### Organization Tips

**Naming Convention:**
- Keep LumiFlow's automatic naming
- Add descriptive suffixes: `G_KeyLight_Warm`
- Use consistent naming across projects

**Collections:**
- Keep lights in "LumiFlow Lights" collection
- Create sub-collections for complex setups
- Use Blender's outliner filters

**Scene Management:**
- Save incremental versions
- Use different .blend files for lighting tests
- Document your setup in text objects
- Screenshot your best setups for reference

### Common Mistakes to Avoid

**Too Many Lights:**
- More ≠ better
- Start with 2-3 lights, add only if needed
- Each light should have a purpose

**Ignoring Shadows:**
- Shadows create dimension
- Not all shadows are bad
- Control with fill light, not by removing shadows

**Wrong Light Types:**
- Area lights: Soft, general illumination
- Spot lights: Focused, dramatic
- Point lights: Omnidirectional, practical
- Sun lights: Parallel rays, outdoor

**Mismatched Scale:**
- Light size should match real world
- 0.5m = small softbox
- 5m = large studio softbox
- 20m = sky/environment

**Forgetting Color Temperature:**
- All lights same temperature = flat
- Mix warm/cool for visual interest
- Match real-world temperatures

---

## Common Workflows by Use Case

### Product Photography

**Goal:** Clean, professional product shots

**Setup:**
1. Enable LumiFlow (SCENE mode)
2. Apply "Product Shot Advanced"
3. Use Highlight mode on glossy areas
4. Adjust key light power (300-500W)
5. Set temperature: 5500K (neutral)

**Adjustments:**
- Rim light: Increase for edge definition
- Fill light: Decrease for more dimension
- Background: Separate lighting or exclude

**Tips:**
- White background: Use "E-commerce White Background"
- Metallic products: Multiple small highlights
- Matte products: Larger soft lights

### Portrait & Character

**Goal:** Flattering, dimensional portrait lighting

**Setup:**
1. SCENE mode
2. Apply "Portrait Classic" or "Portrait Rembrandt"
3. Use Target mode to point key at face
4. Orbit key light to find flattering angle
5. Temperature: 4500K (skin tone)

**Adjustments:**
- Hair light: Position above/behind for separation
- Fill: Adjust ratio for mood (2:1 to 8:1)
- Rim: Increase for dramatic edge

**Tips:**
- Rembrandt: Look for triangle on cheek
- Beauty: Large soft key, minimal fill
- Dramatic: Hard key, low fill ratio

### Architectural Visualization

**Goal:** Realistic interior/exterior lighting

**Setup:**
1. SCENE mode
2. Apply "Indoor Natural Window" or "Studio Daylight"
3. Use Normal mode for wall-mounted lights
4. Temperature: 5500K outside, 4000K inside
5. Light linking: Separate interior/exterior

**Adjustments:**
- Window light: Large area, soft
- Bounce light: Subtle fill opposite window
- Practicals: Visible in-scene lights

**Tips:**
- Natural light is soft and indirect
- Use light linking for zoned lighting
- Mix temperatures for realism

### Cinematic & Film

**Goal:** Dramatic storytelling lighting

**Setup:**
1. CAMERA mode (multiple angles)
2. Apply dramatic templates per camera
3. High contrast ratios (8:1 or more)
4. Use Flip operations for quick variations
5. Solo Light to test each contribution

**Adjustments:**
- Key: Hard light for drama
- Fill: Minimal or none
- Colored lights: Mood and atmosphere

**Tips:**
- Less is more in cinematic lighting
- Shadows tell story
- Each light has purpose

### Jewelry & Small Objects

**Goal:** Sparkle and detail in small objects

**Setup:**
1. SCENE mode
2. Apply "Jewelry Showcase"
3. Use Highlight mode for all lights
4. Small spot lights (not area)
5. Multiple highlight points

**Adjustments:**
- Reduce light size for sparkle
- Position for multiple sparkle points
- Use black background for drama

**Tips:**
- Small light source = more sparkle
- Multiple angles = more sparkle
- Hard lights, not soft

### Food Photography

**Goal:** Appetizing, dimensional food shots

**Setup:**
1. SCENE mode
2. Apply "Food Photography"
3. 60° angle overhead light (not directly above)
4. Side/back light for depth
5. Warm temperature (3500K-4500K)

**Adjustments:**
- Backlight: Add glow to liquids
- Side light: Texture and dimension
- Never flat overhead lighting

**Tips:**
- Warm = appetizing
- Side/back light = depth
- Avoid flat lighting

### Outdoor & Environment

**Goal:** Realistic natural lighting

**Setup:**
1. SCENE mode
2. Apply environment templates (Golden Hour, Sunny Day, etc.)
3. Sun light: Directional, hard
4. Sky light: Soft, cool fill
5. Match time of day with temperature

**Adjustments:**
- Golden Hour: 3000K, low angle
- Midday: 5500K, overhead
- Blue Hour: 8000K+, soft

**Tips:**
- Sun = hard directional
- Sky = soft fill
- Time of day affects color and angle

---

## Troubleshooting Guide

### Installation Issues

**Problem: Addon not appearing in preferences**

**Solutions:**
- Verify you downloaded the `.zip` file, not source code
- Check Blender version is 4.2 or higher
- Search "LumiFlow" in add-ons list (may need to scroll)
- Try installing in different Blender version

**Problem: Enable button doesn't work**

**Solutions:**
- Check console for error messages (Window > Toggle System Console)
- Disable other lighting addons (potential conflicts)
- Reset Blender preferences (backup first)
- Reinstall addon from fresh download

**Problem: Panel not visible**

**Solutions:**
- Press `N` key to toggle sidebar
- Check if LumiFlow tab is at bottom (scroll down)
- Ensure addon is enabled in preferences
- Restart Blender

---

### Usage Issues

**Problem: Template doesn't create lights**

**Solutions:**
- Ensure object is selected before applying
- Check that object is not hidden
- Verify LumiFlow is enabled (press `L`)
- Check console for error messages
- Try simpler template first (Three-Point Setup)

**Problem: Lights created but not visible**

**Solutions:**
- Check camera view (`Numpad 0`)
- Switch to Material Preview or Rendered (`Z` key)
- Lights may be in CAMERA mode for different camera
- Check light hide settings in Outliner
- Increase light power

**Problem: Smart Controls not working**

**Solutions:**
- Ensure light is selected (active)
- Try clicking in different viewport area
- Check MMB (middle mouse button) is working
- Verify control mode is selected
- Restart modal operator

**Problem: Positioning mode not responding**

**Solutions:**
- Click on actual object surface, not empty space
- Ensure object has mesh geometry (not empty)
- Check console for raycast errors
- Try different positioning mode
- Ensure object is not hidden from viewport

**Problem: Camera assignment not switching**

**Solutions:**
- Ensure CAMERA mode is active
- Check camera names match expected pattern
- Verify scene update handlers registered
- Save and reload file
- Check light names have correct prefix (C_XX_)

**Problem: Light linking not working**

**Solutions:**
- Verify Blender version is 4.2+ (light linking API)
- Check that objects are mesh objects
- Ensure Include/Exclude mode is set correctly
- Try unlinking and re-linking
- Check light properties panel for light linking settings

---

### Performance Issues

**Problem: Viewport lag with overlays**

**Solutions:**
- Enable LOD system in overlay settings
- Reduce icon scale to 0.5 or lower
- Disable mesh outlines
- Hide lights when not adjusting
- Use Solid shading mode for positioning
- Clear scene analysis cache if needed

**Problem: Scene analysis taking too long**

**Solutions:**
- Reduce scene complexity (fewer objects)
- Disable spatial analysis for simple scenes
- Use quick bounds calculation instead of full analysis
- Limit material analysis depth
- Enable caching for repeated operations
- Use subject classification selectively
- Disable advanced features for basic lighting

**Problem: Slow rendering**

**Solutions:**
- Reduce light count (each light = longer render)
- Decrease light blend values
- Use smaller light sizes where possible
- Enable light linking to reduce calculations
- Consider light types (area lights slower than point)

**Problem: Addon slows down Blender**

**Solutions:**
- Disable addon when not using (`L` key)
- Clear scene cache regularly
- Reduce active viewport overlays
- Check for other resource-heavy addons
- Restart Blender to clear memory
- Use scene analysis selectively (disable for simple scenes)
- Enable performance caching for repeated operations

---

### Rendering Issues

**Problem: Lights look different in final render**

**Solutions:**
- Use Rendered viewport mode for preview
- Check render engine settings (Cycles vs Eevee)
- Verify light linking is correctly set
- Check light visibility settings
- Ensure camera clipping isn't hiding lights

**Problem: Shadows too harsh/soft**

**Solutions:**
- Adjust light Blend value (0.0 = hard, 1.0 = soft)
- Change light Size (larger = softer)
- Adjust Distance (closer = softer for area lights)
- Check render samples (low samples = noisy shadows)
- Use appropriate light type (area = soft, spot = hard)

**Problem: Colors look wrong**

**Solutions:**
- Check color temperature settings
- Verify color management in render settings
- Use correct color space (sRGB for most cases)
- Check for multiple colored lights mixing
- Preview in rendered mode

---

## Frequently Asked Questions

### General

**Q: Is LumiFlow really free?**

A: Yes! LumiFlow is 100% free and open-source under GPL v3.0 license. Free for personal and commercial use.

**Q: Does LumiFlow work with Cycles and Eevee?**

A: Yes! LumiFlow works with both Cycles and Eevee render engines. Light linking requires Blender 4.2+.

**Q: Can I use LumiFlow for commercial projects?**

A: Absolutely! GPL v3.0 license allows commercial use. Create and sell renders freely.

**Q: Does LumiFlow require internet connection?**

A: No. After installation, LumiFlow works completely offline. No telemetry or online features.

### Templates

**Q: Can I save my own custom templates?**

A: Not yet in v1.0.0. Planned for future release. Current workaround: Save .blend files as template library.

**Q: Can I modify templates after applying?**

A: Yes! Templates are just starting points. Adjust freely with positioning, smart controls, or manual edits.

**Q: Why do some templates create more lights than others?**

A: Different use cases need different light counts. Product shots may need 2-4 lights, while automotive needs 5+ for reflections.

**Q: Can I mix multiple templates?**

A: Yes! Uncheck "Clear Existing Lights" when applying second template. It will add lights to existing setup.

### Camera Assignment

**Q: What happens if I rename a camera?**

A: Camera numbers stay the same. Renaming doesn't affect assignment. Light names remain unchanged.

**Q: Can I have more than 99 cameras?**

A: Naming supports C_01 through C_99. More than 99 cameras is very rare, but technically possible with manual naming.

**Q: Do global lights (G_) affect render time?**

A: No more than camera lights. Assignment is for organization, doesn't affect performance.

**Q: Can I convert SCENE lights to CAMERA lights?**

A: Yes, by renaming. Change `G_LightName` to `C_01_LightName` manually in Outliner.

### Light Linking

**Q: Does light linking work in Eevee?**

A: Yes! Light linking works in both Cycles and Eevee in Blender 4.2+.

**Q: Can one light link to multiple groups?**

A: Yes! Select light, then link to each group separately.

**Q: Does linking affect render time?**

A: Actually reduces it! Linked lights skip calculations for excluded objects.

**Q: Can I link to individual objects or just groups?**

A: Both! Quick Link works with any selection. Groups are for organization.

### Performance

**Q: How many lights is too many?**

A: Depends on hardware and scene analysis settings. Generally:
- 1-10 lights: No issues
- 10-30 lights: Monitor performance, consider LOD
- 30-50 lights: Optimize settings, use light linking
- 50+ lights: Use light linking, reduce sizes, disable advanced analysis

**Q: Does LumiFlow slow down Blender?**

A: Minimal impact when disabled. Scene analysis and overlays use GPU with LOD optimization. Advanced features like spatial analysis can be disabled for simple scenes. Performance caching helps with repeated operations.

**Q: Can I use LumiFlow on low-end hardware?**

A: Yes! Disable overlays, use Solid mode for positioning, reduce icon scale. Disable advanced scene analysis features for simple scenes. The addon uses efficient caching and LOD systems to maintain performance.

### Compatibility

**Q: What Blender versions are supported?**

A: Blender 4.2.0 and higher. Tested up to 4.5+. Light linking requires 4.2+.

**Q: Does LumiFlow work on macOS Apple Silicon?**

A: Yes! Fully compatible with Apple Silicon Macs (M1, M2, M3).

**Q: Can I use LumiFlow with other addons?**

A: Yes! LumiFlow plays nice with other addons. Disable other lighting addons if conflicts occur.

**Q: Will my old .blend files work with LumiFlow?**

A: Yes! LumiFlow doesn't modify existing data. Can add LumiFlow lights to any scene.

### Learning

**Q: I'm a beginner. Where should I start?**

A:
1. Read Part 1 (Installation) and Part 2 (Getting Started)
2. Follow Quick Start Guide (5 minutes)
3. Try different templates on simple objects
4. Progress to Part 3 (Templates) when comfortable
5. Experiment with scene analysis features for smarter lighting

**Q: What are the advanced scene analysis features?**

A: LumiFlow includes AI-inspired scene understanding:
- **Subject Classification**: Automatically detects 20+ subject types (portrait, product, architecture)
- **Material Analysis**: Adapts lighting based on material properties
- **Obstruction Detection**: Prevents lights from being placed inside objects
- **Spatial Relationships**: Understands object positioning and interactions
- These features work automatically but can be disabled for performance

**Q: How long to learn LumiFlow?**

A: Basics in 1 hour. Proficient in 1 week of practice. Master in 1 month.

**Q: Are there video tutorials?**

A: Community tutorials available on YouTube. Search "LumiFlow Blender". Official tutorials planned.

**Q: Where can I see example renders?**

A: Discord community (#showcase channel), Blender Artists forum, GitHub discussions.

---

## Performance Optimization

### Viewport Performance

**Optimize Overlays:**
```
☑️ Enable LOD System
☑️ Reduce Icon Scale to 0.7
☐ Disable Mesh Outlines (if not needed)
☑️ Show Light Icons (lightweight)
☐ Show Text Labels (only when needed)
```

**Viewport Shading:**
- **Positioning:** Solid mode (fastest)
- **Preview:** Material Preview (balanced)
- **Final Check:** Rendered (slowest, accurate)

**Scene Optimization:**
- Hide lights when not adjusting
- Use collections to toggle visibility
- Reduce active overlay elements
- Close unused viewport panels

### Render Performance

**Light Optimization:**
- Use appropriate light sizes (smaller = faster)
- Reduce blend values where possible
- Minimize light count (each light = longer render)
- Use light linking to reduce calculations

**Scene Optimization:**
- Optimize geometry (fewer polygons)
- Use simplified collision meshes
- Reduce sample count for tests
- Use denoising for faster renders

**Smart Rendering:**
- Test renders at low resolution
- Use render regions for specific areas
- Render layers for complex scenes
- Cache heavy calculations

### Memory Management

**Clear Cache:**
- LumiFlow caches scene analysis
- Cache clears automatically on scene changes
- Manual clear: Disable and re-enable addon

**Blender Memory:**
- Save and reopen for memory reset
- Clear orphan data regularly
- Pack external resources
- Use linked libraries for assets

---

## Community & Support

### Official Resources

**GitHub Repository:**
https://github.com/ProductViz/LumiFlow
- Source code
- Issue tracker
- Releases and downloads

**GitHub Discussions:**
https://github.com/ProductViz/LumiFlow/discussions
- Feature requests
- Community help
- Announcements

**Discord Community:**
https://discord.gg/zqrSFctH5s
- Real-time chat
- Q&A channel
- Showcase renders
- Community events

### Getting Help

**Before Asking:**
1. Read relevant manual sections
2. Check FAQ above
3. Search GitHub issues
4. Check Discord pins

**When Asking:**
- Blender version
- LumiFlow version
- Operating system
- Steps to reproduce issue
- Screenshots/error messages
- .blend file (if possible)

**Response Time:**
- Discord: Usually within hours
- GitHub: Within 1-2 days
- Community is active and helpful!

### Contributing

**Ways to Contribute:**

**Bug Reports:**
- GitHub Issues for bugs
- Include reproduction steps
- Provide system info
- Attach screenshots

**Feature Requests:**
- GitHub Discussions for requests
- Explain use case
- Mockups welcome
- Community votes on features

**Code Contributions:**
- Fork repository
- Create feature branch
- Follow coding guidelines
- Submit pull request
- See CONTRIBUTING.md

**Documentation:**
- Fix typos or improve clarity
- Add examples and use cases
- Create tutorials
- Translate (future)

**Templates:**
- Submit lighting templates
- Professional setups welcome
- Include description and use case
- Share on Discord first

### Support Development

**LumiFlow is Free Forever**

Optional ways to support:

**GitHub Sponsors:**
https://github.com/sponsors/ProductViz
- Monthly or one-time
- Most transparent
- Priority feature requests

**Ko-fi:**
https://ko-fi.com/productviz
- One-time donations
- Monthly support option

**Patreon:**
https://patreon.com/productviz
- Monthly subscriptions
- Early access to builds
- Behind-the-scenes updates

**Spread the Word:**
- Share with friends
- Post your renders
- Star on GitHub
- Review on forums

### Stay Updated

**Release Channels:**
- GitHub Releases (stable)
- Discord #announcements (news)
- GitHub Discussions (development)

**Follow Development:**
- GitHub commits (code changes)
- Monthly roadmap updates
- Community feedback sessions
- Beta testing opportunities

---

## Acknowledgments

### Special Thanks

**Blender Foundation** - For creating Blender

**Community Contributors** - For testing and feedback

**Early Adopters** - For bug reports and suggestions

**Sponsors** - For making development possible

**You!** - For using LumiFlow

---

## Conclusion

### You've Completed the LumiFlow User Manual! 🎉

You now have comprehensive knowledge of:

✅ **Installation and Setup** - LumiFlow is installed and configured  
✅ **Core Features** - Templates, positioning, controls mastered  
✅ **40+ Templates** - Professional lighting for any scenario  
✅ **Advanced Features** - Camera assignment, light linking, flip ops  
✅ **Reference** - Shortcuts, troubleshooting, FAQ

### Your Next Steps

**Practice:**
- Apply templates to different scenes
- Experiment with positioning modes
- Build custom lighting setups
- Share your renders with community

**Learn More:**
- Join Discord community
- Watch community tutorials
- Explore advanced techniques
- Contribute your knowledge

**Stay Connected:**
- Follow GitHub for updates
- Join monthly community events
- Participate in lighting challenges
- Help other beginners

---

## Quick Reference Card

### Essential Shortcuts
```
L               Enable/Disable LumiFlow
P               Toggle Positioning Mode
F               Toggle Smart Control Mode
D               Cycle Through Lights

Ctrl+Shift+A    Template Menu (Add Light)
Ctrl+Shift+C    Flip Operations Menu
Ctrl+Shift+X    Quick Link to Objects
Ctrl+Shift+D    Solo Active Light

Ctrl + MMB      Distance Control
Shift + MMB     Power Control
Alt + MMB       Scale Control
```

### Template Categories
```
Studio & Commercial (6)     Product, Portrait, E-commerce
Dramatic & Cinematic (1)    Film Noir, Horror, Action
Environment & Realistic (1) Golden Hour, Daylight, Night
Utilities & Single (7)      Building Blocks
```

### Assignment Modes
```
SCENE Mode    G_LightName      Global (all cameras)
CAMERA Mode   C_XX_LightName   Per-camera (specific)
```

### Smart Controls
```
Distance      0.1m - 100m      Move closer/farther
Power         1W - 10,000W     Brightness
Scale         0.01m - 50m      Size/softness
Angle         0° - 180°        Spot cone (spots only)
Blend         0.0 - 1.0        Shadow softness
Temperature   1000K - 12,000K  Warm to cool
```

---

## Final Words

**Professional lighting is now accessible to everyone.**

LumiFlow empowers you to create stunning lighting setups in seconds, whether you're a beginner learning fundamentals or a professional speeding up your workflow.

Remember:
- **Start simple** - Templates first, then customize
- **Practice regularly** - Lighting is a skill that improves with use
- **Join the community** - Learn from and help others
- **Have fun!** - Experiment and create beautiful art

**Thank you for choosing LumiFlow!**

We can't wait to see what you create! 🎨✨

---

## Document Information

**LumiFlow User Manual**  
**Version:** 1.0.0  
**Last Updated:** October 15, 2025  
**Language:** English  
**Format:** Markdown

**License:**  
Documentation: CC BY 4.0  
Software: GPL v3.0

**Authors:**  
LumiFlow Development Team  
Community Contributors

**Feedback:**  
GitHub Issues: https://github.com/ProductViz/LumiFlow/issues  
Discord: https://discord.gg/zqrSFctH5s

---

**End of User Manual**

[← Back to Part 4](04_Advanced_Features.md) | [Back to Index](00_INDEX.md)

**Happy Lighting!** 💡✨
