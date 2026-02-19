#!/bin/bash
# qmd-verify.sh — Verify QMD installation & index health
# Author: Otík (for qmd-memory skill)
# Usage: ./qmd-verify.sh

set -e

echo "🔍 QMD installation check..."

# Check if qmd CLI exists
if ! command -v qmd &> /dev/null; then
    echo "❌ qmd CLI not found!"
    echo "   Install with: bun install -g @tobilu/qmd"
    exit 1
fi

echo "✅ qmd CLI: $(qmd --version)"

# Check Bun availability (if Bun installed)
if command -v bun &> /dev/null; then
    echo "✅ Bun: $(bun --version)"
else
    echo "⚠️  Bun not found in PATH (optional—qmd can run on Node too)"
fi

# Check SQLite with extensions (macOS/Linux)
if command -v sqlite3 &> /dev/null; then
    echo "✅ sqlite3: $(sqlite3 --version)"
    
    # Check if extensions are available (macOS)
    if [ "$(uname)" = "Darwin" ]; then
        echo "ℹ️  macOS SQLite detected — ensure installed via 'brew install sqlite'"
    fi
else
    echo "⚠️  sqlite3 not found — QMD may fail (macOS: brew install sqlite)"
fi

# Check QMD cache directory
QMD_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/qmd/models"
if [ -d "$QMD_CACHE" ]; then
    echo "✅ QMD model cache: $QMD_CACHE ($(ls -1 "$QMD_CACHE" 2>/dev/null | wc -l) model(s))"
else
    echo "ℹ️  QMD model cache not yet created (models auto-download on first use)"
fi

# Check if OpenClaw state directory exists
OPENCLAW_STATE="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/main/qmd"
if [ -d "$OPENCLAW_STATE" ]; then
    echo "✅ OpenClaw QMD state: $OPENCLAW_STATE"
else
    echo "ℹ️  OpenClaw QMD state not created yet (will be created after Gateway restart with backend=qmd)"
fi

echo ""
echo "📋 Next steps:"
echo "   1. Add 'memory.backend: qmd' to openclaw.json"
echo "   2. Run 'openclaw gateway restart'"
echo "   3. Test: 'qmd query \"test\" --json' (set XDG dirs first)"

exit 0
