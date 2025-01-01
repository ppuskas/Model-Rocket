# ComfyUI Model Manager for RunPod

A comprehensive model management solution for ComfyUI running on RunPod, handling both base and custom node model requirements.

## Features

- Automated directory structure creation
- Model download management
- Custom node support
- RunPod integration
- Web-based interface

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/comfyui-model-manager.git
cd comfyui-model-manager

# Run setup script
chmod +x setup.sh
./setup.sh

# Set environment variables
export COMFYUI_PATH=/workspace/ComfyUI  # Adjust as needed

# Run the application
python app.py
```

## Directory Structure

The manager handles both base ComfyUI directories and custom node requirements:

### Base Directories
```
models/
├── checkpoints/
├── clip/
├── clip_vision/
└── ... (see docs/directory_structure.md)
```

### Custom Node Directories
```
custom_nodes/
├── ComfyUI-AnimateDiff-Evolved/
└── ComfyUI_IPAdapter_plus/
```

## Documentation

- [Directory Structure](docs/directory_structure.md)
- [Frontend Development](docs/frontend_guide.md)
- [RunPod Integration](docs/runpod_setup.md)

## Supported Custom Nodes

1. [ComfyUI-AnimateDiff-Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved)
2. [ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus)

## Usage in RunPod

1. Set up environment:
```bash
export COMFYUI_PATH=/workspace/ComfyUI
```

2. Create directories:
```bash
python scripts/setup_directories.py
```

3. Access web interface:
```
http://your-runpod-ip:3000
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see [LICENSE](LICENSE)