#!/usr/bin/env python3
"""Closed-loop slide verification, tier 1+2: structurally diff a rebuilt
slide against a target construction spec, then run machine-checkable design
rules. Stdlib only. Vision review (tier 3) stays with the agent.

Usage:
    python spec_diff.py target-spec.json candidate.pptx SLIDE# [--kit kit.json] [--tol 0.05]

target-spec.json comes from slide_anatomy.py (set per-element "mode" to
preserve|flex and fill token_map roles first — unannotated elements are
treated as preserve, at reduced severity). With --kit, fills are verified by
ROLE through the kit (restyle-aware); without it, by literal value.

Exit codes: 0 clean · 1 should-fix findings · 2 blockers.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from slide_anatomy import extract, EMU_PER_IN  # noqa: E402

MARGIN_IN = 0.4
ACCENT_SHARE_MAX = 0.12  # rule 8 with a little slack


def load_kit(path):
    if not path:
        return None
    kit = json.loads(Path(path).read_text())
    return kit.get("colors", {}).get("roles", {})


def role_value(roles, role):
    """Resolve a role name to acceptable value(s) from the kit."""
    if not roles or not role:
        return None
    base = role.split("[")[0]
    val = roles.get(base)
    if isinstance(val, list):
        return [v.upper() for v in val]
    return [val.upper()] if val else None


def first_color(s, theme=None):
    """First color token in a fill/line string, theme refs resolved to hex."""
    for tok in (s or "").split():
        if tok.startswith("#"):
            return tok
        if tok.startswith("theme:"):
            slot = tok.split(":", 1)[1]
            return (theme or {}).get(slot, tok)
    return ""


def match_elements(target, candidate):
    """Pair elements by unique name, then by kind + nearest center."""
    pairs, t_left, c_left = [], list(target), list(candidate)
    t_names = {e["name"]: e for e in t_left if e["name"]}
    c_names = {e["name"]: e for e in c_left if e["name"]}
    for name in list(t_names):
        if name in c_names:
            pairs.append((t_names[name], c_names[name]))
            t_left.remove(t_names[name])
            c_left.remove(c_names[name])
    for t in list(t_left):
        best, bd = None, None
        for c in c_left:
            if c["kind"] != t["kind"] or c["depth"] != t["depth"]:
                continue
            if "x" in t and "x" in c:
                d = abs(t["x"] - c["x"]) + abs(t["y"] - c["y"])
            else:
                d = 0
            if bd is None or d < bd:
                best, bd = c, d
        if best is not None:
            pairs.append((t, best))
            t_left.remove(t)
            c_left.remove(best)
    return pairs, t_left, c_left


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 3:
        sys.exit(__doc__)
    target = json.loads(Path(args[0]).read_text())
    cand = extract(Path(args[1]), int(args[2]))
    kit_path = sys.argv[sys.argv.index("--kit") + 1] if "--kit" in sys.argv else None
    roles = load_kit(kit_path)
    tol_in = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 0.05
    tol = tol_in * EMU_PER_IN
    token_map = {k.upper() if k.startswith("#") else k: v
                 for k, v in target.get("token_map", {}).items()}
    # alias theme: keys to their resolved hex so lookups work either way
    t_theme = target.get("theme", {})
    for k in list(token_map):
        if k.startswith("theme:"):
            hexv = t_theme.get(k.split(":", 1)[1])
            if hexv:
                token_map.setdefault(hexv.upper(), token_map[k])

    findings = []  # (severity, where, message)

    def add(sev, where, msg):
        findings.append((sev, where, msg))

    # Canvas
    tw, th = target["canvas"]["w"], target["canvas"]["h"]
    cw, ch = cand["canvas"]["w"], cand["canvas"]["h"]
    scale = None
    if (tw, th) != (cw, ch):
        if abs(tw / th - cw / ch) < 0.01:
            scale = cw / tw
            add("polish", "canvas", f"different canvas size, same ratio — comparing scaled (×{scale:.3f})")
        else:
            add("blocker", "canvas", f"aspect ratio differs: target {tw}x{th}, candidate {cw}x{ch}")

    pairs, missing, extra = match_elements(target["elements"], cand["elements"])

    for t in missing:
        sev = "blocker" if (t.get("mode") or "preserve") == "preserve" else "should-fix"
        add(sev, f"z{t['z']} {t['name'] or t['kind']}", "missing in candidate")
    for c in extra:
        add("should-fix", f"cand z{c['z']} {c['name'] or c['kind']}", "extra element not in target spec")

    for t, c in pairs:
        where = f"z{t['z']} {t['name'] or t['kind']}"
        mode = t.get("mode") or ""
        strict_sev = "blocker" if mode == "preserve" else "should-fix"
        if t["kind"] != c["kind"]:
            add(strict_sev, where, f"kind changed: {t['kind']} → {c['kind']}")
        # Geometry (skip for flex)
        if mode != "flex" and "x" in t and "x" in c:
            s = scale or 1
            for dim in ("x", "y", "w", "h"):
                d = abs(t[dim] * s - c[dim])
                if d > tol:
                    add(strict_sev if not mode else strict_sev, where,
                        f"{dim} off by {d / EMU_PER_IN:.2f}in "
                        f"(target {t[dim]/EMU_PER_IN:.2f}, got {c[dim]/EMU_PER_IN:.2f})")
        # Color by role (or literal); theme refs resolved through each theme
        for attr in ("fill", "line"):
            t_col = first_color(t.get(attr), target.get("theme"))
            c_col = first_color(c.get(attr), cand.get("theme"))
            if not t_col or t_col == c_col:
                continue  # absent, or identical (incl. same unresolved theme ref)
            key = t_col.upper() if t_col.startswith("#") else t_col
            role = token_map.get(key, "")
            if role and roles:
                expected = role_value(roles, role)
                if not c_col.startswith("#"):
                    add("polish", where,
                        f"{attr} {c_col or 'none'} is an unresolved theme ref — verify role '{role}' manually")
                elif expected and c_col.upper() not in expected:
                    add("blocker", where,
                        f"{attr} {c_col} does not resolve to role '{role}' "
                        f"(expected {', '.join(expected)})")
            elif not roles:
                add("should-fix", where, f"{attr} differs: {t_col} → {c_col or 'none'}")
            else:
                add("polish", where, f"{attr} {t_col} has no role in token_map — unverifiable by role")

    # Flex invariants: consistent spacing within sibling runs of same kind
    flex = [c for t, c in pairs if t.get("mode") == "flex" and "x" in c]
    by_kind = {}
    for c in flex:
        by_kind.setdefault((c["kind"], c["depth"]), []).append(c)
    for (kind, _), els in by_kind.items():
        if len(els) >= 3:
            xs = sorted(e["x"] for e in els)
            gaps = [b - a for a, b in zip(xs, xs[1:])]
            if max(gaps) - min(gaps) > tol:
                add("should-fix", f"flex run ({kind})",
                    f"uneven horizontal spacing: gaps {[round(g/EMU_PER_IN,2) for g in gaps]}in")

    # ---- Tier 2: machine-checkable design rules on the candidate ----
    margin = MARGIN_IN * EMU_PER_IN
    for c in cand["elements"]:
        if "x" not in c or c["depth"] > 0 or c["placeholder"]:
            continue
        if c["x"] < margin - tol or c["y"] < margin - tol or \
           c["x"] + c["w"] > cw - margin + tol or c["y"] + c["h"] > ch - margin + tol:
            add("polish", f"cand z{c['z']} {c['name'] or c['kind']}",
                "outside 0.4in margins (rule 5) — confirm intentional (full-bleed?)")
    if roles:
        accent = (roles.get("accent") or "").upper()
        if accent:
            area = sum(c["w"] * c["h"] for c in cand["elements"]
                       if "x" in c and first_color(c.get("fill"), cand.get("theme")).upper() == accent)
            share = area / (cw * ch)
            if share > ACCENT_SHARE_MAX:
                add("should-fix", "accent scarcity",
                    f"accent fills cover {share:.0%} of canvas (rule 8 cap ~10%)")
    for c in cand["elements"]:
        m = (c.get("textmeta") or "").split("pt")[0]
        if m.isdigit() and int(m) < 10:
            add("should-fix", f"cand z{c['z']} {c['name'] or c['kind']}",
                f"text at {m}pt is below caption size (rule 5)")

    # ---- Report ----
    order = {"blocker": 0, "should-fix": 1, "polish": 2}
    findings.sort(key=lambda f: order[f[0]])
    print(f"# spec_diff — target {target['source']} s{target['slide']} vs "
          f"candidate {cand['source']} s{cand['slide']}")
    print(f"{len(pairs)} matched, {len(missing)} missing, {len(extra)} extra; "
          f"tolerance ±{tol_in}in; kit: {'role-based' if roles else 'literal (no --kit)'}\n")
    if not findings:
        print("CLEAN — no findings. Proceed to tier 3 (visual review).")
        sys.exit(0)
    print("| Severity | Where | Finding |")
    print("|----------|-------|---------|")
    for sev, where, msg in findings:
        print(f"| {sev} | {where} | {msg} |")
    worst = findings[0][0]
    sys.exit(2 if worst == "blocker" else 1 if worst == "should-fix" else 0)


if __name__ == "__main__":
    main()
