# QMD Backend Reference (OpenClaw Docs Excerpt)

**Source:** https://docs.openclaw.ai/concepts/memory  
**Last fetched:** 2026-02-19  
**Section:** QMD backend (experimental)

---

## QMD backend (experimental)

Set `memory.backend = "qmd"` to swap the built-in SQLite indexer for QMD: a local-first search sidecar that combines BM25 + vectors + reranking. Markdown stays the source of truth; OpenClaw shells out to QMD for retrieval.

### Prereqs

- Disabled by default. Opt in per-config (`memory.backend = "qmd"`).
- Install the QMD CLI separately (`bun install -g @tobilu/qmd` or grab a release) and make sure the `qmd` binary is on the gateway’s PATH.
- QMD needs an SQLite build that allows extensions (`brew install sqlite` on macOS).
- QMD runs fully locally via Bun + node-llama-cpp and auto-downloads GGUF models from HuggingFace on first use (no separate Ollama daemon required).
- The gateway runs QMD in a self-contained XDG home under `~/.openclaw/agents/<agentId>/qmd/` by setting `XDG_CONFIG_HOME` and `XDG_CACHE_HOME`.
- OS support: macOS and Linux work out of the box once Bun + SQLite are installed. Windows is best supported via WSL2.

### How the sidecar runs

1. The gateway writes a self-contained QMD home under `~/.openclaw/agents/<agentId>/qmd/` (config + cache + sqlite DB).
2. Collections are created via `qmd collection add` from `memory.qmd.paths` (plus default workspace memory files), then `qmd update + qmd embed` run on boot and on a configurable interval (`memory.qmd.update.interval`, default 5 m).
3. The gateway now initializes the QMD manager on startup, so periodic update timers are armed even before the first `memory_search` call.
4. Boot refresh now runs in the background by default so chat startup is not blocked; set `memory.qmd.update.waitForBootSync = true` to keep the previous blocking behavior.
5. Searches run via `memory.qmd.searchMode` (default `qmd search --json`; also supports `vsearch` and `query`). If the selected mode rejects flags on your QMD build, OpenClaw retries with `qmd query`.
6. If QMD fails or the binary is missing, OpenClaw automatically falls back to the builtin SQLite manager so memory tools keep working.

### Config surface (`memory.qmd.*`)

| Field | Default | Description |
|-------|---------|-------------|
| `command` | `"qmd"` | Override the executable path |
| `searchMode` | `"search"` | Pick which QMD command backs `memory_search` (`search`, `vsearch`, `query`) |
| `includeDefaultMemory` | `true` | Auto-index `MEMORY.md` + `memory/**/*.md` |
| `paths[]` | — | Add extra directories/files (path, optional pattern, optional stable name) |
| `sessions` | — | Opt into session JSONL indexing (`enabled`, `retentionDays`, `exportDir`) |
| `update` | — | Controls refresh cadence (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`, `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`) |
| `limits` | — | Clamp recall payload (`maxResults`, `maxSnippetChars`, `maxInjectedChars`, `timeoutMs`) |
| `scope` | — | Same schema as `session.sendPolicy` (default: DM-only) |

### Example config

```json
{
  "memory": {
    "backend": "qmd",
    "citations": "auto",
    "qmd": {
      "includeDefaultMemory": true,
      "paths": [
        { "name": "docs", "path": "~/notes", "pattern": "**/*.md" }
      ],
      "update": { "interval": "5m", "debounceMs": 15000 },
      "limits": { "maxResults": 6, "timeoutMs": 4000 },
      "scope": {
        "default": "deny",
        "rules": [
          { "action": "allow", "match": { "chatType": "direct" } },
          { "action": "deny", "match": { "keyPrefix": "discord:channel:" } },
          { "action": "deny", "match": { "rawKeyPrefix": "agent:main:discord:" } }
        ]
      }
    }
  }
}
```

### Citations & fallback

- `memory.citations` applies regardless of backend (`auto`/`on`/`off`).
- When QMD runs, `status().backend = "qmd"` so diagnostics show which engine served the results.
- If the QMD subprocess exits or JSON output can’t be parsed, OpenClaw logs a warning and returns the builtin provider (existing Markdown embeddings) until QMD recovers.

### Manual index warm-up

```bash
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"

qmd update
qmd embed
qmd query "test" -c memory-root --json >/dev/null 2>&1
```

---

*End of excerpt. For full docs see https://docs.openclaw.ai/concepts/memory.*
