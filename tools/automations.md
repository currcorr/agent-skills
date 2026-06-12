# Automations

Recurring agent runs that keep the toolkit healthy. Both recipes end in a
file or a PR — never a send. Run them via the Codex app's scheduled
automations, or cron/Task Scheduler with `codex exec` (or `claude -p`).

## 1. Skills-repo housekeeping (daily)

Pull the clone, validate every skill parses, rebuild the pack artifact if
anything changed.

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --full-auto -C ~/skills "
Run the daily skills housekeeping:
1. git pull --ff-only. If the pull fails, stop and write the error to tools/housekeeping-log.md.
2. For every */SKILL.md, check the YAML frontmatter parses and has name + description. List any failures.
3. If anything changed since the last run, rebuild the pack: python tools/build_ey_pack.py releases/ey-consulting-pack.zip — SKIP this step if this repo was created from the pack zip (there is no pack builder; git is the distribution).
4. Commit and push only the rebuilt zip and the log. Do not edit skills.
" 2>/dev/null
```

Cron: `15 6 * * 1-5` (06:15 weekdays).

## 2. Library digest + promotion proposals (weekly)

Summarize the week's template-library activity and propose rule promotions
as a PR for human review.

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --full-auto -C ~/skills "
Weekly template-library review:
1. git pull --ff-only.
2. From git log over the last 7 days, summarize new rows in ey-deck/library/INDEX.md and EXEMPLARS.md.
3. Check EXEMPLARS.md for any quality cited by 2+ entries or repeatedly referenced in annotations. For each, draft the promotion: a numbered rule for ey-brand-kit/references/design-rules.md or an addition to ey-deck/references/storyline-guide.md.
4. If there are promotions, create a branch, apply the edits, push, and open a PR titled 'Library promotions: <date>' describing each proposed rule and its evidence. Never push rule changes to master directly.
5. Write the digest to ey-deck/library/digest-<date>.md on master.
" 2>/dev/null
```

Cron: `0 7 * * 5` (Friday 07:00).

## 3. Friday "what did I correct" review (weekly)

Scan the week's agent session transcripts for things the user repeatedly
fixed, re-explained, or overrode — then turn those corrections into proposed
permanent improvements (skill edits, AGENTS.md lines, new design rules) as a
PR for human review.

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --full-auto -C ~/skills "
Weekly correction review:
1. git pull --ff-only.
2. Read this week's agent session transcripts. Common locations — adjust to this machine:
   Claude Code: ~/.claude/projects/*/  (JSONL per session, filter by mtime < 7 days)
   Codex: ~/.codex/sessions/ or the app's session export folder.
3. Look for correction signals: the user rephrasing the same instruction twice, 'no, I meant', 'again', manual edits to agent output, the same preference stated in multiple sessions, and skills that triggered wrongly or failed to trigger.
4. For each recurring correction, classify the fix: (a) a skill edit (which SKILL.md, what change), (b) an AGENTS.md trigger line, (c) a new/amended design rule, or (d) not automatable - note it for the user.
5. Apply fixes a-c on a branch, push, and open a PR titled 'Correction review: <date>'. In the PR, describe each correction pattern in general terms ONLY - never quote transcript text, client names, or engagement specifics. The analysis stays local; only the distilled rule change leaves the machine.
6. Write a one-page digest to tools/correction-digest-<date>.md listing patterns found, fixes proposed, and the category-d items needing the user.
" 2>/dev/null
```

Cron: `30 16 * * 5` (Friday 16:30 — end of week, while context is fresh).

Notes:
- Transcripts contain client material. This recipe reads them locally and
  must never copy transcript content into commits, PRs, or digests — only
  generalized patterns ("user repeatedly corrects chart palettes" not the
  chart or the client).
- Expect noise the first few weeks; tune the correction signals in step 3
  to whatever your actual phrasing habits are.

## Guardrails

- Automations draft; humans send. Outputs are files and PRs only.
- Anything that edits design rules or skills goes through a PR (recipe 2),
  so the house style never changes without review.
- Unattended runs touch engagement data only within firm-approved tooling
  and the engagement's data-handling rules.
