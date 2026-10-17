---
name: anti-reverse-engineering-analysis
description: Use when asked to analyze how much a product gives away to someone who studies its client, its API or a delivered device, so they can attack its users or copy it, and to plan refactoring that keeps business logic on the server and gives callers only what they need. Covers business logic in the client, shipped code and data, API, error and realtime responses, tokens, headers, enumeration and scraping, and native clients, game clients and on-site devices.
---

# Anti-reverse-engineering analysis

## Purpose

Find what an outsider can learn or do by studying everything that leaves the
servers: the client code, the responses, the tokens and any delivered build or
device. Then plan refactoring so that:

- the server decides every rule that matters, and the client only shows results
  and sends what the user wants to do;
- each caller gets only what its current view needs, and nothing about other
  users or the inside of the system;
- an outsider cannot list or copy the product's data or rules in bulk.

The principle behind every check: anything that reaches a machine the owner
does not control can be read and changed. Hiding it in the client only delays
an attacker. Obfuscation is never a fix on its own.

## Use when

- The user asks how exposed a product is to reverse engineering, exploits built
  from studying the client or API, scraping, or fast copying by a competitor.
- The user wants the client to be a thin client without business logic.
- The user wants to know what error messages, tokens, responses or builds give
  away.
- Before a launch, a first public build, a first delivery of a device, or a
  first public data release.

## Do not use when

- The user wants a general security review of authentication, authorization,
  injection and similar flaws. That belongs to a security review; this skill
  links to such findings but does not repeat them.
- The user wants legal advice. Mention legal protection only as an open question
  for a lawyer.
- The user wants the fixes implemented. This skill analyzes and plans only.

## Scope and assumptions

- Analysis only. Do not change product code, tests, configuration or plans.
  The only file you create is the report.
- Use only tools available in your environment. Do not assume a particular
  agent, operating system, shell, framework or repository layout.
- Do not contact production or shared environments, and do not send requests to
  live systems, unless the user explicitly allows it. Local builds and local
  tests are allowed when the repository's instructions allow them.
- Mark every claim as **observed** (you read or ran it), **inferred** (follows
  from what you read) or **unknown**.

## Report output

1. Read the repository's instructions first (for example `AGENTS.md` or another
   agent instruction file, `CONTRIBUTING.md`, a review protocol or a docs
   index). If they define where skill reports go, how they are named, which
   language they use or a report template, follow them.
2. Otherwise check the repository root for `analysis/`. Create it if missing,
   then `analysis/anti-reverse-engineering-analysis/` if missing.
3. Name the report `<YYYY-MM-DD>-<topic-slug>.md`. Never overwrite an existing
   report; add a numeric suffix if needed.
4. Make the first line the date of the analysis, formatted `YYYY-MM-DD`. Use the
   current date from the environment; do not invent it.
5. If you cannot create files, give the report in your response and say that it
   could not be saved.
6. If Python 3 is available (the command may be `python3`, `python` or `py`),
   use `scripts/report.py` in this skill's folder, with the repository being
   analyzed as the working directory:
   - After defining the scope (workflow step 2), `report.py new "<scope>"`
     creates the report with the date from the system clock, a free file name
     and the headings of **Report template**, and prints its path. Add
     `--dir <folder>` if the repository's instructions set another folder, or
     `--bare` for only the date line if they set another template or language.
   - After writing, `report.py check <report-path>` checks the date line,
     missing or empty sections and anything that looks like a secret or token.
     Add `--no-sections` when the repository's own template or language
     applies. Fix every `FAIL` line and run it again.

   Without Python, apply the same rules and checks by hand.

## External documentation

- **Purpose:** if you can read the web, you may look up official documentation
  or a vendor's published material to support a claim this analysis needs, for
  example whether a key type is meant to be public, or what a framework includes
  in a production build. Forums and blog posts are not evidence.
- **Confidentiality:** what you type into a search leaves the machine. Never put
  code, secrets, internal names, unreleased product or feature names, or
  customer data into a search. Search for the vendor, product or standard by its
  public name.
- **No contact with the product's own systems:** do not open the product's live
  services or administration pages.
- **Label and record:** label such a claim **external source**, never observed,
  and list each source in a **Sources** section at the end of the report: ID
  (S1, S2, ...), title, publisher, link, publication date (or "undated"), date
  read (YYYY-MM-DD), and what it supports.
- **Without web access:** mark the claim **unknown**.

## Workflow

### 1. Check whether you may run the review

- Read the repository's instructions in full before reading code.
- If they say a model may not review code written by its own model family, or
  give another independence rule, find out who wrote the code in scope (the
  request, plan files, co-author lines in commit messages). If the author
  is unknown, ask and wait. If you may not review it, stop and say which model
  family wrote the code and that another family must run the review.
- Note the owner's deliberate decisions and accepted risks written in the
  repository. They are rules, not findings.

### 2. Define the scope

- The user names the scope: a product, an app, a set of packages, a commit
  range or the whole repository. If it is missing, ask.
- Write down what the product is, who its users are, which roles exist (for
  example member, staff, admin, organization, anonymous visitor) and what its
  core value is: the rules, data or know-how a competitor would want.

### 3. Map what leaves the servers

List every surface in scope with its path in the repository. Skip a kind that
does not exist and say so.

1. **Client code and data:** web bundles and their lazy-loaded parts,
   translation files, client configuration and environment files, service
   workers, source maps; desktop, mobile and game builds with their script
   packages, data files and assets; delivered devices or on-site servers with
   their programs, databases, keys and configuration.
2. **Responses:** API response bodies, status codes and headers; error
   responses; realtime messages (WebSocket, server-sent events, push); file
   downloads and exports; e-mails and notifications with links.
3. **Credentials the client holds:** access and refresh tokens, cookies, API
   keys, signed URLs, tickets for other servers.
4. **Public metadata:** API specifications and documentation pages, health and
   version endpoints, robots and sitemaps, `.well-known`, error pages.
5. **Listing surfaces:** list, search, map, autocomplete and pagination
   endpoints, identifiers in URLs, public profile or detail pages.
6. **Things that must never leave:** prompts, model reasoning, matching,
   ranking and scoring rules, reference and test datasets, internal
   identifiers, secrets.

For each surface, note who can reach it: anyone on the internet, logged-in
users, a customer's network, or only an internal network. An internal surface
still counts, but its severity depends on who can reach it.

Prefer evidence over configuration: if you can build the production client
locally without side effects, build it and search the output. Otherwise read the
production build configuration and say that the output was not inspected.

If Python 3 is available, run `scripts/scan_build.py <build-output>` from this
skill's folder on each build, package (APK, IPA, JAR, ZIP) or device image in
scope. It lists source maps, keys and tokens, internal, test and local hosts,
private addresses, staff and admin paths and code files, and server-only files,
without printing secrets in full. Add `--forbid "<text>"` for names that must
not ship, such as unreleased features or internal code names found in step 2.
Treat every hit as a candidate to check in step 4. A clean scan covers only the
patterns that `--list-rules` shows, so still work through the whole checklist.

### 4. Check each surface

Use the checklist below. For every surface, write down the result before moving
on: a finding, or one line saying what was checked and found clean.

### 5. Verify the findings

For each finding, follow the chain in the code from the surface to the cause.

- **VERIFIED:** you followed it line by line, or ran it locally.
- **PLAUSIBLE:** say what is missing to confirm it.

Drop anything without a concrete outsider scenario. Style preferences that no
rule requires are suggestions, not findings.

### 6. Plan the refactoring

Build the plan only from VERIFIED findings, plus PLAUSIBLE findings marked as
needing confirmation first. See **Refactoring plan**. Do not implement it.

### 7. Save the report and summarize

Save the report as described in **Report output**, and run the report check if
the script is available.

Write **At a glance** last, from the finished report, and keep it first in the
file:

- The first line is the count line:
  `N findings · CRITICAL a · HIGH b · MEDIUM c · LOW d · VERIFIED v · PLAUSIBLE p`.
- Then at most three list items, the most severe findings in report order. Each
  item is one plain sentence: what an outsider can do, to whom, and what is
  needed, without method terms. After it, in parentheses: severity, verdict and
  finding ID, for example `(CRITICAL · VERIFIED · CRITICAL-1)`.
- State nothing there that the findings below do not support. Never drop a
  PLAUSIBLE label or raise a severity to make it shorter.

**Reply in chat** with the report path and the **At a glance** section as
written in the file. Add only what the user must know beyond that: a check that
still fails, a file that could not be saved, or evidence that could not be
reached. Do not paste other sections into the chat.

## Checklist

Each item says what counts as a finding. Tag each finding with its category.

### LOGIC: business logic in the client

- List every rule the client enforces or computes: prices, fees, discounts,
  totals, quotas, limits, capacities, age or eligibility rules, deadlines,
  state transitions, permissions, game outcomes and rewards.
- For each, find where the server enforces the same rule.
- **Finding:** the server accepts a request the client would block; the server
  trusts a value the client computed (a price, total, score, result, role,
  time); a feature is protected only by hiding it in the client.
- **Not a finding:** the client repeats a rule for a better user experience
  while the server enforces it too.

### LEAK: shipped code and data

- Staff, admin or internal features in a bundle that anyone can download, even
  if the route is guarded. Lazy-loaded parts can be fetched without logging in
  and show every endpoint and field they use.
- Features, routes, translation strings, feature-flag names or game content
  that are not released yet.
- Source maps, debug builds, comments, internal host names or addresses, keys
  other than those meant to be public.
- Server-only code, test tools, bots or administration tools inside a client
  build.
- A list of every error code, permission or internal state shipped to the
  client when the client needs only some of them.

### LEAK: response content

- For each response, compare the fields returned with the fields the view
  that requests it uses. Extra fields are findings when they concern other
  users, internal state, internal relations, audit data or business volume.
- Sequential or guessable identifiers: they reveal how many users, orders or
  events exist and let anyone walk through them.
- Exact numbers that reveal business metrics, exact locations or times where a
  rounded or coarse value is enough.
- Realtime messages, exports and e-mails follow the same rule as responses.

### ORACLE and LEAK: error responses

- An error response contains a stable code and, at most, the fields of the
  caller's own input that failed. It never contains an internal message, stack
  trace, database or driver error, file path or library version.
- **Oracle:** any difference in status, code, message, fields or response time
  that tells an outsider something they are not entitled to know, such as:
  - "does not exist" versus "not allowed" for another user's resource
    (prefer the same answer for both);
  - registration, login, password reset, invitation or e-mail change that
    reveals whether an account or address exists;
  - validation that reveals the state of someone else's data.
- **Not a finding:** precise errors about the caller's own input and the
  caller's own account state.

### Tokens and sessions

- A JSON Web Token is encoded, not encrypted; its holder and any script that
  can read it can read every claim. Claims carry only what the client needs.
  Personal data, full permission lists or internal role names in a token are
  findings unless the client needs them.
- Storage: a token in `localStorage` or `sessionStorage` can be read by any
  script that runs on the page, so one injected script takes over the account.
  An `HttpOnly` cookie cannot be read by scripts. Report where each token is
  stored and what an injected script could take.
- Token lifetime, refresh token transport, invalidation on logout and password
  change, tokens in URLs (they end up in logs and referrer headers).
- Tickets for other servers (game, match, file) are short-lived, signed and
  bound to one user and one purpose.

### Headers and metadata

- `Server`, `X-Powered-By` or other version headers.
- A Content Security Policy that limits where scripts may come from, which
  reduces what an injected script can do.
- `Strict-Transport-Security`, frame options, `Cache-Control` on responses with
  personal data, a CORS allowlist rather than reflection of any origin.
- API specifications, documentation pages, debug and profiling endpoints are
  off in production. Health endpoints that anyone can reach do not show
  versions or dependency state.

### SCRAPING: listing and bulk extraction

- Can an anonymous visitor or ordinary user list all users, events, items,
  prices or datasets through list, search, map, autocomplete, pagination or by
  walking identifiers?
- Page size has a maximum. Quotas exist per account and per address, not only
  per address. Expensive endpoints (model calls, search, exports) have quotas.
- Logging or alerts exist for unusual volumes.
- Login takes the same time for an unknown account as for a wrong password.

### CLONE: the product's core value

- Which parts of the core value from step 2 can be rebuilt from client code or
  responses: matching, ranking or scoring rules and weights, prompts, model
  reasoning, reference data, pricing logic, algorithms?
- Responses that expose scores, weights, reasoning or intermediate results
  where the user needs only the outcome.
- Endpoints that answer arbitrary queries in volume, so that someone can
  collect the answers and rebuild the data or train a model on them.
- Published datasets, exports or releases that carry no way to trace a leaked
  copy back to its recipient, for example a watermark per recipient.

### Native clients, game clients and delivered devices

Use when the product ships a program or device.

- Assume the full build will be decompiled. Script packages restore to nearly
  the original source, and an encryption key stored inside the program can be
  extracted. The question is therefore not whether it can be read but whether
  reading it helps.
- The server is the authority for competitive and economic state, and it
  filters what each client may know before sending it. Hidden information
  (other players' inventories, positions out of view, private stats) never
  reaches a client that is not entitled to it.
- Bots: can the server detect automated play, for example by reaction-time
  statistics, replays and reports? Bans tie to an account that is costly to
  replace, such as a store account that owns the product.
- Ownership: the server checks ownership with the store or account system, not
  the client.
- Delivered devices: disk encryption tied to the device's hardware, no local
  administrator account for the customer, only signed updates, keys unique per
  device, tamper evidence, and only the data that device needs.

## Severity

If the repository defines a severity scale, use it. Otherwise:

| Severity | Meaning |
| --- | --- |
| CRITICAL | An outsider can harm other users (take over accounts, read or change their data, move money) or bypass a business rule, without special conditions. |
| HIGH | The same with a precondition; or other users' personal data or existence is revealed; or core value from step 2 can be extracted. |
| MEDIUM | Internal structure, unreleased features or business metrics are revealed, or scraping is made easy. |
| LOW | Hardening without a concrete scenario today. |

## Refactoring plan

Group the findings into slices, one slice per surface or per shared cause.
For each slice write:

- **Goal:** what an outsider can no longer learn or do afterwards.
- **Findings covered:** their identifiers.
- **Changes:** which modules or files change and how, at the level of a design
  note, not code.
- **Guard:** an automated check in the repository's normal test or build run
  that fails if the problem returns. Examples: a test that each response type
  only has allowlisted fields; a build check that the production bundle
  contains no staff routes, forbidden strings or source maps; a test that
  login, registration and password reset give the same answer and similar
  timing for known and unknown accounts; a test of response headers; a test
  that a client build contains no server-only files. A fix without a guard
  is not done. For findings in shipped code, propose `scripts/scan_build.py`
  from this skill as that build check: copy it into the repository and run it
  on the build output with `--forbid` for each text that must not return and
  `--allow` for accepted hits. It exits with code 1 when a SECRET or LEAK hit
  is found.
- **Size:** S, M or L, and what makes it so.
- **Risk:** what could break for users or other systems, and how to roll out.
- **Done when:** observable criteria someone else can check.

Order the slices: CRITICAL and HIGH first; within the same severity, cheap
guards first. If the repository has its own planning format (for example plan
files with phase targets), say which format the plan should be converted to,
and convert it only if the user asks.

## Report template

The table under **Findings** is an index with one row per finding, using the
same ID as the finding's own subsection. The subsections keep the full outsider
scenario and verdict; the table does not replace them.

```markdown
YYYY-MM-DD

# Anti-reverse-engineering analysis: <scope>

Code state: <commit or "uncommitted">. Code author: <model family or person,
or unknown>. Reviewer: <model family, agent, model id>.

## At a glance

N findings · CRITICAL a · HIGH b · MEDIUM c · LOW d · VERIFIED v · PLAUSIBLE p

- <plain sentence> (<SEVERITY> · <VERDICT> · <ID>)

## Scope

<what was read, built or run; what was skipped and why>

## Product and core value

<users, roles, what a competitor would want>

## Exposure map

| Surface | Path | What an outsider gets | Status |
| --- | --- | --- | --- |

## Findings

| ID | Severity | Category | Finding in one sentence | Location | Verdict | Slice |
| --- | --- | --- | --- | --- | --- | --- |

### <SEVERITY>-<n> [<CATEGORY>]: <one sentence>

- Location: `<file:line>` and the code that makes it possible
- Outsider scenario: <what they do, step by step, and what they learn or achieve>
- Why tests miss it: <...>
- Verdict: VERIFIED | PLAUSIBLE (<what is missing>)

## Clean areas

<one line per surface checked without findings>

## Refactoring plan

### Slice <n>: <goal>

<findings, changes, guard, size, risk, done when>

## Open questions

<questions for the owner, including legal questions for a lawyer>
```

## Boundaries

- Stay within the requested scope and preserve unrelated changes in the
  working tree.
- Do not claim that a check passed unless you ran it and it passed.
- Do not read another reviewer's report for the same scope until yours is
  saved.
- Never put secrets, tokens or personal data you come across into the report;
  name the file and line instead.
