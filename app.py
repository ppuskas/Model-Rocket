from flask import Flask, render_template, request, jsonify
import asyncio
import sys
from pathlib import Path
import os
import json
from scripts.model_manager import ModelManager

# Global dictionary to track download progress
download_progress = {}

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from manage import main as manage_main

app = Flask(__name__)

def setup_directories():
    """Create necessary directory structure if it doesn't exist"""
    manager = ModelManager()
    manager.create_directory_structure()

def load_model_database():
    """Load model database with SD 1.5 models including Realistic Vision and ControlNet"""
    try:
        with open("model_database.json", 'r') as f:
            db = json.load(f)
            # Flatten the nested structure for template rendering
            flattened_db = {}
            for top_category, subcategories in db.items():
                for subcategory, models in subcategories.items():
                    category_name = f"{top_category} - {subcategory}"
                    flattened_db[category_name] = models
            return flattened_db
    except FileNotFoundError:
        return {
            "SD 1.5 - Base Models": [
                {
                    "name": "SD 1.5",
                    "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors",
                    "type": "checkpoint",
                    "size": "4.27GB",
                    "required": True
                }
            ]
        }

@app.route('/download_progress')
def get_download_progress():
    """Return current download progress for all models"""
    return jsonify(download_progress)

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
    setup_directories()
    app.run(debug=True)
