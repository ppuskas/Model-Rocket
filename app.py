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
        "Base Models": [
            {
                "name": "SDXL 1.0 Base",
                "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
                "type": "checkpoint",
                "size": "6.46GB",
                "required": True
            },
            {
                "name": "SDXL 1.0 Refiner",
                "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
                "type": "checkpoint",
                "size": "6.46GB",
                "required": False
            }
        ],
        "Motion Modules": [
            {
                "name": "MM SDXL v1.0",
                "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.safetensors",
                "type": "motion_module",
                "size": "1.62GB",
                "required": False
            }
        ],
        "IP-Adapter Models": [
            {
                "name": "IP-Adapter SDXL",
                "url": "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sdxl_vit-h.safetensors",
                "type": "ipadapter",
                "size": "402MB",
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
                asyncio.run(manage_main())
            
            summary = output.getvalue()
            message = f"Successfully completed {action}"
        except Exception as e:
            message = f"Error during {action}: {str(e)}"
            error = True

    return render_template('index.html', 
                         message=message, 
                         error=error, 
                         summary=summary,
                         model_database=model_database)

if __name__ == '__main__':
    app.run(debug=True)
