---
name: interactive-brief
description: Build self-contained interactive HTML artifacts consumed on a phone from a file attachment that collect the reader's structured reactions and send them back via pre-filled iMessage or clipboard — briefs, review decks, decision cards. Use when an HTML deliverable must work offline, one card at a time, and return the reader's input. For client-facing sites/reports use ey-site; for general web UI use frontend-design.
license: MIT
---

# Interactive Brief

A self-contained HTML file, texted as an attachment, read on an iPhone one card
at a time, that collects the reader's reactions and returns them to you. Consuming
the brief *is* feeding the system. These invariants are distilled from shipping
the pattern repeatedly — the build gates below are the ones that actually broke.

Gate the finished artifact with `adversarial-design-review` before it ships.

## Principles

- **Self-contained single file.** No external JS/CSS/CDN/font/network deps — it
  renders offline from an iMessage attachment. Inline everything.
- **Bite-sized.** One signal/card at a time (swipe/tap through), never a wall of
  text. Information first, implication second.
- **Two-way.** Each card collects a reaction (keep/drop · "real data" vs "a take"
  · agree/disagree · quick note). The read and the response are the same act.
- **One-tap send-back.** Reactions compile to a compact payload returned via a
  pre-filled iMessage, with a copy-to-clipboard fallback.
- **Plain-English only.** No internal codes (hypothesis IDs, phase/gate numbers)
  anywhere the reader sees — spell the thing out.
- **Phone-first.** Large tap targets, thumb-reachable controls, readable without
  zoom (but never `user-scalable=no` — that forbids pinch-zoom and is hostile).
- **Progressive enhancement.** iMessage/Files QuickLook runs **no JavaScript**.
  Put all content in static HTML (readable in the preview) and let the script
  *upgrade* it to the interactive view. The accompanying text must say "open in
  Safari / save to Files first."

## Hard build gates

Each of these shipped broken at least once. Check every one before sending.

- **A renderer for every data key.** Diff the data object against `render()` at
  build time. A `flags`/decision key that exists in the data but has no renderer
  silently vanishes — and it's usually the most action-seeking content in the
  brief. Silent content drops are faithfulness failures.
- **String-valued reaction state.** Inline `onclick="set('${id}','${k}',1)"`
  coerces `1` to the string `"1"`; a check of `r.keep === 1` then never matches
  and the chip never registers. Use string values everywhere (`"keep"`, `"drop"`,
  `"agree"`, `"push"`) or `data-*` attributes + a delegated listener. Then
  hand-test the full round-trip: tap → chip highlights → payload contains the
  verdict. A reaction UI whose reactions don't register is worse than a read-only
  brief.
- **No surviving placeholders.** Fail generation on any `TODO`/`XXXX`/`[date]`/
  sample value in the data block — the send-back number has shipped as
  `+1XXXXXXXXXX`.
- **iOS `sms:` recipient quirk.** `sms:&body=…` with **no** recipient opens
  Messages and lets the reader pick the thread; `sms:<num>?&body=…` **with** one.
  The old `sms:<num>&body=` form is broken on iOS.
- **Clipboard fallback + feedback.** `navigator.clipboard` needs a secure context
  and silently no-ops on `file://`. Add a `document.execCommand('copy')` fallback
  via a temp textarea; flip the button to "Copied ✓" on success / "long-press the
  text below" on failure.
- **localStorage progress, keyed by id.** A multi-card brief is a multi-sitting
  artifact on a phone; persist `state` + card index to `localStorage` keyed by the
  artifact's date/id and restore on load. It's the only persistence available in
  the attachment context.
- **Sanitize free text.** Strip newlines before a note enters the line-oriented
  payload; escape it before it re-enters HTML (a note containing `</textarea>`
  breaks the card re-render).
- **Label chip rows as questions, pre-light your stance.** An unlabeled chip row
  reads as decoration. Label each row with the question it answers ("Worth
  keeping?", "Agree with my tag?") and pre-select your own position so agreement
  costs zero taps and only disagreement costs one.
- **Hand-write short payload labels.** The machine-facing string is user-facing —
  truncated mid-word labels ("bea…") are a visible defect. Keep payload labels
  short and whole; no codes.
- **If you're asking for a decision, make it a tappable card** with the options as
  buttons that flow into the payload — never bury the ask in prose that might not
  render.

## Verification

1. **Run the JS against a mock DOM** — don't read it. String-coercion and render
   bugs only surface on execution.
2. **Full round-trip test** — tap a reaction, confirm the chip highlights, confirm
   the payload contains the verdict, confirm the `sms:`/clipboard send fires.
3. **Offline/self-contained check** — no external request when opened from a
   `file://` attachment.
4. **Then gate with `adversarial-design-review`** for the tells, measured contrast,
   and 375px signature-element pass.
