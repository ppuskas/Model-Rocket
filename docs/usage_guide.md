# ComfyUI Model Manager Usage Guide

## Installation

### Local Installation

1. System Requirements:
   - Python 3.8+
   - Git
   - Internet connection for downloads

2. Setup:
   ```bash
   git clone https://github.com/yourusername/comfyui-model-manager.git
   cd comfyui-model-manager
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

### RunPod Installation

1. In your RunPod environment:
   ```bash
   git clone https://github.com/yourusername/comfyui-model-manager.git
   cd comfyui-model-manager
   pip install -r requirements.txt
   ```

## Using the Manager

### Testing Locally

```bash
# Run in test mode first
python manage.py --scan --setup --download --path ./test_comfyui --test

# Check the results
ls test_comfyui/models/
cat model_scanner.log
```

### Production Usage

```bash
# Full scan and download
python manage.py --scan --setup --download --path /path/to/comfyui

# Scan only
python manage.py --scan

# Setup directories only
python manage.py --setup --path /path/to/comfyui

# Download only
python manage.py --download --path /path/to/comfyui
```

## Directory Structure

The manager creates and maintains the following structure:

```
ComfyUI/
├── models/
│   ├── checkpoints/  # Base model checkpoints
│   ├── clip/         # CLIP models
│   ├── clip_vision/  # CLIP vision models
│   └── ...
└── custom_nodes/
    ├── ComfyUI-AnimateDiff-Evolved/
    └── ComfyUI_IPAdapter_plus/
```

## Error Handling

1. If downloads fail:
   - Check model_scanner.log
   - Verify internet connection
   - Try running with --download flag only

2. If directories exist:
   - The tool safely skips existing directories
   - Use --setup flag to verify structure

3. Common issues:
   - Permission denied: Run with appropriate permissions
   - Space issues: Ensure sufficient disk space
   - Network timeouts: Check connection, retry download