# QMD GitHub Repo (Excerpt)

**Source:** https://github.com/tobi/qmd  
**Last fetched:** 2026-02-19  

---

## QMD - Query Markup Documents

An on-device search engine for everything you need to remember. Index your markdown notes, meeting transcripts, documentation, and knowledge bases. Search with keywords or natural language. Ideal for your agentic flows.

QMD combines BM25 full-text search, vector semantic search, and LLM re-ranking—all running locally via node-llama-cpp with GGUF models.

---

## Quick Start

```bash
# Install globally (Node or Bun)
npm install -g @tobilu/qmd
# or
bun install -g @tobilu/qmd

# Or run directly
npx @tobilu/qmd ...
bunx @tobilu/qmd ...

# Create collections for your notes, docs, and meeting transcripts
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings
qmd collection add ~/work/docs --name docs

# Add context to help with search results
qmd context add qmd://notes "Personal notes and ideas"
qmd context add qmd://meetings "Meeting transcripts and notes"
qmd context add qmd://docs "Work documentation"

# Generate embeddings for semantic search
qmd embed

# Search across everything
qmd search "project timeline"        # Fast keyword search
qmd vsearch "how to deploy"         # Semantic search
qmd query "quarterly planning"      # Hybrid + reranking (best quality)
```

---

## Architecture Summary

QMD hybrid pipeline:

1. **Query expansion** — LLM generates 2 alternative queries
2. **Parallel retrieval** — BM25 + Vector search (each query ×2)
3. **RRF fusion** — k=60, top-rank bonus (+0.05/#1, +0.02/#2-3)
4. **Top 30 candidates** re-ranked by LLM
5. **Position-aware blend** — Rank 1-3: 75% retrieval, 4-10: 60%, 11+: 40%
6. **Final results** injected into agent prompt

---

## Requirements

- **Node.js ≥ 22** or **Bun ≥ 1.0.0**
- **macOS:** `brew install sqlite` (for extension support)

### GGUF Models (auto-downloaded)

| Model | Purpose | Size |
|-------|---------|------|
| `embeddinggemma-300M-Q8_0` | Vector embeddings | ~300MB |
| `qwen3-reranker-0.6b-q8_0` | Re-ranking | ~640MB |
| `qmd-query-expansion-1.7B-q4_k_m` | Query expansion | ~1.1GB |

Models cached at `~/.cache/qmd/models/`.

---

## MCP Server (for integration)

QMD exposes an MCP server:

- `qmd_search` — BM25 search (collection filter)
- `qmd_vector_search` — Vector search (collection filter)
- `qmd_deep_search` — Deep search (expand + rerank)
- `qmd_get` — Retrieve document
- `qmd_multi_get` — Multi-doc retrieval
- `qmd_status` — Index health + collections

HTTP transport example:

```bash
qmd mcp --http --port 8181   # foreground
qmd mcp --http --daemon      # background (PID: ~/.cache/qmd/mcp.pid)
```

---

*End of excerpt. For full docs see https://github.com/tobi/qmd.*
