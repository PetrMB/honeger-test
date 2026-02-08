# ☁️ Otík na Cloudflare - Distributed Agent Concept

## Vize

**Lightweight verze Otíka dostupná globálně přes Cloudflare Workers**

Zatímco full-featured OpenClaw běží lokálně na Mac mini (všechny skills, data, Ollama), cloudová verze poskytuje:
- ✅ Rychlý global přístup (edge latence)
- ✅ Základní capabilities (bez citlivých dat)
- ✅ Proxy na lokální OpenClaw pro složité úkoly
- ✅ Inference přímo na edge (Workers AI)

## Architecture Options

### Option A: Hybrid (Recommended) 🌟

```
┌─────────────────────────────────────────────┐
│  Cloudflare Workers Edge                    │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Otík Lite (Edge Agent)              │  │
│  │  - Workers AI inference              │  │
│  │  - Basic skills (web search, calc)   │  │
│  │  - No sensitive data                 │  │
│  └────────────┬─────────────────────────┘  │
│               │                             │
│               │ Complex tasks?              │
│               ▼                             │
│  ┌────────────────────────────┐            │
│  │  Tailscale Tunnel          │            │
│  └────────────┬───────────────┘            │
└───────────────┼─────────────────────────────┘
                │
                │ HTTPS over Tailscale
                ▼
┌────────────────────────────────────────────┐
│  Mac mini (Local)                          │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  OpenClaw Full (Main Agent)          │ │
│  │  - All skills                        │ │
│  │  - Ollama models                     │ │
│  │  - Sensitive data (calendar, email) │ │
│  │  - Apple Reminders, Notes, etc.     │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

**When to use Edge:**
- General Q&A (weather, facts, math)
- Web search
- Simple API calls
- Public data queries

**When to proxy to Local:**
- Personal data (calendar, reminders)
- Skills (Apple Notes, Things, iMessage)
- Large context (memory search)
- Vision models (images)

---

### Option B: Pure Edge (Standalone)

```
┌─────────────────────────────────────────┐
│  Cloudflare Workers                     │
│                                         │
│  ┌────────────────────────────────────┐│
│  │  Otík Lite (Standalone)            ││
│  │  - Workers AI (Llama 3.1 8B)       ││
│  │  - KV storage (memory)             ││
│  │  - Durable Objects (sessions)      ││
│  │  - Limited skills (web only)       ││
│  └────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

**Pros:**
- Zero local dependency
- Always available (no Mac mini downtime)
- Fastest latency

**Cons:**
- No access to local skills
- Limited model capability (8B max)
- Can't access personal data

---

### Option C: Pure Proxy (Gateway)

```
Cloudflare Workers → Tailscale → OpenClaw Gateway
```

Just auth + routing, all inference local.

**Pros:**
- All skills available
- Full model capability
- Simple implementation

**Cons:**
- Depends on local uptime
- Latency (edge → home)
- Exposed via public endpoint

---

## Recommended: Hybrid (Option A)

**Triage logic:**

```typescript
async function handleRequest(message: string, context: Context) {
  // Check if request needs local resources
  const needsLocal = detectLocalNeeds(message)
  
  if (needsLocal) {
    // Proxy to local OpenClaw
    return await proxyToLocal(message, context)
  } else {
    // Handle on edge with Workers AI
    return await handleOnEdge(message, context)
  }
}

function detectLocalNeeds(message: string): boolean {
  const localKeywords = [
    'reminder', 'calendar', 'email', 'imessage',
    'things', 'notes', 'obsidian', 'my files',
    'memory', 'photo', 'screenshot'
  ]
  
  return localKeywords.some(kw => 
    message.toLowerCase().includes(kw)
  )
}
```

## Tech Stack (Cloudflare)

```typescript
Runtime:        Cloudflare Workers
AI:             Workers AI (@cf/meta/llama-3.1-8b-instruct)
State:          Durable Objects (sessions)
Storage:        KV (cache), D1 (structured data)
Routing:        Hono or itty-router
Auth:           Workers Auth or custom JWT
Tunnel:         Tailscale + Cloudflare Tunnel (for local proxy)
```

## Implementation Plan

### Phase 1: Edge-only Agent (MVP)

```typescript
// src/agent.ts
import { Ai } from '@cloudflare/ai'

export async function chat(
  message: string,
  env: Env,
  history: Message[] = []
) {
  const ai = new Ai(env.AI)
  
  const response = await ai.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      { role: 'system', content: EDGE_SYSTEM_PROMPT },
      ...history,
      { role: 'user', content: message }
    ],
    stream: false
  })
  
  return response
}

const EDGE_SYSTEM_PROMPT = `
You are Otík Lite - a lightweight assistant running on Cloudflare edge.

Capabilities:
- General Q&A
- Web search
- Math & calculations
- Public API queries

Limitations:
- No access to personal data
- No calendar, reminders, or notes
- For complex tasks, suggest user contacts main instance

Be concise and helpful within your capabilities.
`
```

### Phase 2: Add Local Proxy

```typescript
// src/proxy.ts
export async function proxyToLocal(
  message: string,
  env: Env
): Promise<Response> {
  const localUrl = env.LOCAL_OPENCLAW_URL // via Tailscale
  const token = env.LOCAL_OPENCLAW_TOKEN
  
  const response = await fetch(`${localUrl}/api/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  })
  
  return response.json()
}
```

### Phase 3: Add Skills (Edge-compatible)

```typescript
// Edge skills (no local dependencies)
const EDGE_SKILLS = {
  'web_search': async (query: string) => {
    // Brave Search API
  },
  'weather': async (location: string) => {
    // Weather API
  },
  'currency': async (from: string, to: string) => {
    // Exchange rates
  },
  'wikipedia': async (query: string) => {
    // Wikipedia API
  }
}
```

## Deployment

### Setup Tailscale Tunnel (for local proxy)

```bash
# On Mac mini
brew install tailscale
sudo tailscale up

# Get Tailscale IP
tailscale ip -4
# → 100.88.176.30

# Expose OpenClaw on Tailscale
# (already running on localhost:18789)
```

### Configure Cloudflare Worker

```toml
# wrangler.toml
name = "otik-lite"
main = "src/index.ts"

[ai]
binding = "AI"

[[kv_namespaces]]
binding = "SESSIONS"
id = "..."

[vars]
LOCAL_OPENCLAW_URL = "https://100.88.176.30:18789"

[secrets]
# wrangler secret put LOCAL_OPENCLAW_TOKEN
```

### Deploy

```bash
wrangler deploy
```

## Cost Estimate

| Service | Free Tier | Monthly Cost |
|---------|-----------|--------------|
| Workers | 100k req/day | Free |
| Workers AI | 10k neurons/day | ~$0-5 |
| KV | 100k reads/day | Free |
| Durable Objects | 10GB-ms/month | ~$0-2 |
| **Total** | | **~$0-10/měsíc** |

## Security Considerations

✅ **No sensitive data on edge** - only in local instance  
✅ **Auth tokens** - Cloudflare secrets  
✅ **Tailscale tunnel** - encrypted, not exposed publicly  
✅ **Rate limiting** - Cloudflare native  
✅ **DDoS protection** - Cloudflare native  

## Use Cases

**Edge Agent (Otík Lite):**
- "What's the weather in Prague?"
- "Convert 100 EUR to CZK"
- "Search for Cloudflare Workers docs"
- "Calculate 15% tip on 450 Kč"

**Proxied to Local:**
- "Add milk to my shopping list" → Apple Reminders
- "What's on my calendar today?" → Calendar
- "Send iMessage to Petr" → iMessage skill
- "Search my notes for X" → Obsidian/Notes

**Hybrid (Edge triage, Local execution):**
- "Remind me to call Petr tomorrow at 9am"
  - Edge: Parse intent
  - Local: Create reminder via Apple Reminders skill

## Future Enhancements

- 🔮 **Voice interface** - Cloudflare Stream + Workers AI voice
- 📱 **Mobile app** - Connect to edge or local based on network
- 🌍 **Multi-region** - Auto-route to closest local instance
- 🤝 **Federation** - Multiple local instances, edge coordinates
- 🧠 **Edge memory** - KV-based lightweight memory (public knowledge only)

---

## Next Steps

1. [ ] Setup Cloudflare Workers account
2. [ ] Create basic edge agent (Llama 3.1 8B)
3. [ ] Test Tailscale tunnel to Mac mini
4. [ ] Implement triage logic (edge vs local)
5. [ ] Add edge-compatible skills
6. [ ] Deploy & test from external network

**Estimated effort:** 3-4 heartbeat sessions  
**Benefit:** Global Otík with local fallback! 🌍🦉
