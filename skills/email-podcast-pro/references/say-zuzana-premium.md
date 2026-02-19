# macOS say — Zuzana Premium TTS

## Voice Selection

```bash
# List all voices
say -v '?' | grep -i zuzana

# Zuzana Premium (recommended)
say -v "Zuzana"

# Zuzana Standard (older)
say -v "Zuzana"

# Jan (mužský premium)
say -v "Jan"
```

## Rate Control

```bash
# Slow (150 wpm) — pro dlouhé texty
say -v "Zuzana" -r 150

# Normal (180 wpm)
say -v "Zuzana" -r 180

# Fast (220 wpm)
say -v "Zuzana" -r 220
```

## Output Format

```bash
# MP3 output
say -v "Zuzana" -o "output.mp3" "Text k přečtení"

# WAV output
say -v "Zuzana" -o "output.wav" "Text k přečtení"
```

## File Metadata

```bash
# Add title metadata (if supported)
xattr -w "com.apple.metadata:kMDItemTitle" "Předmět" "output.mp3"
```

## Zuzana Premium Installation

1. Open **System Settings**
2. Go to **Accessibility** → **Spoken Content** → **Manage Voices**
3. Download **Zuzana (Premium)** voice
4. Verify: `say -v '?' | grep Zuzana`

## Comparison

| Voice | Gender | Quality | Recommended Use |
|-------|--------|---------|-----------------|
| Zuzana (Premium) | Ženský | Vysoká | Dlouhé dopisy, články |
| Zuzana (Standard) | Ženský | Střední | Rychlé zprávy |
| Jan (Premium) | Mužský | Vysoká | Formální texty |

## Example

```bash
# Create podcast from text
TEXT="Dobrý den, toto je důležitá zpráva. Prosím přečtěte si ji pozorně."
printf '%s' "$TEXT" | say -v "Zuzana" -r 150 -o "podcast.mp3"
```
