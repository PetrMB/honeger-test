#!/bin/bash
# sync-otto-kanban.sh — Publish updated kanban to otto.honeger.com
# Usage: ./sync-otto-kanban.sh

set -e

KANBAN_SRC="/tmp/otta-kanban/index.html"
KANBAN_DEST="otto@otto.honeger.com:/var/www/html/index.html"

if [ ! -f "$KANBAN_SRC" ]; then
    echo "❌ Source file not found: $KANBAN_SRC"
    echo "   Run: git clone https://github.com/PetrMB/otta-kanban.git /tmp/otta-kanban"
    exit 1
fi

echo "✅ Source: $KANBAN_SRC"
echo "➡️  Destination: $KANBAN_DEST"
echo ""

# Dry-run check
echo "🔍 Dry-run upload..."
scp -n -v "$KANBAN_SRC" "$KANBAN_DEST" 2>&1 | grep -v "^debug" || true

echo ""
echo "🚀 Upload? [y/N]"
read -r confirm

if [ "$confirm" != "y" ]; then
    echo "Upload cancelled."
    exit 0
fi

# Actual upload
echo "📤 Uploading..."
scp "$KANBAN_SRC" "$KANBAN_DEST"

echo ""
echo "✅ Kanban published to otto.honeger.com!"
echo "   URL: https://otto.honeger.com/"
