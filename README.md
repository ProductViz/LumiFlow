# LumiFlow
Smart lighting tools for Blender

![LumiFlow Logo](assets/icons/lumiflow_logo.png)

**LumiFlow** is a professional lighting workflow addon for Blender that provides smart placement, intelligent controls, and interactive positioning for lighting setups.

## 🌟 Features

### Smart Lighting System
- **Intelligent Light Placement**: Automatically position lights based on scene analysis
- **Smart Templates**: Pre-built lighting setups for various scenarios (Studio, Cinematic, Environment)
- **Interactive Positioning**: Real-time light manipulation with visual feedback
- **Camera-Aware Lighting**: Lights that adapt to camera positions and angles

### Positioning Tools
- **Highlight Positioning**: Focus lights on specific scene elements
- **Normal Positioning**: Align lights with surface normals
- **Target Positioning**: Point lights precisely at targets
- **Orbit Positioning**: Circular light arrangements around subjects
- **Free Positioning**: Manual placement with smart constraints
- **Flip Operations**: Mirror and rotate light setups quickly

### Template Library
- **Studio & Commercial**: Professional lighting setups for product photography
- **Dramatic & Cinematic**: Mood lighting for film and animation
- **Environment & Realistic**: Natural lighting simulations
- **Utilities & Single Lights**: Quick individual light solutions

### Visual Feedback System
- **Real-time Overlays**: Visual guides for light positioning
- **Light Path Visualization**: See how light travels through the scene
- **Interactive Cursors**: Smart cursor feedback during operations
- **Camera Overlays**: View camera-specific lighting information

### Smart Controls
- **Scroll Wheel Control**: Adjust light properties with mouse wheel
- **Modal Operators**: Context-sensitive tools for different operations
- **Quick Actions**: Rapid light selection and manipulation
- **Batch Operations**: Apply changes to multiple lights simultaneously

## 📋 Requirements

- **Blender**: 4.2+ (Recommended: 4.5+)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Graphics**: OpenGL 3.3 compatible GPU

## 🚀 Installation

### Method 1: Manual Installation
1. Download the latest LumiFlow release (.zip file)
2. Open Blender and go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the downloaded .zip file
4. Enable the addon by checking the box next to "LumiFlow"
5. Save preferences to make it permanent

### Method 2: Development Installation
1. Clone the repository: `git clone https://github.com/lumiflow-org/LumiFlow`
2. In Blender Preferences > Add-ons, click `Install...`
3. Navigate to the cloned folder and select it
4. Enable the addon

## 🎯 Usage

### Getting Started
1. **Enable LumiFlow**: In the 3D View sidebar, find the LumiFlow panel and click "✅ ENABLED"
2. **Choose Assignment Mode**: Select whether lights should be assigned to Scene or Camera
3. **Add Lights**: Use the pie menu (Shift+Q) to add smart lights
4. **Apply Templates**: Choose from pre-built lighting templates
5. **Position Lights**: Use positioning tools for precise placement

### Main Interface
- **Sidebar Panel**: Located in View3D > Sidebar > LumiFlow
- **Pie Menu**: Access with Shift+Q for quick operations
- **Template Browser**: Browse and apply lighting templates
- **Overlay System**: Visual feedback during operations

### Key Shortcuts
- **Shift+Q**: Open smart light pie menu
- **Scroll Wheel**: Adjust light properties (when enabled)
- **ESC**: Cancel current operation
- **G**: Move lights (with smart constraints)
- **R**: Rotate lights (with smart constraints)

## 🏗️ Architecture

### Core Modules
- **`core/`**: Central state management and globals
- **`operators/`**: All Blender operators organized by functionality
  - `positioning/`: Light placement and manipulation
  - `smart_template/`: Template application and management
  - `smart_control/`: Intelligent light controls
  - `linking/`: Light linking and relationships
- **`panels/`**: UI panels and interface elements
- **`menus/`**: Menu system and pie menus
- **`utils/`**: Utility functions and helpers
- **`overlay/`**: Visual feedback and drawing system
- **`templates/`**: Lighting template definitions
- **`assets/`**: Icons, presets, and resources

### Key Components

#### Base Modal System
- `BaseModalOperator`: Foundation for all modal operations
- Smart state management and cleanup
- Error handling and recovery

#### Template System
- Intelligent scene analysis
- Automatic light configuration
- Custom template creation

#### Overlay System
- Real-time visual feedback
- GPU-accelerated drawing
- Customizable appearance

## 🔧 Configuration

### Addon Preferences
Access via `Edit > Preferences > Add-ons > LumiFlow`

#### General Settings
- **Enable Custom Shortcuts**: Allow keymap overrides
- **Show Tips on Startup**: Display helpful tips
- **Show Development Panel**: Enable debugging tools

#### Overlay Customization
- **Font Scale**: Adjust overlay text size (0.3x - 3.0x)
- **Line Spacing**: Control text line spacing
- **Color Themes**: Choose from predefined themes or custom colors

#### Theme Presets
- **Default**: LumiFlow blue/orange theme
- **High Contrast Dark**: For dark environments
- **Light Theme**: For bright workspaces
- **Warm**: Orange/red color scheme
- **Cool**: Blue/cyan color scheme
- **Minimal**: Grayscale theme
- **Neon**: Bright colors for dark environments
- **Custom**: User-defined colors

## 📚 Template Categories

### Studio & Commercial
- Product photography setups
- Portrait lighting configurations
- Commercial lighting arrangements
- Studio environment simulations

### Dramatic & Cinematic
- Film noir lighting
- Horror atmosphere lighting
- Romantic mood lighting
- Action scene lighting
- Documentary style lighting

### Environment & Realistic
- Outdoor daylight simulation
- Golden hour lighting
- Night time illumination
- Weather-based lighting
- Architectural lighting

### Utilities & Single Lights
- Quick rim lights
- Fill light configurations
- Key light setups
- Ambient lighting solutions
- Special effect lighting

## 🛠️ Development

### Project Structure
```
LumiFlow/
├── __init__.py              # Main addon file
├── core/                   # Core functionality
│   ├── state.py           # State management
│   ├── globals.py         # Global variables
│   └── camera_manager.py  # Camera operations
├── operators/             # All operators
│   ├── positioning/       # Light positioning
│   ├── smart_template/    # Template system
│   ├── smart_control/     # Smart controls
│   └── linking/          # Light linking
├── panels/               # UI panels
├── menus/                # Menu system
├── utils/                # Utility functions
├── overlay/              # Visual feedback
├── templates/            # Lighting templates
├── assets/              # Resources
└── docs/                # Documentation
```

### Building from Source
1. Ensure Python 3.10+ and Blender 4.2+ are installed
2. Clone the repository
3. Install in development mode (see Installation section)
4. Enable development panel in preferences
5. Use reload functionality for rapid testing

### Code Style
- Follow PEP 8 guidelines
- Maximum line length: 120 characters
- Use type hints where appropriate
- Include docstrings for all public functions
- Maintain consistent naming conventions

## 🐛 Troubleshooting

### Common Issues

#### Addon Won't Enable
- Check Blender version compatibility (4.2+)
- Ensure no conflicting addons are enabled
- Check Python console for error messages

#### Modal Operators Stuck
- Use the development panel to stop all modals
- Restart Blender if necessary
- Check for running operations in the console

#### Overlays Not Showing
- Verify overlay is enabled in the panel
- Check GPU drivers are up to date
- Ensure viewport shading supports overlays

#### Performance Issues
- Reduce number of lights in complex scenes
- Disable unnecessary overlays
- Use simpler templates for preview

### Debug Mode
Enable development panel in preferences to access:
- Reload addon functionality
- Stop all modal operators
- Debug information display

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following code style guidelines
4. Test thoroughly with different Blender versions
5. Submit a pull request with detailed description

### Development Guidelines
- All code must be compatible with Blender 4.2+
- Include appropriate license headers
- Remove debug statements before submitting
- Update documentation for new features
- Test on multiple platforms if possible

### Reporting Issues
- Use GitHub Issues with appropriate labels
- Include Blender version and operating system
- Provide steps to reproduce bugs
- Include screenshots or error messages when applicable

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ **Commercial Use**: Use in commercial projects
- ✅ **Modification**: Modify the code
- ✅ **Distribution**: Share with others
- ✅ **Private Use**: Use for personal projects
- ❌ **Warranty**: No warranty provided
- ❌ **Liability**: No liability for damages

## 📞 Support

### Community Support
- **GitHub Discussions**: Ask questions and share ideas
- **Blender Artists Forum**: Community thread for discussions
- **Discord Server**: Real-time chat and support

### Professional Support
- **GitHub Sponsors**: Support development financially
- **Custom Development**: Hire for custom features
- **Training**: Personal or group training sessions

### Documentation
- **User Guide**: Detailed usage instructions
- **API Reference**: Technical documentation
- **Video Tutorials**: Step-by-step video guides
- **FAQ**: Common questions and answers

## 🎉 Roadmap

### Version 1.1 (Planned)
- [ ] Enhanced template system
- [ ] More positioning algorithms
- [ ] Performance optimizations
- [ ] Additional overlay options

### Version 1.2 (Future)
- [ ] Light linking system
- [ ] Advanced camera integration
- [ ] Render engine integration
- [ ] Collaborative features

### Version 2.0 (Long-term)
- [ ] Machine learning integration
- [ ] Cloud-based templates
- [ ] Mobile companion app
- [ ] Professional studio tools

## 🙏 Acknowledgments

- **Blender Foundation**: For the amazing Blender software
- **Community Contributors**: For feedback and improvements
- **Beta Testers**: For helping identify bugs and issues
- **Supporters**: For making continued development possible

## 📈 Version History

### v1.0.0 (Current)
- Initial release
- Core smart lighting system
- Template library with 50+ presets
- Interactive positioning tools
- Visual feedback system
- Customizable UI themes

---

**LumiFlow** - Making professional lighting accessible to everyone.

For licensing inquiries: asqa3d@gmail.com

© 2024 Burhanuddin. All rights reserved.
