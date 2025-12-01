# Part 4: Template Library

**LumiFlow User Manual – Part 4 of 6**

This part is a **catalog of templates** included with LumiFlow and how to choose the right one for your scene.

Templates are **starting points**, not final renders. You can and should customize them with Positioning and Smart Controls.

---
## 1. How LumiFlow Templates Work

A LumiFlow template is a **pre‑built lighting setup** that:

- Creates one or more lights (key, fill, rim, bounce, etc.).
- Positions them relative to your subject and camera.
- Sets reasonable default power, size, and color.
- Names them clearly (e.g., `G_KeyLight`, `G_FillLight`).

You can then:

- Move lights with the **Positioning System**.
- Adjust lights using **Smart Controls**.
- Add or remove lights as needed.

> Think of templates as **lighting presets** that get you 80% of the way there, fast.

---

## 2. Applying Templates (Recap)

You can apply templates in two main ways:

1. **Quick Templates (Panel)**
   - In the LumiFlow panel, find **Quick Templates**.
   - Select your main subject.
   - Click a template button.
   - Configure options in the dialog and click **OK**.

2. **Smart Light & Template Menu (`Ctrl+Shift+A`)**
   - Hover over or select your subject in the 3D Viewport.
   - Press **`Ctrl+Shift+A`**.
   - Choose a template from the category lists (Studio, Dramatic, Environment, Utilities).

For a step‑by‑step example, see **Part 2 – Quick Start, Step 3**.

---

## 3. Template Categories

Exact template names may vary slightly between versions, but they are always grouped into **four main categories**.

### 3.1 Studio & Commercial

**Best for:**
- Product shots (packshots, packaging, devices, bottles, etc.).
- E‑commerce renders on neutral backgrounds.
- Simple character/portrait studio looks.

**Typical characteristics:**
- Clear key/fill/rim separation.
- Clean background control.
- Neutral or slightly warm color temperatures.

**Example templates:**
- **Three‑Point Setup** – Classic key/fill/rim arrangement. Good starting point for many scenes.
- **Product Shot Basic** – Minimal, clean setup for single products.
- **Product Shot Advanced** – More lights for high‑end hero renders.
- **Portrait Classic** – Soft frontal lighting with subtle rim and fill.

**When to choose:**
- When you need a **safe, predictable result** quickly.
- When the subject is the main focus and the background is simple.

---

### 3.2 Dramatic & Cinematic

**Best for:**
- Stylized portraits or characters.
- Mood‑driven shots (horror, noir, cyberpunk, etc.).
- Scenes where **contrast and color** carry the story.

**Typical characteristics:**
- Strong contrast between light and shadow.
- Colored or tinted lights.
- Accented rims and narrow beams.

**Example templates:**
- **Dramatic Portrait** – Strong key with deep shadows and punchy rim.
- Other cinematic setups (names may vary by version) that use a mix of angled keys, colored fills, and stylized backlights.

**When to choose:**
- When you care more about **mood and storytelling** than neutral product accuracy.

---

### 3.3 Environment & Realistic

**Best for:**
- Interior or exterior scenes.
- Daylight, evening, and night moods.
- Scenes that should feel **physically plausible**.

**Typical characteristics:**
- Sun/sky or window‑style lights.
- Bounce or fill lights that simulate indirect illumination.
- Balanced color temperatures between environment and artificial lights.

**Example templates (conceptual):**
- **Studio Daylight** – Neutral daylight feel for indoor products/characters.
- **Indoor Window Light** – Window key light + interior fill.
- **Evening / Night** – Cooler environment with warm interior accents.

**When to choose:**
- When the world around the subject matters (architecture, interiors, outdoor scenes).

---

### 3.4 Utilities & Single Lights

**Best for:**
- Building custom setups from scratch.
- Adding just one extra light (key, rim, logo highlight, etc.).
- Technical uses (debugging, check light linking, etc.).

**Typical characteristics:**
- Single light types (area, spot, sun, etc.).
- Minimal or no secondary lights.

**Example templates:**
- **Single Key Light** – One controllable main light.
- **Single Rim Light** – Edge separation light.
- **Utility Fill / Bounce** – Soft fill with low intensity.

**When to choose:**
- When templates feel “overkill” and you want full creative control.

---

## 4. Choosing the Right Template

Here is a quick decision guide.

- **Product on plain background**  
  → Start with **Product Shot Basic** or **Three‑Point Setup**.

- **Hero product, glossy materials**  
  → **Product Shot Advanced**, then add **Highlight** detail lights (see Part 2 & 5).

- **Simple portrait / character**  
  → **Portrait Classic** for a neutral look.

- **Stylized / dramatic portrait**  
  → **Dramatic Portrait** or another Dramatic/Cinematic variant.

- **Interior with windows**  
  → An **Indoor/Window**‑style template from Environment & Realistic; tweak window direction and fill.

- **Custom look, nothing fits**  
  → Use **Utilities & Single Lights** to build a setup manually.

---

## 5. Customizing Templates

After applying any template, you are expected to **customize** it:

1. **Global balance**  
   - Keep all template lights selected (or reselect them, for example with `Ctrl+D` to select all LumiFlow lights).  
   - Use Distance, Power, and Size Smart Controls to get the overall exposure and softness right.

2. **Per‑light tweaks**  
   - Adjust individual key/fill/rim lights to fine‑tune shape and contrast.

3. **Positioning**  
   - Use **Highlight** mode to place clean highlights.
   - Use **Orbit** or **Target** for character and product keys.

4. **Light linking (advanced)**  
   - If a light should affect only part of the scene, use **Light Linking** (see Part 5) instead of duplicating scenes.

5. **Scene vs Camera assignment**  
   - For multi‑camera setups, keep broad base lights in **Scene** mode (`G_` lights), and angle‑specific accents in **Camera** mode (`C_XX_` lights).

---

## 6. Recommended Starting Templates

If you are unsure where to begin, use this as a default map:

- **Product renders for e‑commerce:**  
  Start with **Product Shot Basic** → refine with Highlight and Smart Controls.

- **Portfolio hero images:**  
  Start with **Product Shot Advanced** or a **Studio & Commercial** variant → more time spent on details.

- **Character/portrait:**  
  Start with **Portrait Classic** → optionally layer a **Dramatic** template for mood experiments.

- **Architecture/interior:**  
  Start with an **Environment & Realistic** template (window/daylight) → refine with Utilities lights.

---

## 7. Next Steps

Now that you understand the Template Library:

- Use **Part 2 – Getting Started Workflow** when you need step‑by‑step recipes.
- Use **Part 3 – Interface & Core Features** as a map of where templates live in the UI.
- Move on to **Part 5 – Advanced Features** to learn about camera assignment, light linking, and other advanced tools used together with templates.

👉 **[Continue to Part 5 →](05_Advanced_Features.md)**
