# Part 3: Interface & Core Features

**LumiFlow User Manual – Part 3 of 6**

This part explains **where everything is** in the LumiFlow panel and how the **core systems** fit together.

Use this chapter as a **map**:
- Part 2 shows you **what to do** step‑by‑step.
- Part 3 shows you **what each button and system does**, with short usage examples.

---
## 1. Understanding the Interface

The LumiFlow panel is organized from **top to bottom** in the order you typically use it:

```text
┌─────────────────────────────┐
│    [Enable/Disable Toggle]  │  ← Master switch
├─────────────────────────────┤
│    [Assignment Mode]        │  ← Scene vs Camera
├─────────────────────────────┤
│    [Quick Templates]        │  ← Popular one‑click templates
├─────────────────────────────┤
│    [Positioning Controls]   │  ← Turn positioning system on/off
├─────────────────────────────┤
│    [Smart Control]          │  ← Turn Smart Controls on/off
├─────────────────────────────┤
│ [Overlay, Update & Support] │  ← Overlays, updates, donate, community
└─────────────────────────────┘
```

---

## 2. Panel Sections

### Section 1: Enable/Disable Toggle

**Location:** Top of the LumiFlow panel.

**Controls:**
- Large **Enable** button (or shows "✅ ENABLED" when active).

**Purpose:**
- Master switch for LumiFlow.
- When disabled: LumiFlow shortcuts and overlays are inactive.
- When enabled: All LumiFlow features are available.

Shortcut: `L` key in the 3D Viewport.

---

### Section 2: Assignment Mode

**Location:** Below the Enable section.

**Controls:**
- Two buttons: **SCENE** and **CAMERA** (only one active at a time).

**Scene Mode (Global Lights):**
- Lights are visible in **all cameras**.
- Names start with `G_` (for example, `G_KeyLight`).
- Best for: Simple scenes, single‑camera shots, shared environment lights.

**Camera Mode (Per‑Camera Lights):**
- Lights are tied to a **specific camera**.
- Names start with `C_XX_` (for example, `C_01_KeyLight`).
- Best for: Multi‑camera studios, different lighting per angle.

**Visual Indicator:**
- The active mode button appears pressed/highlighted.

> For basic scenes, stay in **Scene** mode. For multi‑camera setups, see **Part 2 – Workflow 3** and **Part 5 – Camera Assignment System**.

---

### Section 3: Quick Templates

**Location:** Middle‑upper area of the panel.

**Purpose:**
- One‑click access to several **popular templates** (for example Product Shot, Portrait, etc.).

**Basic usage:**
1. Select your main subject.
2. Click a template button (such as **Product Shot Basic**).
3. Adjust options in the dialog if needed.
4. Click **OK** to create the lights.

For a full list of templates and when to use each, see **Part 4 – Template Library**.

---

### Section 4: Positioning Controls

**Location:** Below Quick Templates.

**Purpose:**
- Turn the **Positioning System** on or off.

**Controls:**
- Large toggle button: **"✅ POSITIONING ENABLED"** / **"❌ POSITIONING DISABLED"**.

**Effect:**
- When enabled: LumiFlow positioning modes (Highlight, Normal, Target, Orbit, etc.) are active.
- When disabled: Positioning tools do not move lights.

Shortcut: `P` key.

> Leave this **enabled** during normal work. If you only want to move lights manually with Blender tools, you can temporarily disable it.

---

### Section 5: Smart Control

**Location:** Below Positioning Controls.

**Purpose:**
- Enable/disable **Smart Controls** – viewport mouse gestures for Distance, Power, Size, etc.

**Controls:**
- Large toggle button: **"✅ SMART CONTROL ENABLED"** / **"❌ SMART CONTROL DISABLED"**.
Shortcut: `F` key.

Additional tool for Area lights (Rectangle/Ellipse):
- Press `Alt+Q` in the 3D Viewport to open the **Scale Axis** popup (XY, X only, Y only) used by Smart Control **Size/Scale**.

**Typical usage:**
- Keep Smart Controls **enabled** most of the time.
- Use `Ctrl+MMB`, `Shift+MMB`, `Alt+MMB`, etc. to adjust lights (see sections below and Part 5/6).

---

### Section 6: Overlay, Update & Support

**Location:** Bottom of the panel.

**Purpose:**
- Control **on‑screen overlays** (info/tips) and access **support/updates/community**.

**Overlay Controls:**
- **Tips Button** – Toggle overlay tips text.
- **Info Button** – Toggle overlay info panel.
- **Clean Viewport** – Hide most overlays for a cleaner view.
- **Light Picker** – Turn on LumiFlow’s light picker.

**Support & Community Controls:**
- **Help** – Open the user guide.
- **Check Updates** – Show update panel to compare current vs latest version.
- **Donate** – Show donation panel (GitHub Sponsors, Patreon, Ko‑fi, etc.).
- **Community** – Open the LumiFlow **community Discord** in your web browser.

> For details on updates, donations, and community links, see **Part 6 – Reference & Support**.

---

## 3. Core Features Overview

This section explains **what each core system does** and **how to use it in practice**. For deep technical details and advanced tips, see **Part 4–6**.

### 1. Smart Light Creation

**What it does:**
- Creates lights with **intelligent positioning** based on the scene and camera.

**Basic workflow:**
1. Prepare your scene with a clear subject and camera (see Part 2 – Quick Start).
2. Hover your mouse over the object you want to light, or select it.
3. For a single light, use **Quick Smart Light**:
   - Hover over the mesh and press **`Ctrl+Shift+Right Mouse`**.
   - LumiFlow creates a Rectangle Area light aimed at the surface.
4. For more control or full setups, use the **Smart Light & Template Menu**:
   - Hover/select the object and press **`Ctrl+Shift+A`**.
   - Choose a Smart Light or a template from the menu.
5. After creation, adjust Distance, Power, and Size using Smart Controls.

**Access:**
- **Smart Light & Template Menu:** `Ctrl+Shift+A`
- **Quick Smart Light (Rectangle Area):** `Ctrl+Shift+Right Mouse` on a mesh

---

### 2. Template System

**What it does:**
- Applies **complete lighting setups** (key/fill/rim, product, portrait, dramatic, environment, etc.) in one action.

**Benefits:**
- Save time compared to manual light creation.
- Learn from professionally designed setups.
- Quickly try different moods for the same scene.

**Template categories (examples):**
- **Studio & Commercial** – Product photography, packshots, portraits, e‑commerce.
- **Dramatic & Cinematic** – Film‑style moods (high contrast, colored lights, etc.).
- **Environment & Realistic** – Daylight, evening, night, atmospheric looks.
- **Utilities & Single Lights** – Single key, rim, or utility lights.

**How to use:**
1. Select your main subject (product, character, or interior group).
2. Choose how to apply the template:
   - **Quick Templates (Panel)** – Click a preset button in the LumiFlow panel.
   - **Smart Light & Template Menu** – Press `Ctrl+Shift+A` and pick a template.
3. In the options dialog, confirm or adjust settings (for example **Camera Relative**, **Preserve Existing Lights**).
4. After the template builds the lights, use Smart Controls and Positioning to fine‑tune the result.

For a full catalog of templates and recommended use cases, see **Part 4 – Template Library**.

---

### 3. Positioning System

**What it does:**
- Provides several **intelligent ways to move lights** based on surfaces, camera, and targets.

**Key modes (summary):**

- **Highlight Mode**  
  Place a light to create a **specular highlight** where you click on the surface of a mesh. 
  Great for glossy products, jewelry, and metallic edges.  
  Works only when you drag over actual geometry (mesh surfaces), not the empty background.

  Shortcut: `Ctrl+Left Mouse drag` on mesh surfaces.

- **Normal Mode**  
  Align a light with the **surface normal** at the point you click on a mesh.  
  Useful for architectural lights on walls, ceilings, etc.  
  Requires dragging over object surfaces so LumiFlow can read the normal.
  
  Shortcut: `Shift+Left Mouse drag` on mesh surfaces.

- **Target Mode**  
  Keep the light’s position but make it **look at** a target object.  
  Typically used by dragging over the subject or target objects to define where the light should aim.
  
  Shortcut: `Ctrl+Alt+Left Mouse drag` on mesh surfaces.

- **Orbit Mode**  
  Rotate light(s) around a pivot point at a fixed distance (turntable style).  
  Works freely in the viewport: your drag controls how lights move around the pivot, not a specific surface.
  
  Shortcut: `Alt+Left Mouse drag` in the 3D Viewport.
  
- **Free Mode**  
  Direct numeric control of light position.  
  Uses your viewport drag and pivot to place the light; it is not tied to surface normals like Highlight/Normal.
  
  Shortcut: `Ctrl+Shift+Left Mouse drag` in the 3D Viewport.

- **Move Mode**  
  Interactive viewport movement with visual feedback.  
  Works as a free move tool in the viewport: you can drag even when not exactly over a mesh surface.
  
  Shortcut: `Shift+Alt+Left Mouse drag` in the 3D Viewport.

> For detailed mode behaviors, tips, and advanced use, see **Part 5 – Positioning System**.

---

### 4. Smart Controls

**What it does:**
- Lets you adjust light properties **directly in the viewport** using mouse gestures.

**Common controls (concept):**
- **Distance** – Move lights closer/farther from the subject.  
  Shortcut: `Ctrl+Middle Mouse Button (Ctrl+MMB) drag`.
- **Power** – Make lights brighter/dimmer.  
  Shortcut: `Shift+Middle Mouse Button (Shift+MMB) drag`.
- **Scale / Size** – Change light size or radius.  
  Shortcut: `Alt+Middle Mouse Button (Alt+MMB) drag`.
- **Angle / Spread** – Control beam spread for spots, sun, etc.  
  Shortcut: `Ctrl+Shift+Middle Mouse Button (Ctrl+Shift+MMB) drag`.
- **Blend** – Soften or sharpen light edges.  
  Shortcut: `Shift+Alt+Middle Mouse Button (Shift+Alt+MMB) drag`.
- **Temperature** – Adjust light warmth/coolness.  
  Shortcut: `Ctrl+Alt+Middle Mouse Button (Ctrl+Alt+MMB) drag`.

**Typical usage pattern:**
1. Select one or more lights.
2. Use the relevant **modifier + MMB** combination.
3. Drag left/right while watching LumiFlow’s on‑screen HUD.
4. Release when you like the result.

For full shortcut details and ranges, see:
- **Part 5 – Smart Controls (advanced tips)**.
- **Part 6 – Reference & Support (shortcut tables)**.

---

### 5. Light Linking System

**What it does:**
- Controls **which objects** a light affects, without moving or changing the light.

**Use cases:**
- Light only the hero product, not the background.
- Exclude foreground from a strong backlight.
- Create focused accents on selected areas.

**Basic idea:**
- **Include mode:** Light affects **only** linked objects.
- **Exclude mode:** Light affects everything **except** linked objects.

Shortcut:
- `Ctrl+Shift+X` with **light(s) selected** – Start **Quick Link mode**. Then click mesh objects in the viewport to include/exclude them as receivers for the selected lights.
- `Ctrl+Shift+X` with **only mesh objects selected** – Toggle **Quick Smart Add** EXCLUDE/INCLUDE for those meshes (control whether Quick Smart Light/templates use them).

Advanced linking workflows are described in **Part 5 – Light Linking System**.

---

### 6. Flip Operations

**What it does:**
- Mirrors or rotates **entire lighting setups** around your subject or camera.

**Examples:**
- **Flip Horizontal** – Mirror lights from left to right.
- **Flip Vertical** – Mirror lights from top to bottom.
- **Front/Back Swap** – Swap lights in front of and behind the subject.
- **Rotate 180°** – Turn setups around camera or target.

Shortcut: `Ctrl+Shift+C` (Flip menu).

Typical use: set up lighting on one side (e.g., left‑key portrait), then flip to the other side instead of rebuilding.

More details and safety tips are in **Part 5 – Flip Operations**.

---

### 7. Solo Light Mode

**What it does:**
- Temporarily **isolate a single light** so you can see exactly what it does.

**Basic usage:**
1. Select a light.
2. Trigger Solo Light (shortcut or panel button).
3. All other lights are hidden.
4. Adjust the soloed light.
5. Disable Solo to restore all lights.

This is especially useful when you have many lights and want to understand each one’s contribution.

---

### 8. Cycle Light Selection

**What it does:**
- Quickly cycle through lights in your scene without searching in the Outliner.

Shortcut: `D` key.

**Behavior:**
- Press `D` repeatedly to move the active selection from one light to the next.
- Often ordered by distance or importance.

This is useful when combined with Smart Controls: cycle → adjust → cycle → adjust, all from the viewport.

---

## 4. Next Steps

You now know **where** LumiFlow’s main systems live and **what they do**.

- To choose and customize templates, read **Part 4 – Template Library**.
- To learn advanced strategies (multi‑camera, light linking, flip, selection tools), read **Part 5 – Advanced Features**.

👉 **[Continue to Part 4 →](04_Template_Library.md)**
