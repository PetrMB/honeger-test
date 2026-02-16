#!/bin/bash
# tts-qwen3.sh — Qwen3-TTS proxy pro OpenClaw s výběrem hlasu
# Usage: tts-qwen3.sh "text" | tts-qwen3.sh -f file.txt
# CONFIG: ~/.config/qwen-tts.json (optional)
# {
#   "voice": "default",           # "default", "male", "female", etc.
#   "language": "cs",             # "cs", "en", "multi"
#   "speed": 1.0                  # 0.5 - 2.0
# }

set -e

# Config
OUTPUT_DIR="/tmp"
OUTPUT_PREFIX="qwen3-tts"
LOG_FILE="/tmp/qwen3-tts.log"
CONFIG_FILE="$HOME/.config/qwen-tts.json"

# Default config
DEFAULT_VOICE="default"
DEFAULT_SPEED="1.0"

# Parse command line
if [ "$1" = "-f" ] && [ -n "$2" ]; then
    TEXT=$(cat "$2")
elif [ -n "$1" ]; then
    TEXT="$1"
else
    echo "Usage: tts-qwen3.sh \"text\""
    echo "       tts-qwen3.sh -f file.txt"
    exit 1
fi

# Load config if exists
if [ -f "$CONFIG_FILE" ]; then
    VOICE=$(jq -r '.voice // "default"' "$CONFIG_FILE" 2>/dev/null || echo "$DEFAULT_VOICE")
    SPEED=$(jq -r '.speed // "1.0"' "$CONFIG_FILE" 2>/dev/null || echo "$DEFAULT_SPEED")
else
    VOICE="$DEFAULT_VOICE"
    SPEED="$DEFAULT_SPEED"
fi

# Generate filename
TIMESTAMP=$(date +%s)
OUTPUT_FILE="${OUTPUT_DIR}/${OUTPUT_PREFIX}-${TIMESTAMP}-${VOICE}.mp3"

# Log
echo "[$(date)] tts-qwen3.sh: voice=$VOICE, speed=$SPEED" >> "$LOG_FILE"

# Try Qwen3-TTS Python wrapper (venv)
VENV_PATH="$HOME/.openclaw/workspace/venv-qwen-tts"
PYTHON_WRAPPER="$HOME/.openclaw/workspace/scripts/tts-qwen3.py"

if [ -f "$VENV_PATH/bin/python3" ] && [ -f "$PYTHON_WRAPPER" ]; then
    echo "[$(date)] tts-qwen3.sh: Using Qwen3-TTS Python wrapper" >> "$LOG_FILE"
    OUTPUT=$("$VENV_PATH/bin/python3" "$PYTHON_WRAPPER" "$TEXT" --model base 2>&1)
    if echo "$OUTPUT" | grep -q "MEDIA:"; then
        echo "$OUTPUT"
        exit 0
    else
        echo "[$(date)] tts-qwen3.sh: Qwen3-TTS failed, fallback to macOS say" >> "$LOG_FILE"
    fi
fi

# Fallback: macOS TTS
MACOS_VOICE="${VOICE:-Zuzana (Premium)}"
echo "[$(date)] tts-qwen3.sh: Using macOS TTS (say -v '$MACOS_VOICE')" >> "$LOG_FILE"
printf "%s" "$TEXT" | say -v "$MACOS_VOICE" -r $(echo "$SPEED * 200" | bc | sed 's/\..*//') -o "$OUTPUT_FILE"

# Output result for OpenClaw
if [ -f "$OUTPUT_FILE" ]; then
    echo "tts-qwen3: Generated $OUTPUT_FILE"
    echo "MEDIA:${OUTPUT_FILE}"
else
    echo "tts-qwen3: ERROR - Failed to generate audio" >&2
    exit 1
fi
