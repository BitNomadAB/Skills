#!/usr/bin/env python3
"""Check the skills in this repository before committing.

  python tools/check_skills.py         report problems
  python tools/check_skills.py --fix   also copy the template report.py to every skill

Checks:
- every skill's scripts/report.py is identical to templates/skill/scripts/report.py;
- a skill with report.py has scripts/report-sections.txt, and every heading in it
  is mentioned in the skill's SKILL.md;
- every Python script under skills/ and templates/ compiles.

Exit codes: 0 OK, 1 problems found.
"""

import argparse
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_REPORT = os.path.join(REPO, "templates", "skill", "scripts", "report.py")


def read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read().replace("\r\n", "\n")


def normalize(text):
    return " ".join(re.sub(r"[\W_]+", " ", text.lower()).split())


def section_lines(path):
    return [line.strip() for line in read(path).splitlines()
            if line.strip() and not line.strip().startswith("#")]


def main():
    parser = argparse.ArgumentParser(description="Check the skills in this repository.")
    parser.add_argument("--fix", action="store_true", help="copy the template report.py to every skill")
    args = parser.parse_args()

    problems = []
    template = read(TEMPLATE_REPORT)
    skills_dir = os.path.join(REPO, "skills")
    for skill in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, skill)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        report = os.path.join(skill_dir, "scripts", "report.py")
        sections = os.path.join(skill_dir, "scripts", "report-sections.txt")
        if not os.path.isfile(report):
            print("NOTE  %s has no scripts/report.py" % skill)
            continue
        if read(report) != template:
            if args.fix:
                shutil.copyfile(TEMPLATE_REPORT, report)
                print("FIXED %s/scripts/report.py copied from the template" % skill)
            else:
                problems.append("%s/scripts/report.py differs from the template; run with --fix" % skill)
        if not os.path.isfile(sections):
            problems.append("%s has report.py but no scripts/report-sections.txt" % skill)
            continue
        skill_text = normalize(read(skill_md))
        for section in section_lines(sections):
            if normalize(section) not in skill_text:
                problems.append('%s: section "%s" in report-sections.txt is not mentioned in SKILL.md'
                                % (skill, section))

    for base in ("skills", "templates"):
        for dirpath, _, filenames in os.walk(os.path.join(REPO, base)):
            for name in filenames:
                if name.endswith(".py"):
                    path = os.path.join(dirpath, name)
                    try:
                        compile(read(path), path, "exec")
                    except SyntaxError as e:
                        problems.append("%s does not compile: line %s: %s"
                                        % (os.path.relpath(path, REPO), e.lineno, e.msg))

    for problem in problems:
        print("FAIL  " + problem)
    if problems:
        return 1
    print("OK    all skills passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
