# Part 6: Reference & Support

**LumiFlow User Manual – Part 6 of 6**

This part is your **quick reference and help center**. Use it when you:

- Forget a shortcut.
- Hit a problem or error.
- Need performance tips.
- Want to reach the LumiFlow community.

---
## 1. Shortcut Overview (Essential)

This is a **short list** of the most important shortcuts. Exact mappings may vary per version and keymap; always check **Edit → Preferences → Keymap** for conflicts.

### 1.1 Global & Panel Shortcuts

- **Toggle LumiFlow** – `L`  
  Enable/disable LumiFlow systems in the 3D Viewport.

- **Open Sidebar** – `N`  
  Show/hide the right‑hand panel where the LumiFlow tab lives.

### 1.2 Creation & Templates

- **Smart Light & Template Menu** – `Ctrl+Shift+A`  
  Open the LumiFlow menu under the mouse cursor.

- **Quick Smart Light (Rectangle Area)** – `Ctrl+Shift+Right Mouse`  
  Drop a smart light directly on the surface under the cursor.

### 1.3 Positioning & Highlighting

- **Highlight Positioning** – `Ctrl + Left Mouse drag`  
  Move the selected light to create a specular highlight where you drag.

- **Toggle Positioning System** – `P`  
  Enable/disable LumiFlow positioning tools.

### 1.4 Smart Controls (Viewport Gestures)

These are the standard LumiFlow bindings; see Part 5 and your keymap for details.

- **Distance** – `Ctrl+Middle Mouse Button (Ctrl+MMB)`  
  Move light(s) closer/farther from the subject.

- **Power** – `Shift+MMB`  
  Change light intensity.

- **Size / Scale** – `Alt+MMB`  
  Change light size or radius.

- **Other controls** (Angle, Blend, Temperature, etc.)  
  Available via additional modifier+MMB combinations depending on light type.

- **Toggle Smart Controls** – `F`  
  Enable/disable Smart Control system.

### 1.5 Assignment, Linking & Flip

- **Scene / Camera Assignment Buttons** – Panel buttons in **Assignment Mode** section.  
  No default keyboard mapping; click in the panel.

- **Quick Light Linking** – `Ctrl+Shift+X`  
  With light(s) selected: start **Quick Link mode** and click mesh objects to include/exclude them as receivers. With only mesh objects selected: toggle **Quick Smart Add** EXCLUDE/INCLUDE for those meshes.

- **Flip Operations Menu** – `Ctrl+Shift+C`  
  Open the Flip menu for mirroring or rotating lighting setups.

### 1.6 Selection & Solo

- **Cycle Lights** – `D`  
  Cycle through scene lights.

- **Select all LumiFlow lights** – `Ctrl+D`  
  Select all lights in the **LumiFlow Lights** collection and make one of them active.

- **Solo Light** – `Ctrl+Shift+D` (or panel button)  
  Isolate the active light by hiding all other LumiFlow lights.

### 1.7 Rendering

- **Render Image** – `F12`  
  Standard Blender render shortcut.

---

## 2. Common Issues & Fixes

### 2.1 LumiFlow Tab Does Not Appear

**Symptoms:**
- You installed the add‑on but see no **LumiFlow** tab in the Sidebar.

**Check:**
1. In Blender, go to `Edit → Preferences → Add-ons`.
2. Search for `LumiFlow`.
3. Make sure the checkbox is **enabled**.

**Also verify:**
- You are in a **3D Viewport** and have pressed `N` to open the Sidebar.

### 2.2 Shortcuts Do Nothing

**Symptoms:**
- Pressing `Ctrl+Shift+A`, `Ctrl+Shift+Right Mouse`, or other LumiFlow keys has no effect.

**Check:**
1. Ensure LumiFlow is **enabled** in the panel (or press `L`).
2. Make sure the **mouse cursor is over the 3D Viewport** when pressing the shortcut.
3. Check for key conflicts in `Edit → Preferences → Keymap`.

If another add‑on or custom keymap uses the same combination, adjust that mapping or LumiFlow’s mapping as needed.

### 2.3 No Lights Are Created

**Symptoms:**
- You trigger Smart Light or a template, but no new lights appear.

**Check:**
- Confirm you have a valid **mesh object** under the cursor or selected.
- Check the **Outliner** for a collection like `LumiFlow Lights`; lights may be created but currently out of view.
- Ensure you are not filtering lights out of the Outliner or Viewport.

### 2.4 Lights Invisible in Eevee / Workbench

**Symptoms:**
- Lights behave differently or light linking does not work in Eevee/Workbench.

**Explanation:**
- **Light Linking** is only fully supported in **Cycles**.  
  Eevee and Workbench do not support the same linking features.

**Fix:**
- Use **Cycles** when testing light linking and advanced LumiFlow features.

### 2.5 Performance Is Slow in Heavy Scenes

**Symptoms:**
- Viewport becomes sluggish when many lights and overlays are active.

**Mitigations:**
- Use **Viewport Shading: Solid** during setup, switch to Rendered only when needed.
- Temporarily disable **overlays** or **Clean Viewport** in Section 6 of the panel.
- Reduce the number of active lights, especially volumetric or high‑cost ones.
- Use **Solo Light** mode to work with one light at a time when fine‑tuning.

---

## 3. Performance Tips

- Prefer **Cycles GPU** if available.
- Use **lower render preview samples** while adjusting lighting.
- Use **Simplify** settings in Blender for heavy geometry.
- Keep HDRI/environment maps at reasonable resolution while iterating.
- Use **Scene Mode base lights** + **Camera Mode accents** instead of many unique full setups per camera.

---

## 4. Community & Support

LumiFlow has an active community and several official support channels.

### 4.1 Official Resources

- **GitHub Repository**  
  Source code, issue tracker, and development roadmap.

- **Documentation (this manual)**  
  The user_manual2 folder and future online docs.

### 4.2 Community Channels

- **Discord Community**  
  Real‑time chat, Q&A, showcase renders, feedback, and events.  
  Open it from the **Community** button in the LumiFlow panel (Section 6) or via the link in the repository.

- **GitHub Discussions**  
  Asynchronous questions, feature requests, and longer technical threads.

### 4.3 Getting Help Effectively

When asking for help, include:

- Blender version and OS.
- LumiFlow version.
- Render engine (Cycles/Eevee/Workbench).
- Short description of what you tried and what happened.
- Screenshots or .blend files if possible.

This makes it easier for maintainers and community members to reproduce and solve your issue.

---

## 5. Staying Up to Date

- Use the **Check Updates** button in the LumiFlow panel to see if a new version is available.
- Follow the repository’s **releases** or announcements channel for changelogs.
- Read the **CHANGELOG** when updating to understand new features and breaking changes.

---

## 6. Final Notes

- LumiFlow is designed to be **non‑destructive**: it creates and manages regular Blender lights and collections.
- You can always fall back to standard Blender tools if needed; LumiFlow’s lights are just lights.
- The more you use templates, positioning modes, and Smart Controls together, the faster you will light complex scenes.

Thank you for using LumiFlow.  
If this manual helped you, consider joining the community and sharing your work.
