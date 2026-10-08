# AI rewires TD SYNNEX's two-cent distribution engine

*Prepared October 8, 2026 for an executive meeting with TD SYNNEX leadership. TD SYNNEX's fiscal year ends November 30 (FY2026 runs Dec 1, 2025 to Nov 30, 2026; Q1 ends Feb 28, Q2 May 31, Q3 Aug 31). "Gross billings" is the company's non-GAAP measure of what customers are invoiced before software, cloud and some Hyve sales are netted down to GAAP revenue. The underlying research relied largely on search-engine excerpts of SEC filings, earnings releases and trade press, because direct access to sec.gov and the investor-relations site was blocked. Figures marked "derived" are arithmetic on cited inputs. Figures marked "estimate" carry the confidence level the research assigned. Sections 1 to 8 are sourced facts. Sections 9 to 11 are interpretation.*

## Executive summary

**TD SYNNEX is the world's largest IT distributor, and FY2026 has turned it into an AI-infrastructure growth story.** It sits between roughly **2,500 technology vendors and more than 150,000 resellers, MSPs and integrators in 100+ countries** ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm)). In Q3 FY26 (ended Aug 31, 2026), **gross billings rose 40% to $31.8B and non-GAAP EPS rose 59% to $5.68** ([Q3 FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026063314/ex991-fy26q3pressrelease.htm)). Most of that growth came from Hyve Solutions, the company's hyperscale server design-and-manufacturing arm, whose billings more than doubled. The economics are thin: gross margin is about 6.6% of revenue, and FY2025 non-GAAP operating income was **roughly two cents per dollar billed** (derived). So the business depends on scale, vendor rebates, working capital and cost-to-serve. That makes the productivity of the commercial organization, not product margin, the main lever, and AI is the obvious tool for it.

The 2030 outlook points three ways at once:
- AI infrastructure spending keeps compounding: IDC forecasts **$758B by 2029** ([IDC](https://www.idc.com/resource-center/press-releases/artificial-intelligence-infrastructure-spending-to-reach-758bn-usd-mark-by-2029-according-to-idc/)).
- Hyperscaler marketplaces grow toward **$163B a year by 2030, with channel partners handling about 59%** ([IT Channel Oxygen](https://itchanneloxygen.com/channel-to-pocket-59-of-hyperscaler-marketplace-spend-by-2030-canalys)).
- Gartner expects AI agents to **intermediate more than $15 trillion of B2B spending by 2028** ([Digital Commerce 360](https://www.digitalcommerce360.com/2025/11/28/gartner-ai-agents-15-trillion-in-b2b-purchases-by-2028/)). Yet Gartner also expects **75% of B2B buyers to prefer human-led sales experiences in 2030** ([DestinationCRM](https://www.destinationcrm.com/Articles/CRM-Insights/Insight/Buyers-Are-Pushing-Back-Against-AI-171784.aspx)).

TD SYNNEX already has the building blocks: the PartnerFirst portal, an AI sales assistant inside Microsoft Teams, Slack and Webex (Digital Bridge), the StreamOne cloud marketplace, the Destination AI partner-enablement program and Hyve. What it does not publish is any outcome metric for AI in its own selling. Rival Ingram Micro reports **about $1B a quarter of net revenue through its AI assistant** ([IT Channel Oxygen](https://itchanneloxygen.com/ingram-micro-divulges-xvantage-vital-statistics-after-q2-overachievement/)). The core question for the meeting is how TD SYNNEX turns AI from something it sells into something that measurably changes how it sells, before partners' and buyers' own AI agents start deciding which distributor gets the order.

| At a glance | Figure (date) |
|---|---|
| Scale | FY2025 revenue $62.5B; gross billings ~$89.4B; ~24,000 full-time staff plus ~6,000 temporary (Nov 30, 2025) |
| Momentum | Q3 FY26 revenue $21.6B (+37.7%), gross billings $31.8B (+40.0%), non-GAAP EPS $5.68 (+58.7%) |
| FY2026 trajectory | ~$80.6B revenue and ~$118B gross billings (derived: Q1-Q3 actuals plus Q4 guidance midpoint) |
| Margins | Q3 FY26 gross margin 6.61% (vs 7.22%); non-GAAP operating margin 3.42% of revenue (2.31% of gross billings) |
| Mix, Q3 FY26 gross billings | Advanced Solutions 46%, Endpoint Solutions 32%, Hyve 22% (derived) |
| Largest vendors | Apple 12% and HP Inc. 10% of FY2025 revenue |
| Main rivals | Ingram Micro (#2 globally), Arrow (#3); Pax8 and ALSO in cloud and MSP channels |
| Leadership | CEO Patrick Zammit (since Sept 1, 2024); CFO David Jordan (since Oct 2025) |
| Watch-outs | Q3 FY26 free cash flow about -$1B; Hyve margin dilution; memory and component shortages |

## 1. A $89B billings middleman that keeps about two cents per dollar

TD SYNNEX came out of the merger of Tech Data and SYNNEX, a deal led by former CEO Rich Hume alongside Tech Data's Apollo take-private ([Channel Insider](https://www.channelinsider.com/news-and-trends/us/td-synnex-ceo-transition/)). It is headquartered in **Clearwater, Florida and Fremont, California**. It employs **about 24,000 full-time staff plus about 6,000 temporary or contract staff (Nov 30, 2025)** and serves **more than 150,000 reseller customers from more than 2,500 vendors in 100+ countries** ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm)). The 10-K describes an "edge-to-cloud" portfolio: cloud, cybersecurity, data and analytics, AI, IoT, mobility and everything-as-a-service. It adds systems design and integration of data center servers and networking built for customers' workloads. About **48% of FY2025 revenue came from outside the US**.

The model is classic two-tier distribution. TD SYNNEX buys from OEMs and software publishers and sells to the resellers, managed service providers (MSPs), system integrators and retailers who serve end customers. Its profit sits in a thin spread shaped by vendor money:
- **Rebates and price protection.** The 10-K says OEM incentive and rebate programs are "important determinants of the final sales price." Cost of revenue is recorded net of volume promotions, price protection and rebates.
- **Marketing reimbursements.** Vendor marketing and infrastructure reimbursements offset operating expenses.
- **Short, nonexclusive contracts.** Supplier agreements are usually nonexclusive, territory-specific, short-term and terminable without cause on short notice. On termination, suppliers generally buy back the inventory ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm); [FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000117739423000010/snx-20221130.htm)).
- **Subsidized financing.** OEMs subsidize the fees of third-party floor-plan lenders, or TD SYNNEX pays them.

In practice, TD SYNNEX makes money on the balance sheet (credit, inventory, logistics) and on vendor programs as much as on markup.

**Billings vs revenue.** The gap between gross billings and GAAP revenue is the first thing a newcomer needs to understand. Software, cloud subscriptions and some Hyve programs are booked "net", meaning only the margin counts as revenue. In FY2025, **revenue was $62.5B against gross billings of about $89.4B, a gap of about 30%** (derived), and net presentation cut reported revenue growth by **about $2.8B, or 5 points** ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm); [Q4 FY25 release](https://www.sec.gov/Archives/edgar/data/1177394/000162828026001271/ex991-fy25q4pressrelease.htm)). As more of the mix becomes software, revenue understates the business. Billings are the better gauge of scale, and revenue is the base for margin percentages.

**Earnings beyond product margin.** TD SYNNEX Capital offers:
- Amplify, short-term credit with 45-, 60-, 75- or 90-day terms ([Business Wire](https://www.businesswire.com/news/home/20230928640010/en/TD-SYNNEX-Capital-Introduces-New-Short-Term-Credit-Program-to-Empower-Partner-Growth)).
- 12-to-60-month payment plans on any IT product or service.
- In the UK, a Tech-as-a-Service product that funds the full term up front and takes credit risk off the partner ([ChannelWeb UK](https://channelweb.co.uk/news/4112793/td-synnex-capital-aims-eliminate-credit-risk-partners-flexible-finance-solutions)).

Lifecycle services run through Shyft Global Services and Renew, which expanded in Europe with Cordon Group in July 2025 for trade-in, data wiping, IT asset disposal and refurbishment ([PCR](https://pcr-online.biz/2025/07/07/td-synnex-lifecycle-with-cordon-group/)). The company does not disclose the size of any of these.

**Hyve Solutions is a different kind of business.** It "partners with leading technology companies to design, manufacture, and deliver traditional and accelerated compute, cloud, and connected infrastructure worldwide" ([Business Wire, Mar 2026](https://www.businesswire.com/news/home/20260303756016/en/TD-SYNNEX-to-Announce-First-Quarter-Fiscal-2026-Results-on-March-31-2026-Announces-Updated-Reportable-Segments)). It runs at least one program with each of the **top five US hyperscalers**. It is adding **more than 1 million square feet** of US manufacturing space, is an NVIDIA HGX design partner, and expects liquid-cooled networking racks in production in the first half of FY2027 ([Distribution Strategy, June 2026](https://distributionstrategy.com/2026/06/td-synnex-doubles-down-on-ai-hyperscalers-and-global-partnerships/)). One secondary source claims TD SYNNEX sold Hyve in 2022. That is wrong: 2026 insider filings still list Dennis Polk as Chair of Hyve Solutions ([Investing.com](https://www.investing.com/news/insider-trading-news/td-synnexs-dennis-polk-hyve-solutions-chair-sells-268m-in-stock-93CH-4771504)).

**Ownership.** Apollo exited fully through three secondary offerings between January and April 2024: about 26.2M shares for roughly **$2.8B** (derived). TD SYNNEX bought back shares alongside two of the offerings ([FY2025 proxy](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000016/fy24proxystatement.htm)).

## 2. FY2026 billings are on track for roughly +32% as Hyve doubles

**FY2024 and FY2025 were modest.** FY2024 revenue was flat (+1.6%). FY2025 revenue grew 6.9% and billings grew about 12%. Management said the business excluding Hyve grew billings "in the high single digits" in FY2025 ([Q4 FY25 call summary](https://finance.yahoo.com/news/td-synnex-q4-earnings-call-154000551.html)).

| Metric | FY2024 (ended Nov 30, 2024) | FY2025 (ended Nov 30, 2025) | Source / confidence |
|---|---|---|---|
| Revenue (GAAP) | $58.45B (+1.6%) | $62.51B (+6.9%; +6.1% constant currency) | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm); high |
| Non-GAAP gross billings | $80.1B | $89.4B (+11.7%) | [Q4 FY25 release](https://www.sec.gov/Archives/edgar/data/1177394/000162828026001271/ex991-fy25q4pressrelease.htm); medium-high (search excerpt) |
| Gross margin | not retrieved | 6.99% | Secondary summary of 10-K; medium |
| Non-GAAP operating income | ~$1.63B (2.78% of revenue) | ~$1.78B (+9.7%; 2.86%) | 10-K via search excerpt; medium |
| GAAP net income | $689.1M | $827.7M (+20.1%) | [FY24 8-K](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000002/ex991-fy24q4pressrelease.htm); 10-K |
| GAAP diluted EPS | $7.95 | $9.95 | FY25 from aggregator [StockTitan](https://www.stocktitan.net/financials/SNX/); medium |
| Non-GAAP diluted EPS | $11.68 (likely, unconfirmed) | ~$13.20 (derived sum of quarters; not company-reported) | Low-medium |
| Revenue by region | not retrieved | Americas $36.18B (+4.0%); Europe $21.70B (+10.5%); APJ $4.64B (+15.2%) | 10-K; high |
| Gross billings by region | Americas $49.66B; Europe $25.40B; APJ $5.00B | Americas $54.08B; Europe $29.01B; APJ $6.34B | Q4 FY25 release reconciliation; medium-high |
| Shareholder returns | not retrieved | $742M | Call summary; medium |

*Regional figures for FY2024 and FY2025 use the old three-segment basis, with Hyve inside Americas. They are not comparable with FY2026 regional figures, which exclude Hyve.*

**FY2026 accelerated sharply.** The company beat the high end of its own guidance in every quarter. Q3 FY26 guidance was about **$27.7B of billings and $4.50 of non-GAAP EPS. Actual results were $31.8B and $5.68** ([Alpha Spread](https://www.alphaspread.com/security/nyse/snx/investor-relations/earnings-call/q2-2026); [Q3 FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026063314/ex991-fy26q3pressrelease.htm)).

| Metric | Q4 FY25 (ended Nov 30, 2025) | Q1 FY26 (ended Feb 28, 2026) | Q2 FY26 (ended May 31, 2026) | Q3 FY26 (ended Aug 31, 2026) | Q4 FY26 guidance (ends Nov 30, 2026) |
|---|---|---|---|---|---|
| Reported | Jan 8, 2026 | Mar 31, 2026 | Jun 25, 2026 | Sep 24, 2026 | ~Jan 2027 |
| Revenue | $17.4B (+9.7%) | $17.2B (+18.1%) | $19.58B (+31.0%) | $21.56B (+37.7%) | $21.8-22.6B |
| Non-GAAP gross billings | $24.3B (+14.7%) | $25.8B (+24.4%) | $28.9B (+33.4%) | $31.8B (+40.0%) | $31.4-32.4B |
| Gross margin | 6.87% | not retrieved | 6.84% (vs 7.00%) | 6.61% (vs 7.22%) | — |
| Non-GAAP operating income | $497M (+17.9%) | ~$590M (derived: Distribution $431M + Hyve $159M) | $615M (+48.5%) | $736M (+55.1%) | — |
| GAAP diluted EPS | $3.04 | $4.04 | $4.15 | $5.18 (+89.1%) | $4.58-5.08 |
| Non-GAAP diluted EPS | $3.83 (+24.0%) | $4.73 (+68.9%) | $4.85 (+62.2%) | $5.68 (+58.7%) | $5.65-6.15 |
| Hyve gross billings | $3.68B (>+50%) | $3.82B (+95%) | $5.46B (+117%) | $7.01B (+117%) | Guided up sequentially |
| Distribution gross billings | ~$20.6B (derived) | $22.0B (+17%) | $23.4B (+22%) | $24.8B (+27%) | — |
| Free cash flow | +$1.4B | not retrieved | ~-$330M (AI-generated summary, unverified) | ~-$1.0B (-$975.6M per secondary source) | Mgmt expects improvement |
| Capital returned | $209M | not retrieved | $151M | $139M | Dividend $0.48/qtr (+9%) |

Sources: [Q4 FY25 release](https://s21.q4cdn.com/109490932/files/doc_financials/2025/q4/TD-SYNNEX-Q4-FY25-Press-Release-vFinal.pdf); [Q1 FY26 8-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026022204/ex991-fy26q1pressrelease.htm); [Q2 FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026045349/ex991-fy26q2pressrelease.htm); [Q3 FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026063314/ex991-fy26q3pressrelease.htm); [Q2 FY26 supplemental](https://s21.q4cdn.com/109490932/files/doc_financials/2026/q2/FQ2-26-SNX-Supplemental-Financial-vFinal.pdf); [Q3 FY26 call highlights](https://finance.yahoo.com/markets/stocks/articles/td-synnex-q3-earnings-call-150335018.html); [MarketChameleon](https://marketchameleon.com/articles/b/2026/9/24/snx-record-fiscal-2026-q3-results-revenue-eps-outlook-dividend).

**FY2026 run rate.** Revenue for Q1-Q3 FY26 totals about **$58.4B**, already close to all of FY2025. With the Q4 guidance midpoint, FY2026 implies about **$80.6B of revenue and about $118B of gross billings, roughly 32% billings growth** (derived). The April 2025 investor-day aspiration was **about 5% annual billings growth** ([2025 Investor Day 8-K](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000033/ex991tdsynnexhosts2025inve.htm)). The Q4 guidance midpoint ($31.9B) is flat against Q3. That implies either a plateau or conservative guidance.

**Margins.** Gross margin keeps falling (7.22% to 6.61% year over year in Q3) because low-margin AI server programs and large North American infrastructure deals dilute it. Management attributes this to mix, not price erosion. Operating margin is rising anyway because costs are not growing as fast as volume.

**A reporting conflict to know about.** Company-sourced summaries put the Q3 non-GAAP operating margin at **3.42%**, while one Investing.com article said 2.31%. Both are arithmetically right. $736M is 3.41% of revenue and 2.31% of gross billings. Use the revenue basis when comparing with company targets ([TradingView](https://www.tradingview.com/news/tradingview:1edf60b61b7ea:0-td-synnex-reports-record-q3-fiscal-2026-revenue-21-6b-non-gaap-eps-5-68/); [Investing.com](https://in.investing.com/news/stock-market-news/td-synnex-q3-2026-slides-record-results-mask-margin-cash-concerns-93CH-5605270)).

**Cash is the pressure point.** Q3 FY26 free cash flow was about **-$1B**, driven by inventory and working capital for Hyve programs. Net working capital reached **$6.5B**, and the cash conversion cycle lengthened by 6 days year over year ([Q3 call highlights](https://finance.yahoo.com/markets/stocks/articles/td-synnex-q3-earnings-call-150335018.html)). Long-term borrowings were about $3.59B at Q2 ([Alpha Spread](https://www.alphaspread.com/security/nyse/snx/investor-relations/earnings-call/q2-2026)). Buybacks fell from $173M in Q4 FY25 to about $100M in Q3 FY26. Management still holds its long-term target of converting **95% of non-GAAP net income into free cash flow**. The stock fell after the Q3 beat, which one outlet attributed to cash and margin concerns ([Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-td-synnex-tops-q3-2026-forecasts-but-shares-fall-93CH-4915629)).

## 3. Three businesses with very different economics: Endpoint, Advanced and Hyve

**Segment reporting.** Since Q1 FY26, TD SYNNEX reports four segments: **Americas, Europe and APJ (together, "Distribution"), plus Hyve Solutions** as a global segment. The CEO is the chief operating decision-maker ([Q1 FY26 10-Q](https://www.sec.gov/Archives/edgar/data/1177394/000162828026023123/snx-20260228.htm)). Inside Distribution, the company also reports two product portfolios:
- **Endpoint Solutions:** PCs, mobile phones and accessories, printers, peripherals, supplies, endpoint software and consumer electronics.
- **Advanced Solutions:** data center technologies such as hybrid cloud, security, storage, networking, servers, software and converged infrastructure.

Through FY2025, Hyve sat inside Advanced Solutions ([FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000009/snx-20241130.htm)). As a result, **FY2026 Advanced Solutions growth rates are not comparable with FY2025's**. The like-for-like FY2025 comparison is Advanced excluding Hyve, which grew 8% in Q4 FY25 and 10% in Q2 FY25.

**Reported segment mix, Q3 FY26 (quarter ended Aug 31, 2026). Confidence: high (10-Q revenue; segment profit from call summaries).**

| Segment | Revenue | Share of revenue | Gross billings | Share of billings | Non-GAAP operating income | Share of op. income |
|---|---|---|---|---|---|---|
| Americas | $10.32B | 47.9% | not retrieved | — | not retrieved | — |
| Europe | $6.37B | 29.5% | not retrieved | — | +116% y/y (dollars not retrieved) | — |
| APJ | $1.07B (+21.7%) | 5.0% | not retrieved | — | not retrieved | — |
| **Distribution subtotal** | $17.76B | 82.4% | $24.8B (+27%) | 78% | $483.5M (+55%) | ~66% |
| **Hyve Solutions** | $3.80B (+52%) | 17.6% | $7.01B (+117%) | 22% | ~$253M (+56%) | ~34% |
| **Total** | $21.56B | 100% | $31.8B | 100% | $736M | 100% |

Sources: [Q3 FY26 10-Q](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026064256/snx-20260831.htm); [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/td-synnex-q3-earnings-beat-112300659.html); [Motley Fool transcript](https://www.fool.com/earnings/call-transcripts/2026/09/24/td-synnex-snx-q3-2026-earnings-call-transcript/). One third-party analysis puts Hyve at 38.8% of operating profit, which does not match the 34% derived from the reported dollars ([Beancount](https://beancount.io/pt/blog/2026/10/05/td-synnex-fy2026-q3-earnings-analysis)).

**Portfolio mix by gross billings.** TD SYNNEX does not publish full-year Endpoint and Advanced totals in anything the research could access. The FY2025 figures below are therefore **estimates** rebuilt from quarterly disclosures. They reconcile to the reported Q3 FY25 total of $22.7B, which validates the method.

| Bucket | FY2025 estimate | Share FY2025 | Q3 FY26 reported | Share Q3 FY26 | Q3 FY26 growth | Confidence |
|---|---|---|---|---|---|---|
| Endpoint Solutions | ~$35-36B | ~40% | $10.3B | 32% | +16% | FY25 medium; Q3 high |
| Advanced Solutions excl. Hyve | ~$42-43B | ~47-48% | $14.5B | 46% | +37% | FY25 medium; Q3 high |
| Hyve Solutions | ~$11.4B (sum of reported quarters) | ~12.7% | $7.0B | 22% | +117% | High |
| Total | ~$89.4B | 100% | $31.8B | 100% | +40% | High |

On a **revenue** basis, the picture flips, because software in Advanced Solutions is booked net. The research estimates that in FY2025 Endpoint was **~54% of revenue**, Advanced excluding Hyve ~36% and Hyve ~10%. Confidence is low to medium ([Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/09/24/td-synnex-snx-q3-2026-earnings-call-transcript/); [Investing.com Q2 FY25](https://ca.investing.com/news/company-news/td-synnex-q2-2025-slides-12-gross-billings-growth-despite-eps-challenges-93CH-4075943)).

**Product categories below the bucket level are not disclosed at all.** The research found no company, broker or analyst split. The table below is the research team's own triangulation, anchored only on Apple (~$7.5B) and HP (~$6.3B) FY2025 revenue. It is a rough sizing, not a reportable fact.

| Category (FY2025 gross billings, ESTIMATE) | Est. billings | Est. share | Confidence |
|---|---|---|---|
| PCs (notebooks, desktops, Mac, Chromebooks) | ~$18-21B | 20-23% | Low |
| Mobile (phones, tablets) | ~$5-7B | 6-8% | Low |
| Peripherals, printers, supplies, accessories, consumer electronics, endpoint software | ~$8-10B | 9-11% | Low |
| Software, SaaS, cloud marketplaces, security software | ~$15-22B | 17-25% | Very low |
| Servers, storage, networking, converged infrastructure (non-Hyve) | ~$20-27B | 22-30% | Very low |
| Hyve (hyperscale ODM/AI racks; ~2/3 manufacturing, ~1/3 supply-chain services in Q3 FY26) | ~$11.4B | ~12.7% | High |
| Stand-alone services | Not separable | n/a | n/a |

**Where growth is coming from.**
- **AI infrastructure leads.** Hyve billings grew more than 50% in Q4 FY25, 95% in Q1 FY26 and 117% in both Q2 and Q3 FY26. The matching +117% figures are not an error: $5.46B vs $2.52B and $7.01B vs $3.22B ([Q3 FY26 supplemental](https://s21.q4cdn.com/109490932/files/content_files/FQ326-SNX-Supplemental-Financial-vFinal.pdf)).
- **Advanced Solutions is next,** up 37% in Q3 FY26 on "infrastructure, software, and AI-related technologies." The quarter included a deal with VAR Mark III Systems (some sources spell it "Mach3") for an **NVIDIA AI factory on Vera Rubin NVL72** systems. The CEO called it one of the largest enterprise AI factory deployments expected through the channel. TD SYNNEX supplies design, integration, deployment, co-administration, financing and supply chain ([Channel Dive](https://www.channeldive.com/news/td-synnex-mark-3-systems-nvidia-ai-factory/831399/)).
- **Endpoint is growing on price, not units:** +16% in Q3 with "higher average selling prices and a modest decline in units." **AI PCs are close to 50% of personal-computing revenue** ([GuruFocus](https://www.gurufocus.com/news/9096085/td-synnex-corp-snx-q3-2026-earnings-call-highlights-record-billings-surge-40-as-ai-infrastructure-demand-accelerates)). The CFO estimated that about **two points of Q1 FY26 billings growth came from higher prices and pull-forward**, as OEMs passed through memory costs ([Channel Dive](https://www.channeldive.com/news/td-synnex-q1-2026-revenue-growth-component-price-hikes/816275/)).
- **Category outlook.** CEO Zammit expects PCs, cybersecurity, cloud, software and servers to grow strongly in 2026, and is more cautious on storage and networking ([IT Channel Oxygen](https://itchanneloxygen.com/td-synnex-ceo-on-european-portfolio-gaps-exertis-rightsizing-and-kit-shortages/)).

**Hyve's growth comes with risks.**
- **Customer concentration.** Hyve is ramping three new hyperscale customers. New programs are mostly networking and described as margin neutral to accretive, but will not reach full margin until the second half of FY2027, and some contracts carry cancellation rights ([MarketBeat](https://www.marketbeat.com/instant-alerts/transcript-td-synnex-q3-earnings-call-highlights-2026-09-24/)). One unnamed customer was **11% of FY2025 revenue** (12% in FY2024). The 10-K links this to the systems design and integration line, which points to a Hyve hyperscaler, but the customer is not named.
- **Amazon warrant.** A secondary source reports an Amazon equity warrant for about **3.2M shares**, issued in May 2026 and vesting on revenue thresholds tied to Hyve ([Webull](https://www.webull.com/news/15634357347550208)). Its terms are unverified.

**Regional growth.** Europe is outgrowing the Americas: FY2025 revenue +10.5%, Q1 FY26 billings +25%, and Q3 FY26 non-GAAP operating income +116%. APJ is small (~5% of revenue) but growing fast.

## 4. Strategy has narrowed to AI infrastructure, digital channels and specialization

**Leadership.** Patrick Zammit became CEO **effective September 1, 2024**. He succeeded Rich Hume after serving as COO from January 2024 ([Business Wire](https://www.businesswire.com/news/home/20240619892207/en); [Channel Insider](https://www.channelinsider.com/news-and-trends/us/td-synnex-ceo-transition/)). He started his career at Avnet, ran Europe from 2017 and added APJ in 2021. One research note initially carried a September 2025 start date. The verification pass found 2024 consistent across multiple sources, so treat 2024 as correct. Other leaders:
- **David Jordan** became EVP and CFO in October 2025, replacing Marshall Witt. He was previously Americas CFO and head of investor relations ([Business Wire](https://www.businesswire.com/news/home/20251002799791/en/TD-SYNNEX-Announces-CFO-Transition)).
- **Reyna Thompson** became President, North America on Dec 1, 2024. She previously led North America Advanced Solutions, which serves "over 12,000 channel partners" ([TD SYNNEX release](https://s21.q4cdn.com/109490932/files/doc_news/2024/09/1/TD-SYNNEX-to-Appoint-Reyna-Thompson-President-North-America-2024.pdf)).
- **Wendy Welch** became SVP Public Sector Sales in May 2026, covering Federal, state and local government and education, including DLT Solutions ([Business Wire](https://www.businesswire.com/news/home/20260512914047/en/TD-SYNNEX-Accelerates-Investment-in-U.S.-Public-Sector-Business-at-Annual-Red-White-You-Event)).
- **Sergio Farache** is chief strategy and technology officer ([ChannelWeb UK](https://www.channelweb.co.uk/news-network/2026/hpe-taps-td-synnex-ingram-micro-as-global-distribution-backbone-in-post-juniper-acquisition-channel-reset)).
- **Douglas Britt** joined the board in June 2026, expanding it from ten to eleven members ([SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001177394/000162828026044641/snx-20260617.htm)).

**Formal targets: the record conflicts on which investor day is the latest.** The March 2022 investor day set four pillars: strengthen the end-to-end portfolio, invest in high-growth technologies, digitally transform the business, expand the global footprint. It framed TD SYNNEX as a "solutions orchestrator." Medium-term targets were **6-7% revenue CAGR, ~3% non-GAAP operating margin and 15-20% total shareholder return** ([Business Wire](https://www.businesswire.com/news/home/20220329005663/en/TD-SYNNEX-Hosts-2022-Virtual-Investor-Day-and-Outlines-Key-Strategic-Growth-Initiatives-and-Medium-Term-Outlook/)). The strategy research found no later investor day. The go-to-market research, however, cites an **April 10, 2025 investor day** 8-K with newer medium-term aspirations: **~5% gross-billings CAGR, 10-12%+ EPS CAGR and 95% free-cash-flow conversion**. Its listed initiatives included marketplace and digital sales, financing and everything-as-a-service, cloud/IaaS, SMB/MSP/CSP and data/AI ([8-K](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000033/ex991tdsynnexhosts2025inve.htm)). The 2025 document is primary and more recent, so treat its targets as current. The 95% FCF figure management repeated in June 2026 matches it. FY2026 is far ahead of the growth target and far behind the cash target.

**Zammit's operating priorities**, pieced together from earnings calls and interviews rather than a single strategy document, fall into three groups.

*Commercial model.* On the Q2 FY26 call he described three commercial pillars ([Benzinga](https://www.benzinga.com/news/26/06/60099131/td-synnex-q2-2026-earnings-call-transcript)):
- **Omnichannel engagement:** digital self-serve "when they want speed" and humans "when they want expertise," enabled by PartnerFirst and machine-learning, generative and agentic AI.
- **Specialization:** "we segment our commercial teams in groups of specialists," tier the customer base strategically and "in some cases we reallocate resources monthly."
- **Investment in enablement.**

He also said SMB customers are growing "well above market." A Q1 transcript summary referred to "four strategic pillars," so the framing varies by call.

*Market view* ([Computer Weekly](https://www.computerweekly.com/microscope/news/366651273/TD-Synnex-boss-talks-of-widening-AI-impact)):
- Enterprises are moving from AI experiments to production "AI factory" deployments.
- AI creates new security, governance and compliance needs, and financial operations and security operations will grow in importance.
- Vendors increasingly want partners that can reach customers, activate demand and execute globally, which raises distribution's strategic value.

*Admitted weak spots* ([IT Channel Oxygen](https://itchanneloxygen.com/td-synnex-ceo-on-european-portfolio-gaps-exertis-rightsizing-and-kit-shortages/)):
- TD SYNNEX is missing "some important cybersecurity vendors" in Europe.
- Memory shortages will create "a lot of tensions" with vendors, partners and end users.

**M&A is small and platform-focused:**
- **Apptium**, the cloud-commerce engine behind StreamOne, acquired July 1, 2025 for about **$105.1M** ([TD SYNNEX news](https://news.tdsynnex.com/featured/td-synnex-acquires-apptium-to-accelerate-innovation-breadth-of-cloud-and-everything-as-a-service-offerings/)).
- **Gateway Computer** in Japan, October 2025 ([TD SYNNEX release](https://s21.q4cdn.com/109490932/files/doc_news/TD-SYNNEX-Completes-Share-Acquisition-of-Gateway-Computer-Corporation-a-Japanese-IT-Solutions-and-Services-Provider-2025.pdf)).
- **Exclusive Networks Poland's** AV/unified-communications and gaming units, around January 2026 ([Installation International](https://www.installation-international.com/business/acquisitions/td-synnex-completes-polish-av-uc-acquisition)).

The newest partnership is a **global distribution agreement with Siemens, signed Oct 5, 2026**, covering industrial automation, software and AI, cybersecurity and electrification ([Distribution Strategy](https://distributionstrategy.com/2026/10/td-synnex-siemens-launch-global-distribution-partnership-for-industrial-ai/)). It extends TD SYNNEX into operational technology.

**Sustainability.** TD SYNNEX has Science Based Targets initiative (SBTi) approved climate targets. It met its 2030 Scope 1+2 goal early, with emissions **down nearly 43% since 2022** ([ChannelWeb UK](https://www.channelweb.co.uk/news/2025/td-synnex-achieves-2030-climate-targets-ahead-of-schedule)).

## 5. Reaching 150,000 partners through specialists, portals and marketplaces

**Who TD SYNNEX sells to.** It reaches end customers almost entirely indirectly, through VARs, ISVs, system integrators, MSPs, retailers and public-sector specialists. The exception is Hyve, which sells directly to hyperscalers.

**How the commercial organization is structured.** Regional presidents lead North America, Europe, APJ and Latin America and the Caribbean. In North America, Advanced Solutions acts as a specialist overlay with named practices: CloudSolv, CyberSolv, Public Sector and Destination AI ([Channel Drive](https://channeldrive.in/people/td-synnex-to-appoint-reyna-thompson-as-president-north-america/)). No public source describes the split between inside and field sales, vendor business units or headcount by role. The "specialists plus tiers plus monthly reallocation" language is the best public description of the coverage model.

**How partners transact.** There are four main routes:
- **PartnerFirst**, a unified portal launched in North America in September 2025 and in Europe in July 2026, where it consolidated the InTouch and Software Store portals ([Business Wire](https://www.businesswire.com/news/home/20250925575232/en/Introducing-TD-SYNNEX-PartnerFirst-a-Unified-Digital-Portal-for-Enhanced-Partner-Experience); [IT Social](https://itsocial.fr/tech-digital/tech-digital-actualites/distribution-it-td-synnex-deploie-partnerfirst-son-guichet-numerique-unifie-pour-les-revendeurs-europeens/)).
- **Legacy EC Express** and real-time XML/API integrations used by quoting and PSA tools.
- **Digital Bridge**, an integration layer launched in January 2025. Its AI assistant started in Microsoft Teams, then Slack and Webex. It pulls live pricing, stock and documentation, and turns pasted SKU lists into quotes. Connectors for Salesforce and QuickBooks Online went live in August 2026 ([Digital Bridge AI agent page](https://www.tdsynnex.com/na/us/digital-bridge/ai-agent/); [Distribution Strategy](https://distributionstrategy.com/2026/08/td-synnex-expands-digital-commerce-platform-with-ai-and-sales-automation/)).
- **Human reps.**

On the January 2026 call, management said a new AI assistant lets customers transact in self-service mode 24/7 inside PartnerFirst. In 2026, PartnerFirst added two capabilities: campaign tools for nurturing resellers and end users, and **lifecycle-stage analysis (close, renewal, upsell, churn) for Microsoft and Cisco** ([Channel Insider](https://www.channelinsider.com/channel-business/td-synnex-partnerfirst-ai-lifecycle-tools/)). The company is "building machine learning, generative AI and agentic AI into PartnerFirst" to recommend products and flag opportunities ([Distribution Strategy](https://distributionstrategy.com/2026/06/td-synnex-doubles-down-on-ai-hyperscalers-and-global-partnerships/)). It discloses no share of orders by channel (digital vs rep) and no outcome metrics for Digital Bridge.

**The cloud and MSP motion runs through StreamOne.**
- **The platform.** StreamOne Ion is the current-generation cloud marketplace. It offers PSA connectors for ConnectWise and Autotask, a headless commerce API and white-label storefronts, which reached the UK and Ireland in May 2026 ([Business Wire Nov 2024](https://www.businesswire.com/news/home/20241112213300/en/TD-SYNNEX-Elevates-StreamOne-with-New-Commerce-and-Security-Capabilities); [PCR](https://pcr-online.biz/2026/05/18/td-synnex-makes-streamone-uki/)).
- **Adoption figures conflict.** The November 2024 release and CEO Zammit in 2025 cite **30,000 active partners and 500,000 end users** ([ChannelWeb](https://channelweb.co.uk/news-network/2025/td-synnex-ceo-patrick-zammit-on-streamone-cloud-marketplace-growth-tariffs-and-broadcom-ceo-hock-tan-s-channel-commitment)). Another executive's comments reported by CRN Asia say "20,000+ partners actively working in the platform" ([CRN Asia](https://www.crnasia.com/news-network/2025/td-synnex-to-bolster-digital-commerce)). The 30,000 figure is the company's headline number, but it is now about a year old. A narrower metric, 8,000+ North American resellers transacting, dates from November 2024.
- **Hyperscaler and Microsoft ties.** AWS Marketplace offers are sold through StreamOne Stellr, with TD SYNNEX as Designated Seller of Record under an AWS Strategic Collaboration Agreement signed August 2025 ([Business Wire](https://www.businesswire.com/news/home/20250827433532/en/TD-SYNNEX-Signs-Strategic-Collaboration-Agreement-with-AWS-to-Accelerate-Cloud-and-AI-Adoption-Across-the-Americas)). TD SYNNEX earned Microsoft's new **"Frontier Distributor"** designation in March 2026, the second distributor to do so after Ingram Micro ([CRN Australia](https://www.crn.com.au/news/2026/distributor/tech-data-receives-microsoft-frontier-distributor-status)).
- **MSP program.** MSP Evolve launched in May 2024 ([Business Wire](https://www.businesswire.com/news/home/20240521971059/en/TD-SYNNEX-Introduces-MSP-Evolve-to-Empower-MSP-Growth-Strategies)).
- **No cloud revenue figure.** TD SYNNEX discloses no cloud revenue, ARR or StreamOne billings figure.

**Communities and enablement.**
- **PartnerLINK.** In April 2025, North American partner communities were restructured into PartnerLINK, which replaced the legacy TechSelect, Varnex and CommunitySolv structures. It has four communities: Ascend, Advantage, Canada and a Public Sector option ([Business Wire](https://www.businesswire.com/news/home/20250422504630/en/TD-SYNNEX-Prepares-Partners-for-Market-Evolution-With-New-Specialized-Community-Structure)). In 2022, the legacy communities had **1,200+ members with $6.3B of buying power** ([Channel Futures](https://channelfutures.com/distribution/td-synnex-vp-discusses-unifying-partner-communities-post-merger)).
- **Partner Loyalty program.** Launched May 2025, it is tiered and rewards Advanced Solutions growth with training, event travel credit, StreamOne credit and preferential financing ([Business Wire](https://www.businesswire.com/news/home/20250513461477/en/TD-SYNNEX-Accelerates-Innovation-and-Growth-Through-New-Partner-Loyalty-Program)).
- **Destination AI.** Launched August 2023 and the main AI enablement program, it bundles reference architectures, Practice Builder training, demos and proof-of-value support, and 40+ AI vendors in the catalog ([Business Wire](https://www.businesswire.com/news/home/20230815618891/en/TD-SYNNEX-Launches-Destination-AI-Program-to-Support-Partner-Enablement)). The Practice Accelerator (October 2024) added six-week cohorts. A May 2025 "next phase" added the Solution Grid and Aware/Ready/Expert partner profiling ([Business Wire](https://www.businesswire.com/news/home/20250514898978/en/TD-SYNNEX-Unveils-Next-Phase-of-Destination-AI-to-Operationalize-Partners-AI-Strategies)). In October 2025, TD SYNNEX added GPU capacity on Nebius, and in April 2026 it reserved dedicated HGX B300 clusters there. In July 2026 it opened an **AI Factory in Paris with NVIDIA and Cisco** for EMEA partners ([ITreseller.ch](https://www.itreseller.ch/Artikel/105793/TD_Synnex_eroeffnet_KI-Factory_fuer_Kunden_in_Europa.html)).
- **No adoption figures.** The company publishes no enrollment or revenue metrics for Destination AI.

| Program / platform | What it is | Launched / latest | Scale disclosed |
|---|---|---|---|
| PartnerFirst | Unified digital portal: commerce, StreamOne, enablement, loyalty, campaigns, lifecycle analytics, Services Marketplace with AI search | NA Sept 2025; Europe July 2026; AI features 2026 | None |
| Digital Bridge | Integration layer and AI assistant in Teams, Slack, Webex; Salesforce and QuickBooks connectors | Jan 2025; connectors Aug 2026 | "Thousands" of partners |
| StreamOne Ion / Stellr | Cloud and SaaS marketplace, PSA integration, white-label storefronts, AWS Marketplace seller-of-record | Ion migration 2024-25; UK&I storefronts May 2026; Apptium acquired Jul 2025 | 30,000 partners / 500k end users (2024-25; 20,000+ per another exec) |
| Destination AI | AI enablement: Practice Builder, Practice Accelerator, Solution Grid, Innovation Centers, Nebius GPU cloud, Paris AI Factory | Aug 2023; phases Oct 2024, May 2025; Paris Jul 2026 | 40+ AI vendors; 250+ UK partners at one event |
| PartnerLINK | NA partner communities (Ascend, Advantage, Canada, Public Sector) | Apr 2025 | Legacy communities 1,200+ members (2022) |
| Partner Loyalty | Tiered rewards favoring Advanced Solutions growth | May 2025 | None |
| MSP Evolve | MSP tools, training, StreamOne access | May 2024 | None |
| CloudSolv / CyberSolv / SOC-as-a-Service | NA Advanced Solutions practices | Ongoing | Four programs rated 5-star in CRN 2025 guide |
| TD SYNNEX Capital / Amplify | Short-term credit (45-90 days), 12-60 month financing, UK Tech-as-a-Service | Amplify Sept 2023 | None |
| Public Sector / DLT | Federal and SLED unit; contract vehicles (NCPA, Equalis) | New SVP May 2026 | None |
| Events | Inspire (NA, Oct 7-9, 2026 per third-party listing; LAC ~700 leaders), Red, White & You, High-Growth Conference | Annual | — |

**Partner pain points.** The research found no credible partner survey on TD SYNNEX. The available signals are indirect:
- **Loyalty program skepticism.** One critique questions whether the loyalty tiers improve partner profitability or just add another tier to climb ([Business of Tech](https://businessof.tech/?p=11243)).
- **Supply shortages.** UK partners face possible "pandemic levels" of kit shortages in 2026.
- **Europe security gaps.** The CEO himself acknowledged missing cybersecurity vendors in Europe.
- **Portal sprawl.** The consolidation onto PartnerFirst and the StreamOne Ion migration suggest the post-merger portal landscape was fragmented.

## 6. Vendors are consolidating around two global distributors

**Vendor concentration.**
- **Two vendors cross the 10%-of-revenue threshold:** **Apple at 12% of FY2025 revenue (12% in FY2024, 11% in FY2023) and HP Inc. at 10% in FY2025** (below 10% earlier). That is roughly $7.5B and $6.3B (derived) ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm)).
- **Other primary suppliers** named in the filings are Cisco, Dell, HPE, IBM, Lenovo, Microsoft and Samsung ([FY2024 annual report](https://www.sec.gov/Archives/edgar/data/1177394/000117739425000018/ars.pdf)). None is quantified.
- **Concentration relative to Endpoint.** Measured against estimated Endpoint revenue, Apple and HP are roughly 22% and 19% (estimate). Hyve's growth will probably push both below their current shares of total revenue in FY2026.

**Vendors are trimming their distributor lists, and TD SYNNEX is mostly on the winning side.**
- **HPE.** After acquiring Juniper, HPE named **Ingram Micro and TD SYNNEX as its two global distribution partners on May 14, 2026** ([HPE](https://www.hpe.com/us/en/newsroom/press-release/2026/05/hpe-unifies-global-distribution-with-ingram-micro-and-td-synnex.html)). One Q2 call summary said "HP" chose TD SYNNEX as one of two global distributors. No HP Inc. announcement exists, and this is likely a mix-up with HPE.
- **Microsoft.** The Frontier Distributor tier (March 2026) followed CSP authorization rules, effective October 1, 2025, that partner-source summaries describe as including about $30M of trailing revenue per region ([Pax8](https://www.pax8.com/blog/microsoft-csp-changes/)).
- **Broadcom/VMware.** Broadcom culled VMware service-provider partners in 2025 but **added nine European territories** to TD SYNNEX's distribution agreement ([ChannelWeb UK](https://www.channelweb.co.uk/news/4189399/vmware-adds-territories-td-synnex-distribution-agreement-amid-overall-partner-cull)).
- **Cisco.** Cisco launched its Cisco 360 partner program on February 1, 2026, consolidating incentives and trimming some rebates ([SDxCentral](https://www.sdxcentral.com/articles/cisco-deals-deadlines-for-partner-program-overhaul/2025/03/)).

The pattern is consistent: vendors cut the long tail and keep a few scaled distributors. That helps TD SYNNEX, but it also means every major vendor relationship is now a two-horse race with Ingram.

**AI ecosystem position.**
- **NVIDIA.** TD SYNNEX was NVIDIA's **EMEA Distributor of the Year for 2026**, its first top overall EMEA award, and Americas Distributor of the Year for 2025 for the second year running ([Dutch IT Channel](https://www.dutchitchannel.nl/news/729796/td-synnex-is-nvidia-emea-distributeur-van-het-jaar-2026); [Business Wire](https://www.businesswire.com/news/home/20250319046522/en)).
- **HPE.** TD SYNNEX expanded HPE Unleash AI solutions in June 2026.
- **Dell.** It signed Dell AI Factory agreements in Asia.
- **Hyperscalers and AI clouds.** Its hyperscaler relationships run through Hyve, and it reserves GPU capacity from AI-native cloud provider Nebius.
- **Software.** SAS made TD SYNNEX its primary global distributor in 2023 ([Nasdaq](https://www.nasdaq.com/press-release/ai-and-analytics-leader-sas-selects-td-synnex-as-primary-global-distribution-partner)).
- **Gaps.** No AMD, Intel-specific, Supermicro or Microsoft Copilot distribution agreements surfaced in the research. That is not proof they don't exist.

| Vendor | Relationship highlights (dated) | Strategic significance |
|---|---|---|
| Apple | 12% of FY2025 revenue (largest vendor) | Endpoint anchor; concentration risk |
| HP Inc. | 10% of FY2025 revenue (first time above 10%) | PC refresh and price-driven Endpoint growth |
| HPE (incl. Juniper) | One of two global distributors (May 2026); 2026 Distributor of the Year NA and Central Europe; Unleash AI (Jun 2026) | Vendor consolidation winner, shared with Ingram |
| Cisco | Global Distributor of the Year 2025; Cisco 360 program (Feb 2026); co-sponsor of Paris AI Factory | Networking/security core; incentive rules changing |
| Microsoft | Frontier Distributor (Mar 2026); Global Device Partner of the Year 2025; CSP aggregator; lifecycle analytics in PartnerFirst | Cloud/SMB and Copilot-era software flow |
| NVIDIA | EMEA Distributor of the Year 2026; Americas 2025 (second year); Vera Rubin AI factory deal (Sept 2026) | AI infrastructure center of gravity |
| Dell | Distributor of the Year 2024 (EMEA, NA, APJ); AI Factory agreements (Dec 2024-Jan 2025) | Server/PC; AI factory channel |
| Lenovo | 2025 Distributor of the Year, US and UK&I | PC and infrastructure |
| AWS | Strategic Collaboration Agreement (Aug 2025); Marketplace Designated Seller of Record via StreamOne Stellr | Marketplace channel to 2030 |
| Google Cloud | 2026 Distribution Market Reach Partner of the Year | Marketplace/cloud |
| Broadcom / VMware | Nine added European territories amid partner cull; authorized training center | Software concentration winner |
| Nebius | Reserved NVIDIA HGX B300 clusters (Apr 2026) | New "AI cloud as supplier" model |
| Siemens | Global distribution partnership (Oct 5, 2026) | Industrial AI / operational technology adjacency |
| SAS | Primary global distributor (Sept 2023) | Analytics/AI software |

**How vendor economics work.** Vendor funds flow through cost of revenue (volume promotions, price protection, rebates) and through operating-expense reimbursements, not through a separate services line. Volume rebates depend on sales volume and customer breadth, and growth-based rebates get harder to earn as TD SYNNEX gets bigger ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1177394/000162828026003598/snx-20251130.htm)). The current memory-price inflation helps inventory values but raises availability risk and working-capital needs. No disclosure quantifies market development funds (MDF), rebates or any "data services to vendors."

## 7. Ingram Micro's Xvantage sets the AI benchmark TD SYNNEX will be judged against

**Market position.** TD SYNNEX ranks **#1 in Omdia's Global Distributor 250 for 2025**, ahead of Ingram Micro (#2) and Arrow (#3) ([ChannelPartner.de](https://www.channelpartner.de/article/4206826/td-synnex-ist-weltweit-groster-distributor-vor-ingram-und-arrow.html)). Estimates of total market size vary with definition:
- **$463B** for 2024 (Canalys/Omdia), with the top 15 distributors at more than 61%.
- **$389.9B** of revenue for the top 250 distributors in 2025 (Omdia), with the top 15 at 72.9%.
- **About $531B** for 2025, up 15% (Omdia, as reported in trade press).

Sources: [Omdia](https://omdia.tech.informa.com/blogs/2025/jun/next-for-technology-distribution); [Channel Dive](https://www.channeldive.com/news/old-school-distribution-channels-dwarf-hyperscaler-marketplaces-omdia/816270/); [Dutch IT Channel](https://www.dutchitchannel.nl/research/757065/it-distributie-groeit-naar-531-miljard-dollar). On those bases, TD SYNNEX's share is **roughly 12-16%** (derived). Some analysts may not count Hyve's manufacturing sales as distribution.

| Company (period) | Latest sales | Growth | Margin | AI / platform posture |
|---|---|---|---|---|
| TD SYNNEX (Q3 FY26, ended Aug 31, 2026) | Revenue $21.6B; billings $31.8B | +37.7% / +40.0% | Gross 6.61%; non-GAAP op. 3.42% | Hyve AI racks; Destination AI; PartnerFirst/Digital Bridge AI assistant; no AI revenue metric disclosed |
| Ingram Micro (Q2 2026, ended Jun 27, 2026) | Net sales $14.5B | +13.6% | Gross 6.60% | Xvantage live in 22 countries, ~75% of revenue in live markets; AI assistant (IDA) ~$1B net revenue in the quarter; >2M self-service orders/qtr (Q1); MCP server (Aug 2026); GPU sales more than doubled |
| Arrow ECS (Q2 2026) | $2.63B (billings $5.9B) | +14% | ECS op. income -12% | ArrowSphere AI assistants (limited release); says memory shortages push demand to cloud |
| ALSO Holding (H1 2026) | EUR 8.3B | +21% | EBITDA 2.0% | Cloud EUR 1.1B (+31%), 6M users; acquisitive |
| Pax8 (private) | Unverified (~$1B ARR in 2022; later figures conflict) | n/a | n/a | MSP-only marketplace; Agent Store; "Managed Intelligence Provider" concept; MCP in commerce APIs |
| Westcon-Comstor (FY ended Feb 28, 2026) | Gross invoiced $5.7B | +9.6% | n/a | Cybersecurity ~52%; recurring 68% of gross sales |
| ScanSource (FY ended Jun 30, 2026) | $3.23B | +6.1% | Gross 13.6% | Recurring revenue 33.7% of gross profit |
| Dicker Data (H1 2026) | A$2.10B gross | +14.2% | Gross 9.8% | APAC specialist |
| Esprinet (H1 2026) | EUR 2.09B | +8% | Adj. EBITDA 1.53% | Southern Europe |
| Avnet (FY ended Jun 27, 2026) | $27.6B | +25% | Adj. op. 3.1% | Components; "Ask Avnet" agent |
| CDW / Insight (Q2 2026), customers and sometimes rivals | $6.57B / $2.4B | ~+10% / +15% | Gross 20.1% / 21.7% | Buy direct on large deals |

Sources: [Ingram Micro 8-K](https://www.sec.gov/Archives/edgar/data/0001897762/000162828026051043/earningsreleaseq226.htm); [IT Channel Oxygen](https://itchanneloxygen.com/ingram-micro-divulges-xvantage-vital-statistics-after-q2-overachievement/); [Futurum](https://futurumgroup.com/insights/ingram-micro-q1-fy-2026-earnings-driven-by-xvantage-scale-and-ai-deal-mix/); [Channel Insider](https://www.channelinsider.com/ai/ingram-micro-mcp-server-xvantage/); [Arrow 8-K](https://www.sec.gov/Archives/edgar/data/0000007536/000000753626000127/arw-20260806xex99d1.htm); [IT Europa (ALSO)](https://www.iteuropa.com/news/also-lifts-first-half-profit-61-cloud-and-ai-demand-grows); [Pax8 Agent Store](https://www.pax8.com/en-us/news-post/pax8-unveils-transformational-agent-store/); [ChannelWeb UK (Westcon)](https://www.channelweb.co.uk/news/2026/westcon-comstor-fy26-results); [ScanSource](https://scansource.com/about/press-releases/2026/scansource-delivers-strong-fourth-quarter-and-full-year-results); [ASX (Dicker)](https://announcements.asx.com.au/asxpdf/20260828/pdf/073d0n9049xpjr.pdf); [Esprinet](https://www.emarketstorage.it/sites/default/files/comunicati/2026-09/20260909_188933.pdf); [Avnet 8-K](https://www.sec.gov/Archives/edgar/data/0000008858/000000885826000066/avt-20260805xex99d1.htm); [CDW](https://www.sec.gov/Archives/edgar/data/0001402057/000140205726000062/cdw-2026630earningsrelease.htm). Gross margins are not strictly comparable because companies net different shares of revenue. Quarter windows differ by up to one month.

**Size and growth.** TD SYNNEX is larger and growing faster than Ingram. Its Q2 FY26 revenue was about 35% above Ingram's Q2 net sales (derived). Even its Distribution segment alone grew billings 22% against Ingram's 13.6% net-sales growth, though billings and net sales are different measures.

**AI story.** Here Ingram has the more legible narrative. It publishes AI-attributed revenue (IDA at about **7% of Q2 net sales**, derived), self-service order counts and engagement lifts. Xvantage users show time on platform +40%, order value +12% and revenue per customer +23%. In August 2026, Ingram launched an MCP (Model Context Protocol) server that lets partners plug their own AI agents into its catalog. Pax8 is building the same agent-facing layer for MSPs. TD SYNNEX's own distinctive assets are elsewhere: Hyve, which Ingram has no equivalent of, a broad endpoint-to-data-center portfolio, and growing AI-factory delivery capability.

## 8. The 2030 outlook: agents, marketplaces and AI factories reshape distribution

**The market is concentrating.** Omdia expects the 15 largest distributors to strengthen their position as vendors streamline distributor networks. It forecasts **partner-delivered IT growth of 6.7% in 2026** and argues that indirect vendors "cannot go alone" ([Dutch IT Channel](https://www.dutchitchannel.nl/research/757065/it-distributie-groeit-naar-531-miljard-dollar); [Omdia](https://omdia.tech.informa.com/blogs/2026/jan/how-will-changing-it-spending-trends-impact-global-channel-chiefs)). The research found no public forecast of total distribution revenue for 2028-2030.

**AI infrastructure demand forecasts keep being revised up.**
- **IDC:** **$758B of AI infrastructure spending by 2029**, with accelerated servers above 95% of AI server spend.
- **Gartner (Sept 2026):** **$2.67 trillion** of total AI spending in 2026, about $1.48 trillion of it infrastructure. Gartner expects AI-optimized server spending to triple over five years ([Campus Technology](https://campustechnology.com/articles/2026/09/21/infrastructure-accounts-for-more-than-half-of-worldwide-ai-spending.aspx); [Computer Weekly](https://computerweekly.com/news/366638605/Gartner-AI-and-datacentre-spending-ramps)).
- **Edge computing:** about $450B by 2029, also IDC ([IDC](https://www.idc.com/resource-center/press-releases/edgecomputingforecast/)).

**AI PCs are mainstream, but PC volume is falling.**
- AI PCs are expected to be **55% (Gartner) to 59% (Counterpoint) of 2026 shipments** ([CRN India](https://www.crn.in/?p=72875); [Counterpoint](https://counterpointresearch.com/ko/reports/ai-advanced-pcs-to-surpass-half-of-global-shipments-in-2026)).
- IDC cut its 2026 PC unit forecast by **11.3%** because of memory shortages, with prices potentially **up as much as 17%** and the shortage possibly lasting into 2027 ([3DTested on IDC](https://www.3dtested.com/desktops/gaming-pcs/idc-slashes-2026-pc-shipment-forecast-amid-memory-shortages-total-pc-market-value-to-nonetheless-increase-to-usd274-billion-due-to-ongoing-price-hikes)). For distributors this means fewer devices at higher prices.

**Marketplaces are re-routing software sales more than replacing distributors.**
- Omdia forecasts hyperscaler marketplace software sales rising from about **$30B in 2024 to $163B in 2030** (29.1% CAGR) ([Intelligent CIO](https://www.intelligentcio.com/apac/2025/10/07/omdia-forecasts-us163bn-hyperscaler-cloud-marketplace-sales-by-2030/)). One release gives the base as $16B; more sources cite $30B.
- Channel partners' share of marketplace spend is forecast to rise from 37% in 2025 to 50% in 2027 and 59% in 2030.
- Distribution remains about **5.7 times** the size of the marketplace opportunity. Analyst Jay McBain says marketplaces handle under 1% of the tech and telecom industry ([Channel Dive](https://www.channeldive.com/news/old-school-distribution-channels-dwarf-hyperscaler-marketplaces-omdia/816270/)).
- Distributors take part through private-offer mechanisms: AWS Channel Partner Private Offers (CPPO), Microsoft multiparty private offers and Google channel private offers.
- AWS's "AI Agents and Tools" marketplace category launched with 800-900+ listings that support MCP and A2A, the protocols that let AI agents call tools and other agents ([Channel Insider](https://www.channelinsider.com/ai/the-new-aws-marketplace-category-for-ai-agents-and-tools/)).

**Agentic buying: big forecasts, cautious buyers.**
- **The bullish case.** Gartner expects AI agents to **intermediate more than $15 trillion of B2B spending by 2028** and **60% of B2B seller work to run through generative-AI conversational interfaces by 2028** ([DestinationCRM](https://www.destinationcrm.com/Articles/CRM-News/CRM-Featured-Articles/Gartner-60-of-Sales-to-Be-Carried-Out-by-AI-160659.aspx)). A widely repeated claim that "90% of B2B purchases will be handled by AI agents by 2028" could not be traced to Gartner and should not be used.
- **The cautious case.** Gartner also predicts that **75% of B2B buyers will prefer human-led sales experiences by 2030**, though another secondary source cites a 2026 Gartner survey in which 67% prefer a rep-free experience. These partly conflict. Gartner further expects **more than 40% of agentic AI projects to be cancelled by end-2027** ([Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)).
- **Market size and pace.** McKinsey sizes agentic commerce at **$3-5 trillion by 2030**, mostly retail. It argues B2B adoption is slower because "delegation is institutional," but scales once purchasing authority is set ([Digital Commerce 360](https://www.digitalcommerce360.com/2025/10/20/mckinsey-forecast-5-trillion-agentic-commerce-sales-2030/)).
- **The technical stack is forming.** MCP was donated to the Linux Foundation's Agentic AI Foundation in December 2025. Google backs A2A (agent-to-agent). Payment protocols include AP2, ACP and UCP, plus Visa's Trusted Agent Protocol and Mastercard Agent Pay ([Digital Commerce 360](https://www.digitalcommerce360.com/2025/10/16/visa-mastercard-both-launch-agentic-ai-payments-tools/)).

**New value pools mostly go to others.**
- Canalys/Omdia size the partner opportunity in AI and agentic-AI services at **about $267B by 2030** (35.3% CAGR). The report's own URL says $276B, so the exact figure is unresolved. They rate the opportunity "very high" for global system integrators, "high" for consultants and MSPs, and only **"low to medium" for resellers and distributors**. Notably, 47% of customers rely on partners for agentic AI ([IT Channel Oxygen](https://itchanneloxygen.com/ai-opportunity-for-resellers-and-distributors-low-to-medium-analyst/)).
- Gartner calls agentic AI "catastrophic for some" IT providers ([Gartner](https://www.gartner.com/en/documents/8270921)).

**Sales workforces are holding flat while coverage grows.**
- Bain finds that tech sales hiring grew 18% from 2017 to 2022 but **under 1% a year since**, as AI lets firms cover more accounts without adding reps ([Bain](https://www.bain.com/es-mx/insights/the-new-sales-productivity-equation-b2b-growth-agenda-2026/)).
- McKinsey reports that **90% of distributors have AI initiatives but only 11% have fully adopted them** ([Distribution Strategy](https://distributionstrategy.com/2026/09/distributors-move-from-buying-ai-software-to-buying-ai-companies-technology-and-talent/)). Its 2026 B2B Pulse finds the winners rebuild workflows end to end rather than adding point tools.
- Adjacent distributors are moving fast: Fastenal bought agentic-AI firm Rampp.ai, and Amazon Business, now at **about $60B in annualized gross sales**, is rolling out agentic checkout ([MarketScale](https://www.marketscale.com/industries/software-and-technology/amazon-business-hits-60-billion-in-annualized-gross-sales-as-agentic-ai-reshapes-b2b-procurement)).

## 9. What the 2030 outlook implies for TD SYNNEX's commercial organization

*This section is interpretation. It builds on the sourced facts above but is not itself sourced.*

**TD SYNNEX now runs two commercial organizations, and the AI vision should treat them differently.** Hyve sells engineered programs to a handful of hyperscalers. It is an account-management and program-execution business, and its constraints are capital, capacity and component supply. Distribution serves 150,000 partners through a long tail of transactions, and its constraint is cost-to-serve. The "AI for the commercial organization" conversation is mostly about Distribution. The two are financially linked, though: Distribution's thin profit pool funds Hyve's working capital. Every point of Distribution cost-to-serve that AI removes is effectively Hyve growth capital. That is a sharper framing than "AI efficiency."

**The first AI prize is the coverage model, not a chatbot.** Zammit's description of specialist groups, tiered customers and monthly reallocation is the vocabulary of a data-driven sales operation running on a monthly cycle. By 2030, the plausible end state is continuous, AI-driven allocation of specialist time, with transactional demand handled by self-service and agents. Bain's finding that tech sales hiring has flattened while coverage grows suggests the target: hold roughly 24,000 staff roughly flat while billings scale. Inside sales, quoting, the deal desk and customer service will change first. Specialist roles in AI factories, security, public sector and Hyve programs should grow.

**Being "agent-ready" is becoming table stakes, and it changes what wins share.** Ingram's MCP server, Pax8's MCP-enabled catalog and AWS's agent marketplace all point the same way. Partners' and buyers' AI agents will query several distributors' price, availability, configuration and credit terms programmatically. Digital Bridge already lives inside Teams, Slack and Webex, which is a genuine head start. The next steps would be to publish standards-based agent endpoints and to make credit terms and allocation machine-readable. The risk is that agent-to-agent buying turns distribution into a price comparison. The defense is to compete on what agents cannot easily compare: credit, allocation during shortages, multi-vendor solution configuration and post-sale services.

**What isn't measured won't be credited.** Ingram reports AI-assisted revenue, self-service order counts and per-customer lift. TD SYNNEX reports none. A 2030 commercial vision needs a scorecard that investors and vendors can see, for example:
- billings influenced or closed by AI;
- digital and self-service share of orders;
- quote turnaround time;
- cost-to-serve per partner tier;
- specialist capacity per partner.

**Marketplace orchestration is the software battleground of the decade.** Omdia expects $163B of marketplace spend by 2030 with 59% flowing through partners. That rewards whoever runs the multi-party private-offer and billing layer between hyperscalers, ISVs, MSPs and resellers. TD SYNNEX has much of the stack: StreamOne, Apptium, AWS seller-of-record status and Microsoft Frontier status. Yet it discloses no cloud metrics, while ALSO grows cloud 31% and Pax8 builds agent stores for MSPs. The open question is whether StreamOne becomes TD SYNNEX's "agent store" for MSPs, or whether that role goes to Pax8 or the hyperscalers.

**The distributor's AI value pool is enabling partners, not delivering services.** Analysts rate direct AI-services capture by distributors "low to medium." TD SYNNEX's strongest AI moves fit the enabler role instead:
- the Mark III AI factory deal, where TD SYNNEX supplies design, integration, co-administration, financing and supply chain behind a VAR;
- the Paris AI Factory;
- reserved Nebius GPU capacity;
- Destination AI profiling.

The Mark III deal looks like a repeatable template: the distributor as general contractor for enterprise AI factories delivered by VARs. It combines Hyve-grade integration know-how with financing and partner reach that marketplaces lack.

**Margin math makes this urgent.** Gross margin is falling, Hyve consumes working capital, and the stock fell on a record quarter. With roughly two cents of operating profit per billed dollar, small changes matter. AI that improves pricing discipline, credit decisions, rebate capture and stock allocation in a memory shortage pays off directly. Allocation is also a trust issue, given the CEO's own warning about "tensions" with partners. Transparent, AI-assisted allocation could become a differentiator.

**Partner and demand data is becoming a product for vendors.** As HPE, Microsoft, Broadcom and Cisco concentrate on fewer distributors, each vendor is effectively running a contest between TD SYNNEX and Ingram. PartnerFirst's lifecycle-stage analysis for Microsoft and Cisco hints at the next thing vendors will buy from distributors: partner-level demand sensing, renewal and churn prediction, and campaign execution. This could become an explicit service line rather than an implicit benefit.

**Humans stay where buyers want them.** Gartner's 75%-prefer-humans prediction and Omdia's view that relationships remain a differentiator argue against an "agents replace sellers" narrative. The more defensible 2030 model is agents handling the routine flow, with fewer but more expert humans on complex, high-value or regulated deals. Public sector and AI factories are the obvious examples.

## 10. Conversation starters for the 2030 discussion

1. **"Which of your two commercial engines should AI serve first: the 150,000-partner Distribution tail or the Hyve programs?"** Distribution cost-to-serve gains fund Hyve's working capital. How does leadership think about that trade-off?
2. **"You reallocate specialists monthly today. What would it take to do it continuously, and what share of the ~24,000 workforce would look different by 2030?"** This tests ambition on coverage and on the shape of the workforce.
3. **"Ingram reports about $1B a quarter through its AI assistant. What would TD SYNNEX's equivalent metric be, and when would you be ready to publish it?"** This tests measurement and investor storytelling.
4. **"When a partner's own Copilot or agent asks three distributors for price, availability and credit, how does TD SYNNEX win the answer?"** This opens the agent-readiness discussion: MCP/A2A endpoints and machine-readable credit and terms.
5. **"Is the Mark III Vera Rubin AI factory deal a one-off or a product?"** This explores packaging design, integration, financing and co-administration as a repeatable AI-factory offer for VARs.
6. **"Omdia says partners will handle 59% of $163B in marketplace spend by 2030. What share of that does StreamOne need, and does it become an agent store for MSPs?"** This brings in the Pax8 and ALSO comparison.
7. **"With memory shortages straining relationships, could AI-driven, transparent allocation become a partner-loyalty advantage?"** This connects operations and trust.
8. **"Vendors are consolidating to two global distributors. What data and demand-generation services would make TD SYNNEX the clear first choice over Ingram?"** This explores turning PartnerFirst lifecycle analytics into a vendor-facing product.
9. **"The April 2025 targets were ~5% billings growth and 95% FCF conversion, and FY2026 is running at roughly +32% with negative free cash flow. How should the commercial organization's 2030 targets be reset?"** This tests the strategy-finance link.
10. **"Where do humans remain essential in 2030: public sector, AI factories, security, Europe?"** This explores how specialist investment should shift as transactional work automates.

## 11. Facts to verify before the meeting

- **Investor-day targets.** Confirm whether the April 10, 2025 investor-day targets (~5% billings CAGR, 10-12%+ EPS CAGR, 95% FCF conversion) are the current official framework. One research note found no investor day after 2022.
- **FY2025 and FY2024 full-year figures.** Check against the Q4 FY25 8-K and the 10-K: non-GAAP operating income (~$1.78B), gross billings ($89.4B), GAAP EPS ($9.95, from an aggregator), FY2024 non-GAAP EPS ($11.68, ambiguous table) and full-year non-GAAP EPS (the ~$13.20 is a derived sum, not a reported figure).
- **Endpoint vs Advanced splits.** Get full-year FY2024 and FY2025 figures from the 10-K or investor deck. The FY2025 split and all product-category shares in this report are estimates, some of very low confidence.
- **Free cash flow and balance sheet.** Confirm exact Q2 and Q3 FY26 free cash flow (~-$330M and ~-$975.6M come from secondary sources), plus net debt, leverage and remaining buyback authorization.
- **Customers and Hyve.** Identify the unnamed customer at 11% of FY2025 revenue and Hyve's named hyperscaler customers. Confirm the terms of the reported Amazon warrant (~3.2M shares, May 2026).
- **StreamOne partner count.** Current figure: 30,000 (headline, 2024-25) vs 20,000+ (another executive). Also look for any 2026 cloud, ARR or Digital Bridge adoption metrics.
- **HP vs HPE.** Confirm that the Q2 call reference to "HP" choosing two global distributors means HPE.
- **CEO start date.** Confirm Zammit's effective date (September 1, 2024 per multiple sources) and the current executive roster. Check who replaced Chief Business Officer Simon Leung after his reported September 2025 retirement, and who the regional presidents are.
- **Merger history and ownership.** Confirm the Tech Data–SYNNEX merger closing date and whether MiTAC still holds a significant stake.
- **Analyst figures.** Confirm the Canalys/Omdia partner AI-services figure ($267B vs $276B), the Omdia marketplace base year ($30B vs $16B), and the definitions behind the $390B-$531B market-size range.
- **Gartner claims.** Do not use the "90% of B2B purchases by AI agents by 2028" claim unless it is found in a Gartner primary source. Check the Gartner "75% prefer human" prediction against the conflicting 67%-prefer-rep-free survey.
- **Inspire North America 2026.** It runs this week (Oct 7-9, 2026 per a third-party listing). Check for any new AI, PartnerFirst or StreamOne announcements before the meeting.

## Conclusion

The FY2026 numbers show AI demand reaching TD SYNNEX first as low-margin, capital-heavy hardware flowing through Hyve. That flatters growth and strains cash. The deeper 2030 question is about the Distribution business. Hyperscaler marketplaces are increasingly running through partners, and Omdia's data suggest distributors are not about to be replaced by them. The sharper risk is that buyers' and partners' AI agents start choosing among distributors on whatever can be read by a machine. In that world, scale and vendor awards matter less than four things: callable catalog and pricing, machine-readable credit, trusted allocation, and AI-factory delivery that no marketplace offers.

TD SYNNEX already has most of the parts. They include Digital Bridge inside partners' collaboration tools, StreamOne with Apptium, the Mark III-style AI-factory template, and a coverage model that already reallocates specialists monthly. What it lacks is a published scorecard and an explicit decision about which work goes to agents and which stays with experts. With roughly two cents of operating profit per billed dollar, getting that balance right is a necessity rather than an option. A 2030 conversation that starts there will feel grounded to this leadership team.
