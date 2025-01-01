import os
import requests
import logging
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

class DownloadManager:
    def __init__(self, base_dir: str, max_retries: int = 3):
        self.base_dir = Path(base_dir)
        self.max_retries = max_retries
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging system"""
        log_dir = self.base_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f'download_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def create_directory(self, dir_type: str) -> Path:
        """Create and return directory path"""
        dir_path = self.base_dir / dir_type
        dir_path.mkdir(exist_ok=True)
        logging.info(f"Created/verified directory: {dir_path}")
        return dir_path
        
    def download_file(self, url: str, target_dir: str, filename: Optional[str] = None) -> Optional[Path]:
        """Download file with retry logic"""
        dir_path = self.create_directory(target_dir)
        
        if not filename:
            filename = url.split('/')[-1]
            
        file_path = dir_path / filename
        
        if file_path.exists():
            logging.info(f"File already exists: {file_path}")
            return file_path
            
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                logging.info(f"Successfully downloaded: {url} to {file_path}")
                return file_path
                
            except Exception as e:
                logging.error(f"Download attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt == self.max_retries - 1:
                    logging.error(f"Max retries reached for {url}")
                    return None
                    
        return None
        
    def process_download_list(self, download_list: List[Dict[str, str]]) -> Dict[str, List[str]]:
        """Process a list of downloads with their target directories"""
        results = {
            'success': [],
            'failed': []
        }
        
        for item in download_list:
            url = item['url']
            target_dir = item['directory']
            filename = item.get('filename')
            
            result = self.download_file(url, target_dir, filename)
            
            if result:
                results['success'].append(str(result))
            else:
                results['failed'].append(url)
                
        return results

# Usage Example:
if __name__ == "__main__":
    download_list = [
        {
            'url': 'example_url',
            'directory': 'models',
            'filename': 'custom_name.safetensors'
        }
    ]
    
    manager = DownloadManager('download_root')
    results = manager.process_download_list(download_list)
    print(f"Successful downloads: {len(results['success'])}")
    print(f"Failed downloads: {len(results['failed'])}")