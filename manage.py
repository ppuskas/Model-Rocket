#!/usr/bin/env python3
import argparse
import asyncio
import os
from pathlib import Path
from scripts.model_scanner import ModelScanner
from scripts.model_manager import ModelManager

import platform

# Default paths
DEFAULT_PATHS = {
    "runpod": "/workspace/ComfyUI",
    "windows": os.path.expanduser("~/ComfyUI"),
    "linux": os.path.expanduser("~/ComfyUI"),
    "darwin": os.path.expanduser("~/ComfyUI")
}

def get_default_path():
    """Get default ComfyUI path based on environment"""
    if os.path.exists("/workspace"):
        return DEFAULT_PATHS["runpod"]
    return DEFAULT_PATHS[platform.system().lower()]

async def check_environment():
    """Verify environment and paths exist"""
    base_path = get_default_path()
    
    if not os.path.exists(base_path):
        print(f"Warning: {base_path} not found. ComfyUI may not be installed.")
        print(f"Creating directory: {base_path}")
        os.makedirs(base_path, exist_ok=True)
    
    return True

async def verify_permissions():
    """Check if we have write permissions in the required directories"""
    base_path = get_default_path()
    test_path = os.path.join(base_path, "models", "test_write")
    try:
        os.makedirs(os.path.dirname(test_path), exist_ok=True)
        with open(test_path, 'w') as f:
            f.write('test')
        os.remove(test_path)
        return True
    except Exception as e:
        print(f"Permission error: {str(e)}")
        print("You might need to run: sudo chown -R $(whoami) /workspace/ComfyUI")
        return False

async def check_disk_space():
    """Verify sufficient disk space"""
    import shutil
    import os
    
    # Use the ComfyUI base path to check disk space
    base_path = get_default_path()
    try:
        _, _, free = shutil.disk_usage(os.path.dirname(base_path))
        free_gb = free // (2**30)
        if free_gb < 10:  # Less than 10GB free
            print(f"Warning: Only {free_gb}GB free space available.")
            print("Some model downloads might fail.")
            return False
        return True
    except FileNotFoundError:
        print(f"Warning: Could not check disk space for {base_path}")
        return True  # Continue anyway

async def main():
    parser = argparse.ArgumentParser(description='ComfyUI Model Manager for RunPod')
    parser.add_argument('--scan', action='store_true', help='Scan repositories for models')
    parser.add_argument('--download', action='store_true', help='Download models')
    parser.add_argument('--setup', action='store_true', help='Create directory structure')
    parser.add_argument('--test', action='store_true', help='Run in test mode with minimal downloads')
    parser.add_argument('--path', default=None, help='Base path for ComfyUI')
    parser.add_argument('--force', action='store_true', help='Skip environment checks')
    
    args = parser.parse_args()

    # Set default path based on environment
    if args.path is None:
        args.path = get_default_path()

    # Environment checks
    if not args.force:
        checks = await asyncio.gather(
            check_environment(),
            verify_permissions(),
            check_disk_space()
        )
        if not all(checks):
            print("\nEnvironment checks failed. Use --force to override.")
            return

    if args.scan:
        print("Starting repository scan...")
        scanner = ModelScanner(test_mode=args.test)
        await scanner.scan_repository("https://github.com/comfyanonymous/ComfyUI")
        db_file = "model_database.json"
        scanner.save_model_database(db_file)
        if os.path.exists(db_file):
            print(f"Scanning complete. Model database saved to {db_file}")
        else:
            print("Warning: Model database file was not created")
    
    if args.download:
        manager = ModelManager(base_path=args.path)
        # Always create directory structure before download
        manager.create_directory_structure()
        await manager.download_models()
        print("Model downloads complete.")

    # Print summary
    print("\nRun Summary:")
    print(f"Base Path: {str(Path(args.path))}")  # Normalize path separators
    print(f"Test Mode: {'Yes' if args.test else 'No'}")
    print(f"Log File: {os.path.abspath('model_scanner.log')}")
    
    if os.path.exists("model_database.json"):
        print(f"Model Database: {os.path.abspath('model_database.json')}")

if __name__ == "__main__":
    asyncio.run(main())
