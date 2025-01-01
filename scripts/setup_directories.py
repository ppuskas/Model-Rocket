import os
import sys
from pathlib import Path

def create_directory_structure(base_path):
    """Create the necessary directory structure for ComfyUI models"""
    
    # Base ComfyUI directories
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
    
    # Custom node directories
    custom_dirs = [
        "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module",
        "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-lora",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-full"
    ]
    
    print("Creating directory structure...")
    
    # Create all directories
    for dir_path in base_dirs + custom_dirs:
        full_path = Path(base_path) / dir_path
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {full_path}")
        except Exception as e:
            print(f"Error creating {full_path}: {e}", file=sys.stderr)
            
    print("Directory structure creation complete.")

if __name__ == "__main__":
    base_path = os.getenv("COMFYUI_PATH", "/workspace/ComfyUI")
    create_directory_structure(base_path)