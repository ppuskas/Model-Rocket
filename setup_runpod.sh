#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}ComfyUI Model Manager - RunPod Setup${NC}"
echo "----------------------------------------"

# Check if running in RunPod
if [ ! -d "/workspace" ]; then
    echo -e "${RED}Error: /workspace not found. Are you running this in RunPod?${NC}"
    exit 1
fi

# Check if ComfyUI exists
if [ ! -d "/workspace/ComfyUI" ]; then
    echo -e "${RED}Error: ComfyUI not found in /workspace${NC}"
    echo "Please make sure you're using a ComfyUI template"
    exit 1
fi

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Fix permissions if needed
echo -e "\n${YELLOW}Checking permissions...${NC}"
if [ ! -w "/workspace/ComfyUI" ]; then
    echo "Fixing permissions for /workspace/ComfyUI"
    sudo chown -R $(whoami) /workspace/ComfyUI
fi

# Check disk space
SPACE=$(df -BG /workspace | awk 'NR==2 {print $4}' | sed 's/G//')
if [ $SPACE -lt 10 ]; then
    echo -e "${RED}Warning: Less than 10GB free space available ($SPACE GB)${NC}"
    echo "Some model downloads might fail"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run test mode
echo -e "\n${YELLOW}Running in test mode...${NC}"
python manage.py --scan --setup --download --test

# Check results
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Test run completed successfully!${NC}"
    echo "To run in full mode:"
    echo "python manage.py --scan --setup --download"
else
    echo -e "\n${RED}Test run failed. Check model_scanner.log for details${NC}"
fi