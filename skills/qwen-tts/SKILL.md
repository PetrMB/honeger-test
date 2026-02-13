---
name: qwen-tts
description: Qwen3-TTS local text-to-speech (wrapper for macOS say with Qwen3-TTS backup).
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["bash"] },
        "install":
          [
            {
              "id": "script",
              "kind": "custom",
              "label": "Qwen3-TTS script",
              "url": "https://github.com/QwenLM/Qwen3-TTS",
            },
          ],
      },
  }
---

# qwen-tts

Use `tts-qwen3` for local Qwen3-TTS with macOS fallback.

## Usage

```bash
# Direct text
tts-qwen3 "Hello there"

# From file
tts-qwen3 -f text.txt
```

## Output

Returns `MEDIA:/tmp/qwen3-tts-<timestamp>.mp3` for OpenClaw.

## Fallback

If Qwen3-TTS server is not running, falls back to macOS built-in TTS (`say -v Jan`).

## Setup

1. Qwen3-TTS wrapper script at `~/.openclaw/workspace/scripts/tts-qwen3.sh`
2. When Qwen3-TTS Ollama integration is available, replace fallback with actual API call
3. Compatible with OpenClaw `tts` tool (MEDIA: output)

## Notes

- Current implementation uses macOS TTS as fallback
- No API key required (fully local)
- Supports voice cloning when Qwen3-TTS is available
