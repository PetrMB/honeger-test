# 📋 Otik Kanban — Pracovní board

## 💡 Nápady do budoucna

| # | Nápad | Typ | Stav |
|---|-------|-----|------|
| 1 | iOS/Android App | feature | 📋 Backlog |
| 2 | Smart Home (Philips Hue, 8Sleep, HA) | integrace | 📋 Backlog |
| 3 | Email Automation (Gmail Pub/Sub) | integrace | 📋 Backlog |
| 4 | Apple Music Control | integrace | 📋 Backlog |
| 5 | Divadlo Bot (volné lístky) | feature | 📋 Backlog |
| 6 | Webhooks (external triggers) | integrace | 📋 Backlog |

---

## 🔄 Probíhá

| # | Úkol | Stav | Start |
|---|------|------|-------|
| 1 | Sales API - Databáze akcí | 🟡 WIP | 8.2.2026 |
| 2 | Otík Cloudflare Replicant | 🔬 Research | 8.2.2026 |

### Podrobnosti

#### Sales API
- FastAPI + Cloudflare Workers + D1 Database
- Scraping, fuzzy search, price history
- MVP scaffolding hotovo (api/, models/, scraper/, scripts/)

#### Otík Cloudflare
- Hybrid edge agent: Workers AI + Tailscale tunnel
- Self-replicating pattern (inspirováno Moltbook)

---

## ✅ Hotovo

### 2026-02-20

| # | Úkol | Typ | Datum |
|---|------|-----|-------|
| 1 | Ranní briefing (OpenClaw + Moltbook) | automation | 20.2.2026 |
| 2 | OCR letáky (Penny 3, Lidl 6) | cron | 20.2.2026 |
| 3 | Reminders sync (Coshida, Tampony, Karafa, Tento) | automation | 20.2.2026 |
| 4 | TTS odpovědi na iMessage | integration | 20.2.2026 |

### 2026-02-19

| # | Úkol | Typ | Datum |
|---|------|-----|-------|
| 1 | QMD memory system (Ray Fernando) | research | 19.2.2026 |
| 2 | Daily log created | documentation | 19.2.2026 |
| 3 | Backup fallback (`2026-02-18.md`) | backup | 19.2.2026 |

### 2026-02-17

| # | Úkol | Typ | Datum |
|---|------|-----|-------|
| 1 | Things 3 poznámka (AGENTS.md) | docs | 17.2.2026 |
| 2 | Nákupní sync + OCR letáky | automation | 17.2.2026 |
| 3 | shopping-deals.py + update-reminders.py | scripts | 17.2.2026 |
| 4 | Fuzzy search v reminderech | feature | 17.2.2026 |

### 2026-02-10

| # | Úkol | Typ | Datum |
|---|------|-----|-------|
| 1 | Security audit (Rufio credential stealer) | security | 10.2.2026 |
| 2 | Credentials scoping | security | 10.2.2026 |
| 3 | Kupi.cz archiv | cleanup | 10.2.2026 |
| 4 | Sales API MVP scaffolding | feature | 10.2.2026 |
| 5 | Memory backup cron (23:55) | automation | 10.2.2026 |
| 6 | Nightly Build cron (3:00) | automation | 10.2.2026 |
| 7 | OCR script verification | cron | 10.2.2026 |
| 8 | Kanban board (Markdown) | feature | 10.2.2026 |
| 9 | GitHub Kanban guide | docs | 10.2.2026 |
| 10 | Clean workspace | cleanup | 10.2.2026 |
| 11 | GitHub Projects smazán | cleanup | 10.2.2026 |

### Starší úkoly (z paměti)

- TTS Voice Fix (Zuzana → Jan) — 8.2.
- GitHub Token → Bitwarden — 8.2.
- Qwen 2.5 14B + Model Sync — 8.2.
- X/Twitter Skill — 8.2.
- Moltbook CLAIMED ✅ — 8.2.
- Email Cleanup — 8.2.
- Bitwarden Password Manager — 8.2.
- Model Stack Update (Qwen3-Coder-Next) — 8.2.
- BambuLab Access Codes — 6.2.
- Kanban GitHub Pages — 6.2.
- Voice/TTS Setup — 6.2.
- WhatsApp & iMessage — 5.2.
- Kimi K2.5 Cloud Model — 5.2.
- OpenClaw Restart & Opravy — 4.2.
- Lokální AI modely (Ollama) — 4.2.
- Brave Search API — 4.2.
- Apple Notes & Reminders — 4.2.
- Peekaboo Screen Recording — 4.2.
- BambuLab IP adresy — 4.2.

---

**Last updated:** 2026-02-20 15:53 CET  
**Sync:** Nightly Build (3:00 daily)
