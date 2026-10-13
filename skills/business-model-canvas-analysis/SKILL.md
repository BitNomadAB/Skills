---
name: business-model-canvas-analysis
description: Use when asked to create, review, compare, or validate a business model using the Business Model Canvas (BMC).
---

# Business Model Canvas Analysis

## Purpose

Create or assess a business model using the nine Business Model Canvas (BMC) building blocks. Show how the blocks fit together, what evidence supports them, and which assumptions need validation.

The BMC is a structured description and discussion aid. A completed canvas is not proof of customer demand, product-market fit, profitability, or operational feasibility.

## Use when

- The user asks to create, review, compare, or update a Business Model Canvas.
- The user wants to understand how an existing product, service, platform, or organization creates, delivers, and captures value.
- The user asks for an evidence-based view of business model assumptions from a product repository or related materials.

## Do not use when

- The user only wants a business plan, market-size estimate, financial forecast, pitch deck, or product requirements document. Offer the BMC as a framing tool only if useful.
- The user expects repository contents alone to establish real customer behavior, market demand, costs, pricing effectiveness, or financial viability.

## Scope and assumptions

- Confirm whether the canvas describes the **current**, **proposed**, or **target** model, for which organization/product, market, geography, and time period.
- Treat repository evidence as evidence of implementation or stated intent, not automatic proof of commercial reality. Mark each material claim as **observed**, **stakeholder-reported**, **inferred**, or **unknown**, and include its source where possible.
- Do not invent customers, segments, prices, conversion rates, costs, market facts, partnerships, or revenue. Use explicit unknowns and questions instead.
- If multiple business models or materially different time horizons are in scope, create separate canvases. Do not mix current facts with a proposed future state without labeling them.
- For nonprofits, public services, internal platforms, or other non-commercial models, adapt value and funding flows explicitly. Do not invent customer revenue just to fill a block.
- Use only tools available in the current environment. Never assume a particular agent, operating system, shell, or repository layout.
- Treat the task as analysis. Do not change product code, pricing, or business operations unless the user separately requests implementation. Always save a report according to **Report output**.

## Workflow

### 1. Establish the model boundary

1. Confirm the subject, intended audience, model status (current, proposed, or target), scope, market, and time horizon.
2. Clarify what the organization is trying to accomplish and whose value is being considered.
3. Identify available evidence: user or stakeholder input, product and pricing documentation, repository files, contracts, support materials, operational data, and financial information.
4. Record evidence sources and limitations. Distinguish implemented capabilities from approved plans and external claims.
5. If the subject contains different customer groups or business models, decide whether separate canvases are needed.

### 2. Fill the nine building blocks

For each block, summarize what is known, cite evidence, label confidence or status, and list important unknowns.

1. **Customer Segments:** Which distinct people or organizations does the model serve? Identify users, buyers, payers, beneficiaries, and decision-makers separately when they differ. State which segments are in and out of scope.
2. **Value Propositions:** What value is offered to each segment? Describe the customer need, problem, or desired outcome and how the offering addresses it. Do not treat a feature list as proof of customer value.
3. **Channels:** How does the organization reach, sell to, deliver to, and support each segment? Distinguish planned channels from channels shown to be in use.
4. **Customer Relationships:** What kind of relationship is established and maintained for each segment, such as self-service, assisted support, account management, or community? Include how customers are acquired, served, and retained when evidence exists.
5. **Revenue Streams:** Who pays, for what, when, and through which pricing or payment mechanism? Separate actual revenue from proposed pricing and distinguish one-time, recurring, usage-based, licensing, transaction, or other flows where relevant.
6. **Key Resources:** What assets are essential to deliver the value proposition, operate channels, maintain relationships, or earn revenue? Consider people, technology, data, intellectual property, capital, and infrastructure.
7. **Key Activities:** What work must the organization perform especially well to deliver the model? Consider product development, operations, sales, service, compliance, and platform management as relevant.
8. **Key Partnerships:** Which external organizations or suppliers provide essential resources, activities, access, or capabilities? State the nature of the dependency and whether it is confirmed, planned, or merely assumed.
9. **Cost Structure:** What significant costs arise from the model's resources, activities, channels, relationships, and partnerships? Separate known costs from estimates and identify fixed, variable, or usage-sensitive costs only when supported.

### 3. Check coherence across blocks

- Trace each value proposition to the segment it serves, the channel that reaches it, and the relationship used to serve it.
- Trace revenue to the party that pays and to the value received. A user, buyer, payer, and beneficiary may be different parties.
- Trace major costs to the resources, activities, channels, relationships, and partners that cause them.
- Check that key resources, activities, and partnerships plausibly support delivery of the promised value.
- Identify contradictions, dependencies, missing links, and unsupported assumptions. Explain why each matters instead of calling a block “weak” without reasoning.
- For multi-sided platforms or marketplaces, map each side's segments, value propositions, channels, relationships, and revenue or subsidy flows. Make cross-side dependencies and network effects explicit; do not combine all sides into one customer segment.

### 4. Prioritize validation

1. List assumptions that are both consequential to the model and uncertain.
2. Rank them qualitatively by impact and uncertainty, explaining the basis. Do not invent precise scores.
3. For the most important assumptions, suggest a proportionate validation method, the evidence to collect, and a decision signal or threshold only when the user can define one.
4. Separate evidence already available from experiments or research that are only proposed.
5. State questions for customers, partners, operators, or financial owners when repository evidence cannot answer them.

## Decision rules

- A blank or unknown block is an analysis finding, not permission to invent an answer.
- Keep customer value, product functionality, and organizational capability distinct. A working feature does not establish demand or willingness to pay.
- Where several segments are served differently, map the relevant blocks per segment rather than forcing a single generic description.
- Where the paying party differs from the user or beneficiary, state who receives value and who funds it.
- Distinguish actual, contracted, planned, and hypothesized revenue, costs, partnerships, and channels.
- If sources conflict, report the conflict and identify which owner or evidence could resolve it.
- Do not infer profitability from revenue streams and cost categories without reliable amounts, time periods, and assumptions.
- Tie recommendations to specific block interactions or assumptions and describe the intended outcome and material tradeoffs.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/business-model-canvas-analysis/` if missing.
- Save every completed BMC analysis as a Markdown report in `analysis/business-model-canvas-analysis/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.

## Expected result

Provide a concise analysis with these sections, omitting a section only when it is not applicable and explaining why:

1. **Canvas scope:** subject, audience, status, market, and time horizon.
2. **Business Model Canvas:** all nine blocks, with unknowns clearly marked. A table is suitable when readable.
3. **Evidence and confidence:** sources and whether claims are observed, stakeholder-reported, inferred, or unknown.
4. **Coherence and gaps:** how the blocks connect, contradictions, dependencies, and consequential omissions.
5. **Priority assumptions:** the most important uncertainties and why they matter.
6. **Validation actions:** proposed research or experiments, evidence sought, and decision signals where available.

When comparing models, provide one canvas per model or time horizon and then compare the differences. Include relevant repository paths or source identifiers. Do not imply that the canvas itself validates the business.

## Boundaries

- The BMC describes a model; it does not establish market demand, competitive advantage, legal compliance, or financial viability.
- Make clear whether claims are based on repository evidence, stakeholder input, external data, or assumptions.
- Do not present proposed validation as completed research or inferred values as confirmed facts.
- Preserve unrelated user changes and report evidence or sources that could not be accessed.