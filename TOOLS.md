# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Locations

### Home (Mac location)
- **Address:** Pražská 742, Benátky nad Jizerou
- **Use for:** Default home location, routing from home

### Work (Petr's workplace)
- **Name:** Laurin & Klement kampus
- **Address:** Mladá Boleslav
- **Use for:** Work location, lunch/restaurant searches nearby, routing to/from work

### Route Planning
- Home ↔ Work: ~20-25 km via Benátky nad Jizerou → Mladá Boleslav
- For Google Places searches near work, use "Laurin Klement kampus Mladá Boleslav"
- For home area searches, use "Benátky nad Jizerou"

## Text-to-Speech (TTS)

### Voice Wake Say
- **Preferred voice:** Jan (cs_CZ) - Český mužský hlas **PREMIUM** 🌟
- **Kvalita:** Enhanced/Premium verze (stažena z System Settings)
- **Usage:** `printf 'text' | say -v Jan`
- **Rate:** Default (můžeš upravit pomocí `-r <rychlost>`)

### Available Commands
```bash
# Základní použití
printf 'Ahoj Petře!' | say -v Jan

# Rychlejší řeč
printf 'Text' | say -v Jan -r 220

# Pomalejší řeč
printf 'Text' | say -v Jan -r 160
```

## Helper Scripts

### Ollama Model Sync
- **Path:** `~/.openclaw/workspace/scripts/sync-ollama-models.sh`
- **Usage:** `~/.openclaw/workspace/scripts/sync-ollama-models.sh`
- **What it does:** Automatically syncs all local Ollama models to OpenClaw config
- **When to use:** After `ollama pull <model>` or when models get out of sync
- **README:** `~/.openclaw/workspace/scripts/README-sync-ollama.md`

---

Add whatever helps you do your job. This is your cheat sheet.
