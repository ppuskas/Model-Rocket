# ComfyUI Model Directory Structure

## Base ComfyUI Structure
```
ComfyUI/
└── models/
    ├── checkpoints/        # Base model checkpoints
    ├── clip/              # CLIP models
    ├── clip_vision/       # CLIP vision models
    ├── configs/           # Model configurations
    ├── controlnet/        # ControlNet models
    ├── diffusers/         # Diffusers format models
    ├── embeddings/        # Textual inversion embeddings
    ├── ipadapter/         # Basic IP-Adapter models
    ├── loras/            # LoRA models
    ├── style_models/      # CLIP vision style models
    ├── unet/              # UNet models
    └── vae/               # VAE models
```

## Custom Node Requirements

### AnimateDiff-Evolved
Required Structure:
```
ComfyUI/
└── custom_nodes/
    └── ComfyUI-AnimateDiff-Evolved/
        └── models/
            ├── motion-module/      # Motion modules
            ├── motion-lora/        # Motion LoRAs
            └── mm_sd15_v2.yaml    # Config file
```

Setup Instructions:
1. Create AnimateDiff directories:
```bash
mkdir -p ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module
mkdir -p ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-lora
```
2. Download and place the mm_sd15_v2.yaml config file

### IPAdapter-Plus
Required Structure:
```
ComfyUI/
└── custom_nodes/
    └── ComfyUI_IPAdapter_plus/
        └── models/
            ├── ip-adapter/        # IPAdapter models
            ├── ip-adapter-plus/   # Plus models
            └── ip-adapter-full/   # Full models
```

Setup Instructions:
1. Create IPAdapter directories:
```bash
mkdir -p ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter
mkdir -p ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus
mkdir -p ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-full
```

## Directory Setup Script
Add this to the frontend for initial setup:

```python
def setup_directories():
    base_dirs = [
        "models/checkpoints",
        "models/clip",
        "models/clip_vision",
        "models/configs",
        "models/controlnet",
        "models/diffusers",
        "models/embeddings",
        "models/ipadapter",
        "models/loras",
        "models/style_models",
        "models/unet",
        "models/vae"
    ]
    
    custom_dirs = [
        "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module",
        "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-lora",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-full"
    ]
    
    # Create all directories
    for dir_path in base_dirs + custom_dirs:
        full_path = os.path.join(COMFYUI_PATH, dir_path)
        os.makedirs(full_path, exist_ok=True)
