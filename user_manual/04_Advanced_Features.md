# Part 4: Advanced Features

**LumiFlow User Manual - Part 4 of 5**

---

## Table of Contents

- [Positioning System](#positioning-system)
- [Smart Controls](#smart-controls)
- [Light Linking System](#light-linking-system)
- [Camera Assignment System](#camera-assignment-system)
- [Flip Operations](#flip-operations)
- [Selection Tools](#selection-tools)

---

## Positioning System

LumiFlow provides 6 intelligent positioning modes for precise light placement.

### Mode 1: HIGHLIGHT

**Purpose:** Position light at specular highlight point

**How It Works:**
1. Raycasts from camera to selected object
2. Calculates reflection vector at hit point
3. Positions light in reflection direction
4. Distance based on object size

**Use Cases:**
- Product photography with glossy materials
- Jewelry and metallic objects
- Creating specular highlights intentionally
- Car and vehicle renders

**How to Use:**
1. Select a light
2. Enable Highlight positioning mode
3. Click on object surface where you want highlight
4. Light moves to create highlight at that point

**Algorithm:**
```
View Vector = HitPoint - CameraLocation
Reflect Vector = View.reflect(SurfaceNormal)
Light Position = HitPoint + ReflectVector * OptimalDistance
```

**Tips:**
- Works best with glossy/metallic materials
- Click on areas you want bright highlights
- Distance auto-adjusts based on object size
- Use Material Preview to see highlights in real-time

---

### Mode 2: NORMAL

**Purpose:** Align light perpendicular to surface

**How It Works:**
1. Raycasts to object surface
2. Gets surface normal at hit point
3. Positions light along normal direction
4. Offsets distance from surface

**Use Cases:**
- Architectural lighting (wall sconces)
- Wall-mounted lights
- Ceiling lights
- Surface-aligned fixtures

**How to Use:**
1. Select a light
2. Enable Normal positioning mode
3. Click on wall/ceiling/surface
4. Light positions perpendicular to surface

**Tips:**
- Perfect for architectural visualization
- Great for wall and ceiling lights
- Adjust distance after positioning
- Use with spot lights for realistic fixtures

---

### Mode 3: TARGET

**Purpose:** Point light at selected objects

**How It Works:**
1. Calculates center of target object(s)
2. Updates light rotation to aim at center
3. Maintains current light position
4. Works with multiple targets

**Use Cases:**
- Character lighting
- Directional spotlights
- Pointing light at specific areas
- Following moving objects

**How to Use:**
1. Select a light
2. Select target object(s)
3. Enable Target mode
4. Click Apply or use shortcut
5. Light rotation updates to point at targets

**Multi-Target:**
- Calculates weighted center of all targets
- Considers object sizes for weighting
- Points at optimal center point

**Tips:**
- Maintains light distance
- Only changes rotation, not position
- Great for spotlights
- Can target multiple objects at once

---

### Mode 4: ORBIT

**Purpose:** Rotate light around pivot point

**How It Works:**
1. Gets pivot point (from light custom property)
2. Calculates current angle from pivot
3. Increments/decrements angle
4. Positions light at new angle, maintaining distance

**Use Cases:**
- 360° product shots
- Turntable lighting
- Circular light movement
- Rotating lighting setups

**How to Use:**
1. Select a light
2. Enable Orbit mode
3. Use MMB drag or arrow keys
4. Light rotates around subject
5. Maintains constant distance

**Algorithm:**
```
CurrentVector = LightPosition - PivotPoint
Distance = CurrentVector.length
RotationMatrix = Matrix.Rotation(AngleDelta, 'Z')
NewVector = RotationMatrix @ CurrentVector
NewPosition = PivotPoint + NewVector
```

**Tips:**
- Perfect for turntable animations
- Maintains distance automatically
- Can orbit multiple lights simultaneously
- Use with keyframes for rotation animation

---

### Mode 5: FREE

**Purpose:** Manual XYZ coordinate positioning

**How It Works:**
- Direct numerical input for X, Y, Z coordinates
- Can be relative or absolute positioning
- Precise control for exact placement

**Use Cases:**
- Precise positioning requirements
- Matching specific coordinates
- Technical/engineering visualization
- Grid-aligned lighting

**How to Use:**
1. Select a light
2. Enable Free mode
3. Enter X, Y, Z values
4. Choose Relative or Absolute
5. Click Apply

**Relative vs Absolute:**
- **Relative:** Adds values to current position
- **Absolute:** Sets exact world coordinates

**Tips:**
- Most precise positioning method
- Good for symmetric setups
- Use with Grid Snapping
- Copy coordinates between lights for alignment

---

### Mode 6: MOVE

**Purpose:** Interactive drag-based movement

**How It Works:**
- Modal operator (stays active)
- Click and drag to move light
- Real-time viewport feedback
- Axis constraints available

**Use Cases:**
- Intuitive light positioning
- Visual placement
- Quick adjustments
- Interactive fine-tuning

**How to Use:**
1. Select a light
2. Enable Move mode
3. Click and drag in viewport
4. Release to place light
5. ESC to cancel, ENTER to confirm

**Keyboard Modifiers:**
- `X` key: Constrain to X-axis
- `Y` key: Constrain to Y-axis
- `Z` key: Constrain to Z-axis
- `Shift`: Slow/precise movement

**Features:**
- Real-time viewport feedback
- Distance display
- Grid snapping support
- Undo support (`Ctrl+Z`)

**Tips:**
- Most intuitive positioning method
- Good for quick adjustments
- Use axis constraints for precise control
- Enable Grid Snapping for alignment

---

## Smart Controls

Adjust light properties with intuitive mouse gestures.

### Control Basics

**How to Use:**
1. Select a light
2. Select control mode (Distance, Power, etc.)
3. Hold `MMB` (Middle Mouse Button)
4. Drag left (decrease) or right (increase)
5. Release to confirm

**Visual Feedback:**
- HUD display shows property name and current value
- Real-time viewport update
- Color-coded indicators

### Control 1: DISTANCE

**Property:** Light distance from pivot point  
**Range:** 0.1m - 100m

**What It Does:**
- Moves light closer or farther from subject
- Maintains light direction
- Affects light intensity (inverse square law)

**Use Cases:**
- Quick distance adjustments
- Softening or hardening shadows
- Balancing multiple lights

**Tips:**
- Closer = brighter and harder shadows
- Farther = dimmer and softer shadows
- For area lights: distance also affects softness
- Use in combination with Power control

### Control 2: POWER

**Property:** Light intensity (Watts)  
**Range:** 1W - 10,000W

**What It Does:**
- Adjusts light brightness
- Does not change position or size
- Logarithmic scaling for precision

**Use Cases:**
- Balancing key and fill ratios
- Brightening or dimming scenes
- Fine-tuning exposure

**Common Values:**
- 50-150W: Fill lights
- 200-400W: Key lights
- 500-1000W: Sun lights
- 10-50W: Accent lights

**Tips:**
- Start with template defaults
- Key-to-fill ratio typically 2:1 to 4:1
- Use render preview to judge
- Remember inverse square law affects perceived brightness

### Control 3: SCALE

**Property:** Light size or radius  
**Range:** 0.01m - 50m

**What It Does:**
**For Area Lights:**
- Changes physical size
- Larger = softer shadows
- Smaller = harder shadows

**For Point/Spot Lights:**
- Changes radius
- Affects shadow softness

**Use Cases:**
- Softening harsh shadows
- Simulating different light sources
- Matching real-world fixtures

**Common Sizes:**
- 0.5-1m: Small softbox
- 2-4m: Large softbox
- 0.1-0.3m: Hard light source
- 10-20m: Large diffused sky

**Tips:**
- Larger is not always better
- Match size to real-world fixture
- Size affects render time
- Larger lights = softer but slower

### Control 4: ANGLE

**Property:** Spot light cone angle  
**Range:** 0° - 180°  
**Light Type:** Spot lights only

**What It Does:**
- Adjusts spot light cone width
- Narrow = focused beam
- Wide = broad coverage

**Use Cases:**
- Focused spotlights
- Stage lighting effects
- Dramatic lighting
- Selective illumination

**Common Angles:**
- 20-40°: Focused spotlight
- 45-60°: Standard spot
- 90-120°: Wide coverage
- 10-20°: Very focused beam

**Tips:**
- Combine with Blend control for soft edges
- Use for dramatic effects
- Can create "light pools"
- Adjust based on distance to subject

### Control 5: BLEND

**Property:** Shadow/edge softness  
**Range:** 0.0 (hard) - 1.0 (soft)

**What It Does:**
- Adjusts shadow edge softness
- 0.0 = Hard, crisp shadows
- 1.0 = Very soft, diffused shadows

**Use Cases:**
- Fine-tuning shadow quality
- Matching reference photos
- Stylistic choices (hard vs soft)
- Balancing realism

**Common Values:**
- 0.0-0.2: Harsh sunlight
- 0.3-0.5: Indoor lighting
- 0.6-0.8: Soft studio lighting
- 0.9-1.0: Very diffused

**Tips:**
- Works with Spot and Area lights
- Affects render time (higher = slower)
- Combine with Size for ultimate softness control
- Preview in rendered mode for accuracy

### Control 6: TEMPERATURE

**Property:** Color temperature (Kelvin)  
**Range:** 1000K - 12,000K

**What It Does:**
- Adjusts light color on warm-to-cool spectrum
- Lower K = warmer (orange/red)
- Higher K = cooler (blue)

**Color Guide:**

**Warm (1000K-3500K):**
- 1000K-2000K: Candlelight, fire (deep orange)
- 2500K-3000K: Tungsten bulbs (warm yellow)
- 3000K-3500K: Warm white (studio warm)

**Neutral (4000K-6000K):**
- 4000K-4500K: Fluorescent (neutral)
- 5000K-5500K: Daylight (neutral-cool)
- 5500K-6000K: Electronic flash

**Cool (6500K-12000K):**
- 6500K-7500K: Overcast sky (cool)
- 8000K-10000K: Clear blue sky
- 10000K+: Very cool blue

**Use Cases:**
- Matching real-world lighting
- Creating mood and atmosphere
- Color grading
- Separating light sources visually

**Tips:**
- Mix warm and cool for visual interest
- Warm = cozy, inviting
- Cool = clinical, sci-fi
- Neutral = professional, clean
- Reference real-world temperatures

---

## Light Linking System

Control which lights affect which objects.

### Concepts

**Light Linking:** Selective control of which objects a light illuminates

**Two Modes:**
1. **Include Mode:** Light ONLY affects linked objects
2. **Exclude Mode:** Light affects everything EXCEPT linked objects

### Quick Link

**Shortcut:** `Ctrl+Shift+X`

**How to Use:**
1. Select a light (make it active object)
2. Additionally select target objects
3. Press `Ctrl+Shift+X`
4. Light instantly links to selected objects

**Use Case Example:**
- Light only the hero product
- Exclude background from light
- Spotlight on specific character

### Object Groups

**Purpose:** Reusable collections of objects for linking

**Create Group:**
1. Select objects
2. LumiFlow panel → Light Linking
3. Click "Create Group from Selection"
4. Name your group
5. Group created!

**Use Group:**
1. Select light
2. Choose group from list
3. Click "Link Light to Group"
4. All group objects linked

**Benefits:**
- Reusable across multiple lights
- Easy management of complex scenes
- Batch linking operations

### Include vs Exclude

**Include Mode:**
```
Light → Only Linked Objects
Background → No light received
Result: Focused, selective lighting
```

**Use When:**
- Spotlight on hero object
- Stage lighting on performer
- Product-only lighting

**Exclude Mode:**
```
Light → Everything EXCEPT Linked Objects
Background → Receives light
Result: Light avoids certain objects
```

**Use When:**
- Remove foreground from backlight
- Prevent unwanted reflections
- Avoid lighting specific objects

### Collection-Based Linking

**Alternative Method:** Use Blender collections

1. Create collection in Outliner
2. Add objects to collection
3. LumiFlow panel → Link to Collection
4. Choose collection
5. Light links to all collection objects

**Benefits:**
- Integrates with existing workflow
- Works with Blender's native system
- Dynamic (new objects auto-link)

### Advanced Techniques

**Multiple Lights, One Group:**
- Create object group
- Link multiple lights to same group
- All lights affect only group objects

**Layered Lighting:**
1. Key light: Links to hero only (Include)
2. Fill light: Links to everything (no linking)
3. Rim light: Excludes foreground (Exclude)

**Per-Object Lighting:**
- Each object gets dedicated light
- All other objects excluded
- Complete control over each object's lighting

---

## Camera Assignment System

Organize lights for multi-camera setups.

### Understanding Modes

**SCENE Mode (Global):**
- Lights visible in ALL cameras
- Prefix: `G_`
- Simple, straightforward

**CAMERA Mode (Per-Camera):**
- Lights assigned to specific cameras
- Prefix: `C_XX_`
- Professional multi-angle setups

### Scene Mode Workflow

**Best For:**
- Single-camera projects
- Simple scenes
- Beginners

**How It Works:**
1. Set mode to SCENE
2. Add lights
3. All lights get `G_` prefix
4. Always visible regardless of camera

**Example:**
```
G_KeyLight
G_FillLight
G_RimLight
```

### Camera Mode Workflow

**Best For:**
- Multi-camera studios
- Different lighting per angle
- Professional workflows

**How It Works:**
1. Set mode to CAMERA
2. Set Camera 1 active
3. Add lights → `C_01_*` prefix
4. Switch to Camera 2
5. Add lights → `C_02_*` prefix
6. Lights auto show/hide per camera

**Example:**
```
Camera 1:
  - C_01_KeyLight (visible)
  - C_01_FillLight (visible)

Camera 2:
  - C_02_KeyLight (visible)
  - C_02_DramaticRim (visible)

When Camera 1 active: See C_01_* lights
When Camera 2 active: See C_02_* lights
```

### Multi-Camera Setup Tutorial

**Scenario:** Product shot from 3 angles

**Step 1: Create Cameras**
1. Add Camera 1 (front view)
2. Position and angle
3. Duplicate (`Shift+D`) for Camera 2 (side)
4. Duplicate again for Camera 3 (top)

**Step 2: Set Camera Mode**
1. LumiFlow panel
2. Click CAMERA button

**Step 3: Light Each Camera**

**Camera 1 (Front):**
1. Set Camera 1 active (`Ctrl+Numpad 0`)
2. Apply "Product Shot Basic"
3. Lights: `C_01_KeyLight`, `C_01_FillLight`

**Camera 2 (Side):**
1. Switch to Camera 2
2. Apply "Dramatic Portrait"
3. Lights: `C_02_KeyLight`, `C_02_RimLight`

**Camera 3 (Top):**
1. Switch to Camera 3
2. Manually add lights
3. Lights: `C_03_TopKey`, `C_03_Fill`

**Step 4: Add Global Light**
1. Switch to SCENE mode temporarily
2. Add rim light
3. Creates `G_RimLight`
4. Visible in all cameras!
5. Switch back to CAMERA mode

**Step 5: Test**
1. Switch through cameras
2. Observe light visibility changes
3. Each camera has unique lighting + global light

### Naming Convention

**Global Lights:**
```
G_LightName
G_KeyLight
G_SunLight
G_RimLight
```

**Camera Lights:**
```
C_XX_LightName
C_01_KeyLight    (Camera 1)
C_02_KeyLight    (Camera 2)
C_15_BackLight   (Camera 15)
```

**Parsing:**
- `G_` = Global
- `C_` = Camera-specific
- `XX` = Two-digit camera number
- Rest = Light name

### Auto-Switching

**How It Works:**
- Scene update handler detects camera changes
- Parses all light names in scene
- Shows lights matching active camera
- Hides non-matching camera lights
- Always shows global (`G_`) lights

**Performance:**
- Cached for speed
- Debounced to prevent rapid updates
- Efficient even with 50+ lights

### Persistence

**Saving:**
- Light assignments saved in light names
- No external data files
- Open file anywhere = assignments work

**Blender Restart:**
- All assignments persist
- Names are part of Blender data
- No reconfiguration needed

---

## Flip Operations

Mirror or rotate entire lighting setups.

### 8 Flip Operations

**Access:** `Ctrl+Shift+C` (Flip menu)

### 1. Flip Horizontal

**Function:** Mirror lights across vertical plane (X-axis)

**Algorithm:**
```
NewX = -OldX
NewY = OldY
NewZ = OldZ
```

**Use Case:**
- Set up left side, flip to right
- Mirror lighting setups
- Symmetric lighting

### 2. Flip Vertical

**Function:** Mirror lights across horizontal plane (Z-axis)

**Algorithm:**
```
NewX = OldX
NewY = OldY
NewZ = -OldZ
```

**Use Case:**
- Top to bottom flip
- Invert lighting setup

### 3. Front/Back Swap

**Function:** Swap lights front/back of subject

**Reference:** Camera forward vector

**Use Case:**
- Reverse lighting direction
- Swap key and rim positions

### 4. Left/Right Swap

**Function:** Swap lights left/right of subject

**Reference:** Camera right vector

**Use Case:**
- Swap side lighting
- Mirror left-right only

### 5. To Camera Front

**Function:** Position light behind target, facing camera

**Arrangement:** Light → Subject → Camera

**Use Case:**
- Backlight facing camera
- Rim lights
- Edge lighting

### 6. To Camera Back

**Function:** Position light in front of target, facing away from camera

**Arrangement:** Camera → Subject → Light

**Use Case:**
- Key light facing away
- Unusual dramatic lighting

### 7. Rotate Around Camera Z

**Function:** 180° rotation around camera Z-axis

**Use Case:**
- Rotate entire setup around camera
- Maintain camera-relative positions

### 8. Rotate Around Target Z

**Function:** 180° rotation around target Z-axis

**Use Case:**
- Rotate setup around subject
- Maintain subject-relative positions

### Multi-Light Support

**All operations work with:**
- Single lights
- Multiple selected lights
- Entire lighting setups

**Workflow:**
1. Select lights to flip (or all: `A` key)
2. Press `Ctrl+Shift+C`
3. Choose operation
4. All selected lights transform together
5. Relative positions preserved

---

## Selection Tools

Quick navigation and isolation tools.

### Cycle Select Light

**Shortcut:** `D` key

**Function:** Cycle through all scene lights

**Order:** Closest to camera first

**Behavior:**
- Press once: Select next light
- Keeps pressing: Cycles through all
- Wraps around to first light
- Skips non-light objects

**Use Cases:**
- Quickly check all lights
- Find specific light
- Rapid property adjustments

### Solo Light

**Shortcut:** `Ctrl+Shift+D`

**Function:** Isolate single light

**How It Works:**
1. Select a light
2. Press `Ctrl+Shift+D`
3. All other lights hide (viewport and render)
4. Only selected light visible

**Unsolo:**
- Press `Ctrl+Shift+D` again
- All lights restore

**Use Cases:**
- Test individual light contribution
- Fine-tune without interference
- Understand each light's role
- Debug lighting issues

**Benefits:**
- See exactly what each light does
- Adjust in isolation
- Prevents confusion in complex setups

---

## Tips & Best Practices

### Positioning

**Start Broad, Then Refine:**
1. Use templates for base positioning
2. Use Move mode for rough adjustments
3. Use specific modes (Highlight, Target) for precision
4. Final tweaks with Smart Controls

**Layered Approach:**
- Key light first (main illumination)
- Fill light second (shadow control)
- Rim/accent last (final touches)

### Smart Controls

**Use Preview Modes:**
- Material Preview for interactive feedback
- Rendered for accurate preview
- Solid for fast positioning

**Adjust One Property at a Time:**
- Change distance, observe
- Then power, observe
- Then temperature, observe
- Systematic approach prevents confusion

### Light Linking

**Plan Groups Early:**
- Define object groups before lighting
- Group by purpose (hero, background, props)
- Reuse groups across scenes

**Test Frequently:**
- Render preview after each link
- Verify include/exclude behavior
- Check for unintended shadows

### Camera Assignment

**Name Cameras Clearly:**
- Camera_Front
- Camera_Side
- Camera_Top
- Easier to match with C_01, C_02, etc.

**Document Your Setup:**
- Note which camera is which number
- Use Blender's camera bookmarks
- Name lights descriptively

---

## Next Steps

**Fantastic!** You've mastered LumiFlow's advanced features!

### Continue to Part 5

In **Part 5: Reference & Support**, you'll find:
- Complete keyboard shortcut reference
- Tips and best practices
- Troubleshooting guide
- Frequently asked questions
- Community resources

👉 **[Continue to Part 5 →](05_Reference_Support.md)**

---

## Quick Links

- [← Back to Part 3](03_Template_Library.md)
- [Back to Index](00_INDEX.md)
- [Part 5: Reference & Support →](05_Reference_Support.md)

---

**Master the Tools!** 🎯✨
