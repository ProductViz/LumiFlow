# Part 1: Introduction & Installation

**LumiFlow User Manual - Part 1 of 5**

---

## Table of Contents

- [Introduction](#introduction)
- [What is LumiFlow?](#what-is-lumiflow)
- [Key Features](#key-features)
- [Who is LumiFlow For?](#who-is-lumiflow-for)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [First-Time Setup](#first-time-setup)

---

## Introduction

Welcome to **LumiFlow** - your professional lighting companion for Blender! This manual will guide you through everything you need to know to master lighting in Blender, from basic setups to advanced multi-camera workflows.

### What is LumiFlow?

**LumiFlow** is a free, open-source Blender addon that revolutionizes 3D lighting workflows. It combines intelligent automation with professional-grade templates to help artists create stunning lighting setups in seconds rather than hours.

**Think of LumiFlow as your personal lighting director** - it understands your scene, suggests optimal light placement, and provides intuitive controls for fine-tuning every aspect of your lighting.

### Philosophy

LumiFlow is built on three core principles:

1. **Accessibility** - Professional lighting should be available to everyone, not just experts
2. **Speed** - Reduce lighting setup time from hours to minutes
3. **Quality** - Deliver professional, industry-standard results

---

## Key Features

### 🌟 Smart Lighting System

Core of LumiFlow's workflow:

- **Intelligent Light Placement** – Places lights based on scene geometry and subject context
- **Scene-Aware Templates** – Uses templates tuned for studio, cinematic, environment, and utility use cases
- **Context-Aware Behavior** – Works together with positioning modes, smart controls, and overlays

### 📷 Scene & Camera Assignment

Organize lights for single- and multi-camera projects:

- **Scene Mode** – Global lights visible in all cameras
- **Camera Mode** – Assign lights to specific cameras
- **Automatic Switching** – Lights show/hide when changing cameras
- **Organized Naming** – Clear prefixes (G_ for global, C_XX_ for camera)

### 💡 Smart Light Addition

Fast ways to add lights exactly where you need them:

- **Smart Light & Template Menu (`Ctrl+Shift+A`)** – Add Blender lights on the hovered mesh or apply templates to selected objects
- **Quick Smart Light (`Ctrl+Shift+Right Mouse`)** – Drop a Rectangle Area Light directly on the hovered mesh with smart distance and orientation

### 🎛️ Smart Controls

Real-time property adjustments with mouse gestures:

- **Distance Control** – Move lights closer or farther
- **Power Control** – Adjust light intensity
- **Scale Control** – Change light size/radius
- **Angle Control** – Modify spot light spread, area light spread (Cycles only)
- **Blend Control** – Soft vs hard shadows
- **Temperature Control** – Warm to cool color shifts

### 🎯 Positioning Tools

6 intelligent positioning modes that understand your scene:

- **Highlight Mode** – Position lights at specular highlights
- **Normal Mode** – Align with surface normals
- **Target Mode** – Point lights at objects
- **Orbit Mode** – Rotate around subjects
- **Free Mode** – Manual XYZ positioning
- **Move Mode** – Interactive drag-based movement

### 🔗 Quick Light Linking

Control which lights affect which objects:

- **Quick Link** – One-click light-to-object linking
- **Object Groups** – Create reusable object collections
- **Include/Exclude Modes** – Selective lighting control
- **Collection Support** – Work with existing Blender collections

### 🗂️ Template Library (15 Professional Setups)

Pre-designed lighting setups covering major use cases:

- **Studio & Commercial** – Product photography, packshots, portraits, e-commerce
- **Dramatic & Cinematic** – Film noir, horror, action, romance
- **Environment & Realistic** – Daylight, golden hour, night scenes
- **Utilities & Single Lights** – Individual light types and utility setups for custom builds

### 💼 Light Management

Tools to keep complex scenes under control:

- **Cycle Lights** – Quickly move focus between lights in the scene
- **Solo Light** – Isolate a single light to fine-tune contribution
- **Consistent Naming & Collections** – Lights organized under LumiFlow collections

### 🎨 Visual Feedback System

Real-time viewport overlays:

- **Light Icons & Direction Arrows** – See light type and orientation at a glance
- **Distance Indicators** – Visual distance feedback from light to subject
- **Tips & Info Overlays** – On-screen guides for controls, modes, and active operations

### ⌨️ Keyboard Shortcuts

Streamlined workflow with intuitive shortcuts:

- **L** – Enable/disable addon
- **P** – Toggle positioning mode
- **F** – Toggle smart control mode
- **D** – Cycle through lights
- **Ctrl+Shift+A** – Smart Light & Template menu (add light on hovered mesh or apply templates)
- **Ctrl+Shift+Right Mouse** – Quick Smart Light (Rectangle Area on hovered mesh)
- **Ctrl+Shift+C** – Flip operations menu
- **Ctrl+Shift+X** – Quick link to objects
- **Ctrl+Shift+D** – Solo active light
- **Smart Controls:** *modifier key + MMB drag* – Adjust distance, power, size, angle, blend, and temperature
- **Positioning Tools:** *modifier key + LMB drag* – Move, orbit, and refine light placement in the viewport

---

## Who is LumiFlow For?

LumiFlow is primarily designed for **product visualization** and 3D product rendering, but it also supports a wide range of Blender lighting workflows.

### 🛍️ Product Visualization & 3D Product Artists

Ideal for e-commerce, packaging, industrial, and marketing renders:
- Professional 3-point and studio-style lighting templates
- Highlight positioning for glossy and reflective materials
- Auto-scaling for products of different sizes

### 👤 Portrait & Character Artists

Ideal for character lighting and portraits:
- Classic portrait setups (Rembrandt, beauty, dramatic)
- Hair and rim light configurations
- Temperature control for skin tones

### 🏗️ Architectural Visualizers

Essential for interior and exterior renders:
- Natural window light simulation
- Indoor and outdoor environment templates
- Normal positioning for wall-mounted lights

### 🎬 Filmmakers & Animators

Professional cinematic lighting:
- Film noir, thriller, and action templates
- Multi-camera assignment system
- Solo light mode for testing individual lights

### 🎓 Students & Beginners

Learn professional lighting techniques:
- Pre-made templates teach lighting principles
- Visual feedback shows light behavior
- Easy-to-understand interface

### 💼 Professionals

Speed up production workflows:
- Batch light creation and adjustment
- Template-based rapid prototyping
- Keyboard-driven efficiency

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Blender Version** | 4.2.0 or higher |
| **Operating System** | Windows 10, macOS 12, Ubuntu 20.04 |
| **RAM** | 4GB |
| **GPU** | OpenGL 3.3 compatible |
| **Disk Space** | 50MB for addon |

### Recommended Requirements

| Component | Recommendation |
|-----------|----------------|
| **Blender Version** | 4.5.0 or higher |
| **Operating System** | Windows 11, macOS 14, Ubuntu 22.04 |
| **RAM** | 8GB or more |
| **GPU** | Modern GPU with 4GB VRAM |
| **Display** | 1920x1080 or higher |

### Tested Platforms

✅ **Windows**
- Windows 10 (64-bit)
- Windows 11

✅ **macOS**
- macOS Big Sur (11.x)
- macOS Monterey (12.x)
- macOS Ventura (13.x)
- macOS Sonoma (14.x)
- Both Intel and Apple Silicon supported

✅ **Linux**
- Ubuntu 20.04, 22.04, 24.04
- Fedora 38, 39
- Arch Linux (latest)
- Other distributions with compatible Blender versions

### Renderer Compatibility

| Renderer | Support Status |
|----------|----------------|
| **Cycles** | ✅ Full support |
| **Eevee** | ✅ Full support |
| **Workbench** | ⚠️ Limited (no light linking) |

---

## Installation

### Method 1: From GitHub Releases (Recommended)

This is the easiest and most reliable method for most users.

#### Step 1: Download the Addon

1. Visit the [LumiFlow Releases page](https://github.com/ProductViz/LumiFlow/releases)
2. Find the latest release (for example: `v1.0.0`)
3. Download the `.zip` file:
   - Look for `LumiFlow-v1.0.0.zip` in the **Assets** section
   - Click to download
4. **Important**: Do NOT extract/unzip the file!

#### Step 2: Install in Blender

1. **Open Blender**
   - Launch Blender 4.2 or higher

2. **Open Preferences**
   - Windows/Linux: `Edit > Preferences`
   - macOS: `Blender > Preferences`
   - Shortcut: `F4` then click Preferences

3. **Navigate to Add-ons**
   - Click the **Add-ons** tab on the left sidebar

4. **Install the Addon**
   - Click the **Install...** button at the top right
   - Navigate to your Downloads folder
   - Select the `LumiFlow-v1.0.0.zip` file
   - Click **Install Add-on**

5. **Enable the Addon**
   - The add-ons list will show with LumiFlow highlighted
   - Check the checkbox next to **Lighting: LumiFlow**
   - You should see the addon expand showing details

6. **Verify Installation**
   - Look for the message "Add-on enabled successfully"
   - Close Preferences window

#### Step 3: Access LumiFlow

1. In the 3D Viewport, press `N` key to open the sidebar
2. You should see a **LumiFlow** tab
3. Click the tab to open the LumiFlow panel
4. Success! LumiFlow is now installed ✅

---

### Method 2: From Gumroad

If you prefer a pay-what-you-want download or supporter bundle, you can get LumiFlow from Gumroad.

#### Step 1: Download from Gumroad

1. Visit the official Gumroad page: [https://lumiflow.gumroad.com/l/xhzmmr](https://lumiflow.gumroad.com/l/xhzmmr)
2. Choose your contribution (you can enter **0** for a free download)
3. Complete the checkout and download the `.zip` file
4. **Important**: Do NOT extract/unzip the file!

#### Step 2: Install in Blender

The installation steps are identical to Method 1:

1. Open Blender and go to **Edit > Preferences > Add-ons**
2. Click **Install...** and select the downloaded `.zip` from Gumroad
3. Enable **Lighting: LumiFlow** in the list
4. Open the **LumiFlow** tab in the 3D Viewport sidebar (`N` key) to confirm installation

---

## First-Time Setup

### Initial Configuration

Once installed, let's configure LumiFlow for optimal performance.

#### Step 1: Open LumiFlow Panel

1. Press `N` key in 3D Viewport (toggles sidebar)
2. Click the **LumiFlow** tab
3. You should see the main control panel

#### Step 2: Enable the Addon

1. Click the **Enable** button or press `L` key
2. Panel status changes to "✅ ENABLED"
3. All features are now active

#### Step 3: Choose Default Assignment Mode

Decide your default lighting mode:

- **SCENE Mode** (Default)
  - For single-camera projects
  - All lights visible everywhere
  - Simpler workflow

- **CAMERA Mode**
  - For multi-camera projects
  - Lights assigned per camera
  - Professional multi-angle setups

You can switch modes anytime, so start with **SCENE** mode for simplicity.

#### Step 4: Overlay & Utility Buttons (Optional)

Use the bottom row of icons in the LumiFlow panel to control overlays and helper tools:

1. In the LumiFlow panel, look at the **bottom icon row**.
2. From left to right, you will find:
   - **Overlay Tips (❓ icon)** – Toggle on-screen hints about active controls and modes.
   - **Overlay Info (ℹ️ icon)** – Toggle technical overlay with light data, modes, and status.
   - **Clean Viewport** – Temporarily hide Blender overlays for a clean lighting preview.
   - **Light Picker** – Enable quick light picking in the viewport for faster selection.
   - **User Guide (Help icon)** – Open the LumiFlow user guide in your browser.
   - **Check Updates** – Show the update panel to check for new LumiFlow versions.
   - **Donate** – Show the donation panel if you want to support development.

These buttons are optional, but very helpful when lighting complex product scenes.

### Console Access (Debugging)

If you encounter issues, access the console for error messages:

**Windows:**
1. `Window > Toggle System Console`
2. Console window appears showing all Blender output

**macOS/Linux:**
1. Close Blender
2. Open Terminal
3. Run: `blender` (or `/Applications/Blender.app/Contents/MacOS/blender` on macOS)
4. Blender launches with terminal showing output

### Verification Checklist

Before proceeding to Part 2, verify:

- ✅ LumiFlow panel visible in sidebar (`N` key)
- ✅ Enable button works (press `L` key)
- ✅ Assignment mode buttons functional
- ✅ Template section visible
- ✅ No error messages in console
- ✅ Blender version 4.2 or higher

---

## Troubleshooting Installation

### Issue: Addon Not Appearing

**Solutions:**
1. Ensure you downloaded the `.zip` file (not source code)
2. Verify Blender version is 4.2 or higher
3. Check `Edit > Preferences > Add-ons` - search for "LumiFlow"
4. Try unchecking and re-checking the enable checkbox
5. Restart Blender completely

### Issue: Enable Button Doesn't Work

**Solutions:**
1. Check console for error messages
2. Ensure no conflicting addons (disable other lighting addons)
3. Try fresh Blender user preferences:
   - Backup current preferences
   - Load Factory Settings
   - Reinstall addon

### Issue: Panel Not Visible

**Solutions:**
1. Press `N` key to toggle sidebar
2. Scroll down in sidebar to find LumiFlow tab
3. Check if addon is enabled in preferences
4. Try maximizing 3D Viewport area

### Issue: Shortcuts Not Working

**Solutions:**
1. Check Keymap in Preferences
2. Look for conflicts with other addons
3. Try using panel buttons instead of shortcuts
4. Reset keymap to default

---

## Next Steps

**Congratulations!** LumiFlow is now installed and ready to use! 🎉

### Continue to Part 2

In **Part 2: Getting Started & Core Features**, you'll learn:
- Your first lighting setup in 5 minutes
- Understanding the interface in detail
- Basic workflows for common scenarios
- How to use Scene vs Camera assignment modes

👉 **[Continue to Part 2 →](02_Getting_Started_Core_Features.md)**

---

## Quick Links

- [Back to Index](00_INDEX.md)
- [Part 2: Getting Started →](02_Getting_Started_Core_Features.md)
- [GitHub Issues](https://github.com/ProductViz/LumiFlow/issues)
- [Discord Community](https://discord.gg/zqrSFctH5s)

---

**Happy Lighting!** 💡✨
