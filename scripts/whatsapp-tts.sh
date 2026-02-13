#!/bin/bash
# whatsapp-tts.sh — Send TTS reply to WhatsApp via OpenClaw
# Usage: whatsapp-tts.sh "text"

set -e

TEXT="$1"
if [ -z "$TEXT" ]; then
    echo "Usage: whatsapp-tts.sh \"text\""
    exit 1
fi

# Generate TTS file using Qwen3-TTS wrapper
OUTPUT=$(/Users/otto/.openclaw/workspace/scripts/tts-qwen3.sh "$TEXT" | grep "^MEDIA:" | cut -d: -f2-)

if [ -z "$OUTPUT" ] || [ ! -f "$OUTPUT" ]; then
    echo "Error: Failed to generate TTS" >&2
    exit 1
fi

# Send via OpenClaw message tool (WhatsApp channel)
echo "Sending to WhatsApp: $OUTPUT"
# Note: This must be called from OpenClaw context via sessions_send or similar
# For direct execution, use: openclaw sessions_send <key> "MEDIA:$OUTPUT"

echo "TTS file ready: $OUTPUT"
