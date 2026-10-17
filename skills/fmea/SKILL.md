---
name: fmea
description: Use when asked to perform or update a Failure Mode and Effects Analysis (FMEA) for a system, product, service, software component, or process.
---

# FMEA

## Purpose

Systematically identify how an in-scope system, product, service, software component, or process can fail to perform its intended function; examine the causes and effects; assess existing controls; and define proportionate actions to reduce risk.

FMEA is a structured analysis, not proof that all failure modes have been found or that a system is safe, reliable, or compliant.

## Use when

- The user asks for a Failure Mode and Effects Analysis (FMEA), a software/system/process FMEA, or an update to an existing FMEA.
- The user wants to understand failure paths and controls before a design, release, operational, or process decision.
- The user needs to prioritize actions to prevent failures, reduce their effects, or improve the chance they are detected.

## Do not use when

- The user needs a full safety case, fault-tree analysis of combinations of events, security threat model, or compliance certification. FMEA may inform these but does not replace them.
- The user expects quantitative failure probabilities, severity ratings, or a valid RPN without data and an agreed rating method.
- The user asks only for a code defect review or test plan without a failure-mode analysis.

## Scope and assumptions

- Define the FMEA type and scope: system/design, process, software, service, or another specified context. State the item or process boundary, lifecycle phase, operating conditions, users, and assumptions.
- Start from intended functions and requirements. If they are unclear, record the gap; do not invent requirements to make a failure mode fit.
- Use design, process, operational, test, incident, and domain-expert evidence where available. Repository evidence alone may not establish operating exposure, failure likelihood, effect severity, or control effectiveness.
- Mark important claims as **observed**, **source-reported**, **inferred**, or **unknown**. Cite evidence and preserve disagreement between stakeholders.
- Do not invent rating scales, historical frequencies, detection probabilities, owners, due dates, or actions as if they were agreed facts.
- Use only tools available in the current environment. Never assume a particular agent, operating system, shell, FMEA template, or repository layout.
- Treat the task as analysis. Do not modify production code, designs, or processes unless the user separately requests implementation. Always save a report according to **Report output**.

## External documentation

- **Purpose:** if you can read the web, you may look up official documentation or a vendor's published material to support a claim this analysis needs, for example a dependency's documented failure behavior or limits, or its published incident reports. Forums and blog posts are not evidence.
- **Confidentiality:** what you type into a search leaves the machine. Never put code, secrets, internal names, unreleased product or feature names, or customer data into a search. Search for the vendor, product or standard by its public name.
- **No contact with the product's own systems:** do not open the product's live services or administration pages.
- **Label and record:** label such a claim **external source**, never observed, and list each source in a **Sources** section at the end of the report: ID (S1, S2, ...), title, publisher, link, publication date (or "undated"), date read (YYYY-MM-DD), and what it supports.
- **Without web access:** mark the claim **unknown**.

## Workflow

### 1. Define the analysis

1. Confirm the purpose, decision, FMEA type, item or process under review, boundaries, lifecycle phase, and operating environment.
2. Identify intended functions, requirements, interfaces, users, and important assumptions. If a requirement is missing, record it as an open question.
3. Gather available evidence, including architecture or process descriptions, specifications, tests, incident history, monitoring, change records, and relevant expert input.
4. Decompose the scope into functions, steps, components, or interfaces at a level where distinct failure modes can be described and acted on.
5. Identify affected stakeholders and reviewers needed to confirm effects, severity, occurrence, controls, and actions.

### 2. Identify failure modes and effects

For each function or process step, record:

- **Function/requirement:** what the item or step is intended to do.
- **Failure mode:** the specific way it could fail to meet that function.
- **Effect(s):** what happens locally, at the next level, and to the user, system, process, or organization.
- **Cause/mechanism:** why the failure mode could occur, supported by evidence or explicitly marked as a hypothesis.
- **Existing prevention controls:** what is already intended to prevent the cause or failure mode.
- **Existing detection controls:** what is already in place to detect the cause or failure before or after the effect occurs.

Keep cause, failure mode, and effect separate. Describe specific, actionable failure modes rather than broad labels such as “system fails” or “human error.” Consider relevant operating conditions, interfaces, data, dependencies, maintenance, and misuse of the process without assigning blame to individuals.

### 3. Assess and prioritize risk

1. Use the organization's existing severity, occurrence, and detection definitions and scales when provided. Record which rubric and version were used.
2. Assess **Severity (S)** from the effect, **Occurrence (O)** from evidence about likelihood or frequency, and **Detection (D)** from the defined difficulty or likelihood of detection before the effect. State the direction of each scale, especially whether a higher D means harder detection.
3. If no agreed scale or adequate evidence exists, use clearly labeled qualitative descriptions or leave ratings **not rated**. Do not create numeric ratings that appear authoritative.
4. Use an RPN only when the user or organization requires it and the applicable method defines it. If used, show the inputs and calculation. Do not treat RPN as a probability, compare values from incompatible scales, or let a low product conceal a high-severity effect.
5. Follow the organization's action-priority method if one exists. Otherwise prioritize transparently using consequence, evidence, exposure, control weakness, and uncertainty; explain the basis rather than presenting false precision.
6. Distinguish current controls from proposed actions. Do not credit a planned action as an existing control or as reduced residual risk.

### 4. Recommend and track actions

- Tie each recommended action to a specific cause, failure mode, effect, or control gap.
- Prefer eliminating the cause or reducing occurrence where feasible; also consider limiting the effect and improving detection.
- State expected risk reduction and tradeoffs when supported. Do not claim that an action eliminates risk without evidence.
- Assign an owner, target date, or status only when provided or agreed. Otherwise mark it **TBD**.
- Reassess residual risk only after action completion and with the same agreed scales and evidence basis. Keep before-action and after-action ratings distinguishable.
- If evidence is insufficient to select an action, state what test, data, or expert review is needed.

## Decision rules

- Analyze failure modes against intended functions and realistic operating conditions, not against imagined requirements.
- A cause is not a failure mode, and a failure mode is not its effect. Keep each distinct in the record.
- Record existing prevention and detection controls separately and assess whether evidence shows they are implemented and effective.
- Do not infer occurrence ratings from code complexity, number of dependencies, or lack of a known incident.
- Do not infer detectability solely from the presence of logging, tests, alerts, or monitoring; assess coverage, timing, and evidence of effectiveness.
- Preserve high-severity concerns for explicit review even when occurrence is low or an aggregate score is small.
- FMEA is strongest for individual failure modes; it may not reveal combinations, dependencies, or sequences of failures. Recommend complementary analysis when these are material.
- For deliberate, adversarial behavior, use a threat-modeling method as well; FMEA is not a substitute for security threat analysis.
- Do not label the work FMECA or claim criticality analysis unless the requested method and its additional criteria are actually applied.
- Keep recommendations in scope and distinguish evidence, assumptions, and stakeholder judgments.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/fmea/` if missing.
- Save every completed FMEA as a Markdown report in `analysis/fmea/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - Before analysis, `report.py new "<topic>"` creates the report with the date from the system clock, a free file name and the headings from **Expected result**, and prints its path. Write the report into that file.
  - After writing, `report.py check <report-path>` checks the date line, missing or empty sections and anything that looks like a secret or token. Fix every `FAIL` line and run it again.
  - Without Python, apply the rules above by hand and check the same things yourself before finishing.

## Expected result

Provide a concise FMEA report with these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **At a glance:** the count line and at most three key points, as described below.
2. **Scope and method:** FMEA type, item/process boundary, functions, lifecycle phase, environment, and rating method.
3. **FMEA table:** an ID for each row (F1, F2, ...), function, failure mode, effects, causes, current prevention controls, current detection controls, evidence, and ratings where justified.
4. **Priorities:** high-severity concerns by row ID, selected action priorities or RPN method, and rationale.
5. **Recommended actions:** the row ID each action targets, action, targeted cause or control gap, expected effect, owner/status/date if known, and residual-risk plan. Refer to the row ID instead of repeating the failure mode.
6. **Assumptions and open questions:** missing requirements, evidence, stakeholders, and complementary analyses needed.

Include source identifiers and dates where available. Clearly separate existing controls, hypotheses, recommendations, and completed actions.

**At a glance** comes first and must be readable in under a minute:

- The first line is the count line: `N failure modes · N high-severity concerns · N recommended actions · ratings: <rubric used, or not rated>`. Count only what the sections below record.
- Then at most three list items, taken from the top of the report's own priorities. Each item is one plain sentence: what is at stake, for whom, and what is needed, without method terms. After the sentence, in parentheses: the report's own priority or label, the evidence label (for example observed, inferred or unknown), and the ID or heading where the details are.
- State nothing in At a glance that the sections below do not support. Do not raise certainty, add scores or drop an evidence label to make it shorter.

**Reply in chat:** after saving and checking the report, reply with the report path and the **At a glance** section as written in the file. Add only what the user must know beyond that: a check that still fails, a file that could not be saved, or evidence that could not be reached. Do not paste other sections into the chat.

## Boundaries

- FMEA does not guarantee completeness, safety, reliability, or regulatory compliance.
- Do not present unsupported scores, probabilities, or residual-risk reductions as facts.
- Do not modify the analyzed system or process unless the user separately requests implementation.
- Preserve unrelated user changes and report evidence or sources that could not be accessed.
