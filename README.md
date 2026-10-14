# Vibe coding is great. But who checks if your idea actually makes sense?

I've put together a free collection of AI skills based on established methods used by software architects, engineers and business strategists.

The idea is simple: You don't need to understand software architecture or business strategy to start asking the right questions.

These skills help your AI coding assistant:

- Figure out if your business idea is viable and who would actually pay for it.
- Analyze your competitors and market.
- Find weaknesses in your app's architecture before they become expensive problems.
- Identify what could go wrong and how to prevent it.
- Help you make better technical and business decisions.

Think of it as giving your AI assistant a set of professional checklists and structured thinking processes.

Instead of just asking AI to build something, let it challenge what you're building and how you're building it.

Works with compatible AI coding agents. Free and open for community contributions.

## Agent Skills

Portable, repository-focused skills that help coding agents analyze and change a codebase. Each skill is a small package a user can copy into a repository and ask an agent to apply.

## Repository layout

```text
skills/
	<skill-name>/
		SKILL.md           # Required: purpose, workflow, and expected result
		references/         # Optional: supporting material loaded when needed
		scripts/            # Optional: deterministic helper scripts
		assets/             # Optional: files used by a skill
templates/
	skill/
		SKILL.md            # Starter template for new skills
		scripts/            # Shared report helper, copied into every skill
tools/                  # Checks and tests for this repository
CONTRIBUTING.md         # Authoring and portability rules
```

Keep each skill self-contained. Add optional folders only when a skill needs them, and keep its `SKILL.md` as the clear entry point.

Every completed analysis is saved as a dated Markdown report under `analysis/<skill-name>/` in the repository being analyzed. The report's first line is the analysis date in `YYYY-MM-DD` format.

## Helper scripts

Some steps are mechanical and give the same answer every time, so the skills include small Python 3 scripts for them. The scripts use only the standard library. They are optional: without Python, the agent follows the same steps from `SKILL.md`.

- `scripts/report.py` in every skill creates the dated report file with the right headings and checks the finished report for a wrong date, missing or empty sections, and anything that looks like a secret.
- `scripts/scan_build.py` in Anti-Reverse-Engineering Analysis searches a built client or package for source maps, keys and tokens, internal host names, staff and admin paths and server-only files. It can also run as a check in a build.

## Using a skill

1. Download or copy the complete skill folder into the skills location supported by the agent or coding environment.
2. Ask the agent to use the skill for the task in the current repository.
3. If the environment does not support skill folders, provide `SKILL.md` as agent instructions. Include any referenced files as well.

Skill discovery locations and tool APIs vary by agent. A skill should explain the work, while the agent maps that workflow to tools available in its environment. Check the target agent's documentation for its expected install location and metadata format.

## Creating a skill

Copy [`templates/skill/SKILL.md`](templates/skill/SKILL.md) into a descriptively named folder under `skills/`, then follow [`CONTRIBUTING.md`](CONTRIBUTING.md). Keep each skill focused on one job and make its workflow and verification criteria explicit.

## Available skills

- [ATAM Architecture Analysis](skills/atam-architecture-analysis/SKILL.md): evaluate an architecture against prioritized quality-attribute scenarios, record tradeoffs and risks, and report evidence and open questions.
- [Cynefin Context Analysis](skills/cynefin-context-analysis/SKILL.md): analyze a decision or situation by its causal context, select an appropriate response pattern, and make uncertainty and context shifts explicit.
- [Business Model Canvas Analysis](skills/business-model-canvas-analysis/SKILL.md): map and assess a current or proposed business model across the nine BMC building blocks, including evidence, assumptions, and validation priorities.
- [Lean Canvas Analysis](skills/lean-canvas-analysis/SKILL.md): map a startup's riskiest business hypotheses across the nine Lean Canvas blocks and prioritize practical validation experiments.
- [Porter's Five Forces Analysis](skills/porters-five-forces-analysis/SKILL.md): assess industry structure and competitive pressure across the five forces, with explicit scope, evidence, and strategic implications.
- [FMEA](skills/fmea/SKILL.md): identify failure modes, causes, effects, and existing controls, then prioritize evidence-based risk-reduction actions.
- [Anti-Reverse-Engineering Analysis](skills/anti-reverse-engineering-analysis/SKILL.md): find what an outsider can learn or do by studying a product's client, API, error responses, tokens or delivered builds, and plan refactoring that keeps business logic on the server, with an automated guard for every fix.
