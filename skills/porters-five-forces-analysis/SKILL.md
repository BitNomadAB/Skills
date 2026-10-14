---
name: porters-five-forces-analysis
description: Use when asked to analyze an industry's competitive structure, attractiveness, or sources of competitive pressure using Porter's Five Forces.
---

# Porter's Five Forces Analysis

## Purpose

Analyze how industry structure shapes competitive pressure and the potential to capture value. Assess all five forces using evidence, explain their drivers, and connect the analysis to the user's strategic question.

The framework evaluates an industry's structure. It does not by itself predict a company's success, calculate actual profitability, or replace analysis of the company's capabilities and choices.

## Use when

- The user asks for Porter's Five Forces or an industry-structure analysis.
- The user wants to understand competitive pressure, bargaining power, substitutes, or barriers to entry in a defined market.
- The user wants to assess how industry structure may affect a strategy, product, or investment decision.

## Do not use when

- The user only needs a list of competitors, a SWOT analysis, product positioning, or a financial forecast. Five Forces may inform those tasks but does not replace them.
- The user expects a reliable industry conclusion without a defined market, geography, time horizon, or relevant evidence.
- The user wants the five forces applied as a scorecard to an individual company without specifying the industry and strategic question.

## Scope and assumptions

- Define the focal industry or market, product category, customer group, geography, value-chain position, and time horizon. State meaningful boundaries and exclusions.
- Identify the focal perspective: for example, an entrant, incumbent, supplier, buyer, or investor. A force can affect parties differently.
- Treat repository evidence as information about the focal organization, not sufficient proof of market-wide conditions. Use credible, current industry sources when available and state their date and scope.
- Mark important claims as **observed**, **source-reported**, **inferred**, or **unknown**. Do not invent market shares, competitor behavior, switching costs, margins, or growth rates.
- Use only tools and sources available in the current environment. If current external evidence cannot be accessed, provide a provisional analysis and list the evidence needed.
- Analyze the industry structure rather than rating the focal company. Do not modify code or business operations unless separately requested. Always save a report according to **Report output**.

## Workflow

### 1. Define the industry and decision

1. Clarify the strategic question and the decision it should inform.
2. Define the market narrowly enough to identify meaningful competitors, buyers, suppliers, and substitutes, but not so narrowly that relevant alternatives disappear.
3. State geography, customer segment, value-chain layer, time horizon, and exclusions. If different segments or regions have materially different structures, analyze them separately.
4. Identify available evidence and its limits: market studies, public filings, customer or supplier data, contracts, pricing, industry reporting, policy, and repository materials.
5. Record the evidence date. Separate current conditions from trends or forecasts.

### 2. Assess the five forces

For each force, describe its current pressure on the focal industry, the main drivers, supporting evidence, uncertainty, and strategic implications. A qualitative label such as **low**, **moderate**, **high**, or **uncertain** may be used only with explicit reasoning; do not add unsupported numeric scores.

1. **Threat of new entrants:** Assess how easily a new competitor can enter and reach viable scale. Consider economies of scale, required capital, customer switching costs, brand or trust, access to distribution and inputs, regulation, learning effects, network effects, and likely incumbent response. Distinguish existing competitors from potential entrants.
2. **Bargaining power of suppliers:** Identify suppliers of critical inputs and assess their concentration, uniqueness, substitutes, switching costs, contribution to quality or cost, and ability to move downstream. Include dependence on platforms or infrastructure providers when relevant.
3. **Bargaining power of buyers:** Identify the parties that purchase from industry participants. Assess buyer concentration and volume, switching costs, available alternatives, price sensitivity, information, differentiation, and ability to integrate backward or sponsor alternatives. Distinguish end customers from powerful intermediaries when relevant.
4. **Threat of substitutes:** Identify different products, services, processes, or behaviors that meet the same underlying customer need. Assess their relative price and performance, convenience, switching costs, and the likelihood customers will adopt them. Do not limit substitutes to products in the same category.
5. **Rivalry among existing competitors:** Assess the intensity and basis of competition among current industry participants. Consider the number and relative strength of rivals, market growth, differentiation, capacity and fixed costs, switching costs, exit barriers, and strategic stakes. State whether rivalry is mainly about price, features, service, access, or another factor.

### 3. Connect the forces to the decision

- Explain how each force affects the industry's ability to sustain prices, margins, or other forms of value capture over the stated time horizon.
- Identify interactions between forces. For example, buyer power may rise when substitutes increase, or supplier power may be amplified by high switching costs.
- Separate industry-wide pressure from advantages or disadvantages specific to the focal organization.
- Translate findings into strategic implications that follow from evidence, such as reducing dependence, differentiating around buyer needs, choosing a segment, or avoiding direct exposure to a force.
- Identify what could change the analysis, including technology, regulation, distribution shifts, consolidation, or changing customer behavior, when evidence supports those possibilities.

### 4. Check evidence and confidence

1. Cite a source for consequential market claims, with publication date or observation period when available.
2. Distinguish measured facts from source interpretation and the analyst's inference.
3. Report conflicting or weak evidence and avoid presenting forecasts as current facts.
4. For each high-impact unknown, state what information would confirm or challenge the assessment.
5. If evidence is insufficient to rate a force, mark it **uncertain** rather than guessing.

## Decision rules

- All five forces must be considered, but their importance and evidence depth may differ by market.
- Define substitutes by the need they satisfy, not only by industry classification or product similarity.
- Do not treat complementors, regulators, macroeconomic conditions, or internal capabilities as a sixth force. When relevant, describe them separately as factors that may alter one or more of the five forces.
- Do not confuse low current rivalry with low competitive pressure; other forces may still constrain value capture.
- Do not infer attractive company economics directly from a force rating. Company position, execution, costs, and strategic choices also matter.
- Avoid generic claims such as “high competition” without naming the mechanism and evidence.
- When market boundaries are disputed, show plausible alternative boundaries and explain how each changes the analysis.
- Keep recommendations tied to a specific force, mechanism, and strategic question. State material tradeoffs and unresolved assumptions.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/porters-five-forces-analysis/` if missing.
- Save every completed Five Forces analysis as a Markdown report in `analysis/porters-five-forces-analysis/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - Before analysis, `report.py new "<topic>"` creates the report with the date from the system clock, a free file name and the headings from **Expected result**, and prints its path. Write the report into that file.
  - After writing, `report.py check <report-path>` checks the date line, missing or empty sections and anything that looks like a secret or token. Fix every `FAIL` line and run it again.
  - Without Python, apply the rules above by hand and check the same things yourself before finishing.

## Expected result

Provide a concise analysis with these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **Scope and strategic question:** industry definition, focal perspective, geography, value-chain position, and time horizon.
2. **Five-forces assessment:** force, pressure level if supportable, drivers, evidence, confidence, and implications.
3. **Overall structure:** how the forces interact and what they imply for industry value capture.
4. **Strategic implications:** options relevant to the focal decision, with rationale and tradeoffs.
5. **Evidence gaps and change drivers:** what remains unknown and what could change the assessment.

Use a comparison table when it remains readable. Cite source names, dates, and links or repository paths where available. Make clear when findings are provisional because evidence is incomplete or stale.

## Boundaries

- Five Forces is an industry-structure framework, not a complete company strategy or profitability model.
- Repository evidence alone rarely establishes market-wide bargaining power, entry barriers, or substitute behavior.
- Do not present assumptions or undated claims as current market facts.
- Preserve unrelated user changes and report evidence or sources that could not be accessed.