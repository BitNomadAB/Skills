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
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - Before analysis, `report.py new "<topic>"` creates the report with the date from the system clock, a free file name and the headings from **Expected result**, and prints its path. Write the report into that file.
  - After writing, `report.py check <report-path>` checks the date line, missing or empty sections and anything that looks like a secret or token. Fix every `FAIL` line and run it again.
  - Without Python, apply the rules above by hand and check the same things yourself before finishing.

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

Provide a concise report with these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **At a glance:** the count line and at most three key points, as described below.
2. **<Section heading>:** <What the section contains.>
3. **<Section heading>:** <What the section contains. For technical findings, start with a table that gives each finding an ID.>

**At a glance** comes first and must be readable in under a minute:

- The first line is the count line: `<counts defined for this skill, taken only from the sections below>`.
- Then at most three list items, taken from the top of the report's own priorities. Each item is one plain sentence: what is at stake, for whom, and what is needed, without method terms. After the sentence, in parentheses: the report's own priority or label, the evidence label (for example observed, inferred or unknown), and the ID or heading where the details are.
- State nothing in At a glance that the sections below do not support. Do not raise certainty, add scores or drop an evidence label to make it shorter.

**Reply in chat:** after saving and checking the report, reply with the report path and the **At a glance** section as written in the file. Add only what the user must know beyond that: a check that still fails, a file that could not be saved, or evidence that could not be reached. Do not paste other sections into the chat.

## Boundaries

- Stay within the requested scope and preserve unrelated user changes.
- Do not claim a check passed unless it was actually run and passed.
- <Add any skill-specific safety, compatibility, or scope constraints.>