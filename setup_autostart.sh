#!/bin/bash

# Setup script for Screenshot Renamer Auto-Start
# This script sets up a Launch Agent to automatically run the screenshot renamer

PYTHON_PATH="/Users/weirenlan/miniconda/bin/python"

echo "🚀 Setting up Screenshot Renamer for automatic startup..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the current directory (project root)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Create logs directory
echo "📝 Creating logs directory..."
mkdir -p "$PROJECT_DIR/logs"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Warning: OPENAI_API_KEY environment variable is not set${NC}"
    echo "You'll need to either:"
    echo "  1. Set it in your shell profile (.zshrc or .bash_profile)"
    echo "  2. Edit the plist file with your API key"
    echo ""
fi

# Create the Launch Agent directory if it doesn't exist
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_AGENTS_DIR"

# Generate the plist file with correct paths
PLIST_FILE="$LAUNCH_AGENTS_DIR/com.user.screenshot-renamer.plist"

echo "📄 Creating Launch Agent configuration..."

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.screenshot-renamer</string>
    
    <key>Program</key>
    <string>$PYTHON_PATH</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_PATH</string>
        <string>$PROJECT_DIR/app.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>OPENAI_API_KEY</key>
        <string>${OPENAI_API_KEY:-your-api-key-here}</string>
    </dict>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/logs/screenshot-renamer.log</string>
    
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/logs/screenshot-renamer-error.log</string>
</dict>
</plist>
EOF

echo -e "${GREEN}✅ Launch Agent configuration created at: $PLIST_FILE${NC}"

# Load the Launch Agent
echo "🔄 Loading Launch Agent..."
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Screenshot Renamer is now set to start automatically!${NC}"
else
    echo -e "${RED}❌ Failed to load Launch Agent${NC}"
    exit 1
fi

# Check if it's running
echo "🔍 Checking service status..."
launchctl list | grep screenshot-renamer

echo ""
echo "🎉 Setup complete! Your screenshot renamer will now:"
echo "   • Start automatically when you log in"
echo "   • Restart automatically if it crashes"
echo "   • Log output to: $PROJECT_DIR/logs/"
echo ""
echo "📋 Management commands:"
echo "   • Stop service:    launchctl unload ~/Library/LaunchAgents/com.user.screenshot-renamer.plist"
echo "   • Start service:   launchctl load ~/Library/LaunchAgents/com.user.screenshot-renamer.plist"
echo "   • View logs:       tail -f $PROJECT_DIR/logs/screenshot-renamer.log"
echo "   • View errors:     tail -f $PROJECT_DIR/logs/screenshot-renamer-error.log" 