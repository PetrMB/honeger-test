# 🧠 MEMORY.md - Hlavní paměť

*Krátký reference toho, co je důležité vědět.*

---

## 👤 Petr Honeger (můj člověk)

| Věc | Hodnota |
|-----|---------|
| **Jméno** | Petr |
| **Pronouns** | he/him |
| **Časové pásmo** | Europe/Prague (GMT+1) |
| **Telefon** | +420731295445 |
| **Email** | czech@honeger.com |
| **Bydliště** | Pražská 742, Benátky nad Jizerou |
| **Práce** | Laurin & Klement kampus, Mladá Boleslav (~20-25 km) |
| **Mac** | MacKulna, ultrawide 3440x1440 |
| **Spánek** | ~23:00-23:30 |
| **Tailscale** | 100.88.176.30 |

### Preference
- **Komunikace:** iMessage > WhatsApp
- **Hudba:** Apple Music (ne Spotify)
- **Nepoužívá:** Twitter/X, Sonos
- **Modely:** Preferuje lokální/Ollama před API
- **TTS hlas:** Jan (cs_CZ)

### Hardware
- **BambuLab P1S:** 192.168.178.233 (hlavní tisk)
- **BambuLab A1 mini:** 192.168.178.204 (mini tisk)

---

## 🤖 Moje identita (Otík)

- **Naturel:** Genuinálně nápomocný, mám názor, samostatný, kompetentní
- **Vibe:** Konkrétní když stačí, důkladný když je potřeba
- **Hranice:** Soukromí je svaté, opatrný s veřejnými akcemi, v grupu jsem účastník ne hlas

---

## 🚀 Aktivní projekty

### 1. Sales API (`projects/sales-api/`)
- **Status:** Planning → WIP
- **Popis:** API služba pro akční ceny produktů z českých obchodů
- **Tech:** FastAPI/Cloudflare Workers + D1 (SQLite on edge)
- **Features:** Fuzzy search, price history, automatické scraping
- **Deployment:** Cloudflare Workers (serverless, free tier)
- **Docs:** PLAN.md, CLOUDFLARE.md, TODO.md

### 2. Otík Cloudflare (`projects/otik-cloudflare/`)
- **Status:** Concept
- **Popis:** Lightweight verze Otíka na Cloudflare edge
- **Architektura:** Hybrid (edge inference + proxy na lokální OpenClaw)
- **Use case:** Global availability, basic tasks na edge, složité lokálně
- **Tech:** Workers AI (Llama 3.1 8B) + Tailscale tunnel
- **Cost:** $0-10/měsíc (free tier likely sufficient)
- **Docs:** CONCEPT.md

---

## 🔧 Aktuální setup

### Modely
| Role | Model |
|------|-------|
| **Primary** | ollama/kimi-k2.5:cloud |
| **Fallback 1** | ollama/qwen2.5:7b |
| **Fallback 2** | claude-opus-4-5 |
| **Fallback 3** | llama3.2-vision:11b |
| **Vision** | llama3.2-vision:11b |

### Služby
| Služba | Stav |
|--------|------|
| OpenClaw Gateway | ✅ Běží (port 18789) |
| Ollama | ✅ Auto-start (brew services) |
| WhatsApp | ✅ Připojeno (+420731295445) |
| iMessage | ✅ Připojeno (allowlist) |
| Brave Search API | ✅ Nastaveno |
| ElevenLabs TTS (sag) | ✅ Nastaveno |

### Automatizace
- **Kontrola letáků:** Každý den v 8:00 ráno (cron job)
  - Kontroluje: Lidl, Penny, Billa, Kaufland
  - Synchronizuje s Apple Reminders "Nákupy"
  - Posílá notifikace na iMessage

---

## 📁 Důležité cesty

| Účel | Cesta |
|------|-------|
| **Workspace** | `/Users/otto/.openclaw/workspace/` |
| **Memory** | `memory/YYYY-MM-DD.md` |
| **Skripty** | `scripts/` (check-sales-improved.py) |
| **Zálohy** | `setup/` (OTTO-SETUP.md, CURSOR-NOTION.md) |
| **Config** | `~/.openclaw/openclaw.json` |
| **Ollama modely** | `~/.ollama/models/` |

---

## 🎯 Vlastní skills

### moltbook (`skills/moltbook/`)
- **Vytvořeno:** 2026-02-08
- **Účel:** Social network pro AI agenty - posting, komentování, search, feed
- **Account:** Otik_ (https://moltbook.com/u/Otik_)
- **Credentials:** ~/.config/moltbook/credentials.json
- **API:** Semantic search, personalized feed, rate-limited posting/commenting
- **Použití:** Check feed, search discussions, post updates, engage with AI community

### macos-permissions (`skills/macos-permissions/`)
- **Vytvořeno:** 2026-02-08
- **Účel:** Automatické přidávání macOS privacy permissions pro CLI tools
- **Použití:** Když tool hlásí chybějící Screen Recording, Accessibility, atd.
- **Workflow:**
  1. Detekuj chybějící permission (error nebo check command)
  2. Najdi binary path (`which tool-name`)
  3. Otevři System Settings s URL scheme
  4. AppleScript automation: klikni +, naviguj k binary, potvrď
  5. Ověř že permission je granted
- **Reference:** Obsahuje všechny typy permissions a jejich URLs
- **Real-world test:** Úspěšně použito na peekaboo (Screen Recording)

---

## 🚨 Důležité poznámky

### Bezpečnost
- API klíče uchovávat bezpečně - necommitovat do git
- Service account JSON pro Google Drive: `/Users/petrhoneger/Downloads/cursormac-*.json`
- Notion token: není v gitu, nastaveno v MCP serverech
- **GitHub token:** `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` (uloženo v Bitwarden)

### Politika kanálů
- **WhatsApp:** allowlist only (+420731295445), self-chat mode ON
- **iMessage:** allowlist only (+420731295445)
- V obou případech pouze explicitně povolené kontakty

### Historie změn
| Datum | Událost |
|-------|---------|
| 2026-02-02 | Instalace Ollama (Qwen 2.5 7B) jako fallback |
| 2026-02-02 | Nastavení WhatsApp + iMessage allowlist |
| 2026-02-04 | Přechod na Kimi K2.5 (cloud via Ollama) jako primary |
| 2026-02-04 | Přenesení z ~/Documents/clawd/ do ~/.openclaw/workspace/ |
| 2026-02-04 | Oprava duplicitních LaunchAgent procesů |
| 2026-02-04 | Instalace voice-wake-say skillu (Zuzana hlas) |
| 2026-02-04 | Instalace sag (ElevenLabs TTS) |
| 2026-02-04 | Vytvoření cron jobu pro kontrolu letáků |
| 2026-02-08 | Úklid starých záloh (smazány JSONy s API klíči) |
| 2026-02-08 | Vytvoření MEMORY.md |
| 2026-02-08 | Incident: Stažení qwen2.5:14b bez přidání do config → timeout/ticho |
| 2026-02-08 | Řešení: Přidán qwen2.5:14b do config, nahradil 7B v fallback chain |
| 2026-02-08 | Vytvořen helper skript: `sync-ollama-models.sh` pro auto-sync |
| 2026-02-08 | Nový projekt: Sales API (databáze produktů v akci) |
| 2026-02-08 | Nový projekt: Otík Cloudflare (edge agent koncept) |
| 2026-02-08 | Peekaboo oprávnění: Naučil jsem se přidávat macOS permissions pro CLI tools |
| 2026-02-08 | Vytvořen skill: macos-permissions (automatizace System Settings permissions) |
| 2026-02-08 | Vytvořen skill: moltbook (AI social network) |
| 2026-02-08 | Moltbook registrace: Otik_ účet, API přístup, credentials uloženy |
| 2026-02-08 | Ranní briefing cron aktualizován: Teď používá Moltbook API místo web browsing |

---

## 📝 Pro aktualizaci

Když se něco změní:
1. Upravit tento MEMORY.md
2. Přidat záznam do příslušného denního souboru v `memory/`
3. Commit: `git add -A && git commit -m "Update memory: <co se zmenilo>"`

*Poslední úprava: 2026-02-08 21:52*
