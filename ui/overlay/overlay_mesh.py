"""
Mesh Overlay Module
Contains mesh stroke and object outline functions.
"""

import bpy
import bmesh
import gpu
import numpy as np
import random
import colorsys
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from .config import OverlayConfig
import logging

logger = logging.getLogger(__name__)

class OutlineOverlay:
    """Class for managing mesh outline overlays with solid color rendering."""

    def __init__(self):
        self.batch_cache = {}
        self.color_cache = {}  # Cache colors to avoid regeneration every frame
        self.use_cache = True
        self.frame_counter = 0
        self.memory_pool = {}  # Pool for numpy arrays to reduce allocations

        # Zoom-aware optimization settings - adjusted for better quality preservation
        self.zoom_settings = {
            'near_distance': 10.0,   # Objects closer than this get full quality
            'mid_distance': 50.0,    # Objects in mid range get medium quality
            'far_distance': 150.0,   # Objects beyond this get low quality or culled
            'min_screen_size': 0.005, # Minimum screen space size (as fraction) - less aggressive
            'lod_levels': 4,         # Number of LOD levels - increased for more granularity
        }
        self.last_viewport_distance = None

        # Selection-aware settings
        self.selection_settings = {
            'selected_color_multiplier': 1.3,  # Make selected colors more vibrant
            'selected_always_full_quality': True,  # Selected objects always get LOD 0
            'selected_outline_width': 2.0,     # Outline width for selected objects
            'unselected_alpha': 1.0,           # Alpha for unselected objects
            'selected_alpha': 1.0,             # Alpha for selected objects
        }

    def _get_object_batch_key(self, obj):
        """Generate cache key for object batch based on mesh data."""
        if not obj.data:
            return None

        # Include modifiers in cache key for proper invalidation
        modifier_hash = hash(tuple((mod.name, mod.type) for mod in obj.modifiers))
        return (obj.data.as_pointer(), modifier_hash)

    def _calculate_viewport_distance(self, context):
        """Calculate approximate viewport distance from camera/view."""
        try:
            # Get the 3D view region
            region_3d = context.space_data.region_3d
            if region_3d:
                # Use the view distance as a proxy for zoom level
                return region_3d.view_distance
        except Exception as e:
            logger.debug(f"Cannot get viewport distance: {e}")
        return 10.0  # Default fallback distance

    def _calculate_object_screen_size(self, obj, context, viewport_distance):
        """Calculate approximate screen space size of object."""
        try:
            # Get object bounding box
            bbox = obj.bound_box
            if not bbox:
                return 0.0

            # Calculate bounding box size
            bbox_min = Vector(bbox[0])
            bbox_max = Vector(bbox[7])
            size = (bbox_max - bbox_min).length

            # Get distance from camera to object
            camera_pos = context.space_data.region_3d.view_matrix.inverted().translation
            obj_pos = obj.matrix_world.translation
            distance = (obj_pos - camera_pos).length

            # Calculate screen space size (approximate)
            # This is a simplified calculation - in reality it depends on FOV, etc.
            screen_size = size / max(distance, 0.1)

            return screen_size
        except Exception as e:
            logger.debug(f"Cannot calculate object screen size: {e}")
        return 1.0  # Default to visible if calculation fails

    def _get_lod_level(self, distance):
        """Get level of detail based on distance with 4 levels for smoother transitions."""
        settings = self.zoom_settings
        if distance <= settings['near_distance']:
            return 0  # Full quality - all triangles
        elif distance <= settings['mid_distance'] * 0.5:
            return 1  # High quality - 75% triangles
        elif distance <= settings['mid_distance']:
            return 2  # Medium quality - 50% triangles
        elif distance <= settings['far_distance'] * 0.7:
            return 3  # Low quality - 25% triangles
        else:
            return 4  # Very low quality - bounding box

    def _should_cull_object(self, obj, context, viewport_distance):
        """Determine if object should be culled based on zoom level."""
        try:
            # Selected objects are never culled - always visible
            if hasattr(obj, 'select_get') and obj.select_get():
                return False
        except Exception as e:
            logger.debug(f"Cannot check object selection: {e}")

        screen_size = self._calculate_object_screen_size(obj, context, viewport_distance)
        return screen_size < self.zoom_settings['min_screen_size']

    def _get_selection_aware_color(self, obj, base_color):
        """Modify color based on selection state for better visual feedback."""
        try:
            # Check if object is selected
            is_selected = hasattr(obj, 'select_get') and obj.select_get()
            if not is_selected:
                return base_color

            # Make selected objects more vibrant by increasing saturation/lightness
            r, g, b, a = base_color
            multiplier = self.selection_settings['selected_color_multiplier']

            # Ensure RGB values are in valid range
            r = max(0.0, min(1.0, r))
            g = max(0.0, min(1.0, g))
            b = max(0.0, min(1.0, b))

            # Increase saturation and lightness for selected objects
            # Convert RGB to HSL-like adjustment
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            # Boost saturation and lightness for selected objects
            s = min(1.0, s * multiplier)
            l = min(1.0, l * (multiplier * 0.8))  # Slightly less lightness boost

            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (r, g, b, a)
        except Exception as e:
            logger.debug(f"Cannot get selection-aware color: {e}")
        return base_color

    def _get_selection_aware_lod(self, obj, distance):
        """Get LOD level with selection priority override."""
        try:
            # Selected objects always get full quality regardless of distance
            if hasattr(obj, 'select_get') and obj.select_get() and self.selection_settings['selected_always_full_quality']:
                return 0  # Full quality for selected objects
        except Exception as e:
            logger.debug(f"Cannot check object selection for LOD: {e}")

        # Use normal distance-based LOD for unselected objects
        return self._get_lod_level(distance)

    def _get_cached_color(self, obj, alpha=1.0):
        """Get cached color for object, generate if not cached."""
        # Use object's data pointer for consistent color per object
        cache_key = obj.data.as_pointer() if obj.data else hash(obj.name)

        # Return cached color if available
        if cache_key in self.color_cache:
            cached_color = self.color_cache[cache_key]
            return (cached_color[0], cached_color[1], cached_color[2], alpha)

        # Generate new color and cache it
        import random

        # Generate random but consistent values based on seed
        rng = random.Random(cache_key)

        # Generate pastel colors (high lightness, medium-low saturation)
        # Similar to Blender's default random colors
        hue = rng.random()  # 0.0 - 1.0 (full hue range)
        saturation = rng.uniform(0.5, 0.8)  # Medium saturation for vibrant but soft colors
        lightness = rng.uniform(0.55, 0.75)  # High lightness for pastel effect

        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        color_rgb = (r, g, b)

        # Cache the RGB values (without alpha)
        self.color_cache[cache_key] = color_rgb

        return (r, g, b, alpha)  # Alpha = 1.0 = SOLID (no transparency)

    def _get_object_color(self, obj, alpha=1.0):
        """Generate random pastel color for each object (SOLID - no transparency)."""
        # Use cached version for performance
        return self._get_cached_color(obj, alpha)

    def draw_solid_color_overlay(self, context):
        """
        Draw SOLID color overlays with random pastel colors per object.
        Ultra-optimized for performance with zoom-aware culling and LOD.
        Full opacity (no transparency).
        """
        # Calculate viewport distance for zoom-aware optimizations
        viewport_distance = self._calculate_viewport_distance(context)

        # GPU state setup - proper settings for solid overlay rendering
        gpu.state.depth_test_set('LESS_EQUAL')  # Respect depth for proper occlusion
        gpu.state.depth_mask_set(True)  # Write to depth buffer for solid rendering
        gpu.state.blend_set('NONE')  # No blending - solid colors only
        gpu.state.face_culling_set('BACK')  # Cull back faces for performance

        # Get visible mesh objects with zoom-aware filtering
        mesh_objects = []
        for obj in context.visible_objects:
            if obj.type == 'MESH' and obj.visible_get():
                # Apply screen space culling for distant/small objects
                if not self._should_cull_object(obj, context, viewport_distance):
                    mesh_objects.append(obj)

        if not mesh_objects:
            # Reset GPU state
            gpu.state.depth_mask_set(True)
            gpu.state.depth_test_set('NONE')
            gpu.state.face_culling_set('NONE')
            return

        # Use single shader instance for all objects (performance optimization)
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        shader.bind()

        # Separate selected and unselected objects for different rendering
        selected_objects = []
        unselected_objects = []

        for obj in mesh_objects:
            try:
                is_selected = hasattr(obj, 'select_get') and obj.select_get()
                if is_selected:
                    selected_objects.append(obj)
                else:
                    unselected_objects.append(obj)
            except Exception as e:
                logger.debug(f"Cannot check object selection: {e}")
                unselected_objects.append(obj)

        # Render unselected objects first (background)
        for obj in unselected_objects:
            # Get LOD level based on distance
            camera_pos = context.space_data.region_3d.view_matrix.inverted().translation
            obj_pos = obj.matrix_world.translation
            distance = (obj_pos - camera_pos).length
            lod_level = self._get_selection_aware_lod(obj, distance)

            # Create batch with LOD consideration
            batch = self._create_solid_batch_lod(obj, context, lod_level)
            if batch:
                # Get base color and apply selection-aware modifications
                base_color = self._get_cached_color(obj, alpha=self.selection_settings['unselected_alpha'])
                final_color = self._get_selection_aware_color(obj, base_color)

                shader.uniform_float("color", final_color)

                # Apply object transformation and draw
                gpu.matrix.push()
                gpu.matrix.multiply_matrix(obj.matrix_world)
                batch.draw(shader)
                gpu.matrix.pop()

        # Render selected objects last (foreground) for proper depth ordering
        for obj in selected_objects:
            # Selected objects always get full quality
            lod_level = 0  # Force full quality for selected objects

            # Create batch with full quality
            batch = self._create_solid_batch_lod(obj, context, lod_level)
            if batch:
                # Get enhanced color for selected objects
                base_color = self._get_cached_color(obj, alpha=self.selection_settings['selected_alpha'])
                final_color = self._get_selection_aware_color(obj, base_color)

                shader.uniform_float("color", final_color)

                # Apply object transformation and draw
                gpu.matrix.push()
                gpu.matrix.multiply_matrix(obj.matrix_world)
                batch.draw(shader)
                gpu.matrix.pop()

        # Draw outlines for selected objects (after solid rendering for proper depth)
        if selected_objects:
            self._draw_selected_object_outlines(context, selected_objects)

        # Reset GPU state properly
        gpu.state.depth_mask_set(True)
        gpu.state.depth_test_set('NONE')
        gpu.state.face_culling_set('NONE')

        # Periodic cache cleanup (every 100 frames)
        self.frame_counter += 1
        if self.frame_counter % 100 == 0:
            self._cleanup_cache()

    def _get_pooled_array(self, size, dtype):
        """Get numpy array from memory pool or create new one."""
        pool_key = (size, dtype)
        if pool_key in self.memory_pool and len(self.memory_pool[pool_key]) > 0:
            return self.memory_pool[pool_key].pop()
        return np.empty(size, dtype=dtype)

    def _return_to_pool(self, array):
        """Return numpy array to memory pool for reuse."""
        if array is not None:
            pool_key = (array.size, array.dtype)
            if pool_key not in self.memory_pool:
                self.memory_pool[pool_key] = []
            # Keep pool size reasonable (max 10 arrays per type)
            if len(self.memory_pool[pool_key]) < 10:
                self.memory_pool[pool_key].append(array)

    def _create_solid_batch(self, obj, context):
        """
        Create optimized GPU batch for solid rendering.
        Uses triangle mesh with proper caching and memory pooling for maximum performance.
        Compatible with Blender 4.2+.
        """
        # Generate cache key
        cache_key = self._get_object_batch_key(obj)
        solid_cache_key = (cache_key, "solid_v4")  # v4 for ultra-optimized version

        # Return cached batch if available
        if self.use_cache and solid_cache_key in self.batch_cache:
            return self.batch_cache[solid_cache_key]

        # Get evaluated mesh (with modifiers applied)
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.data

        if not mesh or not mesh.polygons:
            eval_obj.to_mesh_clear()
            return None

        # Fast vertex extraction using pooled numpy arrays
        vert_count = len(mesh.vertices)
        verts = self._get_pooled_array(vert_count * 3, np.float32)
        verts = verts[:vert_count * 3]  # Resize if needed
        mesh.vertices.foreach_get('co', verts)
        verts = verts.reshape(-1, 3)

        # Fast triangle extraction with pre-calculation
        tri_count = sum(len(poly.vertices) - 2 for poly in mesh.polygons if len(poly.vertices) >= 3)

        if tri_count == 0:
            self._return_to_pool(verts)
            eval_obj.to_mesh_clear()
            return None

        triangles = self._get_pooled_array(tri_count * 3, np.int32)
        triangles = triangles[:tri_count * 3]  # Resize if needed

        idx = 0
        for poly in mesh.polygons:
            poly_verts = poly.vertices
            vert_count = len(poly_verts)

            if vert_count < 3:
                continue

            # Triangle fan triangulation (fastest method)
            for i in range(1, vert_count - 1):
                triangles[idx] = poly_verts[0]
                triangles[idx + 1] = poly_verts[i]
                triangles[idx + 2] = poly_verts[i + 1]
                idx += 3

        if idx == 0:
            self._return_to_pool(verts)
            self._return_to_pool(triangles)
            eval_obj.to_mesh_clear()
            return None

        # Trim arrays to actual size used
        triangles = triangles[:idx]

        # Create GPU batch with optimized settings
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'TRIS',
            {"pos": verts},
            indices=triangles
        )

        # Cache the batch for future use
        if self.use_cache:
            self.batch_cache[solid_cache_key] = batch

        # Return arrays to pool for reuse
        self._return_to_pool(verts)
        self._return_to_pool(triangles)

        eval_obj.to_mesh_clear()
        return batch

    def _create_solid_batch_lod(self, obj, context, lod_level):
        """
        Create GPU batch with Level of Detail consideration.
        LOD 0: Full quality (all triangles - 100%)
        LOD 1: High quality (75% triangles)
        LOD 2: Medium quality (50% triangles)
        LOD 3: Low quality (25% triangles)
        LOD 4: Very low quality (bounding box approximation)
        """
        # For LOD 0, use full quality
        if lod_level == 0:
            return self._create_solid_batch(obj, context)

        # Generate LOD-specific cache key
        cache_key = self._get_object_batch_key(obj)
        lod_cache_key = (cache_key, f"solid_lod_{lod_level}")

        # Return cached LOD batch if available
        if self.use_cache and lod_cache_key in self.batch_cache:
            return self.batch_cache[lod_cache_key]

        # Get evaluated mesh (with modifiers applied)
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.data

        if not mesh or not mesh.polygons:
            eval_obj.to_mesh_clear()
            return None

        if lod_level == 1:
            # High quality: 75% triangles (every 4th triangle removed)
            return self._create_high_lod_batch(mesh, lod_cache_key, eval_obj)
        elif lod_level == 2:
            # Medium quality: 50% triangles (every other triangle)
            return self._create_medium_lod_batch(mesh, lod_cache_key, eval_obj)
        elif lod_level == 3:
            # Low quality: 25% triangles (aggressive reduction)
            return self._create_low_detail_lod_batch(mesh, lod_cache_key, eval_obj)
        elif lod_level >= 4:
            # Very low quality: Use bounding box approximation
            return self._create_low_lod_batch(obj, lod_cache_key, eval_obj)

        # Fallback to full quality
        eval_obj.to_mesh_clear()
        return self._create_solid_batch(obj, context)

    def _create_high_lod_batch(self, mesh, cache_key, eval_obj):
        """Create high quality LOD batch (75% triangles - minimal reduction)."""
        # Fast vertex extraction using pooled numpy arrays
        vert_count = len(mesh.vertices)
        verts = self._get_pooled_array(vert_count * 3, np.float32)
        verts = verts[:vert_count * 3]
        mesh.vertices.foreach_get('co', verts)
        verts = verts.reshape(-1, 3)

        # Calculate triangles with 25% reduction (keep 75%)
        full_tri_count = sum(len(poly.vertices) - 2 for poly in mesh.polygons if len(poly.vertices) >= 3)
        tri_count = int(full_tri_count * 0.75)  # 75% of triangles

        if tri_count == 0:
            self._return_to_pool(verts)
            eval_obj.to_mesh_clear()
            return None

        triangles = self._get_pooled_array(tri_count * 3, np.int32)
        triangles = triangles[:tri_count * 3]

        idx = 0
        tri_idx = 0
        for poly in mesh.polygons:
            poly_verts = poly.vertices
            vert_count = len(poly_verts)

            if vert_count < 3:
                continue

            # Triangle fan triangulation with 25% reduction
            for i in range(1, vert_count - 1):
                if tri_idx % 4 != 3:  # Skip every 4th triangle (25% reduction)
                    triangles[idx] = poly_verts[0]
                    triangles[idx + 1] = poly_verts[i]
                    triangles[idx + 2] = poly_verts[i + 1]
                    idx += 3
                tri_idx += 1

        if idx == 0:
            self._return_to_pool(verts)
            self._return_to_pool(triangles)
            eval_obj.to_mesh_clear()
            return None

        # Trim arrays
        triangles = triangles[:idx]

        # Create GPU batch
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'TRIS',
            {"pos": verts},
            indices=triangles
        )

        # Cache the batch
        if self.use_cache:
            self.batch_cache[cache_key] = batch

        # Return arrays to pool
        self._return_to_pool(verts)
        self._return_to_pool(triangles)

        eval_obj.to_mesh_clear()
        return batch

    def _create_low_detail_lod_batch(self, mesh, cache_key, eval_obj):
        """Create low detail LOD batch (25% triangles - aggressive reduction)."""
        # Fast vertex extraction using pooled numpy arrays
        vert_count = len(mesh.vertices)
        verts = self._get_pooled_array(vert_count * 3, np.float32)
        verts = verts[:vert_count * 3]
        mesh.vertices.foreach_get('co', verts)
        verts = verts.reshape(-1, 3)

        # Calculate triangles with 75% reduction (keep 25%)
        full_tri_count = sum(len(poly.vertices) - 2 for poly in mesh.polygons if len(poly.vertices) >= 3)
        tri_count = full_tri_count // 4  # 25% of triangles

        if tri_count == 0:
            self._return_to_pool(verts)
            eval_obj.to_mesh_clear()
            return None

        triangles = self._get_pooled_array(tri_count * 3, np.int32)
        triangles = triangles[:tri_count * 3]

        idx = 0
        tri_idx = 0
        for poly in mesh.polygons:
            poly_verts = poly.vertices
            vert_count = len(poly_verts)

            if vert_count < 3:
                continue

            # Triangle fan triangulation with 75% reduction
            for i in range(1, vert_count - 1):
                if tri_idx % 4 == 0:  # Keep only every 4th triangle (25% retention)
                    triangles[idx] = poly_verts[0]
                    triangles[idx + 1] = poly_verts[i]
                    triangles[idx + 2] = poly_verts[i + 1]
                    idx += 3
                tri_idx += 1

        if idx == 0:
            self._return_to_pool(verts)
            self._return_to_pool(triangles)
            eval_obj.to_mesh_clear()
            return None

        # Trim arrays
        triangles = triangles[:idx]

        # Create GPU batch
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'TRIS',
            {"pos": verts},
            indices=triangles
        )

        # Cache the batch
        if self.use_cache:
            self.batch_cache[cache_key] = batch

        # Return arrays to pool
        self._return_to_pool(verts)
        self._return_to_pool(triangles)

        eval_obj.to_mesh_clear()
        return batch

    def _create_medium_lod_batch(self, mesh, cache_key, eval_obj):
        """Create medium quality LOD batch (50% triangles)."""
        # Fast vertex extraction using pooled numpy arrays
        vert_count = len(mesh.vertices)
        verts = self._get_pooled_array(vert_count * 3, np.float32)
        verts = verts[:vert_count * 3]
        mesh.vertices.foreach_get('co', verts)
        verts = verts.reshape(-1, 3)

        # Calculate triangles with 50% reduction
        full_tri_count = sum(len(poly.vertices) - 2 for poly in mesh.polygons if len(poly.vertices) >= 3)
        tri_count = full_tri_count // 2  # 50% reduction

        if tri_count == 0:
            self._return_to_pool(verts)
            eval_obj.to_mesh_clear()
            return None

        triangles = self._get_pooled_array(tri_count * 3, np.int32)
        triangles = triangles[:tri_count * 3]

        idx = 0
        tri_idx = 0
        for poly in mesh.polygons:
            poly_verts = poly.vertices
            vert_count = len(poly_verts)

            if vert_count < 3:
                continue

            # Triangle fan triangulation with 50% reduction
            for i in range(1, vert_count - 1):
                if tri_idx % 2 == 0:  # Keep every other triangle
                    triangles[idx] = poly_verts[0]
                    triangles[idx + 1] = poly_verts[i]
                    triangles[idx + 2] = poly_verts[i + 1]
                    idx += 3
                tri_idx += 1

        if idx == 0:
            self._return_to_pool(verts)
            self._return_to_pool(triangles)
            eval_obj.to_mesh_clear()
            return None

        # Trim arrays
        triangles = triangles[:idx]

        # Create GPU batch
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'TRIS',
            {"pos": verts},
            indices=triangles
        )

        # Cache the batch
        if self.use_cache:
            self.batch_cache[cache_key] = batch

        # Return arrays to pool
        self._return_to_pool(verts)
        self._return_to_pool(triangles)

        eval_obj.to_mesh_clear()
        return batch

    def _create_low_lod_batch(self, obj, cache_key, eval_obj):
        """Create low quality LOD batch (bounding box approximation)."""
        # Get bounding box
        bbox = obj.bound_box
        if not bbox:
            eval_obj.to_mesh_clear()
            return None

        # Create simple cube vertices from bounding box
        bbox_verts = np.array([
            [bbox[0][0], bbox[0][1], bbox[0][2]],  # 0: ---
            [bbox[1][0], bbox[1][1], bbox[1][2]],  # 1: +--
            [bbox[2][0], bbox[2][1], bbox[2][2]],  # 2: -+-
            [bbox[3][0], bbox[3][1], bbox[3][2]],  # 3: ++-
            [bbox[4][0], bbox[4][1], bbox[4][2]],  # 4: --+
            [bbox[5][0], bbox[5][1], bbox[5][2]],  # 5: +-+
            [bbox[6][0], bbox[6][1], bbox[6][2]],  # 6: -++
            [bbox[7][0], bbox[7][1], bbox[7][2]],  # 7: +++
        ], dtype=np.float32)

        # Simple cube triangles (12 triangles for a cube)
        bbox_triangles = np.array([
            0, 1, 2,    1, 3, 2,  # Bottom face
            4, 6, 5,    5, 6, 7,  # Top face
            0, 2, 4,    2, 6, 4,  # Front face
            1, 5, 3,    5, 7, 3,  # Back face
            0, 4, 1,    1, 4, 5,  # Left face
            2, 3, 6,    3, 7, 6,  # Right face
        ], dtype=np.int32)

        # Create GPU batch
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'TRIS',
            {"pos": bbox_verts},
            indices=bbox_triangles
        )

        # Cache the batch
        if self.use_cache:
            self.batch_cache[cache_key] = batch

        eval_obj.to_mesh_clear()
        return batch

    def _draw_selected_object_outlines(self, context, selected_objects):
        """Draw outline/wireframe overlays for selected objects."""
        if not selected_objects:
            return

        # Set up outline rendering state
        gpu.state.depth_test_set('LESS_EQUAL')
        gpu.state.depth_mask_set(False)  # Don't write to depth for outlines
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(self.selection_settings['selected_outline_width'])

        # Use line shader for outlines
        outline_shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        outline_shader.bind()

        # Outline color (bright contrasting color)
        outline_color = (1.0, 1.0, 0.0, 0.8)  # Bright yellow outline
        outline_shader.uniform_float("color", outline_color)

        for obj in selected_objects:
            # Create wireframe batch for outline
            wire_batch = self._create_wireframe_batch(obj, context)
            if wire_batch:
                gpu.matrix.push()
                gpu.matrix.multiply_matrix(obj.matrix_world)
                wire_batch.draw(outline_shader)
                gpu.matrix.pop()

        # Reset line width
        gpu.state.line_width_set(1.0)
        gpu.state.depth_mask_set(True)
        gpu.state.blend_set('NONE')

    def _create_wireframe_batch(self, obj, context):
        """Create wireframe batch for outline rendering."""
        # Generate cache key for wireframe
        cache_key = self._get_object_batch_key(obj)
        wire_cache_key = (cache_key, "wireframe")

        # Return cached wireframe batch if available
        if self.use_cache and wire_cache_key in self.batch_cache:
            return self.batch_cache[wire_cache_key]

        # Get evaluated mesh
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.data

        if not mesh or not mesh.edges:
            eval_obj.to_mesh_clear()
            return None

        # Extract edge vertices
        edges = mesh.edges
        vertices = mesh.vertices

        # Create vertex array for edges
        edge_verts = []
        edge_indices = []

        for i, edge in enumerate(edges):
            v1_idx, v2_idx = edge.vertices
            v1 = vertices[v1_idx]
            v2 = vertices[v2_idx]

            edge_verts.extend([v1.co.x, v1.co.y, v1.co.z])
            edge_verts.extend([v2.co.x, v2.co.y, v2.co.z])

            edge_indices.extend([i * 2, i * 2 + 1])

        if not edge_verts:
            eval_obj.to_mesh_clear()
            return None

        # Create GPU batch for lines
        import numpy as np
        verts_array = np.array(edge_verts, dtype=np.float32).reshape(-1, 3)
        indices_array = np.array(edge_indices, dtype=np.int32)

        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
            shader, 'LINES',
            {"pos": verts_array},
            indices=indices_array
        )

        # Cache the batch
        if self.use_cache:
            self.batch_cache[wire_cache_key] = batch

        eval_obj.to_mesh_clear()
        return batch

    def draw_outline_stencil_method(self, context):
        """Placeholder for stencil outline method - not implemented in this version."""
        pass

    def _cleanup_cache(self):
        """Periodic cache cleanup to prevent memory leaks."""
        # Limit color cache size (keep most recently used)
        max_color_cache = 1000
        if len(self.color_cache) > max_color_cache:
            # Remove oldest entries (simple FIFO)
            items_to_remove = len(self.color_cache) - max_color_cache
            keys_to_remove = list(self.color_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.color_cache[key]

        # Limit batch cache size
        max_batch_cache = 500
        if len(self.batch_cache) > max_batch_cache:
            # Remove oldest entries
            keys_to_remove = list(self.batch_cache.keys())[:len(self.batch_cache) - max_batch_cache]
            for key in keys_to_remove:
                del self.batch_cache[key]

        # Clean up memory pool (remove unused arrays)
        for pool_key in list(self.memory_pool.keys()):
            pool = self.memory_pool[pool_key]
            # Keep only the 5 most recent arrays per type
            if len(pool) > 5:
                self.memory_pool[pool_key] = pool[-5:]


# Global overlay instance
_overlay_instance = None

def get_outline_overlay():
    """Get or create global outline overlay instance."""
    global _overlay_instance
    if _overlay_instance is None:
        _overlay_instance = OutlineOverlay()
    return _overlay_instance

def _validate_world_shader_darkness(context):
    """
    Validate if world shader has dark background color with strength below 0.3.
    Returns True if world background is dark enough to need overlay assistance.
    """
    try:
        world = context.scene.world
        if not world or not world.use_nodes:
            # No world or nodes - consider it dark
            return True
        
        # Get world node tree
        node_tree = world.node_tree
        if not node_tree:
            return True
        
        # Find Background shader node
        background_node = None
        for node in node_tree.nodes:
            if node.type == 'BACKGROUND':
                background_node = node
                break
        
        if not background_node:
            # No background node found - consider it dark
            return True
        
        # Get background color and strength
        bg_color = background_node.inputs['Color'].default_value
        bg_strength = background_node.inputs['Strength'].default_value
        
        # Calculate luminance (perceived brightness) from RGB
        # Using standard luminance formula: 0.299*R + 0.587*G + 0.114*B
        luminance = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]
        
        # Check if background is dark (low luminance) AND low strength
        # Dark threshold: luminance < 0.2 (20% brightness)
        # Strength threshold: < 0.3 (30% strength)
        is_dark_color = luminance < 0.05
        is_low_strength = bg_strength < 0.2
        
        # Return True if EITHER condition is met (dark color OR low strength)
        # This ensures overlay is shown when lighting is insufficient
        return is_dark_color or is_low_strength
        
    except Exception as e:
        logger.debug(f"Cannot validate world shader darkness: {e}")
        # On error, assume it's dark to be safe
        return True

def _draw_scene_object_strokes_if_no_lights():
    """
    Draw scene object SOLID color overlays when viewport shading is RENDERED and there are no lights.
    Uses efficient GPU-based method with random pastel colors per object (full opacity).
    Compatible with Blender 4.2+.
    
    Now includes validation for dark world shader backgrounds (luminance < 0.2 or strength < 0.3).
    """
    context = bpy.context

    # Only draw in RENDERED viewport shading mode
    if context.space_data.shading.type != 'RENDERED':
        return

    # Only draw when there are no lights in scene
    light_objects = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
    if light_objects:
        return
    
    # Validate world shader - only show overlay if background is dark
    if not _validate_world_shader_darkness(context):
        # World background is bright enough - no need for overlay
        return

    # Get outline method from preferences (with fallback to solid color)
    outline_method = 'SOLID_COLOR'  # Default to solid color
    try:
        addon_prefs = bpy.context.preferences.addons.get(__package__.split('.')[0] or "LumiFlow")
        if addon_prefs and hasattr(addon_prefs.preferences, 'outline_method'):
            outline_method = addon_prefs.preferences.outline_method
    except Exception as e:
        logger.debug(f"Cannot get outline method preference: {e}")

    # Get overlay instance
    overlay = get_outline_overlay()

    # Use appropriate rendering method
    if outline_method == 'SOLID_COLOR':
        # Use optimized solid color overlay (RECOMMENDED - fastest and most compatible)
        overlay.draw_solid_color_overlay(context)
    elif outline_method == 'GPU_OFFSET':
        # Use GPU offset outline method (wireframe style)
        overlay.draw_outline_stencil_method(context)
    else:
        # Fallback to silhouette method (slowest, most accurate)
        _draw_scene_object_strokes_silhouette(context)


def _draw_scene_object_strokes_silhouette(context):
    """Fallback silhouette drawing method - placeholder."""
    pass