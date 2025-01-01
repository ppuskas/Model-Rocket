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
    if os.path.exists("/workspace"):
        assert path == "/workspace/ComfyUI"
    else:
        system = platform.system().lower()
        expected = os.path.expanduser("~/ComfyUI")
        assert path == expected

@pytest.mark.asyncio
async def test_environment_check():
    """Test environment verification"""
    result = await check_environment()
    assert result == True
    assert os.path.exists(get_default_path())
