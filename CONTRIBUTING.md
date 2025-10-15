# Contributing to LumiFlow

Thank you for your interest in contributing to LumiFlow! 🎉

LumiFlow is a community-driven open-source project, and we welcome contributions of all kinds - from bug reports and feature requests to code contributions and documentation improvements.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for everyone, regardless of experience level, gender identity, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards
**Examples of behavior that contributes to a positive environment:**
- Being respectful and inclusive
- Welcoming newcomers and helping them learn
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or personal attacks
- Publishing others' private information without permission
- Any conduct that could reasonably be considered inappropriate

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

**When submitting a bug report, include:**
- **Clear title** - Descriptive and specific
- **Blender version** - e.g., Blender 4.2.0
- **LumiFlow version** - e.g., v1.0.0
- **Operating System** - Windows 10, macOS 14, Ubuntu 22.04, etc.
- **Steps to reproduce** - Numbered, clear steps
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Screenshots/Videos** - If applicable
- **Error messages** - From Blender console or logs
- **Scene file** - If possible, share a minimal .blend file

**Example Bug Report:**
```markdown
**Title:** Light linking fails when using custom collections

**Blender Version:** 4.2.1
**LumiFlow Version:** 1.0.0
**OS:** Windows 11

**Steps to Reproduce:**
1. Create a custom collection named "Products"
2. Add 3 mesh objects to the collection
3. Add Area light using Ctrl+Shift+A
4. Try to link light to collection objects
5. Error appears in console

**Expected:** Light should link to all objects in collection
**Actual:** Error "Cannot access collection items"

**Error Message:**
```
AttributeError: 'Collection' object has no attribute 'link_status'
```

**Screenshot:** [attached]
```

### 💡 Suggesting Features

We love hearing new ideas! Before suggesting a feature:
1. Check [GitHub Discussions](https://github.com/ProductViz/LumiFlow/discussions) for similar requests
2. Check the [Roadmap](#roadmap) to see if it's already planned

**When suggesting a feature, include:**
- **Clear title** - Concise description
- **Problem it solves** - Why is this needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - Other approaches you've thought of
- **Use cases** - Real-world scenarios
- **Mockups/Examples** - If applicable

### 🎨 Contributing Templates

Want to add lighting templates? Great!

**Template Contribution Guidelines:**
1. Follow existing template structure in `assets/templates/`
2. Include proper metadata (category, description, author)
3. Test template in clean scene
4. Provide preview image (1920x1080)
5. Document light setup and intended use

**Template Structure:**
```python
{
    "name": "My Awesome Setup",
    "category": "studio_commercial",
    "description": "Three-point studio lighting for product shots",
    "author": "Your Name",
    "version": "1.0.0",
    "lights": [
        # Light definitions here
    ]
}
```

### 📝 Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples and use cases
- Create tutorials or guides
- Improve code comments and docstrings
- Translate documentation (future)

---

## 🛠️ Development Setup

### Prerequisites
- **Blender 4.2+** (download from [blender.org](https://www.blender.org))
- **Git** for version control
- **Python 3.11** (bundled with Blender)
- **Code editor** - VS Code with Python extension recommended

### Local Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
```bash
git clone https://github.com/YOUR-USERNAME/LumiFlow.git
cd LumiFlow
```

3. **Create a development branch:**
```bash
git checkout -b feature/my-awesome-feature
```

4. **Link to Blender addons directory:**

**Windows:**
```bash
mklink /D "%APPDATA%\Blender Foundation\Blender\4.2\scripts\addons\LumiFlow" "C:\path\to\LumiFlow"
```

**macOS/Linux:**
```bash
ln -s ~/path/to/LumiFlow ~/Library/Application\ Support/Blender/4.2/scripts/addons/LumiFlow
```

5. **Enable addon in Blender:**
   - Open Blender
   - Go to `Edit > Preferences > Add-ons`
   - Enable "LumiFlow"
   - Check "Developer Extras" in preferences

6. **Enable Blender Console** (for debugging):
   - **Windows:** `Window > Toggle System Console`
   - **macOS/Linux:** Run Blender from terminal: `blender`

### Project Structure
```
LumiFlow/
├── __init__.py              # Addon entry point, bl_info
├── base_modal.py            # Base class for modal operators
├── preferences.py           # Addon preferences
├── registration.py          # Class registration
│
├── core/                    # Core systems
│   ├── state.py            # Global state management
│   ├── template_system.py  # Template loading/processing
│   └── assign_manager.py   # Camera-light assignments
│
├── operators/               # All operators
│   ├── smart_ops.py        # Smart control operators
│   ├── linking_ops.py      # Light linking operators
│   ├── positioning/        # Positioning operators
│   └── smart_template/     # Template system operators
│
├── ui/                      # User interface
│   ├── main_panel.py       # Main sidebar panel
│   ├── pie_menus.py        # Pie menu definitions
│   └── overlay/            # Viewport overlay system
│
├── utils/                   # Utilities
│   ├── light.py            # Light creation/manipulation
│   ├── properties.py       # Property definitions
│   └── scene_analysis.py   # Scene analysis tools
│
└── assets/                  # Assets
    ├── icons/              # UI icons
    └── templates/          # Lighting templates
```

---

## 📐 Coding Guidelines

### Python Style Guide

We follow **PEP 8** with some modifications:

**General Rules:**
- Maximum line length: **120 characters**
- Indentation: **4 spaces** (no tabs)
- Encoding: **UTF-8**
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes

**Example:**
```python
def create_area_light(
    name: str,
    location: Vector,
    energy: float = 100.0,
    size: float = 1.0
) -> bpy.types.Object:
    """Create an area light at specified location.
    
    Args:
        name: Light object name
        location: World space position
        energy: Light energy/power in watts
        size: Light size in meters
        
    Returns:
        Created light object
        
    Raises:
        RuntimeError: If light creation fails
    """
    # Implementation here
    pass
```

### Naming Conventions

**Files and Modules:**
- Use `snake_case` for file names
- Example: `smart_template_ops.py`, `light_manager.py`

**Classes:**
- Use `PascalCase` for class names
- Blender operators: `LUMI_OT_operation_name`
- Example: `SmartLightManager`, `LUMI_OT_add_smart_light`

**Functions and Variables:**
- Use `snake_case` for functions and variables
- Private functions: prefix with underscore `_private_function`
- Example: `create_light()`, `_validate_context()`

**Constants:**
- Use `UPPER_CASE` for constants
- Example: `DEFAULT_ENERGY = 100.0`

### Code Organization

**Imports:**
```python
# Standard library
import os
import sys
from typing import List, Dict, Optional

# Third-party (Blender)
import bpy
from mathutils import Vector, Matrix

# Local imports
from ..core.state import get_state
from ..utils.light import create_light
```

**Docstrings:**
```python
def complex_function(param1: str, param2: int = 0) -> bool:
    """One-line summary of the function.
    
    More detailed explanation if needed. Can be multiple
    paragraphs explaining the function's behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: If param1 is empty
        RuntimeError: If operation fails
        
    Example:
        >>> complex_function("test", 42)
        True
    """
    pass
```

### Error Handling

**Use proper logging instead of print:**
```python
import logging

logger = logging.getLogger(__name__)

# BAD
print("Light created")

# GOOD
logger.info("Light created successfully")
logger.debug(f"Light properties: energy={energy}, size={size}")
logger.warning("No camera found, using default placement")
logger.error(f"Failed to create light: {e}", exc_info=True)
```

**Exception handling:**
```python
# BAD - Silent failure
try:
    create_light()
except:
    pass

# GOOD - Logged failure
try:
    create_light()
except Exception as e:
    logger.error(f"Light creation failed: {e}", exc_info=True)
    self.report({'ERROR'}, "Failed to create light")
    return {'CANCELLED'}
```

### Blender-Specific Guidelines

**Operators:**
```python
class LUMI_OT_my_operator(bpy.types.Operator):
    """Tooltip shown to user"""
    bl_idname = "lumi.my_operator"
    bl_label = "My Operator"
    bl_description = "Detailed description"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Implementation
        return {'FINISHED'}
```

**Property Groups:**
```python
class MyProperties(bpy.types.PropertyGroup):
    my_prop: bpy.props.FloatProperty(
        name="My Property",
        description="What this property does",
        default=1.0,
        min=0.0,
        max=10.0
    )
```

---

## 📝 Commit Guidelines

### Commit Message Format

We use **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, missing semicolons, etc.)
- `refactor` - Code refactoring
- `perf` - Performance improvement
- `test` - Adding tests
- `chore` - Maintenance tasks

**Examples:**
```
feat(templates): add golden hour lighting template

Add new template for golden hour outdoor lighting with
warm color temperature and low angle key light.

Closes #123
```

```
fix(linking): resolve error when linking to empty collection

Fixed AttributeError when trying to link lights to collections
with no objects.

Fixes #456
```

```
docs(readme): update installation instructions

Added troubleshooting section for Windows installation
and clarified addon enabling steps.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes:**
   - Test on clean Blender scene
   - Test on complex scene with many objects
   - Test on multiple Blender versions (4.2, 4.3, 4.4)
   - Check for errors in console

2. **Code quality:**
   - Run through your code for obvious issues
   - Remove debug print statements
   - Add logging where appropriate
   - Update docstrings

3. **Documentation:**
   - Update README if needed
   - Update CHANGELOG.md
   - Add code comments for complex logic

### Submitting Pull Request

1. **Push to your fork:**
```bash
git push origin feature/my-awesome-feature
```

2. **Create Pull Request on GitHub:**
   - Clear title describing the change
   - Reference related issues
   - Include screenshots/videos if UI changes
   - Describe testing performed

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested on Blender 4.2
- [ ] Tested on Blender 4.3+
- [ ] Tested in clean scene
- [ ] Tested in complex scene
- [ ] No console errors

## Screenshots
[If applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings/errors
- [ ] Changelog updated
```

### Review Process

1. **Automated checks** run on PR
2. **Maintainer review** - May request changes
3. **Address feedback** - Make requested changes
4. **Approval** - PR approved and merged

---

## 🧪 Testing Guidelines

### Manual Testing Checklist

**For New Features:**
- [ ] Feature works as expected in isolation
- [ ] Feature works with existing features
- [ ] No console errors or warnings
- [ ] Undo/Redo works correctly
- [ ] Works in different viewport shading modes
- [ ] Works with different scene setups

**For Bug Fixes:**
- [ ] Bug is reproducible before fix
- [ ] Bug is fixed after changes
- [ ] Fix doesn't break existing functionality
- [ ] No new console errors

### Test Scenarios

**Basic Tests:**
```
1. Fresh Blender startup → Enable addon → Works?
2. Add light → Modify properties → No errors?
3. Apply template → Lights created correctly?
4. Switch cameras → Light visibility updates?
5. Disable addon → Clean unregistration?
```

**Edge Cases:**
```
1. Empty scene - No objects
2. Large scene - 100+ objects
3. No camera in scene
4. Multiple cameras
5. Complex light linking setups
```

---

## 📖 Documentation

### Code Documentation

**Function Docstrings:**
```python
def calculate_optimal_distance(
    light_type: str,
    target_size: float,
    desired_intensity: float = 1.0
) -> float:
    """Calculate optimal light distance for target illumination.
    
    Uses inverse square law and light type characteristics to
    determine the ideal distance for achieving desired intensity
    on the target surface.
    
    Args:
        light_type: Type of light ('POINT', 'SPOT', 'AREA', 'SUN')
        target_size: Size of target object in meters
        desired_intensity: Target intensity (0.0 to 1.0)
        
    Returns:
        Optimal distance in meters
        
    Note:
        For SUN lights, always returns 0.0 as distance is irrelevant
        
    Example:
        >>> calculate_optimal_distance('POINT', 2.0, 0.8)
        3.5
    """
```

**Class Documentation:**
```python
class SmartLightManager:
    """Manages intelligent light placement and scene analysis.
    
    This class provides methods for analyzing scene geometry,
    calculating optimal light positions, and managing light
    properties based on context.
    
    Attributes:
        lights: List of managed light objects
        scene_bounds: Calculated scene bounding box
        camera: Active camera reference
        
    Example:
        >>> manager = SmartLightManager()
        >>> manager.analyze_scene(context)
        >>> manager.place_key_light(target_object)
    """
```

### User Documentation

When adding features, update:
- README.md - Feature list and usage
- Tooltips - `bl_description` in operators
- Panel labels - Clear, concise text

---

## 🌍 Community

### Getting Help

- **Discord**: [Join our server](https://discord.gg/zqrSFctH5s)
- **GitHub Discussions**: [Ask questions](https://github.com/ProductViz/LumiFlow/discussions)
- **Blender Artists**: Search or post on forum

### Staying Updated

- Watch the repository for notifications
- Join monthly community calls
- Follow development blog (coming soon)

---

## 📜 License

By contributing to LumiFlow, you agree that your contributions will be licensed under the **GPL v3.0** license.

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make LumiFlow better for everyone. Thank you for being part of our community! 🎨✨

---

**Questions?** Contact maintainers:
- GitHub: [@ProductViz](https://github.com/ProductViz)
- Discord: Join our server
- Email: Coming soon

**Happy Contributing!** 🚀
