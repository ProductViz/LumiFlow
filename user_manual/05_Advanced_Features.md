# Part 5: Advanced Features

**LumiFlow User Manual – Part 5 of 6**

This part is for **advanced and production use**. It assumes you:

- Understand the basics from **Part 2 – Getting Started Workflow**.
- Know the panel layout and core systems from **Part 3 – Interface & Core Features**.
- Are comfortable picking templates from **Part 4 – Template Library**.

Here you will learn how to **combine LumiFlow systems** for multi‑camera, multi‑object, and heavy scenes.

---
## 1. Camera Assignment System

Organize lights in scenes with **multiple cameras**.

### 1.1 Concepts

- **Scene Mode (Global Lights)**
  - Lights are visible in **all cameras**.
  - Names start with `G_` (e.g. `G_KeyLight`).
  - Good for: Base environment lighting, simple projects.

- **Camera Mode (Per‑Camera Lights)**
  - Lights are attached to a **specific camera**.
  - Names start with `C_XX_` (e.g. `C_01_KeyLight`).
  - Good for: Multi‑angle product studios, complex shots.

A typical production scene uses **both**:

- `G_` lights as a shared base.
- `C_XX_` lights for per‑camera accents and fixes.

### 1.2 Recommended Strategy

1. **Build a global base in Scene Mode**
   - Set Assignment Mode to **Scene**.
   - Apply a studio template (such as Product Shot Basic) to your main subject.
   - Adjust with Smart Controls until it looks good from most angles.

2. **Switch to Camera Mode for per‑camera lights**
   - Set Assignment Mode to **Camera**.
   - For each camera:
     - Make the camera active (`Ctrl+Numpad 0`).
     - Apply a small template or add Utility lights for that view.

3. **Check visibility**
   - As you switch cameras, confirm:
     - `G_` lights stay visible in all cameras.
     - Each camera only shows its own `C_XX_` lights.

For step‑by‑step example, revisit **Part 2 – Workflow 3: Multi‑Camera Product Studio**.

---

## 2. Positioning System (Advanced Tips)

This section assumes you know the basic modes from **Part 3**. Here we focus on **practical tricks**.

### 2.1 Highlight Mode – Production Use

Use **Highlight** mode when you want **precise specular highlights**:

- Jewelry and watches.
- Logos and metallic edges.
- Shiny plastic or glass.

**Workflow tip:**
1. Select your key or accent light.
2. Enable Highlight positioning.
3. In the 3D Viewport, hold **`Ctrl + Left Mouse`** and drag over the surface where you want a highlight.
4. Fine‑tune distance and power with Smart Controls.

### 2.2 Normal Mode – Architectural & Product Panels

Use **Normal** mode when aligning lights to walls, floors, or large surfaces:

- Wall washers.
- Ceiling panels.
- Softbox against backdrop.

**Workflow tip:**
1. Select an Area or Spot light.
2. Enable Normal mode.
3. Click on the wall/ceiling/floor where the light should aim.
4. Adjust Distance and Size to control spread.

### 2.3 Target & Orbit – Shaping Character and Product Keys

- **Target mode** – Keep light in place but always **look at** the target object.
- **Orbit mode** – Move light **around** a pivot (often the subject) while preserving distance.

**Workflow tip (portrait):**
1. Select the key light.
2. Use Target to lock the light on the face.
3. Use Orbit to move around the character while the light keeps looking at the target.

### 2.4 Free & Move – Fine Adjustments

- **Free mode** – Numeric entry; use when you need exact coordinates.
- **Move mode** – Interactive movement with overlay feedback.

Use these when Highlight/Normal/Orbit get you close, but you need a final small adjustment.

---

## 3. Smart Controls – Advanced Techniques

You already know the basics (Distance, Power, Size). Here are some **advanced patterns**.

### 3.1 Multi‑Light Balancing

1. Select **all lights** of a template (for example with `Ctrl+D` to select all LumiFlow lights).
2. Use:
   - Distance (`Ctrl+MMB`) to change perceived size and softness.
   - Power (`Shift+MMB`) to keep exposure within good ranges.
3. Deselect one or two lights (e.g. rim) and adjust them independently.

This approach keeps the setup **coherent** while still allowing accents.

### 3.2 Animating Smart Controls

Smart Controls change standard light properties (power, location, size, etc.). You can still use Blender keyframes:

1. Use Smart Controls to set a value.
2. Hover the mouse over the property in the Properties Editor.
3. Press **`I`** to insert a keyframe.

This works well for shots where lights move or change intensity over time.

### 3.3 Safe Ranges

LumiFlow is designed to keep **reasonable ranges**, but you can still overshoot.

- Watch the HUD values.
- If a value becomes extreme (e.g. very high power), reduce distance or size first.

For full shortcut mapping and ranges, see **Part 6 – Reference & Support**.

### 3.4 Scale Axis for Area Lights

For Area lights with **Rectangle** or **Ellipse** shape, Smart Control **Size/Scale** can use different axes:

- **XY** – Uniform scaling (both sides together).
- **X only / Y only** – Stretch the light in just one direction.

In the 3D Viewport, press `Alt+Q` to open the **Scale Axis** popup and switch between XY / X / Y while using Size/Scale Smart Controls.

Use axis control when you need to fine‑tune the shape of softboxes, strips, or other rectangular area lights.

---

## 4. Light Linking System (Advanced)

### 4.1 Why Use Light Linking?

Light Linking lets you avoid **duplicating scenes** or using heavy compositing tricks when:

- A light should affect **only the hero product**, not the backdrop.
- A ceiling light should affect **only furniture**, not walls.
- You want a rim light that affects **only one character** in a group.

### 4.2 Basic Include / Exclude Logic

- **Include mode:**
  - Light affects **only** its linked objects.
- **Exclude mode:**
  - Light affects **everything except** its linked objects.

### 4.3 Quick Linking Workflow

There are two ways to use Quick Link, depending on what you have selected.

**A. Link selected lights to meshes (Quick Link mode)**

1. Select one or more **lights** you want to control.
2. Press `Ctrl+Shift+X`.
3. In the 3D Viewport, click mesh objects to include/exclude them as receivers for the selected lights.
4. Press `X` or release modifiers to exit Quick Link mode, or `Esc` to cancel.

**B. Toggle Quick Smart Add include/exclude on meshes**

1. Select one or more **mesh objects** (no lights selected).
2. Press `Ctrl+Shift+X`.
3. LumiFlow toggles the **Quick Smart Add** EXCLUDE/INCLUDE flag on those meshes (controls whether Quick Smart Light/templates target them by default).

Check the result by toggling the relevant light(s) on/off and watching only the intended objects change.

### 4.4 Best Practices

- Use short, descriptive light names (`G_BackdropFill`, `C_01_LogoRim`).
- Keep link sets simple; too many tiny links are hard to manage.
- Document special links in scene notes if other artists will touch the file.

---

## 5. Flip Operations

Flip tools speed up **symmetrical or alternative** lighting setups.

### 5.1 Typical Uses

- Mirror a portrait lighting from left to right.
- Invert a top‑down light setup.
- Test a shot with lights moved behind the camera instead of in front.

### 5.2 Common Operations

- **Flip Horizontal** – Mirror across a vertical plane (left ↔ right).
- **Flip Vertical** – Mirror across a horizontal plane (top ↔ bottom).
- **Front/Back Swap** – Swap lights in front of and behind the subject.
- **Rotate 180°** – Spin lights around camera or target.

Shortcut: `Ctrl+Shift+C` (Flip menu).

**Workflow tip:**
- Save a version before flipping a complex setup, in case you want to revert.

---

## 6. Selection & Solo Tools

Managing many lights is easier with dedicated selection tools.

### 6.1 Cycle Light Selection

Shortcut: `D` key.

- Cycles through lights in your scene.
- Combine with Smart Controls to quickly tweak each light.

### 6.2 Solo Light Mode

**What it does:**
- Temporarily hides all lights except the selected one.

**Typical workflow:**
1. Select a light.
2. Trigger Solo Light (`Ctrl+Shift+D` or button in the panel).
3. Adjust the soloed light.
4. Unsold to bring all lights back.

This helps you understand each light’s contribution without distraction.

### 6.3 Utility Selection Tools

Depending on your version, LumiFlow may also include utility operators such as:

- Select all LumiFlow lights (`Ctrl+D`).
- Delete selected LumiFlow lights or collections.
- Auto‑select the light under the mouse.

These are especially helpful in dense scenes with many objects and lights.

---

## 7. Putting It All Together

In complex projects you will often:

1. Use **Scene Mode** for base environment lights.
2. Use **Camera Mode** for per‑angle accents and fixes.
3. Rely on **Templates** for fast starting points.
4. Use **Positioning** and **Smart Controls** for final shaping.
5. Use **Light Linking** to control exactly what each light affects.
6. Use **Flip** and **Selection tools** to iterate quickly.

When in doubt:

- Revisit **Part 2** for workflow ideas.
- Revisit **Part 3** for where to find features.

👉 **[Continue to Part 6 →](06_Reference_Support.md)**
