"""Build td-synnex/site/index.html from the Markdown report, the 10-Q data file and the chart kit."""
import json, re, html, pathlib, markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports" / "TD SYNNEX commercial AI vision 2030.md"
DATA = json.loads((ROOT / "data" / "q3fy26_data.json").read_text())
SRC = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "site" / "index.html"

md_text = REPORT.read_text()
title_line, rest = md_text.split("\n", 1)
report_title = title_line.lstrip("# ").strip()
# Split off the intro notes (before the first h2)
intro, body = rest.split("\n## ", 1)
body = "## " + body
intro_html = markdown.markdown(intro.strip(), extensions=["tables", "sane_lists"])

# ---------- data helpers ----------
q = {r["period"]: r for r in DATA["quarterly"]["data"]}
QS = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
b = lambda m: round(m / 1000, 2) if m is not None else None
seg3, seg3p = DATA["segments_q3"]["Q3_FY26"], DATA["segments_q3"]["Q3_FY25"]
SEGS = ["Americas", "Europe", "APJ", "Hyve"]
bs = DATA["balance_sheet"]
pm = DATA["product_mix"]

CHARTS = []
def fig(cid, title, sub, kind, spec, caption):
    CHARTS.append({"id": cid, "type": kind, "spec": spec})
    return (f'<figure class="viz" id="{cid}"><p class="vt">{title}</p><p class="vs">{sub}</p>'
            f'<div class="viz-body"></div><figcaption>{caption}</figcaption></figure>')

F = {}
F["quarterly"] = fig("c-quarterly", "Revenue and gross billings by quarter",
    "USD billions, fiscal quarters (FY ends Nov 30). Q4 FY26 is the guidance midpoint.", "columns",
    {"categories": QS + ["Q4 FY26e"], "unit": "$B", "height": 300, "labelLast": True,
     "series": [
        {"name": "Revenue (GAAP)", "values": [b(q[p]["revenue"]) for p in QS] + [22.2], "est": [0]*7 + [1],
         "note": [None]*7 + ["Guidance midpoint ($21.8–22.6B)"]},
        {"name": "Gross billings (non-GAAP)", "label": True, "values": [b(q[p]["gross_billings_nongaap"]) for p in QS] + [31.9], "est": [0]*7 + [1],
         "note": [None]*7 + ["Guidance midpoint ($31.4–32.4B)"]}]},
    "Revenue: 10-Q for Q3 FY25 and Q3 FY26; Q4 FY25 from the 10-Q cash conversion table; Q1 FY26 and FY25 quarters derived or from earnings releases. Gross billings: earnings releases (not in the 10-Q). Faded bars are guidance.")
gm_q = QS[1:]
F["gm"] = fig("c-gm", "Gross margin is drifting down as mix shifts",
    "Gross profit as % of GAAP revenue, by quarter", "line",
    {"categories": gm_q, "unit": "%", "min": 6.4, "max": 7.4, "ticks": [6.4, 6.6, 6.8, 7.0, 7.2, 7.4],
     "series": [{"name": "Gross margin", "values": [q[p]["gross_margin_pct"] for p in gm_q]}], "labelIdx": [1]},
    "Q3 FY25 and Q3 FY26: 10-Q. Other quarters derived from 10-Q totals or earnings releases. The y-axis starts at 6.4% to make the change visible.")
dates = ["Aug 31, 2025", "Nov 30, 2025", "Aug 31, 2026"]
F["wc"] = fig("c-wc", "Hyve's build-out shows up in inventory",
    "Balance sheet items, USD billions", "columns",
    {"categories": dates, "unit": "$B",
     "series": [{"name": "Accounts receivable", "values": [10.93, b(bs["2025-11-30"]["accounts_receivable"]), b(bs["2026-08-31"]["accounts_receivable"])]},
                {"name": "Inventory", "values": [9.14, b(bs["2025-11-30"]["inventory"]), b(bs["2026-08-31"]["inventory"])]},
                {"name": "Accounts payable", "values": [15.65, b(bs["2025-11-30"]["accounts_payable"]), b(bs["2026-08-31"]["accounts_payable"])]}]},
    "Source: 10-Q, quarter ended Aug 31, 2026, p. 3 and 43. Cash conversion cycle: 23 days, 16 days and 31 days at the three dates. Net debt rose from about $2.2B to about $4.8B between November and August (derived).")
rev_share = [round(seg3[s]["revenue"] / seg3["Total"]["revenue"] * 100, 1) for s in SEGS]
oi_share = [round(seg3[s]["operating_income_gaap"] / seg3["Total"]["operating_income_gaap"] * 100, 1) for s in SEGS]
F["segshare"] = fig("c-segshare", "Hyve is 18% of revenue but 39% of operating income",
    "Share of Q3 FY26 total, by segment (GAAP)", "stack",
    {"names": SEGS, "unit": "%", "pct": True, "max": 100, "labelW": 150,
     "rows": [{"label": "Revenue", "parts": rev_share}, {"label": "Operating income", "parts": oi_share}]},
    f"Source: 10-Q, quarter ended Aug 31, 2026, p. 26-27. Q3 FY26 GAAP operating income: Hyve ${seg3['Hyve']['operating_income_gaap']:.0f}M vs Americas ${seg3['Americas']['operating_income_gaap']:.0f}M.")
F["segrev"] = fig("c-segrev", "Every segment grew, Hyve and the Americas fastest",
    "Segment revenue, USD billions, Q3 FY25 vs Q3 FY26", "columns",
    {"categories": SEGS, "unit": "$B", "labelAll": True,
     "series": [{"name": "Q3 FY25", "values": [b(seg3p[s]["revenue"]) for s in SEGS]},
                {"name": "Q3 FY26", "values": [b(seg3[s]["revenue"]) for s in SEGS]}]},
    "Source: 10-Q, quarter ended Aug 31, 2026, p. 26-27. Prior year recast to the four-segment structure. Hyve revenue is much lower than its billings because many Hyve programs are booked net.")
g26, g25 = pm["Q3_FY26"]["gross_billings"], pm["Q3_FY25"]["gross_billings"]
F["mix"] = fig("c-mix", "Gross billings mix: Hyve more than doubled",
    "Non-GAAP gross billings by portfolio, USD billions", "stack",
    {"names": ["Endpoint Solutions", "Advanced Solutions (ex-Hyve)", "Hyve"], "unit": "$B", "labelW": 90,
     "rows": [{"label": "Q3 FY25", "parts": [b(g25["endpoint"]), b(g25["advanced_ex_hyve"]), b(g25["hyve"])]},
              {"label": "Q3 FY26", "parts": [b(g26["endpoint"]), b(g26["advanced_ex_hyve"]), b(g26["hyve"])]}]},
    "Source: earnings release and call commentary (secondary; billings are not in the 10-Q). Q3 FY25 Endpoint and Advanced are back-calculated from reported growth rates. Growth: Endpoint +16%, Advanced +37%, Hyve +117%.")
cats = DATA["estimates"]["categories"]
short = {"PCs": "PCs", "Mobile": "Mobile phones, tablets", "Peripherals": "Peripherals, print, CE",
         "Software": "Software, cloud, security", "Servers": "Servers, storage, network", "Hyve": "Hyve (reported)"}
rows = []
for c in cats:
    lab = next(v for k, v in short.items() if c["category"].startswith(k))
    lo, hi = b(c["low"]), b(c["high"])
    rows.append({"label": lab, "value": round((lo + hi) / 2, 1), **({"lo": lo, "hi": hi} if lo != hi else {}),
                 "hl": c["confidence"].startswith("high"), "note": "Confidence: " + c["confidence"]})
F["cats"] = fig("c-cats", "Estimated FY2025 product mix",
    "Gross billings by category, USD billions. Bars show the estimated range; the tick is the midpoint.", "bars",
    {"rows": rows, "unit": "$B", "labelW": 170, "max": 30, "valueName": "Estimated range"},
    "These are research-team estimates, not company disclosures. Only Hyve is reported. TD SYNNEX publishes no category split below Endpoint, Advanced and Hyve. FY2025 gross billings were about $89.4B.")
conc = DATA["concentration"]
F["conc"] = fig("c-conc", "No single vendor or customer dominates",
    "Share of consolidated revenue (%), as disclosed", "bars",
    {"rows": [{"label": "Apple, FY2025", "value": 12, "hl": True},
              {"label": "Apple, 9M FY26", "value": conc["vendors"]["Apple"]["9M_FY26"], "hl": True},
              {"label": "HP Inc., FY2025", "value": 10},
              {"label": "Largest customer, FY2025", "value": 11},
              {"label": "Largest customer, 9M FY26", "value": 0, "text": "under 10%", "note": "Below the 10% disclosure threshold"}],
     "unit": "%", "max": 14, "labelW": 190},
    "Source: FY2025 10-K and 10-Q, quarter ended Aug 31, 2026, p. 9-10. The 10-Q discloses only shares of 10% or more; a zero bar means below that threshold. HP Inc. was also below 10% in FY2026 to date.")
F["margins"] = fig("c-margins", "Distributors earn about a third of a reseller's gross margin",
    "Gross margin, latest reported period (%)", "bars",
    {"rows": [{"label": "TD SYNNEX (Q3 FY26)", "value": 6.61, "hl": True},
              {"label": "Ingram Micro (Q2 2026)", "value": 6.60},
              {"label": "Dicker Data (H1 2026)", "value": 9.8},
              {"label": "ScanSource (FY2026)", "value": 13.6},
              {"label": "CDW (Q2 2026)", "value": 20.1},
              {"label": "Insight (Q2 2026)", "value": 21.7}],
     "unit": "%", "max": 24, "labelW": 190},
    "Sources: company releases via the research notes; TD SYNNEX from the 10-Q. Periods differ, so treat as indicative. CDW and Insight are large resellers that are both customers and, on big deals, competitors.")
F["mkt"] = fig("c-mkt", "Hyperscaler marketplaces grow, and partners handle more of it",
    "Omdia forecast: software sold through hyperscaler marketplaces, USD billions", "columns",
    {"categories": ["2024", "2030 (forecast)"], "unit": "$B", "labelAll": True, "height": 240,
     "series": [{"name": "Marketplace software sales", "values": [30, 163]}]},
    "Source: Omdia via Intelligent CIO (Oct 2025); 29.1% compound annual growth. One release gives a $16B 2024 base. Partner share of marketplace spend: 37% in 2025, 50% in 2027, 59% in 2030 (forecast). Distribution is still about 5.7 times the size of the marketplace opportunity.")

# ---------- diagrams (inline SVG / HTML) ----------
ARROW = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" class="dg-head"/></marker></defs>'
def box(x, y, w, h, t, lines, core=False, meta=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{"dg-core" if core else "dg-box"}"/>'
    s += f'<text x="{x+12}" y="{y+22}" class="dg-t">{html.escape(t)}</text>'
    for i, l in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+42+i*16}" class="dg-s">{html.escape(l)}</text>'
    if meta:
        s += f'<text x="{x+12}" y="{y+h-10}" class="dg-m">{html.escape(meta)}</text>'
    return s
def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None, anchor="middle"):
    s = f'<path d="M{x1},{y1}L{x2},{y2}" class="dg-arrow" marker-end="url(#ah)"/>'
    if label:
        s += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" class="dg-m">{html.escape(label)}</text>'
    return s
svg = ['<svg viewBox="0 0 990 330" role="img" aria-label="How TD SYNNEX makes money: vendors sell through TD SYNNEX to partners, who serve end customers; Hyve builds for hyperscalers">', ARROW]
svg.append(box(10, 60, 175, 170, "Technology vendors", ["~2,500 OEMs, software", "and cloud publishers", "Apple, HP, Cisco, Dell,", "HPE, Lenovo, Microsoft,", "NVIDIA, AWS, Google"], meta="REBATES · MDF · TERMS"))
svg.append('<rect x="255" y="16" width="320" height="300" rx="10" class="dg-core"/>')
svg.append('<text x="271" y="40" class="dg-t">TD SYNNEX</text><text x="271" y="57" class="dg-m">FY2025 · $89.4B BILLINGS · ~2¢ PROFIT PER $1</text>')
svg.append(box(271, 70, 288, 128, "Distribution (Americas, Europe, APJ)", ["Endpoint: PCs, phones, print, peripherals", "Advanced: servers, storage, networking,", "software, security, cloud", "Credit, logistics, marketplaces, enablement"]))
svg.append(box(271, 212, 288, 90, "Hyve Solutions", ["Designs and builds servers and racks", "for hyperscalers and AI clouds"], meta="Q3 FY26 · 39% OF GAAP OP. INCOME"))
svg.append(box(675, 40, 165, 160, "150,000+ partners", ["VARs, MSPs, system", "integrators, retailers,", "public sector resellers,", "cloud providers"]))
svg.append(box(865, 70, 118, 100, "End customers", ["Businesses,", "government,", "consumers"]))
svg.append(box(675, 230, 308, 70, "Hyperscalers and GPU clouds", ["All five top US hyperscalers; Amazon warrant"]))
svg.append(arrow(187, 145, 253, 145, "SUPPLY", 220, 136))
svg.append(arrow(561, 125, 673, 125, "CREDIT · STOCK", 617, 116))
svg.append(arrow(840, 120, 863, 120))
svg.append(arrow(561, 262, 673, 262, "BUILT TO SPEC", 617, 253))
svg.append('</svg>')
F["model"] = ('<figure class="viz diagram"><p class="vt">How the business works</p><p class="vs">Two-tier distribution plus a hyperscale manufacturing arm</p>'
              + "".join(svg) + '<figcaption>Sources: FY2025 10-K; 10-Q, quarter ended Aug 31, 2026. Operating profit per dollar billed is derived from FY2025 non-GAAP operating income and gross billings.</figcaption></figure>')

routes = [("PartnerFirst portal", "Unified digital portal; North America Sept 2025, Europe July 2026. AI assistant for 24/7 self-service."),
          ("APIs and integrations", "EC Express, real-time XML/API feeds, Digital Bridge connectors to Teams, Slack, Webex, Salesforce, QuickBooks."),
          ("StreamOne Ion marketplace", "Cloud and MSP motion: PSA connectors, headless commerce API, white-label storefronts, AWS seller of record."),
          ("Specialists and reps", "Sales specialists by technology and customer tier, inside sales, PartnerLINK communities, Destination AI.")]
F["routes"] = ('<figure class="viz"><p class="vt">Four ways partners buy from TD SYNNEX</p><p class="vs">From fully digital to fully human</p><div class="routes">'
               + "".join(f'<div class="route"><span class="route-k">{"Digital" if i<3 else "Human"}</span><b>{html.escape(t)}</b><span>{html.escape(d)}</span></div>' for i, (t, d) in enumerate(routes))
               + '</div><figcaption>Source: section 5 of this report; company releases and trade press, 2024-2026.</figcaption></figure>')

tiers = [("Agent-served", "Long-tail partners", "AI account managers recommend, quote and reorder. Partner and procurement agents buy through APIs."),
         ("Hybrid", "Growth partners", "A named human, backed by AI tools for pipeline, pricing and enablement."),
         ("High-touch", "Strategic partners and complex deals", "Specialist teams for AI factories, public sector, security and data center.")]
F["coverage"] = ('<figure class="viz"><p class="vt">The 2030 coverage model, in three motions</p><p class="vs">One platform underneath: agent-ready catalog, price, stock, credit and order status</p><div class="tiers">'
                 + "".join(f'<div class="tier t{i}"><span class="route-k">{html.escape(k)}</span><b>{html.escape(w)}</b><span>{html.escape(d)}</span></div>' for i, (k, w, d) in enumerate(tiers))
                 + '</div><div class="rails">Agent-ready commerce rails · data foundation · AI governance</div><figcaption>Interpretation: a preliminary recommendation for discussion, not a company plan.</figcaption></figure>')

# ---------- convert body ----------
sections = re.split(r"\n(?=## )", body.strip())
INTERP = {"9", "10", "12"}
toc, out = [], []
def short_label(h):
    h = re.sub(r"^\d+\.\s*", "", h)
    return h if len(h) < 52 else h[:50].rsplit(" ", 1)[0] + "…"

def insert_before(h, anchor, frag):
    i = h.find(anchor)
    if i < 0: raise SystemExit(f"anchor not found: {anchor[:60]}")
    return h[:i] + frag + h[i:]
def insert_after_block(h, needle, frag):
    i = h.find(needle)
    if i < 0: raise SystemExit(f"needle not found: {needle[:60]}")
    opens = {t: h.rfind(f"<{t}", 0, i) for t in ("p", "ul", "table")}
    tag = max(opens, key=opens.get)
    j = h.find(f"</{tag}>", i) + len(f"</{tag}>")
    return h[:j] + frag + h[j:]

for sec in sections:
    head, _, content = sec.partition("\n")
    htxt = head[3:].strip()
    m = re.match(r"(\d+)\.\s", htxt)
    num = m.group(1) if m else None
    sid = "s" + num if num else re.sub(r"[^a-z]+", "-", htxt.lower()).strip("-")[:30]
    h = markdown.markdown(content, extensions=["tables", "sane_lists"])
    h = h.replace("<table>", '<div class="tbl-wrap"><table>').replace("</table>", "</table></div>")
    h = re.sub(r'<a href="(http[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', h)
    if num == "1":
        h = insert_before(h, "<p><strong>Billings vs revenue.", F["model"])
    if num == "2":
        h = insert_before(h, "<p><strong>FY2026 run rate.", F["quarterly"])
        h = insert_before(h, "<p><strong>A reporting conflict", F["gm"])
        h = insert_before(h, "<p>The cash conversion cycle lengthened", F["wc"])
    if num == "3":
        h = insert_before(h, "<p><strong>Nine months ended", F["segshare"] + F["segrev"])
        h = insert_before(h, "<p><strong>Product categories below", F["mix"])
        h = insert_before(h, "<p><strong>Where growth is coming from.", F["cats"])
    if num == "5":
        h = insert_before(h, "<p><strong>The cloud and MSP motion", F["routes"])
    if num == "6":
        h = insert_after_block(h, "</p>", F["conc"]) if False else h.replace("</p>", "</p>" + F["conc"], 1)
    if num == "7":
        h = insert_after_block(h, "Ingram Micro (Q2 2026", F["margins"])
    if num == "8":
        h = insert_after_block(h, "Omdia forecasts hyperscaler marketplace", F["mkt"])
    if num == "12":
        h = insert_after_block(h, "By 2030 the commercial organization should work", F["coverage"])
    label = "Interpretation" if num in INTERP else ("Section " + num if num else "")
    badge = f'<span class="interp">Interpretation</span>' if num in INTERP else ""
    eyebrow = f'<div class="sec-no">{"Section " + num if num else ("Summary" if "Executive" in htxt else "Appendix" if "Review" in htxt else "Close")}</div>'
    out.append(f'<section class="sec" id="{sid}">{eyebrow}<h2>{html.escape(re.sub(r"^\d+\.\s*", "", htxt))}</h2>{badge}{h}</section>')
    toc.append(f'<li><a href="#{sid}">{html.escape(short_label(htxt))}</a></li>')

sections_html = "\n".join(out)

# ---------- hero manifest ----------
t, tp = seg3["Total"], seg3p["Total"]
manifest = [
    ("Q3 FY26 revenue", f"${t['revenue']/1000:.1f}B", f"<b>+{(t['revenue']/tp['revenue']-1)*100:.1f}%</b> year on year"),
    ("Q3 FY26 gross billings", "$31.8B", "<b>+40.0%</b> · earnings release"),
    ("Hyve operating income", f"${seg3['Hyve']['operating_income_gaap']:.0f}M", f"vs Americas ${seg3['Americas']['operating_income_gaap']:.0f}M (GAAP)"),
    ("Gross margin", f"{t['gross_margin_pct']:.2f}%", f"<b class=\"neg\">−{(tp['gross_margin_pct']-t['gross_margin_pct'])*100:.0f} bp</b> vs {tp['gross_margin_pct']:.2f}%"),
    ("Free cash flow, 9 months", "−$2.2B", "<b class=\"neg\">vs −$0.03B</b> a year earlier (derived)"),
]
manifest_html = "".join(f'<div><span class="k">{k}</span><span class="v">{v}</span><span class="d">{d}</span></div>' for k, v, d in manifest)

css = (SRC / "style.css").read_text()
css += """
.routes,.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-top:4px}
.route,.tier{display:flex;flex-direction:column;gap:4px;padding:12px;border:1px solid var(--rule);border-radius:6px;background:var(--paper);font-family:var(--f-ui);font-size:13.5px;line-height:1.45;min-width:0}
.route b,.tier b{font-size:14.5px}
.route span:last-child,.tier span:last-child{color:var(--ink-2)}
.route-k{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.tier.t0{border-top:3px solid var(--s1)}.tier.t1{border-top:3px solid var(--s2)}.tier.t2{border-top:3px solid var(--s3)}
.rails{margin-top:10px;padding:9px 12px;border-radius:6px;background:var(--accent-wash);font-family:var(--f-mono);font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink);text-align:center}
.intro-notes{font-family:var(--f-ui);font-size:13.5px;line-height:1.55;color:var(--ink-2);max-width:760px;margin-top:20px}
.intro-notes p{max-width:none}
.intro-notes summary{cursor:pointer;color:var(--accent);font-weight:600}
"""
js = (SRC / "charts.js").read_text()

page = f"""<title>TD SYNNEX 2030 Briefing</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>{css}</style>
<header class="topbar"><div class="topbar-in">
  <a class="brand" href="#top">SNX <span>2030</span></a>
  <span class="meta">TD SYNNEX research briefing · updated Oct 12, 2026 with the Q3 FY26 10-Q</span>
  <span class="spacer"></span>
  <button class="toc-btn" id="toc-btn" type="button" aria-expanded="false" aria-controls="toc">Contents</button>
</div></header>
<div class="hero" id="top">
  <div class="eyebrow">Executive meeting briefing · NYSE: SNX · fiscal year ends Nov 30</div>
  <h1>{html.escape(report_title)}</h1>
  <p class="dek">The business, its numbers, its channel and vendor ecosystem, and what AI could make of its commercial organization by 2030.</p>
  <div class="manifest">{manifest_html}</div>
  <div class="source-line">Quarter ended Aug 31, 2026. Revenue, operating income and margin from the 10-Q; gross billings from the earnings release.</div>
  <details class="intro-notes"><summary>How to read this briefing</summary>{intro_html}</details>
</div>
<div class="shell">
  <nav class="toc" id="toc" aria-label="Contents"><div class="h">Contents</div><ol>{''.join(toc)}</ol></nav>
  <main><article>
{sections_html}
  <footer class="foot">Prepared for an executive meeting with TD SYNNEX leadership. Sources are linked inline; page numbers refer to the Form 10-Q for the quarter ended Aug 31, 2026. Sections marked Interpretation are the authors' analysis, not company statements.</footer>
  </article></main>
</div>
<script>window.CHARTS={json.dumps(CHARTS)};</script>
<script>{js}</script>
<script>
(function(){{
  const btn=document.getElementById('toc-btn'),toc=document.getElementById('toc');
  btn.addEventListener('click',()=>{{const o=toc.classList.toggle('open');btn.setAttribute('aria-expanded',o);}});
  toc.addEventListener('click',e=>{{if(e.target.tagName==='A'){{toc.classList.remove('open');btn.setAttribute('aria-expanded','false');}}}});
  const links=[...toc.querySelectorAll('a')];const map=new Map(links.map(a=>[a.getAttribute('href').slice(1),a]));
  if('IntersectionObserver' in window){{const io=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting){{links.forEach(l=>l.classList.remove('on'));const a=map.get(e.target.id);if(a)a.classList.add('on');}}}});}},{{rootMargin:'-20% 0px -70% 0px'}});
  document.querySelectorAll('section.sec').forEach(s=>io.observe(s));}}
}})();
</script>
"""
OUT.write_text(page)
print("wrote", OUT, len(page)//1024, "KB;", len(CHARTS), "charts;", len(sections), "sections")
