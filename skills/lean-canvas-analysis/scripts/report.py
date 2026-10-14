#!/usr/bin/env python3
"""Create and check the analysis report for this skill.

Run it with the repository being analyzed as the working directory:

  python <skill-folder>/scripts/report.py new "<topic>"
  python <skill-folder>/scripts/report.py check <report-path>

new    Creates analysis/<skill-name>/<YYYY-MM-DD>-<topic-slug>.md in the
       repository root (the nearest folder above the working directory that
       contains .git). The date comes from the system clock, an existing
       report is never overwritten (a numeric suffix is added instead), and
       the file starts with the date line, a title and the required section
       headings. Prints the path of the new file.
         --dir DIR   create the report in DIR instead
         --bare      write only the date line
         --root DIR  treat DIR as the repository root

check  Fails when the first line is not today's date (or --date), when the
       date in the file name differs from the first line, when a required
       section heading is missing or a section is empty, or when a line looks
       like a secret or token.
         --date YYYY-MM-DD  the day the analysis was performed, if not today
         --no-sections      skip the section checks, for example when the
                            repository prescribes its own template or language

The skill name and title are read from ../SKILL.md. Required sections are read
from report-sections.txt next to this script, one heading per line.

Exit codes: 0 OK, 1 problems found, 2 usage or file error.
Needs Python 3.8 or later and only the standard library.
"""

import argparse
import datetime
import os
import re
import sys
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
SECTIONS_FILE = os.path.join(SCRIPT_DIR, "report-sections.txt")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Credentials that must never be copied into a report. Only the pattern name
# is printed, never the matched text.
SECRET_PATTERNS = [
    ("private key", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ("AWS access key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("Stripe secret key", r"\b[rs]k_(?:live|test)_[0-9A-Za-z]{10,}"),
    ("webhook signing secret", r"\bwhsec_[0-9A-Za-z]{10,}"),
    ("GitHub token", r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{22,})"),
    ("Slack token", r"\bxox[abposr]-[A-Za-z0-9-]{10,}"),
    ("AI provider API key", r"\bsk-(?:ant-|proj-|svcacct-)[A-Za-z0-9_-]{20,}|\bsk-[A-Za-z0-9]{40,}\b"),
    ("signed token (JWT)", r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    ("password in a URL", r"\b[a-z][a-z0-9+.-]{1,20}://[^\s/:@\"'`<>]{1,64}:[^\s/@\"'`<>]{1,128}@"),
]
SECRET_RES = [(name, re.compile(pattern)) for name, pattern in SECRET_PATTERNS]

TRANSLITERATE = str.maketrans({
    "æ": "ae", "Æ": "ae", "ø": "o", "Ø": "o", "ß": "ss", "œ": "oe", "Œ": "oe",
    "ł": "l", "Ł": "l", "đ": "d", "Đ": "d", "þ": "th", "Þ": "th",
})


def read_skill_info():
    """Return (name, title) from ../SKILL.md, falling back to the folder name."""
    name = os.path.basename(SKILL_DIR)
    title = None
    try:
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
    except OSError:
        return name, name
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            m = re.match(r"name:\s*(\S.*?)\s*$", lines[i])
            if m:
                name = m.group(1).strip("'\"")
    for line in lines[body_start:]:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    return name, title or name


def read_sections():
    try:
        with open(SECTIONS_FILE, encoding="utf-8-sig") as f:
            lines = [line.strip() for line in f]
    except OSError:
        return []
    return [line for line in lines if line and not line.startswith("#")]


def find_repo_root(start):
    path = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return os.path.abspath(start)
        path = parent


def slugify(text):
    text = unicodedata.normalize("NFKD", text.translate(TRANSLITERATE))
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return slug[:60].rstrip("-") or "analysis"


def normalize(text):
    words = re.sub(r"[\W_]+", " ", text.lower()).split()
    while words and words[0].isdigit():
        words.pop(0)
    return " ".join(words)


def display_path(path):
    rel = os.path.relpath(path)
    return rel if not rel.startswith("..") else path


def parse_date(text):
    if not DATE_RE.match(text):
        return None
    try:
        return datetime.date.fromisoformat(text)
    except ValueError:
        return None


def parse_headings(lines):
    """Return (line_index, level, text) for each ATX heading outside code fences."""
    headings = []
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2)))
    return headings


def cmd_new(args):
    name, title = read_skill_info()
    today = datetime.date.today().isoformat()
    if args.dir:
        folder = os.path.abspath(args.dir)
    else:
        root = os.path.abspath(args.root) if args.root else find_repo_root(os.getcwd())
        folder = os.path.join(root, "analysis", name)
    os.makedirs(folder, exist_ok=True)

    parts = [today, ""]
    if not args.bare:
        parts += ["# %s: %s" % (title, args.topic.strip()), ""]
        for section in read_sections():
            parts += ["## " + section, ""]
    content = "\n".join(parts).rstrip("\n") + "\n"

    base = "%s-%s" % (today, slugify(args.topic))
    number = 1
    while True:
        filename = base + (".md" if number == 1 else "-%d.md" % number)
        path = os.path.join(folder, filename)
        try:
            with open(path, "x", encoding="utf-8", newline="\n") as f:
                f.write(content)
            break
        except FileExistsError:
            number += 1
    print(display_path(path))
    return 0


def cmd_check(args):
    name, _ = read_skill_info()
    expected = datetime.date.today()
    if args.date:
        expected = parse_date(args.date)
        if expected is None:
            print("FAIL  --date must be a real date written YYYY-MM-DD, got %r" % args.date)
            return 2
    try:
        with open(args.report, encoding="utf-8-sig") as f:
            text = f.read()
    except OSError as e:
        print("FAIL  cannot read %s: %s" % (args.report, e))
        return 2
    except UnicodeDecodeError:
        print("FAIL  %s is not UTF-8 text; save it as UTF-8 and check again" % args.report)
        return 2

    problems = []
    notes = []
    lines = text.splitlines()

    first = lines[0].strip() if lines else ""
    first_date = parse_date(first)
    if first_date is None:
        problems.append("the first line must be the analysis date written YYYY-MM-DD, found %r" % first[:40])
    elif first_date != expected:
        problems.append(
            "the first line says %s, but the analysis date is %s (from the system clock). "
            "Write the real date. If the analysis really was performed on another day, "
            "run the check again with --date set to that day." % (first, expected.isoformat()))

    m = re.match(r"(\d{4}-\d{2}-\d{2})", os.path.basename(args.report))
    if m and first_date is not None and m.group(1) != first:
        problems.append("the file name starts with %s but the first line says %s" % (m.group(1), first))

    headings = parse_headings(lines)
    if not args.no_sections:
        found = [normalize(h_text) for _, level, h_text in headings if level >= 2]
        for section in read_sections():
            wanted = normalize(section)
            if not any(h == wanted or h.startswith(wanted + " ") for h in found):
                problems.append('missing section heading "%s"' % section)

    for index, (line_no, level, h_text) in enumerate(headings):
        if level < 2:
            continue
        end = len(lines)
        for other_line, other_level, _ in headings[index + 1:]:
            if other_level <= level:
                end = other_line
                break
        if not any(line.strip() for line in lines[line_no + 1:end]):
            problems.append('section "%s" on line %d is empty. Fill it in, or write why it does not apply'
                            % (h_text, line_no + 1))

    for line_no, line in enumerate(lines, 1):
        for secret_name, secret_re in SECRET_RES:
            if secret_re.search(line):
                problems.append("line %d looks like a %s. Remove it and name the file and line where it "
                                "was found instead" % (line_no, secret_name))
                break

    folder = os.path.dirname(os.path.abspath(args.report))
    if os.path.basename(folder) != name or os.path.basename(os.path.dirname(folder)) != "analysis":
        notes.append("the report is not in analysis/%s/. That is fine only if the repository's "
                     "instructions say where reports go" % name)

    for problem in problems:
        print("FAIL  " + problem)
    for note in notes:
        print("NOTE  " + note)
    if problems:
        print("%d problem(s) in %s. Fix them and run the check again." % (len(problems), args.report))
        return 1
    print("OK    %s passed all checks" % args.report)
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Create and check analysis reports for this skill.")
    commands = parser.add_subparsers(dest="command")
    commands.required = True

    new = commands.add_parser("new", help="create a new report file")
    new.add_argument("topic", help="short description of what is analyzed; used for the title and file name")
    new.add_argument("--dir", help="folder to create the report in, instead of analysis/<skill-name>/")
    new.add_argument("--root", help="repository root, if it cannot be found from the working directory")
    new.add_argument("--bare", action="store_true", help="write only the date line")
    new.set_defaults(func=cmd_new)

    check = commands.add_parser("check", help="check a finished report")
    check.add_argument("report", help="path to the report file")
    check.add_argument("--date", help="the day the analysis was performed, YYYY-MM-DD (default: today)")
    check.add_argument("--no-sections", action="store_true", help="do not check required section headings")
    check.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
