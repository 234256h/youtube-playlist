#!/bin/bash
# Example workflow: Download from Zoom and Upload to Google Drive
# This script demonstrates how to chain both operations

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Zoom to Google Drive Workflow ===${NC}\n"

# Check if URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <zoom-recording-url> [google-drive-folder-name]"
    echo ""
    echo "Example:"
    echo "  $0 'https://zoom.us/rec/share/xxxxx' 'My Recordings'"
    echo ""
    exit 1
fi

ZOOM_URL="$1"
DRIVE_FOLDER="${2:-Zoom Recordings}"

# Step 1: Download from Zoom
echo -e "${GREEN}Step 1: Downloading from Zoom...${NC}"
python download_zoom_recordings.py "$ZOOM_URL"

if [ $? -ne 0 ]; then
    echo "❌ Download failed. Exiting."
    exit 1
fi

# Step 2: Find the most recently created folder in downloads/
echo -e "\n${GREEN}Step 2: Finding downloaded files...${NC}"
LATEST_FOLDER=$(ls -td downloads/*/ | head -1)

if [ -z "$LATEST_FOLDER" ]; then
    echo "❌ No downloaded folders found. Exiting."
    exit 1
fi

echo "Found: $LATEST_FOLDER"

# Step 3: Upload to Google Drive
echo -e "\n${GREEN}Step 3: Uploading to Google Drive...${NC}"
python upload_to_google_drive.py "$LATEST_FOLDER" --drive-folder "$DRIVE_FOLDER"

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Complete! Files downloaded and uploaded successfully.${NC}"
else
    echo -e "\n❌ Upload failed."
    exit 1
fi

