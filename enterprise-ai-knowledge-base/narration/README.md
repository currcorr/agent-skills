# Narration-Clean Variant (for NotebookLM / audio & video)

These files are a **format-only transformation** of the reader-facing modules in the parent directory, optimized to be **read aloud** by tools that generate audio overviews and video (e.g., NotebookLM). **The substance is preserved** — the same content, facts, figures, dates, vendor names, maturity labels, and verify-warnings as the reader versions; only the presentation changed. (The reader set marks things to double-check with a ⚠ glyph; the narration set carries the same warnings in spoken words like "verify" instead, since the glyph doesn't narrate.)

## What's different from the reader version
- **Letter-tag scaffolding removed** — `(a)/(b)/(c)/(d)/(e)/(f)` (and `(b′)`, `(c/d)` variants) became plain spoken sub-headings like **Why it matters**, **How it works**, **Where it goes wrong**, **A concrete example**.
- **Inline cross-references removed** — `(Module 3.8)`, `(1.5)`, `(2.6/3.9)` became prose bridges ("as covered in the retrieval module") or were dropped, so each file **stands alone** when uploaded by itself.
- **Tables converted to prose / spoken lists** — the radar summary, the platform tradeoff table, etc. now narrate as sentences.
- **Symbols and notation spelled out** — `→`, `×`, `≥`, `≈`, `O(n²)`, `king − man + woman ≈ queen`, formulas, and code/ASCII (Cypher, JSON, `Database.Savepoint`) rendered as speech-friendly prose (with a glossed fenced block where the literal form still helps).
- **Self-contained** — each file opens with a one-line standalone-context note; authoring artifacts ("Proceed to…", "(Pass 2)") removed.

## Which set should I use?
- **Reading on screen / skimming / reference** → use the **parent-directory** files (richer formatting, tables, cross-links).
- **Feeding NotebookLM to generate an Audio Overview or video, or any text-to-speech** → use **these** files.

## Important
- Upload **one variant set, not both**, to avoid duplicate-content weighting in NotebookLM.
- These are generated from the reader files; if you edit the reader modules, regenerate the affected narration file.
- The **`SOURCES.md`** appendix and the record-time verification checklist live in the parent directory and apply equally here — re-verify ⚠-flagged vendor/regulatory/rankings claims before recording. (Notably: **Logik.ai was acquired by ServiceNow, not Salesforce.**)
