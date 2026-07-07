---
title: Reinvention, not bolt-on
subtitle: Where AI value actually lands in the sales organization, and how to capture it
client: Executive briefing
date: July 2026
author: Curran Corrigan
confidentiality: Confidential — draft for discussion
---

# Demo deck: 16 slides of real consulting content, built to the design
# doctrine (doctrine/design-doctrine.md): density varies by archetype class,
# takeaway bars are opt-in, exhibits own their stage, one local judgment per
# slide. This is the reference build — copy it as a starting point.
# The 'xp-' keys are the experience layer (render_experience.py); the PDF
# renderer ignores them entirely — see doctrine/experience-spec.md.
# Edit any line below and re-render: python3 render_deck.py content/demo-ai-sales-transformation.md --brand default --pdf
# Interactive version: python3 render_experience.py content/demo-ai-sales-transformation.md --brand default

```slide
archetype: title
title: Reinvention, not bolt-on
subtitle: Where AI value actually lands in the sales organization, and how to capture it
```

```slide
archetype: exec-summary
kicker: Executive summary
title: Fund operating-model reinvention, not another tool pilot
xp-goto: 1 :: s4
xp-goto: 2 :: s6
xp-goto: 3 :: s8
xp-goto: 4 :: s12
---
- Bolt-on AI is failing at enterprise scale :: MIT's *The GenAI Divide* (2025) finds 95% of GenAI pilots deliver no measurable P&L impact, with over half of budgets aimed at sales and marketing, where ROI is lowest
- Redesign separates the winners :: BCG (2025) measures 60%+ cost reduction where the process is redesigned end to end, against <20% without; McKinsey's high performers are ~3x more likely to redesign workflows
- Buyers are moving whether sellers do or not :: 51% now start research with an AI chatbot more often than Google, and 69% chose a different vendor than planned on AI guidance (G2, n=1,076, March 2026)
- The ask of this group :: Fund an assessment-first program that redesigns coverage, roles, comp, and process together, and set the measurement bar at P&L impact from day one
```

```slide
archetype: section-divider
title: The gap between AI adoption and AI value
subtitle: Almost every enterprise is running the same play, and it is not working
xp-act: The gap
```

```slide
archetype: kpi
kicker: The gap
title: The default play is failing at enterprise scale, and the failure is organizational, not technical
source: MIT, The GenAI Divide, 2025
notes: The 95% figure is directionally strong but methodologically contested; read it as a signal with wide error bars, not a point estimate.
xp-drill: Integration is the dividing line :: MIT's value-creating ~5% embedded AI in the workflow itself: integrated systems, not tools bolted on the side
xp-drill: The redesign multiplier :: 60%+ cost reduction with end-to-end process redesign, against <20% without (BCG, 2025)
xp-drill: The same signal twice :: McKinsey's high performers are ~3x more likely to redesign workflows end to end (McKinsey, 2025)
---
- 95% :: of GenAI pilots show no measurable P&L impact
- ~5% :: integrated systems that create value :: counter
```

```slide
archetype: two-col
kicker: The gap
title: Enterprises are bolting AI onto existing processes and capturing almost none of the available value
split: 2-1
source: MIT, The GenAI Divide, 2025; McKinsey, 2025
---
## What the evidence shows :: stat-rail
- >50% :: of GenAI budgets go to sales and marketing tools, exactly where measured ROI is lowest
- ~3x :: more likely to redesign workflows end to end: McKinsey's high performers versus the rest
- org, not model :: MIT's diagnosis is explicitly organizational: the failure sits in how firms deploy, not in the models
## The pattern that fails :: steps
- Buy the tool
- Leave coverage, roles, comp, and process untouched
- No P&L movement

**The tool is the trigger; the operating-model redesign is the work.**
```

```slide
archetype: data
kicker: The gap
title: Agentic AI pays only when the process is redesigned end to end
subtitle: Cost reduction from agentic deployments, by approach
source: BCG, 2025; McKinsey finds high performers ~3x more likely to redesign workflows
---
- With end-to-end process redesign :: 60%+ :: highlight
- Without process redesign :: <20%
```

```slide
archetype: section-divider
title: What changes in the sales motion
subtitle: Sellers, buyers, and the stack are all moving at once
xp-act: What changes
```

```slide
archetype: journey
kicker: How buyers choose
title: The shortlist is fixed before the first conversation: buyers now run three of five stages on AI research alone
highlight: 3
source: G2 buyer survey, n=1,076, March 2026; Gartner 2026 projections; house five-phase buying journey
---
stages:
1. Awareness :: problem sensing
2. Understand need :: solution mapping
3. Define criteria :: the shortlist forms
4. Evaluate options :: first seller contact
5. Validate & select :: commit

lane: Buyer actions
1: Senses underperformance; runs educational research to frame the problem
2: Names the problem; asks an AI assistant to map solutions and candidate partners
3: Sets selection criteria; has AI score the market and draft the shortlist
4: Invites the shortlist to respond; compares proposals with decision makers
5: Validates references and commercials; signs

lane: Where they look
1: Peer networks, industry press
2: ==51%== start with an AI chatbot, not Google — up from 29% in 2025
3: AI-synthesized vendor comparisons; analyst notes as tie-breakers
4: Your partners, proposals, orals
5: References, procurement

lane: Seller visibility
1-3!: Dark :: No calls, no RFIs: the firm cannot see this work happening
4-5: Visible :: First contact arrives with the shortlist already fixed

lane: What decides it
2: Whether the machine can find and cite your point of view
3: ==69%== chose a different vendor than planned on AI guidance; ~33% bought a previously unfamiliar firm
5: Whether stage-4 claims survive procurement's own AI check

bracket: 1-3 :: Pre-contact zone :: ~70% of the journey is complete before a seller knows the deal exists. Being findable and citable to the buyer's AI is now the top of the funnel.
bracket: 4-5 :: Selling starts here :: Against criteria and a shortlist the firm did not shape.
```

```slide
archetype: comparison
kicker: What changes
title: Plan for productivity-led substitution: fewer people covering more, with humans still in every loop
source: Salesforce State of Sales; Forrester; company reporting on 11x, 2025-26
xp-model: substitution :: default=100 :: range=20,500,10 :: mults=1.5,1.75,2
---
|  | Augmentation, today | Replacement in practice |
| --- | --- | --- |
| The mechanism | AI absorbs the **~70% of rep time that is not selling**: research, notes, CRM hygiene, follow-ups | Productivity math: one AE plus AI covers **1.5-2x the book**, so headcount falls with humans still in every loop |
| The evidence | ~70% non-selling share (Salesforce; a Forrester study of 3,000 reps lands near the same figure), barely changed in five years | Pure-replacement AI-SDR economics collapsed: 11x saw ~70-80% churn and ARR fall from ~$14M to ~$3M; survivors pivoted to augmentation |
| What to plan for | Productivity is the frame that wins with the field | Voice-gated role replacement is real but slower; ROI claims there are still vendor-reported and unaudited |
| Net effect | Headcount falls through productivity, not seat-for-seat replacement — finance books it as replacement either way |
```

```slide
archetype: quote
attribution: BCG, 2025
---
Design your company for AI, not AI for your company.
```

```slide
archetype: section-divider
title: An assessment-first program, not another tool pilot
subtitle: From an eight-week readiness assessment to a scaled operating model, instrumented for P&L impact from day one
xp-act: The program
```

```slide
archetype: timeline
kicker: The program
title: Three phases over eighteen months, and the first funded decision lands in week eight
axis: W0 :: M18
gate: 11% :: Week 8 :: first funded redesign decision
takeaway: Coverage, roles, comp, and process move together — sequential change failed in the XaaS transition and it fails here.
---
- Assess :: Weeks 1-8 :: AI-readiness and maturity assessment: data and retrieval governance, workflow inventory, value-pool sizing. :: span: 11 :: exit: Funded redesign decision, not a report
- Design and pilot :: Months 3-6 :: Redesign coverage, roles, comp, and process simultaneously, then pilot the redesigned workflow with the tools inside it. :: span: 22 :: exit: One revenue workflow live end-to-end
- Scale :: Months 6-18 :: Roll out the new operating model with change management across every role a sale touches. :: span: 67 :: exit: P&L instrumented from day one
```

```slide
archetype: framework
kicker: The program
title: Value concentrates where reinvention meets the full operating model
x-axis: Scope of change: point solution → operating model
y-axis: Depth of change: bolt-on → reinvention
plot: Tool pilots :: Most enterprise spend today
target: Reinvention :: Where the 18-month program lands
xp-plot: self
xp-read: Tool pilots :: You sit with most enterprise GenAI spend: licenses bolted onto the existing process. This is the zone where MIT finds 95% of pilots showing no measurable P&L impact.
xp-move: Tool pilots :: Both axes have to move. Redesign one revenue workflow end to end first, then take coverage, roles, comp, and process with it: depth before breadth.
xp-src: Tool pilots :: MIT, The GenAI Divide, 2025
xp-read: Workflow islands :: Real but local gains: one redesigned workflow with the tools inside it, and value capped by the surrounding organization.
xp-move: Workflow islands :: Widen the scope. The redesign that worked locally has to reach coverage, roles, comp, and process across the operating model, where BCG's 60%+ zone sits.
xp-src: Workflow islands :: BCG, 2025
xp-read: Platform sprawl :: Broad deployment across an untouched operating model: cost and change fatigue without measured value. The spend is wide; the process underneath has not changed.
xp-move: Platform sprawl :: Deepen the change. Pick the revenue workflows the platform already touches and redesign them end to end, with roles and comp moving too.
xp-src: Platform sprawl :: MIT, The GenAI Divide, 2025; BCG, 2025
xp-read: Reinvention :: You place yourself where the 18-month program lands: coverage, roles, comp, and process moving together. BCG measures 60%+ cost reduction here; MIT's value-creating ~5% live here.
xp-move: Reinvention :: Hold the bar. The open question is whether the P&L shows it: the program sets that measurement bar from day one.
xp-src: Reinvention :: BCG, 2025; MIT, The GenAI Divide, 2025
---
## Workflow islands
Real but local gains: one redesigned workflow with the tools inside it, value capped by the surrounding organization.
## Reinvention :: highlight
Coverage, roles, comp, and process move together: BCG's 60%+ cost-reduction zone, MIT's value-creating ~5%.
## Tool pilots
Where most GenAI spend sits today: licenses bolted onto the existing process. The 95% lives here.
## Platform sprawl
Broad deployment across an untouched operating model — cost and change fatigue without measured value.
```

```slide
archetype: comparison
kicker: The program
title: Bolt-on and reinvention look similar in month one and nothing alike in month twelve
highlight-col: 3
source: MIT, The GenAI Divide, 2025; BCG, 2025
---
| Dimension | Bolt-on | Reinvention |
| --- | --- | --- |
| What gets bought | Tools layered on the existing process | A redesigned workflow with tools inside it |
| Org change | Coverage, roles, comp untouched | Coverage, roles, comp, process move together |
| Measured result | 95% of pilots show no P&L impact (MIT) | ~5% of integrated systems create value (MIT) |
| Cost reduction | <20% (BCG) | 60%+ (BCG) |
| Who wins | Incumbent habits | AI-native challengers, and incumbents that redesign |
```

```slide
archetype: closing
title: Decisions we need from this group
contact: Curran Corrigan, EY
xp-act: Decisions
---
- Agree the scope of the 8-week AI-readiness assessment and name the executive sponsor :: — :: —
- Pick one revenue workflow for end-to-end redesign, not a tool pilot :: — :: —
- Set the measurement bar now: P&L impact and workflow-level metrics :: — :: —
```

# Appendix — backup exhibit (dense data variant).

```slide
archetype: data
kicker: Appendix
title: Every number in this deck traces to one of these rows
dense: true
---
| Study | Finding | Read-through |
| --- | --- | --- |
| MIT, The GenAI Divide (2025) | 95% of GenAI pilots show no measurable P&L impact | The failure is organizational, not technical; figure is directionally strong, methodologically contested |
| MIT, The GenAI Divide (2025) | ~5% of integrated systems create value | Integration into the workflow is the dividing line |
| BCG (2025) | 60%+ cost reduction with end-to-end process redesign | Redesign is the value unlock, not the tool |
| BCG (2025) | <20% cost reduction without process redesign | Tool-only deployments stall below the business case |
| McKinsey (2025) | High performers ~3x more likely to redesign workflows | Same signal from a second source |
| G2 buyer survey, n=1,076 (Mar 2026) | 51% start research with an AI chatbot over Google, up from 29% in 2025 | The pre-contact zone is expanding fast |
| G2 buyer survey, n=1,076 (Mar 2026) | 69% chose a different vendor than planned on AI guidance | Buyer-side AI already reroutes deals |
| Salesforce State of Sales | ~70% of rep time is not selling; Forrester (n=3,000) lands near the same figure | Augmentation's first target, barely moved in five years |
| Company reporting on 11x (2025-26) | ~70-80% churn; ARR ~$14M to ~$3M | Pure-replacement AI-SDR economics collapsed |
| Gartner (projection) | 90% of B2B buying AI-agent-touched by 2028; 75% of buyers still prefer human interaction by 2030 | Direction of travel, not a measurement |
```
