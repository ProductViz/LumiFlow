# Changelog

All notable changes to LumiFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-15

### 🎉 Initial Public Release

**LumiFlow** - Smart lighting tools for Blender 4.2+

### ✨ Added

#### Core Features
- **Smart Lighting System** with intelligent light placement
- **Template Library** with 40+ professional lighting setups
  - Studio & Commercial templates
  - Dramatic & Cinematic templates
  - Environment & Realistic templates
  - Utilities & Single light templates
- **Interactive Positioning Tools**
  - Highlight, Normal, Target, Orbit, Free positioning modes
  - Real-time visual feedback in viewport
  - Camera-aware light placement

#### Light Management
- **Camera-Light Assignment System**
  - Scene mode (global lights visible to all cameras)
  - Camera mode (lights assigned to specific cameras)
  - Automatic light visibility switching on camera change
  - Organized naming conventions (G_ for global, C_XX_ for camera-specific)
- **Light Linking System**
  - Quick object group creation
  - One-click light-to-object linking
  - Support for include/exclude modes
  - Read-only light groups from collections

#### Smart Controls
- **Scroll-based Property Control**
  - Distance, Power, Size/Radius adjustment
  - Angle/Spread control for spots
  - Color temperature control
  - Blend/softness control
- **Modal Operators** for interactive manipulation
- **Batch Operations** for multiple light adjustments

#### Positioning Operations
- **6 Positioning Modes**:
  - Highlight - Position at specular highlight
  - Normal - Align with surface normal
  - Target - Point at selected objects
  - Orbit - Rotate around target
  - Free - Manual XYZ positioning
  - Move - Drag-based positioning
- **Flip Operations** - Mirror/rotate entire light setups
  - Horizontal flip, Vertical flip
  - Front/Back, Left/Right swaps
  - Camera forward/backward positioning

#### Visual Feedback System
- **Real-time Overlays**
  - Light position and direction indicators
  - Power and distance visualization
  - Interactive cursor feedback
  - Camera-based overlay system
- **Mesh Outline Overlay** for subject identification
  - LOD system for performance
  - Solid color rendering with random pastels
  - Selection-aware highlighting

#### User Interface
- **Main Control Panel** in 3D View sidebar
  - Light assignment mode selector
  - Template browser and favorites
  - Light linking controls
  - Positioning tool access
- **Pie Menus** for quick access
  - Add Light Pie (Ctrl+Shift+A)
  - Smart Template Pie
  - Flip Menu (Ctrl+Shift+C)
- **Keyboard Shortcuts**
  - L - Toggle addon
  - P - Toggle positioning mode
  - D - Cycle through lights
  - Ctrl+Shift+X - Quick link
  - Ctrl+Shift+D - Solo light

#### Technical Features
- **Performance Optimization**
  - Caching system for expensive operations
  - Debouncing for frequent updates
  - LOD system for viewport overlays
  - Memory pooling for GPU batches
- **Error Handling**
  - Comprehensive logging system
  - Graceful fallbacks for edge cases
  - User-friendly error messages
- **State Management**
  - Modal operator coordination
  - Scene update handlers
  - Camera change detection
  - Persistent light assignments

### 🔧 Technical Implementation

#### Architecture
- **Modular Design** with separated concerns
  - `core/` - State management, template system, assignment manager
  - `operators/` - Interactive tools and commands
  - `ui/` - Panels, menus, and overlays
  - `utils/` - Helper functions and utilities
- **Singleton Patterns** for global state
- **Observer Pattern** for scene updates
- **Command Pattern** for undo/redo support

#### Code Quality
- **Professional Error Handling**
  - 84 code quality improvements
  - Proper logging throughout codebase
  - No silent exception failures
- **Clean Codebase**
  - No debug print statements in production
  - Proper Python logging infrastructure
  - PEP 8 compliance (max 120 chars)
- **Type Hints & Docstrings** for maintainability

#### Compatibility
- **Blender 4.2+** support (tested up to 4.5)
- **Cross-platform** - Windows, macOS, Linux
- **GPU Compatibility** - OpenGL 3.3+

### 📚 Documentation
- Comprehensive README with features and installation
- GPL v3.0 LICENSE
- Code documentation with docstrings
- User-friendly error messages
- In-addon tooltips and help text

### 🎯 Performance
- **Optimized Rendering**
  - GPU-based mesh overlay system
  - Batch rendering for efficiency
  - Smart culling based on viewport distance
  - 4-level LOD system for distant objects
- **Fast Operations**
  - Cached template data
  - Debounced property updates
  - Efficient scene graph queries

### 🐛 Known Limitations
- Template analyzer has 37 exception handlers (non-critical, will improve in v1.1)
- Overlay system optimized for scenes with <100 objects
- Light linking requires Blender 4.2+ light linking API

### 🙏 Credits
- Blender Foundation for Blender
- Community testers and early adopters
- All contributors and supporters

---

## Future Releases

### Planned for v1.1.0
- [ ] Enhanced template analyzer error handling
- [ ] Additional studio lighting templates
- [ ] Performance improvements for large scenes
- [ ] Advanced camera integration features

### Planned for v1.2.0
- [ ] AI-assisted lighting suggestions
- [ ] Rendering integration (Cycles/Eevee optimization)
- [ ] Studio workflow tools
- [ ] Community template sharing

---

## Version History Summary

| Version | Release Date | Highlights |
|---------|--------------|------------|
| **1.0.0** | 2025-10-15 | 🎉 Initial public release with 40+ templates, smart positioning, and camera-aware lighting |

---

## Migration Guide

### From Previous Development Versions
If you were using development builds:
1. Uninstall old version completely
2. Delete `__pycache__` directories
3. Install v1.0.0 from release
4. Light assignments will be migrated automatically from naming conventions

### Breaking Changes
- None (initial release)

---

## Support & Feedback

- **Bug Reports**: [GitHub Issues](https://github.com/ProductViz/LumiFlow/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/ProductViz/LumiFlow/discussions)
- **Community**: [Discord Server](https://discord.gg/zqrSFctH5s)

---

**LumiFlow v1.0.0** - Making professional lighting accessible to everyone! 🎨✨
