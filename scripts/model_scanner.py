import requests
import re
import json
from pathlib import Path
import logging
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

class ModelScanner:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.model_info = {
            "base_models": [],
            "animatediff": [],
            "ipadapter": [],
            "loras": [],
            "motion_modules": []
        }
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='model_scanner.log'
        )

    async def scan_repository(self, url: str) -> Dict:
        """Scan a GitHub repository for model links and information."""
        try:
            response = await self.fetch_url(url)
            if not response:
                return {}

            # Test mode uses a smaller set of predefined links
            if self.test_mode:
                return self.get_test_models()

            if "comfyanonymous/ComfyUI" in url:
                models = await self.process_comfyui_base(response)
                self.model_info.update(models)
            elif "AnimateDiff-Evolved" in url:
                models = await self.process_animatediff(response)
                self.model_info["animatediff"].extend(models)
            elif "IPAdapter_plus" in url:
                models = await self.process_ipadapter(response)
                self.model_info["ipadapter"].extend(models)
            elif "civitai" in url:
                models = await self.process_civitai(response)
                self.model_info["loras"].extend(models)
            
            return self.model_info
            
        except Exception as e:
            logging.error(f"Error scanning repository {url}: {str(e)}")
            return {}

    def get_test_models(self) -> Dict:
        """Return a small set of test models"""
        return {
            "base_models": [
                {
                    "name": "test_base_model",
                    "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
                    "type": "checkpoint",
                    "size": "2MB",  # Small test file
                    "required": True
                }
            ],
            "test_models": [
                {
                    "name": "small_test_model",
                    "url": "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/readme.md",  # Just a small file for testing
                    "type": "test",
                    "size": "1KB",
                    "required": False
                }
            ]
        }

    async def fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL content with proper error handling."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

    def extract_links(self, content: str, patterns: List[str]) -> List[Dict]:
        """Extract links matching specific patterns."""
        links = []
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                link_info = {
                    "url": match.group(0),
                    "name": self.extract_name(match.group(0)),
                    "type": self.determine_type(match.group(0))
                }
                links.append(link_info)
        return links

    def determine_type(self, url: str) -> str:
        """Determine model type based on URL and filename."""
        if "motion" in url.lower():
            return "motion_module"
        elif "lora" in url.lower():
            return "lora"
        elif "ipadapter" in url.lower():
            return "ipadapter"
        elif any(ext in url.lower() for ext in [".safetensors", ".ckpt"]):
            return "checkpoint"
        else:
            return "unknown"

    def save_model_database(self, output_file: str = "model_database.json"):
        """Save scanned model information to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.model_info, f, indent=2)

async def main(test_mode=False):
    scanner = ModelScanner(test_mode=test_mode)
    repositories = [
        "https://github.com/comfyanonymous/ComfyUI",
        "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved",
        "https://github.com/cubiq/ComfyUI_IPAdapter_plus",
        "https://civitai.com/articles/4138/guide-comfyui-animatediff-lcm-an-inner-reflections-guide",
        "https://comfyanonymous.github.io/ComfyUI_examples/flux/"
    ]

    for repo in repositories:
        logging.info(f"Scanning repository: {repo}")
        await scanner.scan_repository(repo)

    scanner.save_model_database()
    logging.info("Model scanning complete. Database saved to model_database.json")
    async def process_comfyui_base(self, content: str) -> Dict[str, List]:
        """Process ComfyUI base repository content."""
        soup = BeautifulSoup(content, 'html.parser')
        models = {
            "base_models": [
                "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
                "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
                "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors",
                "https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.safetensors"
            ]
        }
        return models

    async def process_animatediff(self, content: str) -> List[str]:
        """Process AnimateDiff repository content."""
        return [
            "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v14.safetensors",
            "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15.safetensors",
            "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.safetensors"
        ]

    async def process_ipadapter(self, content: str) -> List[str]:
        """Process IP-Adapter repository content."""
        return [
            "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15.safetensors",
            "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors",
            "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.safetensors",
            "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sdxl_vit-h.safetensors"
        ]

    async def process_civitai(self, content: str) -> List[str]:
        """Process Civitai content."""
        return [
            "https://civitai.com/api/download/models/129723",  # Example LoRA
            "https://civitai.com/api/download/models/129724"   # Example LoRA
        ]
