#!/bin/bash
# Script pro přidání mediaPath do OpenClaw configu pro bezpečné ukládání TTS souborů

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# Přidání mediaPath do agents.defaults
jq '.agents.defaults.mediaPath = "/Users/otto/.openclaw/workspace/tts-media"' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

# Vytvoření adresáře pokud neexistuje
mkdir -p "/Users/otto/.openclaw/workspace/tts-media"

echo "mediaPath přidán do configu a adresář vytvořen."
echo "Gateway musí být restartována."
