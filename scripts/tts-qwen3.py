#!/usr/bin/env python3
"""
tts-qwen3.py — Qwen3-TTS wrapper for OpenClaw
Usage: tts-qwen3.py "text" [--voice ID]
Output: MEDIA:/tmp/qwen3-tts-<timestamp>.mp3
"""

import argparse
import os
import sys
import uuid
from pathlib import Path

# Config
OUTPUT_DIR = "/tmp"
OUTPUT_PREFIX = "qwen3-tts"
CONFIG_FILE = os.path.expanduser("~/.config/qwen-tts.json")
MODELS_DIR = os.path.expanduser("~/.qwen-tts")

# Models
MODELS = {
    "base": {
        "path": os.path.join(MODELS_DIR, "Qwen3-TTS-12Hz-0.6B-Base"),
        "voices": 1,
    },
    "custom": {
        "path": os.path.join(MODELS_DIR, "Qwen3-TTS-12Hz-1.7B-CustomVoice"),
        "voices": 10,  # speakers 0-9
    },
}


def load_config():
    """Load config from ~/.config/qwen-tts.json"""
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"voice": "default", "model": "base"}


def get_speaker_id(voice_name):
    """Map voice name to speaker ID"""
    voices = {
        "default": 0,
        "male": 0,
        "female": 1,
        "child": 2,
        "elderly-male": 3,
        "elderly-female": 4,
    }
    return voices.get(voice_name, 0)


def generate_tts(text, model_name="base", speaker_id=0):
    """Generate TTS using Qwen3-TTS model"""
    try:
        from qwen_tts import TTS
    except ImportError:
        print("ERROR: qwen-tts not installed. Install with: pip install qwen-tts", file=sys.stderr)
        return None
    
    model_path = MODELS.get(model_name, MODELS["base"])["path"]
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}", file=sys.stderr)
        return None
    
    # Initialize TTS
    tts = TTS(model_path=model_path)
    
    # Generate audio
    output_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_PREFIX}-{uuid.uuid4().hex[:8]}-{model_name}-s{speaker_id}.mp3")
    tts.tts_to_file(text=text, speaker_id=speaker_id, file_path=output_path)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Qwen3-TTS wrapper for OpenClaw")
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("-f", "--file", help="Read text from file")
    parser.add_argument("--voice", type=str, default="default", help="Speaker ID or voice name (0, 1, 2, ...)")
    parser.add_argument("--model", type=str, default="base", choices=["base", "custom"], help="Model to use")
    args = parser.parse_args()
    
    # Load text
    if args.file:
        with open(args.file, "r") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Usage: tts-qwen3.py \"text\" [-f file] [--voice ID] [--model base|custom]")
        sys.exit(1)
    
    # Load config (override args)
    config = load_config()
    voice = config.get("voice", args.voice)
    model = config.get("model", args.model)
    
    # Get speaker ID
    speaker_id = get_speaker_id(voice)
    
    # Generate TTS
    output_path = generate_tts(text, model_name=model, speaker_id=speaker_id)
    
    if output_path and os.path.exists(output_path):
        print(f"tts-qwen3: Generated {output_path}")
        print(f"MEDIA:{output_path}")
    else:
        print("ERROR: Failed to generate audio", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
