import os
import json
import asyncio
import aiohttp
import logging
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm

class ModelManager:
    def __init__(self, base_path: str = "/workspace/ComfyUI"):
        self.base_path = Path(base_path)
        self.setup_logging()
        self.load_model_database()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("model_manager.log"),
                logging.StreamHandler()
            ]
        )

    def load_model_database(self):
        """Load model information from JSON database."""
        try:
            with open("model_database.json", 'r') as f:
                self.model_database = json.load(f)
        except FileNotFoundError:
            logging.error("Model database not found. Run model_scanner.py first.")
            self.model_database = {}

    def get_target_directory(self, model_type: str, url: str = None) -> Path:
        """Determine target directory based on model type and optionally URL."""
        type_to_dir = {
            "checkpoint": self.base_path / "models/checkpoints",
            "motion_module": self.base_path / "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module",
            "motion_lora": self.base_path / "custom_nodes/ComfyUI-AnimateDiff-Evolved/motion_lora",
            "motion_loras": self.base_path / "custom_nodes/ComfyUI-AnimateDiff-Evolved/motion_lora",
            "lora": self.base_path / "models/loras", 
            "ipadapter": self.base_path / "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter",
            "vae": self.base_path / "models/vae",
            "controlnet": self.base_path / "models/controlnet",
            "clip": self.base_path / "models/clip",
            "clip_vision": self.base_path / "models/clip_vision"
        }
        
        # Additional type detection from URL if needed
        if model_type == "unknown" and url:
            url_lower = url.lower()
            if "motion-lora" in url_lower or ("motion" in url_lower and "lora" in url_lower):
                model_type = "motion_lora"
            elif "motion" in url_lower:
                model_type = "motion_module"
            elif "controlnet" in url_lower:
                model_type = "controlnet"
            elif "clip" in url_lower and "vision" in url_lower:
                model_type = "clip_vision"
            elif "clip" in url_lower:
                model_type = "clip"
                
        return type_to_dir.get(model_type, self.base_path / "models/other")

    async def download_file(self, url: str, target_path: Path):
        """Download file with progress bar and progress tracking."""
        from app import download_progress
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                total_size = int(response.headers.get('content-length', 0))
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                downloaded = 0
                with open(target_path, 'wb') as f:
                    with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(len(chunk))
                            
                            # Update progress percentage
                            if total_size > 0:
                                progress = int((downloaded / total_size) * 100)
                                download_progress[url] = progress

    async def download_models(self, model_types: List[str] = None, model_urls: List[str] = None, test_mode: bool = False):
        """Download selected model types or specific model URLs."""
        if test_mode:
            logging.info("Running in test mode - simulating downloads")
            test_models = [
                {
                    "name": "Test Model 1",
                    "url": "https://example.com/test1.safetensors",
                    "type": "checkpoint",
                    "size": "1MB"
                },
                {
                    "name": "Test Model 2", 
                    "url": "https://example.com/test2.safetensors",
                    "type": "lora",
                    "size": "1MB"
                }
            ]
            for model in test_models:
                logging.info(f"Test mode: Would download {model['name']} ({model['size']}) to {model['type']} directory")
            return

        if model_urls:
            # Download specific models by URL
            for url in model_urls:
                try:
                    # For direct URLs, determine model type from URL
                    model_type = "unknown"
                    url_lower = url.lower()
                    if "motion" in url_lower:
                        model_type = "motion_module"
                    elif "lora" in url_lower:
                        model_type = "lora"
                    elif "ipadapter" in url_lower:
                        model_type = "ipadapter"
                    elif any(ext in url_lower for ext in [".safetensors", ".ckpt"]):
                        model_type = "checkpoint"
                    
                    target_dir = self.get_target_directory(model_type, url)
                    target_path = target_dir / Path(url).name
                    
                    if target_path.exists():
                        logging.info(f"Skipping existing model: {target_path.name}")
                        continue

                    logging.info(f"Downloading from {url} to {target_path.absolute()}")
                    await self.download_file(url, target_path)
                    logging.info(f"Successfully downloaded {target_path.name}")
                except Exception as e:
                    logging.error(f"Failed to download from {url}: {str(e)}")
            return

        # Handle direct URL downloads
        if model_urls:
            for url in model_urls:
                try:
                    # Determine model type from URL
                    url_lower = url.lower()
                    if "motion" in url_lower and "lora" in url_lower:
                        model_type = "motion_lora"
                    elif "motion" in url_lower:
                        model_type = "motion_module"
                    elif "lora" in url_lower:
                        model_type = "lora"
                    elif "ipadapter" in url_lower:
                        model_type = "ipadapter"
                    elif any(ext in url_lower for ext in [".safetensors", ".ckpt"]):
                        model_type = "checkpoint"
                    else:
                        model_type = "unknown"

                    target_dir = self.get_target_directory(model_type)
                    target_path = target_dir / Path(url).name
                    
                    if target_path.exists():
                        logging.info(f"Skipping existing model: {target_path.name}")
                        continue

                    logging.info(f"Downloading from {url} to {target_path}")
                    await self.download_file(url, target_path)
                    logging.info(f"Successfully downloaded {target_path.name}")
                except Exception as e:
                    logging.error(f"Failed to download from {url}: {str(e)}")
            return

        # Handle model database downloads
        if not model_types:
            model_types = list(self.model_database.keys())
            
        for category, models in self.model_database.items():
            if model_types and category not in model_types:
                continue
            
            for model in models:
                try:
                    target_dir = self.get_target_directory(model['type'])
                    target_path = target_dir / Path(model['url']).name

                    if target_path.exists():
                        logging.info(f"Skipping existing model: {target_path.name}")
                        continue

                    logging.info(f"Downloading {model['name']} to {target_path.absolute()}")
                    await self.download_file(model['url'], target_path)
                    logging.info(f"Successfully downloaded {model['name']}")
                except Exception as e:
                    logging.error(f"Failed to download {model['name']}: {str(e)}")

    def create_directory_structure(self):
        """Create all necessary directories."""
        directories = [
            "models/checkpoints",
            "models/clip",
            "models/clip_vision",
            "models/controlnet",
            "models/vae",
            "models/loras",
            "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module",
            "custom_nodes/ComfyUI-AnimateDiff-Evolved/motion_lora",
            "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter",
            "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus",
        ]

        for dir_path in directories:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {full_path}")

async def main():
    # Initialize manager
    manager = ModelManager()
    
    # Create directory structure
    manager.create_directory_structure()
    
    # Download all models
    await manager.download_models()

if __name__ == "__main__":
    asyncio.run(main())
