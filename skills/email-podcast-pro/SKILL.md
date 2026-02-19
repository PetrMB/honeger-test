# email-podcast-pro Skill — Emaily na Zuzanu Premium

**Status:** `active`  
**Last update:** 2026-02-19  
**Author:** Otík

---

## 🎙️ Co dělá tento skill?

Stáhne **dlouhé emaily** (více než 500 slov) z imap účtu, vyfiltruje obchodní spam a převádí je na **podcasty** pomocí Zuzany Premium (český ženský hlas).

**Kdo by to měl používat:**
- Lidé, kteří chtějí "poslouchat si poštu" místo čtení
- Lidé s nízkým zrakem nebo oční únavou
- Lidé, kteří chtějí efektivně zpracovat velké množství emailů

---

## ✅ Požadavky

| Komponenta | Popis |
|-----------|-------|
| **himalaya** | IMAP email CLI (`brew install himalaya`) |
| **say** | macOS text-to-speech (standardně dostupné) |
| **ffmpeg** | Konverze audio formátů (`brew install ffmpeg`) |
| **gog** | Google Workspace CLI (volitelné pro uložení do Drive) |

---

## 🛠️ Konfigurace (volitelné)

Vytvoř `~/.config/email-podcast-pro/config.json`:

```json
{
  "filter": {
    "minWords": 500,
    "excludeKeywords": ["sleva", "akce", "kupón", "předplatné", "nabídka", "speciální", "výprodej"],
    "excludeFrom": ["info@", "newsletter@", "noreply@", "auto@"]
  },
  "output": {
    "format": "mp3",
    "bitrate": "128k",
    "voice": "Zuzana",
    "rate": 150,
    "directory": "~/Music/Podcasts/Emaily"
  }
}
```

---

## 🚀 Jak používat

### 1. Základní spuštění (všechny nečtené emaily)

```bash
email-podcast-pro
```

### 2. Konkrétní email

```bash
email-podcast-pro --id <email-id>
```

### 3. Emaily za posledních N dní

```bash
email-podcast-pro --days 3
```

---

## 🧠 Jak funguje filtrování?

### 1. **Délka** (musí splňovat obě podmínky)
- ✅ `> 500 slov` **VOLITELNĚ** (výchozí)
- ✅ `> 3 odstavce`

### 2. **Vyloučení klíčových slov**
- `sleva`, `akce`, `kupón`, `předplatné`, `nabídka`, `speciální`, `výprodej`

### 3. **Vyloučení odesílatelů**
- `info@`, `newsletter@`, `noreply@`, `auto@`

### 4. **Kvalita textu**
- Vyloučí emaily s více než 60% URL odkazů (typické pro spam)
- Vyloučí emaily bez interpunkce (typické pro boty)

---

## 📁 Výstup

Každý podcast dostane:
- **Soubor:** `podcast-${email-id}-${timestamp}.mp3`
- **Názvosloví:** `Podcast od [Jméno] - [Předmět] (email).mp3`
- **Metadata:** ID, Autor,Datum, Předmět (MP3 tags)

---

## 🔄 Cron Job (Automatické spuštění)

```bash
# Každé ráno v 8:00 (kdy spíš spíš)
0 8 * * * cd ~/.openclaw/workspace && ./skills/email-podcast-pro/script/email-to-podcast.sh --auto 2>&1 >> /tmp/email-podcast.log
```

---

## ⚙️ Více informací

### Himalaya pomoc

```bash
# Seznam emailů
himalaya list inbox --limit 10

# Přečíst email
himalaya read <id>

# Vyhledat emaily
himalaya search --from "petr" --subject "důležité"
```

### macOS say parametry

```bash
# Zuzana Premium (ženský, rychlejší)
say -v "Zuzana" -r 150

# Zuzana (ženský, standard)
say -v "Zuzana"

# Jan (mužský, premium)
say -v "Jan" -r 160
```

---

## 🤔 Troubleshooting

| Problém | Řešení |
|---------|--------|
| `himalaya: command not found` | `brew install himalaya` + přihlášení |
| `No Zuzana voice` | Stáhni premium verzi v System Settings → Accessibility → Spoken Content → Manage Voices |
| `No email found` | Zkontroluj `himalaya list inbox` |
| `Audio file empty` | Zkontroluj `say -v "Zuzana" "test"` |

---

## 📚 Reference

- **Himalaya docs:** https://himalaya.dev/docs/
- **macOS say:** `man say`
- **Zuzana Premium:** System Settings → Accessibility → Spoken Content → Manage Voices

---

*Skill maintained by Otík — "poslouchej si poštu, ne čti ji"*
