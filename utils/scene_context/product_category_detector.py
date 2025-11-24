"""
ProductCategoryDetector - Detects product category from scene analysis.

Detects 8 product categories:
- jewelry: Rings, necklaces, watches, gemstones
- food: Dishes, beverages, ingredients
- cosmetics: Makeup, perfumes, skincare
- electronics: Phones, cameras, computers
- automotive: Cars, motorcycles, wheels
- apparel: Clothing, shoes, bags
- furniture: Chairs, tables, decor
- generic: Default fallback

Detection methods:
1. Name-based (highest confidence)
2. Material-based (medium confidence)
3. Geometry-based (lower confidence)
4. Combined (best accuracy)
"""

import bpy
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from mathutils import Vector

from .material_analyzer import MaterialData
from .bounds_calculator import BoundsData


class ProductCategory(str, Enum):
    """Supported product categories."""
    JEWELRY = "jewelry"
    FOOD = "food"
    COSMETICS = "cosmetics"
    ELECTRONICS = "electronics"
    AUTOMOTIVE = "automotive"
    APPAREL = "apparel"
    FURNITURE = "furniture"
    GENERIC = "generic"


class ProductSubcategory(str, Enum):
    """Product subcategories for more specific detection."""
    # Jewelry
    RING = "ring"
    NECKLACE = "necklace"
    WATCH = "watch"
    EARRING = "earring"
    GEMSTONE = "gemstone"
    
    # Food
    BEVERAGE = "beverage"
    DISH = "dish"
    INGREDIENT = "ingredient"
    DESSERT = "dessert"
    
    # Cosmetics
    PERFUME = "perfume"
    MAKEUP = "makeup"
    SKINCARE = "skincare"
    
    # Electronics
    PHONE = "phone"
    CAMERA = "camera"
    COMPUTER = "computer"
    ACCESSORY = "accessory"
    
    # Automotive
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    WHEEL = "wheel"
    
    # Apparel
    CLOTHING = "clothing"
    FOOTWEAR = "footwear"
    BAG = "bag"
    
    # Furniture
    SEATING = "seating"
    TABLE = "table"
    STORAGE = "storage"
    LIGHTING = "lighting"
    
    # Generic
    GENERIC = "generic"


# ============================================================================
# LOOKUP TABLES - Category-specific lighting parameters
# ============================================================================

CATEGORY_LIGHTING_PARAMS = {
    ProductCategory.JEWELRY: {
        'color_temp': 5800,
        'key_fill_ratio': 4.0,
        'style': 'dramatic',
        'intensity_multiplier': 1.3,
        'size_multiplier': 1.2,
        'recommended_template': 'jewelry_sparkle',
        'back_light_intensity': 0.7,
    },
    ProductCategory.FOOD: {
        'color_temp': 3800,
        'key_fill_ratio': 2.0,
        'style': 'soft',
        'intensity_multiplier': 0.9,
        'size_multiplier': 1.4,
        'recommended_template': 'food_appetizing',
        'back_light_intensity': 0.3,
    },
    ProductCategory.COSMETICS: {
        'color_temp': 5200,
        'key_fill_ratio': 2.5,
        'style': 'soft',
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.3,
        'recommended_template': 'beauty_soft',
        'back_light_intensity': 0.4,
    },
    ProductCategory.ELECTRONICS: {
        'color_temp': 5500,
        'key_fill_ratio': 3.0,
        'style': 'studio',
        'intensity_multiplier': 1.1,
        'size_multiplier': 1.1,
        'recommended_template': 'product_clean',
        'back_light_intensity': 0.5,
    },
    ProductCategory.AUTOMOTIVE: {
        'color_temp': 5500,
        'key_fill_ratio': 3.5,
        'style': 'dramatic',
        'intensity_multiplier': 1.2,
        'size_multiplier': 1.5,
        'recommended_template': 'automotive_dramatic',
        'back_light_intensity': 0.6,
    },
    ProductCategory.APPAREL: {
        'color_temp': 5000,
        'key_fill_ratio': 2.5,
        'style': 'natural',
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.2,
        'recommended_template': 'fashion_natural',
        'back_light_intensity': 0.4,
    },
    ProductCategory.FURNITURE: {
        'color_temp': 4500,
        'key_fill_ratio': 2.5,
        'style': 'natural',
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.3,
        'recommended_template': 'interior_warm',
        'back_light_intensity': 0.3,
    },
    ProductCategory.GENERIC: {
        'color_temp': 5500,
        'key_fill_ratio': 3.0,
        'style': 'studio',
        'intensity_multiplier': 1.0,
        'size_multiplier': 1.0,
        'recommended_template': 'product_standard',
        'back_light_intensity': 0.5,
    },
}

# Name patterns for category detection
NAME_PATTERNS = {
    ProductCategory.JEWELRY: [
        'ring', 'necklace', 'bracelet', 'earring', 'pendant',
        'gem', 'diamond', 'gold', 'silver', 'jewelry', 'jewel',
        'watch', 'wristwatch', 'chain', 'brooch', 'tiara',
        'ruby', 'sapphire', 'emerald', 'pearl', 'platinum',
    ],
    ProductCategory.FOOD: [
        'food', 'dish', 'plate', 'bowl', 'cup', 'glass', 'bottle',
        'fruit', 'vegetable', 'meat', 'bread', 'cake', 'dessert',
        'beverage', 'drink', 'coffee', 'wine', 'beer', 'juice',
        'pizza', 'burger', 'salad', 'soup', 'pasta', 'sushi',
    ],
    ProductCategory.COSMETICS: [
        'lipstick', 'makeup', 'perfume', 'cream', 'lotion',
        'cosmetic', 'beauty', 'skincare', 'foundation', 'mascara',
        'fragrance', 'serum', 'powder', 'blush', 'eyeshadow',
        'nail', 'polish', 'shampoo', 'conditioner',
    ],
    ProductCategory.ELECTRONICS: [
        'phone', 'smartphone', 'laptop', 'computer', 'tablet',
        'camera', 'headphone', 'speaker', 'monitor', 'keyboard',
        'mouse', 'gadget', 'device', 'electronic', 'screen',
        'tv', 'television', 'remote', 'charger', 'cable',
    ],
    ProductCategory.AUTOMOTIVE: [
        'car', 'vehicle', 'automobile', 'wheel', 'tire',
        'motorcycle', 'bike', 'engine', 'automotive', 'truck',
        'suv', 'sedan', 'coupe', 'bumper', 'headlight',
    ],
    ProductCategory.APPAREL: [
        'shirt', 'pants', 'dress', 'jacket', 'coat',
        'shoe', 'boot', 'sneaker', 'hat', 'bag',
        'clothing', 'apparel', 'fashion', 'wear', 'jeans',
        'skirt', 'blouse', 'suit', 'tie', 'scarf',
    ],
    ProductCategory.FURNITURE: [
        'chair', 'table', 'desk', 'sofa', 'couch', 'bed',
        'cabinet', 'shelf', 'lamp', 'furniture', 'decor',
        'stool', 'bench', 'drawer', 'wardrobe', 'bookshelf',
    ],
}

# Subcategory patterns
SUBCATEGORY_PATTERNS = {
    # Jewelry
    'ring': ProductSubcategory.RING,
    'necklace': ProductSubcategory.NECKLACE,
    'chain': ProductSubcategory.NECKLACE,
    'pendant': ProductSubcategory.NECKLACE,
    'watch': ProductSubcategory.WATCH,
    'wristwatch': ProductSubcategory.WATCH,
    'earring': ProductSubcategory.EARRING,
    'gem': ProductSubcategory.GEMSTONE,
    'diamond': ProductSubcategory.GEMSTONE,
    'ruby': ProductSubcategory.GEMSTONE,
    'sapphire': ProductSubcategory.GEMSTONE,
    
    # Food
    'drink': ProductSubcategory.BEVERAGE,
    'beverage': ProductSubcategory.BEVERAGE,
    'coffee': ProductSubcategory.BEVERAGE,
    'wine': ProductSubcategory.BEVERAGE,
    'bottle': ProductSubcategory.BEVERAGE,
    'glass': ProductSubcategory.BEVERAGE,
    'dish': ProductSubcategory.DISH,
    'plate': ProductSubcategory.DISH,
    'bowl': ProductSubcategory.DISH,
    'cake': ProductSubcategory.DESSERT,
    'dessert': ProductSubcategory.DESSERT,
    
    # Electronics
    'phone': ProductSubcategory.PHONE,
    'smartphone': ProductSubcategory.PHONE,
    'camera': ProductSubcategory.CAMERA,
    'laptop': ProductSubcategory.COMPUTER,
    'computer': ProductSubcategory.COMPUTER,
    
    # More mappings...
}


@dataclass
class ProductCategoryResult:
    """Result of product category detection."""
    category: ProductCategory
    subcategory: ProductSubcategory
    confidence: float  # 0.0 - 1.0
    detection_method: str  # "name", "material", "geometry", "combined"
    
    # Recommended lighting parameters (from lookup table)
    recommended_color_temp: int
    recommended_key_fill_ratio: float
    recommended_style: str
    intensity_multiplier: float
    size_multiplier: float
    
    # Detection details
    detection_reasons: List[str] = field(default_factory=list)
    
    @staticmethod
    def default() -> 'ProductCategoryResult':
        """Return default generic result."""
        params = CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC]
        return ProductCategoryResult(
            category=ProductCategory.GENERIC,
            subcategory=ProductSubcategory.GENERIC,
            confidence=0.3,
            detection_method="fallback",
            recommended_color_temp=params['color_temp'],
            recommended_key_fill_ratio=params['key_fill_ratio'],
            recommended_style=params['style'],
            intensity_multiplier=params['intensity_multiplier'],
            size_multiplier=params['size_multiplier'],
            detection_reasons=["No strong category signals detected"],
        )


class ProductCategoryDetector:
    """
    Detects product category from scene analysis.
    
    Uses multiple detection methods:
    1. Object name pattern matching (highest confidence)
    2. Material property analysis (medium confidence)
    3. Geometry analysis (lower confidence)
    4. Combined heuristics (best accuracy)
    
    Usage:
        detector = ProductCategoryDetector()
        result = detector.detect(objects, material_data, bounds)
        
        # Access results
        print(f"Category: {result.category}")
        print(f"Confidence: {result.confidence}")
        print(f"Recommended color temp: {result.recommended_color_temp}K")
    """
    
    def __init__(self):
        self._name_patterns = NAME_PATTERNS
        self._subcategory_patterns = SUBCATEGORY_PATTERNS
    
    def detect(self,
               objects: List[bpy.types.Object],
               material_data: Optional[MaterialData] = None,
               bounds: Optional[BoundsData] = None) -> ProductCategoryResult:
        """
        Detect product category using multiple signals.
        
        Args:
            objects: List of product objects to analyze
            material_data: Material analysis data (optional)
            bounds: Bounding box data (optional)
            
        Returns:
            ProductCategoryResult with category, confidence, and recommendations
        """
        if not objects:
            return ProductCategoryResult.default()
        
        results = []
        
        # Method 1: Name-based detection (highest priority)
        name_result = self._detect_from_names(objects)
        if name_result:
            results.append(name_result)
            # High confidence name match - return early
            if name_result.confidence >= 0.8:
                return name_result
        
        # Method 2: Material-based detection
        if material_data:
            material_result = self._detect_from_materials(material_data)
            if material_result:
                results.append(material_result)
        
        # Method 3: Geometry-based detection
        if bounds:
            geometry_result = self._detect_from_geometry(objects, bounds)
            if geometry_result:
                results.append(geometry_result)
        
        # Combine results for best accuracy
        if results:
            return self._combine_results(results)
        
        return ProductCategoryResult.default()
    
    def _detect_from_names(self, objects: List[bpy.types.Object]) -> Optional[ProductCategoryResult]:
        """
        Detect category from object names.
        
        Checks object names against known patterns for each category.
        """
        category_scores: Dict[ProductCategory, int] = {}
        matched_patterns: Dict[ProductCategory, List[str]] = {}
        detected_subcategory = ProductSubcategory.GENERIC
        
        for obj in objects:
            name_lower = obj.name.lower()
            
            # Check against category patterns
            for category, patterns in self._name_patterns.items():
                for pattern in patterns:
                    if pattern in name_lower:
                        category_scores[category] = category_scores.get(category, 0) + 1
                        if category not in matched_patterns:
                            matched_patterns[category] = []
                        matched_patterns[category].append(pattern)
                        
                        # Check for subcategory
                        if pattern in self._subcategory_patterns:
                            detected_subcategory = self._subcategory_patterns[pattern]
        
        if not category_scores:
            return None
        
        # Get best matching category
        best_category = max(category_scores, key=category_scores.get)
        match_count = category_scores[best_category]
        
        # Calculate confidence based on match count and uniqueness
        other_scores = [s for c, s in category_scores.items() if c != best_category]
        max_other = max(other_scores) if other_scores else 0
        
        # Higher confidence if clear winner
        if match_count >= 3:
            confidence = min(0.95, 0.7 + (match_count * 0.05))
        elif match_count == 2:
            confidence = 0.75 if max_other < 2 else 0.6
        else:
            confidence = 0.6 if max_other == 0 else 0.5
        
        params = CATEGORY_LIGHTING_PARAMS[best_category]
        patterns_str = ", ".join(matched_patterns.get(best_category, [])[:3])
        
        return ProductCategoryResult(
            category=best_category,
            subcategory=detected_subcategory,
            confidence=confidence,
            detection_method="name",
            recommended_color_temp=params['color_temp'],
            recommended_key_fill_ratio=params['key_fill_ratio'],
            recommended_style=params['style'],
            intensity_multiplier=params['intensity_multiplier'],
            size_multiplier=params['size_multiplier'],
            detection_reasons=[f"Name patterns matched: {patterns_str}"],
        )
    
    def _detect_from_materials(self, material_data: MaterialData) -> Optional[ProductCategoryResult]:
        """
        Detect category from material properties.
        
        Uses metallic, roughness, transmission, and SSS values to infer category.
        """
        category = None
        confidence = 0.0
        reasons = []
        
        # High metallic + low roughness = Jewelry (polished metal)
        if material_data.average_metallic > 0.7 and material_data.average_roughness < 0.2:
            category = ProductCategory.JEWELRY
            confidence = 0.7
            reasons.append(f"High metallic ({material_data.average_metallic:.2f}) + low roughness suggests polished metal/jewelry")
        
        # High metallic + medium roughness = Automotive (brushed metal)
        elif material_data.average_metallic > 0.6 and 0.2 <= material_data.average_roughness < 0.5:
            category = ProductCategory.AUTOMOTIVE
            confidence = 0.55
            reasons.append(f"Metallic with medium roughness suggests automotive/industrial")
        
        # Glass-like (transmission) = Cosmetics or Food
        elif material_data.has_transmission and material_data.average_transmission > 0.3:
            category = ProductCategory.COSMETICS  # Perfume bottles, etc.
            confidence = 0.5
            reasons.append(f"High transmission ({material_data.average_transmission:.2f}) suggests glass containers")
        
        # SSS = Food or Cosmetics (skin-like materials)
        elif material_data.has_sss and material_data.average_sss > 0.2:
            category = ProductCategory.FOOD
            confidence = 0.45
            reasons.append(f"Subsurface scattering suggests organic materials (food)")
        
        # Dielectric + very low roughness = Electronics (plastic screens)
        elif material_data.dominant_type == 'dielectric' and material_data.average_roughness < 0.15:
            category = ProductCategory.ELECTRONICS
            confidence = 0.5
            reasons.append("Smooth dielectric surface suggests electronics/screens")
        
        # High roughness + dielectric = Fabric/Apparel
        elif material_data.dominant_type == 'dielectric' and material_data.average_roughness > 0.7:
            category = ProductCategory.APPAREL
            confidence = 0.45
            reasons.append("High roughness dielectric suggests fabric/textiles")
        
        if not category:
            return None
        
        params = CATEGORY_LIGHTING_PARAMS[category]
        
        return ProductCategoryResult(
            category=category,
            subcategory=ProductSubcategory.GENERIC,
            confidence=confidence,
            detection_method="material",
            recommended_color_temp=params['color_temp'],
            recommended_key_fill_ratio=params['key_fill_ratio'],
            recommended_style=params['style'],
            intensity_multiplier=params['intensity_multiplier'],
            size_multiplier=params['size_multiplier'],
            detection_reasons=reasons,
        )
    
    def _detect_from_geometry(self,
                              objects: List[bpy.types.Object],
                              bounds: BoundsData) -> Optional[ProductCategoryResult]:
        """
        Detect category from geometry properties.
        
        Uses size, aspect ratio, and vertex density to infer category.
        """
        category = None
        confidence = 0.0
        reasons = []
        
        diagonal = bounds.diagonal
        dims = bounds.dimensions
        
        # Calculate aspect ratios
        aspect_xy = dims.x / max(0.001, dims.y)
        aspect_xz = dims.x / max(0.001, dims.z)
        height_ratio = dims.z / max(0.001, max(dims.x, dims.y))
        
        # Calculate vertex density (complexity)
        total_verts = 0
        total_faces = 0
        for obj in objects:
            if obj.type == 'MESH' and obj.data:
                total_verts += len(obj.data.vertices)
                total_faces += len(obj.data.polygons)
        
        volume = dims.x * dims.y * dims.z
        vertex_density = total_verts / max(0.001, volume) if volume > 0 else 0
        
        # Very small + high complexity = Jewelry
        if diagonal < 0.15 and vertex_density > 50000:
            category = ProductCategory.JEWELRY
            confidence = 0.55
            reasons.append(f"Very small size ({diagonal:.3f}m) with high detail suggests jewelry")
        
        # Small + high complexity = Jewelry or Electronics
        elif diagonal < 0.3 and vertex_density > 20000:
            category = ProductCategory.JEWELRY
            confidence = 0.45
            reasons.append(f"Small size with complex geometry suggests jewelry/small product")
        
        # Very large + wide = Automotive
        elif diagonal > 2.0 and aspect_xy > 1.5 and aspect_xz > 2.0:
            category = ProductCategory.AUTOMOTIVE
            confidence = 0.5
            reasons.append(f"Large size ({diagonal:.2f}m) with wide aspect suggests vehicle")
        
        # Large + tall = Furniture
        elif diagonal > 0.8 and height_ratio > 0.5:
            category = ProductCategory.FURNITURE
            confidence = 0.45
            reasons.append(f"Large size ({diagonal:.2f}m) with height suggests furniture")
        
        # Medium + flat = Electronics
        elif 0.1 < diagonal < 0.5 and height_ratio < 0.2:
            category = ProductCategory.ELECTRONICS
            confidence = 0.4
            reasons.append("Medium flat shape suggests electronics (phone/tablet)")
        
        # Tall + thin = Cosmetics (bottles)
        elif height_ratio > 2.0 and diagonal < 0.3:
            category = ProductCategory.COSMETICS
            confidence = 0.4
            reasons.append("Tall thin shape suggests bottle/container")
        
        if not category:
            return None
        
        params = CATEGORY_LIGHTING_PARAMS[category]
        
        return ProductCategoryResult(
            category=category,
            subcategory=ProductSubcategory.GENERIC,
            confidence=confidence,
            detection_method="geometry",
            recommended_color_temp=params['color_temp'],
            recommended_key_fill_ratio=params['key_fill_ratio'],
            recommended_style=params['style'],
            intensity_multiplier=params['intensity_multiplier'],
            size_multiplier=params['size_multiplier'],
            detection_reasons=reasons,
        )
    
    def _combine_results(self, results: List[ProductCategoryResult]) -> ProductCategoryResult:
        """
        Combine multiple detection results for best accuracy.
        
        Weights results by confidence and method reliability.
        """
        if len(results) == 1:
            return results[0]
        
        # Weight by method reliability
        method_weights = {
            "name": 1.5,      # Name matching is most reliable
            "material": 1.0,  # Material is moderately reliable
            "geometry": 0.7,  # Geometry is least reliable
        }
        
        # Calculate weighted scores per category
        category_scores: Dict[ProductCategory, float] = {}
        category_reasons: Dict[ProductCategory, List[str]] = {}
        category_subcategory: Dict[ProductCategory, ProductSubcategory] = {}
        
        for result in results:
            weight = method_weights.get(result.detection_method, 1.0)
            weighted_score = result.confidence * weight
            
            cat = result.category
            category_scores[cat] = category_scores.get(cat, 0) + weighted_score
            
            if cat not in category_reasons:
                category_reasons[cat] = []
            category_reasons[cat].extend(result.detection_reasons)
            
            # Keep non-generic subcategory
            if result.subcategory != ProductSubcategory.GENERIC:
                category_subcategory[cat] = result.subcategory
        
        # Get best category
        best_category = max(category_scores, key=category_scores.get)
        best_score = category_scores[best_category]
        
        # Calculate final confidence
        # Boost if multiple methods agree
        agreeing_methods = [r for r in results if r.category == best_category]
        
        if len(agreeing_methods) >= 2:
            # Multiple methods agree - boost confidence
            base_confidence = max(r.confidence for r in agreeing_methods)
            confidence = min(0.95, base_confidence + 0.15)
            detection_method = "combined"
        else:
            # Single method - use original confidence
            confidence = agreeing_methods[0].confidence
            detection_method = agreeing_methods[0].detection_method
        
        # Get subcategory
        subcategory = category_subcategory.get(best_category, ProductSubcategory.GENERIC)
        
        # Get lighting params
        params = CATEGORY_LIGHTING_PARAMS[best_category]
        
        # Combine reasons
        all_reasons = category_reasons.get(best_category, [])
        if len(agreeing_methods) >= 2:
            methods = [r.detection_method for r in agreeing_methods]
            all_reasons.append(f"Multiple methods agree: {', '.join(methods)}")
        
        return ProductCategoryResult(
            category=best_category,
            subcategory=subcategory,
            confidence=confidence,
            detection_method=detection_method,
            recommended_color_temp=params['color_temp'],
            recommended_key_fill_ratio=params['key_fill_ratio'],
            recommended_style=params['style'],
            intensity_multiplier=params['intensity_multiplier'],
            size_multiplier=params['size_multiplier'],
            detection_reasons=all_reasons,
        )
    
    def get_lighting_params(self, category: ProductCategory) -> dict:
        """Get lighting parameters for a category."""
        return CATEGORY_LIGHTING_PARAMS.get(category, CATEGORY_LIGHTING_PARAMS[ProductCategory.GENERIC])


__all__ = [
    'ProductCategoryDetector',
    'ProductCategoryResult',
    'ProductCategory',
    'ProductSubcategory',
    'CATEGORY_LIGHTING_PARAMS',
]
