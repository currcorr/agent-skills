---
name: last30days
version: "2.8"
source: https://github.com/mvanhorn/last30days-skill
description: "Research any topic from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web. Surface what people are actually discussing, recommending, betting on, and debating right now."
argument-hint: 'last30 AI video tools, last30 best project management tools'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
user-invocable: true
install: git submodule or copy from mvanhorn/last30days-skill
security-review: 2026-03-04
security-status: approved-with-notes
tags:
  - research
  - reddit
  - x
  - youtube
  - tiktok
  - hackernews
  - trends
  - prompts
---

# last30days

Research ANY topic across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, and the web from the last 30 days. Surfaces real-time discussion, recommendations, trends, and prediction market odds.

## Usage

```
/last30 AI video tools
/last30days best project management tools
/last30days claude code skills --quick
/last30days iran war --deep
```

## Options

| Flag | Description |
|------|-------------|
| `--quick` | Faster, fewer sources (8-12 each) |
| `--deep` | Comprehensive (50-70 Reddit, 40-60 X) |
| `--days=N` | Look back N days instead of 30 |
| `--agent` | Non-interactive mode for agent pipelines |
| `--search=reddit,hn` | Restrict to specific sources |

## Sources

| Source | Auth Required |
|--------|--------------|
| Reddit | OpenAI API key (or Codex login) |
| X/Twitter | xAI API key (recommended) or browser cookies |
| YouTube | yt-dlp (no key needed) |
| TikTok + Instagram | SCRAPECREATORS_API_KEY |
| Hacker News | None (free Algolia API) |
| Polymarket | None (free Gamma API) |
| Web | Brave / Parallel AI / OpenRouter API key |

## Required Env Vars

```bash
OPENAI_API_KEY=...           # Reddit search
XAI_API_KEY=...              # X/Twitter search (preferred over cookies)
BRAVE_API_KEY=...            # Web search (or PARALLEL_API_KEY / OPENROUTER_API_KEY)
SCRAPECREATORS_API_KEY=...   # TikTok + Instagram (100 free credits, then PAYG)
```

## Installation

```bash
# Clone into your skills directory
git clone https://github.com/mvanhorn/last30days-skill ~/.claude/skills/last30days

# Install Python deps
pip install -r ~/.claude/skills/last30days/requirements.txt  # minimal — stdlib only

# Install yt-dlp for YouTube support
brew install yt-dlp

# Configure API keys
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << EOF
OPENAI_API_KEY=your_key
XAI_API_KEY=your_key
BRAVE_API_KEY=your_key
EOF
```

## Security Notes (Reviewed 2026-03-04)

**Status: Approved with notes**

✅ No hidden outbound endpoints — all API calls documented in SKILL.md  
✅ Read-only — no posting, no account modification on any platform  
✅ API keys scoped correctly — each key only goes to its own provider  
✅ No keys written to output files or logs  

⚠️ **Twitter cookie auth** — Can use raw browser cookies (`AUTH_TOKEN` + `CT0`) to call Twitter's unofficial GraphQL API. Violates Twitter ToS. If cookies are exposed, account is accessible until expiry. **Recommendation: use `XAI_API_KEY` instead** — cleaner, ToS-compliant, no cookie exposure risk.  

⚠️ **Prompt injection surface** — Raw social content (Reddit/X/TikTok posts) is surfaced into the AI's context window. Crafted posts could attempt prompt injection. Risk is limited to output text only — skill takes no autonomous actions.

## Output Format

Returns a structured research report:
- **What I learned** — key findings by topic with source citations
- **Stats block** — post counts, engagement metrics, top voices per platform
- **Invitation** — follow-up prompts based on actual research findings

Expert mode persists for the conversation — follow-up questions answered from research without re-running.
