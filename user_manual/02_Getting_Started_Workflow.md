# Part 2: Getting Started Workflow

**LumiFlow User Manual – Part 2 of 6**

This part focuses on **doing**, not theory. You will:

- Install and enable LumiFlow (review only briefly).
- Build your **first product lighting** using a template.
- Learn the **core LumiFlow workflow loop**.
- Try a few common example workflows.

---
## 1. Quick Start – Single Product Shot

Goal: **Clean product lighting** for a single camera.

### Step 1 – Prepare Your Scene

1. Open Blender and load your **product model** (or any simple object).
2. Make sure you have a **camera** looking at the product.
3. You can keep existing Blender lights for now; LumiFlow can preserve or replace them later.

> Tip: Frame the camera so the product fills most of the view. This makes templates easier to judge.

### Step 2 – Enable LumiFlow

1. Open the **LumiFlow** tab in the right‑hand Sidebar (`N` key in the 3D Viewport).
2. Click **Enable** at the top of the panel (or press `L`).
3. Confirm the status shows something like **"✅ ENABLED"**.

### Step 3 – Apply a Template

You will now add a **complete lighting setup** around your product.

There are two main entry points:

- **Quick Templates (Panel)**
  1. In the LumiFlow panel, find the **Quick Templates** section.
  2. Click a template such as **Product Shot Basic** or **Three‑Point Setup**.

- **Smart Light & Template Menu (`Ctrl+Shift+A`)**
  1. Hover over your product in the 3D Viewport (or select it).
  2. Press **`Ctrl+Shift+A`**.
  3. Choose a template from the categories (Studio & Commercial, Dramatic & Cinematic, etc.).

A **Template Options** dialog appears. Important options:

- **Camera Relative**  
  When ON, the template aligns to the **active camera**. This is best for most product and portrait shots.

- **Preserve Existing Lights**  
  - **OFF (recommended for first tests):** LumiFlow will remove non‑LumiFlow lights first, so you only see the new setup.
  - **ON:** LumiFlow keeps any existing lights in your scene and adds its own. Useful if you already have environment or special lights.

- Other options may include material adaptation or limiting lights to selected objects. For deeper explanations, see **Part 4 – Template Library**.

Click **OK** to build the lights.

### Step 4 – View Your Lighting

1. Press **`Numpad 0`** to look through the active camera.
2. Press **`Z`** and choose **Rendered** or **Material Preview**.
3. You should see your product lit by the LumiFlow lights (usually with names like `G_KeyLight`, `G_FillLight`, etc.).

### Step 5 – Balance All LumiFlow Lights Together

Right after applying a template, **keep all new LumiFlow lights selected**. If you clicked away, you can reselect them quickly:

- Use your preferred selection method, **or**
- Press `Ctrl+D` to select all LumiFlow lights in the scene.

With all template lights selected, use **Smart Controls** to balance the setup:

- **Distance** – `Ctrl+Middle Mouse Button (Ctrl+MMB)`
  - Drag left/right to move the lights closer or farther from the subject.
- **Power** – `Shift+MMB`
  - Drag to make all selected lights brighter or dimmer.
- **Size** – `Alt+MMB`
  - Drag to change light size (softer vs harder shadows).

Use these three together until the overall brightness and softness look right.

> Think of this as your **first global balance**: get everything into a good range before worrying about tiny tweaks.

### Step 6 – Optional: Add a Detail Light

Sometimes you want an extra highlight on a logo, edge, or small area. Use **Quick Smart Light** for this.

1. Hover your cursor over the surface where you want more emphasis.
2. Press **`Ctrl+Shift+Right Mouse`**.
3. LumiFlow creates a **Rectangle Area** light automatically aimed at that surface.

Then refine its position using **Highlight positioning**:

- With the new light selected, hold **`Ctrl+Left Mouse`** and drag in the 3D Viewport.  
  LumiFlow moves the light to create a clean specular highlight at the point you drag over.

You can again use Smart Controls (Distance, Power, Size) to blend this detail light into your setup.

### Step 7 – Preview & Render

1. Make sure you are in **Rendered** or **Material Preview**.
2. Adjust any remaining lights as needed.
3. Press **`F12`** to render an image.
4. Compare before/after your LumiFlow adjustments.

You have now:

- Installed and enabled LumiFlow.
- Applied a template.
- Balanced all lights with Smart Controls.
- Optionally added a detail highlight light.

---

## 2. Core LumiFlow Workflow (Short Version)

Once you understand the Quick Start, most LumiFlow sessions follow this pattern:

1. **Choose Assignment Mode**  
   - **Scene** mode for a single shared setup across all cameras.  
   - **Camera** mode when each camera should have its own lighting.

2. **Add a Base Setup with Templates**  
   - Select your main subject.  
   - Use Quick Templates or `Ctrl+Shift+A` to apply a suitable template.

3. **Balance All Template Lights Together**  
   - Keep all template lights selected (or reselect them, for example with `Ctrl+D` to select all LumiFlow lights).  
   - Use Distance, Power, and Size Smart Controls to get a good global balance.

4. **Add and Refine Detail Lights (Optional)**  
   - Use Quick Smart Light (`Ctrl+Shift+Right Mouse`) on areas that need extra emphasis.  
   - Use Highlight positioning (`Ctrl+Left Mouse drag`) and Smart Controls to fit them into the setup.

5. **Control What Each Light Affects (Advanced)**  
   - Use Scene vs Camera assignment and **Light Linking** to control which objects are lit by which lights (see Part 5 for details).

6. **Preview, Render, Iterate**  
   - Render a test image (`F12`).  
   - Adjust lights, then render again.  
   - Save versions of setups you like.

For more detail about each system (Smart Light, Templates, Positioning, Smart Controls, etc.), see **Part 3 – Interface & Core Features**.

---

## 3. Example Workflows

Below are simplified recipes you can adapt. They intentionally avoid deep theory and focus on **what to click** and **why**.

### Workflow 1 – Product Shot (Single Camera)

**Goal:** Clean, neutral product lighting for e‑commerce or portfolio.

1. **Scene Setup**
   - Product model on a simple background.
   - One camera framing the hero view.

2. **Assignment Mode**
   - Set LumiFlow to **Scene** mode (global lights shared by this camera).

3. **Apply a Studio Template**
   - Select your product.
   - Apply **Product Shot Basic** or **Product Shot Advanced**.
   - In the dialog, keep **Camera Relative** ON and **Preserve Existing Lights** OFF for a clean test.

4. **Global Balance**
   - With all new lights selected, use Distance, Power, and Size Smart Controls to reach a good starting look.

5. **Local Tweaks**
   - Tweak individual key/fill/rim lights if needed (slight power or distance changes).

6. **Final Render**
   - Switch to **Cycles**, set a simple HDRI or background if desired, then render.

---

### Workflow 3 – Multi-Camera Product Studio

**Goal:** Different lighting per camera, with optional shared base lights.

1. **Scene Setup**
   - Create 2–3 cameras (front, side, detail).

2. **(Optional, Recommended) Base Lighting in Scene Mode**
   - Switch LumiFlow to **Scene** mode.
   - Apply a simple studio template (for example **Product Shot Basic**) to your product.  
   - These `G_` lights become your **global base** and are visible in all cameras.

3. **Per-Camera Lights in Camera Mode**
   - Switch LumiFlow to **Camera** mode.

4. **Light Camera 1**
   - Set Camera 1 as active (`Ctrl+Numpad 0`).
   - Apply or adjust a template for this angle (for example, Product or Portrait template).  
   - Lights get names like `C_01_KeyLight`.

5. **Light Camera 2 and Others**
   - Switch to Camera 2, repeat with a different template or different tweaks.  
   - Lights get names like `C_02_KeyLight`, etc.

6. **Test Switching**
   - Switch between cameras and verify:  
     - Each camera keeps its own `C_XX_` lights.  
     - All cameras share the same `G_` base lights.

For more assignment strategies and complex scenes, see **Part 5 – Camera Assignment System**.

---

## 4. Next Steps

Once you are comfortable with these workflows:

- Read **Part 3 – Interface & Core Features** to learn:
  - How the LumiFlow panel is structured.
  - Where to find Smart Light, Templates, Positioning, Smart Controls, and overlays.

- Then explore:
  - **Part 4 – Template Library** to discover all templates and when to use them.
  - **Part 5 – Advanced Features** for multi‑camera, light linking, and production workflows.

👉 **[Continue to Part 3 →](03_Interface_Core_Features.md)**
