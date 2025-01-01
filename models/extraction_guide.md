# Model Extraction Guide

## Required Model Categories

### Base Models from ComfyUI
- Extract checkpoint links
- Look for VAE models
- Identify any required base models

### AnimateDiff Models
From AnimateDiff-Evolved repo:
- Motion module downloads
- Motion LoRA models
- Specialized checkpoints

### IP Adapter Models
From IPAdapter Plus:
- IP Adapter models
- Required image encoders
- Face/person-specific models

### LCM Models
From the guide:
- LCM specific models
- LoRA files
- Additional checkpoints

## Extraction Process

1. Parse each repository's README.md
2. Check issues for additional model links
3. Review documentation folders
4. Extract from workflow examples
5. Parse HTML content for guides

## Model Data Structure
Create a JSON file with this structure:
```json
{
  "models": [
    {
      "name": "model_name",
      "category": "category_name",
      "download_url": "url",
      "size": "size_in_mb",
      "required": true/false,
      "description": "description",
      "source_repo": "repo_url"
    }
  ]
}
```

## Frontend Development Instructions

### 1. Basic Flask Application
```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

### 2. HTML Template Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>ComfyUI Model Manager</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- Model selection interface -->
    <div id="model-categories">
        <!-- Dynamic content here -->
    </div>
    
    <!-- Download manager -->
    <div id="download-manager">
        <!-- Progress tracking -->
    </div>
</body>
</html>
```

### 3. RunPod Deployment
Configure for RunPod environment:
- Port mapping: 3000:3000
- Volume mounting for model storage
- Environment variables for paths

### 4. API Endpoints to Implement
```python
@app.route('/api/models', methods=['GET'])
def get_models():
    # Return model list

@app.route('/api/download', methods=['POST'])
def download_model():
    # Handle model download

@app.route('/api/status', methods=['GET'])
def get_status():
    # Return download status
```

## Next Steps
1. Extract all model links
2. Create model database
3. Implement frontend
4. Add download management
5. Test in RunPod environment