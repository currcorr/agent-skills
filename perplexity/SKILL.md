---
name: perplexity
description: >
  BACKUP web search via the Perplexity MCP server. Use only when the user
  explicitly mentions Perplexity, wants a quick pre-synthesized sourced
  answer, or the host's native web search is unavailable or came up short.
  For generic lookups prefer the host's native WebSearch; for decision-grade
  multi-source research use deep-research; for what people are saying right
  now use last30days. Requires the Perplexity MCP server configured — if
  mcp__perplexity__ tools are absent, fall back to native web search
  instead of attempting.
---

# Perplexity Tools

Backup search path. Routing order for search-type requests:

1. **Host-native WebSearch/WebFetch** — generic lookups, finding docs/pages.
2. **deep-research skill** — anything decision-grade that needs verified,
   cited, multi-source findings.
3. **last30days skill** — current community chatter and trends.
4. **Perplexity (this skill)** — quick conversational sourced answers, or
   when the above are unavailable/insufficient and the MCP is configured.

## Perplexity Search

**When to use:** finding resources/URLs with a synthesized ranking, when
native search results were thin.

**Default parameters (ALWAYS USE):**

```typescript
mcp__perplexity__perplexity_search({
  query: "your search query",
  max_results: 3,           // Default is 10 - too many!
  max_tokens_per_page: 512  // Reduce per-result content
})
```

Increase limits (max_results: 5, max_tokens_per_page: 1024) only if the
user explicitly needs comprehensive results or the initial search found
nothing useful.

## Perplexity Ask

**When to use:** a conversational, citation-backed explanation synthesized
from the web rather than a list of results.

```typescript
mcp__perplexity__perplexity_ask({
  messages: [{ role: "user", content: "Explain how postgres advisory locks work" }]
})
```

## Prohibited Tool

**NEVER use** `mcp__perplexity__perplexity_research` — slow and
token-heavy (30-50k tokens). For deep multi-source research, use the
**deep-research skill** instead.

## Key Points

- Default to limited results — avoid context bloat.
- This is the backup, not the front door: native WebSearch first.
- Deep research = deep-research skill, never perplexity_research.
