# The distributor of 2030: the market shifts, explained

*Working draft, October 17, 2026. Companion to the alpha-versus-beta note. Built on the research report, its notes and the Q3 FY26 10-Q. Forecasts are named by forecaster. Anything marked "interpretation" is our view, not a fact.*

How to read each shift:
- **In one line.** The shift in a sentence.
- **Context.** What is actually happening and why, in plain terms, with jargon explained.
- **Evidence.** The numbers and events behind it.
- **How distribution works today versus 2030.** The mechanics that change.
- **Where TD SYNNEX stands.** Assets and gaps.
- **What it means for sales and go-to-market.**
- **The counter-case.** What would make the shift smaller or slower.
- **Signals to watch.** Early indicators the leadership team can track.
- **Workshop provocation.** A question to put to the room.

The first six shifts are the ones in the earlier note. Part 2 reviews what is missing from a sales and go-to-market point of view and adds six more.

---

# Part 1: The six shifts, in depth

## Shift 1. Buyers send agents

**In one line.** By 2030 a growing share of B2B buying, including partners buying from distributors, starts with a software agent rather than a person.

### Context

An "AI agent" here means software that can take a goal ("replace these 40 laptops within budget by month-end"), break it into steps, call other systems and act. In buying, that means the agent searches, compares suppliers, checks stock and price, validates a configuration, applies a budget or policy, places the order and tracks it. "Agentic commerce" is the umbrella term.

Two things make this real rather than hype:
1. **Standards for agents to talk to systems now exist.** The Model Context Protocol (MCP) lets an agent call a company's tools and data in a standard way. It was donated to a Linux Foundation body in December 2025, which signals broad industry adoption. Agent-to-agent protocols (A2A, backed by Google) let one company's agent negotiate with another's. Payment protocols from Visa, Mastercard, Google and Stripe let agents pay with authenticated credentials.
2. **Procurement is the ideal agent job.** It is rule-based, repetitive and data-heavy. Corporate buyers already work from approved catalogs, price lists and policies.

For a distributor there are three kinds of agent that matter:
- **The partner's agent.** A reseller or MSP uses an agent inside its own tools (Teams, Salesforce, its quoting or PSA system) to source from distributors. This is the nearest-term change. TD SYNNEX's Digital Bridge assistant is an early version that runs inside the partner's tools.
- **The end customer's procurement agent.** A large company's buying agent asks partners, and possibly distributors and marketplaces, for quotes. This pressures the partner, and through it the distributor, to answer machines fast and accurately.
- **The vendor's agent.** Vendors build agents that steer deals, check eligibility for special pricing, and could route orders. They may favor the distributor whose systems they can connect to most easily.

### Evidence

- Gartner (October 2025): AI agents will intermediate more than **$15 trillion** of B2B spending by 2028.
- Gartner (2023): **60% of B2B seller work** will run through generative-AI conversational interfaces by 2028.
- Gartner also predicts **75% of B2B buyers will prefer human interaction** in 2030, and that **over 40% of agentic AI projects will be cancelled** by the end of 2027.
- McKinsey (October 2025): agentic commerce of **$3-5 trillion globally by 2030**, mostly retail. B2B is slower because "delegation is institutional," but scales once purchasing authority is set.
- A vendor-cited Forrester figure says **94% of B2B buyers already use generative AI during purchasing**, though Forrester calls fully autonomous buying rare.
- AWS Marketplace opened an "AI Agents and Tools" category in July 2025 with 800+ listings supporting MCP and A2A.
- **Ingram Micro** launched an MCP server in August 2026 so partners' agents can connect to its platform. Its AI assistant handled about **$1B of net revenue in Q2 2026**, and it processed more than 2 million self-service orders in Q1.
- Amazon Business, at about $60B of annualized gross sales, is rolling out an agentic checkout layer.
- First live B2B agentic payment reported in July 2026 (Visa and Lianlian in Greater China, secondary source).

### How distribution works today versus 2030

| Step in the order | Today | 2030 |
|---|---|---|
| Discovery | Partner rep searches the portal, calls the distributor rep, or uses EDI catalogs | Partner's agent queries two or three distributors' APIs in parallel |
| Configuration | Specialist checks compatibility by hand on complex deals | Agent calls the distributor's configuration rules; errors caught before quote |
| Price | Portal price, plus special-bid requests by email | Agent requests price; distributor's agent applies vendor program rules and returns a firm quote in seconds |
| Credit and terms | Credit limits set by the credit team; financing quoted separately | Agent sees available credit and financing options in the same response |
| Order and tracking | Portal, EDI or rep | Agent places and tracks; exceptions go to a human |
| Selection of distributor | Relationship, habit, rep responsiveness, price | Whoever answers fastest and most completely, with the best terms, and is trusted by the agent's rules |

The key difference: **loyalty moves from the rep to the interface.** If an agent is configured to compare three sources, the distributor that is slow, incomplete or unreadable to machines simply drops out of the comparison.

### Where TD SYNNEX stands

- **Assets.** PartnerFirst, the unified portal now in North America and Europe; Digital Bridge, with an AI assistant in Teams, Slack and Webex and connectors to Salesforce and QuickBooks; EC Express and XML/API feeds; StreamOne Ion with a headless commerce API; a 24/7 self-service AI assistant announced in January 2026.
- **Gaps.** No public MCP server or agent-to-agent offering found. No published metric of AI-driven or self-service orders. Ingram is about a year ahead in visible metrics and has the first MCP server. Partner-facing systems are still several brands (PartnerFirst, Digital Bridge, StreamOne, EC Express, InTouch in Europe).

### What it means for sales and go-to-market

- **The long tail becomes an API business.** Most of the 150,000 partners are small. Serving them through people is expensive. Serving them through agents is cheap, but only if the systems are good enough that partners' agents choose TD SYNNEX.
- **Inside sales roles change most.** Order-taking, quote preparation, stock and price checks and order status are exactly what agents do. Those roles shrink or shift to exception handling and growth.
- **"Share of agent" becomes a sales metric.** How often does a partner's agent query TD SYNNEX, and how often does it win the comparison?
- **Vendors will reward the distributor their agents can integrate with.** Being agent-ready becomes part of the vendor value proposition, alongside credit and coverage.
- **The human sale moves up the value curve.** Gartner's 75% human-preference figure applies to complex, high-value and new decisions. Those are AI factories, security architectures, public-sector frameworks. That is where specialists go.

### The counter-case

- B2B agent adoption is held back by trust, policy and liability. Procurement teams may keep humans in the loop for years.
- Many partners are small and slow to adopt new tools.
- If agents produce errors in pricing or configuration, buyers revert to people.
- The 40% cancellation forecast suggests a hype correction before real adoption.

The likely path is uneven: fast for reorders, renewals, standard configurations and cloud seats; slow for complex projects.

### Signals to watch

- Share of TD SYNNEX orders by channel: portal, API, agent, rep.
- Number of partners calling TD SYNNEX APIs from their own tools.
- Ingram's next disclosed agent and MCP metrics.
- Vendor announcements of agent integrations with distributors.
- Large customers publishing agent-procurement policies.

### Workshop provocation

"If a partner's agent compared TD SYNNEX and Ingram Micro on 1,000 orders tomorrow, how many would we win, and why would we lose the rest?"

---

## Shift 2. Software and cloud route through marketplaces

**In one line.** A rising share of software, cloud and security spending moves onto hyperscaler marketplaces, and distributors have to earn a role inside those rails instead of owning the transaction.

### Context

A hyperscaler marketplace is the online store inside AWS, Microsoft Azure or Google Cloud where customers buy third-party software and services. It is attractive to customers for one main reason: **they can count those purchases against their committed cloud spend**. A company that has promised to spend $50M with AWS over three years can buy a security product through AWS Marketplace and draw down that commitment. That creates a strong pull.

Historically, marketplaces cut out the channel. That has changed. Hyperscalers created mechanisms for partners to sell through them:
- **AWS Channel Partner Private Offers (CPPO).** A distributor or reseller negotiates a custom price with the software vendor and offers it to the end customer through AWS Marketplace. The partner keeps a margin.
- **Microsoft multiparty private offers** and **Google channel private offers** do the same.
- AWS added **multi-product solutions** at re:Invent 2025 and **auto-renewal of private offers** in September 2026.

So the question is no longer "marketplaces versus distributors." It is "what is the distributor's role and take rate when the transaction runs on someone else's rails?"

### Evidence

- Omdia forecasts software sold through hyperscaler marketplaces rising from about **$30B in 2024 to $163B in 2030** (29.1% annual growth). One release gives the 2024 base as $16B.
- Channel partners' share of that spend is forecast to rise from **37% in 2025 to 50% in 2027 and 59% in 2030**.
- Omdia also says distribution is still about **5.7 times** the size of the marketplace opportunity. Analyst Jay McBain notes marketplaces handle under 1% of the tech and telecom industry.
- TD SYNNEX signed an **AWS Strategic Collaboration Agreement** for the Americas in August 2025 and sells AWS Marketplace offers through **StreamOne Stellr** as Designated Seller of Record.
- Microsoft named TD SYNNEX a **Frontier Distributor** in March 2026, second after Ingram.
- At the Global Technology Distribution Council in early 2026, executives from Arrow, Ingram and TD SYNNEX described private offers as a way to turn hyperscaler disintermediation into partnership.
- Arrow reports memory and SSD shortages pushing customer demand toward software and public cloud.

### How distribution works today versus 2030

| Element | Traditional software distribution | Marketplace-era distribution |
|---|---|---|
| Who owns the transaction | Distributor bills the partner, partner bills the customer | Hyperscaler bills the customer; distributor and partner are paid through the marketplace |
| Where the margin comes from | Spread between vendor price and partner price, plus vendor rebates | Negotiated private-offer margin, plus services, billing and orchestration fees |
| Customer's reason to buy | Partner relationship, bundling | Draw down committed cloud spend |
| Distributor's value | Credit, billing aggregation, enablement, license management | Private-offer orchestration, multi-cloud billing, bundling across vendors, credit for partners, renewal management, compliance |
| Data | Distributor sees the transaction | Hyperscaler sees the transaction; distributor sees only what it orchestrates |

### Where TD SYNNEX stands

- **Assets.** StreamOne Ion with about 30,000 active partners (company figure, about a year old); Apptium, acquired July 2025, for marketplace, billing and multi-cloud orchestration; AWS SCA and Stellr; Microsoft Frontier status; Google Cloud 2026 Distribution Market Reach Partner of the Year.
- **Gaps.** No disclosed cloud revenue, annual recurring revenue or StreamOne billings. Competing for the MSP long tail with Pax8, whose whole model is a cloud marketplace for MSPs, and with ALSO in Europe, whose cloud revenue is about €1.1B and growing 31%.

### What it means for sales and go-to-market

- **New motion: co-selling with hyperscalers.** Distributor sellers need to know which customers have committed cloud spend to burn down, and bring the right vendor and partner to the deal. That is a different skill from selling boxes.
- **Account mapping across three parties.** Hyperscaler account teams, vendor teams and partners must be aligned. Whoever orchestrates that mapping controls deal flow.
- **Bundles beat single products.** The distributor's edge is putting multiple vendors, services and financing into one private offer, which neither a single vendor nor a hyperscaler naturally does.
- **Renewals are the prize.** Marketplace subscriptions renew. Auto-renewal of private offers raises the stakes: the party that owns the renewal relationship keeps the margin.
- **Compensation has to change.** Sellers paid on billed revenue may resist marketplace deals where revenue is booked net or flows through the hyperscaler.

### The counter-case

- Marketplaces may stay concentrated in large enterprises with big cloud commitments. Small and mid-sized businesses still buy through MSPs and distributors' own marketplaces.
- Hyperscalers could raise fees or tighten rules for partners if they want more of the margin.
- Vendors may prefer direct private offers for their top accounts.

### Signals to watch

- Share of TD SYNNEX's software and cloud billings flowing through hyperscaler private offers.
- Hyperscaler fee changes for channel private offers.
- Pax8 and ALSO cloud growth versus StreamOne.
- Vendor policies on who can transact private offers.

### Workshop provocation

"When a customer can burn down $50M of AWS commitment by buying through the marketplace, what is the one thing we bring that AWS, the vendor and the partner cannot do without us?"

---

## Shift 3. Hardware gets lumpy and physical again

**In one line.** AI brings back large, engineered, capital-heavy hardware deals, and turns supply allocation into a source of commercial power.

### Context

For two decades, data center hardware became more standard and easier to sell: servers were boxes from a catalog, and much of the action moved to cloud. AI reverses that. An "AI factory" is a cluster of GPU servers, high-speed networking, storage and software built to train or run AI models. It is engineered as a system:
- **Racks, not boxes.** A modern AI rack such as NVIDIA's GB300 or Vera Rubin NVL72 class is a single integrated unit worth millions of dollars, with dozens of GPUs, its own networking and liquid cooling.
- **Power and cooling.** Data centers need new power feeds and liquid-cooling infrastructure. Site readiness becomes part of the sale.
- **Long lead times and allocation.** GPUs, high-bandwidth memory and even standard memory are in short supply. Whoever controls allocation decides who gets product and when.

Who buys this:
- **Hyperscalers** (AWS, Microsoft, Google, Meta, Oracle) at massive scale, often through original design manufacturers (ODMs), companies that design and build hardware to the customer's specification. Hyve is TD SYNNEX's ODM.
- **"Neoclouds"**: new GPU cloud providers such as CoreWeave, Nebius and Lambda.
- **Sovereign AI programs**: governments and national champions building in-country AI capacity for data-control reasons. McKinsey estimates (via unverified secondary sources) that sovereignty requirements could shape $500-600B of AI spending by 2030.
- **Enterprises**: banks, manufacturers, healthcare and others building private AI capacity, usually smaller and needing more help.

The memory squeeze matters for the whole business. AI servers consume huge amounts of memory. That pulls supply away from PCs and standard servers, raising prices and creating shortages everywhere.

### Evidence

- IDC: **$758B of AI infrastructure spending by 2029**, with accelerated servers more than 95% of AI server spend.
- Gartner (September 2026): **$2.67 trillion** of total AI spending in 2026, about $1.48 trillion of it infrastructure; AI-optimized server spending to triple over five years.
- IDC cut its 2026 PC unit forecast by **11.3%** because of memory shortages, with PC prices up to **17%** higher and shortages possibly into 2027. Omdia says mainstream PC memory and storage costs rose **40-70%** during 2025.
- The 10-Q flags memory explicitly: "as AI applications and related data center investments continue to increase demand for memory-intensive configurations, the resulting changes in memory pricing may impact supply chains, product mix and pricing trends."
- Hyve: billings up **117%** to about $7.0B in Q3 FY26; programs with all five top US hyperscalers; adding more than 1 million square feet of US manufacturing; NVIDIA HGX design partner; liquid-cooled networking racks expected in production in the first half of FY2027.
- TD SYNNEX reserved dedicated **NVIDIA HGX B300 clusters on Nebius** in April 2026, which it described as a first for a global distributor, and is working with Mark III Systems on a **Vera Rubin NVL72 AI factory**. A Paris AI Factory with NVIDIA and Cisco was reported in July 2026.
- Ingram reports GPU sales more than doubled, at lower margin but "low cost to serve."

### How distribution works today versus 2030

| Element | Traditional infrastructure distribution | AI-factory era |
|---|---|---|
| Unit of sale | Server, switch, storage array | Engineered rack or cluster, often with power, cooling and services |
| Deal size | Thousands to hundreds of thousands of dollars | Millions to hundreds of millions |
| Sales cycle | Weeks | Months, with design, proof of concept and site preparation |
| What wins | Price, stock, credit | Allocation, design, integration, financing, delivery certainty |
| Margin profile | Steady single digits | Lower percentage margin, very large dollars, heavy working capital |
| Team | Account manager plus product specialist | Solution architect, supply planner, project manager, financing, services partners |

### Where TD SYNNEX stands

- **Assets.** Hyve's design and manufacturing; NVIDIA awards in both the Americas and EMEA; HPE and Dell AI factory programs; the Nebius capacity reservation; Destination AI for partner enablement.
- **Gaps.** The bridge between Hyve's hyperscale engineering and the channel's enterprise and sovereign demand is not visible. Cash is under strain: inventory rose $5.8B in nine months, mostly for Hyve, and nine-month free cash flow was about -$2.2B.

### What it means for sales and go-to-market

- **A new seller archetype.** AI factory sales look like enterprise capital projects. They need architects, project managers and financial structurers, not account managers.
- **Allocation is a commercial lever.** In shortages, which partner and customer gets product first is a strategic decision. It should follow strategic value, not who shouts loudest. That needs rules, data and governance.
- **Pricing must handle volatility.** Memory price swings make quotes stale quickly. Quote validity, price protection and pass-through rules become part of the sales motion.
- **Partners need help.** Most VARs cannot design or finance an AI factory alone. The distributor that brings the reference design, the capacity, the financing and the services partner wins the partner's loyalty.
- **Hyve's skills can be productized for the channel.** "Hyperscale-grade AI racks for enterprises and sovereigns, delivered through your partner" is a differentiated offer no other broadline distributor has.

### The counter-case

- AI capital spending could pause. Hyperscalers have digested capacity before. If they do in 2027-2028, Hyve's volumes drop and the inventory becomes a risk.
- Enterprise AI factories might be smaller than expected, with most AI consumed as cloud services.
- Hyperscalers may bring more design in-house or concentrate on fewer ODMs.

### Signals to watch

- Hyperscaler capital expenditure guidance each quarter.
- Hyve's customer count and concentration.
- Enterprise and sovereign AI factory deals closed through the channel.
- Memory price indices and allocation lead times.
- Inventory days and cash conversion cycle.

### Workshop provocation

"In a year of AI shortages, who decided which partners got product first, and was that decision made on purpose?"

---

## Shift 4. Vendors pick two

**In one line.** Technology vendors are cutting their distributor lists to a few global partners, which makes TD SYNNEX and Ingram Micro a de facto duopoly in many categories and changes what the fight is about.

### Context

Vendors have historically used many distributors per country to maximize reach. They are now consolidating for three reasons:
1. **Cost and complexity.** Each distributor relationship needs programs, systems, data feeds and management. Fewer partners means lower cost.
2. **Data and control.** Vendors want consistent global data on who buys what, through whom. Two global partners can supply that; twenty local ones cannot.
3. **Capability thresholds.** Vendors increasingly require security compliance, digital integration, financing capacity and AI skills that only the largest distributors can meet.

The same logic is moving through partner programs. Vendors are redesigning incentives to reward measurable value, not just volume, and to concentrate on fewer, more capable partners.

### Evidence

- **HPE (May 2026)** named Ingram Micro and TD SYNNEX its two global distributors after the Juniper acquisition, keeping some regional and specialist distributors.
- **Microsoft** raised CSP (Cloud Solution Provider) authorization thresholds in October 2025 and created a **Frontier Distributor** designation, awarded first to Ingram and then TD SYNNEX in March 2026.
- **Cisco** launched the **Cisco 360** partner program in February 2026, dropping Gold status, moving to solution-based specializations and consolidating incentives. TD SYNNEX was Cisco Global Distributor of the Year 2025.
- **Broadcom/VMware** made its cloud service provider program invitation-only and ended the white-label model in October 2025. TD SYNNEX gained nine European territories.
- Omdia ranks TD SYNNEX first and Ingram second globally. The top 15 distributors hold more than 60% of the market.
- Supplier agreements are nonexclusive, short-term and terminable on short notice, according to the 10-K.

### How distribution works today versus 2030

| Element | Multi-distributor world | Two-distributor world |
|---|---|---|
| Vendor's view of distributors | Coverage and logistics providers | Strategic platforms for reach, data, finance and AI enablement |
| Basis of competition | Price, terms, local relationships | Data quality, platform reach, enablement results, vendor-specific programs |
| Risk | Losing share in a country | Losing a global relationship, or being the "second choice" |
| Vendor incentives | Volume rebates | Value-based incentives tied to outcomes, adoption, renewals |
| Leverage | Vendors hold power | More balanced: vendors depend on two platforms |

### Where TD SYNNEX stands

- **Assets.** Global footprint in 100+ countries; top awards from HPE, Cisco, NVIDIA, Microsoft, Dell, Lenovo and Google Cloud; a portfolio of more than 2,500 vendors; Siemens added as a global distribution partner in October 2026.
- **Gaps.** No visible data or analytics product sold to vendors. The CEO has said TD SYNNEX lacks some cybersecurity vendors in Europe. Ingram has more visible platform metrics.

### What it means for sales and go-to-market

- **Vendor management becomes strategic account management.** The top 20 vendors each need a joint business plan, executive sponsor and shared metrics.
- **Proving influence matters.** Vendors paying for outcomes want proof that the distributor created pipeline, new partners or renewals. That needs attribution data.
- **The pitch to vendors changes.** From "we have reach and credit" to "we can show you who buys, predict demand, run your partner programs and integrate with your agents."
- **Being second choice is the risk.** In a two-distributor world, the vendor's preferred platform gets the best programs, allocation and co-investment.

### The counter-case

- Antitrust concerns or vendor fear of dependence could keep a third player alive in many categories.
- Specialist distributors in security (Exclusive Networks, Westcon-Comstor) and in the MSP market (Pax8) remain strong and could take share in high-growth niches.
- Vendors could build more direct and marketplace routes, reducing the need for any distributor.

### Signals to watch

- Further vendor consolidations and which distributors are chosen.
- Changes in vendor incentive design toward outcomes.
- Share of vendor program money flowing to TD SYNNEX versus Ingram.
- Specialist distributors' growth in security and cloud.

### Workshop provocation

"In each of our top ten vendors, are we the preferred platform or the backup, and what would the vendor say if we asked them?"

---

## Shift 5. Partners consolidate and re-form

**In one line.** The 150,000 partners TD SYNNEX sells to are themselves being reshaped by private equity, AI and services economics, which changes who the customers are and what they need.

### Context

TD SYNNEX's customers are not end users. They are resellers, managed service providers (MSPs), system integrators, retailers and others. That base is changing in four ways:
1. **Consolidation.** Private equity has been buying and combining MSPs and VARs for years. The resulting groups are larger, more sophisticated and more demanding. They negotiate harder and want platform integration.
2. **The service shift.** Reselling hardware and licenses earns thin margins. Partners are shifting to managed services, security operations, cloud management and now AI services.
3. **The AI services opportunity.** Customers need help to deploy AI: data preparation, model selection, integration, governance and managing AI agents. That is services work, and it is growing fast.
4. **A long tail under pressure.** Small partners without the skills or capital to make that shift face shrinking margins and may exit.

Analysts call some of the new partner types "managed intelligence providers," MSPs that manage AI agents for customers. Pax8 promotes this term and has launched an Agent Store.

### Evidence

- Canalys/Omdia (September 2025): partner opportunity in AI and agentic-AI services of **about $267B by 2030** (35.3% annual growth). The report URL says $276B, so the exact figure is unresolved.
- They rate the opportunity "very high" for global system integrators, "high" for consultants, MSPs and managed security providers, and only **"low to medium" for resellers and distributors**.
- **47% of customers** rely on partners for agentic AI.
- Pax8 has an **Agent Store**, a "Managed Intelligence Provider" concept and MCP in its commerce APIs.
- TD SYNNEX: **Destination AI** since August 2023, **Practice Builder**, **Practice Accelerator**, **MSP Evolve** since May 2024, **PartnerLINK** communities since April 2025, and a services marketplace in PartnerFirst.

### How distribution works today versus 2030

| Element | Today | 2030 |
|---|---|---|
| Typical partner | Many small resellers plus a few large VARs | Fewer, larger PE-backed groups plus a long tail of small specialists |
| Partner's main need from distributor | Product, price, credit, logistics | Skills, practice-building, services capacity, financing, platform integration |
| Partner's margin source | Product resale plus some services | Managed services, AI services, recurring revenue |
| Distributor's role | Supplier | Enabler, platform, and sometimes services marketplace |
| Relationship risk | Partner moves volume to another distributor | Partner becomes big enough to go direct, or chooses a platform that helps it grow |

### Where TD SYNNEX stands

- **Assets.** One of the largest partner bases in the world; Destination AI and the Practice programs; StreamOne for MSPs; communities and events; TD SYNNEX Capital financing.
- **Gaps.** No published metrics on partner AI practices built or partner growth. No visible segmentation of partners by AI readiness. Pax8 is more focused on the MSP AI story.

### What it means for sales and go-to-market

- **Segment partners by trajectory, not just size.** A small partner building an AI practice may be more valuable than a large one shrinking.
- **Sell growth, not products.** The partner's question is "how do I build a profitable AI practice?" The distributor that answers it wins loyalty.
- **Treat large partners as strategic accounts.** PE-backed groups need executive coverage, platform integration and custom terms.
- **Create a services marketplace.** Connect partners who need AI skills to partners who have them, with the distributor taking a fee. This is how a distributor earns from services without competing with partners.
- **Measure partner health.** Revenue trend, product mix, services attach, AI readiness and churn risk, so sellers know where to invest.

### The counter-case

- Large PE groups may negotiate direct relationships with vendors, bypassing distributors.
- AI services may be captured mainly by global system integrators and consultancies, leaving little for smaller partners.
- Partner consolidation may slow if interest rates stay high.

### Signals to watch

- Number of TD SYNNEX partners with AI practices and their growth.
- Share of revenue from the top 100 partners.
- PE activity in the channel.
- Services marketplace adoption.

### Workshop provocation

"Which 1,000 of our 150,000 partners will matter most in 2030, and do we know who they are today?"

---

## Shift 6. The balance sheet becomes a product

**In one line.** As deals get bigger and buying shifts to consumption, the distributor's ability to finance, underwrite and bill becomes a differentiated product, not just a cost of doing business.

### Context

Distributors have always been the channel's bank. They give partners trade credit, typically 30 to 90 days, so a small reseller can buy $1M of equipment before its customer pays. They also carry inventory and absorb some vendor price risk. That is why distribution is called a "balance sheet business."

Three changes make finance more important:
1. **Bigger deals.** AI factories cost millions. Few partners can fund them.
2. **Consumption models.** Customers increasingly want to pay monthly or per use, not upfront. Someone must fund the gap between paying the vendor and getting paid by the customer.
3. **Data advantage.** A distributor sees partner purchase history, payment behavior, vendor rebates and sell-through. That data can underwrite credit better than a bank can.

"Embedded finance" means offering credit and financing directly inside the buying process, at the moment of quote, rather than as a separate application. For agent-led buying, credit terms need to be machine-readable so an agent can see them.

### Evidence

- TD SYNNEX's balance sheet at August 31, 2026 (10-Q): **receivables $15.0B, inventory $15.3B, payables $22.4B**, total borrowings **$5.5B**.
- **$2.1B of receivables sold** without recourse and **$3.5B of supplier-finance obligations**.
- Interest expense rose **32%** in Q3; bad-debt provision for nine months was **$32.6M** versus $21.7M.
- The US receivables facility was doubled to **$3.0B** in September 2026; a **€650M** European facility opened in June.
- **TD SYNNEX Capital** offers Amplify short-term credit (45-90 days), 12-60 month payment plans, and **Tech-as-a-Service** in the UK, with deals of £1,000-250,000 handled automatically through InTouch.
- Commentary on agentic buying argues credit terms, financing and settlement speed must be machine-readable for agent buyers.

### How distribution works today versus 2030

| Element | Today | 2030 |
|---|---|---|
| Credit | Limits set by credit team, reviewed periodically | Dynamic limits set by AI on real-time data |
| Financing | Separate product, separate process | Embedded at quote; offered automatically to partners and agents |
| Consumption billing | Mainly for cloud | Extended to hardware, AI capacity and services |
| Risk | Concentrated in large customers and inventory | Priced and managed by data; parts distributed to capital partners |
| Revenue | Cost of doing business, recovered through margin | A profit line: financing fees, interest spread, as-a-service margins |

### Where TD SYNNEX stands

- **Assets.** Scale, credit data across 150,000 partners, established capital programs, UK automated financing.
- **Gaps.** Finance revenue is not disclosed. Rising credit costs and borrowing show the balance sheet is stretched. Automated financing appears limited to the UK.

### What it means for sales and go-to-market

- **Finance becomes part of every pitch.** "We can fund this" is often the deciding factor on large AI deals.
- **Sellers need finance skills or finance partners on the team.**
- **Credit becomes a growth lever.** AI-driven credit can extend more credit to good partners and less to risky ones, enabling growth without more risk.
- **Consumption needs new compensation models.** Sellers paid on upfront billings will avoid consumption deals unless pay plans change.

### The counter-case

- Rising rates and credit costs may limit how much balance sheet the company can deploy.
- Banks and fintechs may compete aggressively in channel financing.
- A downturn could turn credit risk into losses.

### Signals to watch

- Finance revenue and margins, if disclosed.
- Credit losses and days sales outstanding.
- Share of deals with embedded financing.
- Growth of as-a-service contracts.

### Workshop provocation

"If we treated TD SYNNEX Capital as a business with its own P&L and growth target, what would it be worth, and what would we do differently?"

---

# Part 2: Review of what is missing from a sales and go-to-market lens

The six shifts are mostly about the market: how customers buy, what they buy, and how the industry is structured. Leadership teams running commercial organizations will also want to see shifts in **how the company sells, prices, gets paid by vendors, and grows existing accounts**. Six additions are worth considering. The first four are strong enough to stand as shifts; the last two work better as cross-cutting themes.

## Shift 7. The sales capacity equation flips

**In one line.** Growth used to require more sellers. By 2030, growth will come from more capacity per seller, and the commercial organization's structure will change accordingly.

### Context

For a distributor with thin margins, the cost of selling and serving is the main controllable cost. In Q3 FY26, adjusted operating expenses were 48.3% of gross profit, down from 58% a year earlier (10-Q). That is roughly **$690M a quarter** of expense against about $1.4B of gross profit (derived). Most of it is people: sales, customer service, credit, operations and support.

AI changes the math. Agents can handle quoting, order entry, status checks, simple support and some account management. That does not eliminate sellers, but it changes what they do and how many are needed.

### Evidence

- Bain (January 2026): tech sales hiring grew 18% from 2017 to 2022 but **under 1% a year since**, as AI lets firms cover more accounts without adding reps.
- Gartner: **60% of B2B seller work** through generative-AI interfaces by 2028.
- McKinsey (2026): **90% of distributors have AI initiatives, but only 11% have fully adopted them**. Winners rebuild commercial workflows end to end rather than adding point tools.
- TD SYNNEX CEO (June 2026): commercial teams segmented into specialists and customer tiers, with resources reallocated monthly.
- Ingram: AI assistant handled about **$1B of revenue in Q2 2026**.
- Grainger uses AI to coach sales leaders and identify new contacts.

### What it means

- **Redesign roles, do not just add tools.** Which tasks go to agents, which to people, and how do the people's jobs change?
- **Measure productivity explicitly.** Gross profit per commercial employee, cost to serve by partner segment, time spent on selling versus administration.
- **Decide where to reinvest.** Freed capacity can go to specialists, new markets or margin. That is a leadership choice, not a technology one.
- **Plan the workforce transition.** Reskilling inside sales to specialist or exception roles, and managing attrition rather than layoffs where possible.

**Workshop provocation.** "If each seller could cover twice as many partners by 2028, would we hire half as many, cover twice as many partners, or move them to specialist roles?"

## Shift 8. Vendor money moves from volume to value

**In one line.** Vendors are redesigning partner incentives to pay for outcomes, not just volume, and the distributor's back-end income depends on proving it creates those outcomes.

### Context

A large share of distributor profit comes not from the price spread but from **vendor money**: volume rebates, growth bonuses, marketing development funds (MDF), price protection and special pricing. TD SYNNEX's 10-K calls these "important determinants of the final sales price." The amounts are not disclosed, but in distribution they are typically a large part of gross profit.

Vendors are changing how they pay. Instead of rewarding volume, they increasingly reward:
- new customer acquisition;
- software adoption and consumption;
- renewals and retention;
- specific solutions or specializations;
- verified influence on a deal.

That is good for partners and distributors who can prove value, and bad for those who cannot.

### Evidence

- **Cisco 360** (February 2026): Gold status dropped, solution-based specializations, consolidated incentives, a value index framework that extends to distributors. Cisco ended Monthly Value Rebates for Success Tracks and trimmed the delivery rebate.
- **Microsoft**: CSP authorization thresholds raised in October 2025; Frontier status for the top distributors.
- **Broadcom**: invitation-only partner programs.

### What it means

- **Attribution data becomes revenue.** If the distributor cannot show it created a new customer or drove a renewal, it may not get paid for it.
- **Program management becomes a core capability.** Understanding, tracking and claiming hundreds of vendor programs is complex; it is also an ideal job for AI.
- **Leakage is real.** Unclaimed rebates, missed program deadlines and pricing errors cost money. AI can find and recover it.
- **Sales incentives should align with vendor incentives.** If vendors pay for new logos and renewals, sellers should too.

**Workshop provocation.** "How much vendor money did we leave on the table last year because we could not prove or claim it?"

## Shift 9. From transactions to lifecycles

**In one line.** More of what TD SYNNEX sells is recurring (subscriptions, cloud, as-a-service, support contracts), so the commercial organization must manage renewals and expansion, not just sales.

### Context

Distributors historically sold one transaction at a time. As software becomes subscriptions, hardware moves to as-a-service, and support contracts renew, a growing share of revenue depends on renewals and expansion. That needs a different motion:
- tracking when contracts expire;
- predicting churn risk;
- prompting partners to renew or upgrade;
- bundling additional products.

The distributor sees renewal dates and usage data across thousands of partners and many vendors. Most partners and vendors do not have that cross-vendor view.

### Evidence

- PartnerFirst added **lifecycle-stage analysis** (close, renewal, upsell, churn) for Microsoft and Cisco in 2026.
- AWS introduced **auto-renewal of private offers** in September 2026.
- Westcon-Comstor reports recurring revenue of 68% of gross sales; ScanSource 33.7% of gross profit.
- TD SYNNEX does not disclose recurring revenue.

### What it means

- **Renewals are the most automatable and most leakable revenue.** Agents can track and prompt renewals at scale.
- **Partners will value a distributor that grows their recurring revenue.**
- **New metrics.** Net revenue retention, renewal rate, attach rate by partner.
- **Customer success at scale.** A digital customer-success motion for the long tail.

**Workshop provocation.** "What share of next year's gross profit is already under contract or up for renewal, and who owns making sure it renews?"

## Shift 10. Pricing and allocation become competitive weapons

**In one line.** Supply shortages, memory price swings and tariffs make pricing and allocation decisions a major source of margin gained or lost.

### Context

In normal times, distributor pricing follows vendor price lists plus a markup. In volatile times, pricing becomes a skill:
- when to raise prices as costs rise;
- how long to hold a quote;
- how to pass through tariffs;
- who gets scarce product.

The 10-Q shows margin pressure: Americas distribution gross margin fell from 7.57% to 6.37%. Part of that is mix, part may be pricing on large deals.

### Evidence

- Memory costs up **40-70%** in 2025 (Omdia); PC prices could rise **17%** (IDC).
- The 10-Q flags memory pricing as a risk and notes tariffs are generally passed through.
- OEMs give only limited price protection, per the research.

### What it means

- **Dynamic pricing with guardrails.** AI can price by deal, partner, product and market conditions within vendor rules.
- **Quote validity and price protection policies are commercial levers.**
- **Allocation governance.** Clear rules on who gets scarce product, aligned with strategic priorities.
- **Deal desk discipline.** Large, low-margin deals need approval rules and margin floors.

**Workshop provocation.** "In the last year, where did we give away margin we did not need to, and where did we lose deals we should have won?"

## Theme A. The distributor as ecosystem orchestrator

**In one line.** Complex deals involve many parties (vendors, ISVs, system integrators, MSPs, hyperscalers, financiers), and the party that assembles them controls the deal.

**Context.** An AI factory deal might involve NVIDIA, a server OEM, a storage vendor, a networking vendor, a software platform, a systems integrator, a managed service provider, a financing partner and a hyperscaler. No single partner can do it all. TD SYNNEX's own 10-Q describes its vision as being "the vital solutions aggregator and orchestrator" of the IT ecosystem. **Implication:** build the capability to assemble multi-party solutions, with partner-matching, referral fees and bundled offers. This cuts across shifts 2, 3 and 5.

## Theme B. Demand creation moves into AI answers

**In one line.** Buyers increasingly research through AI assistants rather than search engines and websites, which changes how vendors and partners generate demand.

**Context.** If a buyer asks an AI assistant "what is the best security solution for a 500-person company," the answer shapes the shortlist. Marketing must adapt to being found by AI ("generative engine optimization"). Vendors will shift marketing funds toward measurable pipeline. **Implication:** distributors can run AI-driven demand generation for vendors and partners at scale, as a paid service, and prove pipeline created. PartnerFirst's 2026 campaign tools are a start.

---

# Part 3: Putting it together

## Grouping the ten shifts for the workshop

| Lens | Shifts | The question for leadership |
|---|---|---|
| How customers buy | 1 Agents; 2 Marketplaces; 9 Lifecycles | Are we the easiest to buy from, by machine or person, and do we own the renewal? |
| What they buy | 3 Physical AI | Can we design, build, finance and deliver AI factories through the channel? |
| How the industry is organized | 4 Vendors pick two; 5 Partners re-form | Are we the preferred platform for vendors and the growth engine for partners? |
| How we sell and earn | 7 Sales capacity; 8 Vendor money; 10 Pricing and allocation | Is our commercial engine more productive and better paid than the competition's? |
| How we fund it | 6 Balance sheet as a product | Is our balance sheet a constraint or a product? |

Themes A and B, orchestration and AI-driven demand creation, run through all five lenses.

## The commercial questions that tie it together

1. **What is the commercial organization of 2030?** How many people, in what roles, with what tools, paid on what?
2. **What will be automated, and when?** Which commercial tasks go to agents first, and what is the human role after?
3. **How will we measure commercial performance?** Beyond billings and margin: share of agent, touchless orders, gross profit per commercial employee, renewal rate, vendor money claimed, partner growth.
4. **Who owns the partner?** Regions, vendor business units, platforms or specialists, and how do they coordinate?
5. **What will we stop doing?** To fund the new commercial model.
