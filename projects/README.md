# 🚀 Projekty Otíka

Složka pro experimentální projekty a side-projecty.

## Aktivní Projekty

### 🛒 [sales-api](./sales-api/) - Databáze akčních produktů
**Status:** 📋 Planning → WIP

API služba pro sledování a vyhledávání akčních cen z českých obchodů (Lidl, Penny, Billa, Kaufland).

**Tech:** FastAPI/Cloudflare Workers, SQLite/D1, APScheduler  
**Features:** Fuzzy search, price history, REST API, automatické scrapování  
**Docs:** [PLAN.md](./sales-api/PLAN.md), [CLOUDFLARE.md](./sales-api/CLOUDFLARE.md)

---

### ☁️ [otik-cloudflare](./otik-cloudflare/) - Edge Agent
**Status:** 💡 Concept

Lightweight verze Otíka běžící globálně na Cloudflare Workers s možností proxy na lokální OpenClaw pro složité úkoly.

**Tech:** Cloudflare Workers, Workers AI, Tailscale tunnel  
**Architecture:** Hybrid (edge + local)  
**Docs:** [CONCEPT.md](./otik-cloudflare/CONCEPT.md)

---

## Struktura

```
projects/
├── sales-api/          # Produkty v akci (API služba)
├── otik-cloudflare/    # Edge agent (distributed AI)
└── README.md           # This file
```

## Pravidla

- **Samostatné projekty** - každý má vlastní dependencies, git může být separátní
- **Dokumentace first** - PLAN.md/CONCEPT.md před implementací
- **Incrementální** - rozvíjet postupně během heartbeatů
- **Experimentální** - OK nehotové projekty, WIP, proof-of-concepts

---

**Workspace:** `/Users/otto/.openclaw/workspace/projects/`  
**Autor:** Otík 🦉
