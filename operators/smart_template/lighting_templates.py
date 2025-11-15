"""
LumiFlow Lighting Templates Operator - Refactored
Orchestration only, delegates to core + utils.
"""

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from mathutils import Vector
from typing import List, Dict, Any

from ...utils.common import (
    lumi_is_addon_enabled, lumi_get_light_collection, lumi_move_to_collection
)
from ...utils.light import lumi_set_light_pivot
from ...utils.scene_context import SceneAnalyzer, SceneContext
from ...utils.positioning import (
    calculate_position_from_template, calculate_optimal_distance
)
from ...utils.material_adaptation import (
    generate_lighting_recommendations, apply_material_adjustments_to_light
)
from ...utils.obstruction_detector import get_enhanced_detector
from ...utils.color import lumi_kelvin_to_rgb
from ...core.template_system import TemplateSystem, ValidationResult
from ...utils.template_intelligence import (
    get_research_template_entry,
    get_research_lookup_tables,
)
from .template_library import get_template


def _template_enum_items(self, context):
    """Dynamic enum items for template selection in the apply dialog."""
    items = []
    current_id = getattr(self, "template_id", "") or ""
    try:
        from .template_library import list_templates
        templates = list_templates()
        has_current = False

        # Read Studio & Commercial visibility preferences so the list of
        # templates here is consistent with the Studio menu categories.
        prefs = None
        try:
            addon = bpy.context.preferences.addons.get("LumiFlow")
            if addon:
                prefs = addon.preferences
        except Exception:
            prefs = None

        show_apparel = getattr(prefs, "studio_commercial_show_apparel", True) if prefs else True
        show_automotive = getattr(prefs, "studio_commercial_show_automotive", True) if prefs else True
        show_cosmetics = getattr(prefs, "studio_commercial_show_cosmetics", True) if prefs else True
        show_electronics = getattr(prefs, "studio_commercial_show_electronics", True) if prefs else True
        show_food = getattr(prefs, "studio_commercial_show_food", True) if prefs else True
        show_furniture = getattr(prefs, "studio_commercial_show_furniture", True) if prefs else True
        show_jewelry = getattr(prefs, "studio_commercial_show_jewelry", True) if prefs else True
        # Generic flag is optional in preferences; default to True
        show_generic = getattr(prefs, "studio_commercial_show_generic", True) if prefs else True

        for tmpl in templates:
            tid = tmpl.get("id") or tmpl.get("template_id")
            if not tid:
                continue

            # Apply Studio & Commercial visibility filters based on template ID
            category = tmpl.get("category", "") or ""
            include = True
            if category == "Studio & Commercial":
                tid_lower = tid.lower()
                if tid_lower.startswith("apparel_") and not show_apparel:
                    include = False
                elif tid_lower.startswith("automotive_") and not show_automotive:
                    include = False
                elif tid_lower.startswith("cosmetics_") and not show_cosmetics:
                    include = False
                elif tid_lower.startswith("electronics_") and not show_electronics:
                    include = False
                elif tid_lower.startswith("food_") and not show_food:
                    include = False
                elif tid_lower.startswith("furniture_") and not show_furniture:
                    include = False
                elif tid_lower.startswith("jewelry_") and not show_jewelry:
                    include = False
                else:
                    # Generic Studio & Commercial template (no product prefix)
                    if not show_generic:
                        include = False

            if not include:
                continue

            name = tmpl.get("name", tid)
            desc = tmpl.get("description", "")
            items.append((tid, name, desc))
            if tid == current_id:
                has_current = True
        if current_id and not has_current:
            items.append((current_id, current_id, "Current template"))
        if not items:
            items.append(("default", "Default", "Default template"))
    except Exception:
        # Fallback: only expose current template id
        if current_id:
            items = [(current_id, current_id, "Current template")]
        else:
            items = [("default", "Default", "Default template")]
    return items


def _on_template_choice_update(self, context):
    """Keep template_id in sync when user changes template in the dialog."""
    try:
        if getattr(self, "template_choice", ""):
            self.template_id = self.template_choice
    except Exception:
        pass


class LUMI_OT_apply_lighting_template(bpy.types.Operator):
    """Apply photographic lighting template to selected objects"""
    bl_idname = "lumi.apply_lighting_template"
    bl_label = "Apply Lighting Template"
    bl_options = {'REGISTER', 'UNDO'}

    # === PROPERTIES ===
    template_id: StringProperty(name="Template ID", default="")
    template_choice: EnumProperty(
        name="Template",
        items=_template_enum_items,
        update=_on_template_choice_update,
    )
    auto_scale: BoolProperty(name="Auto Scale", default=True)
    manual_distance: FloatProperty(name="Manual Distance", default=0.0, min=0.0)
    use_camera_relative: BoolProperty(name="Camera Relative", default=False)
    enable_obstruction_detection: BoolProperty(name="Obstruction Detection", default=False)
    obstruction_fallback_strategy: EnumProperty(
        name="Fallback Strategy",
        items=[
            ('SKIP_LIGHT', "Skip Light", "Skip lights with obstructions"),
            ('ADJUST_POSITION', "Adjust Position", "Find clear position"),
            ('WARN_ONLY', "Warn Only", "Create anyway with warning"),
        ],
        default='ADJUST_POSITION'
    )
    show_obstruction_warnings: BoolProperty(name="Show Warnings", default=True)
    use_material_adaptation: BoolProperty(name="Material Adaptation", default=True)
    intensity_multiplier: FloatProperty(name="Intensity Multiplier", default=1.0, min=0.1)
    size_multiplier: FloatProperty(name="Size Multiplier", default=1.0, min=0.1)
    preserve_existing: BoolProperty(name="Preserve Existing", default=False)
    apply_mode: EnumProperty(
        name="Apply Mode",
        items=[
            ('GUIDED_STRICT', "Guided (Strict)", "Match recommended lighting ratios and color as strictly as possible"),
            ('BALANCED', "Guided (Balanced)", "Blend smart defaults with template values"),
            ('CREATIVE', "Creative", "Allow more deviation from the guided defaults"),
        ],
        default='BALANCED',
    )
    contrast_preset: EnumProperty(
        name="Contrast Preset",
        items=[
            ('NEUTRAL', "Neutral", "Use base ratios as-is"),
            ('SOFTER', "Softer", "Slightly reduce contrast (more fill)"),
            ('MORE_CONTRAST', "More Contrast", "Slightly increase contrast (stronger key/rim)"),
        ],
        default='NEUTRAL',
    )
    material_profile_override: EnumProperty(
        name="Material Profile",
        items=[
            ('AUTO', "Auto", "Use detected material profile from scene"),
            ('REFLECTIVE', "Highly Reflective", "Treat as metallic/high gloss"),
            ('MATTE', "Dark Matte", "Treat as dark matte surfaces"),
            ('MIXED', "Mixed", "Mixed materials; use neutral adjustment"),
        ],
        default='AUTO',
    )
    scene_product_type_override: EnumProperty(
        name="Scene Category",
        items=[
            ('AUTO', "Auto (Detected)", "Use detected scene product type"),
            ('jewelry', "Jewelry", "Jewelry products"),
            ('watches', "Watches", "Watch products"),
            ('food', "Food", "Food / beverage products"),
            ('cosmetics', "Cosmetics", "Cosmetics and beauty"),
            ('apparel', "Apparel", "Clothing / fashion"),
            ('electronics', "Electronics", "Electronic devices"),
            ('furniture', "Furniture", "Furniture and interior objects"),
            ('automotive', "Automotive", "Cars and vehicles"),
        ],
        default='AUTO',
    )

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def invoke(self, context, event):
        """Invoke operator with dialog when called from UI.

        Basic research-aware defaults are applied here so the dialog starts
        with sensible values without forcing behavior during execute().
        """

        # Sync dropdown template_choice with current template_id so the
        # dialog starts with the template that initiated the operator.
        if getattr(self, "template_id", ""):
            try:
                self.template_choice = self.template_id
            except Exception:
                pass

        # Initialize intensity multiplier lightly from research mood profile
        try:
            effective_template_id = self.template_choice or self.template_id
            research_entry = get_research_template_entry(effective_template_id)
        except Exception:
            research_entry = {}

        if research_entry and abs(self.intensity_multiplier - 1.0) < 1e-3:
            moods = research_entry.get("mood", []) or []
            moods_lower = [m.lower() for m in moods]
            # Very simple heuristic: high_key/clean a bit brighter, dramatic/low_key a bit darker
            if any(m in moods_lower for m in ("high_key", "clean")):
                self.intensity_multiplier = 1.1
            elif any(m in moods_lower for m in ("low_key", "dramatic")):
                self.intensity_multiplier = 0.9

        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        """Draw operator properties in dialog"""
        layout = self.layout

        # Header: template selection (dropdown)
        layout.prop(self, "template_choice")

        # Scene category override + compatibility summary
        detected_product_type = getattr(context.scene, "lumi_product_type", "unknown") or "unknown"
        product_types_text = "n/a"
        product_types = []
        try:
            research_entry = get_research_template_entry(self.template_id)
            product_types = research_entry.get("product_types", []) if research_entry else []
            if product_types:
                product_types_text = ", ".join(product_types)
        except Exception:
            product_types_text = "n/a"

        layout.prop(self, "scene_product_type_override", text="Scene")

        # Determine effective scene type (override if set, otherwise detected)
        override = self.scene_product_type_override
        if override and override != 'AUTO':
            effective_scene_type = override
        else:
            effective_scene_type = detected_product_type

        # Live compatibility indicator (Match / Mismatch)
        row = layout.row()
        if effective_scene_type in {"", "unknown"} or not product_types:
            row.label(text="Not enough data")
        else:
            if effective_scene_type in product_types:
                row.label(text="Match")
            else:
                row.alert = True
                row.label(text="Mismatch")

        layout.separator()

        # Apply mode (research-strict / balanced / creative)
        layout.prop(self, "apply_mode")

        layout.separator()

        # Placement & preservation
        cameras_in_scene = any(obj.type == 'CAMERA' for obj in context.scene.objects)
        if cameras_in_scene:
            layout.prop(self, "use_camera_relative")
        else:
            row = layout.row()
            row.label(text="Camera Relative: No cameras in scene")
            row.enabled = False

        layout.prop(self, "preserve_existing")
        layout.prop(self, "enable_obstruction_detection")

        layout.separator()

        # Global controls
        col = layout.column()
        col.prop(self, "intensity_multiplier")
        col.prop(self, "size_multiplier")
        col.prop(self, "use_material_adaptation")

        layout.separator()

        # Advanced: Geometry & Distance
        box = layout.box()
        box.label(text="Geometry & Distance")
        box.prop(self, "auto_scale")
        box.prop(self, "manual_distance")

        # Advanced: Ratios & Mood
        box = layout.box()
        box.label(text="Ratios & Mood")
        box.prop(self, "contrast_preset")

        # Advanced: Material & Adaptation
        box = layout.box()
        box.label(text="Material & Adaptation")
        box.prop(self, "use_material_adaptation")
        box.prop(self, "material_profile_override")

    def execute(self, context):
        """Main execution - orchestration only."""
        try:
            # === 1. VALIDATE ===
            template_system = TemplateSystem()

            # Validate template
            template_validation = template_system.validate_template(self.template_id)
            if not template_validation.valid:
                for error in template_validation.errors:
                    self.report({'ERROR'}, error)
                return {'CANCELLED'}

            # Validate scene
            scene_validation = template_system.validate_scene(context, context.selected_objects)
            if not scene_validation.valid:
                for error in scene_validation.errors:
                    self.report({'ERROR'}, error)
                return {'CANCELLED'}

            for warning in scene_validation.warnings:
                self.report({'WARNING'}, warning)

            template = template_system.current_template

            # === 2. ANALYZE SCENE ===
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(
                context.selected_objects,
                include_camera=True,
                include_classification=self.enable_obstruction_detection,
                include_materials=self.use_material_adaptation
            )

            # Apply scene category override (if user chooses a specific type)
            override = getattr(self, "scene_product_type_override", "AUTO")
            if override and override != 'AUTO':
                scene_ctx.product_type = override
                try:
                    context.scene.lumi_product_type = override
                except Exception:
                    pass

            # Precompute a lightweight research-based intensity factor that
            # combines material and mood profiles. Stored on the operator
            # instance and used by _create_single_light().
            self._runtime_intensity_factor = self._compute_profile_intensity_factor(scene_ctx)

            # === 2b. CONTEXT-AWARE WARNING (non-blocking, research-based) ===

            # === 3. CLEAR EXISTING LIGHTS (if requested) ===
            if not self.preserve_existing:
                self._clear_existing_lights(context)

            # === 4. CALCULATE POSITIONS ===
            positions = self._calculate_light_positions(scene_ctx, template, context)

            # === 5. HANDLE OBSTRUCTIONS ===
            if self.enable_obstruction_detection and scene_ctx.classifications:
                positions = self._adjust_for_obstructions(positions, scene_ctx, context)

            # === 5. CREATE LIGHTS ===
            lights = self._create_lights(positions, template, context)

            if not lights:
                self.report({'WARNING'}, "No lights created")
                return {'CANCELLED'}

            # === 6. BASIC RESEARCH RATIOS (intensity) ===
            self._apply_basic_intensity_ratios(lights)

            # === 7. MATERIAL ADAPTATIONS ===
            if self.use_material_adaptation and scene_ctx.materials:
                recommendations = generate_lighting_recommendations(scene_ctx.materials)
                for light in lights:
                    apply_material_adjustments_to_light(light, recommendations)

            # === 8. ORGANIZE ===
            self._organize_lights(lights, context)

            # === 9. SELECT ===
            self._select_lights(lights, context)

            self.report({'INFO'}, f"Applied '{self.template_id}': {len(lights)} lights created")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply template: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def _compute_profile_intensity_factor(self, scene_ctx: SceneContext) -> float:
        """Compute a small global intensity factor from material & mood profiles.

        Phase 2 integration: we only nudge intensity slightly based on
        high-level profiles, and clamp the result to a safe range.
        """

        factor = 1.0

        # 1) Material profile influence
        try:
            lookup = get_research_lookup_tables()
        except Exception:
            lookup = {}

        mat_profiles = lookup.get("material_profiles", []) or []
        material_data = getattr(scene_ctx, "materials", None)

        if material_data:
            dominant_type = getattr(material_data, "dominant_type", "") or ""
            avg_roughness = getattr(material_data, "average_roughness", 0.5)

            target_profile_name = None
            if dominant_type == "metallic":
                target_profile_name = "metallic_high_gloss"
            elif dominant_type == "dielectric" and avg_roughness > 0.7:
                target_profile_name = "dark_matte"

            if target_profile_name:
                for mp in mat_profiles:
                    if mp.get("name") == target_profile_name:
                        try:
                            mp_factor = float(mp.get("recommended_intensity_multiplier", 1.0))
                            if mp_factor > 0:
                                factor *= mp_factor
                        except Exception:
                            pass
                        break

        # 2) Mood profile influence (simple high_key vs low_key adjustment)
        try:
            research_entry = get_research_template_entry(self.template_id)
        except Exception:
            research_entry = {}

        moods = [m.lower() for m in (research_entry.get("mood", []) or [])]
        if any(m in moods for m in ("high_key", "clean")):
            factor *= 1.05
        if any(m in moods for m in ("low_key", "dramatic")):
            factor *= 0.95

        # Clamp to a conservative range to avoid extreme jumps
        factor = max(0.6, min(1.6, factor))
        return factor

    def _calculate_light_positions(self, scene_ctx: SceneContext,
                                   template: Dict, context) -> List[Dict]:
        """Calculate initial light positions (no obstruction)."""
        positions = []

        # Calculate base distance
        if self.manual_distance > 0:
            base_distance = self.manual_distance
        else:
            template_distance = template.get('settings', {}).get('base_distance', 2.0)
            distance_profile = self._build_distance_profile(scene_ctx)
            base_distance = calculate_optimal_distance(
                scene_ctx.bounds,
                template_distance,
                self.auto_scale,
                distance_profile=distance_profile,
            )

        # Get camera matrix if needed
        camera_matrix = None
        if self.use_camera_relative and scene_ctx.camera:
            camera_matrix = scene_ctx.camera.matrix

        # Calculate each light position
        for light_template in template.get('lights', []):
            try:
                position = calculate_position_from_template(
                    light_template,
                    scene_ctx.bounds.center,
                    base_distance,
                    camera_matrix=camera_matrix,
                    use_camera_relative=self.use_camera_relative
                )

                positions.append({
                    'light_template': light_template,
                    'position': position,
                    'target': scene_ctx.bounds.center
                })
            except Exception as e:
                self.report({'WARNING'}, f"Failed to calculate position: {e}")
                continue

        return positions

    def _build_distance_profile(self, scene_ctx: SceneContext) -> Dict[str, Any]:
        """Build a simple distance_profile dict from research metadata.

        This Phase 2 implementation is intentionally conservative:
        - Uses product_type (scene or template) to pick a base distance_factor.
        - Applies small adjustments based on mood tags (high_key/low_key).
        - Provides optional min/max distance clamps for extreme cases.
        """

        profile: Dict[str, Any] = {}

        # Try to read research entry; fall back to defaults if unavailable
        try:
            research_entry = get_research_template_entry(self.template_id)
        except Exception:
            research_entry = {}

        # Determine effective product_type
        scene_product_type = getattr(scene_ctx, "product_type", "unknown") or "unknown"
        template_product_types = research_entry.get("product_types", []) or []

        if scene_product_type and scene_product_type not in {"", "unknown"}:
            effective_product_type = scene_product_type
        elif template_product_types:
            effective_product_type = str(template_product_types[0])
        else:
            effective_product_type = "generic"

        effective_product_type = effective_product_type.lower()

        # Base factor by product_type (small objects vs large subjects)
        distance_factor = 1.0
        min_distance = None
        max_distance = None

        if effective_product_type in {"jewelry", "watches"}:
            distance_factor = 0.7
            min_distance = 0.4
            max_distance = 3.0
        elif effective_product_type in {"food", "cosmetics"}:
            distance_factor = 0.9
            min_distance = 0.5
            max_distance = 4.0
        elif effective_product_type in {"apparel", "electronics", "furniture"}:
            distance_factor = 1.0
            min_distance = 0.8
            max_distance = 8.0
        elif effective_product_type in {"automotive"}:
            distance_factor = 1.3
            min_distance = 3.0
            max_distance = 20.0

        # Mood-based refinement (high_key vs low_key)
        moods = [m.lower() for m in research_entry.get("mood", []) or []]
        if any(m in moods for m in ("high_key", "clean")):
            distance_factor *= 0.95  # slightly closer for high-key/clean
        if any(m in moods for m in ("low_key", "dramatic")):
            distance_factor *= 1.05  # slightly farther for low-key/dramatic

        profile["distance_factor"] = float(distance_factor)
        if min_distance is not None:
            profile["min_distance"] = float(min_distance)
        if max_distance is not None:
            profile["max_distance"] = float(max_distance)

        return profile

    def _adjust_for_obstructions(self, positions: List[Dict],
                                 scene_ctx: SceneContext, context) -> List[Dict]:
        """Adjust positions for obstructions."""
        from ...utils.operators import lumi_ray_cast_between_points

        adjusted_positions = []
        background_objects = scene_ctx.get_background_objects()

        for pos_data in positions:
            has_obstruction, hit_location = self._check_obstruction(
                pos_data['position'], pos_data['target'],
                background_objects, context
            )

            if has_obstruction:
                if self.obstruction_fallback_strategy == 'SKIP_LIGHT':
                    if self.show_obstruction_warnings:
                        name = pos_data['light_template'].get('name', 'Light')
                        self.report({'WARNING'}, f"{name}: Skipped due to obstruction")
                    continue
                elif self.obstruction_fallback_strategy == 'ADJUST_POSITION':
                    # Find clear position
                    clear_pos = self._find_clear_position(
                        pos_data['position'], pos_data['target'],
                        background_objects, context
                    )
                    if clear_pos:
                        pos_data['position'] = clear_pos
                    else:
                        continue
                # WARN_ONLY: continue with warning
                elif self.show_obstruction_warnings:
                    name = pos_data['light_template'].get('name', 'Light')
                    self.report({'WARNING'}, f"{name}: Has obstruction")

            adjusted_positions.append(pos_data)

        # Update pivots for adjusted positions
        for pos_data in adjusted_positions:
            if 'light_obj' in pos_data:
                # Position was adjusted, update pivot to target
                lumi_set_light_pivot(pos_data['light_obj'], pos_data['target'])

        return adjusted_positions

    def _check_obstruction(self, from_pos: Vector, to_pos: Vector,
                           obstacles: List, context) -> tuple:
        """Check for obstruction using raycast."""
        from ...utils.operators import lumi_ray_cast_between_points

        hit, hit_obj, hit_location, distance = lumi_ray_cast_between_points(
            context, from_pos, to_pos
        )

        if hit and hit_obj in obstacles:
            return (True, hit_location)
        return (False, None)

    def _find_clear_position(self, original: Vector, target: Vector,
                            obstacles: List, context, max_attempts=10) -> Vector:
        """Find clear position near original."""
        import random

        direction = (original - target).normalized()
        distance = (original - target).length

        for i in range(max_attempts):
            # Try positions around original
            offset = Vector((
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-0.5, 1)
            )).normalized() * (distance * 0.2)

            test_pos = original + offset
            has_obstruction, _ = self._check_obstruction(test_pos, target, obstacles, context)

            if not has_obstruction:
                return test_pos

        return None

    def _create_lights(self, positions: List[Dict], template: Dict, context) -> List:
        """Create light objects from positions."""
        lights = []

        for pos_data in positions:
            try:
                light = self._create_single_light(pos_data, context)
                if light:
                    lights.append(light)
            except Exception as e:
                self.report({'WARNING'}, f"Failed to create light: {e}")
                continue

        return lights

    def _apply_basic_intensity_ratios(self, lights: List[bpy.types.Object]) -> None:
        """Apply simple research-based intensity ratios for key/fill/back/rim.

        This is a light-touch Phase 1 implementation:
        - Uses research_lookup_templates.json (key_*_ratio fields) when available.
        - Derives light roles heuristically from object names (Key/Fill/Back/Rim).
        - If metadata or roles are missing, it safely falls back without changes.
        - Operates on already-created lights (energies already include user multipliers).
        """

        # Only operate when we have lights and a valid template id
        if not lights or not self.template_id:
            return

        # Skip in creative mode for now (Phase 3 will refine behavior)
        apply_mode = getattr(self, "apply_mode", "BALANCED")
        if apply_mode == 'CREATIVE':
            return

        try:
            research_entry = get_research_template_entry(self.template_id)
        except Exception:
            research_entry = {}

        if not research_entry:
            return

        key_fill_ratio = research_entry.get("key_fill_ratio")
        key_back_ratio = research_entry.get("key_back_ratio")
        key_rim_ratio = research_entry.get("key_rim_ratio")

        # If no ratios defined, do nothing
        if not any([key_fill_ratio, key_back_ratio, key_rim_ratio]):
            return

        # Helper to strip G_/C_XX_ prefixes from light names
        def _base_name(obj_name: str) -> str:
            name = obj_name
            if name.startswith("G_"):
                return name[2:]
            if name.startswith("C_") and "_" in name[2:5]:
                # C_XX_Name pattern
                parts = name.split("_", 2)
                if len(parts) == 3:
                    return parts[2]
            return name

        # Classify lights by heuristic roles
        key_lights = []
        fill_lights = []
        back_lights = []
        rim_lights = []

        for light in lights:
            data = getattr(light, "data", None)
            if not data or not hasattr(data, "energy"):
                continue
            base = _base_name(light.name).lower()
            if "key" in base:
                key_lights.append(light)
            elif "fill" in base:
                fill_lights.append(light)
            elif "rim" in base or "edge" in base:
                rim_lights.append(light)
            elif "back" in base or "background" in base or "bg" in base:
                back_lights.append(light)

        # If we couldn't detect any key light, pick the brightest as key
        if not key_lights:
            brightest = None
            max_energy = -1.0
            for light in lights:
                data = getattr(light, "data", None)
                if not data or not hasattr(data, "energy"):
                    continue
                if data.energy > max_energy:
                    max_energy = data.energy
                    brightest = light
            if brightest is not None:
                key_lights.append(brightest)

        if not key_lights:
            # Still nothing usable
            return

        # Compute baseline KEY energy (average of current key lights)
        key_energies = [light.data.energy for light in key_lights if hasattr(light.data, "energy")]
        if not key_energies:
            return
        base_key_energy = sum(key_energies) / len(key_energies)

        # Helper to adjust a group of lights to target ratio
        def _apply_ratio(group: List[bpy.types.Object], ratio: float) -> None:
            if not group or not ratio or ratio <= 0:
                return
            ratio_adj = float(ratio)
            preset = getattr(self, "contrast_preset", "NEUTRAL")
            if apply_mode == 'BALANCED':
                if preset == 'SOFTER':
                    ratio_adj *= 0.8
                elif preset == 'MORE_CONTRAST':
                    ratio_adj *= 1.2
            if ratio_adj <= 0:
                ratio_adj = float(ratio)
            target = base_key_energy / ratio_adj
            for obj in group:
                data = getattr(obj, "data", None)
                if not data or not hasattr(data, "energy"):
                    continue
                current = data.energy
                if apply_mode == 'GUIDED_STRICT':
                    data.energy = target
                else:
                    # Simple blend: 50% current, 50% target for balanced behavior
                    data.energy = (current * 0.5) + (target * 0.5)

        # Adjust fill / back / rim according to available ratios
        if key_fill_ratio:
            _apply_ratio(fill_lights, float(key_fill_ratio))
        if key_back_ratio:
            _apply_ratio(back_lights, float(key_back_ratio))
        if key_rim_ratio:
            _apply_ratio(rim_lights, float(key_rim_ratio))

    def _create_single_light(self, pos_data: Dict, context) -> bpy.types.Object:
        """Create single light object."""
        light_template = pos_data['light_template']

        # Create light data
        light_type = light_template.get('type', 'AREA')
        base_name = light_template.get('name', 'Light')
        
        # Add prefix based on assignment mode
        assignment_mode = getattr(context.scene, 'lumi_light_assignment_mode', 'SCENE')
        if assignment_mode == 'SCENE':
            light_name = f"G_{base_name}"
        else:  # CAMERA mode
            active_camera = context.scene.camera
            if active_camera:
                camera_name = active_camera.name
                # Determine camera prefix
                if camera_name.endswith('.001'):
                    camera_prefix = 'C_01'
                elif camera_name.endswith('.002'):
                    camera_prefix = 'C_02'
                elif camera_name.endswith('.003'):
                    camera_prefix = 'C_03'
                elif camera_name.endswith('.004'):
                    camera_prefix = 'C_04'
                elif camera_name.endswith('.005'):
                    camera_prefix = 'C_05'
                elif camera_name.endswith('.006'):
                    camera_prefix = 'C_06'
                elif camera_name.endswith('.007'):
                    camera_prefix = 'C_07'
                elif camera_name.endswith('.008'):
                    camera_prefix = 'C_08'
                elif camera_name.endswith('.009'):
                    camera_prefix = 'C_09'
                elif camera_name == 'Camera':
                    camera_prefix = 'C_00'
                else:
                    import re
                    match = re.search(r'\d+', camera_name)
                    camera_num = match.group(0).zfill(2) if match else '00'
                    camera_prefix = f'C_{camera_num}'
                light_name = f"{camera_prefix}_{base_name}"
            else:
                light_name = f"C_00_{base_name}"
        
        light_data = bpy.data.lights.new(light_name, light_type)

        # Get properties dict
        properties = light_template.get('properties', {})

        # Set base intensity (including runtime factor from material/mood profiles)
        runtime_factor = getattr(self, "_runtime_intensity_factor", 1.0)
        intensity = properties.get('intensity', 100.0) * self.intensity_multiplier * runtime_factor
        light_data.energy = intensity

        # Determine base color from template
        base_color = properties.get('color', (1.0, 1.0, 1.0))
        color = base_color

        # If template color is effectively neutral, we may override with
        # research-based color temperature (unless in CREATIVE mode).
        apply_mode_color = getattr(self, "apply_mode", "BALANCED")
        if apply_mode_color != 'CREATIVE':
            try:
                research_entry = get_research_template_entry(self.template_id)
            except Exception:
                research_entry = {}

            if research_entry:
                kelvin = research_entry.get("recommended_color_temp")
                if isinstance(kelvin, (int, float)) and kelvin > 0:
                    if apply_mode_color == 'GUIDED_STRICT':
                        color = lumi_kelvin_to_rgb(float(kelvin))
                    else:
                        # Check if base color is near white; only then override
                        try:
                            r, g, b = base_color
                            if (
                                abs(r - 1.0) < 1e-3 and
                                abs(g - 1.0) < 1e-3 and
                                abs(b - 1.0) < 1e-3
                            ):
                                color = lumi_kelvin_to_rgb(float(kelvin))
                        except Exception:
                            # If base_color is malformed, fall back to kelvin color
                            color = lumi_kelvin_to_rgb(float(kelvin))

        light_data.color = color

        if light_type == 'AREA':
            size = properties.get('size', 1.0) * self.size_multiplier
            light_data.size = size
            light_data.shape = properties.get('shape', 'SQUARE')
            # Set size_y for RECTANGLE and ELLIPSE
            if light_data.shape in ['RECTANGLE', 'ELLIPSE']:
                size_y = properties.get('size_y', size) * self.size_multiplier
                light_data.size_y = size_y
        elif light_type == 'SPOT':
            light_data.spot_size = properties.get('spot_size', 0.785398)  # 45 deg
            light_data.spot_blend = properties.get('spot_blend', 0.15)
        elif light_type == 'SUN':
            light_data.angle = properties.get('angle', 0.53)  # Default sun angle

        # Create object
        light_obj = bpy.data.objects.new(light_name, light_data)
        light_obj.location = pos_data['position']

        # Orient to target
        direction = (pos_data['target'] - pos_data['position']).normalized()
        light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

        # Set pivot based on rotation method
        rotation_config = light_template.get('rotation', {})
        rotation_method = rotation_config.get('method', 'target')  # Default to target

        if rotation_method == 'euler':
            # Euler rotation: Set pivot 3 meters in front of light in facing direction
            pivot_position = pos_data['position'] + direction * 3.0
            lumi_set_light_pivot(light_obj, pivot_position)
        else:
            # Target rotation: Set pivot to target center
            lumi_set_light_pivot(light_obj, pos_data['target'])

        # Link to scene
        context.scene.collection.objects.link(light_obj)

        # Assign light to camera based on current assignment mode
        try:
            from ...core.assign_manager import assign_light_to_active_camera
            assign_light_to_active_camera(light_obj)
        except Exception as e:
            self.report({'WARNING'}, f"Failed to assign light '{light_name}' to camera: {e}")

        return light_obj

    def _organize_lights(self, lights: List, context):
        """Organize lights into collection."""
        collection = lumi_get_light_collection(context.scene)
        if collection:
            for light in lights:
                if light.name not in collection.objects:
                    lumi_move_to_collection(light, collection)

    def _select_lights(self, lights: List, context):
        """Select created lights."""
        bpy.ops.object.select_all(action='DESELECT')
        for light in lights:
            light.select_set(True)
        if lights:
            context.view_layer.objects.active = lights[0]

    def _clear_existing_lights(self, context):
        """Remove existing lights from LumiFlow collection based on assignment mode"""
        try:
            collection = lumi_get_light_collection(context.scene)
            if not collection:
                return

            # Get current assignment mode
            assignment_mode = getattr(context.scene, 'lumi_light_assignment_mode', 'SCENE')
            
            all_lights = [obj for obj in collection.objects if obj.type == 'LIGHT']
            lights_to_remove = []
            
            if assignment_mode == 'SCENE':
                # In SCENE mode, only remove lights with G_ prefix (global lights)
                lights_to_remove = [light for light in all_lights if light.name.startswith('G_')]
            else:  # CAMERA mode
                # In CAMERA mode, only remove lights with C_XX prefix matching active camera
                active_camera = context.scene.camera
                if active_camera:
                    camera_name = active_camera.name
                    
                    # Determine camera prefix
                    if camera_name.endswith('.001'):
                        camera_prefix = 'C_01'
                    elif camera_name.endswith('.002'):
                        camera_prefix = 'C_02'
                    elif camera_name.endswith('.003'):
                        camera_prefix = 'C_03'
                    elif camera_name.endswith('.004'):
                        camera_prefix = 'C_04'
                    elif camera_name.endswith('.005'):
                        camera_prefix = 'C_05'
                    elif camera_name.endswith('.006'):
                        camera_prefix = 'C_06'
                    elif camera_name.endswith('.007'):
                        camera_prefix = 'C_07'
                    elif camera_name.endswith('.008'):
                        camera_prefix = 'C_08'
                    elif camera_name.endswith('.009'):
                        camera_prefix = 'C_09'
                    elif camera_name == 'Camera':
                        camera_prefix = 'C_00'
                    else:
                        # Extract number from camera name or use default
                        import re
                        match = re.search(r'\d+', camera_name)
                        camera_num = match.group(0).zfill(2) if match else '00'
                        camera_prefix = f'C_{camera_num}'
                    
                    # Remove lights with matching camera prefix
                    lights_to_remove = [light for light in all_lights if light.name.startswith(camera_prefix + '_')]
                else:
                    # No active camera, remove all C_00 lights (default)
                    lights_to_remove = [light for light in all_lights if light.name.startswith('C_00_')]
            
            # Remove the filtered lights
            for light_obj in lights_to_remove:
                try:
                    # Remove from collection
                    collection.objects.unlink(light_obj)
                    
                    # Remove from scene if not in other collections
                    if len(light_obj.users_collection) == 0:
                        bpy.data.objects.remove(light_obj, do_unlink=True)
                        
                except Exception as e:
                    pass

        except Exception as e:
            pass


class LUMI_OT_preview_template(bpy.types.Operator):
    bl_idname = "lumi.preview_template"
    bl_label = "Preview Template"
    bl_description = "Preview lighting template with real-time adjustments"
    bl_options = {'REGISTER', 'UNDO'}

    # Template selection
    template_id: StringProperty(
        name="Template ID",
        description="Template to preview",
        default="portrait_rembrandt"
    )

    # Preview state
    _preview_lights = []
    _original_lights = []
    _preview_collection = None
    _intensity_multiplier = 1.0
    _rotation_offset = 0.0
    _current_template_index = 0
    _available_templates = []

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def invoke(self, context, event):
        """Initialize preview mode"""
        try:
            # 1. Create temporary collection for preview lights
            if "LumiFlow_Preview" in bpy.data.collections:
                bpy.data.collections.remove(bpy.data.collections["LumiFlow_Preview"])

            self._preview_collection = bpy.data.collections.new("LumiFlow_Preview")
            context.scene.collection.children.link(self._preview_collection)

            # 2. Store original lights state
            self._original_lights = []
            for obj in context.scene.objects:
                if obj.type == 'LIGHT':
                    self._original_lights.append({
                        'object': obj,
                        'visible': obj.visible_get(),
                        'energy': obj.data.energy if hasattr(obj.data, 'energy') else 1.0
                    })
                    # Dim original lights
                    obj.hide_viewport = True

            # 3. Get available templates for cycling
            self._available_templates = self._get_available_templates()
            if self.template_id in self._available_templates:
                self._current_template_index = self._available_templates.index(self.template_id)
            else:
                self._current_template_index = 0
                if self._available_templates:
                    self.template_id = self._available_templates[0]

            # 4. Create initial preview lights
            if not self.create_preview_lights(context):
                return self.cancel(context)

            # 5. Start modal
            context.window_manager.modal_handler_add(self)

            # Show instructions
            self.report({'INFO'}, "Preview Mode: Scroll=Intensity, R=Rotate, Tab=Next Template, Enter=Apply, Esc=Cancel")

            return {'RUNNING_MODAL'}

        except Exception as e:
            return self.cancel(context)

    def modal(self, context, event):
        """Handle modal interactions"""
        if event.type == 'MOUSEMOVE':
            return {'PASS_THROUGH'}

        # Intensity adjustment with mouse wheel
        if event.type == 'WHEELUPMOUSE':
            self._intensity_multiplier = min(3.0, self._intensity_multiplier * 1.1)
            self.update_preview_intensity(context)
            self.report({'INFO'}, f"Intensity: {self._intensity_multiplier:.2f}")
            return {'RUNNING_MODAL'}

        elif event.type == 'WHEELDOWNMOUSE':
            self._intensity_multiplier = max(0.1, self._intensity_multiplier / 1.1)
            self.update_preview_intensity(context)
            self.report({'INFO'}, f"Intensity: {self._intensity_multiplier:.2f}")
            return {'RUNNING_MODAL'}

        # Rotate setup with R key
        elif event.type == 'R' and event.value == 'PRESS':
            self._rotation_offset += math.radians(15)  # 15 degrees
            self.update_preview_rotation(context)
            self.report({'INFO'}, f"Rotation: {math.degrees(self._rotation_offset):.0f}°")
            return {'RUNNING_MODAL'}

        # Cycle templates with Tab
        elif event.type == 'TAB' and event.value == 'PRESS':
            if self._available_templates:
                self._current_template_index = (self._current_template_index + 1) % len(self._available_templates)
                self.template_id = self._available_templates[self._current_template_index]
                self.recreate_preview_lights(context)
                template = get_template(self.template_id)
                template_name = template.get('name', self.template_id) if template else self.template_id
                self.report({'INFO'}, f"Template: {template_name}")
            return {'RUNNING_MODAL'}

        # Confirm and apply template
        elif event.type in {'LEFTMOUSE', 'RET'} and event.value == 'PRESS':
            return self.confirm_and_apply(context)

        # Cancel preview
        elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            return self.cancel(context)

        return {'PASS_THROUGH'}

    def create_preview_lights(self, context):
        """Create semi-transparent preview lights"""
        try:
            # Clear existing preview lights
            self.cleanup_preview_lights()

            # Get template
            template = get_template(self.template_id)
            if not template:
                return False

            # Analyze subject
            analyzer = SceneAnalyzer(context)
            scene_ctx = analyzer.analyze_scene(context.selected_objects)

            # Calculate positions
            positions = self._calculate_light_positions(scene_ctx, template, context)

            # Create preview lights
            for position_data in positions:
                light_template = position_data['light_template']
                world_pos = position_data['position']
                target_pos = position_data['target']

                # Create light
                light_name = f"Preview_{light_template.get('name', 'Light')}"
                light_type = light_template.get('type', 'AREA')
                properties = light_template.get('properties', {})

                # Create light data with preview characteristics
                light_data = bpy.data.lights.new(name=light_name, type=light_type)
                light_data.energy = properties.get('intensity', 100) * 0.5  # 50% intensity for preview

                # Set preview color (slightly tinted for visibility)
                color = properties.get('color', (1.0, 1.0, 1.0))
                preview_color = (color[0] * 0.8 + 0.2, color[1] * 0.8 + 0.2, color[2] * 0.9 + 0.1)  # Slight cyan tint
                light_data.color = preview_color

                # Configure type-specific properties
                if light_type == 'AREA':
                    shape = properties.get('shape', 'RECTANGLE')
                    light_data.shape = shape if shape in ['RECTANGLE', 'SQUARE', 'DISK', 'ELLIPSE'] else 'RECTANGLE'
                    light_data.size = properties.get('size', 1.0)
                    # Set size_y properly for RECTANGLE and ELLIPSE
                    if light_data.shape in ['RECTANGLE', 'ELLIPSE']:
                        light_data.size_y = properties.get('size_y', light_data.size)
                    else:
                        light_data.size_y = light_data.size

                elif light_type == 'SPOT':
                    light_data.spot_size = math.radians(properties.get('spot_size', 45))
                    light_data.spot_blend = properties.get('spot_blend', 0.2)

                elif light_type == 'SUN':
                    light_data.angle = math.radians(properties.get('angle', 0.5))

                # Create object
                light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
                light_obj.location = world_pos

                # Point light at target
                direction = (target_pos - world_pos).normalized()
                light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

                # Add to preview collection
                self._preview_collection.objects.link(light_obj)
                self._preview_lights.append(light_obj)

                # Automatic camera light assignment for preview lights
                try:
                    from ...core.assign_manager import assign_light_to_active_camera
                    assign_light_to_active_camera(light_obj)
                except Exception:
                    pass

            return True

        except Exception as e:
            return False

    def update_preview_intensity(self, context):
        """Update intensity of all preview lights"""
        for light in self._preview_lights:
            if light.data and hasattr(light.data, 'energy'):
                # Get original intensity from template
                template = get_template(self.template_id)
                if template:
                    for light_template in template.get('lights', []):
                        if light_template.get('name', 'Light') in light.name:
                            base_intensity = light_template.get('properties', {}).get('intensity', 100)
                            light.data.energy = base_intensity * 0.5 * self._intensity_multiplier
                            break

    def update_preview_rotation(self, context):
        """Rotate entire lighting setup around subject"""
        if not context.selected_objects:
            return

        # Get subject center
        subject_center = sum((obj.location for obj in context.selected_objects), Vector()) / len(context.selected_objects)

        # Rotate each light around subject center
        for light in self._preview_lights:
            # Get original position relative to subject
            original_offset = light.location - subject_center

            # Apply rotation
            rotated_offset = original_offset.copy()
            rotated_offset.rotate(Matrix.Rotation(self._rotation_offset, 3, 'Z'))

            # Set new position
            light.location = subject_center + rotated_offset

            # Update light direction to still point at subject
            direction = (subject_center - light.location).normalized()
            light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    def recreate_preview_lights(self, context):
        """Recreate preview lights with new template"""
        self.cleanup_preview_lights()
        self._intensity_multiplier = 1.0
        self._rotation_offset = 0.0
        self.create_preview_lights(context)

    def cleanup_preview_lights(self):
        """Remove all preview lights"""
        for light in self._preview_lights:
            if light.data:
                bpy.data.lights.remove(light.data)
        self._preview_lights.clear()

    def cleanup_preview(self, context):
        """Remove all preview elements"""
        # Remove preview lights
        self.cleanup_preview_lights()

        # Remove preview collection
        if self._preview_collection and self._preview_collection.name in bpy.data.collections:
            bpy.data.collections.remove(self._preview_collection)

        # Restore original lights
        for light_data in self._original_lights:
            light_obj = light_data['object']
            if light_obj:
                light_obj.hide_viewport = not light_data['visible']

        self._preview_collection = None
        self._original_lights.clear()

    def confirm_and_apply(self, context):
        """Apply the current template and exit preview mode"""
        try:
            # Cleanup preview first
            self.cleanup_preview(context)

            # Apply the template using the existing operator
            bpy.ops.lumi.apply_lighting_template(
                template_id=self.template_id,
                intensity_multiplier=self._intensity_multiplier
            )

            self.report({'INFO'}, f"Applied template: {self.template_id}")
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}

    def cancel(self, context):
        """Cancel preview and restore original state"""
        self.cleanup_preview(context)
        self.report({'INFO'}, "Preview cancelled")
        return {'CANCELLED'}

    def _get_available_templates(self):
        """Get list of all available template IDs"""
        try:
            from .template_library import list_templates
            all_templates = list_templates()
            return [template['id'] for template in all_templates]
        except:
            return ['rembrandt', 'butterfly', 'split', 'loop']  # Fallback list

    def _calculate_light_positions(self, scene_ctx, template, context):
        """Calculate light positions using new scene context"""
        positions = []

        # Calculate base distance
        if template.get('settings', {}).get('base_distance'):
            base_distance = template['settings']['base_distance']
        else:
            base_distance = calculate_optimal_distance(scene_ctx.bounds, 2.0, True)

        # Get camera matrix if needed
        camera_matrix = None
        if scene_ctx.camera:
            camera_matrix = scene_ctx.camera.matrix

        # Calculate each light position
        for light_template in template.get('lights', []):
            try:
                position = calculate_position_from_template(
                    light_template,
                    scene_ctx.bounds.center,
                    base_distance,
                    camera_matrix=camera_matrix,
                    use_camera_relative=False
                )

                positions.append({
                    'light_template': light_template,
                    'position': position,
                    'target': scene_ctx.bounds.center
                })
            except Exception as e:
                continue

        return positions


class LUMI_OT_preview_lighting_template(bpy.types.Operator):
    """Preview lighting template without creating lights"""
    bl_idname = "lumi.preview_lighting_template"
    bl_label = "Preview Template"
    bl_description = "Preview lighting template positions"
    bl_options = {'REGISTER'}

    template_id: StringProperty(name="Template ID", default="portrait_rembrandt")

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)

    def execute(self, context):
        try:
            # Get template info
            template = get_template(self.template_id)
            if not template:
                return {'CANCELLED'}

            light_count = len(template.get('lights', []))
            template_name = template.get('name', 'Unknown')
            category = template.get('category', 'unknown')

            self.report({'INFO'}, f"Template: {template_name} ({category}) - {light_count} lights")
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}


class LUMI_OT_save_custom_template(bpy.types.Operator):
    """Save current scene lighting as reusable template"""
    bl_idname = "lumi.save_custom_template"
    bl_label = "Save Custom Template"
    bl_description = "Save current scene lighting setup as a custom template"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties for template metadata
    template_name: StringProperty(
        name="Template Name",
        description="Name for the custom template",
        default="My Template",
        maxlen=64
    )

    template_category: EnumProperty(
        name="Category",
        description="Template category",
        items=[
            ('portrait', "Portrait", "Portrait lighting setup"),
            ('product', "Product", "Product photography lighting"),
            ('fashion', "Fashion", "Fashion photography lighting"),
            ('automotive', "Automotive", "Automotive photography lighting"),
            ('custom', "Custom", "Custom user-defined lighting")
        ],
        default='custom'
    )

    template_description: StringProperty(
        name="Description",
        description="Brief description of the template",
        default="",
        maxlen=256
    )

    include_world: BoolProperty(
        name="Include World Settings",
        description="Include world lighting settings in template",
        default=False
    )

    save_location: EnumProperty(
        name="Save Location",
        description="Where to save the template",
        items=[
            ('user', "User Presets", "Save to user preferences folder"),
            ('project', "Project Folder", "Save to current .blend file directory")
        ],
        default='user'
    )

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                any(obj.type == 'LIGHT' for obj in context.scene.objects))

    def invoke(self, context, event):
        """Show popup dialog for template parameters"""
        # Set default template name based on scene
        if hasattr(context.scene, 'name') and context.scene.name:
            self.template_name = f"{context.scene.name}_lighting"

        # Show dialog
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        """Draw the popup dialog"""
        layout = self.layout

        # Template info
        col = layout.column()
        col.label(text="Template Information:", icon='INFO')
        col.prop(self, "template_name")
        col.prop(self, "template_category")
        col.prop(self, "template_description")

        col.separator()

        # Options
        col.label(text="Options:", icon='PREFERENCES')
        col.prop(self, "include_world")
        col.prop(self, "save_location")

        # Info
        lights_count = len([obj for obj in context.scene.objects if obj.type == 'LIGHT'])
        col.separator()
        col.label(text=f"Lights to save: {lights_count}", icon='LIGHT')

    def execute(self, context):
        """Execute the template saving"""
        try:
            # 1. Validate template name
            if not self.template_name.strip():
                self.report({'ERROR'}, "Template name cannot be empty")
                return {'CANCELLED'}

            # 2. Get all lights in scene
            lights = self.get_scene_lights(context)
            if not lights:
                self.report({'ERROR'}, "No lights found in scene to save")
                return {'CANCELLED'}

            # 3. Convert to relative template format
            template_data = self.convert_to_template(lights, context)

            # 4. Add metadata
            import datetime
            template_data.update({
                "id": self.generate_template_id(),
                "name": self.template_name,
                "category": self.template_category,
                "description": self.template_description,
                "author": getattr(context.preferences.system, 'author', 'Unknown'),
                "date": datetime.datetime.now().isoformat(),
                "blender_version": bpy.app.version_string,
                "lumiflow_version": "1.0.0",
                "settings": {
                    "base_distance": 2.0,
                    "auto_scale": True,
                    "preserve_existing": False
                }
            })

            # 5. Include world settings if requested
            if self.include_world and context.scene.world:
                template_data["world"] = self.get_world_settings(context.scene.world)

            # 6. Save to file
            saved_path = self.save_template_to_file(template_data)

            self.report({'INFO'}, f"Template saved: {self.template_name} ({saved_path})")
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}

    def get_scene_lights(self, context):
        """Get all lights in LumiFlow collection and scene"""
        lights = []

        # Get lights from LumiFlow collection
        collection = lumi_get_light_collection(context.scene)

        if collection:
            for obj in collection.objects:
                if obj.type == 'LIGHT':
                    lights.append(obj)
        else:
            # Fallback: get all lights in scene
            for obj in context.scene.objects:
                if obj.type == 'LIGHT':
                    lights.append(obj)

        return lights

    def convert_to_template(self, lights, context):
        """Convert absolute light positions to relative template format"""
        # Calculate subject center for relative positioning
        subject_center = Vector((0, 0, 0))
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if selected_objects:
            # Use selected objects as subject reference
            total_pos = sum((obj.location for obj in selected_objects), Vector())
            subject_center = total_pos / len(selected_objects)

        # Calculate reference distance (largest dimension of all lights)
        all_positions = [light.location for light in lights]
        if all_positions:
            min_pos = Vector((min(pos.x for pos in all_positions),
                            min(pos.y for pos in all_positions),
                            min(pos.z for pos in all_positions)))
            max_pos = Vector((max(pos.x for pos in all_positions),
                            max(pos.y for pos in all_positions),
                            max(pos.z for pos in all_positions)))
            reference_distance = (max_pos - min_pos).length / 2
        else:
            reference_distance = 2.0

        # Convert each light to template format
        template_lights = []
        for light in lights:
            # Calculate relative position
            relative_pos = light.location - subject_center
            distance = relative_pos.length

            # Convert to spherical coordinates
            if distance > 0.001:  # Avoid division by zero
                azimuth = math.degrees(math.atan2(relative_pos.y, relative_pos.x))
                elevation = math.degrees(math.asin(relative_pos.z / distance))
            else:
                azimuth = 0
                elevation = 0

            # Get light properties
            light_data = {
                "name": light.name,
                "type": light.data.type,
                "position": {
                    "method": "spherical",
                    "params": {
                        "azimuth": azimuth,
                        "elevation": elevation,
                        "distance": distance / reference_distance if reference_distance > 0 else 1.0
                    }
                },
                "rotation": {
                    "target": "subject",
                    "offset": tuple(light.rotation_euler)
                },
                "properties": {
                    "intensity": getattr(light.data, 'energy', 100),
                    "color": tuple(getattr(light.data, 'color', (1, 1, 1))),
                    "size": getattr(light.data, 'size', 1.0) if hasattr(light.data, 'size') else 1.0
                }
            }

            # Add type-specific properties
            if light.data.type == 'AREA':
                light_data["properties"]["shape"] = light.data.shape
                if hasattr(light.data, 'size_y'):
                    light_data["properties"]["size_y"] = light.data.size_y
            elif light.data.type == 'SPOT':
                light_data["properties"]["spot_size"] = math.degrees(light.data.spot_size)
                light_data["properties"]["spot_blend"] = light.data.spot_blend
            elif light.data.type == 'SUN':
                light_data["properties"]["angle"] = math.degrees(light.data.angle)

            template_lights.append(light_data)

        return {
            "lights": template_lights,
            "reference_distance": reference_distance,
            "subject_center": tuple(subject_center)
        }

    def get_world_settings(self, world):
        """Extract world lighting settings"""
        world_data = {
            "strength": 1.0,
            "color": (1, 1, 1)
        }

        if world.use_nodes and world.node_tree:
            # Find world output and background shader
            for node in world.node_tree.nodes:
                if node.type == 'BACKGROUND':
                    world_data["strength"] = node.inputs['Strength'].default_value
                    color_input = node.inputs['Color'].default_value
                    world_data["color"] = tuple(color_input[:3])
                    break

        return world_data

    def generate_template_id(self):
        """Generate unique template ID"""
        import re
        import time

        # Clean template name for ID
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', self.template_name.lower())
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')

        # Add timestamp for uniqueness
        timestamp = str(int(time.time()))[-6:]  # Last 6 digits

        return f"{self.template_category}_{clean_name}_{timestamp}"

    def save_template_to_file(self, template_data):
        """Save template as JSON file"""
        import json
        import os

        # Determine save path
        if self.save_location == 'user':
            # User presets folder
            import bpy.utils
            presets_path = bpy.utils.user_resource('SCRIPTS', path="presets")
            save_dir = os.path.join(presets_path, "lumiflow_templates")
        else:
            # Project folder
            if bpy.data.filepath:
                blend_dir = os.path.dirname(bpy.data.filepath)
                save_dir = os.path.join(blend_dir, "lumiflow_templates")
            else:
                # Fallback to temp directory
                import tempfile
                save_dir = os.path.join(tempfile.gettempdir(), "lumiflow_templates")

        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', self.template_name)
        filename = f"{safe_name}.json"
        filepath = os.path.join(save_dir, filename)

        # Handle existing files
        counter = 1
        base_filepath = filepath
        while os.path.exists(filepath):
            name_part, ext = os.path.splitext(base_filepath)
            filepath = f"{name_part}_{counter}{ext}"
            counter += 1

        # Save JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)

        return filepath

    @staticmethod
    def load_custom_templates():
        """Load all custom templates from user folders"""
        import json
        import os
        import bpy.utils

        templates = []

        # Check user presets folder
        presets_path = bpy.utils.user_resource('SCRIPTS', path="presets")
        if presets_path:
            templates_dir = os.path.join(presets_path, "lumiflow_templates")
            if os.path.exists(templates_dir):
                templates.extend(LUMI_OT_save_custom_template._load_templates_from_dir(templates_dir))

        # Check project folder if blend file is saved
        if bpy.data.filepath:
            blend_dir = os.path.dirname(bpy.data.filepath)
            project_templates_dir = os.path.join(blend_dir, "lumiflow_templates")
            if os.path.exists(project_templates_dir):
                templates.extend(LUMI_OT_save_custom_template._load_templates_from_dir(project_templates_dir))

        return templates

    @staticmethod
    def _load_templates_from_dir(directory):
        """Load templates from a specific directory"""
        import json
        import os

        templates = []

        try:
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)
                            template_data['_filepath'] = filepath  # Store file path for management
                            templates.append(template_data)
                    except (json.JSONDecodeError, IOError) as e:
                        pass
        except OSError:
            pass

        return templates


class LUMI_OT_manage_custom_templates(bpy.types.Operator):
    """Manage custom templates (delete, export, etc.)"""
    bl_idname = "lumi.manage_custom_templates"
    bl_label = "Manage Custom Templates"
    bl_description = "Manage custom lighting templates"
    bl_options = {'REGISTER'}

    action: EnumProperty(
        name="Action",
        description="Action to perform",
        items=[
            ('list', "List", "List all custom templates"),
            ('delete', "Delete", "Delete a template"),
            ('export', "Export", "Export template to file"),
            ('import', "Import", "Import template from file")
        ],
        default='list'
    )

    template_to_delete: StringProperty(
        name="Template to Delete",
        description="Path to template file to delete"
    )

    def execute(self, context):
        """Execute template management action"""
        try:
            if self.action == 'list':
                templates = LUMI_OT_save_custom_template.load_custom_templates()
                if templates:
                    template_names = [t.get('name', 'Unknown') for t in templates]
                    self.report({'INFO'}, f"Found {len(templates)} custom templates: {', '.join(template_names)}")
                else:
                    self.report({'INFO'}, "No custom templates found")

            elif self.action == 'delete' and self.template_to_delete:
                if self.delete_template(self.template_to_delete):
                    self.report({'INFO'}, f"Template deleted: {self.template_to_delete}")
                else:
                    self.report({'ERROR'}, f"Failed to delete template: {self.template_to_delete}")

            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}

    def delete_template(self, filepath):
        """Delete a template file"""
        import os
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except OSError:
            pass
        return False


class LUMI_OT_save_lighting_template(bpy.types.Operator):
    """Save current lighting setup as template"""
    bl_idname = "lumi.save_lighting_template"
    bl_label = "Save Template"
    bl_description = "Save current lighting setup as custom template"
    bl_options = {'REGISTER', 'UNDO'}

    template_name: StringProperty(
        name="Template Name",
        description="Name for the new template",
        default="Custom Template"
    )

    template_id: StringProperty(
        name="Template ID",
        description="Unique identifier for template",
        default="custom_template"
    )

    @classmethod
    def poll(cls, context):
        return (lumi_is_addon_enabled() and
                context.mode == 'OBJECT' and
                any(obj.type == 'LIGHT' for obj in context.scene.objects))

    def execute(self, context):
        try:
            # TODO: Implement template saving functionality
            # This would analyze current lights and create template data
            return {'FINISHED'}

        except Exception as e:
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(LUMI_OT_apply_lighting_template)
    bpy.utils.register_class(LUMI_OT_preview_template)
    bpy.utils.register_class(LUMI_OT_preview_lighting_template)
    bpy.utils.register_class(LUMI_OT_save_custom_template)
    bpy.utils.register_class(LUMI_OT_manage_custom_templates)
    bpy.utils.register_class(LUMI_OT_save_lighting_template)


def unregister():
    bpy.utils.unregister_class(LUMI_OT_apply_lighting_template)
    bpy.utils.unregister_class(LUMI_OT_preview_template)
    bpy.utils.unregister_class(LUMI_OT_preview_lighting_template)
    bpy.utils.unregister_class(LUMI_OT_save_custom_template)
    bpy.utils.unregister_class(LUMI_OT_manage_custom_templates)
    bpy.utils.unregister_class(LUMI_OT_save_lighting_template)