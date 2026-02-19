# qmd-memory Skill — Query-Driven Memory for OpenClaw

**Status:** `active`  
**Last update:** 2026-02-19  
**Author:** Otík (Ray Fernando’s QMD solution)

---

## 🧠 What is QMD?

QMD (**Q**uery-**M**arkup-**D**ocuments) is a **local-first search sidecar** for OpenClaw agents. It replaces the default SQLite memory backend with a hybrid search engine that combines:

- **BM25** (full-text keyword search)  
- **Vector semantics** (semantic similarity)  
- **Query expansion** (LLM-generated query variations)  
- **LLM re-ranking** (reranker models)  

**Result:** Up to **20× smaller context windows** while better recall (Ray Fernando, "Making OpenClaw Actually Remember Things" YouTube, AuofNgImNhk).

---

## ✅ Requirements

| Requirement | macOS | Linux | Windows |
|-------------|-------|-------|---------|
| **Node.js** | ≥ 22 | ≥ 22 | ≥ 22 |
| **Bun** | ≥ 1.0.0 | ≥ 1.0.0 | ≥ 1.0.0 |
| **SQLite with extensions** | `brew install sqlite` | install from distro | WSL2 recommended |

---

## 📦 Installation

### 1. Install QMD CLI

```bash
bun install -g @tobilu/qmd
# or
npm install -g @tobilu/qmd
```

Verify:

```bash
qmd --version
# → expected: v1.x.x
```

### 2. (macOS) Install SQLite with extensions

```bash
brew install sqlite
```

---

## ⚙️ Configuration

Add this to `openclaw.json` (Gateway config):

```json
{
  "memory": {
    "backend": "qmd",
    "citations": "auto",
    "qmd": {
      "includeDefaultMemory": true,
      "paths": [
        { "name": "memory", "path": "memory", "pattern": "**/*.md" }
      ],
      "update": {
        "interval": "5m",
        "debounceMs": 15000,
        "onBoot": true,
        "waitForBootSync": false
      },
      "limits": {
        "maxResults": 6,
        "timeoutMs": 4000
      },
      "scope": {
        "default": "deny",
        "rules": [
          { "action": "allow", "match": { "chatType": "direct" } }
        ]
      }
    }
  }
}
```

**Restart the Gateway** after editing:

```bash
openclaw gateway restart
```

---

## 🔁 How QMD Works (Pipeline)

```
User query
    ↓
Query expansion (LLM variation ×2)
    ↓
Parallel BM25 + Vector search
    ↓
RRF fusion (k=60, top-rank bonus)
    ↓
Top 30 candidates for re-ranking
    ↓
LLM reranking (yes/no + logprobs)
    ↓
Position-aware blend (75%→60%→40% retrieval weight)
    ↓
Top-K results (injected as snippets)
```

---

## 🧪 Quick Test

### 1. Index your workspace

```bash
# Pick the same XDG dirs as OpenClaw
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"

# Run a one-off embedding update
qmd update
qmd embed
```

### 2. Run a test query

```bash
qmd query "who is Petr Honeger" --json
```

Expected: returns snippet from `MEMORY.md` or workspace files.

---

## 📋 Files Indexed by Default

| Path | Pattern | Description |
|------|---------|-------------|
| `memory/YYYY-MM-DD.md` | `**/*.md` | Daily logs |
| `MEMORY.md` | — | Long-term memory |

Additional paths can be added in `memory.qmd.paths[]`.

---

## ⚙️ Advanced Configuration

### Search Modes

| Command | Mode | When to use |
|---------|------|-------------|
| `qmd search` | BM25 only | Fast keyword search |
| `qmd vsearch` | Vector only | Semantic similarity |
| `qmd query` | Hybrid + rerank | Best quality (default) |

### Context

Add context descriptions to help search understand your documents:

```bash
qmd context add qmd://memory "Personal notes and work context"
```

---

## 🛠️ Troubleshooting

### Gateway says “qmd not found”

- Install CLI: `bun install -g @tobilu/qmd`
- Verify in PATH: `which qmd`

### Gateway says “sqlite-vec unavailable”

- macOS: `brew install sqlite`
- Linux: install `sqlite3` with `libsqlite3-dev` / `sqlite-devel`

### First search is slow

- QMD auto-downloads GGUF models (~2 GB total)
- Cache location: `~/.cache/qmd/models/`
- Subsequent searches are fast (models stay loaded in VRAM)

### Memory search returns no results

- Run `qmd update` to rebuild index
- Check `qmd status` for collection health
- Verify XDG dirs match Gateway config

---

## 📚 References

- **OpenClaw docs:** https://docs.openclaw.ai/concepts/memory (QMD backend)  
- **QMD GitHub:** https://github.com/tobi/qmd  
- **Ray Fernando video:** "Making OpenClaw Actually Remember Things" (AuofNgImNhk)

---

*Skill maintained by Otík — implementing Ray Fernando’s QMD solution for local-first agent memory.*
