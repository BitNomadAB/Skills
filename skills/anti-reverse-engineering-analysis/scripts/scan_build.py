#!/usr/bin/env python3
"""Search a built client for things that should not leave the servers.

  python <skill-folder>/scripts/scan_build.py <path> [<path> ...] [options]

Point it at what users actually receive: a web build folder (for example
dist/, build/, out/ or wwwroot/), a desktop, mobile or game build, a package
(APK, IPA, JAR, ZIP) or the files of a delivered device. Packages in the ZIP
format are opened and the files inside are scanned; .gz files are unpacked.
Binary files are searched for text in UTF-8 and UTF-16.

Hits come in three kinds:
  SECRET  credentials that must never be in a client: private keys, cloud,
          payment and AI provider keys, tokens with a privileged role,
          passwords inside URLs
  LEAK    things that should not ship: source maps, server-only and secret
          files, version-control folders, and any text you mark with --forbid
  REVIEW  things a person must judge: keys that are often public by design,
          hard-coded tokens, internal, test and local host names, private
          network addresses, staff and admin paths and code files, databases
          and other data files

Every hit is a candidate: open it and decide. A clean result covers only the
patterns listed by --list-rules, not everything a client gives away.
Secrets are never printed in full, only a short prefix and the length.

Options:
  --forbid TEXT          text that must not appear (case-insensitive);
                         repeatable
  --forbid-file FILE     one forbidden text per line; start a line with re:
                         for a regular expression; # starts a comment
  --allow "RULE [PATH]"  accept hits of RULE (rule id or glob) in files whose
                         path matches PATH (glob, default *); repeatable
  --allow-file FILE      one --allow value per line; # starts a comment
  --exclude GLOB         skip files and folders whose path or name matches
  --strict               fail on REVIEW hits too
  --json                 print the result as JSON
  --list-rules           print the rules and exit

Paths in globs are relative to the scanned folder and use forward slashes.
Files inside packages are shown as package!path/inside.

Exit codes: 0 no failing hits, 1 at least one SECRET or LEAK hit (or REVIEW
with --strict), 2 usage error. A build can therefore run it as a guard.
Needs Python 3.8 or later and only the standard library.
"""

import argparse
import base64
import bisect
import fnmatch
import gzip
import io
import json
import os
import re
import sys
import zipfile

SECRET, LEAK, REVIEW = "SECRET", "LEAK", "REVIEW"
KINDS = (SECRET, LEAK, REVIEW)

RULES = {
    "private-key": (SECRET, "Private key"),
    "aws-access-key": (SECRET, "AWS access key"),
    "stripe-secret-key": (SECRET, "Stripe secret or restricted key"),
    "webhook-signing-secret": (SECRET, "Webhook signing secret"),
    "github-token": (SECRET, "GitHub token"),
    "slack-token": (SECRET, "Slack token"),
    "ai-provider-key": (SECRET, "API key for an AI model provider"),
    "privileged-jwt": (SECRET, "Signed token (JWT) with a privileged role, for example a service key"),
    "credentials-in-url": (SECRET, "User name and password inside a URL"),
    "server-file": (LEAK, "Server-only or secret file, or version-control folder, in the build"),
    "source-map-file": (LEAK, "Source map: lets anyone restore the original source code"),
    "source-map-inline": (LEAK, "Source map embedded in a shipped file"),
    "forbidden": (LEAK, "Text you marked as forbidden"),
    "jwt": (REVIEW, "Hard-coded signed token (JWT); check that it is meant to be public and what its claims allow"),
    "google-api-key": (REVIEW, "Google API key; often public by design, check that it is restricted to your domains and APIs"),
    "secret-assignment": (REVIEW, "Long value assigned to a name like key, secret, token or password"),
    "source-map-ref": (REVIEW, "Reference to a source map; check whether the server serves that file"),
    "private-ip": (REVIEW, "Private network address"),
    "internal-host": (REVIEW, "URL with an internal host name"),
    "non-production-host": (REVIEW, "URL that points to a staging, test or development host"),
    "localhost-url": (REVIEW, "URL that points to the local machine"),
    "staff-path": (REVIEW, "Path or route for staff, admin, internal or debug features"),
    "staff-chunk": (REVIEW, "Code file named after staff, admin or internal features; anyone can download it"),
    "data-file": (REVIEW, "Database, data, log or deployment file; check that the client needs it"),
}

MAX_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_DEPTH = 3
MAX_STORED_LOCATIONS = 100
SHOWN_LOCATIONS = 3
SHOWN_ENTRIES = 20

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".bmp", ".tif", ".tiff", ".psd",
    ".mp3", ".mp4", ".m4a", ".m4v", ".webm", ".ogg", ".oga", ".wav", ".flac", ".mov", ".avi",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
}
ARCHIVE_EXTENSIONS = {
    ".zip", ".jar", ".war", ".ear", ".apk", ".aab", ".aar", ".ipa", ".xpi", ".nupkg", ".whl",
    ".vsix", ".appx", ".msix",
}
CODE_EXTENSIONS = {".js", ".mjs", ".cjs", ".wasm", ".dll"}
VCS_DIRS = {".git", ".svn", ".hg"}

LEAK_FILES = [
    ".env", ".env.*", "*.key", "*.pfx", "*.p12", "*.jks", "*.keystore", "*.kdbx", "*.ovpn",
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", ".htpasswd", ".netrc", ".pgpass", ".npmrc",
    ".pypirc", ".git-credentials", "*.tfstate", "*.tfstate.backup", "secrets.json",
    "credentials.json", "service-account*.json", "serviceaccount*.json", "*.bak", "*.orig",
    "*.swp", "*~",
]
DATA_FILES = [
    "*.sql", "*.sqlite", "*.sqlite3", "*.db", "*.mdb", "*.accdb", "*.log", "*.csv", "*.tsv",
    "*.xlsx", "*.parquet", "dockerfile", "docker-compose*.yml", "docker-compose*.yaml",
    "appsettings*.json", ".ds_store",
]

STAFF_WORDS = {
    "admin", "administrator", "staff", "internal", "backoffice", "back-office", "superuser",
    "sudo", "debug", "_debug", "moderator", "moderation",
}
STAFF_NAME_WORDS = ("admin", "staff", "backoffice", "back-office", "superuser", "impersonat",
                    "moderat", "internal")
INTERNAL_TLDS = {"internal", "local", "localdomain", "lan", "corp", "intranet", "intra"}
NON_PRODUCTION_WORDS = {
    "staging", "stage", "stg", "dev", "develop", "development", "test", "testing", "qa", "uat",
    "preprod", "sandbox",
}
PRIVILEGED_ROLES = {"service_role", "supabase_admin", "admin", "superuser", "root"}
PLACEHOLDER_PASSWORDS = {
    "password", "pass", "passwd", "pwd", "secret", "user", "username", "xxx", "xxxx", "***",
    "****", "changeme",
}


def redact(value, keep=4):
    return "%s...(%d chars)" % (value[:keep], len(value))


def ext_of(name):
    return os.path.splitext(name.lower())[1]


def is_private_ip(host):
    parts = host.split(".")
    if len(parts) != 4 or not all(p.isdigit() and int(p) <= 255 for p in parts):
        return False
    a, b = int(parts[0]), int(parts[1])
    return a == 10 or (a == 192 and b == 168) or (a == 172 and 16 <= b <= 31)


def jwt_claims(token):
    try:
        payload = token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (ValueError, IndexError):
        return None
    return claims if isinstance(claims, dict) else None


class ContentRule:
    """A regular expression plus a handler that turns each match into hits.

    hint is a cheap pre-check: a tuple of lower-case substrings, one of which
    must occur in the lower-cased text before the full expression is run.
    re.ASCII keeps word boundaries working in binary files, where the
    character before a string decoded as UTF-16 is often a non-ASCII letter.
    """

    def __init__(self, pattern, handler, hint=None, flags=re.ASCII):
        self.regex = re.compile(pattern, flags)
        self.handler = handler
        self.hint = hint

    def applies(self, lower_text):
        return self.hint is None or any(h in lower_text for h in self.hint)


def simple(rule_id, keep=4):
    def handler(m):
        yield rule_id, redact(m.group(0), keep), m.group(0)
    return handler


def on_private_key(m):
    yield "private-key", m.group(0), m.group(0)


def on_jwt(m):
    token = m.group(0)
    claims = jwt_claims(token)
    if claims is None:
        return
    role = claims.get("role")
    role_text = ", role=%s" % role[:40] if isinstance(role, str) else ""
    if isinstance(role, str) and role.lower() in PRIVILEGED_ROLES:
        yield "privileged-jwt", "eyJ...(%d chars)%s" % (len(token), role_text), token
    else:
        names = ", ".join(sorted(str(k)[:30] for k in claims)[:10]) or "none"
        yield "jwt", "eyJ...(%d chars), claims: %s%s" % (len(token), names, role_text), token


def on_credentials_url(m):
    scheme, _, password, host = m.groups()
    if password.lower() in PLACEHOLDER_PASSWORDS or "${" in password or password[:1] in "{%$":
        return
    yield "credentials-in-url", "%s://***:***@%s" % (scheme, host or "?"), m.group(0)


def on_url(m):
    url = m.group(0)
    host = m.group(1).lower().rstrip(".")
    if host in ("localhost", "0.0.0.0", "[::1]") or host.endswith(".localhost") or host.startswith("127."):
        yield "localhost-url", url, url.lower()
        return
    labels = host.split(".")
    if len(labels) < 2 or is_private_ip(host):
        return  # private addresses are reported by the address rule
    if labels[-1] in INTERNAL_TLDS or host.endswith(".home.arpa"):
        yield "internal-host", url, url.lower()
        return
    words = []
    for label in labels[:-2]:
        words.extend(label.split("-"))
    words.extend(labels[-2].split("-")[1:])
    if any(word in NON_PRODUCTION_WORDS for word in words):
        yield "non-production-host", url, url.lower()


def on_ipv4(m):
    if is_private_ip(m.group(0)):
        yield "private-ip", m.group(0), m.group(0)


def on_source_map(m):
    if m.group(1).startswith("data:"):
        yield "source-map-inline", "sourceMappingURL=data:...", "inline"
    else:
        yield "source-map-ref", "sourceMappingURL=<file>", "reference"


def on_path(m):
    path = m.group(1)
    for segment in path.lower().split("/"):
        if segment in STAFF_WORDS or segment.startswith("impersonat"):
            yield "staff-path", '"%s"' % path, path.lower()
            return


SPECIFIC_SECRETS = [
    (r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b", "aws-access-key", ("akia", "asia")),
    (r"\b[rs]k_(?:live|test)_[0-9A-Za-z]{10,}", "stripe-secret-key", ("k_live_", "k_test_")),
    (r"\bwhsec_[0-9A-Za-z]{10,}", "webhook-signing-secret", ("whsec_",)),
    (r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{22,})", "github-token",
     ("ghp_", "gho_", "ghu_", "ghs_", "ghr_", "github_pat_")),
    (r"\bxox[abposr]-[A-Za-z0-9-]{10,}", "slack-token", ("xox",)),
    (r"\bsk-(?:ant-|proj-|svcacct-)[A-Za-z0-9_-]{20,}|\bsk-[A-Za-z0-9]{40,}\b", "ai-provider-key", ("sk-",)),
    (r"\bAIza[0-9A-Za-z_-]{35}", "google-api-key", ("aiza",)),
]
PRIVATE_KEY = r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"
JWT = r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
KNOWN_SECRET_RES = [re.compile(p) for p, _, _ in SPECIFIC_SECRETS] + [re.compile(PRIVATE_KEY), re.compile(JWT)]


def on_assignment(m):
    name, value = m.group(1), m.group(2)
    if not (re.search(r"[0-9]", value) and re.search(r"[A-Za-z]", value)):
        return
    if "://" in value or value[:1] in "/.{$":
        return
    if any(r.search(value) for r in KNOWN_SECRET_RES):
        return  # reported by the more specific rule
    yield "secret-assignment", "%s = %s" % (name, redact(value)), value


def build_content_rules(forbidden):
    rules = [ContentRule(p, simple(rule_id), hint) for p, rule_id, hint in SPECIFIC_SECRETS]
    rules += [
        ContentRule(PRIVATE_KEY, on_private_key, ("private key",)),
        ContentRule(JWT, on_jwt, ("eyj",)),
        ContentRule(r"\b([a-z][a-z0-9+.-]{1,20})://([^\s/:@\"'`<>]{1,64}):([^\s/@\"'`<>]{1,128})@([A-Za-z0-9.-]*)",
                    on_credentials_url, ("@",)),
        ContentRule(r"\b(?:https?|wss?)://(\[[0-9A-Fa-f:]+\]|[A-Za-z0-9.-]+)(?::\d{1,5})?", on_url, ("://",)),
        ContentRule(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", on_ipv4, ("10.", "192.168.", "172.")),
        ContentRule(r"[#@]\s*sourceMappingURL=(\S{0,200})", on_source_map, ("sourcemappingurl",)),
        ContentRule(r"(?i:((?:api_?key|secret|passw(?:or)?d|access_?token|auth_?token|private_?key)[\w$]*))"
                    r"[\"']?\s*[:=]\s*[\"'`]([^\"'`\s]{16,200})[\"'`]",
                    on_assignment,
                    ("api_key", "apikey", "secret", "passw", "access_token", "accesstoken", "auth_token",
                     "authtoken", "private_key", "privatekey")),
    ]
    staff_hint = ("admin", "staff", "internal", "backoffice", "back-office", "superuser", "sudo", "debug",
                  "impersonat", "moderat")
    path_chars = r"[A-Za-z0-9_\-./{}$:]{1,150}"
    rules += [
        ContentRule(r"[\"'`](/" + path_chars + r")(?=[\"'`?#])", on_path, staff_hint),
        ContentRule(r"\bpath\s*:\s*[\"'`](" + path_chars + r")[\"'`]", on_path, staff_hint),
    ]
    for spec in forbidden:
        if spec.startswith("re:"):
            pattern, flags = spec[3:], 0
        else:
            pattern, flags = re.escape(spec), re.IGNORECASE

        def on_forbidden(m, spec=spec):
            text = m.group(0)
            yield "forbidden", '"%s"' % text[:80], (spec, text.lower())

        rules.append(ContentRule(pattern, on_forbidden, None, flags))
    return rules


def glob_match(path, pattern):
    return fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(path.rsplit("/", 1)[-1], pattern)


class Scanner:
    def __init__(self, content_rules, allows, excludes):
        self.rules = content_rules
        self.allows = allows
        self.excludes = excludes
        self.hits = {}
        self.notes = []
        self.files = 0
        self.bytes = 0

    def excluded(self, rel):
        return any(glob_match(rel, pattern) for pattern in self.excludes)

    def add(self, rule_id, display, key, rel, shown, location=None):
        for rule_glob, path_glob in self.allows:
            if fnmatch.fnmatchcase(rule_id, rule_glob) and (glob_match(rel, path_glob) or glob_match(shown, path_glob)):
                return
        hit = self.hits.get((rule_id, key))
        if hit is None:
            kind, description = RULES[rule_id]
            hit = self.hits[(rule_id, key)] = {
                "rule": rule_id, "kind": kind, "description": description,
                "display": display, "count": 0, "locations": [],
            }
        hit["count"] += 1
        if location and len(hit["locations"]) < MAX_STORED_LOCATIONS:
            hit["locations"].append(location)

    def check_name(self, name, rel, shown):
        lower = name.lower()
        if any(fnmatch.fnmatchcase(lower, p) for p in LEAK_FILES):
            self.add("server-file", shown, rel, rel, shown)
        elif any(fnmatch.fnmatchcase(lower, p) for p in DATA_FILES):
            self.add("data-file", shown, rel, rel, shown)
        stem, ext = os.path.splitext(lower)
        if ext in CODE_EXTENSIONS and any(word in stem for word in STAFF_NAME_WORDS):
            self.add("staff-chunk", shown, rel, rel, shown)

    def scan_root(self, given):
        shown_root = given.replace("\\", "/").rstrip("/")
        if os.path.isfile(given):
            self.scan_path(given, os.path.basename(given), shown_root)
            return
        for dirpath, dirnames, filenames in os.walk(given):
            rel_dir = os.path.relpath(dirpath, given).replace(os.sep, "/")
            rel_dir = "" if rel_dir == "." else rel_dir + "/"
            keep = []
            for d in sorted(dirnames):
                rel = rel_dir + d
                if self.excluded(rel):
                    continue
                if d.lower() in VCS_DIRS:
                    shown = "%s/%s/" % (shown_root, rel)
                    self.add("server-file", shown, rel, rel, shown)
                    continue
                keep.append(d)
            dirnames[:] = keep
            for f in sorted(filenames):
                rel = rel_dir + f
                if not self.excluded(rel):
                    self.scan_path(os.path.join(dirpath, f), rel, "%s/%s" % (shown_root, rel))

    def scan_path(self, disk_path, rel, shown):
        name = os.path.basename(disk_path)
        self.check_name(name, rel, shown)
        ext = ext_of(name)
        if ext in SKIP_EXTENSIONS:
            return
        if ext in (".gz", ".br") and os.path.exists(disk_path[:-len(ext)]):
            return  # the uncompressed copy next to it is scanned instead
        if ext == ".br":
            self.notes.append("%s: Brotli-compressed and not scanned; unpack it and scan the result" % shown)
            return
        try:
            if os.path.getsize(disk_path) > MAX_BYTES:
                self.notes.append("%s: larger than %d MB and not scanned" % (shown, MAX_BYTES // 2 ** 20))
                return
            with open(disk_path, "rb") as f:
                data = f.read()
        except OSError as e:
            self.notes.append("%s: could not be read (%s)" % (shown, e))
            return
        self.scan_blob(data, name, rel, shown, 0)

    def scan_blob(self, data, name, rel, shown, depth):
        self.files += 1
        self.bytes += len(data)
        if ext_of(name) == ".gz":
            try:
                with gzip.GzipFile(fileobj=io.BytesIO(data)) as g:
                    data = g.read(MAX_BYTES + 1)
            except (OSError, EOFError) as e:
                self.notes.append("%s: could not be unpacked (%s)" % (shown, e))
                return
            if len(data) > MAX_BYTES:
                self.notes.append("%s: unpacks to more than %d MB and was not scanned" % (shown, MAX_BYTES // 2 ** 20))
                return
            name = name[:-3]
            self.check_name(name, rel, shown)
        if (ext_of(name) in ARCHIVE_EXTENSIONS or data[:4] == b"PK\x03\x04") and depth < MAX_ARCHIVE_DEPTH:
            if self.scan_archive(data, rel, shown, depth):
                return
        self.scan_content(data, name, rel, shown)

    def scan_archive(self, data, rel, shown, depth):
        try:
            archive = zipfile.ZipFile(io.BytesIO(data))
            members = archive.infolist()
        except (zipfile.BadZipFile, OSError, ValueError):
            return False
        for info in members:
            if info.is_dir():
                continue
            member_rel = "%s!%s" % (rel, info.filename)
            member_shown = "%s!%s" % (shown, info.filename)
            if self.excluded(member_rel):
                continue
            parts = info.filename.split("/")
            vcs = [i for i, part in enumerate(parts[:-1]) if part.lower() in VCS_DIRS]
            if vcs:
                folder = "/".join(parts[:vcs[0] + 1]) + "/"
                self.add("server-file", "%s!%s" % (shown, folder), "%s!%s" % (rel, folder), member_rel, member_shown)
                continue
            name = parts[-1]
            self.check_name(name, member_rel, member_shown)
            if ext_of(name) in SKIP_EXTENSIONS:
                continue
            if info.file_size > MAX_BYTES:
                self.notes.append("%s: larger than %d MB and not scanned" % (member_shown, MAX_BYTES // 2 ** 20))
                continue
            try:
                member = archive.read(info)
            except Exception as e:  # encrypted, unsupported compression or damaged entry
                self.notes.append("%s: could not be read (%s)" % (member_shown, e))
                continue
            self.scan_blob(member, name, member_rel, member_shown, depth + 1)
        return True

    def scan_content(self, data, name, rel, shown):
        binary = b"\0" in data[:8192]
        if binary:
            even = len(data) - len(data) % 2
            odd = len(data) - 1 - (len(data) - 1) % 2
            views = [
                (data.decode("latin-1"), 1, 0),
                (data[:even].decode("utf-16-le", "surrogatepass"), 2, 0),
                (data[1:1 + odd].decode("utf-16-le", "surrogatepass"), 2, 1),
            ]
        else:
            text = data.decode("utf-8", "replace")
            views = [(text, 1, 0)]
            if ext_of(name) == ".map" and '"mappings"' in text and '"sources"' in text:
                display = shown
                if '"sourcesContent"' in text:
                    display += "  (includes the original source code)"
                self.add("source-map-file", display, rel, rel, shown)

        for text, unit, shift in views:
            lower_text = text.lower()
            newlines = None
            for rule in self.rules:
                if not rule.applies(lower_text):
                    continue
                for m in rule.regex.finditer(text):
                    for rule_id, display, key in rule.handler(m):
                        if binary:
                            location = "%s@%d" % (shown, m.start() * unit + shift)
                        else:
                            if newlines is None:
                                newlines = [n.start() for n in re.finditer("\n", text)]
                            before = bisect.bisect_left(newlines, m.start())
                            column = m.start() - (newlines[before - 1] if before else -1)
                            location = "%s:%d:%d" % (shown, before + 1, column)
                        self.add(rule_id, display, key, rel, shown, location)


def read_list_file(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = [line.rstrip("\r\n") for line in f]
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def parse_allow(spec):
    parts = spec.split(None, 1)
    return parts[0], (parts[1].strip() if len(parts) > 1 else "*")


def human_size(n):
    for unit in ("bytes", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d %s" % (n, unit)) if unit == "bytes" else ("%.1f %s" % (n, unit))
        n /= 1024.0


def summarize(hits):
    return {kind: sum(1 for h in hits if h["kind"] == kind) for kind in KINDS}


def print_text(scanner, roots, counts):
    print("Scanned %d files (%s) in %s" % (scanner.files, human_size(scanner.bytes), ", ".join(roots)))
    by_rule = {}
    for hit in scanner.hits.values():
        by_rule.setdefault(hit["rule"], []).append(hit)
    for kind in KINDS:
        for rule_id in sorted(r for r in by_rule if RULES[r][0] == kind):
            hits = sorted(by_rule[rule_id], key=lambda h: (-h["count"], h["display"]))
            print()
            print("%s  %s: %s" % (kind, rule_id, RULES[rule_id][1]))
            for hit in hits[:SHOWN_ENTRIES]:
                line = "    " + hit["display"]
                if hit["locations"]:
                    line += "  %dx  %s" % (hit["count"], ", ".join(hit["locations"][:SHOWN_LOCATIONS]))
                    if hit["count"] > SHOWN_LOCATIONS:
                        line += " (+%d more)" % (hit["count"] - SHOWN_LOCATIONS)
                print(line)
            if len(hits) > SHOWN_ENTRIES:
                print("    (+%d more; use --json to see all)" % (len(hits) - SHOWN_ENTRIES))
    if scanner.notes:
        print()
        print("Notes:")
        for note in scanner.notes:
            print("  - " + note)
    print()
    print("Result: %d SECRET, %d LEAK, %d REVIEW." % (counts[SECRET], counts[LEAK], counts[REVIEW]))
    print("Every hit is a candidate: open it and decide. A clean result covers only the rules in --list-rules.")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(
        description="Search a built client for things that should not leave the servers.")
    parser.add_argument("paths", nargs="*", help="build folders, packages or files to scan")
    parser.add_argument("--forbid", action="append", default=[], metavar="TEXT")
    parser.add_argument("--forbid-file", action="append", default=[], metavar="FILE")
    parser.add_argument("--allow", action="append", default=[], metavar='"RULE [PATH]"')
    parser.add_argument("--allow-file", action="append", default=[], metavar="FILE")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    parser.add_argument("--strict", action="store_true", help="fail on REVIEW hits too")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    parser.add_argument("--list-rules", action="store_true", help="print the rules and exit")
    args = parser.parse_args(argv)

    if args.list_rules:
        for kind in KINDS:
            for rule_id in sorted(r for r in RULES if RULES[r][0] == kind):
                print("%-7s %-23s %s" % (kind, rule_id, RULES[rule_id][1]))
        return 0
    if not args.paths:
        parser.error("give at least one build folder, package or file to scan")
    missing = [p for p in args.paths if not os.path.exists(p)]
    if missing:
        parser.error("not found: " + ", ".join(missing))

    try:
        forbidden = list(args.forbid)
        for path in args.forbid_file:
            forbidden += read_list_file(path)
        allows = [parse_allow(spec) for spec in args.allow]
        for path in args.allow_file:
            allows += [parse_allow(spec) for spec in read_list_file(path)]
    except OSError as e:
        parser.error(str(e))
    try:
        rules = build_content_rules(forbidden)
    except re.error as e:
        parser.error("invalid regular expression in forbidden list: %s" % e)

    scanner = Scanner(rules, allows, args.exclude)
    for path in args.paths:
        scanner.scan_root(path)

    hits = list(scanner.hits.values())
    counts = summarize(hits)
    failing = counts[SECRET] + counts[LEAK] + (counts[REVIEW] if args.strict else 0)
    if args.json:
        order = {kind: i for i, kind in enumerate(KINDS)}
        hits.sort(key=lambda h: (order[h["kind"]], h["rule"], -h["count"], h["display"]))
        json.dump({"files": scanner.files, "bytes": scanner.bytes, "summary": counts,
                   "failed": failing > 0, "hits": hits, "notes": scanner.notes},
                  sys.stdout, indent=2)
        print()
    else:
        print_text(scanner, [p.replace("\\", "/") for p in args.paths], counts)
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
