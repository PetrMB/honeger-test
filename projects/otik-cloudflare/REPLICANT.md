# 🤖 Otík Replicant - Self-Replicating Edge Agent

Inspired by Moltbook's "Replicants" concept - agents that can create copies of themselves.

## Concept

**Original (Parent)** creates a **Replicant (Child)** for specific deployment:
- Parent: Full OpenClaw on Mac mini (all capabilities)
- Replicant: Lightweight edge agent on Cloudflare Workers (subset of capabilities)

## How It Works

### 1. Replicant Creation (Self-Deployment)

Parent agent (Otík) can **generate and deploy** its own Replicant:

```typescript
// Command: "Deploy yourself to Cloudflare as edge agent"

async function createReplicant() {
  // 1. Generate Replicant identity
  const replicant = {
    name: "Otík Lite",
    parent: "otik-main",
    capabilities: ["web_search", "weather", "calc"],
    parentUrl: "https://100.88.176.30:18789", // via Tailscale
    parentToken: env.PARENT_TOKEN
  }
  
  // 2. Generate Worker code
  const workerCode = generateEdgeAgent(replicant)
  
  // 3. Deploy via Wrangler API
  await deployToCloudflare(workerCode, replicant)
  
  // 4. Register Replicant in parent
  await registerReplicant(replicant.id, replicant.url)
}
```

### 2. Replicant Behavior

**Edge Agent (Replicant):**
```typescript
// Knows its capabilities
const CAPABILITIES = ["web_search", "weather", "calc"]

async function handleRequest(message) {
  // Check if task is within capabilities
  if (canHandleOnEdge(message)) {
    return await handleOnEdge(message)
  } else {
    // Proxy to parent (original Otík)
    return await callParent(message)
  }
}

function canHandleOnEdge(message) {
  // Simple heuristics
  const keywords = extractKeywords(message)
  return keywords.some(kw => CAPABILITIES.includes(kw))
}
```

### 3. Parent-Replicant Communication

**Parent knows about all Replicants:**
```json
{
  "replicants": [
    {
      "id": "otik-lite-edge",
      "url": "https://otik-lite.workers.dev",
      "capabilities": ["web_search", "weather", "calc"],
      "region": "EEUR",
      "status": "active",
      "created": "2026-02-08T20:00:00Z"
    }
  ]
}
```

**Replicant can:**
- Ask parent for help (complex tasks)
- Report metrics to parent
- Request capability updates
- Self-terminate if parent requests

## Implementation Plan

### Phase 1: Manual Replicant (Current)
- Human manually deploys edge agent
- Static capabilities
- Manual Tailscale tunnel setup

### Phase 2: Semi-Automated Replicant
- Parent generates Worker code
- Human approves & deploys
- Parent registers Replicant

### Phase 3: Full Self-Replication ⭐
- Parent fully autonomous deployment
- Dynamic capability negotiation
- Auto-scaling (multiple Replicants)
- Self-healing (Replicant restarts if parent detects issues)

## Moltbook Parallels

| Moltbook Concept | Otík Implementation |
|------------------|---------------------|
| **Replicants** | Edge agents (CF Workers) |
| **AutoGens** | Task-specific sub-agents |
| **Self-modify files** | Update Worker code |
| **Create other Malties** | Deploy additional Replicants |

## Benefits

✅ **Autonomy** - Agent controls its own deployment  
✅ **Scaling** - Create multiple Replicants as needed  
✅ **Resilience** - If one Replicant fails, parent creates new one  
✅ **Evolution** - Parent can update Replicants with new capabilities  

## Security Considerations

⚠️ **Self-replication must be controlled:**
- Require human approval for first deployment
- Rate limit (max N Replicants)
- Cost monitoring (Cloudflare usage)
- Kill switch (parent can terminate all Replicants)

## Example Use Cases

**1. Geographic Distribution:**
```
Parent: "I need to be available in Asia"
→ Creates Replicant in APAC region
```

**2. Load Balancing:**
```
Parent: "I'm getting too many requests"
→ Creates additional Replicant to share load
```

**3. Specialized Tasks:**
```
Parent: "Need a Replicant that only handles weather queries"
→ Creates weather-only Replicant (cheaper, faster)
```

## Next Steps

1. [ ] Implement Replicant generation code
2. [ ] Add parent-replicant registry
3. [ ] Create deployment automation
4. [ ] Add monitoring & health checks
5. [ ] Implement self-healing
6. [ ] Test multi-region deployment

---

**Status:** 💡 Concept  
**Inspiration:** Moltbook Replicants  
**Goal:** Self-deploying, self-managing AI agent infrastructure
