# Part 1: Introduction & Installation

**LumiFlow User Manual – Part 1 of 6**

LumiFlow is a lighting assistant for Blender that helps you build **professional lighting setups in minutes**, using templates, smart positioning, and viewport-based controls.

Use this Part to get LumiFlow **installed, enabled, and verified** before you start lighting real scenes.

---
## 1. What Is LumiFlow?

LumiFlow is a Blender add-on focused on **lighting for product visualization and look‑development**.

With LumiFlow you can:

- Create studio lighting from templates in a few clicks.
- Drop smart lights directly onto surfaces from the viewport.
- Position and adjust lights using simple mouse gestures (Smart Controls).
- Separate **Scene** (global) and **Camera** (per‑camera) lights.
- Use light linking, flip operations, and selection tools for complex scenes.

LumiFlow does **not** replace Blender’s render engines. It works **on top of** Cycles/Eevee/Workbench by creating and managing lights in your scene.

---

## 2. Requirements & Compatibility

### Blender

- Blender **3.x or newer** is recommended.
- LumiFlow is designed and tested primarily with **Cycles**.

### Operating System

- ✅ **Windows 10 (64‑bit)**
- ✅ **Windows 11**

> macOS and Linux users may still be able to use LumiFlow, but this new manual edition focuses on officially tested Windows builds.

### Render Engines

| Renderer   | Support Status                       |
|-----------|---------------------------------------|
| **Cycles** | ✅ Full support                       |
| **Eevee**  | ⚠️ Limited (no light linking)         |
| **Workbench** | ⚠️ Limited (no light linking)     |

For the **best experience** (especially with Light Linking and advanced features), use **Cycles**.

---

## 3. Installing LumiFlow

1. **Download the add-on (.zip)**
   - Get the latest LumiFlow `.zip` file from the official source (Gumroad, Blender Market, or GitHub release).
   - Do **not** unzip the file.

2. **Open Blender Preferences**
   - In Blender, go to `Edit → Preferences…`.
   - Switch to the **Add-ons** tab.

3. **Install the add-on**
   - Click **Install…** (top-right of the Add-ons tab).
   - Choose the **LumiFlow .zip** file you downloaded.
   - Click **Install Add-on**.

4. **Enable the add-on**
   - In the Add-ons search bar, type `LumiFlow`.
   - Enable the checkbox next to **LumiFlow**.
   - Preferences are saved automatically in recent Blender versions.

> If you do not see LumiFlow in the list, make sure you installed the correct `.zip` and did not extract it.

---

## 4. Finding the LumiFlow Panel

1. Open any Blender file or start with **File → New → General**.
2. Make sure you are in a **3D Viewport**.
3. Press **`N`** to open the right‑hand **Sidebar**.
4. Look for the **LumiFlow** tab along the side of the sidebar.
5. Click **LumiFlow** to open the main panel.

If you do not see the tab:
- Confirm the add-on is enabled in Preferences.
- Make sure the mouse is over a 3D Viewport when pressing `N`.

---

## 5. Enabling LumiFlow in the Viewport

LumiFlow has a master **Enable** toggle so you can temporarily turn its systems on or off.

1. In the **LumiFlow** panel, locate the **Enable** section at the top.
2. Click the big **Enable** button.
3. When LumiFlow is active, the status changes to something like **"✅ ENABLED"**.

**Shortcut:**
- Press **`L`** in the 3D Viewport to quickly toggle LumiFlow on/off.

> When disabled, LumiFlow does not draw overlays or react to shortcuts, but your existing lights remain in the scene.

---

## 6. Quick Verification Test

Before diving into workflows, run this **simple test** to confirm LumiFlow is installed correctly.

1. **Create a simple test scene**
   - Add any mesh object (for example, a cube or a product model).
   - Add a camera pointing at the object.

2. **Enable LumiFlow**
   - Open the **LumiFlow** panel.
   - Click **Enable** (or press `L`).

3. **Open the Smart Light & Template Menu**
   - Move your mouse over the 3D Viewport.
   - Press **`Ctrl+Shift+A`**.
   - You should see a **LumiFlow menu** with Smart Light and template categories.

4. **Apply a quick template**
   - With your object selected, choose a simple studio template (for example, **Product Shot Basic**).
   - Accept the default options in the dialog.
   - LumiFlow should create several lights around your object.

5. **Preview the result**
   - Press `Z` and switch to **Rendered** or **Material Preview**.
   - You should see your object lit by the new LumiFlow lights.

If you reach this point, LumiFlow is **installed and working**.

## 7. Customizing LumiFlow Shortcuts (Optional)

You can change the keyboard shortcuts LumiFlow uses so they fit your own workflow.

### 7.1 Using LumiFlow Add-on Preferences (Recommended)

1. In Blender, go to `Edit → Preferences…`.
2. Open the **Add-ons** tab.
3. In the search box, type `LumiFlow`.
4. Find **LumiFlow** in the list and click the small arrow on the right to expand its settings.
5. Scroll down to the **Shortcut Settings** section.
6. For each action, adjust:
   - `Key` (for example `A`, `D`, `F`),
   - `Event` (`Press` or `Release`),
   - and the modifier checkboxes (`Ctrl`, `Shift`, `Alt`).
7. When you are happy with your changes, click **Apply Shortcuts** to write them to Blender's keymap.
8. Click **Save Preferences** in the bottom-left of the Preferences window so your shortcuts are kept for the next Blender session.

If you want to go back to the default LumiFlow mappings, open the same **Shortcut Settings** section and click **Reset to Default**.

### 7.2 Adjusting Shortcuts in the Keymap Tab (Advanced)

For advanced users, you can also edit shortcuts directly in Blender's keymap:

1. Go to `Edit → Preferences… → Keymap`.
2. In the search box, type `LumiFlow` to find LumiFlow operators.
3. Expand an entry and change the key combination as needed.
4. Click **Save Preferences** so Blender remembers your custom keymap.

---

## 8. Next Steps

You are ready to start lighting real scenes.

- Continue to **Part 2 – Getting Started Workflow** to:
  - Build your first product shot from scratch.
  - Learn the basic workflows and keyboard shortcuts.
  - Understand how templates, positioning, and Smart Controls fit together.

👉 **[Go to Part 2 →](02_Getting_Started_Workflow.md)**
