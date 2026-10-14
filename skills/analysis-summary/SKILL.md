---
name: analysis-summary
description: Use when asked to summarize the analysis reports that other skills saved under analysis/, to give people a simple overview of the most critical findings, or to create a work loop (also called a ralph loop) that fixes the technical findings with tests. Writes analysis/summary/<date>-summary.md for people and one self-contained work loop file per technical analysis. Each analysis keeps its own priorities; they are never ranked against each other. It only prepares the files and then asks the user; it never starts a work loop on its own.
---

# Analysis summary

## Purpose

Turn the reports saved under `analysis/` into two kinds of files in `analysis/summary/`:

1. `<YYYY-MM-DD>-summary.md`, written for people. It starts with a very simple overview of the most critical findings of each analysis, followed by each analysis's own top list and a business summary.
2. `<YYYY-MM-DD>-workloop-<skill-name>.md`, one per technical analysis. A work loop is a file that an agent runs again and again, each time in a fresh session. Each run fixes one finding with a test and records the result in the file. The file is the only memory between runs, so it must contain everything a run needs.

Each analysis keeps its own priority scale and order. Do not merge or rank findings across analyses.

## Use when

- The user asks to summarize, compile or give an overview of the saved analysis reports.
- The user asks what is most critical according to the analyses.
- The user asks for a work loop, ralph loop or fix plan for the findings.

## Do not use when

- There are no reports under `analysis/`. Tell the user which analysis skills to run first.
- The user wants a new analysis. Use the skill for that analysis.
- The user wants the fixes made now in this session. This skill only prepares the summary and the work loops, then asks the user whether to start one.

## Scope and assumptions

- Write only in `analysis/summary/`. Do not change product code, tests, configuration or the source reports.
- Use only what the reports say. Do not re-run analyses, add findings, or change a report's priorities. You may check whether files a report cites still exist and have changed, to judge whether the report is out of date.
- Do not assume a particular agent, operating system, shell or repository layout. The work loop must run with any agent that can read files, edit code and run commands.
- Business findings never become work loop tasks.
- Never start a work loop and never fix product code, even if the request mentions fixing the findings. Whether a loop runs, and when, is the user's decision. See workflow step 5.

Classify each analysis folder:

| Folder under `analysis/` | Kind | Goes to |
| --- | --- | --- |
| `anti-reverse-engineering-analysis` | technical | summary and a work loop |
| `fmea` | technical | summary and a work loop |
| `atam-architecture-analysis` | technical | summary and a work loop |
| `business-model-canvas-analysis` | business | business summary |
| `lean-canvas-analysis` | business | business summary |
| `porters-five-forces-analysis` | business | business summary |
| `cynefin-context-analysis` | decision context | business summary |
| any other folder | read the report: technical if its actions change code, configuration, tests or infrastructure, otherwise business | as for that kind; state your choice under **Reports included** |

## Report output

- Create `analysis/summary/` if it is missing. Never overwrite an existing file; add a numeric suffix instead.
- The first line of every file is today's date, formatted `YYYY-MM-DD`. Use the date from the environment or a reliable clock; do not invent it.
- Write the summary in the language the user writes to you, unless the repository's instructions name a report language. Write work loops in English unless the repository's instructions say otherwise; task details may keep the source report's language.
- If file creation is unavailable, give the summary in your response and state that nothing could be saved. Work loops are useless without files; say that they could not be created.
- **Helper script (optional):** if Python 3 is available (the command may be `python3`, `python` or `py`), use `scripts/report.py` in this skill's folder, with the repository being analyzed as the working directory:
  - `report.py new summary --title "<product or repository name>"` creates `analysis/summary/<date>-summary.md` with the date from the system clock and the headings from **Expected result**, and prints its path.
  - `report.py new "workloop <skill-name>" --bare` creates `analysis/summary/<date>-workloop-<skill-name>.md` with only the date line. If there are several reports from the same skill, add the topic: `"workloop <skill-name> <topic>"`.
  - After writing, run `report.py check <path>` on the summary and `report.py check <path> --no-sections` on each work loop. If the summary is not in English, translate each heading directly, keep their order, and check it with `--no-sections` as well; the date, empty-section and secret checks still run. Fix every `FAIL` line and run the check again.
  - Without Python, apply the rules above by hand.

## Workflow

### 1. Find the reports

1. Read the repository's instructions. If they say where reports are kept or which reports count, follow them.
2. List the folders under `analysis/`, except `summary/`.
3. In each folder, group the reports by topic: the file name without the date and without a numeric suffix. For each topic, use the newest report: the latest date, and on the same date the highest suffix. Use older reports only if the user asks.
4. For each report used, record: analysis, path, date from its first line, code state if the report names a commit, and age in days.
5. Mark a report as out of date if it is older than 30 days, or if it names a commit, the repository uses version control, and files the report cites have changed since that commit. Keep it, but say so.
6. If no reports exist, stop and tell the user which analysis skills could produce them.

### 2. Read each report in its own order

Read each report in full. For each technical report, list its actionable items in the order the report gives them:

| Analysis | Item | Order |
| --- | --- | --- |
| Anti-reverse-engineering | each finding, with the refactoring-plan slice that covers it (changes, guard, done when) | severity CRITICAL, HIGH, MEDIUM, LOW; within a severity VERIFIED before PLAUSIBLE, then the plan's slice order |
| FMEA | each recommended action, with the failure mode, effect and cause it targets | the report's **Priorities** section first, then the remaining actions in table order |
| ATAM | each recommendation tied to a risk | the priority of the scenario the risk affects, as the report states it |
| Other technical | each recommended action or fix | the report's own order |

For each item record the report's own priority label, the evidence label (VERIFIED, PLAUSIBLE, observed, inferred or unknown), the code locations, the effect, the test or guard the report asks for, and how to tell that it is done.

For each business report, list in its own order: the riskiest assumptions, the proposed experiments or next steps, and the main strategic implications. For Cynefin, record the assessed context and the recommended way to act.

When two analyses describe the same problem (same cause or same code location), note "also found by" on both. Do not merge them and do not move either one in its list.

### 3. Write one work loop per technical report

Create one work loop for each technical report that has at least one actionable item. Use the template in **Work loop template**.

- Copy everything a run needs into the task: problem, effect, locations, test, fix and done-when. The source report may be linked for background, but a run must be able to work without it. Do not tell a run to use this skill or its scripts.
- Do not investigate the findings yourself, for example by checking branches, line numbers or keys. Each run of the work loop checks its task against the current code. Note what the report says and put the open points under **Open questions**.
- Keep the report's order. Number the tasks T1, T2, and so on.
- A task must fit in one run: one change plus its tests. If an item is larger and the report describes steps, make one task per step. Otherwise create the task with status BLOCKED and the question "needs a decision or a breakdown".
- Create a task with status BLOCKED, and put the question under Notes, when it needs a person: revoking or replacing a leaked key or password, a product or business decision, a legal question, access to production or paid services, or a change outside the repository. It stays in the list so it is not forgotten. Fill in the fields the report supports and write "not applicable until unblocked" in the others.
- Mark PLAUSIBLE or inferred items "Confirm first" under Evidence. Evidence and status are separate: a task can be both "Confirm first" and BLOCKED.
- Leave out findings the repository's instructions mark as an accepted risk or a deliberate decision. List them in one line under **Open questions** so a person can confirm.
- Fill in the run commands. Replace `<N>` with three times the number of tasks whose status is OPEN (not counting tasks blocked from the start), plus 2. Replace `<AGENT COMMAND>` with the command that runs your own agent non-interactively with a prompt, if you know it, for example `claude -p` (Claude Code), `codex exec` (OpenAI Codex CLI) or `gemini -p` (Gemini CLI); check the agent's documentation for the exact form. If you do not know it, keep the placeholder and tell the user.
- Use one branch name for all work loops from the same summary: `workloop/<summary date>`. If the repository does not use version control, delete the Branch line.
- The work loop files do not need to be committed before the first run; each run commits its own file.

### 4. Write the summary

Write the sections listed under **Expected result**, in that order. The reader is a person who may not know the analysis methods.

**Most critical** must be readable in under a minute:

- Start with one sentence: how many reports were included, their dates, and whether any is out of date.
- Then one short block per analysis, titled with the analysis name, technical analyses first, in the order of the classification table. Do not rank the analyses or say which matters most.
- For each technical analysis, give at most three bullets, taken from the top of its own order and only from its highest levels (for example CRITICAL and HIGH). Each bullet is one plain sentence: what can go wrong, for whom, and what is needed. The sentence itself has no codes or method terms; the report's priority label and the work loop task follow in parentheses after it. Include tasks blocked from the start and say that a person must act. If nothing reaches those levels, write one line saying so.
- For each business analysis, give one or two bullets: its riskiest assumption and the next step it proposes.
- Keep the whole section to at most about fifteen bullets.

**Top lists per analysis** has one subsection per technical analysis with a table of at most ten items in the report's own order: number, finding in one sentence, priority in the report, evidence, where, work loop task, and "also found by" when it applies. Say how many more items the report has.

**Business summary** has one subsection per business or decision-context analysis, with three to five bullets in that report's own order. If a technical finding directly threatens a business claim and both reports support it (for example a finding that lets a competitor copy the product's core rules, against a claimed unfair advantage), add at most three bullets about it at the end.

### 5. Check and report

Run the checks described in **Report output**. Then tell the user:

- the path to the summary, and the **Most critical** bullets;
- each work loop file with its number of tasks, and how many are blocked from the start;
- how to start a work loop (point to the file's **How to run** section), and that loops should run one at a time.

End by asking the user whether to start a work loop, and if so which one. Then stop and wait. Do not start a loop in the same turn, and do not treat the original request (for example "fix the findings") as a yes. Start a loop only after the user answers yes to this question for that specific loop.

## Work loop template

Replace everything in angle brackets. Keep the instruction section word for word.

````markdown
YYYY-MM-DD

# Work loop: <analysis name>, <report topic>

Loop status: RUNNING

- Source report: `<report path>` (dated <date>, code state <commit or unknown>)
- Summary: `<summary path>`
- Branch: `workloop/<summary date>` (only if the repository uses version control)
- Run work loops one at a time, never two at once in the same working copy.

## How to run

Each run is a fresh agent session, started in the repository root, with this instruction:

> Follow the instructions in `<path of this file>`. Do one task, then stop.

Repeat until the line `Loop status:` says FINISHED or PAUSED. You can start each run by hand in a new chat, or use one of these commands, which stop after <N> runs at most.

PowerShell:

```powershell
$f = "<path of this file>"
foreach ($i in 1..<N>) {
    if (Select-String -Path $f -Pattern '^Loop status: (FINISHED|PAUSED)' -Quiet) { break }
    <AGENT COMMAND> "Follow the instructions in $f. Do one task, then stop."
}
```

Bash:

```bash
f="<path of this file>"
for i in $(seq 1 <N>); do
  grep -Eq '^Loop status: (FINISHED|PAUSED)' "$f" && break
  <AGENT COMMAND> "Follow the instructions in $f. Do one task, then stop."
done
```

Runs without a person watching need permission to edit files and run tests without asking. Give that permission only in a separate copy of the repository, such as a git worktree or a container.

## Instructions for each run

Do not edit this section.

You are one run of a repeated work loop. You remember nothing from earlier runs; this file is the only record of progress. Do exactly one task, update this file, then stop.

1. Read this whole file and the repository's own instructions, if it has any (for example AGENTS.md, CLAUDE.md, CONTRIBUTING.md or README.md). The repository's instructions take precedence over this file.
2. If `Loop status` is FINISHED or PAUSED, say so and stop.
3. If the repository uses version control, check for uncommitted changes to files it already tracks, outside the `analysis/` folder. Ignore untracked files such as build output and caches. If there are such changes, set `Loop status: PAUSED`, add a line under Log saying the working copy was not clean, and stop. Otherwise switch to the branch named at the top of this file, creating it from the current branch if it does not exist. Never work on the default branch.
4. Find out how the repository runs its tests and its build: its instructions, project or package files, or CI configuration. If it has no automated tests at all, set `Loop status: PAUSED`, write under Log that a test setup is needed, and stop. Do not add a test framework on your own.
5. Take the first task under Tasks with `Status: OPEN`. The tasks are in priority order.
6. Check that the problem still exists in the current code. If it does not, set the status to ALREADY-FIXED, write under Result how you checked, and go to step 11.
7. If Evidence says "Confirm first", reproduce the problem before changing anything. If you cannot, set the status to BLOCKED, write what you tried under Notes, and go to step 11.
8. Write the test described under Test and run it. It must fail, and fail because of this problem. If you cannot write such a test, do not change product code: set the status to BLOCKED, explain under Notes, and go to step 11.
9. Make the smallest change that fixes the problem and makes the test pass. Stay within the task. Do not change business rules, prices, texts or features beyond what the task describes. If you notice a related problem outside the task, write it under Notes instead of fixing it.
10. Run the full test suite, and the build if the repository has one.
    - If everything passes, set the status to DONE and write the changed files and the name of the new test under Result.
    - If you cannot make everything pass in this run, undo your changes to code and tests, including new files. Add 1 to Attempts and write what you tried under Notes. If Attempts is now 3, set the status to BLOCKED.
    - Never delete, skip or weaken a test to make the suite pass.
11. If no task has `Status: OPEN` any more, set `Loop status: FINISHED`.
12. Add one line under Log: today's date, task id, new status and one short sentence. When the loop is finished, add a line with the number of tasks per status.
13. If the repository uses version control, commit this file together with the files you changed or created for the task, adding each one by name (never everything at once), with the message `workloop <task id>: <task title>`. Add trailer lines, such as a co-author line, if the repository's or your own instructions require them. Never push, amend, rebase, reset or force anything.
14. Stop. Do not start another task.

Set the status to BLOCKED instead of acting, and write the question under Notes, when a task needs a person: revoking or replacing a leaked key or password, a product or business decision, a legal question, access to production or paid services, or a change outside this repository.

Never copy secrets, tokens or personal data into this file or into a commit message. Name the file and line instead.

Statuses: OPEN, DONE, ALREADY-FIXED, BLOCKED.

## Tasks

### T1: <one-sentence title>

- Status: OPEN
- Priority in the report: <the report's own label>
- Source: `<report path>`, <finding id or heading>
- Also found by: <other analysis and its work loop task, or none>
- Evidence: <VERIFIED or observed | PLAUSIBLE or inferred, Confirm first>
- Where: `<file:line>`
- Problem: <what is wrong, in two or three sentences>
- Effect: <what can happen, and to whom>
- Test: <what the test must show, and where it belongs>
- Fix: <the change, at the level of a design note>
- Done when: <criteria someone else can check>
- Attempts: 0
- Result:
- Notes:

## Log

- <date>: work loop created with <n> tasks, <k> of them blocked from the start.
````

## Decision rules

- Never compare or rank findings across analyses. Each analysis keeps its own priority labels and order, in the summary and in its work loop.
- Never change a report's priority. If a report gives no order, keep the order in which it lists the items and say "order as in the report".
- Do not add findings, causes or fixes that the report does not support. If a report is too vague to write a test or a done-when, create the task as BLOCKED and say what is missing.
- If two reports contradict each other about the same thing, keep both as written and add the contradiction to **Open questions**.
- If there are no technical reports, create no work loops and say so under **Work loops**. If there are no business reports, say so under **Business summary**.
- Plain language in **Most critical**: one sentence per item, no codes, no method terms, nothing a person must look up.

## Expected result

The summary file has these sections, using each bold name as a heading. If a section does not apply, keep its heading and explain why under it:

1. **Most critical:** the very short overview for people, one block per analysis, as described in workflow step 4.
2. **Top lists per analysis:** one table per technical analysis, in that analysis's own order.
3. **Business summary:** one subsection per business or decision-context analysis.
4. **Work loops:** each work loop file with its analysis, number of tasks, tasks blocked from the start, and a pointer to its **How to run** section.
5. **Reports included:** analysis, report path, date, code state ("not stated" if the report names none), age, and notes such as out of date or the classification of an unknown folder. List reports that were found but not used, and why.
6. **Open questions:** questions for people: blocked tasks that need a decision, contradictions between reports, out-of-date reports and accepted risks to confirm.

Each work loop file follows **Work loop template**.

## Boundaries

- Write only in `analysis/summary/`. Do not edit the source reports, product code, tests or configuration.
- Never decide on your own to run a work loop. Prepare the files, ask, and wait for an explicit yes for a specific loop.
- Do not present a finding as more or less serious than its report does.
- Never copy secrets, tokens or personal data into the summary or the work loops; name the file and line instead.
- Preserve unrelated user changes, and report reports or files that could not be read.
