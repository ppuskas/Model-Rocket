from flask import Flask, render_template, request, jsonify
import asyncio
import sys
from pathlib import Path
import os
import json

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from manage import main as manage_main

app = Flask(__name__)

def load_model_database():
    """Load default model database with hardcoded models"""
    return {
        "IP-Adapter Models": [
            {
                "name": "IP-Adapter SDXL Base",
                "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl_vit-h.safetensors",
                "type": "ipadapter",
                "size": "402MB",
                "required": False
            },
            {
                "name": "IP-Adapter Plus SDXL",
                "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors",
                "type": "ipadapter",
                "size": "402MB",
                "required": False
            },
            {
                "name": "IP-Adapter Plus Face SDXL",
                "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors",
                "type": "ipadapter",
                "size": "402MB",
                "required": False
            }
        ],
        "ControlNet Models": [
            {
                "name": "ControlNet SDXL Canny",
                "url": "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-canny-rank256.safetensors",
                "type": "controlnet",
                "size": "1.5GB",
                "required": False
            },
            {
                "name": "ControlNet SDXL Depth",
                "url": "https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-depth-rank256.safetensors",
                "type": "controlnet",
                "size": "1.5GB",
                "required": False
            }
        ],
        "AnimateDiff Models": [
            {
                "name": "AnimateDiff SDXL",
                "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.safetensors",
                "type": "motion_module",
                "size": "1.62GB",
                "required": False
            },
            {
                "name": "AnimateDiff SD1.5",
                "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15.safetensors",
                "type": "motion_module",
                "size": "1.62GB",
                "required": False
            },
            {
                "name": "Motion LoRA SDXL",
                "url": "https://huggingface.co/guoyww/animatediff/resolve/main/motion_lora_sdxl.safetensors",
                "type": "motion_lora",
                "size": "50MB",
                "required": False
            }
        ]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = False
    summary = None
    model_database = load_model_database()

    if request.method == 'POST':
        test_mode = 'test_mode' in request.form
        selected_models = request.form.getlist('models[]')
        
        # Build command line arguments
        sys.argv = ['manage.py', '--download']
        if selected_models:
            sys.argv.extend(['--models'] + selected_models)
        if test_mode:
            sys.argv.append('--test')

        try:
            # Capture stdout to get the summary
            import io
            import contextlib
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(manage_main())
                loop.close()
            
            summary = output.getvalue()
            message = "Successfully downloaded selected models"
        except Exception as e:
            import traceback
            message = f"Error during download: {str(e)}\n{traceback.format_exc()}"
            error = True

    return render_template('index.html', 
                         message=message, 
                         error=error, 
                         summary=summary,
                         model_database=model_database)

@app.route('/test')
def test_page():
    """Test route with minimal model database"""
    test_database = {
        "Test Models": [
            {
                "name": "Test Model 1",
                "url": "https://test.com/model1.safetensors",
                "type": "test",
                "size": "1KB",
                "required": False
            },
            {
                "name": "Test Model 2", 
                "url": "https://test.com/model2.safetensors",
                "type": "test",
                "size": "1KB",
                "required": True
            }
        ]
    }
    return render_template('index.html', 
                         model_database=test_database,
                         message="Test Mode Active",
                         error=False,
                         summary=None)

if __name__ == '__main__':
    app.run(debug=True)
