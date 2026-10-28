#!/usr/bin/env python3
"""Verification script for the Low-Energy & ADHD-Friendly Daily Routine Guide.

Checks HTML validity, internal links, license/credit lines, and that no
secrets or .github/workflows are present. Exits non-zero on any failure.
"""
from html.parser import HTMLParser
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"ok: {msg}")


class HtmlChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(
                f"unexpected close </{tag}>; stack tail: {self.stack[-5:]}"
            )

    def report(self, path):
        for e in self.errors:
            fail(f"{path}: {e}")
        if self.stack:
            fail(f"{path}: unclosed tags: {self.stack}")
        if not self.errors and not self.stack:
            ok(f"{path}: valid HTML structure")


def check_html():
    for name in ("index.html", "cards.html"):
        path = os.path.join(SITE, name)
        checker = HtmlChecker()
        with open(path, encoding="utf-8") as fh:
            checker.feed(fh.read())
        checker.report(path)


def check_links():
    for name in ("index.html", "cards.html"):
        path = os.path.join(SITE, name)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        links = re.findall(r'href="([^"]+)"', html)
        for link in links:
            if link.startswith("#"):
                target = link[1:]
                if re.search(r'id="%s"' % re.escape(target), html) or \
                   re.search(r'\bname="%s"' % re.escape(target), html):
                    ok(f"{name} anchor {link}")
                else:
                    fail(f"{name}: anchor {link} not found")
            else:
                candidate = os.path.join(SITE, link.lstrip("/"))
                if not os.path.exists(candidate):
                    # allow relative ../LICENSE from site/
                    candidate2 = os.path.normpath(os.path.join(SITE, link))
                    if not os.path.exists(candidate2):
                        fail(f"{name}: link {link} -> {candidate} not found")
                    else:
                        ok(f"{name}: link {link}")
                else:
                    ok(f"{name}: link {link}")


def check_license():
    path = os.path.join(ROOT, "LICENSE")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    expected = "Copyright (c) 2026 Asdale Dynamics, LLC"
    if expected in content:
        ok("LICENSE contains exact copyright line")
    else:
        fail("LICENSE missing exact copyright line")


def check_readme_credit():
    path = os.path.join(ROOT, "README.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if "Asdale Dynamics, LLC" in content:
        ok("README credits Asdale Dynamics, LLC")
    else:
        fail("README does not credit Asdale Dynamics, LLC")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" in content:
        ok("README contains copyright line")
    else:
        fail("README missing copyright line")


def check_no_workflows():
    path = os.path.join(ROOT, ".github", "workflows")
    if os.path.exists(path):
        fail(".github/workflows exists (should not)")
    else:
        ok("no .github/workflows directory")


def check_no_secrets():
    patterns = [
        (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style API key"),
        (r"AKIA[0-9A-Z]{16}", "AWS access key"),
        (r"ghp_[A-Za-z0-9]{36,}", "GitHub personal access token"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key block"),
    ]
    for root, _dirs, files in os.walk(ROOT):
        if ".git" in root:
            continue
        for fname in files:
            if fname == "verify.py":
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8") as fh:
                    content = fh.read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for pat, label in patterns:
                if re.search(pat, content):
                    fail(f"{fpath}: possible {label} found")


def main():
    print("== Verifying Low-Energy Routine Guide ==")
    check_html()
    check_links()
    check_license()
    check_readme_credit()
    check_no_workflows()
    check_no_secrets()
    print()
    if FAILURES:
        print(f"VERIFICATION FAILED: {len(FAILURES)} issue(s)")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    print("VERIFICATION PASSED: all checks ok")


if __name__ == "__main__":
    main()
