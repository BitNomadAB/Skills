---
name: atam-architecture-analysis
description: Use when asked to evaluate an existing or proposed software architecture using ATAM, identify quality-attribute risks and tradeoffs, or produce an architecture evaluation report.
---

# ATAM Architecture Analysis

## Purpose

Evaluate how architectural decisions support or threaten important quality goals. Use the Architecture Tradeoff Analysis Method (ATAM) structure to make assumptions, evidence, risks, sensitivities, and tradeoffs explicit.

This skill guides an agent-assisted analysis. It does not replace a facilitated ATAM evaluation with the relevant stakeholders.

## Use when

- The user requests an ATAM, architecture evaluation, or quality-attribute risk and tradeoff analysis.
- The user wants an evidence-based review of how a software architecture supports goals such as availability, performance, security, modifiability, or deployability.

## Do not use when

- The request is only for a code-level defect review, implementation plan, or architecture diagram with no quality-attribute evaluation.
- The user expects a certified, complete, or stakeholder-approved ATAM from repository evidence alone.

## Scope and assumptions

- Treat the task as analysis. Do not modify production code or architecture unless the user separately requests implementation.
- Always save each completed ATAM analysis as a report according to **Report output**. This does not authorize changes to production code or architecture.
- A repository reveals only part of an architecture. Mark information as **observed**, **stakeholder-confirmed**, **inferred**, or **unknown**. Do not present assumptions as facts.
- Do not invent business goals, quality targets, stakeholder priorities, operational conditions, or measurements. Ask focused questions when needed; otherwise record the gap and its effect on confidence.
- Use only tools available in the current environment. Never assume a particular agent, operating system, shell, diagramming tool, or repository layout.

## Workflow

### 1. Establish scope and evidence

1. Confirm the system or subsystem, architecture version, evaluation purpose, and whether the user wants a written report.
2. Read relevant repository instructions before inspecting or changing files.
3. Locate useful evidence: architecture views and decision records, service and module boundaries, dependency and deployment configuration, data flows, interfaces, security controls, tests, and operational configuration.
4. Record the source for each important architectural claim. Distinguish intended design in documentation from behavior visible in implementation and deployment configuration.
5. Identify missing evidence and stakeholders who can confirm business drivers, scenario priorities, operating conditions, and acceptable measures.

### 2. Follow ATAM Phase 1: evaluation team and architecture

Work through the first six ATAM steps. If the team or business context is unavailable, say so and mark the affected results as provisional.

1. **Present ATAM and set expectations.** Explain the scope, participants available, evidence limits, and intended output.
2. **Present business drivers.** Capture the system's purpose, stakeholders, constraints, important capabilities, and business goals. Trace each driver to its source or mark it unknown.
3. **Present the architecture.** Summarize relevant components, connectors, runtime and deployment structure, data flows, external dependencies, and important decisions. Use only views supported by evidence.
4. **Identify architectural approaches.** Record significant patterns, tactics, technologies, and design decisions that shape quality attributes. Link each to its evidence and rationale when known.
5. **Build and prioritize a quality-attribute utility tree.** Refine business goals into relevant quality attributes and concrete scenarios. Prioritize with stakeholders when possible; keep business importance and technical difficulty as separate judgments.
6. **Analyze architectural approaches.** For the highest-priority scenarios, trace how the architecture is expected to respond. Identify decisions that enable, constrain, or threaten that response, and record missing evidence.

### 3. Follow ATAM Phase 2: stakeholders and results

7. **Elicit and prioritize stakeholder scenarios.** Ask stakeholders for concrete situations that matter to them, then prioritize them. If stakeholders are unavailable, label repository-derived scenarios as candidates, not approved priorities.
8. **Analyze the prioritized scenarios.** Repeat the scenario analysis for the agreed priorities. Refine scenarios and priorities when new evidence changes the assessment.
9. **Present results.** Summarize the scope, architecture, prioritized scenarios, findings, risk themes, recommendations, assumptions, and unresolved questions. Separate evidence from interpretation.

### 4. Make scenarios testable

When evidence is available, describe each quality-attribute scenario using:

- **Source:** who or what produces the stimulus.
- **Stimulus:** the event or condition.
- **Environment:** the conditions under which it occurs.
- **Response:** the system behavior expected.
- **Response measure:** a measurable criterion for judging the response.

Keep missing fields explicit as unknown or to be confirmed. Do not fabricate numeric targets. Use only quality attributes relevant to the stated business drivers; examples include availability, performance, security, modifiability, interoperability, and operability.

### 5. Classify findings carefully

- **Risk:** an architectural decision or unresolved issue may prevent a scenario's response from meeting its goal.
- **Non-risk:** available evidence suggests a decision supports a particular scenario under stated assumptions. This is not a guarantee that the architecture is risk-free.
- **Sensitivity point:** a decision or parameter can significantly affect the response to a quality-attribute scenario.
- **Tradeoff point:** one decision affects multiple quality attributes, with a benefit to one potentially creating a cost to another.
- **Risk theme:** a group of related risks with a shared architectural cause or concern.

For each finding, cite the relevant repository evidence or stakeholder input, explain the cause-and-effect reasoning, identify affected scenarios and quality attributes, and state confidence and unknowns. Do not label every concern a risk if the evidence does not support that conclusion.

## Decision rules

- Prioritize scenarios from business goals and stakeholder input, not from a generic checklist of quality attributes.
- Assess technical difficulty separately from business importance. Explain the basis for each judgment; do not imply false precision with unsupported scores.
- If business drivers or stakeholders are unavailable, continue only as a provisional, repository-based assessment and list the questions needed to validate it.
- If architecture documentation conflicts with code or deployment configuration, report the discrepancy rather than silently choosing one source.
- If a scenario has no measurable response criterion, retain it as incomplete and state what measurement or target is needed.
- If the evidence cannot establish a risk, sensitivity, or tradeoff, report the concern as an open question instead of overstating the finding.
- Tie each recommendation to a finding or evidence gap. State the expected benefit, relevant quality attribute, and any cost or tradeoff when known.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/atam-architecture-analysis/` if missing.
- Save every completed ATAM analysis as a Markdown report in `analysis/atam-architecture-analysis/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - Before analysis, `report.py new "<topic>"` creates the report with the date from the system clock, a free file name and the headings from **Expected result**, and prints its path. Write the report into that file.
  - After writing, `report.py check <report-path>` checks the date line, missing or empty sections and anything that looks like a secret or token. Fix every `FAIL` line and run it again.
  - Without Python, apply the rules above by hand and check the same things yourself before finishing.

## Expected result

Provide a concise evaluation with these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **Executive summary:** scope, overall assessment, and most important findings.
2. **Scope and evidence:** system boundary, sources inspected, participants, assumptions, and limitations.
3. **Business drivers and utility tree:** goals, selected quality attributes, scenarios, and priority basis.
4. **Architecture and approaches:** relevant design decisions with evidence.
5. **Scenario analysis:** expected response, response measure, reasoning, and evidence for each prioritized scenario.
6. **Findings:** risks, non-risks, sensitivity points, tradeoff points, and related risk themes.
7. **Recommendations and open questions:** actionable next steps and what stakeholders must confirm.

Use tables when they improve comparison. Keep observations, interpretations, and recommendations distinguishable. Include file paths or other source identifiers for repository evidence.

## Boundaries

- A repository-only assessment is not a complete ATAM workshop and must not be described as stakeholder-approved.
- Do not claim that a system satisfies a quality attribute without an applicable scenario, evidence, and response measure.
- Do not change production code or architecture unless the user requests implementation. The report described under **Report output** is required.
- Preserve unrelated user changes and report checks or sources that could not be accessed.