#!/bin/bash

# Uninstall script for Screenshot Renamer Auto-Start
# This script removes the Launch Agent and stops automatic startup

echo "🗑️  Uninstalling Screenshot Renamer auto-start..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PLIST_FILE="$HOME/Library/LaunchAgents/com.user.screenshot-renamer.plist"

# Check if the plist file exists
if [ ! -f "$PLIST_FILE" ]; then
    echo -e "${RED}❌ Launch Agent not found. Nothing to uninstall.${NC}"
    exit 1
fi

# Unload the Launch Agent
echo "🔄 Stopping and unloading Launch Agent..."
launchctl unload "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Launch Agent unloaded successfully${NC}"
else
    echo -e "${RED}❌ Failed to unload Launch Agent (it might not be running)${NC}"
fi

# Remove the plist file
echo "🗑️  Removing Launch Agent configuration..."
rm "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Launch Agent configuration removed${NC}"
else
    echo -e "${RED}❌ Failed to remove Launch Agent configuration${NC}"
    exit 1
fi

echo ""
echo "🎉 Uninstall complete! Screenshot Renamer will no longer start automatically."
echo "📝 Note: Log files in the 'logs' directory have been preserved."
echo "    You can manually delete them if desired." 