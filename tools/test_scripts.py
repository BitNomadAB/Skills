#!/usr/bin/env python3
"""Tests for the helper scripts in the skills.

  python tools/test_scripts.py

Fake credentials are assembled at run time so that this file never contains
anything a secret scanner would flag.
"""

import base64
import datetime
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(REPO, "skills", "fmea", "scripts", "report.py")
SUMMARY_REPORT = os.path.join(REPO, "skills", "analysis-summary", "scripts", "report.py")
SCAN = os.path.join(REPO, "skills", "anti-reverse-engineering-analysis", "scripts", "scan_build.py")
TODAY = datetime.date.today().isoformat()

AWS_KEY = "AKIA" + "IOSFODNN7" + "EXAMPLE"
STRIPE_KEY = "sk_" + "live_" + "a1B2c3D4e5F6g7H8i9J0k1L2"
GOOGLE_KEY = "AIza" + "SyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q"


def run(script, args, cwd):
    result = subprocess.run([sys.executable, script] + args, cwd=cwd, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout + result.stderr


def make_jwt(claims):
    def part(obj):
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip("=")
    return "%s.%s.%s" % (part({"alg": "HS256", "typ": "JWT"}), part(claims), "c2lnbmF0dXJlLXZhbHVlLXg")


def write(path, content, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if mode == "w":
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
    else:
        with open(path, "wb") as f:
            f.write(content)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        os.makedirs(os.path.join(self.repo, ".git"))
        os.makedirs(os.path.join(self.repo, "src", "deep"))

    def tearDown(self):
        self.tmp.cleanup()

    def new(self, topic, *extra):
        code, out = run(REPORT, ["new", topic] + list(extra), os.path.join(self.repo, "src", "deep"))
        self.assertEqual(code, 0, out)
        return os.path.join(self.repo, "src", "deep", out.strip())

    def check(self, path, *extra):
        return run(REPORT, ["check", path] + list(extra), self.repo)

    def fill(self, path):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        filled = []
        for line in lines:
            filled.append(line)
            if line.startswith("## "):
                filled += ["", "Content."]
        write(path, "\n".join(filled) + "\n")

    def test_new_creates_dated_skeleton_at_repo_root(self):
        path = self.new("Payment flow – Ärende 42")
        expected_dir = os.path.join(self.repo, "analysis", "fmea")
        self.assertEqual(os.path.dirname(os.path.abspath(path)), expected_dir)
        self.assertEqual(os.path.basename(path), "%s-payment-flow-arende-42.md" % TODAY)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertTrue(text.startswith(TODAY + "\n"))
        self.assertIn("# FMEA: Payment flow", text)
        self.assertIn("## Scope and method", text)
        self.assertIn("## Assumptions and open questions", text)

    def test_new_never_overwrites(self):
        first = self.new("Same topic")
        second = self.new("Same topic")
        self.assertNotEqual(first, second)
        self.assertTrue(second.endswith("-same-topic-2.md"))

    def test_bare_and_dir(self):
        path = self.new("x", "--bare", "--dir", os.path.join(self.repo, "docs", "reviews"))
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), TODAY + "\n")
        self.assertIn(os.path.join("docs", "reviews"), path)

    def test_relative_dir_starts_at_repo_root(self):
        path = self.new("x", "--dir", "docs/reviews")
        self.assertEqual(os.path.dirname(os.path.abspath(path)), os.path.join(self.repo, "docs", "reviews"))
        code, out = self.check(path)
        self.assertIn("NOTE  the report is not in analysis/fmea/", out)

    def test_folder_setting_and_title(self):
        cwd = os.path.join(self.repo, "src")
        code, out = run(SUMMARY_REPORT, ["new", "summary", "--title", "Shop"], cwd)
        self.assertEqual(code, 0, out)
        path = os.path.join(cwd, out.strip())
        self.assertEqual(os.path.basename(path), "%s-summary.md" % TODAY)
        self.assertEqual(os.path.dirname(os.path.abspath(path)), os.path.join(self.repo, "analysis", "summary"))
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("# Analysis summary: Shop", text)
        self.assertIn("## Most critical", text)
        code, out = run(SUMMARY_REPORT, ["new", "workloop fmea", "--bare"], cwd)
        self.assertEqual(code, 0, out)
        self.assertTrue(out.strip().endswith("%s-workloop-fmea.md" % TODAY), out)
        code, out = run(SUMMARY_REPORT, ["check", path], self.repo)
        self.assertNotIn("NOTE", out)

    def test_empty_skeleton_fails_and_filled_report_passes(self):
        path = self.new("Checkout")
        code, out = self.check(path)
        self.assertEqual(code, 1)
        self.assertIn("is empty", out)
        self.fill(path)
        code, out = self.check(path)
        self.assertEqual(code, 0, out)

    def test_wrong_date_fails(self):
        path = self.new("Checkout")
        self.fill(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        write(path, text.replace(TODAY, "2024-05-12", 1))
        code, out = self.check(path)
        self.assertEqual(code, 1)
        self.assertIn("first line says 2024-05-12", out)
        self.assertIn("file name starts with", out)

    def test_missing_section_and_no_sections_flag(self):
        path = self.new("Checkout")
        self.fill(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        write(path, text.replace("## Priorities", "## Something else"))
        code, out = self.check(path)
        self.assertEqual(code, 1)
        self.assertIn('missing section heading "Priorities"', out)
        code, out = self.check(path, "--no-sections")
        self.assertEqual(code, 0, out)

    def test_secret_fails_without_printing_it(self):
        path = self.new("Checkout")
        self.fill(path)
        with open(path, "a", encoding="utf-8") as f:
            f.write("Key found: %s\n" % STRIPE_KEY)
        code, out = self.check(path)
        self.assertEqual(code, 1)
        self.assertIn("Stripe secret key", out)
        self.assertNotIn(STRIPE_KEY, out)

    def test_byte_order_mark_and_numbered_headings(self):
        path = self.new("Checkout")
        self.fill(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        text = text.replace("## Scope and method", "## 1. Scope and method")
        with open(path, "w", encoding="utf-8-sig") as f:
            f.write(text)
        code, out = self.check(path)
        self.assertEqual(code, 0, out)


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dist = os.path.join(self.tmp.name, "dist")
        os.makedirs(self.dist)

    def tearDown(self):
        self.tmp.cleanup()

    def scan(self, *extra):
        code, out = run(SCAN, ["dist", "--json"] + list(extra), self.tmp.name)
        data = json.loads(out[out.index("{"):]) if "{" in out else None
        return code, data, out

    def rules(self, data):
        return {hit["rule"] for hit in data["hits"]}

    def test_clean_build_passes(self):
        write(os.path.join(self.dist, "index.js"),
              'fetch("/api/events");const u="https://api.example.com/v1";console.log("ok");')
        code, data, out = self.scan()
        self.assertEqual(code, 0, out)
        self.assertEqual(data["hits"], [])

    def test_finds_planted_problems(self):
        anon = make_jwt({"role": "anon", "iss": "supabase"})
        service = make_jwt({"role": "service_role", "iss": "supabase"})
        js = "\n".join([
            'const a="%s";' % AWS_KEY,
            'const cfg={apiKey:"%s"};' % GOOGLE_KEY,
            'const anon="%s",svc="%s";' % (anon, service),
            'const db="postgres://app:Sup3rS3cret@db.example.com:5432/app";',
            'const s={clientSecret:"9f8e7d6c5b4a3f2e1d0c"};',
            'route({path:"admin/users"});fetch("/api/internal/stats");',
            'const api="https://api.staging.example.com",dev="http://10.0.0.12:8080",lo="http://localhost:3000";',
            'const nas="http://nas.local/share";',
            "// Project Falcon launch",
            "//# sourceMappingURL=index.js.map",
        ])
        write(os.path.join(self.dist, "assets", "index.js"), js)
        write(os.path.join(self.dist, "assets", "index.js.map"),
              '{"version":3,"sources":["a.ts"],"sourcesContent":["x"],"mappings":"AAAA"}')
        write(os.path.join(self.dist, ".env"), "X=1")
        write(os.path.join(self.dist, "assets", "AdminPanel-3f2a.js"), "export default 1;")

        # A .NET user-string entry: length byte, UTF-16 text, terminal byte.
        dex = b"\0\0\0" + bytes([2 * len(STRIPE_KEY) + 1]) + STRIPE_KEY.encode("utf-16-le") + b"\0"
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("classes.dex", dex)
            z.writestr("assets/.git/config", "[core]")
        write(os.path.join(self.dist, "app.apk"), buffer.getvalue(), mode="wb")

        code, data, out = self.scan("--forbid", "project falcon")
        self.assertEqual(code, 1, out)
        found = self.rules(data)
        for rule in ["aws-access-key", "google-api-key", "jwt", "privileged-jwt", "credentials-in-url",
                     "secret-assignment", "staff-path", "non-production-host", "private-ip",
                     "localhost-url", "internal-host", "source-map-ref", "source-map-file",
                     "server-file", "staff-chunk", "stripe-secret-key", "forbidden"]:
            self.assertIn(rule, found, out)
        for secret in (AWS_KEY, STRIPE_KEY, GOOGLE_KEY, service, "Sup3rS3cret", "9f8e7d6c5b4a3f2e1d0c"):
            self.assertNotIn(secret, out)
        stripe = [h for h in data["hits"] if h["rule"] == "stripe-secret-key"][0]
        self.assertTrue(stripe["locations"][0].startswith("dist/app.apk!classes.dex@"), stripe)
        paths = [h["display"] for h in data["hits"] if h["rule"] == "server-file"]
        self.assertIn("dist/app.apk!assets/.git/", paths)
        self.assertIn("dist/.env", paths)

        code, text_out = run(SCAN, ["dist"], self.tmp.name)
        self.assertEqual(code, 1)
        self.assertIn("SECRET  aws-access-key", text_out)
        self.assertNotIn(AWS_KEY, text_out)

    def test_allow_exclude_and_strict(self):
        write(os.path.join(self.dist, "index.js"), 'fetch("/api/admin/users");const k="%s";' % AWS_KEY)
        write(os.path.join(self.dist, "vendor", "lib.js"), 'const k="%s";' % AWS_KEY)
        code, data, out = self.scan("--allow", "aws-access-key index.js", "--exclude", "vendor")
        self.assertEqual(code, 0, out)
        self.assertEqual(self.rules(data), {"staff-path"})
        code, data, out = self.scan("--allow", "aws-access-key", "--strict")
        self.assertEqual(code, 1, out)

    def test_list_rules_and_usage_errors(self):
        code, out = run(SCAN, ["--list-rules"], self.tmp.name)
        self.assertEqual(code, 0)
        self.assertIn("staff-path", out)
        code, out = run(SCAN, [os.path.join(self.tmp.name, "missing")], self.tmp.name)
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
