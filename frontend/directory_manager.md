# Directory Management for Model Frontend

## Directory Verification Component

```javascript
// Frontend directory verification
class DirectoryManager {
    constructor() {
        this.directories = {
            base: [
                "models/checkpoints",
                "models/clip",
                "models/clip_vision",
                "models/controlnet",
                // ... other base directories
            ],
            animateDiff: [
                "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-module",
                "custom_nodes/ComfyUI-AnimateDiff-Evolved/models/motion-lora"
            ],
            ipAdapter: [
                "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter",
                "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus",
                "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-full"
            ]
        };
    }

    async verifyDirectories() {
        const response = await fetch('/api/verify-directories');
        const status = await response.json();
        this.updateDirectoryStatus(status);
    }

    updateDirectoryStatus(status) {
        // Update UI with directory status
        Object.entries(status).forEach(([dir, exists]) => {
            const element = document.querySelector(`#dir-${dir}`);
            if (element) {
                element.classList.toggle('directory-missing', !exists);
            }
        });
    }
}
```

## Backend API Endpoints

```python
@app.route('/api/verify-directories')
def verify_directories():
    base_path = os.getenv('COMFYUI_PATH', '/workspace/ComfyUI')
    status = {}
    
    # Check all required directories
    for dir_type, dir_list in REQUIRED_DIRECTORIES.items():
        for dir_path in dir_list:
            full_path = os.path.join(base_path, dir_path)
            status[dir_path] = os.path.exists(full_path)
    
    return jsonify(status)

@app.route('/api/create-directories', methods=['POST'])
def create_directories():
    setup_directories()
    return jsonify({"status": "success"})
```

## Directory Status UI

```html
<div class="directory-status">
    <h3>Required Directories</h3>
    <div class="directory-groups">
        <div class="base-directories">
            <h4>Base ComfyUI Directories</h4>
            <!-- Dynamically populated -->
        </div>
        
        <div class="custom-directories">
            <h4>Custom Node Directories</h4>
            <!-- Dynamically populated -->
        </div>
    </div>
    
    <button id="create-directories" onclick="createMissingDirectories()">
        Create Missing Directories
    </button>
</div>
```

## Directory Verification Flow

1. On frontend load:
   - Check directory status
   - Display missing directories
   - Enable/disable download buttons based on directory status

2. Before download:
   - Verify target directory exists
   - Create if missing (with user permission)
   - Proceed with download

3. After custom node installation:
   - Recheck directory structure
   - Create new required directories
   - Update UI status