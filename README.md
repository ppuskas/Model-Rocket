# ComfyUI Model Manager

A tool for managing ComfyUI models in both local and RunPod environments. Automates the process of setting up directories, downloading models, and organizing dependencies.

## Quick Start - Local Environment

```bash
# 1. Clone the repository
git clone https://github.com/ppuskas/Model-Rocket.git
cd Model-Rocket

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run test mode (uses minimal downloads)
python3 manage.py --scan --setup --download --test

# 4. Verify setup worked
# On Windows:
dir %USERPROFILE%\ComfyUI\models
type model_scanner.log

# On Linux/Mac:
ls ~/ComfyUI/models/
cat model_scanner.log
```

## Quick Start - RunPod Environment

```bash
# After starting your RunPod instance:

# 1. Clone the repository in your RunPod terminal
cd /workspace
git clone https://github.com/ppuskas/Model-Rocket.git
cd Model-Rocket

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run test mode first (uses minimal downloads)
python3 manage.py --scan --setup --download --test

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
python3 manage.py --scan --setup --download
```

### Individual Steps
```bash
# Just scan repositories
python3 manage.py --scan

# Just create directories
python3 manage.py --setup

# Just download models
python3 manage.py --download
```

## Directory Structure

The following structure will be created in your home directory (or /workspace on RunPod):

```
ComfyUI/
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

### Common Issues

#### Local Environment
1. Permission Issues
   - Ensure you have write permissions in your home directory
   - On Windows, run as administrator if needed
   - On Linux/Mac: `chmod -R u+w ~/ComfyUI`

2. Space Issues
   - Ensure at least 10GB free space
   - Models are downloaded to your home directory

3. Python Environment
   - Use Python 3.8 or higher
   - Consider using a virtual environment

#### RunPod Environment

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
