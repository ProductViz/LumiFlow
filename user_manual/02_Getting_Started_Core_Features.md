# Part 2: Getting Started & Core Features

**LumiFlow User Manual - Part 2 of 5**

This part is focused on **practical usage** of LumiFlow after installation. Here you will learn:
- How to build your first lighting setup in a few minutes
- How to understand the main LumiFlow panel sections
- How core features like Smart Light, Templates, Smart Controls, and Assignment Modes fit into real workflows

Use this chapter when you want to **start lighting real scenes**, especially for product visualization.

---

## Table of Contents

- [Quick Start Guide](#quick-start-guide)
- [Understanding the Interface](#understanding-the-interface)
- [Core Features Overview](#core-features-overview)
- [Assignment Modes Explained](#assignment-modes-explained)
- [Basic Workflows](#basic-workflows)

---

## Quick Start Guide

Let's create your first professional lighting setup in just **5 minutes**!

### Your First Lighting Setup

#### Step 1: Prepare Your Scene (1 minute)

1. **Start Fresh**
   - Open Blender (File > New > General)
   - You'll see the default scene with cube, camera, and light

2. **Remove Default Light**
   - Click on the default light (cone-shaped object)
   - Press `X` key and confirm delete
   - We'll replace it with LumiFlow lights

3. **Position Your View**
   - Press `Numpad 7` for top view
   - Press `Numpad 0` to view through camera
   - Scroll to zoom if needed

**Your scene is now ready!**

#### Step 2: Enable LumiFlow (30 seconds)

1. **Open Sidebar**
   - Press `N` key in 3D Viewport
   - Sidebar appears on the right

2. **Find LumiFlow Tab**
   - Click the **LumiFlow** tab
   - Panel opens showing controls

3. **Activate Addon**
   - Press `L` key (or click Enable button)
   - Status shows "✅ ENABLED"

**LumiFlow is now active!**

#### Step 3: Apply Your First Template (1 minute)

1. **Select Your Subject**
   - Click on the cube (or your object)
   - It highlights in orange (selected)

2. **Choose a Template**
   - In LumiFlow panel, find "Quick Templates" section
   - Click **"Three-Point Setup"**
   - A dialog window appears

3. **Configure Options**
   - ✅ Check "Clear Existing Lights" (removes any old lights)
   - Leave "Auto-Scale" checked (adjusts to scene size)
   - Click **OK**

**Lights are now created!**

#### Step 4: View Your Lighting (1 minute)

1. **Enter Camera View**
   - Press `Numpad 0` to look through camera
   - You'll see your object from camera perspective

2. **Change Viewport Shading**
   - Press `Z` key to open shading menu
   - Select **"Material Preview"** or **"Rendered"**
   - You'll see realistic lighting!

3. **Observe the Setup**
   - Look in the Outliner (top-right panel)
   - You should see three new lights:
     - `G_KeyLight` (main light, brightest)
     - `G_FillLight` (soft, fills shadows)
     - `G_RimLight` (back edge lighting)

**Your object is now professionally lit!**

#### Step 5: Adjust a Light (1.5 minutes)

1. **Select a Light**
   - Click on `G_KeyLight` in viewport or Outliner
   - Light becomes active (highlighted)

2. **Adjust Light Power (Smart Controls)**
   - Hold `Shift + Middle Mouse Button (Shift + MMB)`
   - Drag mouse **left** (dimmer) or **right** (brighter)
   - Watch the HUD display showing current power value
   - Release when satisfied

3. **Adjust Light Distance (Smart Controls)**
   - Hold `Ctrl + Middle Mouse Button (Ctrl + MMB)`
   - Drag to move the light **closer** or **farther** from the subject
   - Release when positioned well

4. **Render Preview**
   - Press `F12` to render
   - See your final result!

**🎉 Congratulations!** You've created your first professional lighting setup with LumiFlow!

---

## Understanding the Interface

Let's explore every part of the LumiFlow panel in detail.

### Main Panel Layout

The LumiFlow panel is organized into logical sections from top to bottom:

```
┌─────────────────────────────┐
│    [Enable/Disable Toggle]  │  ← Master switch
├─────────────────────────────┤
│    [Assignment Mode]        │  ← Scene vs Camera
├─────────────────────────────┤
│    [Quick Templates]        │  ← 6 popular templates
├─────────────────────────────┤
│    [Positioning Controls]   │  ← enable disable positioning
├─────────────────────────────┤
│    [Smart Control]          │  ← enable disable smart control
├─────────────────────────────┤
│  [Overlay, Update & Donate] │  ← Visual feedback config
└─────────────────────────────┘
```

### Section 1: Enable/Disable Toggle

**Location:** Top of panel

**Controls:**
- Large **Enable** button (or shows "✅ ENABLED" when active)
- Status indicator

**Purpose:**
- Master switch for all LumiFlow functionality
- When disabled: All LumiFlow features are inactive
- When enabled: Full access to all tools

**Keyboard Shortcut:** `L` key

**Visual Feedback:**
- **Disabled**: Button shows "Enable" in gray
- **Enabled**: Button shows "✅ ENABLED" in green

### Section 2: Assignment Mode

**Location:** Below enable toggle

**Controls:**
- Two buttons: **SCENE** and **CAMERA**
- Only one can be active at a time

**SCENE Mode:**
- Creates global lights (prefix: `G_`)
- Lights visible in ALL cameras
- Best for: Single-camera projects, simple scenes

**CAMERA Mode:**
- Creates camera-specific lights (prefix: `C_01_`, `C_02_`, etc.)
- Lights visible only in assigned camera
- Best for: Multi-camera setups, different lighting per angle

**Visual Indicator:**
- Active mode button is highlighted/pressed
- Inactive mode button is flat

### Section 3: Quick Templates

**Location:** Middle-upper panel

**Purpose:** One-click access to the 6 most popular lighting templates

**Available Templates:**
1. **Three-Point Setup** - Classic 3-light setup (key, fill, rim)
2. **Product Shot Basic** - 2-light product photography
3. **Product Shot Advanced** - 4-light high-end product
4. **Portrait Classic** - Standard portrait lighting
5. **Dramatic Portrait** - High-contrast dramatic lighting
6. **Studio Daylight** - Simulated natural daylight

**How to Use:**
- Click any template button
- Dialog appears with options
- Configure and click OK
- Lights are created instantly

### Section 4: Positioning Controls

**Location:** Below quick templates

**Purpose:** Enable/disable positioning system

**Controls:**
- Large toggle button: **✅ POSITIONING ENABLED** / **❌ POSITIONING DISABLED**
- When enabled: All positioning modes (Highlight, Normal, Target, etc.) are active
- When disabled: Positioning system is inactive

**Keyboard Shortcut:** `P` key

**Visual Feedback:**
- **Enabled**: Button shows "✅ POSITIONING ENABLED" in green
- **Disabled**: Button shows "❌ POSITIONING DISABLED" in gray

### Section 5: Smart Control

**Location:** Below positioning controls

**Purpose:** Enable/disable smart control system for mouse-based property adjustments

**Controls:**
- Large toggle button: **✅ SMART CONTROL ENABLED** / **❌ SMART CONTROL DISABLED**
- When enabled: Mouse drag controls (Distance, Power, Scale, etc.) are active
- When disabled: Smart control system is inactive

**Additional Settings (when enabled):**
- **Scale Axis** selector: XY (Uniform), X only, Y only
- Only available for Area lights with Rectangle/Ellipse shapes
- Controls which axis to scale when using Scale control

**Keyboard Shortcut:** `F` key

**Visual Feedback:**
- **Enabled**: Button shows "✅ SMART CONTROL ENABLED" in green
- **Disabled**: Button shows "❌ SMART CONTROL DISABLED" in gray

### Section 6: Overlay Settings & Donate

**Location:** Bottom panel

**Purpose:** Configure viewport visual feedback and access support options

**Overlay Controls:**
- **Tips Button** (?) - Toggle overlay tips display
- **Info Button** (i) - Toggle overlay info display
- **Clean Viewport** - Toggle clean viewport mode
- **Light Picker** - Toggle light picker mode

**Support Controls:**
- **Help Button** (?) - Open user guide
- **Check Updates** - Toggle update panel
- **Donate** - Toggle donation panel

**Conditional Panels:**
- **Update Panel**: Shows when "Check updates" is enabled
  - Displays current version vs latest version
  - Update button when new version available
- **Donate Panel**: Shows when "Donate" is enabled
  - Links to GitHub Sponsors, Patreon, Ko-fi
  - Support information

---

## Core Features Overview

### 1. Smart Light Creation

**What it does:** Creates lights with intelligent positioning based on scene analysis

**How it works:**
- Analyzes the target object (hovered or selected)
- Calculates optimal light positions
- Sets appropriate default properties
- Names lights based on assignment mode
- Organizes in "LumiFlow Lights" collection

**Access:**
- Smart Light & Template Menu: `Ctrl+Shift+A`
- Quick Smart Light (Rectangle Area): `Ctrl+Shift+Right Mouse` on hovered mesh

**Smart Features:**
- Auto-distance based on object size
- Pivot point initialization with raycast
- Camera-aware positioning
- Automatic naming conventions

### 2. Template System

**What it does:** Applies professional lighting setups in one click

**Benefits:**
- Save hours of manual positioning
- Learn from professional setups
- Consistent quality results
- Customizable after application

**Template Categories (15 templates total):**

- **Studio & Commercial** – Product photography, packshots, portraits, e-commerce
- **Dramatic & Cinematic** – Story-driven moods (film noir, horror, action, romance)
- **Environment & Realistic** – Daylight, golden hour, night, and atmospheric setups
- **Utilities & Single Lights** – Individual lights and utility setups for custom builds

For a full list of templates and examples, see **Part 3: Template Library**.

### 3. Positioning System

**What it does:** 6 different methods to position lights precisely

**Modes:**

**Highlight Mode**
- Positions light at specular highlight
- Perfect for glossy products
- Works with camera angle

**Normal Mode**
- Aligns light with surface normal
- Great for architectural lighting
- Perpendicular wall lights

**Target Mode**
- Points light at selected objects
- Maintains current position
- Updates rotation only

**Orbit Mode**
- Rotates light around pivot
- Maintains distance
- 360° turntable lighting

**Free Mode**
- Manual XYZ coordinate input
- Precise numerical control
- Relative or absolute positioning

**Move Mode**
- Interactive mouse-based movement
- Real-time viewport feedback
- Axis constraints available

### 4. Smart Controls

**What it does:** Adjusts light properties with intuitive mouse gestures directly in the viewport.

**Control Types (via Smart Controls):**

- **Distance** – Move the light closer or farther from the subject.
- **Power** – Make the light brighter or dimmer.
- **Scale** – Change light size or radius.
- **Angle** – Control cone/spread for spot, sun, and area lights.
- **Blend** – Soften or sharpen shadows.
- **Temperature** – Make the light warmer or cooler.

**How to Use (concept):**
- Select a light.
- Use the appropriate **modifier + Middle Mouse Button (MMB)** combination.
- Drag left/right and watch the on-screen HUD feedback.
- Release to confirm the new value.

For detailed shortcut combinations and ranges, see **Part 4: Advanced Features** and **Part 5: Reference & Support**.

### 5. Light Linking System

**What it does:** Control which lights affect which objects

**Use Cases:**
- Light only the hero product, not background
- Exclude foreground objects from backlight
- Create focused spotlights on specific areas

**Modes:**

**Include Mode**
- Light ONLY affects linked objects
- Other objects receive no light from this source

**Exclude Mode**
- Light affects everything EXCEPT linked objects
- Useful for removing unwanted light

**Quick Link:** `Ctrl+Shift+X`
- Select light (active)
- Select objects
- Press shortcut
- Instant linking!

### 6. Flip Operations

**What it does:** Mirror or rotate entire lighting setups

**8 Operations:**

1. **Flip Horizontal** - Mirror across vertical plane (X-axis)
2. **Flip Vertical** - Mirror across horizontal plane (Z-axis)
3. **Front/Back Swap** - Swap lights front/back of subject
4. **Left/Right Swap** - Swap lights left/right
5. **To Camera Front** - Move lights behind subject, facing camera
6. **To Camera Back** - Move lights in front, facing away
7. **Rotate Camera Z** - 180° rotation around camera Z-axis
8. **Rotate Target Z** - 180° rotation around target Z-axis

**Access:** `Ctrl+Shift+C` (Flip menu)

**Use Case Example:**
- Set up lighting for left side of face
- Use "Flip Horizontal" to mirror for right side
- Saves time repositioning each light

### 7. Solo Light Mode

**What it does:** Isolate a single light for testing

**How to Use:**
1. Select a light
2. Press `Ctrl+Shift+D` (or use panel button)
3. All other lights hide
4. Only selected light visible

**Benefits:**
- Test individual light contribution
- Fine-tune without interference
- Understand each light's role

**Unsolo:**
- Press `Ctrl+Shift+D` again
- Or select another light and solo it

### 8. Cycle Light Selection

**What it does:** Quickly navigate through scene lights

**Keyboard:** `D` key

**Behavior:**
- Cycles through all lights in scene
- Order: Closest to camera first
- Skips non-light objects
- Wraps around to first light

**Use Case:**
- Quickly check all lights
- Adjust properties of multiple lights
- Find specific light without searching Outliner

---

## Assignment Modes Explained

Understanding Scene vs Camera modes is crucial for organizing complex lighting setups.

### SCENE Mode (Global Lights)

**Concept:** Lights visible in ALL cameras

**Naming Convention:** `G_LightName`
- `G_` = Global prefix
- Examples: `G_KeyLight`, `G_RimLight`, `G_SunLight`

**Use Cases:**
- Single-camera projects
- Environment lighting (sun, sky)
- Base lighting that should always be present
- Simple scenes

**Workflow:**
1. Set assignment mode to SCENE
2. Add lights
3. Lights automatically prefixed with `G_`
4. Visible in all cameras automatically

**Benefits:**
- Simpler to understand
- Good for beginners
- Less management overhead

### CAMERA Mode (Per-Camera Lights)

**Concept:** Lights assigned to specific cameras

**Naming Convention:** `C_XX_LightName`
- `C_` = Camera prefix
- `XX` = Camera number (01, 02, 03, etc.)
- Examples: `C_01_KeyLight`, `C_02_Backlight`

**Use Cases:**
- Multi-camera studio setups
- Different lighting for different angles
- Professional multi-shot projects
- Architectural walkthroughs

**How It Works:**
1. Active camera determines camera number
2. Lights created get camera prefix
3. When switching cameras, visibility auto-updates

**Example Scenario:**

```
Camera 1 (Front View):
  - C_01_KeyLight (visible)
  - C_01_FillLight (visible)
  - G_SunLight (visible - global)

Camera 2 (Side View):
  - C_02_KeyLight (visible)
  - C_02_RimLight (visible)
  - G_SunLight (visible - global)

When you switch to Camera 1:
  ✅ Shows: C_01_* lights + G_* lights
  ❌ Hides: C_02_* lights

When you switch to Camera 2:
  ✅ Shows: C_02_* lights + G_* lights
  ❌ Hides: C_01_* lights
```

**Workflow:**
1. Set assignment mode to CAMERA
2. Set Camera 1 as active (`Ctrl+Numpad 0`)
3. Add lights → automatically named `C_01_*`
4. Switch to Camera 2
5. Add lights → automatically named `C_02_*`
6. Switch between cameras → visibility updates automatically!

**Benefits:**
- Different lighting per camera angle
- Organized, automatic management
- Professional multi-angle workflows

### Mixed Mode Strategy

You can combine both modes in one scene:

**Global Lights (G_):** Environment, fill, base lighting
**Camera Lights (C_XX_):** Key lights, accents, specific highlights

**Example:**
```
G_SunLight - Daylight simulation (always on)
G_SkyLight - Blue sky fill (always on)
C_01_KeyLight - Front view main light
C_02_KeyLight - Side view main light
```

### Switching Between Modes

You can change mode at any time:
- Click SCENE or CAMERA button in panel
- New lights use new prefix
- Existing lights keep their prefixes

**Existing lights** don't auto-update - they maintain their original assignment.

---

## Basic Workflows

Let's walk through common scenarios step-by-step.

### Workflow 1: Product Photography

**Goal:** Professional product shot with clean lighting

**Steps:**

1. **Scene Setup**
   - Add product model (or use simple object)
   - Position camera for good angle
   - Delete default light

2. **Enable LumiFlow**
   - Press `L` key
   - Keep SCENE mode

3. **Apply Template**
   - Select product
   - Click "Product Shot Basic"
   - Check "Clear Existing Lights"
   - Click OK

4. **Adjust Key Light**
   - Select `G_KeyLight`
   - Use Highlight positioning mode
   - Click on product's glossy area
   - Light positions at highlight

5. **Fine-Tune Power**
   - Key light still selected
   - Hold `MMB`, drag right (increase power)
   - Aim for 300-500W for most products

6. **Adjust Temperature**
   - Switch to Temperature control
   - Hold `MMB`, drag
   - Try 5500K for neutral daylight
   - Or 3000K for warm studio look

7. **Render Test**
   - Press `F12`
   - Evaluate result
   - Adjust as needed

**Result:** Professional product shot in under 5 minutes!

### Workflow 2: Portrait Lighting

**Goal:** Flattering character lighting

**Steps:**

1. **Scene Setup**
   - Character model in scene
   - Camera positioned for portrait
   - Remove default light

2. **Enable LumiFlow** (`L` key)

3. **Apply Portrait Template**
   - Select character
   - Choose "Portrait Classic"
   - Apply with Auto-Scale

4. **Position Key Light**
   - Select `G_KeyLight`
   - Use Target mode
   - Point at character's face

5. **Adjust for Face Structure**
   - Use Orbit mode
   - Hold `MMB`, drag to rotate around character
   - Find flattering angle (usually 30-45°)

6. **Temperature for Skin Tone**
   - Select Fill light
   - Temperature control
   - Set to 4500K (neutral warm)

7. **Final Touches**
   - Rim light: increase power for edge definition
   - Key light: adjust distance for softness

**Result:** Professional portrait lighting!

### Workflow 3: Multi-Camera Setup

**Goal:** Different lighting for multiple camera angles

**Steps:**

1. **Scene Setup**
   - Subject in scene
   - Create 3 cameras:
     - Camera 1: Front view
     - Camera 2: Side view
     - Camera 3: Top view

2. **Switch to CAMERA Mode**
   - Click CAMERA button in panel

3. **Light Camera 1**
   - Set Camera 1 active (`Ctrl+Numpad 0`)
   - Apply "Three-Point Setup"
   - Lights created with `C_01_` prefix

4. **Light Camera 2**
   - Switch to Camera 2
   - Apply "Dramatic Portrait"
   - Lights created with `C_02_` prefix

5. **Light Camera 3**
   - Switch to Camera 3
   - Manually add lights with `Ctrl+Shift+A`
   - Lights get `C_03_` prefix

6. **Add Global Fill**
   - Switch to SCENE mode temporarily
   - Add soft area light from above
   - Creates `G_FillLight`
   - Switch back to CAMERA mode

7. **Test Camera Switching**
   - Switch through cameras with `Numpad 0`
   - Observe lights show/hide automatically
   - Each camera has its own lighting!

**Result:** Professional multi-angle setup!

### Workflow 4: Architectural Interior

**Goal:** Realistic interior lighting with natural windows

**Steps:**

1. **Scene Setup**
   - Interior room model
   - Window openings
   - Camera inside room

2. **Apply Template**
   - Select interior objects
   - Use "Indoor Natural Window"
   - Template creates window + bounce lights

3. **Position Window Light**
   - Select window light
   - Use Normal mode
   - Click on window wall
   - Light aligns perpendicular

4. **Adjust Daylight Color**
   - Window light selected
   - Temperature control: 5500K (daylight)

5. **Add Fill Light**
   - Manual add Area light
   - Position as ceiling light
   - Temperature: 4000K (interior warm)

6. **Light Linking**
   - Select ceiling light
   - Select furniture objects
   - `Ctrl+Shift+X` (Quick Link)
   - Ceiling light only affects furniture

**Result:** Realistic architectural lighting!

---

## Tips for Beginners

### Start Simple
- Begin with SCENE mode
- Use templates first before custom setups
- Master one control type at a time

### Understand the Basics
- Key light: Brightest, main illumination
- Fill light: Softens shadows
- Rim/Back light: Edge separation from background

### Learn by Templates
- Apply different templates to same scene
- Observe how lights are positioned
- Note power levels and distances
- Recreate manually to learn

### Use Viewport Shading
- `Z` key → Material Preview for quick feedback
- Rendered mode for accurate preview
- Solid mode for positioning (faster)

### Keyboard Shortcuts
- Master `L` (enable), `P` (positioning), `F` (smart control)
- Learn `D` (cycle lights) and `Ctrl+Shift+A` (template menu) early
- Smart controls: `Ctrl+MMB` (distance), `Shift+MMB` (power), `Alt+MMB` (scale)

### Save Often
- Templates are non-destructive
- Experiment freely
- Save different versions to compare

---

## Next Steps

**Great job!** You now understand LumiFlow's core features and basic workflows!

### Continue to Part 3

In **Part 3: Template Library**, you'll discover:
- Complete guide to all 15 templates
- When to use each template
- Template customization techniques
- Category-specific workflows

👉 **[Continue to Part 3 →](03_Template_Library.md)**

---

## Quick Links

- [← Back to Part 1](01_Introduction_Installation.md)
- [Back to Index](00_INDEX.md)
- [Part 3: Template Library →](03_Template_Library.md)

---

**Keep Lighting!** 💡✨
