#!/bin/bash
# Installation script for ClaudeMCP Remote Script
# Automatically detects OS and installs to correct location

set -e

echo "ClaudeMCP Remote Script - Installation"
echo "======================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    INSTALL_DIR="$HOME/Music/Ableton/User Library/Remote Scripts/ClaudeMCP_Remote"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    INSTALL_DIR="$USERPROFILE/Documents/Ableton/User Library/Remote Scripts/ClaudeMCP_Remote"
else
    # Linux (assume similar to macOS structure)
    INSTALL_DIR="$HOME/Music/Ableton/User Library/Remote Scripts/ClaudeMCP_Remote"
fi

echo "Target installation directory:"
echo "$INSTALL_DIR"
echo ""

# Check if Ableton Remote Scripts directory exists
REMOTE_SCRIPTS_DIR="$(dirname "$INSTALL_DIR")"
if [ ! -d "$REMOTE_SCRIPTS_DIR" ]; then
    echo "Error: Ableton Remote Scripts directory not found at:"
    echo "$REMOTE_SCRIPTS_DIR"
    echo ""
    echo "Please ensure Ableton Live is installed and has been run at least once."
    exit 1
fi

# Backup existing installation if present
if [ -d "$INSTALL_DIR" ]; then
    BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Backing up existing installation to:"
    echo "$BACKUP_DIR"
    mv "$INSTALL_DIR" "$BACKUP_DIR"
    echo ""
fi

# Copy files
echo "Installing ClaudeMCP Remote Script..."
cp -r ClaudeMCP_Remote "$INSTALL_DIR"

# Verify installation
if [ -f "$INSTALL_DIR/__init__.py" ] && [ -f "$INSTALL_DIR/liveapi_tools.py" ]; then
    echo ""
    echo "Installation successful!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Ableton Live"
    echo "2. The ClaudeMCP_Remote script will load automatically"
    echo "3. Verify installation with: python3 examples/test_connection.py"
    echo ""
    echo "The Remote Script listens on TCP port 9004"
else
    echo ""
    echo "Installation failed. Please check file permissions."
    exit 1
fi
