# RunPod Setup Guide

## Initial Pod Configuration

### Required TCP Ports
When creating your RunPod, expose the following ports:
- `3000` - Model Manager web interface
- `8188` - ComfyUI interface

In RunPod's "Expose TCP Ports" field, enter:
```
3000,8188
```

### Volume Configuration
- Ensure you have sufficient storage allocated (recommended minimum: 100GB)
- Use persistent storage if you want to keep the models between sessions

### Template
- Use the official ComfyUI template if available
- Or use a template with Python 3.8+ and Git installed

## Post-Deployment Setup

1. Open terminal in RunPod
2. Clone and set up the manager:
```bash
cd /workspace
git clone https://github.com/yourusername/comfyui-model-manager.git
cd comfyui-model-manager
chmod +x setup_runpod.sh
./setup_runpod.sh
```

## Accessing Interfaces
After setup:
- Model Manager: `http://[your-pod-ip]:3000`
- ComfyUI: `http://[your-pod-ip]:8188`

## Troubleshooting Network Issues
If you can't connect:
1. Verify ports are correctly exposed in Pod settings
2. Check RunPod's networking status
3. Try accessing via direct IP rather than hostname
4. Ensure no firewall is blocking the ports