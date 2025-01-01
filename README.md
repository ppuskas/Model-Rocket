# ComfyUI Model Manager for RunPod

A tool designed specifically for managing ComfyUI models in RunPod environments. Automates the process of setting up directories, downloading models, and organizing dependencies.

## Quick RunPod Start

```bash
# After starting your RunPod instance:

# 1. Clone the repository in your RunPod terminal
cd /workspace
git clone https://github.com/yourusername/comfyui-model-manager.git
cd comfyui-model-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run test mode first (uses minimal downloads)
python manage.py --scan --setup --download --test

# 4. Verify setup worked
ls /workspace/ComfyUI/models/
cat model_scanner.log
```

## Features

- 🚀 Optimized for RunPod environments
- 📂 Automatic directory structure creation
- ⬇️ Model downloading with progress tracking
- ✅ Test mode for verification
- 📊 Detailed logging

## RunPod-Specific Setup

### Prerequisites
- RunPod instance with ComfyUI template
- Git installed (included in ComfyUI template)
- Python 3.8+ (included in template)

### Default Paths
The tool is configured for RunPod's default paths:
```
/workspace/ComfyUI/         # Base ComfyUI directory
/workspace/ComfyUI/models/  # Models directory
```

## Usage

### Test Mode
```bash
# Run with test flag for minimal downloads
python manage.py --scan --setup --download --test
```

### Full Mode
```bash
# Run without test flag for full functionality
python manage.py --scan --setup --download
```

### Individual Steps
```bash
# Just scan repositories
python manage.py --scan

# Just create directories
python manage.py --setup

# Just download models
python manage.py --download
```

## Directory Structure

```
/workspace/ComfyUI/
├── models/
│   ├── checkpoints/
│   ├── clip/
│   ├── clip_vision/
│   ├── controlnet/
│   ├── loras/
│   └── vae/
└── custom_nodes/
    ├── ComfyUI-AnimateDiff-Evolved/
    │   └── models/
    │       ├── motion-module/
    │       └── motion-lora/
    └── ComfyUI_IPAdapter_plus/
        └── models/
            ├── ip-adapter/
            └── ip-adapter-plus/
```

## Troubleshooting

### Common RunPod Issues

1. Storage Space
   - Check available space: `df -h`
   - RunPod volumes should have enough space for models

2. Permission Issues
   - Default RunPod user has correct permissions
   - If needed: `sudo chown -R $(whoami) /workspace/ComfyUI`

3. Network Issues
   - RunPod has good connectivity
   - Downloads can be resumed if interrupted

## Logs and Monitoring

- Check `model_scanner.log` for detailed scan info
- Real-time download progress displayed
- Directory creation logged to console

## Contributing

1. Fork the repository
2. Create your feature branch
3. Test changes on RunPod
4. Submit pull request

## License

MIT License - see [LICENSE](LICENSE)