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
    """Load model database with Realistic Vision models"""
    try:
        with open("model_database.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Base Models": [
                {
                    "name": "Realistic Vision V5.0",
                    "url": "https://huggingface.co/SG161222/Realistic_Vision_V5.0_noVAE/resolve/main/Realistic_Vision_V5.0.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
                    "required": False
                },
                {
                    "name": "Realistic Vision V4.0",
                    "url": "https://huggingface.co/SG161222/Realistic_Vision_V4.0_noVAE/resolve/main/Realistic_Vision_V4.0.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
                    "required": False
                },
                {
                    "name": "Realistic Vision V3.0",
                    "url": "https://huggingface.co/SG161222/Realistic_Vision_V3.0_VAE/resolve/main/Realistic_Vision_V3.0.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
                    "required": False
                },
                {
                    "name": "Realistic Vision V2.0",
                    "url": "https://huggingface.co/SG161222/Realistic_Vision_V2.0/resolve/main/Realistic_Vision_V2.0.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
                    "required": False
                },
                {
                    "name": "Realistic Vision V1.4",
                    "url": "https://huggingface.co/SG161222/Realistic_Vision_V1.4/resolve/main/Realistic_Vision_V1.4.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
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
