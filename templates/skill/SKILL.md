---
name: <skill-name>
description: <What the skill does and the specific requests or situations that should activate it.>
---

# <Skill title>

## Purpose

<Describe the job this skill performs and the useful outcome.>

## Use when

- <Concrete request or condition that should activate this skill.>
- <Another relevant condition, if needed.>

## Do not use when

- <Nearby request or condition that belongs to another workflow.>

## Scope and assumptions

- <State whether this skill analyzes only, may edit files, or supports both modes.>
- <Name essential prerequisites and assumptions; do not assume a particular agent tool.>

## Report output

- Before analysis, check the repository root for `analysis/`. Create it if missing, then create `analysis/<skill-name>/` if missing.
- Save every completed analysis as a Markdown report in that folder, even if the user did not separately request a report file.
- Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing report; add a numeric suffix if needed.
- Make the report's first line the date the analysis was performed, formatted `YYYY-MM-DD`. Use the current date from the environment or a reliable clock; do not invent it.
- If file creation is unavailable, provide the report in the response and state that it could not be saved.

## Workflow

1. **Understand the task:** <Resolve the requested outcome and constraints.>
2. **Inspect the repository:** <Find relevant files, local instructions, and existing patterns before deciding what to do.>
3. **Analyze:** <Describe the checks or reasoning needed for this skill's job.>
4. **Act:** <Make only the requested changes, or state findings without editing when the task is analysis-only.>
5. **Verify:** <Run the most relevant available check and explain any limitation.>

## Decision rules

- <Give explicit criteria for important choices or branches.>
- <Say what to do when required information is missing or evidence is inconclusive.>

## Expected result

- <List the expected findings or recommendations to include in the saved report.>
- <State what the agent should summarize for the user and how to link to the report.>

## Boundaries

- Stay within the requested scope and preserve unrelated user changes.
- Do not claim a check passed unless it was actually run and passed.
- <Add any skill-specific safety, compatibility, or scope constraints.>