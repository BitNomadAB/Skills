---
name: cynefin-context-analysis
description: Use when asked to analyze a decision, incident, initiative, or problem with the Cynefin framework and recommend a context-appropriate way to act.
---

# Cynefin Context Analysis

## Purpose

Use the Cynefin framework to reason about the context in which a decision or problem exists and choose an appropriate way to respond. Make evidence, uncertainty, perspectives, and possible context changes explicit.

Cynefin is a sense-making framework, not a fixed taxonomy, scoring model, or method for labeling people, teams, technologies, or entire organizations.

## Use when

- The user asks for a Cynefin analysis of a specific decision, incident, initiative, or situation.
- The user needs to distinguish what can be handled with established practice, expert analysis, experimentation, or urgent stabilization.

## Do not use when

- The user only wants a technical architecture assessment with no decision context. Use an architecture-specific method, such as ATAM, when appropriate.
- The user expects a definitive domain assignment from code or documentation alone, without evidence about operating conditions, causal relationships, or stakeholder perspectives.

## Scope and assumptions

- First identify the decision or situation to analyze, its boundary, time horizon, and the people affected. Do not classify a whole system when only one decision or part of it is in scope.
- A software or repository analysis can provide evidence about implementation, dependencies, incidents, and constraints. It rarely establishes the full decision context by itself.
- Mark claims as **observed**, **stakeholder-reported**, **inferred**, or **unknown**. Include the source or reasoning for important claims.
- Do not assume there is only one valid perspective or one domain. Different parts of the situation can have different contexts, and context can change over time.
- Use only tools available in the current environment. Never assume a specific agent, operating system, shell, or repository layout.
- Treat the task as analysis. Do not change production systems or non-report files unless the user explicitly requests implementation. Always save a report according to **Report output**.

## Workflow

### 1. Frame the situation

1. State the decision or problem in one sentence. Identify the decision owner, affected stakeholders, system boundary, and time horizon where known.
2. Clarify what outcome matters and what constraints apply, including urgency, reversibility, safety, and available options.
3. Gather relevant evidence from the user, stakeholders, repository, incident history, operational data, and existing decisions. Separate observations from assumptions and interpretations.
4. If the framing is too broad, split it into smaller decisions or aspects that may have different contexts.

### 2. Examine causal context

Ask what evidence supports the way cause and effect behave in this situation:

- Are outcomes sufficiently repeatable that established practice reliably connects a known situation to a response?
- Are causal relationships knowable, but dependent on analysis or expert judgment?
- Do causes and effects become clear mainly in retrospect, with multiple plausible outcomes and no reliable prediction in advance?
- Is the situation unstable enough that immediate action is needed before analysis can be useful?

Do not infer a domain from the amount of code, the number of components, a technology label, or the difficulty of explaining the system. Technical complexity alone does not establish a Cynefin context.

### 3. Identify the best-supported domain or domains

Use these descriptions as working hypotheses, not rigid definitions:

| Context | Causal characteristics | Typical response |
| --- | --- | --- |
| **Clear** (also called Simple or Obvious in older material) | Cause and effect are stable and readily apparent; established practice fits the situation. | **Sense, categorize, respond.** Use appropriate best practice, monitor results, and watch for changing conditions. |
| **Complicated** | Cause and effect exist but are not immediately apparent; analysis or relevant expertise is needed. More than one sound solution may exist. | **Sense, analyze, respond.** Investigate, consult expertise, compare options, then apply suitable good practice. |
| **Complex** | Cause and effect cannot be reliably determined in advance; patterns emerge through interaction and become clearer retrospectively. | **Probe, sense, respond.** Run bounded, safe-to-fail probes, observe outcomes, amplify what works, and dampen what does not. |
| **Chaotic** | There is no useful stable relationship to analyze before acting; delay risks further harm or loss of control. | **Act, sense, respond.** Take proportionate action to stabilize and limit harm, observe the result, then respond as the context changes. |
| **Disorder** (also described as confusion) | The context is not sufficiently understood to choose among the other domains, or perspectives disagree about the context. | Break the situation into smaller parts, surface competing interpretations, gather evidence, and move each part toward a better-understood context. |

Some sources use older names for domains. Use **Clear**, **Complicated**, **Complex**, **Chaotic**, and **Disorder** consistently in the analysis, noting alternate names only when useful to the audience.

### 4. Select actions that fit the context

- In **Clear**, use an established practice only while its conditions still hold. Monitor for exceptions, complacency, or a shift into another context.
- In **Complicated**, show the evidence, expertise, and reasoning behind the analysis. State which assumptions could change the recommendation.
- In **Complex**, prefer multiple small, bounded probes over one irreversible large-scale commitment when feasible. Define what to observe and how to limit downside before each probe.
- In **Chaotic**, prioritize immediate stabilization and safety. Do not delay necessary action while seeking a complete explanation. Reassess once the situation is stable enough to analyze.
- In **Disorder**, do not force a single classification. Decompose the situation and resolve disagreement or missing information before choosing a domain-specific response.
- Match the action to its real risk, reversibility, urgency, and impact. A domain label does not override legal, safety, security, or operational requirements.

### 5. Reassess and communicate

1. Identify indicators that would confirm or challenge the working domain hypothesis.
2. State when to review the decision and what changes would trigger reassessment or a move to another response pattern.
3. Present disagreements and alternate perspectives fairly. Do not hide material uncertainty behind a single label.
4. Tie recommendations to evidence and state their risks, limits, and expected learning or outcome.

## Decision rules

- Domain selection is contextual. Do not assign a permanent Cynefin label to a technology, team, service, or organization.
- When different parts of a situation have different causal characteristics, analyze them separately and describe their dependencies.
- When the domain is disputed, state the competing hypotheses, the evidence each relies on, and the smallest safe next step that can distinguish them.
- Use **Complex** when experimentation and emergent patterns are warranted, not merely when the system is large, unfamiliar, or technically difficult.
- Use **Chaotic** only when urgency and instability make immediate stabilizing action more appropriate than prior analysis. A serious incident is not automatically chaotic if its causal dynamics are understood and stable enough to analyze.
- Do not create numeric domain scores or imply objective certainty unless the user provides a validated method and evidence for doing so.
- A move between domains is an expected possibility. Include a review point instead of treating the initial classification as permanent.
- If evidence is insufficient, report a provisional hypothesis or **Disorder**; explain what information would improve the assessment.

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/cynefin-context-analysis/` if missing.
- Save every completed Cynefin analysis as a Markdown report in `analysis/cynefin-context-analysis/`, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- The report's first line must be the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.

## Expected result

Provide a concise analysis with these sections, omitting a section only when it is not applicable and explaining why:

1. **Decision or situation:** scope, affected parties, desired outcome, and time horizon.
2. **Evidence and perspectives:** observations, sources, assumptions, disagreements, and unknowns.
3. **Context assessment:** best-supported domain or domains, causal reasoning, confidence, and plausible alternatives.
4. **Recommended response:** domain-appropriate actions, constraints, and rationale.
5. **Reassessment:** indicators, review point, and conditions that would change the response.
6. **Open questions:** stakeholder input or evidence still needed.

For Complex contexts, include probe hypotheses, bounds, observations, and decision criteria. For Chaotic contexts, include immediate stabilization actions and how to reassess after stabilization. Do not invent measurements or stakeholder agreement.

## Boundaries

- The framework supports sense-making; it does not prove a classification or guarantee an outcome.
- Make clear whether the assessment is based on repository evidence, stakeholder input, or both.
- Do not substitute a domain label for technical, safety, security, or regulatory analysis.
- Preserve unrelated user changes and report evidence or sources that could not be accessed.