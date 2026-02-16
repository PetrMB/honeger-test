#!/bin/bash
# test-voices.sh — Generate test audio with different macOS voices
# Output: MP3 128kbps, 44.1kHz (compatible with OpenClaw)

VOICES=(
    "Jan"
    "Zuzana"
    "Zuzana (Premium)"
    "Daniel"
    "Princess"
    "Vicki"
    "Victoria"
)

TEXT="Ahoj Petře! Toto je test různých hlasů v macOS."

for VOICE in "${VOICES[@]}"; do
    echo "Generating: $VOICE"
    # Intermediate AIFF (macOS native)
    AIFF="/tmp/voice-test-$(echo $VOICE | tr ' ' _).aiff"
    # Final MP3
    MP3="/tmp/voice-test-$(echo $VOICE | tr ' ' _).mp3"
    
    say -v "$VOICE" "$TEXT" -o "$AIFF"
    ffmpeg -y -i "$AIFF" -acodec libmp3lame -ab 128k -ar 44100 "$MP3" 2>/dev/null
    rm "$AIFF"
    
    if [ -f "$MP3" ]; then
        echo "MEDIA:${MP3}"
    else
        echo "ERROR: failed to convert $VOICE"
    fi
done
