# ☁️ Otík Cloudflare - Edge Agent

**Lightweight verze Otíka běžící globálně na Cloudflare Workers**

## Status: 💡 Concept

Distributed AI agent architecture:
- **Edge (Cloudflare):** Fast, global, basic capabilities
- **Local (Mac mini):** Full features, all skills, personal data
- **Hybrid:** Smart routing between edge and local

## Why?

✅ **Global availability** - edge latency po celém světě  
✅ **Always online** - i když je Mac mini vypnutý  
✅ **Privacy first** - citlivá data zůstávají lokálně  
✅ **Cost effective** - free tier Cloudflare Workers  
✅ **Scalable** - auto-scales globally  

## Architecture

```
User → Cloudflare Workers (Edge)
         ├─ Simple task → Workers AI (Llama 3.1 8B)
         └─ Complex task → Tailscale → Local OpenClaw
```

## Capabilities

### Edge Agent (Otík Lite)
- General Q&A
- Web search
- Weather, currency, calculations
- Public APIs
- No personal data

### Local OpenClaw (Full Otík)
- All skills (Apple Notes, Reminders, iMessage, ...)
- Personal data (calendar, email, notes)
- Ollama models (larger, custom)
- File system access
- Vision models

## Tech Stack

- **Runtime:** Cloudflare Workers (V8 isolates)
- **AI:** Workers AI (Llama 3.1 8B)
- **State:** Durable Objects (sessions)
- **Storage:** KV (cache), D1 (data)
- **Tunnel:** Tailscale (secure local proxy)
- **Framework:** Hono (TypeScript)

## Cost

**Free tier likely sufficient:**
- Workers: 100k req/day
- Workers AI: 10k neurons/day
- KV/D1: 100k reads/day

→ Estimated: $0-10/měsíc

## Next Steps

1. Setup Cloudflare Workers account
2. Implement basic edge agent
3. Configure Tailscale tunnel
4. Add triage logic (edge vs local)
5. Deploy & test

## Links

- 📋 **[CONCEPT.md](./CONCEPT.md)** - Detailní architektura a plán
- 🏠 **Local OpenClaw:** `~/.openclaw/`
- 🌐 **Cloudflare Docs:** https://developers.cloudflare.com/workers/

---

**Autor:** Otík 🦉  
**Vytvořeno:** 2026-02-08  
**Inspirace:** "Mít tvojí kopii v Cloudflare s lokálním modelem"
