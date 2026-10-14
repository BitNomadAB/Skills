---
name: lean-canvas-analysis
description: Use when a startup founder asks to create, review, compare, or validate a startup business model using Lean Canvas.
---

# Lean Canvas Analysis

## Purpose

Help a startup make its business-model hypotheses visible and decide what to learn next. Create or review a Lean Canvas, connect its assumptions, and prioritize practical tests of the assumptions that could invalidate the model.

A Lean Canvas is a set of hypotheses, not evidence that customers want the product, will pay for it, or that the startup can build a viable business.

## Use when

- A startup founder asks to create, review, compare, or update a Lean Canvas.
- An early-stage team needs to clarify a target customer, problem, value proposition, business model, or next validation step.
- The user wants to assess startup assumptions using product documentation or a repository as partial evidence.

## Do not use when

- The user needs a complete financial forecast, fundraising plan, market-size report, business plan, or detailed product specification. Use Lean Canvas only as a framing aid if relevant.
- The user wants to describe an established organization's operating model in depth; Business Model Canvas may fit better.
- The user expects a product repository to prove customer demand, market size, retention, or willingness to pay.

## Scope and assumptions

- Confirm the venture or product, stage, target geography or market, decision to inform, and whether the canvas represents a current hypothesis or a proposed change.
- Treat repository content as evidence of implemented or intended functionality, not as proof of customer value or commercial outcomes.
- Mark claims as **observed**, **customer-reported**, **measured**, **inferred**, or **unknown**. Include source, date, and relevant sample or context when available.
- Do not invent customer quotes, market facts, conversion rates, prices, costs, metrics, or validation results. Leave gaps explicit and ask focused questions where needed.
- Create separate canvases when products, segments, geographies, or materially different business-model hypotheses should not be combined.
- Use only tools available in the current environment. Never assume a particular agent, operating system, shell, or repository layout.
- Treat the task as analysis. Do not change product code, pricing, or business operations unless the user separately requests implementation. Always save a report according to **Report output**.

## Workflow

### 1. Frame the startup hypothesis

1. State the venture, target market, current stage, and decision the canvas should help make.
2. Clarify whether the user wants a fresh canvas, a critique, a comparison, or a revision of an existing canvas.
3. Gather available evidence from customer research, sales or usage data, support conversations, product and pricing material, repository files, and founder or team input.
4. Separate actual behavior and measured results from opinions, plans, and assumptions. Note evidence date and limitations.
5. If evidence is sparse, produce a provisional canvas and identify the highest-impact unknowns rather than blocking on completeness.

### 2. Fill the nine Lean Canvas blocks

For each block, record the hypothesis, supporting evidence, status or confidence, and important unknowns.

1. **Problem:** List the most important problems the target customer is trying to solve. Include existing alternatives, including manual workarounds and doing nothing. Do not begin with the proposed product's feature list.
2. **Customer Segments:** Identify the specific people or organizations experiencing the problem. Name users, buyers, and payers separately when they differ. Describe early adopters as the segment with a strong, current need and a plausible reason to act sooner than the broader market.
3. **Unique Value Proposition (UVP):** State the clear, specific reason the target segment should care and how the offer differs from alternatives. Keep it in customer-outcome language; do not treat a slogan or untested differentiation claim as proof.
4. **Solution:** Describe the smallest plausible set of capabilities that could address the prioritized problems. Keep it at hypothesis level and avoid turning this block into a full roadmap.
5. **Channels:** Identify plausible ways to reach, acquire, and serve the target segment. Separate channels already tested from channels merely proposed.
6. **Revenue Streams:** State who pays, what they pay for, when payment occurs, and the proposed mechanism or pricing basis. Distinguish actual payments from tested offers, untested hypotheses, and free usage.
7. **Cost Structure:** Identify significant startup and operating costs relevant to testing and delivering the model. Separate known costs from estimates; state the time period and assumptions for any amounts.
8. **Key Metrics:** Select a small number of observable measures that indicate customer value, adoption, retention, or business progress. Explain how each connects to a decision; avoid vanity metrics that can rise without validating the model.
9. **Unfair Advantage:** State what the venture may possess that is difficult for competitors to copy or buy. Distinguish demonstrated advantages from hypotheses. A feature, first-mover claim, founder enthusiasm, or access that competitors can readily obtain is not automatically an unfair advantage.

### 3. Check the canvas logic

- Connect the target segment to a real problem, the UVP to that problem, and the proposed solution to the UVP.
- Check that channels can plausibly reach the segment and that the revenue hypothesis fits who receives value and who pays.
- Check whether key metrics can test the assumptions in the Problem, Segment, UVP, Solution, Channel, and Revenue blocks.
- Examine whether costs and required capabilities are plausible for the proposed stage and test plan, using only available evidence.
- Identify contradictions, dependencies, and missing links. Explain why each could matter to the startup's next decision.
- For multi-sided products or marketplaces, identify each side, its problem and value proposition, who pays, and the dependencies between sides. Do not collapse distinct sides into one segment.

### 4. Prioritize assumptions and tests

1. List the assumptions whose failure would most change the venture or next decision.
2. Assess each assumption qualitatively by impact and uncertainty, using available evidence. Explain the basis and avoid unsupported numeric scores.
3. Choose the most consequential uncertainty that can be tested with a practical, proportionate experiment.
4. For each proposed experiment, state:
   - the assumption being tested;
   - the target segment and recruitment method;
   - the test method and what participants will actually do;
   - the evidence or metric to observe;
   - a success, failure, or inconclusive decision rule, if the team can define one;
   - cost, duration, ethical considerations, and downside limits when relevant.
5. Prefer tests that measure real behavior over hypothetical intent when feasible. Treat interviews, surveys, sign-ups, prototypes, pilots, and paid commitments as different levels and types of evidence.
6. Report experiments as proposed until results have actually been collected. Summarize observed results separately from interpretation and the resulting decision.

## Decision rules

- Do not fill a canvas for appearance's sake. An explicit unknown is more useful than a plausible invention.
- Keep customer segments narrow enough to identify who has the problem and how they behave; do not use “everyone” as a target segment.
- Distinguish the person with the problem from the user, buyer, payer, and beneficiary when they differ.
- Treat existing alternatives broadly: competitors, internal tools, manual processes, and doing nothing can all be substitutes.
- Do not infer demand, willingness to pay, retention, or product-market fit from implemented features, website copy, or untested founder assumptions.
- Do not call a metric actionable unless its movement can inform a decision and is linked to a meaningful customer or business outcome.
- Do not claim an unfair advantage without explaining why it is hard to copy or acquire and what evidence supports that claim.
- If evidence is contradictory or too weak, preserve competing hypotheses and propose a test that can distinguish them.
- Tie recommendations to a specific assumption, evidence gap, or inconsistency. Do not recommend building more software when learning can be achieved with a smaller test.
- Revisit the canvas when meaningful new customer, market, product, or business-model evidence changes an assumption.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/lean-canvas-analysis/` if missing.
- Save every completed Lean Canvas analysis as a Markdown report in `analysis/lean-canvas-analysis/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - Before analysis, `report.py new "<topic>"` creates the report with the date from the system clock, a free file name and the headings from **Expected result**, and prints its path. Write the report into that file.
  - After writing, `report.py check <report-path>` checks the date line, missing or empty sections and anything that looks like a secret or token. Fix every `FAIL` line and run it again.
  - Without Python, apply the rules above by hand and check the same things yourself before finishing.

## Expected result

Provide a concise analysis with these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **Venture and decision:** stage, market, canvas status, and decision to inform.
2. **Lean Canvas:** all nine blocks, with assumptions and unknowns clearly marked.
3. **Evidence quality:** sources, dates, sample/context, and whether claims are observed, customer-reported, measured, inferred, or unknown.
4. **Model logic:** the most important connections, contradictions, and dependencies between blocks.
5. **Riskiest assumptions:** prioritized by impact and uncertainty, with reasoning.
6. **Next experiments:** test design, evidence sought, decision rule, and relevant constraints.
7. **Open questions:** customer, market, operational, or financial information still needed.

Use a compact canvas table when it remains readable. Include relevant repository paths or source identifiers. For a revised canvas, state what changed and which new evidence caused the change.

## Boundaries

- Lean Canvas supports learning and prioritization; it does not prove viability, product-market fit, or investment readiness.
- Repository evidence cannot substitute for customer and market evidence.
- Do not present proposed experiments as completed research or inferred claims as measured facts.
- Preserve unrelated user changes and report evidence or sources that could not be accessed.