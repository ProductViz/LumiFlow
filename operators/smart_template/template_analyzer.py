"""
Template Analyzer Module
Analyze selected objects for intelligent template adaptation.
"""

# Import modul utama Blender
import bpy
import bmesh
from typing import Dict, List, Tuple, Optional, Any
from mathutils import Vector, Matrix
import mathutils
import statistics

class SubjectAnalysis:
    """Enhanced subject analysis result with advanced detection capabilities"""
    def __init__(self):
        self.bounds = {
            "min": Vector(),
            "max": Vector(),
            "center": Vector(),
            "dimensions": Vector(),
            "diagonal": float(0.0),
            "radius": float(0.0)
        }
        self.orientation = {
            "forward": Vector((0, 1, 0)),
            "up": Vector((0, 0, 1)),
            "right": Vector((1, 0, 0)),
            "matrix": Matrix()
        }
        self.materials = {
            "dominant_type": "dielectric",  # "metallic", "dielectric", "glass"
            "has_emission": False,
            "average_roughness": 0.5,
            "transparency": 0.0
        }
        # Enhanced type detection
        self.type = "product"  # Legacy compatibility
        self.subject_classification = {
            "primary_type": "product",
            "subtype": "generic",
            "confidence": 0.5,
            "secondary_types": [],  # For hybrid subjects
            "characteristics": {}
        }
        self.topology_analysis = {
            "vertex_count": 0,
            "face_count": 0,
            "edge_count": 0,
            "topology_score": 0.0,
            "mesh_density": 0.0,
            "surface_complexity": 0.0,
            "proportions": {}
        }
        self.camera_relation = {
            "distance": 5.0,
            "angle": Vector()
        }
        self.object_count = 0
        self.complexity_score = 0.0


# ===== ADVANCED SUBJECT CLASSIFICATION SYSTEM =====

class AdvancedSubjectClassifier:
    """AI-inspired subject classification with 20+ types and subtypes"""
    
    # Subject type definitions with characteristics
    SUBJECT_TYPES = {
        # HUMAN SUBJECTS
        "human_portrait": {
            "subtypes": ["adult", "child", "elderly", "group", "couple", "family"],
            "topology_patterns": {
                "aspect_ratio_range": (0.4, 0.8),  # Height/Width typical for heads
                "vertex_density": (500, 5000),
                "face_smoothness": 0.8,
                "symmetry_score": 0.7
            },
            "material_indicators": ["skin", "hair", "eye", "cloth"],
            "proportion_keys": ["head_to_body", "facial_features", "limb_ratios"]
        },
        "human_full_body": {
            "subtypes": ["standing", "sitting", "action", "dance", "sport"],
            "topology_patterns": {
                "aspect_ratio_range": (0.2, 0.5),  # Full body proportions
                "vertex_density": (1000, 15000),
                "elongation_factor": 2.0,
                "joint_detection": True
            },
            "material_indicators": ["skin", "fabric", "leather", "metal"],
            "proportion_keys": ["golden_ratio", "anatomical_proportions"]
        },
        
        # PRODUCT SUBJECTS
        "jewelry": {
            "subtypes": ["ring", "necklace", "bracelet", "earrings", "watch"],
            "topology_patterns": {
                "aspect_ratio_range": (0.1, 2.0),
                "vertex_density": (200, 2000),
                "surface_complexity": 0.9,
                "reflectivity_score": 0.8
            },
            "material_indicators": ["gold", "silver", "diamond", "gem"],
            "proportion_keys": ["miniature_scale", "precision_details"]
        },
        "electronics": {
            "subtypes": ["smartphone", "laptop", "camera", "headphones", "gaming"],
            "topology_patterns": {
                "aspect_ratio_range": (0.3, 3.0),
                "vertex_density": (500, 8000),
                "geometric_regularity": 0.9,
                "edge_sharpness": 0.8
            },
            "material_indicators": ["plastic", "metal", "glass", "rubber"],
            "proportion_keys": ["functional_design", "tech_aesthetics"]
        },
        "food": {
            "subtypes": ["fruit", "vegetable", "dessert", "beverage", "dish"],
            "topology_patterns": {
                "aspect_ratio_range": (0.5, 2.0),
                "vertex_density": (300, 5000),
                "organic_curves": 0.8,
                "surface_variation": 0.7
            },
            "material_indicators": ["organic", "liquid", "translucent"],
            "proportion_keys": ["natural_forms", "appetizing_angles"]
        },
        "cosmetics": {
            "subtypes": ["bottle", "compact", "tube", "palette", "brush"],
            "topology_patterns": {
                "aspect_ratio_range": (0.3, 4.0),
                "vertex_density": (400, 3000),
                "brand_geometry": 0.8,
                "surface_finish": 0.9
            },
            "material_indicators": ["glass", "plastic", "metal", "luxury"],
            "proportion_keys": ["premium_feel", "ergonomic_design"]
        },
        
        # ARCHITECTURAL SUBJECTS
        "interior": {
            "subtypes": ["living_room", "kitchen", "bedroom", "office", "bathroom"],
            "topology_patterns": {
                "aspect_ratio_range": (0.3, 3.0),
                "vertex_density": (1000, 50000),
                "architectural_lines": 0.9,
                "space_volumes": True
            },
            "material_indicators": ["wood", "concrete", "fabric", "glass"],
            "proportion_keys": ["room_proportions", "furniture_scale"]
        },
        "exterior": {
            "subtypes": ["building", "facade", "street", "plaza", "monument"],
            "topology_patterns": {
                "aspect_ratio_range": (0.2, 5.0),
                "vertex_density": (2000, 100000),
                "structural_elements": 0.8,
                "large_scale": True
            },
            "material_indicators": ["concrete", "stone", "glass", "metal"],
            "proportion_keys": ["architectural_scale", "urban_context"]
        },
        "landscape": {
            "subtypes": ["mountain", "forest", "water", "desert", "garden"],
            "topology_patterns": {
                "aspect_ratio_range": (0.1, 10.0),
                "vertex_density": (1000, 200000),
                "natural_irregularity": 0.9,
                "terrain_features": True
            },
            "material_indicators": ["natural", "organic", "water", "rock"],
            "proportion_keys": ["natural_scale", "horizon_line"]
        },
        
        # NATURE SUBJECTS
        "plant": {
            "subtypes": ["tree", "flower", "bush", "grass", "indoor_plant"],
            "topology_patterns": {
                "aspect_ratio_range": (0.3, 5.0),
                "vertex_density": (500, 20000),
                "organic_branching": 0.9,
                "fractal_patterns": 0.8
            },
            "material_indicators": ["leaf", "bark", "flower", "organic"],
            "proportion_keys": ["natural_growth", "botanical_accuracy"]
        },
        "water": {
            "subtypes": ["ocean", "lake", "river", "waterfall", "pool"],
            "topology_patterns": {
                "aspect_ratio_range": (0.1, 10.0),
                "vertex_density": (200, 50000),
                "fluid_dynamics": 0.9,
                "surface_waves": True
            },
            "material_indicators": ["water", "transparent", "reflective"],
            "proportion_keys": ["water_scale", "flow_patterns"]
        },
        "terrain": {
            "subtypes": ["mountain", "hill", "valley", "cliff", "canyon"],
            "topology_patterns": {
                "aspect_ratio_range": (0.2, 8.0),
                "vertex_density": (1000, 100000),
                "geological_features": 0.8,
                "elevation_changes": True
            },
            "material_indicators": ["rock", "soil", "mineral", "natural"],
            "proportion_keys": ["geological_scale", "erosion_patterns"]
        },
        
        # VEHICLE SUBJECTS
        "automotive": {
            "subtypes": ["car", "motorcycle", "truck", "bus", "racing"],
            "topology_patterns": {
                "aspect_ratio_range": (0.3, 0.7),
                "vertex_density": (2000, 20000),
                "aerodynamic_curves": 0.8,
                "mechanical_precision": 0.9
            },
            "material_indicators": ["metal", "glass", "rubber", "paint"],
            "proportion_keys": ["vehicle_proportions", "automotive_design"]
        },
        
        # ABSTRACT/ARTISTIC
        "abstract": {
            "subtypes": ["geometric", "organic", "conceptual", "sculpture", "art"],
            "topology_patterns": {
                "aspect_ratio_range": (0.1, 10.0),
                "vertex_density": (100, 50000),
                "artistic_freedom": 1.0,
                "creative_geometry": 0.9
            },
            "material_indicators": ["artistic", "mixed", "experimental"],
            "proportion_keys": ["artistic_composition", "creative_balance"]
        }
    }
    
    @classmethod
    def classify_subject(cls, objects: List[bpy.types.Object], analysis: SubjectAnalysis) -> Dict[str, Any]:
        """
        Advanced subject classification using ML-inspired algorithms
        
        Args:
            objects: List of objects to classify
            analysis: Basic analysis data
            
        Returns:
            Classification result with confidence scores
        """
        try:
            # Initialize classification scores
            type_scores = {}
            
            # Analyze each subject type
            for subject_type, type_config in cls.SUBJECT_TYPES.items():
                score = cls._calculate_type_score(objects, analysis, subject_type, type_config)
                type_scores[subject_type] = score
            
            # Apply fuzzy logic for hybrid detection
            primary_type, confidence = cls._apply_fuzzy_logic(type_scores)
            
            # Determine subtype
            subtype = cls._detect_subtype(objects, analysis, primary_type)
            
            # Find secondary types (for hybrid subjects)
            secondary_types = cls._find_secondary_types(type_scores, primary_type, threshold=0.3)
            
            return {
                "primary_type": primary_type,
                "subtype": subtype,
                "confidence": confidence,
                "secondary_types": secondary_types,
                "all_scores": type_scores,
                "characteristics": cls._extract_characteristics(objects, analysis, primary_type)
            }
            
        except Exception as e:
            pass
            return {
                "primary_type": "product",
                "subtype": "generic",
                "confidence": 0.1,
                "secondary_types": [],
                "all_scores": {},
                "characteristics": {}
            }
    
    @classmethod
    def _calculate_type_score(cls, objects, analysis, subject_type, type_config) -> float:
        """Calculate confidence score for a specific subject type"""
        try:
            score = 0.0
            weight_total = 0.0
            
            # Topology analysis (40% weight)
            topology_score = cls._analyze_topology_patterns(objects, analysis, type_config)
            score += topology_score * 0.4
            weight_total += 0.4
            
            # Material analysis (30% weight)
            material_score = cls._analyze_material_indicators(objects, analysis, type_config)
            score += material_score * 0.3
            weight_total += 0.3
            
            # Proportion analysis (20% weight)
            proportion_score = cls._analyze_proportions(objects, analysis, type_config)
            score += proportion_score * 0.2
            weight_total += 0.2
            
            # Context analysis (10% weight)
            context_score = cls._analyze_context(objects, analysis, type_config)
            score += context_score * 0.1
            weight_total += 0.1
            
            return min(1.0, score / weight_total) if weight_total > 0 else 0.0
            
        except Exception as e:
            pass
            return 0.0
    
    @classmethod
    def _analyze_topology_patterns(cls, objects, analysis, type_config) -> float:
        """Analyze mesh topology patterns for classification"""
        try:
            topology_patterns = type_config.get("topology_patterns", {})
            score = 0.0
            checks = 0
            
            # Aspect ratio check
            if "aspect_ratio_range" in topology_patterns:
                min_ratio, max_ratio = topology_patterns["aspect_ratio_range"]
                dims = analysis.bounds["dimensions"]
                if dims.z > 0 and dims.x > 0:
                    actual_ratio = dims.z / max(dims.x, dims.y)
                    if min_ratio <= actual_ratio <= max_ratio:
                        score += 1.0
                    else:
                        # Gradual falloff
                        distance = min(abs(actual_ratio - min_ratio), abs(actual_ratio - max_ratio))
                        score += max(0, 1.0 - distance)
                checks += 1
            
            # Vertex density check
            if "vertex_density" in topology_patterns:
                min_density, max_density = topology_patterns["vertex_density"]
                total_verts = sum(len(obj.data.vertices) for obj in objects if obj.type == 'MESH' and obj.data)
                if min_density <= total_verts <= max_density:
                    score += 1.0
                elif total_verts > 0:
                    # Gradual scoring
                    if total_verts < min_density:
                        score += total_verts / min_density
                    else:
                        score += min(1.0, max_density / total_verts)
                checks += 1
            
            # Surface complexity
            if "surface_complexity" in topology_patterns:
                expected_complexity = topology_patterns["surface_complexity"]
                actual_complexity = analysis.complexity_score
                similarity = 1.0 - abs(expected_complexity - actual_complexity)
                score += max(0, similarity)
                checks += 1
            
            # Geometric regularity
            if "geometric_regularity" in topology_patterns:
                expected_regularity = topology_patterns["geometric_regularity"]
                actual_regularity = cls._calculate_geometric_regularity(objects)
                similarity = 1.0 - abs(expected_regularity - actual_regularity)
                score += max(0, similarity)
                checks += 1
            
            return score / checks if checks > 0 else 0.0
            
        except Exception as e:
            pass
            return 0.0
    
    @classmethod
    def _analyze_material_indicators(cls, objects, analysis, type_config) -> float:
        """Analyze material properties for classification"""
        try:
            material_indicators = type_config.get("material_indicators", [])
            if not material_indicators:
                return 0.5  # Neutral score if no indicators
            
            score = 0.0
            found_materials = []
            
            # Collect material names and properties
            for obj in objects:
                if obj.type == 'MESH' and obj.data and obj.data.materials:
                    for mat in obj.data.materials:
                        if mat and mat.name:
                            found_materials.append(mat.name.lower())
                            
                            # Check material nodes for indicators
                            if mat.use_nodes and mat.node_tree:
                                for node in mat.node_tree.nodes:
                                    if hasattr(node, 'name'):
                                        found_materials.append(node.name.lower())
            
            # Score based on material indicator matches
            matches = 0
            for indicator in material_indicators:
                for material in found_materials:
                    if indicator.lower() in material:
                        matches += 1
                        break
            
            score = matches / len(material_indicators) if material_indicators else 0.5
            
            # Bonus for material type alignment
            dominant_type = analysis.materials.get("dominant_type", "dielectric")
            if dominant_type == "metallic" and any(m in material_indicators for m in ["metal", "gold", "silver"]):
                score += 0.2
            elif dominant_type == "glass" and "glass" in material_indicators:
                score += 0.2
            
            return min(1.0, score)
            
        except Exception as e:
            pass
            return 0.0
    
    @classmethod
    def _analyze_proportions(cls, objects, analysis, type_config) -> float:
        """Analyze geometric proportions for classification"""
        try:
            proportion_keys = type_config.get("proportion_keys", [])
            if not proportion_keys:
                return 0.5
            
            dims = analysis.bounds["dimensions"]
            score = 0.0
            checks = 0
            
            for key in proportion_keys:
                if key == "golden_ratio":
                    # Check for golden ratio in dimensions
                    ratios = [
                        max(dims.x, dims.y) / min(dims.x, dims.y) if min(dims.x, dims.y) > 0 else 0,
                        max(dims.y, dims.z) / min(dims.y, dims.z) if min(dims.y, dims.z) > 0 else 0,
                        max(dims.x, dims.z) / min(dims.x, dims.z) if min(dims.x, dims.z) > 0 else 0
                    ]
                    golden_ratio = 1.618
                    best_match = min(abs(r - golden_ratio) for r in ratios if r > 0)
                    score += max(0, 1.0 - best_match / golden_ratio)
                    checks += 1
                
                elif key == "anatomical_proportions":
                    # Human body proportions (head = 1/8 of body height)
                    if dims.z > dims.x and dims.z > dims.y:  # Vertical object
                        head_ratio = dims.x / dims.z if dims.z > 0 else 0
                        ideal_ratio = 1/8
                        similarity = 1.0 - abs(head_ratio - ideal_ratio) / ideal_ratio
                        score += max(0, similarity)
                    checks += 1
                
                elif key == "miniature_scale":
                    # Small objects (jewelry, etc.)
                    max_dim = max(dims.x, dims.y, dims.z)
                    if max_dim < 0.1:  # Very small
                        score += 1.0
                    elif max_dim < 0.5:  # Small
                        score += 0.7
                    else:
                        score += 0.3
                    checks += 1
                
                elif key == "architectural_scale":
                    # Large scale objects
                    max_dim = max(dims.x, dims.y, dims.z)
                    if max_dim > 10.0:  # Very large
                        score += 1.0
                    elif max_dim > 3.0:  # Large
                        score += 0.7
                    else:
                        score += 0.3
                    checks += 1
            
            return score / checks if checks > 0 else 0.5
            
        except Exception as e:
            pass
            return 0.0
    
    @classmethod
    def _analyze_context(cls, objects, analysis, type_config) -> float:
        """Analyze scene context for classification"""
        try:
            score = 0.5  # Base neutral score
            
            # Object count context
            obj_count = len(objects)
            if "group" in type_config.get("subtypes", []) and obj_count > 3:
                score += 0.3
            elif "single" in type_config.get("subtypes", []) and obj_count == 1:
                score += 0.3
            
            # Complexity context
            complexity = analysis.complexity_score
            if "high_detail" in type_config.get("subtypes", []) and complexity > 0.7:
                score += 0.2
            elif "simple" in type_config.get("subtypes", []) and complexity < 0.3:
                score += 0.2
            
            return min(1.0, score)
            
        except Exception as e:
            pass
            return 0.5
    
    @classmethod
    def _apply_fuzzy_logic(cls, type_scores) -> Tuple[str, float]:
        """Apply fuzzy logic to determine primary type with confidence"""
        try:
            if not type_scores:
                return "product", 0.1
            
            # Sort by score
            sorted_scores = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
            
            if len(sorted_scores) < 2:
                return sorted_scores[0][0], sorted_scores[0][1]
            
            best_type, best_score = sorted_scores[0]
            second_type, second_score = sorted_scores[1]
            
            # Calculate confidence based on score separation
            score_gap = best_score - second_score
            confidence_bonus = min(0.3, score_gap * 0.5)
            final_confidence = min(1.0, best_score + confidence_bonus)
            
            return best_type, final_confidence
            
        except Exception as e:
            pass
            return "product", 0.1
    
    @classmethod
    def _detect_subtype(cls, objects, analysis, primary_type) -> str:
        """Detect specific subtype within primary type"""
        try:
            type_config = cls.SUBJECT_TYPES.get(primary_type, {})
            subtypes = type_config.get("subtypes", ["generic"])
            
            if len(subtypes) <= 1:
                return subtypes[0] if subtypes else "generic"
            
            # Simple subtype detection based on characteristics
            dims = analysis.bounds["dimensions"]
            obj_count = len(objects)
            
            # Human subtypes
            if primary_type in ["human_portrait", "human_full_body"]:
                if obj_count > 2:
                    return "group"
                elif dims.z / max(dims.x, dims.y) > 2.0:
                    return "standing" if primary_type == "human_full_body" else "adult"
                else:
                    return "sitting" if primary_type == "human_full_body" else "adult"
            
            # Product subtypes
            elif primary_type == "jewelry":
                max_dim = max(dims.x, dims.y, dims.z)
                if max_dim < 0.02:
                    return "ring"
                elif dims.z > dims.x and dims.z > dims.y:
                    return "necklace"
                else:
                    return "bracelet"
            
            # Default to first subtype
            return subtypes[0]
            
        except Exception as e:
            pass
            return "generic"
    
    @classmethod
    def _find_secondary_types(cls, type_scores, primary_type, threshold=0.3) -> List[str]:
        """Find secondary types for hybrid subjects"""
        try:
            secondary = []
            for type_name, score in type_scores.items():
                if type_name != primary_type and score >= threshold:
                    secondary.append(type_name)
            
            # Sort by score and limit to top 2
            secondary.sort(key=lambda x: type_scores[x], reverse=True)
            return secondary[:2]
            
        except Exception as e:
            pass
            return []
    
    @classmethod
    def _extract_characteristics(cls, objects, analysis, primary_type) -> Dict[str, Any]:
        """Extract specific characteristics for the detected type"""
        try:
            characteristics = {}
            
            # Basic measurements
            dims = analysis.bounds["dimensions"]
            characteristics["dimensions"] = {
                "width": dims.x,
                "depth": dims.y, 
                "height": dims.z,
                "volume": dims.x * dims.y * dims.z,
                "aspect_ratios": {
                    "w_h": dims.x / dims.z if dims.z > 0 else 1.0,
                    "d_h": dims.y / dims.z if dims.z > 0 else 1.0,
                    "w_d": dims.x / dims.y if dims.y > 0 else 1.0
                }
            }
            
            # Material characteristics
            characteristics["materials"] = analysis.materials
            
            # Complexity characteristics
            total_verts = sum(len(obj.data.vertices) for obj in objects if obj.type == 'MESH' and obj.data)
            total_faces = sum(len(obj.data.polygons) for obj in objects if obj.type == 'MESH' and obj.data)
            
            characteristics["topology"] = {
                "vertex_count": total_verts,
                "face_count": total_faces,
                "density": total_verts / max(1, analysis.bounds["radius"] ** 2),
                "complexity": analysis.complexity_score
            }
            
            return characteristics
            
        except Exception as e:
            pass
            return {}
    
    @classmethod
    def _calculate_geometric_regularity(cls, objects) -> float:
        """Calculate how regular/geometric vs organic the objects are"""
        try:
            if not objects:
                return 0.5
                
            regularity_scores = []
            
            for obj in objects:
                if obj.type != 'MESH' or not obj.data:
                    continue
                    
                mesh = obj.data
                if len(mesh.polygons) == 0:
                    continue
                
                # Check face regularity (quads vs triangles vs ngons)
                quad_count = sum(1 for poly in mesh.polygons if len(poly.vertices) == 4)
                tri_count = sum(1 for poly in mesh.polygons if len(poly.vertices) == 3)
                ngon_count = len(mesh.polygons) - quad_count - tri_count
                
                total_faces = len(mesh.polygons)
                quad_ratio = quad_count / total_faces
                
                # Higher quad ratio = more regular/geometric
                regularity = quad_ratio * 0.8 + (1 - ngon_count / max(1, total_faces)) * 0.2
                regularity_scores.append(regularity)
            
            return statistics.mean(regularity_scores) if regularity_scores else 0.5
            
        except Exception as e:
            return 0.5


def analyze_topology_enhanced(objects: List[bpy.types.Object], analysis: SubjectAnalysis) -> Dict[str, Any]:
    """Enhanced topology analysis for advanced classification"""
    try:
        topology_data = {
            "vertex_count": 0,
            "face_count": 0,
            "edge_count": 0,
            "topology_score": 0.0,
            "mesh_density": 0.0,
            "surface_complexity": 0.0,
            "proportions": {}
        }
        
        total_vertices = 0
        total_faces = 0
        total_edges = 0
        
        for obj in objects:
            if obj.type == 'MESH' and obj.data:
                mesh = obj.data
                total_vertices += len(mesh.vertices)
                total_faces += len(mesh.polygons)
                total_edges += len(mesh.edges)
        
        # Calculate basic counts
        topology_data["vertex_count"] = total_vertices
        topology_data["face_count"] = total_faces
        topology_data["edge_count"] = total_edges
        
        # Calculate mesh density (vertices per unit volume)
        volume = analysis.bounds["dimensions"].x * analysis.bounds["dimensions"].y * analysis.bounds["dimensions"].z
        if volume > 0:
            topology_data["mesh_density"] = total_vertices / volume
        
        # Calculate surface complexity based on face-to-vertex ratio
        if total_vertices > 0:
            complexity_ratio = total_faces / total_vertices
            topology_data["surface_complexity"] = min(1.0, complexity_ratio * 2.0)
        
        # Calculate topology score (overall mesh quality indicator)
        if total_faces > 0 and total_vertices > 0:
            vertex_face_ratio = total_vertices / total_faces
            # Ideal ratio is around 0.5-0.8 for good topology
            ideal_ratio = 0.65
            score = 1.0 - abs(vertex_face_ratio - ideal_ratio) / ideal_ratio
            topology_data["topology_score"] = max(0.0, min(1.0, score))
        
        return topology_data
        
    except Exception as e:
        return {
            "vertex_count": 0,
            "face_count": 0,
            "edge_count": 0,
            "topology_score": 0.0,
            "mesh_density": 0.0,
            "surface_complexity": 0.0,
            "proportions": {}
        }


def analyze_subject(objects: List[bpy.types.Object], context: bpy.types.Context) -> SubjectAnalysis:
    """
    Complete subject analysis.
    
    Args:
        objects: List of objects to analyze
        context: Blender context
        
    Returns:
        SubjectAnalysis object with complete analysis
    """
    # # Coba eksekusi kode dengan error handling
    try:
        analysis = SubjectAnalysis()
        
        if not objects:
            return analysis
        
        # Filter valid mesh objects
        valid_objects = [obj for obj in objects 
                        if obj and obj.type == 'MESH' and obj.data]
        
        if not valid_objects:
            return analysis
        
        analysis.object_count = len(valid_objects)
        
        # Calculate bounds
        bounds_data = calculate_bounds(valid_objects)
        analysis.bounds.update(bounds_data)
        
        # Detect orientation
        orientation_data = detect_orientation(valid_objects)
        analysis.orientation.update(orientation_data)
        
        # Analyze materials
        material_data = analyze_materials(valid_objects)
        analysis.materials.update(material_data)
        
        # Calculate camera relationship
        camera_data = calculate_camera_relation(valid_objects, context)
        analysis.camera_relation.update(camera_data)
        
        # Calculate complexity score
        analysis.complexity_score = calculate_complexity_score(valid_objects)
        
        # Enhanced topology analysis
        analysis.topology_analysis = analyze_topology_enhanced(valid_objects, analysis)
        
        # Advanced subject classification
        classification = AdvancedSubjectClassifier.classify_subject(valid_objects, analysis)
        analysis.subject_classification.update(classification)
        
        # Legacy compatibility
        analysis.type = classification["primary_type"]
        
        return analysis
        
    # # Tangani error jika terjadi
    except Exception as e:
        analysis = SubjectAnalysis()
        analysis.type = "product"  # Safe fallback
        return analysis


def calculate_bounds(objects: List[bpy.types.Object]) -> Dict[str, Any]:
    """
    Calculate combined bounding box for all objects.
    
    Args:
        objects: List of objects to analyze
        
    Returns:
        Dictionary with bounds information
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not objects:
            return {
                "min": Vector(),
                "max": Vector(),
                "center": Vector(),
                "dimensions": Vector((1.0, 1.0, 1.0)),
                "diagonal": 1.0,
                "radius": 0.5
            }
        
        # Initialize bounds with first object
        first_obj = objects[0]
        bbox_corners = [first_obj.matrix_world @ Vector(corner) for corner in first_obj.bound_box]
        
        min_coord = Vector(bbox_corners[0])
        max_coord = Vector(bbox_corners[0])
        
        # Process all objects
        for obj in objects:
            # # Coba eksekusi kode dengan error handling
            try:
                # Get world-space bounding box corners
                world_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                
                for corner in world_corners:
                    # Update min/max for each axis
                    for i in range(3):
                        min_coord[i] = min(min_coord[i], corner[i])
                        max_coord[i] = max(max_coord[i], corner[i])
                        
            # # Tangani error jika terjadi
            except Exception as e:
                continue
        
        # Calculate derived values
        center = (min_coord + max_coord) * 0.5
        dimensions = max_coord - min_coord
        diagonal = dimensions.length
        radius = diagonal * 0.5
        
        return {
            "min": min_coord,
            "max": max_coord,
            "center": center,
            "dimensions": dimensions,
            "diagonal": diagonal,
            "radius": radius
        }
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "min": Vector(),
            "max": Vector(),
            "center": Vector(),
            "dimensions": Vector((1.0, 1.0, 1.0)),
            "diagonal": 1.0,
            "radius": 0.5
        }


def detect_orientation(objects: List[bpy.types.Object]) -> Dict[str, Any]:
    """
    Detect primary orientation from object transforms.
    
    Args:
        objects: List of objects to analyze
        
    Returns:
        Dictionary with orientation data
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not objects:
            return {
                "forward": Vector((0, 1, 0)),
                "up": Vector((0, 0, 1)),
                "right": Vector((1, 0, 0)),
                "matrix": Matrix()
            }
        
        # Collect all object matrices
        matrices = []
        for obj in objects:
            # # Coba eksekusi kode dengan error handling
            try:
                matrices.append(obj.matrix_world.copy())
            # # Tangani error jika terjadi
            except Exception:
                continue
        
        if not matrices:
            return {
                "forward": Vector((0, 1, 0)),
                "up": Vector((0, 0, 1)),
                "right": Vector((1, 0, 0)),
                "matrix": Matrix()
            }
        
        # Average the orientations
        avg_forward = Vector()
        avg_up = Vector()
        avg_right = Vector()
        
        for matrix in matrices:
            # Extract basis vectors (normalized)
            right = matrix.to_3x3() @ Vector((1, 0, 0))
            forward = matrix.to_3x3() @ Vector((0, 1, 0))
            up = matrix.to_3x3() @ Vector((0, 0, 1))
            
            avg_right += right.normalized()
            avg_forward += forward.normalized()
            avg_up += up.normalized()
        
        # Normalize averages
        count = len(matrices)
        avg_right = (avg_right / count).normalized()
        avg_forward = (avg_forward / count).normalized()
        avg_up = (avg_up / count).normalized()
        
        # Create orientation matrix
        orientation_matrix = Matrix()
        orientation_matrix[0][0:3] = avg_right
        orientation_matrix[1][0:3] = avg_forward
        orientation_matrix[2][0:3] = avg_up
        
        return {
            "forward": avg_forward,
            "up": avg_up,
            "right": avg_right,
            "matrix": orientation_matrix
        }
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "forward": Vector((0, 1, 0)),
            "up": Vector((0, 0, 1)),
            "right": Vector((1, 0, 0)),
            "matrix": Matrix()
        }


def analyze_materials(objects: List[bpy.types.Object]) -> Dict[str, Any]:
    """
    Sample and analyze materials from objects.
    
    Args:
        objects: List of objects to analyze
        
    Returns:
        Dictionary with material analysis
    """
    # # Coba eksekusi kode dengan error handling
    try:
        material_types = []
        emission_count = 0
        roughness_values = []
        transparency_values = []
        total_materials = 0
        
        for obj in objects:
            # # Coba eksekusi kode dengan error handling
            try:
                if not obj.data or not hasattr(obj.data, 'materials'):
                    continue
                
                for mat_slot in obj.material_slots:
                    if not mat_slot.material:
                        continue
                    
                    material = mat_slot.material
                    total_materials += 1
                    
                    # Analyze material properties
                    material_type = analyze_single_material(material)
                    material_types.append(material_type)
                    
                    # Check for emission
                    if has_emission(material):
                        emission_count += 1
                    
                    # Sample roughness
                    roughness = get_material_roughness(material)
                    if roughness is not None:
                        roughness_values.append(roughness)
                    
                    # Sample transparency
                    transparency = get_material_transparency(material)
                    if transparency is not None:
                        transparency_values.append(transparency)
                        
            # # Tangani error jika terjadi
            except Exception as e:
                continue
        
        # Determine dominant material type
        if material_types:
            dominant_type = max(set(material_types), key=material_types.count)
        else:
            dominant_type = "dielectric"
        
        # Calculate averages
        avg_roughness = statistics.mean(roughness_values) if roughness_values else 0.5
        avg_transparency = statistics.mean(transparency_values) if transparency_values else 0.0
        has_any_emission = emission_count > 0
        
        return {
            "dominant_type": dominant_type,
            "has_emission": has_any_emission,
            "average_roughness": avg_roughness,
            "transparency": avg_transparency
        }
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "dominant_type": "dielectric",
            "has_emission": False,
            "average_roughness": 0.5,
            "transparency": 0.0
        }


def analyze_single_material(material: bpy.types.Material) -> str:
    """
    Analyze a single material to determine its type.
    
    Args:
        material: Blender material
        
    Returns:
        Material type string
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not material.use_nodes or not material.node_tree:
            return "dielectric"
        
        # Look for Principled BSDF
        principled_node = None
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled_node = node
                break
        
        if not principled_node:
            return "dielectric"
        
        # Check metallic value
        metallic_input = principled_node.inputs.get('Metallic')
        if metallic_input and metallic_input.default_value > 0.5:
            return "metallic"
        
        # Check transmission for glass
        transmission_input = principled_node.inputs.get('Transmission')
        if transmission_input and transmission_input.default_value > 0.3:
            return "glass"
        
        # Check alpha for transparency
        alpha_input = principled_node.inputs.get('Alpha')
        if alpha_input and alpha_input.default_value < 0.8:
            return "glass"
        
        return "dielectric"
        
    # # Tangani error jika terjadi
    except Exception:
        return "dielectric"


def has_emission(material: bpy.types.Material) -> bool:
    """Check if material has emission."""
    # # Coba eksekusi kode dengan error handling
    try:
        if not material.use_nodes or not material.node_tree:
            return False
        
        # Look for emission nodes
        for node in material.node_tree.nodes:
            if node.type == 'EMISSION':
                return True
            elif node.type == 'BSDF_PRINCIPLED':
                emission_input = node.inputs.get('Emission')
                if emission_input:
                    # Check if emission color is not black
                    if hasattr(emission_input, 'default_value') and len(emission_input.default_value) >= 3:
                        color = emission_input.default_value[:3]
                        if any(c > 0.01 for c in color):
                            return True
        
        return False
        
    # # Tangani error jika terjadi
    except Exception:
        return False


def get_material_roughness(material: bpy.types.Material) -> Optional[float]:
    """Get roughness value from material."""
    # # Coba eksekusi kode dengan error handling
    try:
        if not material.use_nodes or not material.node_tree:
            return None
        
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                roughness_input = node.inputs.get('Roughness')
                if roughness_input:
                    return roughness_input.default_value
        
        return None
        
    # # Tangani error jika terjadi
    except Exception:
        return None


def get_material_transparency(material: bpy.types.Material) -> Optional[float]:
    """Get transparency value from material."""
    # # Coba eksekusi kode dengan error handling
    try:
        if not material.use_nodes or not material.node_tree:
            return None
        
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                # Check alpha
                alpha_input = node.inputs.get('Alpha')
                if alpha_input:
                    return 1.0 - alpha_input.default_value
                
                # Check transmission
                transmission_input = node.inputs.get('Transmission')
                if transmission_input:
                    return transmission_input.default_value
        
        return None
        
    # # Tangani error jika terjadi
    except Exception:
        return None


def calculate_camera_relation(objects: List[bpy.types.Object], context: bpy.types.Context) -> Dict[str, Any]:
    """
    Calculate relationship between subject and camera.
    
    Args:
        objects: List of objects
        context: Blender context
        
    Returns:
        Dictionary with camera relationship data
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not objects:
            return {"distance": 5.0, "angle": Vector()}
        
        # Calculate subject center
        bounds = calculate_bounds(objects)
        subject_center = bounds["center"]
        
        # Get active camera
        camera = None
        if context.scene.camera:
            camera = context.scene.camera
        elif context.space_data and hasattr(context.space_data, 'camera'):
            camera = context.space_data.camera
        
        if not camera:
            return {"distance": 5.0, "angle": Vector()}
        
        # Calculate distance and angle
        camera_location = camera.matrix_world.translation
        distance = (camera_location - subject_center).length
        
        # Calculate view angle
        to_camera = (camera_location - subject_center).normalized()
        
        # Get camera forward direction (negative Z axis in camera space)
        # Fix: Separate matrix operation from negation to avoid operator issues
        camera_rotation = camera.matrix_world.to_3x3()
        camera_z_axis = camera_rotation @ Vector((0, 0, 1))
        camera_forward = -camera_z_axis  # Apply negation to the result vector
        
        angle = Vector((
            to_camera.dot(Vector((1, 0, 0))),  # X component
            to_camera.dot(Vector((0, 1, 0))),  # Y component
            to_camera.dot(Vector((0, 0, 1)))   # Z component
        ))
        
        return {
            "distance": distance,
            "angle": angle
        }
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {"distance": 5.0, "angle": Vector()}


def calculate_complexity_score(objects: List[bpy.types.Object]) -> float:
    """
    Calculate complexity score based on object properties.
    
    Args:
        objects: List of objects to analyze
        
    Returns:
        Complexity score (0.0 to 1.0)
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not objects:
            return 0.0
        
        total_score = 0.0
        
        for obj in objects:
            # # Coba eksekusi kode dengan error handling
            try:
                score = 0.0
                
                # Base score from object count
                score += 0.1
                
                # Vertex count factor
                if obj.data and hasattr(obj.data, 'vertices'):
                    vert_count = len(obj.data.vertices)
                    if vert_count > 1000:
                        score += 0.3
                    elif vert_count > 100:
                        score += 0.2
                    else:
                        score += 0.1
                
                # Material complexity
                if hasattr(obj.data, 'materials') and obj.data.materials:
                    mat_count = len([m for m in obj.data.materials if m])
                    score += min(mat_count * 0.1, 0.3)
                
                # Modifier complexity
                if obj.modifiers:
                    mod_count = len(obj.modifiers)
                    score += min(mod_count * 0.05, 0.2)
                
                total_score += score
                
            # # Tangani error jika terjadi
            except Exception:
                total_score += 0.1  # Minimal score for objects with errors
        
        # Normalize to 0-1 range
        normalized_score = min(total_score / len(objects), 1.0)
        
        return normalized_score
        
    # # Tangani error jika terjadi
    except Exception:
        return 0.5  # Default complexity


def detect_subject_type(analysis: SubjectAnalysis) -> str:
    """
    Auto-detect subject type based on analysis.
    
    Args:
        analysis: Complete subject analysis
        
    Returns:
        Subject type string
    """
    # # Coba eksekusi kode dengan error handling
    try:
        dimensions = analysis.bounds["dimensions"]
        diagonal = analysis.bounds["diagonal"]
        complexity = analysis.complexity_score
        
        # Portrait detection (tall and narrow, moderate complexity)
        if dimensions.z > dimensions.x and dimensions.z > dimensions.y:
            if 0.5 < diagonal < 4.0 and complexity > 0.3:
                return "portrait"
        
        # Vehicle detection (large, wide, complex)
        if diagonal > 5.0 and dimensions.y > dimensions.z:
            if complexity > 0.4:
                return "automotive"
        
        # Fashion detection (tall, complex, multiple materials)
        if dimensions.z > dimensions.x * 1.5:
            if analysis.object_count > 1 or complexity > 0.5:
                return "fashion"
        
        # Default to product
        return "product"
        
    # # Tangani error jika terjadi
    except Exception:
        return "product"


def calculate_optimal_distance(analysis: SubjectAnalysis, template: Dict[str, Any]) -> float:
    """
    Calculate ideal light distance based on subject analysis and template.
    
    Args:
        analysis: Subject analysis result
        template: Template dictionary
        
    Returns:
        Optimal distance multiplier
    """
    # # Coba eksekusi kode dengan error handling
    try:
        # Get base distance from template
        base_distance = template.get('settings', {}).get('base_distance', 2.0)
        
        # Scale based on subject size
        subject_radius = analysis.bounds["radius"]
        
        # Different scaling for different subject types
        if analysis.type == "portrait":
            # Closer for portraits
            multiplier = max(1.0, subject_radius * 0.8)
        elif analysis.type == "automotive":
            # Further for vehicles
            multiplier = max(2.0, subject_radius * 1.2)
        elif analysis.type == "fashion":
            # Medium distance for fashion
            multiplier = max(1.5, subject_radius * 1.0)
        else:
            # Standard product distance
            multiplier = max(1.0, subject_radius * 1.0)
        
        # Adjust for complexity
        if analysis.complexity_score > 0.7:
            multiplier *= 1.2  # Further for complex subjects
        elif analysis.complexity_score < 0.3:
            multiplier *= 0.9  # Closer for simple subjects
        
        return base_distance * multiplier
        
    # # Tangani error jika terjadi
    except Exception as e:
        return 2.0  # Safe default


# Utility functions for utils integration
def lumi_get_object_bounds(obj: bpy.types.Object) -> Dict[str, Any]:
    """
    Get single object bounds.
    
    Args:
        obj: Blender object
        
    Returns:
        Dictionary with bounds data
    """
    # # Coba eksekusi kode dengan error handling
    try:
        return calculate_bounds([obj])
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "min": Vector(),
            "max": Vector(), 
            "center": Vector(),
            "dimensions": Vector((1.0, 1.0, 1.0)),
            "diagonal": 1.0,
            "radius": 0.5
        }


def lumi_sample_object_material(obj: bpy.types.Object) -> Dict[str, Any]:
    """
    Sample dominant material from object.
    
    Args:
        obj: Blender object
        
    Returns:
        Dictionary with material data
    """
    # # Coba eksekusi kode dengan error handling
    try:
        return analyze_materials([obj])
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "dominant_type": "dielectric",
            "has_emission": False,
            "average_roughness": 0.5,
            "transparency": 0.0
        }


# ============================================================================
# ENHANCED MATERIAL ANALYSIS SYSTEM
# ============================================================================

# Material-specific lighting adjustment rules
MATERIAL_LIGHTING_RULES = {
    "metallic": {
        "intensity_multiplier": 0.8,
        "size_multiplier": 1.5,  # Softer reflections
        "add_gradient": True,
        "prefer_area_lights": True,
        "avoid_direct_harsh": True,
        "increase_environment": True
    },
    "glass": {
        "add_rim_light": True,
        "rim_intensity": 1.5,
        "backlight_required": True,
        "environment_important": True,
        "intensity_multiplier": 1.2,
        "prefer_soft_shadows": True,
        "transmission_compensation": True
    },
    "skin": {
        "color_temperature": 5200,  # Slightly warm
        "soft_shadows": True,
        "add_fill": True,
        "sss_compensation": True,
        "intensity_multiplier": 1.1,
        "avoid_harsh_directional": True,
        "prefer_area_lights": True
    },
    "fabric": {
        "soft_lighting": True,
        "avoid_harsh_shadows": True,
        "texture_preservation": True,
        "intensity_multiplier": 0.9,
        "prefer_diffused": True,
        "avoid_specular_hotspots": True
    },
    "dielectric": {
        # Standard non-metallic materials (plastic, wood, etc.)
        "intensity_multiplier": 1.0,
        "balanced_lighting": True,
        "moderate_shadows": True
    },
    "emission": {
        # Materials with emission
        "reduce_ambient": True,
        "intensity_multiplier": 0.7,
        "enhance_contrast": True
    }
}


def analyze_materials_advanced(objects: List[bpy.types.Object]) -> Dict[str, Any]:
    """
    Deep material analysis for lighting adaptation.
    
    Args:
        objects: List of objects to analyze
        
    Returns:
        Dictionary with comprehensive material analysis and lighting recommendations
    """
    # # Coba eksekusi kode dengan error handling
    try:
        material_data = {
            "types": {},  # Material type counts
            "properties": {
                "average_metallic": 0.0,
                "average_roughness": 0.0,
                "average_specular": 0.0,
                "average_transmission": 0.0,
                "average_emission_strength": 0.0,
                "has_emission": False,
                "has_glass": False,
                "has_sss": False,
                "has_metallic": False,
                "dominant_color": (1.0, 1.0, 1.0),
                "color_variance": 0.0
            },
            "recommendations": {},
            "material_count": 0,
            "complexity_score": 0.0
        }
        
        metallic_values = []
        roughness_values = []
        specular_values = []
        transmission_values = []
        emission_strengths = []
        colors = []
        material_types = []
        
        # Analyze each object's materials
        for obj in objects:
            if obj.type == 'MESH' and obj.data and hasattr(obj.data, 'materials'):
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        mat_analysis = analyze_material_nodes(mat_slot.material)
                        
                        # Collect values for averaging
                        if mat_analysis["metallic"] is not None:
                            metallic_values.append(mat_analysis["metallic"])
                        if mat_analysis["roughness"] is not None:
                            roughness_values.append(mat_analysis["roughness"])
                        if mat_analysis["specular"] is not None:
                            specular_values.append(mat_analysis["specular"])
                        if mat_analysis["transmission"] is not None:
                            transmission_values.append(mat_analysis["transmission"])
                        if mat_analysis["emission_strength"] is not None:
                            emission_strengths.append(mat_analysis["emission_strength"])
                        if mat_analysis["base_color"]:
                            colors.append(mat_analysis["base_color"])
                        
                        # Count material types
                        mat_type = mat_analysis["type"]
                        material_types.append(mat_type)
                        if mat_type in material_data["types"]:
                            material_data["types"][mat_type] += 1
                        else:
                            material_data["types"][mat_type] = 1
                        
                        material_data["material_count"] += 1
        
        # Calculate averages
        if metallic_values:
            material_data["properties"]["average_metallic"] = sum(metallic_values) / len(metallic_values)
            material_data["properties"]["has_metallic"] = max(metallic_values) > 0.1
        
        if roughness_values:
            material_data["properties"]["average_roughness"] = sum(roughness_values) / len(roughness_values)
        
        if specular_values:
            material_data["properties"]["average_specular"] = sum(specular_values) / len(specular_values)
        
        if transmission_values:
            material_data["properties"]["average_transmission"] = sum(transmission_values) / len(transmission_values)
            material_data["properties"]["has_glass"] = max(transmission_values) > 0.1
        
        if emission_strengths:
            material_data["properties"]["average_emission_strength"] = sum(emission_strengths) / len(emission_strengths)
            material_data["properties"]["has_emission"] = max(emission_strengths) > 0.1
        
        # Calculate dominant color and variance
        if colors:
            material_data["properties"]["dominant_color"] = calculate_dominant_color(colors)
            material_data["properties"]["color_variance"] = calculate_color_variance(colors)
        
        # Detect subsurface scattering
        material_data["properties"]["has_sss"] = detect_subsurface_scattering(objects)
        
        # Calculate complexity score
        material_data["complexity_score"] = calculate_material_complexity(material_data)
        
        # Generate lighting recommendations
        material_data["recommendations"] = generate_lighting_recommendations(material_data)
        
        return material_data
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "types": {"dielectric": 1},
            "properties": {
                "average_metallic": 0.0,
                "average_roughness": 0.5,
                "has_emission": False,
                "has_glass": False,
                "has_sss": False,
                "dominant_color": (1.0, 1.0, 1.0)
            },
            "recommendations": {},
            "material_count": 1,
            "complexity_score": 1.0
        }


def analyze_material_nodes(material: bpy.types.Material) -> Dict[str, Any]:
    """
    Analyze material node tree for detailed properties.
    
    Args:
        material: Blender material to analyze
        
    Returns:
        Dictionary with material properties
    """
    analysis = {
        "type": "dielectric",
        "metallic": None,
        "roughness": None,
        "specular": None,
        "transmission": None,
        "emission_strength": None,
        "base_color": None,
        "has_sss": False,
        "is_glass": False,
        "is_emission": False
    }
    
    # # Coba eksekusi kode dengan error handling
    try:
        if not material.use_nodes or not material.node_tree:
            # Legacy material analysis
            return analyze_legacy_material(material)
        
        # Find principled BSDF node
        principled_node = None
        emission_node = None
        
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled_node = node
            elif node.type == 'EMISSION':
                emission_node = node
        
        if principled_node:
            # Extract principled BSDF values
            analysis["metallic"] = get_node_input_value(principled_node, "Metallic", 0.0)
            analysis["roughness"] = get_node_input_value(principled_node, "Roughness", 0.5)
            analysis["transmission"] = get_node_input_value(principled_node, "Transmission", 0.0)
            
            # Get base color
            base_color_input = get_node_input_value(principled_node, "Base Color", (1.0, 1.0, 1.0, 1.0))
            if len(base_color_input) >= 3:
                analysis["base_color"] = base_color_input[:3]
            
            # Check for subsurface scattering
            if hasattr(principled_node.inputs, 'Subsurface'):
                sss_value = get_node_input_value(principled_node, "Subsurface", 0.0)
                analysis["has_sss"] = sss_value > 0.01
            
            # Determine material type
            if analysis["metallic"] and analysis["metallic"] > 0.5:
                analysis["type"] = "metallic"
            elif analysis["transmission"] and analysis["transmission"] > 0.1:
                analysis["type"] = "glass"
                analysis["is_glass"] = True
            elif analysis["has_sss"]:
                analysis["type"] = "skin"  # Or organic material with SSS
            else:
                analysis["type"] = "dielectric"
        
        if emission_node:
            # Check emission strength
            emission_strength = get_node_input_value(emission_node, "Strength", 1.0)
            analysis["emission_strength"] = emission_strength
            analysis["is_emission"] = emission_strength > 0.1
            if analysis["is_emission"]:
                analysis["type"] = "emission"
        
        return analysis
        
    # # Tangani error jika terjadi
    except Exception as e:
        return analysis


def get_node_input_value(node, input_name: str, default_value):
    """
    Get value from node input, handling both sockets and default values.
    
    Args:
        node: Blender shader node
        input_name: Name of the input socket
        default_value: Default value if input not found
        
    Returns:
        Input value or default
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if input_name in node.inputs:
            input_socket = node.inputs[input_name]
            if input_socket.is_linked:
                # Input is connected, try to get the value from connected node
                # For simplicity, return default for linked inputs
                return default_value
            else:
                # Use default value from socket
                return input_socket.default_value
        return default_value
    except:
        return default_value


def analyze_legacy_material(material: bpy.types.Material) -> Dict[str, Any]:
    """
    Analyze legacy Blender materials (non-nodes).
    
    Args:
        material: Legacy Blender material
        
    Returns:
        Dictionary with basic material properties
    """
    return {
        "type": "dielectric",
        "metallic": 0.0,
        "roughness": 1.0 - getattr(material, 'specular_hardness', 50) / 100.0,
        "specular": getattr(material, 'specular_intensity', 0.5),
        "transmission": getattr(material, 'alpha', 1.0) if hasattr(material, 'alpha') else 0.0,
        "emission_strength": getattr(material, 'emit', 0.0),
        "base_color": tuple(getattr(material, 'diffuse_color', (1.0, 1.0, 1.0))[:3]),
        "has_sss": False,
        "is_glass": False,
        "is_emission": False
    }


def calculate_dominant_color(colors: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """
    Calculate the dominant color from a list of colors.
    
    Args:
        colors: List of RGB color tuples
        
    Returns:
        Dominant color as RGB tuple
    """
    if not colors:
        return (1.0, 1.0, 1.0)
    
    # Simple average for now - could be enhanced with clustering
    r_avg = sum(color[0] for color in colors) / len(colors)
    g_avg = sum(color[1] for color in colors) / len(colors)
    b_avg = sum(color[2] for color in colors) / len(colors)
    
    return (r_avg, g_avg, b_avg)


def calculate_color_variance(colors: List[Tuple[float, float, float]]) -> float:
    """
    Calculate color variance to determine material complexity.
    
    Args:
        colors: List of RGB color tuples
        
    Returns:
        Color variance score (0.0 = uniform, 1.0 = highly varied)
    """
    if len(colors) <= 1:
        return 0.0
    
    # # Coba eksekusi kode dengan error handling
    try:
        # Calculate variance for each channel
        r_values = [color[0] for color in colors]
        g_values = [color[1] for color in colors]
        b_values = [color[2] for color in colors]
        
        r_variance = statistics.variance(r_values) if len(r_values) > 1 else 0.0
        g_variance = statistics.variance(g_values) if len(g_values) > 1 else 0.0
        b_variance = statistics.variance(b_values) if len(b_values) > 1 else 0.0
        
        # Average variance across channels
        avg_variance = (r_variance + g_variance + b_variance) / 3.0
        
        # Normalize to 0-1 range (variance is typically small for colors)
        return min(1.0, avg_variance * 10.0)
        
    except:
        return 0.0


def detect_subsurface_scattering(objects: List[bpy.types.Object]) -> bool:
    """
    Detect if any materials use subsurface scattering.
    
    Args:
        objects: List of objects to check
        
    Returns:
        True if SSS detected, False otherwise
    """
    # # Coba eksekusi kode dengan error handling
    try:
        for obj in objects:
            if obj.type == 'MESH' and obj.data and hasattr(obj.data, 'materials'):
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        for node in mat_slot.material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                if 'Subsurface' in node.inputs:
                                    sss_value = get_node_input_value(node, "Subsurface", 0.0)
                                    if sss_value > 0.01:
                                        return True
                            elif node.type == 'SUBSURFACE_SCATTERING':
                                return True
        return False
    except:
        return False


def calculate_material_complexity(material_data: Dict[str, Any]) -> float:
    """
    Calculate material complexity score for lighting adaptation.
    
    Args:
        material_data: Material analysis data
        
    Returns:
        Complexity score (1.0 = simple, higher = more complex)
    """
    # # Coba eksekusi kode dengan error handling
    try:
        base_score = 1.0
        
        # More material types = higher complexity
        type_count = len(material_data["types"])
        base_score += type_count * 0.5
        
        # Special materials increase complexity
        props = material_data["properties"]
        if props.get("has_glass", False):
            base_score += 1.0
        if props.get("has_emission", False):
            base_score += 0.8
        if props.get("has_sss", False):
            base_score += 1.2
        if props.get("has_metallic", False):
            base_score += 0.6
        
        # Color variance affects complexity
        color_variance = props.get("color_variance", 0.0)
        base_score += color_variance * 0.5
        
        # High transmission or extreme roughness
        if props.get("average_transmission", 0.0) > 0.5:
            base_score += 0.5
        if props.get("average_roughness", 0.5) < 0.1 or props.get("average_roughness", 0.5) > 0.9:
            base_score += 0.3
        
        return base_score
        
    except:
        return 1.0


def generate_lighting_recommendations(material_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate lighting recommendations based on material analysis.
    
    Args:
        material_data: Comprehensive material analysis data
        
    Returns:
        Dictionary with lighting recommendations
    """
    # # Coba eksekusi kode dengan error handling
    try:
        recommendations = {
            "intensity_multiplier": 1.0,
            "size_multiplier": 1.0,
            "color_temperature": 5500,  # Default daylight
            "shadow_softness": 0.5,
            "additional_lights": [],
            "avoid_techniques": [],
            "preferred_techniques": [],
            "special_considerations": []
        }
        
        # Get dominant material types
        type_counts = material_data.get("types", {})
        if not type_counts:
            return recommendations
        
        dominant_type = max(type_counts, key=type_counts.get)
        properties = material_data.get("properties", {})
        
        # Apply rules for dominant material type
        if dominant_type in MATERIAL_LIGHTING_RULES:
            rules = MATERIAL_LIGHTING_RULES[dominant_type]
            
            # Apply basic multipliers
            recommendations["intensity_multiplier"] = rules.get("intensity_multiplier", 1.0)
            recommendations["size_multiplier"] = rules.get("size_multiplier", 1.0)
            
            # Color temperature adjustments
            if "color_temperature" in rules:
                recommendations["color_temperature"] = rules["color_temperature"]
            
            # Special lighting techniques
            if rules.get("add_rim_light", False):
                recommendations["additional_lights"].append({
                    "type": "rim",
                    "intensity": rules.get("rim_intensity", 1.0),
                    "position": "behind_subject"
                })
            
            if rules.get("add_fill", False):
                recommendations["additional_lights"].append({
                    "type": "fill",
                    "intensity": 0.3,
                    "position": "opposite_key"
                })
            
            # Preferred techniques
            if rules.get("prefer_area_lights", False):
                recommendations["preferred_techniques"].append("use_area_lights")
            
            if rules.get("soft_shadows", False):
                recommendations["shadow_softness"] = 0.8
                recommendations["preferred_techniques"].append("soft_shadows")
            
            # Techniques to avoid
            if rules.get("avoid_harsh_shadows", False):
                recommendations["avoid_techniques"].append("harsh_directional_lighting")
            
            if rules.get("avoid_direct_harsh", False):
                recommendations["avoid_techniques"].append("direct_spot_lights")
        
        # Additional adjustments based on specific properties
        if properties.get("has_glass", False):
            recommendations["special_considerations"].append("requires_environment_lighting")
            recommendations["special_considerations"].append("backlight_important")
            
        if properties.get("has_emission", False):
            recommendations["intensity_multiplier"] *= 0.8  # Reduce ambient
            recommendations["special_considerations"].append("reduce_ambient_contribution")
            
        if properties.get("has_metallic", False):
            recommendations["size_multiplier"] *= 1.3  # Larger lights for softer reflections
            recommendations["special_considerations"].append("requires_controlled_reflections")
            
        if properties.get("has_sss", False):
            recommendations["preferred_techniques"].append("subsurface_friendly_lighting")
            recommendations["special_considerations"].append("avoid_extreme_angles")
        
        # Complexity-based adjustments
        complexity = material_data.get("complexity_score", 1.0)
        if complexity > 2.0:
            recommendations["special_considerations"].append("high_complexity_materials")
            recommendations["intensity_multiplier"] *= 0.9  # Slightly reduce intensity for complex materials
        
        return recommendations
        
    # # Tangani error jika terjadi
    except Exception as e:
        return {
            "intensity_multiplier": 1.0,
            "size_multiplier": 1.0,
            "color_temperature": 5500,
            "shadow_softness": 0.5,
            "additional_lights": [],
            "avoid_techniques": [],
            "preferred_techniques": [],
            "special_considerations": []
        }


def apply_material_adjustments(light: bpy.types.Object, recommendations: Dict[str, Any]) -> None:
    """
    Apply material-based adjustments to a light object.
    
    Args:
        light: Blender light object
        recommendations: Lighting recommendations from material analysis
    """
    # # Coba eksekusi kode dengan error handling
    try:
        if not light or not light.data or light.type != 'LIGHT':
            return
        
        # Apply intensity adjustments
        intensity_mult = recommendations.get("intensity_multiplier", 1.0)
        if hasattr(light.data, 'energy'):
            light.data.energy *= intensity_mult
        
        # Apply size adjustments for area lights
        if light.data.type == 'AREA':
            size_mult = recommendations.get("size_multiplier", 1.0)
            if hasattr(light.data, 'size'):
                light.data.size *= size_mult
            if hasattr(light.data, 'size_y'):
                light.data.size_y *= size_mult
        
        # Apply color temperature if supported
        color_temp = recommendations.get("color_temperature")
        if color_temp and hasattr(light.data, 'color'):
            apply_color_temperature(light, color_temp)
        
        # Adjust shadow softness for supported light types
        shadow_softness = recommendations.get("shadow_softness", 0.5)
        if light.data.type == 'SUN' and hasattr(light.data, 'angle'):
            # For sun lights, angle controls softness
            light.data.angle = shadow_softness * 0.1  # Convert to radians
        elif light.data.type == 'SPOT' and hasattr(light.data, 'spot_blend'):
            # For spot lights, increase blend for softer shadows
            light.data.spot_blend = max(0.1, shadow_softness * 0.5)
        
    # # Tangani error jika terjadi
    except Exception as e:
        pass


def apply_color_temperature(light: bpy.types.Object, temperature: float) -> None:
    """
    Apply color temperature to light.
    
    Args:
        light: Blender light object
        temperature: Color temperature in Kelvin
    """
    # # Coba eksekusi kode dengan error handling
    try:
        # Simple color temperature to RGB conversion
        # This is a simplified version - could be enhanced with proper blackbody curve
        if temperature <= 3000:
            # Warm/orange
            color = (1.0, 0.6, 0.2)
        elif temperature <= 4000:
            # Warm white
            color = (1.0, 0.8, 0.5)
        elif temperature <= 5500:
            # Neutral white
            color = (1.0, 1.0, 1.0)
        elif temperature <= 7000:
            # Cool white
            color = (0.8, 0.9, 1.0)
        else:
            # Very cool/blue
            color = (0.6, 0.8, 1.0)
        
        if hasattr(light.data, 'color'):
            light.data.color = color
            
    # # Tangani error jika terjadi
    except Exception as e:
        pass


# Export functions
__all__ = [
    'SubjectAnalysis',
    'analyze_subject',
    'calculate_bounds',
    'detect_orientation', 
    'analyze_materials',
    'analyze_materials_advanced',
    'detect_subject_type',
    'calculate_optimal_distance',
    'apply_material_adjustments',
    'generate_lighting_recommendations',
    'MATERIAL_LIGHTING_RULES',
    'lumi_get_object_bounds',
    'lumi_sample_object_material'
]
