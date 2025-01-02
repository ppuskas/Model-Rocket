import pytest
import os
import platform
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from manage import get_default_path, check_environment

@pytest.mark.asyncio
async def test_get_default_path():
    """Test default path detection"""
    path = get_default_path()
    system = platform.system().lower()
    
    # Test RunPod detection
    if (os.path.exists("/workspace") and 
        system == "linux" and 
        os.environ.get("RUNPOD_POD_ID") is not None):
        assert path == "/workspace/ComfyUI"
        return
        
    # Test Windows detection
    if system == "windows":
        expected = Path(os.path.expanduser("~/ComfyUI"))
        assert Path(path) == expected
        assert ":" in path  # Windows paths have drive letter
        return
        
    # Test Unix-like systems
    assert path.startswith(os.path.expanduser("~"))
    assert path.endswith("ComfyUI")

@pytest.mark.asyncio
async def test_environment_check():
    """Test environment verification"""
    result = await check_environment()
    assert result == True
    assert os.path.exists(get_default_path())
