# Otto Setup 🦉

**Otto Setup Guide** 🦉  
Záloha nastavení a návod k obnově pokud něco klesne.  
**Poslední update:** 2026-02-02

## Základní info

* **Mac:** Mac mini M4, 16GB RAM (MacKulna)
* **macOS:** 15.6.0
* **OpenClaw verze:** 2026.2.1
* **Gateway port:** 18789
* **Workspace:** /Users/otto/clawd

## Modely

* **Primary:** Claude Sonnet 4-5 (Anthropic)
* **Fallback:** Qwen 2.5 7B (Ollama - lokální)
* **Ollama endpoint:** http://localhost:11434

## Účty

### Apple ID (Otto)
* Email: otto@honeger.com
* Použití: iMessage

### Apple ID (Petr)
* Email: czech@honeger.com

### WhatsApp
* Číslo: +420731295445
* Self-chat mode: zapnutý

## Instalace

### OpenClaw CLI
```bash
npm install -g openclaw@latest
brew install steipete/tap/imsg
brew install ollama
```

### Ollama Models
```bash
ollama serve &  # Start server
ollama pull qwen2.5:7b
ollama list  # Verify
```

### Permissions
* Full Disk Access
* Screen Recording
* Notifications
* Accessibility

## Obnova

### Gateway nefunguje
```bash
openclaw status
openclaw gateway restart
```

### Ztracená konfigurace
```bash
cp ~/clawd/setup/openclaw.json.backup ~/.openclaw/openclaw.json
openclaw gateway restart
```

### WhatsApp odhlášen
```bash
openclaw configure whatsapp
```

### Ollama nefunguje
```bash
ollama serve &  # Start server
ollama list     # Check models
```

### Rollback na Claude-only (bez Ollama)
```bash
cp ~/clawd/setup/openclaw.json.backup-before-ollama ~/.openclaw/openclaw.json
openclaw gateway restart
```

## Důležité soubory

* `~/.openclaw/openclaw.json` - konfigurace
* `~/clawd/setup/` - zálohy a dokumentace
* `~/clawd/memory/` - vzpomínky
* `~/.ollama/models/` - Ollama modely

## Odkazy

* Docs: https://docs.openclaw.ai
* Discord: https://discord.gg/clawd
* Ollama: https://ollama.com
