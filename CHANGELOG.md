# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [1.2.0] - 2025-11-29

### Added

- **Select All LumiFlow Lights**: Added a dedicated action to select all lights managed by LumiFlow in the current scene, with its own shortcut entry in the addon preferences.
- **Configurable LumiFlow Shortcuts**: New Shortcut Settings section in Add-on Preferences to view and customize the main LumiFlow shortcuts (Template, Flip, Quick Link/Assign, Cycle, Solo, Select All, Scale Axis, mode toggles, and toggle addon) with Apply/Reset operators and internal conflict detection between LumiFlow actions.

### Changed

- **Overlay tips & keymap icons follow preferences**: Overlay tips and key icons now read shortcut definitions from the new preference-based shortcut system (with fallback to defaults), so on-screen hints always match the currently active LumiFlow keymaps.
- **Shortcut conflict handling with Blender defaults**: Applying shortcuts now detects conflicts against Blender's default 3D View/Object Mode keymaps and shows a confirmation dialog before overriding those defaults.

### Fixed

## [1.1.0] - 2025-11-22

### Added

- **Smart Control Exposure Mode (Blender 4.5+)**: EV-based smart control for `light.data.exposure` using **Shift + Right Mouse Drag**, with adaptive sensitivity.
- **Community Discord Button**: Opening the official LumiFlow community Discord invite link in the default web browser.
- **Limit Light to Selected Object**: Option in the Apply Template dialog to restrict new lights to the selected object only.
- **Quick Smart Add Exclude Overview**: Panel section that appears when there are mesh objects excluded from Quick Smart Add, listing them with per-object toggles.
- **Viewport Scale Axis Shortcut (Alt+Q)**: Quick Scale Axis popup in the 3D View (**Alt+Q**) for Area lights with Rectangle/Ellipse shape, allowing fast switching between XY / X / Y axes used by Smart Control Scale mode.

### Changed

- **Quick Link (Ctrl+Shift+X) on Meshes**: Quick Link on selected meshes now toggles Quick Smart Add Exclude with clear INCLUDE/EXCLUDE feedback and a panel overview listing excluded meshes.
- **Viewport Overlay Toggle Tooltips**: Specific tooltips for overlay tips/info buttons: "Show overlay tips" and "Show overlay info".
- **Scale Axis UI location**: Scale Axis controls were removed from the main LumiFlow panel and are now managed only via the Alt+Q viewport popup for a cleaner, context-sensitive panel layout.
- **Viewport overlay tips & icons**: Refined selected-light tips sections and updated RMB/Q icons and Quick Smart Add/Scale Axis hints so the overlay matches the latest shortcuts.

### Fixed

- **Blender 5.0 compatibility fixes**:
  - Removed deprecated `bgl` dependency from the highlight positioning operator to avoid module import errors in Blender 5.0.
  - Relaxed context checks in the Auto Light Picker operator so it can be started from property update callbacks and non-viewport contexts in Blender 5.0.
  - Corrected addon enable toggle logic to use the `Scene.lumi_enabled` RNA BoolProperty, ensuring the panel reflects the true enabled state.
  - Fixed `KeyError: 'property not found in group'` when clearing temporary hit data by resetting temporary scene properties instead of deleting them.


## [1.0.2] - 2025-11-14

### Added
- **Direct Area Light Addition Shortcut**: Added Ctrl+Shift+Right Mouse Button shortcut to directly add Area light with RECTANGLE shape on mesh surfaces. Streamlines workflow for adding rectangle area lights without opening menus.

### Changed
- **Smart Control Sensitivity System**: Refactored to use only base sensitivity without speed/acceleration factors for more consistent control
- **Spot light cone overlay behavior**: Updated spot light cone visualization so the two front circles now follow both radius (shadow_soft_size) and spot size.
- **Documentation – README**: Updated feature list, smart light addition section, and Getting Started instructions to describe the Smart Light & Template Menu (Ctrl+Shift+A), Quick Smart Light (Ctrl+Shift+Right Mouse), 15-template library across 4 categories, and current workflows.
- **Documentation – User Manual (Parts 1–5)**: Revised all manual parts to be practical and user-focused, aligned with README and the current addon behavior: product visualization focus, GitHub+Gumroad installation, 15-template library details, updated positioning and smart control shortcuts (modifier + MMB / LMB), and refreshed reference, workflows, FAQ, and troubleshooting sections.

### Fixed
- **Excessive power in smart light addition**: Fixed unrealistically high power values by correcting base distances in photometric calculations, reducing power by 85-90% while maintaining proper illumination.
- **Overlay mesh rendering fix**: fixing performance and visual issues (81% faster, cleaner outlines)
- **Overlay tips for smart control shortcuts**: Fixed display issues where overlay tips were not showing correct shortcut information for smart control features. Now overlay tips properly display and update dynamically with the current smart control shortcuts.


## [1.0.1] - 2025-11-04

### Fixed
- **Auto-assign unassigned lights to scene**: Fixed issue where lights without camera assignment were hidden when enabling the addon. Now all unassigned lights are automatically assigned to scene (global visibility) when the enable toggle is activated, with improved logging and forced visibility updates.
- **Keymap behavior when addon disabled**: Fixed issue where all shortcuts including the toggle addon key (L) were unavailable when addon was disabled. Now the toggle addon key (L) remains always functional to allow re-enabling the addon, while all other shortcuts are properly gated behind addon enable state with operator poll methods.
- **Area light scale override with hardcoded values**: Fixed issue where AREA light scale (size and size_y) were always set to hardcoded values (1.0 for square/disk, 1.0×0.5 for rectangle/ellipse) regardless of target object size. Now scale values are properly calculated based on target object dimensions and preserved when changing area shape.
- **SUN light excessive brightness**: Fixed issue where SUN light was excessively bright (~448,000 power) due to incorrect application of inverse square law. SUN light is now treated as a directional source with base power of 15.0 (10x boost from 1.5 for brighter outdoor lighting) and clamped to 0.5-40.0 range, matching Blender best practices for outdoor/directional lighting.
- **Light picker selecting already-selected lights**: Fixed issue where light picker could re-select lights that were already selected. Now light picker only detects and selects unselected lights, improving workflow efficiency when multi-selecting lights with Shift+Click.

## [1.0.0] - 2025-10-15

### Added

#### Core Lighting System
- Smart lighting system with intelligent light placement based on scene analysis
- Scene context analysis engine with AI-inspired subject classification (20+ types)
- Material-based lighting adaptation with automatic property adjustments
- Obstruction detection for safe light positioning
- Camera-aware light placement with real-time collision avoidance

#### Template Library
- 15 professional lighting templates across 4 categories:
  - **Studio & Commercial** (6 templates): Three-Point Setup, High-Key E-commerce, Clamshell Beauty, Product Hero Shot, Catalog Product, Jewelry Macro
  - **Dramatic & Cinematic** (1 template): Dramatic Portrait
  - **Environment & Realistic** (1 template): Overcast Day
  - **Utilities & Single Lights** (7 templates): Key Light, Fill Light, Rim Light, Backlight, Top-Down Light, Single Sun, Single Spot

#### Positioning System
- 6 intelligent positioning modes:
  - **Highlight**: Position at specular highlight with material analysis
  - **Normal**: Align perpendicular to surface normal
  - **Target**: Point at selected objects while maintaining position
  - **Orbit**: Rotate around pivot point with distance preservation
  - **Free**: Manual XYZ coordinate input (relative/absolute)
  - **Move**: Interactive drag-based positioning with axis constraints

#### Smart Controls
- 6 scroll-based property controls with mouse gestures:
  - **Distance**: 0.1m - 100m range with inverse square law feedback
  - **Power**: 1W - 10,000W logarithmic scaling
  - **Scale**: 0.01m - 50m (physical size for area lights, radius for others)
  - **Angle**: 0° - 180° cone width for spot lights
  - **Blend**: 0.0 - 1.0 shadow softness
  - **Temperature**: 1000K - 12,000K color temperature
- Smart sensitivity tracking with adaptive mouse acceleration
- Modal operators for interactive manipulation
- Batch operations for multiple light adjustments

#### Light Management
- **Camera-Light Assignment System**:
  - Scene mode: Global lights visible to all cameras (G_ prefix)
  - Camera mode: Per-camera lights with automatic visibility switching (C_XX_ prefix)
  - Persistent assignments with scene update handlers
- **Light Linking System**:
  - Include/exclude modes for selective illumination
  - Object group creation and management
  - Collection-based linking integration
  - Quick link shortcut (Ctrl+Shift+X)

#### Visual Feedback System
- Real-time viewport overlays with camera-based states
- Mesh outline overlay for subject identification with LOD system
- Material adaptation indicators and obstruction warnings
- Interactive cursor feedback and power/distance visualization
- 4-level LOD system for performance optimization

#### User Interface
- Streamlined main control panel in 3D View sidebar
- Pie menus and quick access:
  - Template Menu (Ctrl+Shift+A)
  - Flip Menu (Ctrl+Shift+C)
  - Quick Link (Ctrl+Shift+X)
- Keyboard shortcuts: L (toggle addon), P (positioning), F (smart control), D (cycle lights), Ctrl+Shift+A (template menu), Ctrl+Shift+C (flip menu), Ctrl+Shift+X (quick link), Ctrl+Shift+D (solo light)
- Update panel with GitHub integration
- Donate panel with sponsorship links

#### Flip Operations
- 8 mirror/rotation operations for entire light setups:
  - Horizontal/Vertical flip
  - Front/Back and Left/Right swaps
  - Camera-relative positioning (front/back)
  - 180° rotations around camera or target Z-axis

#### Selection Tools
- Cycle light selection (D key) with camera-distance ordering
- Solo light mode (Ctrl+Shift+D) for isolation testing
- Quick light deletion and management

#### Technical Features
- Performance optimizations: Advanced caching, debouncing, memory pooling, selective scene analysis
- Comprehensive error handling with 37+ exception handlers and user-friendly messages
- State management with modal operator coordination and persistent light assignments
- Modular architecture: core/, operators/, ui/, utils/ separation
- Type hints, docstrings, and PEP 8 compliance
- Blender 4.2+ support (tested up to 4.5), cross-platform (Windows/macOS/Linux)
- GPU compatibility (OpenGL 3.3+) with batch rendering

#### Documentation
- Comprehensive user manual with 5-part structure
- Quick start guide and core features overview
- Template library reference with usage examples
- Advanced features documentation
- Reference guide with shortcuts and troubleshooting
