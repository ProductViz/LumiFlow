# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Pie menus for quick access:
  - Add Light Pie (Ctrl+Shift+A)
  - Smart Template Pie
  - Flip Menu (Ctrl+Shift+C)
- Keyboard shortcuts: L (toggle addon), P (positioning), D (cycle lights), Ctrl+Shift+X (quick link), Ctrl+Shift+D (solo light)
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
