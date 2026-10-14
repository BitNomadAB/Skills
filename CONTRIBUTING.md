# Authoring Skills

Skills are instructions for agents working in an unfamiliar repository. They should be usable after being copied, without relying on the history or setup of this repository.

## Portability

- Use plain Markdown and keep `SKILL.md` as the package entry point.
- Keep required instructions and assumptions in the skill itself. Treat `references/`, `scripts/`, and `assets/` as optional supporting material.
- Do not assume a particular operating system, shell, editor, agent, model, tool name, package manager, or repository layout. Describe the goal and let the agent use equivalent capabilities available in its environment.
- If a step genuinely requires a specific tool or runtime, state the prerequisite and give a practical fallback where possible.
- Avoid absolute paths, machine-specific configuration, hidden credentials, network dependencies, and instructions that only work in this repository.
- Explain any supporting files using paths relative to the skill folder. A skill copied without those files must not silently depend on them.

## Clear instructions

- Give each skill one recognizable job and a short, concrete description of when to use it. State important exclusions to prevent accidental activation for unrelated work.
- Use direct language, defined terms, and ordered steps. Put critical constraints near the step they govern.
- Make the workflow usable with limited context: direct the agent to inspect relevant repository files and instructions instead of assuming prior knowledge.
- Include decision criteria for meaningful branches. Separate required behavior from optional suggestions, and avoid vague directions such as “be thorough” without saying what to check.
- Say whether the task is analysis-only or may change files. Keep any changes within the requested scope and preserve unrelated user work.
- Specify what a useful result looks like: expected changes or findings, validation to run, and what to report when validation is unavailable or fails.
- Prefer concise, literal wording that smaller local models can follow. Add examples or edge cases only when they disambiguate a real decision; keep deeper reference material in separate files when useful.

## Analysis reports

- Every skill that performs an analysis must save a Markdown report in the repository being analyzed, even when the user did not separately request a report file.
- Before analyzing, check the repository root for `analysis/`. Create it if it does not exist, then create `analysis/<skill-name>/` if needed. Reuse existing folders and preserve their contents.
- Use a filename such as `<YYYY-MM-DD>-<topic-slug>.md`. If it already exists, do not overwrite it; add a numeric suffix to make a new filename.
- The report's first line must be the date the analysis was performed, in ISO format `YYYY-MM-DD`. Use the current date supplied by the environment or a reliable clock, not a file timestamp. Do not invent a date.
- If the agent cannot create files in the repository, provide the report in the response and state that it could not be saved.
- Keep the report within the skill's stated scope. Creating a report does not authorize unrelated changes to the product or repository.
- Give each analysis skill the shared helper `scripts/report.py` and a `scripts/report-sections.txt` that lists the bold section names from **Expected result**, one per line. The helper creates the dated report file and checks the finished report. The skill must still describe the same rules in words, so it works without Python.
- `report.py` is identical in every skill. Edit only `templates/skill/scripts/report.py`, then run `python tools/check_skills.py --fix` to copy it to all skills.
- A skill that collects other reports may use another folder under `analysis/` when its `SKILL.md` says so. Set that folder with a `folder: <path>` line in `report-sections.txt`; Analysis Summary uses `folder: analysis/summary`.

## Helper scripts

- Write scripts in Python 3.8 or later using only the standard library, so they run wherever Python does. Describe each script's usage at the top of the file and in `SKILL.md`, with paths relative to the skill folder.
- A script reads the repository and writes only what the skill says it creates. No network access.
- Never print a secret in full; show a short prefix and the length.
- Use exit code 0 for OK, 1 for problems found and 2 for usage errors, so a script can also run as a check in a build.
- Before committing, run `python tools/check_skills.py` and `python tools/test_scripts.py`. Add tests for new script behavior to `tools/test_scripts.py`, and build fake credentials at run time so the repository never contains strings that secret scanners flag.

## Package shape

```text
skills/<skill-name>/
  SKILL.md
  references/   # Optional, for detailed material not needed on every use
  scripts/      # Optional, for repeatable actions that benefit from code
  assets/       # Optional, for other required package files
```

Use lowercase, hyphen-separated folder names. Keep the package easy to copy as a unit. Do not add optional directories just to match the example.

## Review checklist

- Can an agent identify when to use the skill from its description alone?
- Can it follow the core workflow without access to this repository or a specific vendor's tools?
- Are prerequisites, scope, decision points, and expected results explicit?
- Are file changes and analysis-only behavior clearly distinguished?
- Can a user copy the whole skill folder and understand any dependencies?
- Does the skill say how to validate its work and report limitations?
- Does every completed analysis save a dated report under `analysis/<skill-name>/`, with the date on its first line?
- Do `scripts/report-sections.txt` and **Expected result** list the same sections, and do `python tools/check_skills.py` and `python tools/test_scripts.py` pass?
