#!/usr/bin/env python3
"""Audit and safely fix static HTML/CSS/JS websites.

The script is dependency-free by design. It focuses on checks and fixes that
are useful for static front-end sites without paid builders, paid plugins, or
backend application code.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import html
import json
import mimetypes
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse


TEXT_EXTENSIONS = {
    ".html",
    ".htm",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".xml",
    ".txt",
    ".svg",
    ".webmanifest",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"}
SCRIPT_EXTENSIONS = {".js", ".mjs"}
STYLE_EXTENSIONS = {".css"}
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".cache",
    ".parcel-cache",
    ".next",
    ".nuxt",
    "dist-cache",
    ".site-quality-backups",
    "partials",
}

EXCLUDED_FILES = {
    "README.md",
    "quality-report.json",
    "quality-report.md",
}

RISKY_PUBLIC_PATTERNS = [
    ".env",
    ".env.local",
    ".env.production",
    ".DS_Store",
    "Thumbs.db",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
]

RISKY_SUFFIXES = {
    ".bak",
    ".backup",
    ".old",
    ".orig",
    ".log",
    ".sql",
    ".sqlite",
    ".db",
    ".pem",
    ".key",
    ".p12",
    ".crt",
    ".csr",
    ".map",
}

TRACKING_HINTS = {
    "google-analytics.com": "Google Analytics",
    "googletagmanager.com": "Google Tag Manager",
    "facebook.net": "Meta Pixel",
    "connect.facebook.net": "Meta Pixel",
    "hotjar.com": "Hotjar",
    "clarity.ms": "Microsoft Clarity",
    "fullstory.com": "FullStory",
    "segment.com": "Segment",
    "mixpanel.com": "Mixpanel",
    "plausible.io": "Plausible",
    "umami.is": "Umami",
    "matomo": "Matomo",
}

KNOWN_CDN_HINTS = {
    "cdn.jsdelivr.net",
    "unpkg.com",
    "cdnjs.cloudflare.com",
    "ajax.googleapis.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
}

PLACEHOLDER_PATTERNS = {
    "lorem ipsum": "lorem ipsum",
    "coming soon": "coming soon",
    "your company": "your company",
    "your business": "your business",
    "example.com": "example.com",
    "todo": "TODO",
    "tbd": "TBD",
    "placeholder": "placeholder",
}

LOCAL_OR_STAGING_PATTERN = re.compile(
    r"\b(localhost|127\.0\.0\.1|0\.0\.0\.0|\.local\b|\.test\b|staging\b|preview\b|dev\.|example\.com)\b",
    re.IGNORECASE,
)

LOCAL_FILE_PATTERN = re.compile(r"(/Users/|/home/[^/]+/|[A-Za-z]:\\)")

SECRET_PATTERNS = [
    ("PRIVATE_KEY", re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |)PRIVATE KEY-----")),
    ("GENERIC_API_SECRET", re.compile(r"(?i)\b(api[_-]?secret|client[_-]?secret|secret[_-]?key|private[_-]?key)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]")),
    ("GENERIC_TOKEN", re.compile(r"(?i)\b(access[_-]?token|auth[_-]?token|bearer[_-]?token)\b\s*[:=]\s*['\"][^'\"]{16,}['\"]")),
    ("STRIPE_SECRET_KEY", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{12,}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]

GENERIC_LINK_TEXT = {
    "click here",
    "here",
    "read more",
    "learn more",
    "more",
    "link",
}

GENERIC_BUTTON_TEXT = {
    "submit",
    "send",
    "click here",
    "learn more",
}

CTA_WORDS = {
    "book",
    "call",
    "contact",
    "email",
    "get",
    "quote",
    "schedule",
    "start",
    "subscribe",
    "download",
    "buy",
    "order",
    "request",
}

CATEGORY_GUIDANCE = {
    "Accessibility": "Fix the semantic, keyboard, focus, label, alternative text, or contrast risk in source, then retest with keyboard and a free accessibility audit.",
    "Asset Management": "Replace, optimize, rename, self-host, or document the asset so it is legal, lightweight, accessible, and deployment-safe.",
    "Content Strategy": "Replace placeholder or thin content with accurate, specific, user-focused copy and record the content owner or source.",
    "Conversion Rate Optimisation": "Clarify the action, destination, proof, and user expectation; track only meaningful conversions.",
    "Forms & Lead Capture": "Use accessible labels, a production static-friendly HTTPS endpoint, clear success/failure states, and privacy reassurance.",
    "Front-End Development": "Update the HTML/CSS/JS source with standards-based, portable code and rerun the audit.",
    "Hosting & Infrastructure": "Replace local, staging, or host-specific references with production-safe URLs and document deployment behavior.",
    "Information Architecture": "Correct the URL, link, navigation, sitemap, or hierarchy so users and crawlers can reach the page predictably.",
    "Legal, Privacy & Compliance": "Add or update the policy, notice, consent behavior, or legal review evidence so it matches actual site behavior.",
    "Performance Optimisation": "Reduce asset/code weight, reserve layout space, defer non-critical work, and verify on mobile.",
    "QA": "Fix the broken path, missing asset, invalid state, or launch blocker, then rerun the audit and manual browser checks.",
    "Security": "Remove the risky file, secret, unsafe link, script, or exposure; rotate any exposed credential and retest production output.",
    "SEO": "Add unique, accurate, crawlable metadata/content and confirm sitemap, canonical, robots, and social tags use production URLs.",
    "Static Website Architecture": "Create the missing static support file or fallback and ensure it works on the selected static host.",
    "Tracking Analytics": "Keep tracking consent-aware, privacy-safe, deduplicated, documented, and focused on meaningful events.",
    "UX": "Make the user path clear, remove placeholder or dead-end interactions, and verify the journey on mobile and keyboard.",
}

CODE_GUIDANCE = {
    "MISSING_DOCTYPE": "Add `<!doctype html>` as the first meaningful line of the HTML document.",
    "MISSING_LANG": "Add a valid language code to the `<html>` element, for example `<html lang=\"en\">`.",
    "MISSING_CHARSET": "Add `<meta charset=\"utf-8\">` inside `<head>`.",
    "MISSING_VIEWPORT": "Add `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">` inside `<head>`.",
    "MISSING_TITLE": "Add a unique, descriptive `<title>` that matches the page intent.",
    "MISSING_META_DESCRIPTION": "Add a unique human-written meta description that accurately summarizes the page.",
    "MISSING_CANONICAL": "Add a canonical link using the production HTTPS URL for this page.",
    "IMG_MISSING_ALT": "Add meaningful alt text for informative images or `alt=\"\"` for decorative images.",
    "IMG_MISSING_DIMENSIONS": "Add width and height attributes or reserve layout space in CSS to prevent layout shift.",
    "IMG_LOADING_UNSPECIFIED": "Add `loading=\"lazy\"` for below-fold images and `loading=\"eager\"` only for critical above-fold imagery.",
    "IMG_DECODING_UNSPECIFIED": "Add `decoding=\"async\"` unless the image has a specific rendering dependency.",
    "TARGET_BLANK_WITHOUT_NOOPENER": "Add `rel=\"noopener noreferrer\"` to external links that open in a new tab.",
    "BROKEN_INTERNAL_LINK": "Fix the href path, create the missing target page, or remove the link.",
    "BROKEN_PAGE_ANCHOR": "Create the target `id` or update the fragment to match an existing section.",
    "FORM_CONTROL_MISSING_LABEL": "Connect a visible `<label for=\"...\">` to the control or provide an appropriate accessible name.",
    "BUTTON_MISSING_NAME": "Add visible text or an `aria-label` that describes the button action.",
    "BUTTON_MISSING_TYPE": "Add `type=\"button\"`, `type=\"submit\"`, or `type=\"reset\"` intentionally.",
    "INVALID_JSON_LD": "Fix the JSON-LD syntax and ensure schema matches visible page content.",
    "BLOCKING_HEAD_SCRIPT": "Add `defer`, `async`, or `type=\"module\"` where safe, or move non-critical scripts later.",
    "MISSING_PRIVACY_PAGE": "Create a privacy page that matches forms, analytics, cookies, embeds, and processors.",
    "MISSING_COOKIE_PAGE": "Create a cookie notice/page when analytics, storage, embeds, or tracking cookies are used.",
    "MISSING_ACCESSIBILITY_PAGE": "Create an honest accessibility statement with contact route and known limitations.",
    "MISSING_TERMS_PAGE": "Create terms/legal/disclaimer pages where the site collects leads, sells, gives advice, or has regulated claims.",
    "ROBOTS_BLOCKS_ALL": "Update robots.txt so production pages are crawlable unless the site is intentionally private.",
    "SITEMAP_STALE": "Regenerate sitemap.xml from the current static HTML inventory.",
    "LOCAL_OR_STAGING_REFERENCE": "Replace localhost, staging, preview, test, or example URLs with production-safe URLs before launch.",
    "SECRET_LIKE_VALUE": "Remove the value from public code and rotate it if it was real.",
    "CONSOLE_LOG_FOUND": "Remove debug logging from production JavaScript.",
    "DEBUGGER_FOUND": "Remove `debugger` statements from production JavaScript.",
}

MANUAL_REVIEW_REQUIRED = [
    "Business purpose, audience fit, positioning, page narrative, and proof quality.",
    "Visual polish, brand expression, image suitability, responsive screenshots, and premium feel.",
    "Full WCAG 2.2 AA conformance, screen reader behavior, color contrast judgment, and keyboard journey quality.",
    "Legal, privacy, cookie, accessibility statement, regulated-claim, and industry-specific compliance review.",
    "Live hosting, DNS, HTTPS, redirects, form delivery, analytics dashboards, monitoring alerts, and browser/device QA.",
]


@dataclass
class Issue:
    severity: str
    category: str
    code: str
    file: str
    message: str
    evidence: str = ""
    fixable: bool = False
    how_to_fix: str = ""


@dataclass
class FixAction:
    file: str
    action: str
    written: bool
    detail: str = ""


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str], int]] = []
        self.end_tags: list[tuple[str, int]] = []
        self.title_parts: list[str] = []
        self.heading_stack: list[tuple[str, int, list[str]]] = []
        self.headings: list[tuple[int, str, int]] = []
        self.button_stack: list[tuple[dict[str, str], int, list[str]]] = []
        self.buttons: list[tuple[dict[str, str], str, int]] = []
        self.anchor_stack: list[tuple[dict[str, str], int, list[str]]] = []
        self.links: list[tuple[dict[str, str], str, int]] = []
        self.in_title = False
        self.script_stack: list[tuple[dict[str, str], int, list[str]]] = []
        self.scripts: list[tuple[dict[str, str], str, int]] = []
        self.in_head = False
        self.head_scripts: list[tuple[dict[str, str], int]] = []
        self.comments: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        line = self.getpos()[0]
        data = {name.lower(): value or "" for name, value in attrs}
        self.tags.append((tag, data, line))
        if tag == "head":
            self.in_head = True
        elif tag == "title":
            self.in_title = True
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_stack.append((tag, line, []))
        elif tag == "button":
            self.button_stack.append((data, line, []))
        elif tag == "a":
            self.anchor_stack.append((data, line, []))
        elif tag == "script":
            self.script_stack.append((data, line, []))
            if self.in_head:
                self.head_scripts.append((data, line))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        line = self.getpos()[0]
        self.end_tags.append((tag, line))
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self.heading_stack:
            start_tag, start_line, parts = self.heading_stack.pop()
            if start_tag == tag:
                level = int(tag[1])
                self.headings.append((level, normalize_space("".join(parts)), start_line))
        elif tag == "button" and self.button_stack:
            attrs, start_line, parts = self.button_stack.pop()
            self.buttons.append((attrs, normalize_space("".join(parts)), start_line))
        elif tag == "a" and self.anchor_stack:
            attrs, start_line, parts = self.anchor_stack.pop()
            self.links.append((attrs, normalize_space("".join(parts)), start_line))
        elif tag == "script" and self.script_stack:
            attrs, start_line, parts = self.script_stack.pop()
            self.scripts.append((attrs, "".join(parts), start_line))

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        for _, _, parts in self.heading_stack:
            parts.append(data)
        for _, _, parts in self.button_stack:
            parts.append(data)
        for _, _, parts in self.anchor_stack:
            parts.append(data)
        for _, _, parts in self.script_stack:
            parts.append(data)

    def handle_comment(self, data: str) -> None:
        self.comments.append((data, self.getpos()[0]))


@dataclass
class Page:
    path: Path
    rel: str
    html: str
    parser: PageParser

    @property
    def title(self) -> str:
        return normalize_space("".join(self.parser.title_parts))

    @property
    def tags(self) -> list[tuple[str, dict[str, str], int]]:
        return self.parser.tags


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def rel_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_excluded(path: Path) -> bool:
    return path.name in EXCLUDED_FILES or any(part in EXCLUDED_DIRS for part in path.parts)


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and not is_excluded(path.relative_to(root)):
            yield path


def iter_html_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in iter_files(root)
        if path.suffix.lower() in {".html", ".htm"}
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_page(path: Path, root: Path) -> Page:
    source = read_text(path)
    parser = PageParser()
    try:
        parser.feed(source)
    except Exception:
        # HTMLParser is forgiving, but malformed inputs can still surprise it.
        pass
    return Page(path=path, rel=rel_path(path, root), html=source, parser=parser)


def first_attr(page: Page, tag: str, attr: str, value: str | None = None) -> dict[str, str] | None:
    for found_tag, attrs, _ in page.tags:
        if found_tag != tag:
            continue
        if attr not in attrs:
            continue
        if value is None or attrs.get(attr, "").lower() == value.lower():
            return attrs
    return None


def all_tags(page: Page, tag: str) -> list[tuple[dict[str, str], int]]:
    return [(attrs, line) for found_tag, attrs, line in page.tags if found_tag == tag]


def tag_count(page: Page, tag: str) -> int:
    return sum(1 for found_tag, _, _ in page.tags if found_tag == tag)


def meta_content(page: Page, name: str) -> str:
    lname = name.lower()
    for tag, attrs, _ in page.tags:
        if tag == "meta" and attrs.get("name", "").lower() == lname:
            return attrs.get("content", "").strip()
    return ""


def property_content(page: Page, prop: str) -> str:
    lprop = prop.lower()
    for tag, attrs, _ in page.tags:
        if tag == "meta" and attrs.get("property", "").lower() == lprop:
            return attrs.get("content", "").strip()
    return ""


def link_href(page: Page, rel_value: str) -> str:
    wanted = rel_value.lower()
    for tag, attrs, _ in page.tags:
        if tag != "link":
            continue
        rels = attrs.get("rel", "").lower().split()
        if wanted in rels:
            return attrs.get("href", "").strip()
    return ""


def page_url(root: Path, page: Path, base_url: str) -> str:
    base = base_url.rstrip("/") + "/"
    rel = page.relative_to(root).as_posix()
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return urljoin(base, rel)


def is_probably_external(href: str) -> bool:
    parsed = urlparse(href)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_ignored_href(href: str) -> bool:
    if not href:
        return True
    if href.startswith("#"):
        return True
    parsed = urlparse(href)
    return parsed.scheme in {
        "mailto",
        "tel",
        "sms",
        "javascript",
        "data",
        "blob",
        "whatsapp",
    }


def internal_target_exists(root: Path, page_path: Path, href: str, base_url: str | None) -> bool:
    if is_ignored_href(href):
        return True
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if not base_url:
            return True
        base_host = urlparse(base_url).netloc.lower()
        if parsed.netloc.lower() != base_host:
            return True
        target_path = parsed.path
    else:
        target_path = parsed.path

    if not target_path:
        return True
    if target_path.startswith("/"):
        candidate = root / target_path.lstrip("/")
    else:
        candidate = (page_path.parent / target_path).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            return False

    candidates = [candidate]
    if candidate.suffix == "":
        candidates.extend([candidate / "index.html", candidate.with_suffix(".html")])
    elif candidate.name == "":
        candidates.append(candidate / "index.html")

    return any(path.exists() for path in candidates)


def guess_page_label(path: Path) -> str:
    if path.stem == "index":
        if path.parent.name:
            return path.parent.name.replace("-", " ").replace("_", " ").title()
        return "Home"
    return path.stem.replace("-", " ").replace("_", " ").title()


def find_tag_open(source: str, tag: str) -> re.Match[str] | None:
    return re.search(rf"<{tag}\b[^>]*>", source, flags=re.IGNORECASE)


def insert_after_head_open(source: str, content: str) -> str:
    match = find_tag_open(source, "head")
    if match:
        return source[: match.end()] + "\n" + content.rstrip() + source[match.end() :]
    html_match = find_tag_open(source, "html")
    head = f"\n<head>\n{content.rstrip()}\n</head>\n"
    if html_match:
        return source[: html_match.end()] + head + source[html_match.end() :]
    return f"<!doctype html>\n<html>\n<head>\n{content.rstrip()}\n</head>\n<body>\n{source}\n</body>\n</html>\n"


def insert_before_head_close(source: str, content: str) -> str:
    match = re.search(r"</head\s*>", source, flags=re.IGNORECASE)
    if match:
        return source[: match.start()] + content.rstrip() + "\n" + source[match.start() :]
    return insert_after_head_open(source, content)


def has_attr(tag_source: str, attr: str) -> bool:
    return bool(re.search(rf"\s{re.escape(attr)}\s*=", tag_source, flags=re.IGNORECASE))


def set_or_add_attr(tag_source: str, attr: str, value: str) -> str:
    escaped = html.escape(value, quote=True)
    if has_attr(tag_source, attr):
        return re.sub(
            rf"(\s{re.escape(attr)}\s*=\s*)(['\"])(.*?)(\2)",
            rf'\1"{escaped}"',
            tag_source,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    if tag_source.endswith("/>"):
        return tag_source[:-2].rstrip() + f' {attr}="{escaped}" />'
    return tag_source[:-1].rstrip() + f' {attr}="{escaped}">'


def append_rel_values(tag_source: str, required: set[str]) -> str:
    rel_match = re.search(
        r"(\srel\s*=\s*)(['\"])(.*?)(\2)",
        tag_source,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not rel_match:
        return set_or_add_attr(tag_source, "rel", " ".join(sorted(required)))
    current = set(rel_match.group(3).lower().split())
    merged = " ".join(sorted(current | required))
    return tag_source[: rel_match.start(3)] + merged + tag_source[rel_match.end(3) :]


def file_size_kb(path: Path) -> float:
    try:
        return path.stat().st_size / 1024
    except OSError:
        return 0.0


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 10:
        return None
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:3] == b"GIF" and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in {0xD8, 0xD9}:
                continue
            if index + 2 > len(data):
                break
            length = int.from_bytes(data[index : index + 2], "big")
            if length < 2:
                break
            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            } and index + 7 < len(data):
                height = int.from_bytes(data[index + 3 : index + 5], "big")
                width = int.from_bytes(data[index + 5 : index + 7], "big")
                return width, height
            index += length
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            width = int.from_bytes(data[24:27] + b"\x00", "little") + 1
            height = int.from_bytes(data[27:30] + b"\x00", "little") + 1
            return width, height
        if chunk == b"VP8 " and len(data) >= 30:
            width = int.from_bytes(data[26:28], "little") & 0x3FFF
            height = int.from_bytes(data[28:30], "little") & 0x3FFF
            return width, height
        if chunk == b"VP8L" and len(data) >= 25:
            bits = int.from_bytes(data[21:25], "little")
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            return width, height
    if path.suffix.lower() == ".svg":
        text = data[:4096].decode("utf-8", errors="ignore")
        width_match = re.search(r'\bwidth=["\']?([0-9.]+)', text)
        height_match = re.search(r'\bheight=["\']?([0-9.]+)', text)
        if width_match and height_match:
            return int(float(width_match.group(1))), int(float(height_match.group(1)))
        viewbox = re.search(r'\bviewBox=["\']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)', text)
        if viewbox:
            return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
    return None


def local_asset_path(root: Path, page_path: Path, src: str, base_url: str | None = None) -> Path | None:
    if not src or src.startswith("data:"):
        return None
    parsed = urlparse(src)
    if parsed.scheme in {"http", "https"}:
        if not base_url or parsed.netloc.lower() != urlparse(base_url).netloc.lower():
            return None
        src_path = parsed.path
    else:
        src_path = parsed.path
    if not src_path:
        return None
    if src_path.startswith("/"):
        return root / src_path.lstrip("/")
    return (page_path.parent / src_path).resolve()


def has_focus_css(root: Path) -> bool:
    for path in iter_files(root):
        if path.suffix.lower() != ".css":
            continue
        try:
            text = read_text(path)
        except OSError:
            continue
        if re.search(r":focus(?:-visible)?\b", text):
            return True
    return False


def has_reduced_motion_css(root: Path) -> bool:
    for path in iter_files(root):
        if path.suffix.lower() != ".css":
            continue
        try:
            text = read_text(path)
        except OSError:
            continue
        if "prefers-reduced-motion" in text:
            return True
    return False


def has_design_tokens(root: Path) -> bool:
    for path in iter_files(root):
        if path.suffix.lower() != ".css":
            continue
        try:
            text = read_text(path)
        except OSError:
            continue
        if re.search(r":root\s*{[^}]*--[a-z0-9-]+\s*:", text, flags=re.IGNORECASE | re.DOTALL):
            return True
    return False


def collect_third_party_domains(pages: list[Page]) -> set[str]:
    domains: set[str] = set()
    attr_names = {"src", "href", "action"}
    for page in pages:
        for _, attrs, _ in page.tags:
            for attr in attr_names:
                value = attrs.get(attr, "")
                parsed = urlparse(value)
                if parsed.scheme in {"http", "https"} and parsed.netloc:
                    domains.add(parsed.netloc.lower())
    return domains


def has_forms(pages: list[Page]) -> bool:
    return any(tag == "form" for page in pages for tag, _, _ in page.tags)


def has_tag_with_href(pages: list[Page], words: set[str]) -> bool:
    for page in pages:
        for tag, attrs, _ in page.tags:
            if tag != "a":
                continue
            href = attrs.get("href", "").lower()
            if any(word in href for word in words):
                return True
    return False


def has_tracking(texts: Iterable[str], domains: set[str]) -> bool:
    for domain in domains:
        if any(hint in domain for hint in TRACKING_HINTS):
            return True
    combined = "\n".join(texts).lower()
    return any(hint in combined for hint in TRACKING_HINTS)


def visible_text(source: str) -> str:
    cleaned = re.sub(r"<(script|style|svg)\b.*?</\1\s*>", " ", source, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"<!--.*?-->", " ", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return normalize_space(html.unescape(cleaned))


def word_count(source: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", visible_text(source)))


def page_ids(page: Page) -> set[str]:
    ids = {attrs["id"] for _, attrs, _ in page.tags if attrs.get("id")}
    ids.update(attrs["name"] for tag, attrs, _ in page.tags if tag == "a" and attrs.get("name"))
    return ids


def page_has_skip_link(page: Page) -> bool:
    for attrs, text, _ in page.parser.links:
        href = attrs.get("href", "")
        if href.startswith("#") and "skip" in text.lower():
            return True
        if href in {"#main", "#main-content", "#content"}:
            return True
    return False


def link_target_path(root: Path, page_path: Path, href: str, base_url: str | None) -> Path | None:
    if is_ignored_href(href):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if not base_url:
            return None
        if parsed.netloc.lower() != urlparse(base_url).netloc.lower():
            return None
        target_path = parsed.path
    else:
        target_path = parsed.path
    if not target_path:
        return page_path
    if target_path.startswith("/"):
        candidate = root / target_path.lstrip("/")
    else:
        candidate = (page_path.parent / target_path).resolve()
    candidates = [candidate]
    if candidate.suffix == "":
        candidates.extend([candidate / "index.html", candidate.with_suffix(".html")])
    return next((path for path in candidates if path.exists() and path.suffix.lower() in {".html", ".htm"}), None)


def is_homepage(path: Path, root: Path) -> bool:
    return path.resolve() == (root / "index.html").resolve()


def looks_like_contact_page(page: Page) -> bool:
    rel = page.rel.lower()
    title = page.title.lower()
    headings = " ".join(text.lower() for _, text, _ in page.parser.headings)
    return any(word in rel or word in title or word in headings for word in {"contact", "booking", "quote", "consultation"})


def has_contact_route(page: Page) -> bool:
    if any(tag == "form" for tag, _, _ in page.tags):
        return True
    for tag, attrs, _ in page.tags:
        if tag != "a":
            continue
        href = attrs.get("href", "").lower()
        if href.startswith(("mailto:", "tel:", "https://wa.me", "whatsapp:")) or "booking" in href or "calendar" in href:
            return True
    return False


def has_cta(page: Page) -> bool:
    candidates = [text.lower() for _, text, _ in page.parser.links + page.parser.buttons]
    if any(any(word in text for word in CTA_WORDS) for text in candidates):
        return True
    return has_contact_route(page)


def fix_guidance(code: str, category: str, custom: str = "") -> str:
    return custom or CODE_GUIDANCE.get(code) or CATEGORY_GUIDANCE.get(category, "Review the finding, correct the affected source, and rerun the audit.")


def audit_site(root: Path, base_url: str | None = None) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    html_paths = iter_html_files(root)
    pages = [parse_page(path, root) for path in html_paths]

    def add(
        severity: str,
        category: str,
        code: str,
        file: str,
        message: str,
        evidence: str = "",
        fixable: bool = False,
        how_to_fix: str = "",
    ) -> None:
        issues.append(Issue(severity, category, code, file, message, evidence, fixable, fix_guidance(code, category, how_to_fix)))

    if not html_paths:
        add("critical", "Static Website Architecture", "NO_HTML", ".", "No HTML files were found in the target folder.")
        return issues

    if not (root / "index.html").exists():
        add("critical", "Static Website Architecture", "MISSING_HOMEPAGE", "index.html", "Root index.html homepage is missing.")
    if not (root / "robots.txt").exists():
        add("high", "SEO", "MISSING_ROBOTS", "robots.txt", "robots.txt is missing.", fixable=True)
    else:
        robots_text = read_text(root / "robots.txt")
        if re.search(r"(?im)^\s*disallow\s*:\s*/\s*$", robots_text):
            add("critical", "SEO", "ROBOTS_BLOCKS_ALL", "robots.txt", "robots.txt appears to block the entire production site.")
        if base_url and base_url not in robots_text and "sitemap:" in robots_text.lower():
            add("medium", "SEO", "ROBOTS_SITEMAP_DOMAIN_MISMATCH", "robots.txt", "robots.txt references a sitemap that may not use the configured production domain.")
    if not (root / "sitemap.xml").exists():
        add("high", "SEO", "MISSING_SITEMAP", "sitemap.xml", "sitemap.xml is missing.", fixable=True)
    elif base_url:
        sitemap_text = read_text(root / "sitemap.xml")
        found_urls = set(re.findall(r"<loc>\s*([^<]+)\s*</loc>", sitemap_text, flags=re.IGNORECASE))
        expected_urls = {url for url, _ in sitemap_urls(root, base_url)}
        missing_urls = sorted(expected_urls - found_urls)
        stale_urls = sorted(url for url in found_urls if LOCAL_OR_STAGING_PATTERN.search(url))
        if missing_urls:
            add(
                "medium",
                "SEO",
                "SITEMAP_STALE",
                "sitemap.xml",
                "sitemap.xml does not include every indexable static HTML page.",
                evidence=", ".join(missing_urls[:5]),
                fixable=True,
            )
        if stale_urls:
            add(
                "high",
                "SEO",
                "SITEMAP_STAGING_URL",
                "sitemap.xml",
                "sitemap.xml contains localhost, staging, preview, test, or example URLs.",
                evidence=", ".join(stale_urls[:5]),
            )
    if not (root / "404.html").exists():
        add("medium", "Static Website Architecture", "MISSING_404", "404.html", "Custom 404.html is missing.", fixable=True)
    if not any((root / name).exists() for name in {"_headers", "headers", "staticwebapp.config.json", "vercel.json"}):
        add(
            "medium",
            "Security",
            "MISSING_SECURITY_HEADER_TEMPLATE",
            ".",
            "No static hosting security header template or config file was found.",
            fixable=True,
        )
    if not any((root / name).exists() for name in {"terms.html", "terms/index.html", "legal.html", "legal/index.html"}):
        add("medium", "Legal, Privacy & Compliance", "MISSING_TERMS_PAGE", ".", "No obvious terms, legal, or disclaimer page was found.", fixable=True)
    if not any((root / name).exists() for name in {"accessibility.html", "accessibility/index.html"}):
        add("medium", "Accessibility", "MISSING_ACCESSIBILITY_PAGE", ".", "No obvious accessibility statement page was found.", fixable=True)
    if not any((root / name).exists() for name in {"sitemap.html", "site-map.html", "sitemap/index.html"}):
        add("low", "Information Architecture", "MISSING_HTML_SITEMAP", ".", "No human-readable HTML sitemap page was found.", fixable=True)
    if not (root / "site.webmanifest").exists():
        add("low", "Asset Management", "MISSING_WEB_MANIFEST", "site.webmanifest", "site.webmanifest is missing.", fixable=True)
    if not (root / ".well-known" / "security.txt").exists():
        add("low", "Security", "MISSING_SECURITY_TXT", ".well-known/security.txt", "security.txt is missing.", fixable=True)

    for path in iter_files(root):
        name = path.name
        rel = rel_path(path, root)
        if any(char.isspace() for char in name) or any(char.isupper() for char in name):
            add(
                "low",
                "Asset Management",
                "NON_PORTABLE_FILE_NAME",
                rel,
                "File name contains spaces or uppercase characters; static hosts are often case-sensitive.",
                evidence=name,
            )
        if name in RISKY_PUBLIC_PATTERNS or path.suffix.lower() in RISKY_SUFFIXES:
            add(
                "high",
                "Security",
                "RISKY_PUBLIC_FILE",
                rel,
                "A file that is often unsafe in public deploy output is present.",
                evidence=name,
            )
        suffix = path.suffix.lower()
        if suffix in TEXT_EXTENSIONS:
            text = read_text(path)
            local_match = LOCAL_OR_STAGING_PATTERN.search(text)
            if local_match:
                add(
                    "high",
                    "Hosting & Infrastructure",
                    "LOCAL_OR_STAGING_REFERENCE",
                    rel,
                    "Localhost, staging, preview, test, or example reference found in deployable text.",
                    evidence=local_match.group(0),
                )
            local_file_match = LOCAL_FILE_PATTERN.search(text)
            if local_file_match:
                add(
                    "high",
                    "Security",
                    "LOCAL_FILE_PATH_REFERENCE",
                    rel,
                    "Local machine path found in deployable text.",
                    evidence=local_file_match.group(0),
                )
            for secret_name, pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    add(
                        "critical",
                        "Security",
                        "SECRET_LIKE_VALUE",
                        rel,
                        "Secret-like value found in public static source.",
                        evidence=secret_name,
                    )
            lowered_text = text.lower()
            for pattern_text, label in PLACEHOLDER_PATTERNS.items():
                if pattern_text in lowered_text:
                    add(
                        "medium",
                        "Content Strategy",
                        "PLACEHOLDER_CONTENT",
                        rel,
                        "Placeholder, unfinished, or example content appears in deployable source.",
                        evidence=label,
                    )
                    break
            if suffix in SCRIPT_EXTENSIONS:
                if re.search(r"\bconsole\.(log|debug|info)\s*\(", text):
                    add("low", "Front-End Development", "CONSOLE_LOG_FOUND", rel, "Debug console logging remains in JavaScript.")
                if re.search(r"\bdebugger\s*;", text):
                    add("high", "Front-End Development", "DEBUGGER_FOUND", rel, "debugger statement remains in JavaScript.")
        size = file_size_kb(path)
        if suffix in IMAGE_EXTENSIONS and size > 512:
            add(
                "medium",
                "Performance Optimisation",
                "LARGE_IMAGE",
                rel,
                "Image exceeds 512 KB and should be reviewed for resizing or compression.",
                evidence=f"{size:.1f} KB",
            )
        if suffix in SCRIPT_EXTENSIONS and size > 100:
            add(
                "medium",
                "Performance Optimisation",
                "LARGE_SCRIPT",
                rel,
                "JavaScript file exceeds 100 KB.",
                evidence=f"{size:.1f} KB",
            )
        if suffix in STYLE_EXTENSIONS and size > 100:
            add(
                "medium",
                "Performance Optimisation",
                "LARGE_STYLESHEET",
                rel,
                "CSS file exceeds 100 KB.",
                evidence=f"{size:.1f} KB",
            )
        if suffix == ".svg":
            text = read_text(path)[:20000].lower()
            if "<script" in text or "onload=" in text or "onclick=" in text:
                add("high", "Security", "RISKY_SVG", rel, "SVG contains script or inline event handlers.")

    if not has_focus_css(root):
        add(
            "medium",
            "Accessibility",
            "NO_FOCUS_CSS_FOUND",
            ".",
            "No :focus or :focus-visible CSS was found. Verify visible keyboard focus states.",
        )
    if not has_reduced_motion_css(root):
        add(
            "medium",
            "Accessibility",
            "NO_REDUCED_MOTION_CSS_FOUND",
            ".",
            "No prefers-reduced-motion CSS was found. Motion-heavy sites must respect reduced motion preferences.",
        )
    if not has_design_tokens(root):
        add(
            "low",
            "Design System",
            "NO_CSS_TOKENS_FOUND",
            ".",
            "No CSS custom property token system was detected. Verify color, spacing, typography, radius, and motion consistency manually.",
        )

    titles: dict[str, list[str]] = {}
    descriptions: dict[str, list[str]] = {}
    all_texts: list[str] = []
    incoming_links: set[str] = set()

    for page in pages:
        all_texts.append(page.html)
        rel = page.rel
        lower_html = page.html.lower()
        ids = page_ids(page)
        id_values = [attrs["id"] for _, attrs, _ in page.tags if attrs.get("id")]
        duplicates = sorted(value for value, count in Counter(id_values).items() if count > 1)
        if duplicates:
            add(
                "high",
                "Accessibility",
                "DUPLICATE_ID",
                rel,
                "Duplicate id values can break labels, anchors, scripts, and assistive technology.",
                evidence=", ".join(duplicates[:5]),
            )
        page_word_count = word_count(page.html)
        if page_word_count < 120 and page.path.name != "404.html":
            add(
                "low",
                "Content Strategy",
                "THIN_PAGE_CONTENT",
                rel,
                "Page has very little visible text. Verify it is not thin, unfinished, or missing strategic content.",
                evidence=f"{page_word_count} words",
            )
        if not re.match(r"\s*<!doctype\s+html\b", page.html, flags=re.IGNORECASE):
            add("medium", "Front-End Development", "MISSING_DOCTYPE", rel, "HTML5 doctype is missing.", fixable=True)

        html_tag = next((attrs for tag, attrs, _ in page.tags if tag == "html"), None)
        if html_tag is None:
            add("high", "Accessibility", "MISSING_HTML_TAG", rel, "html element is missing or malformed.")
        elif not html_tag.get("lang"):
            add("high", "Accessibility", "MISSING_LANG", rel, "html lang attribute is missing.", fixable=True)
        elif not re.match(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$", html_tag.get("lang", "")):
            add("medium", "Accessibility", "INVALID_LANG_FORMAT", rel, "html lang attribute does not look like a valid language code.", evidence=html_tag.get("lang", ""))

        if tag_count(page, "main") == 0:
            add("high", "Accessibility", "MISSING_MAIN_LANDMARK", rel, "No main landmark was found.")
        elif tag_count(page, "main") > 1:
            add("medium", "Accessibility", "MULTIPLE_MAIN_LANDMARKS", rel, "More than one main landmark was found.", evidence=str(tag_count(page, "main")))
        if tag_count(page, "header") == 0 and page.path.name != "404.html":
            add("medium", "UX", "MISSING_HEADER", rel, "No header element was found. Verify page orientation and navigation.")
        if tag_count(page, "footer") == 0 and page.path.name != "404.html":
            add("medium", "UX", "MISSING_FOOTER", rel, "No footer element was found. Verify recovery, trust, legal, and contact links.")
        if tag_count(page, "nav") == 0 and len(pages) > 1 and page.path.name != "404.html":
            add("medium", "Information Architecture", "MISSING_NAV_LANDMARK", rel, "No nav landmark was found on a multi-page site.")
        if not page_has_skip_link(page) and tag_count(page, "nav") > 0:
            add("low", "Accessibility", "MISSING_SKIP_LINK", rel, "No skip link was detected for bypassing repeated navigation.")

        if not any(tag == "meta" and "charset" in attrs for tag, attrs, _ in page.tags):
            add("high", "Front-End Development", "MISSING_CHARSET", rel, "meta charset is missing.", fixable=True)
        if not any(tag == "meta" and attrs.get("name", "").lower() == "viewport" for tag, attrs, _ in page.tags):
            add("high", "UX", "MISSING_VIEWPORT", rel, "Responsive viewport meta tag is missing.", fixable=True)

        if not page.title:
            add("high", "SEO", "MISSING_TITLE", rel, "Title tag is missing or empty.", fixable=True)
        else:
            titles.setdefault(page.title.lower(), []).append(rel)
            if len(page.title) < 20:
                add("low", "SEO", "SHORT_TITLE", rel, "Title is shorter than 20 characters and may be too vague.", evidence=page.title)
            if len(page.title) > 65:
                add("low", "SEO", "LONG_TITLE", rel, "Title is longer than 65 characters.", evidence=page.title)

        description = meta_content(page, "description")
        if not description:
            add("high", "SEO", "MISSING_META_DESCRIPTION", rel, "Meta description is missing.")
        else:
            descriptions.setdefault(description.lower(), []).append(rel)
            if len(description) < 70:
                add("low", "SEO", "SHORT_META_DESCRIPTION", rel, "Meta description is shorter than 70 characters and may not explain value clearly.")
            if len(description) > 170:
                add("low", "SEO", "LONG_META_DESCRIPTION", rel, "Meta description is longer than 170 characters.")

        if base_url and not link_href(page, "canonical"):
            add("high", "SEO", "MISSING_CANONICAL", rel, "Canonical link is missing.", fixable=True)
        canonical = link_href(page, "canonical")
        if canonical:
            parsed_canonical = urlparse(canonical)
            if parsed_canonical.scheme != "https":
                add("medium", "SEO", "CANONICAL_NOT_HTTPS", rel, "Canonical URL should use HTTPS.", evidence=canonical)
            if LOCAL_OR_STAGING_PATTERN.search(canonical):
                add("high", "SEO", "CANONICAL_STAGING_URL", rel, "Canonical URL contains localhost, staging, preview, test, or example host.", evidence=canonical)
            if base_url and parsed_canonical.netloc.lower() != urlparse(base_url).netloc.lower():
                add("high", "SEO", "CANONICAL_DOMAIN_MISMATCH", rel, "Canonical URL host does not match the configured base URL.", evidence=canonical)
        canonical_count = sum(1 for tag, attrs, _ in page.tags if tag == "link" and "canonical" in attrs.get("rel", "").lower().split())
        if canonical_count > 1:
            add("medium", "SEO", "MULTIPLE_CANONICALS", rel, "More than one canonical link was found.", evidence=str(canonical_count))

        robots = meta_content(page, "robots").lower()
        if "noindex" in robots:
            add("high", "SEO", "NOINDEX_FOUND", rel, "Page contains a noindex robots directive.", evidence=robots)

        og_requirements = {
            "og:title": property_content(page, "og:title"),
            "og:description": property_content(page, "og:description"),
            "og:image": property_content(page, "og:image"),
            "og:url": property_content(page, "og:url"),
            "og:type": property_content(page, "og:type"),
        }
        for prop, value in og_requirements.items():
            if not value:
                add("low", "SEO", f"MISSING_{prop.upper().replace(':', '_')}", rel, f"{prop} metadata is missing.")
            elif prop in {"og:image", "og:url"} and (LOCAL_OR_STAGING_PATTERN.search(value) or value.startswith("http://")):
                add("medium", "SEO", f"UNSAFE_{prop.upper().replace(':', '_')}", rel, f"{prop} should use a production HTTPS URL.", evidence=value)
        if not meta_content(page, "twitter:card"):
            add("low", "SEO", "MISSING_TWITTER_CARD", rel, "twitter:card metadata is missing.")
        if not link_href(page, "icon") and is_homepage(page.path, root):
            add("low", "Asset Management", "MISSING_FAVICON_LINK", rel, "Homepage has no favicon link.")

        h1_count = sum(1 for level, _, _ in page.parser.headings if level == 1)
        if h1_count == 0:
            add("high", "Accessibility", "MISSING_H1", rel, "No H1 was found.")
        elif h1_count > 1:
            add("medium", "Accessibility", "MULTIPLE_H1", rel, "More than one H1 was found.", evidence=str(h1_count))

        previous_level = 0
        for level, text, line in page.parser.headings:
            if not text:
                add("medium", "Accessibility", "EMPTY_HEADING", rel, "Heading is empty.", evidence=f"line {line}")
            if previous_level and level > previous_level + 1:
                add(
                    "low",
                    "Accessibility",
                    "HEADING_LEVEL_JUMP",
                    rel,
                    "Heading level jumps by more than one.",
                    evidence=f"line {line}: h{previous_level} to h{level}",
                )
            previous_level = level

        for attrs, line in all_tags(page, "img"):
            src = attrs.get("src", "")
            if "alt" not in attrs:
                add("high", "Accessibility", "IMG_MISSING_ALT", rel, "Image is missing alt attribute.", evidence=f"line {line}: {src}")
            if "width" not in attrs or "height" not in attrs:
                local = local_asset_path(root, page.path, src, base_url)
                fixable = bool(local and local.exists() and image_dimensions(local))
                add(
                    "medium",
                    "Performance Optimisation",
                    "IMG_MISSING_DIMENSIONS",
                    rel,
                    "Image is missing width and/or height attributes.",
                    evidence=f"line {line}: {src}",
                    fixable=fixable,
                )
            if attrs.get("loading", "").lower() not in {"lazy", "eager"}:
                add(
                    "low",
                    "Performance Optimisation",
                    "IMG_LOADING_UNSPECIFIED",
                    rel,
                    "Image loading behavior is not specified.",
                    evidence=f"line {line}: {src}",
                    fixable=True,
                )
            if attrs.get("decoding", "").lower() not in {"async", "sync", "auto"}:
                add(
                    "low",
                    "Performance Optimisation",
                    "IMG_DECODING_UNSPECIFIED",
                    rel,
                    "Image decoding behavior is not specified.",
                    evidence=f"line {line}: {src}",
                    fixable=True,
                )
            local = local_asset_path(root, page.path, src, base_url)
            if local and not local.exists():
                add("high", "QA", "MISSING_IMAGE_FILE", rel, "Image source does not resolve.", evidence=f"line {line}: {src}")

        for attrs, text, line in page.parser.links:
            href = attrs.get("href", "")
            if text.lower() in GENERIC_LINK_TEXT:
                add("low", "Content Strategy", "GENERIC_LINK_TEXT", rel, "Link text is generic and may be unclear out of context.", evidence=f"line {line}: {text}")
            if not normalize_space(text) and not attrs.get("aria-label") and not attrs.get("aria-labelledby") and not attrs.get("title"):
                add("high", "Accessibility", "LINK_MISSING_NAME", rel, "Link has no accessible name.", evidence=f"line {line}: {href}")
            if href.strip() in {"", "#", "#!", "javascript:void(0)"}:
                add("medium", "UX", "EMPTY_LINK", rel, "Link has an empty or placeholder href.", evidence=f"line {line}")
            parsed_href = urlparse(href)
            if parsed_href.fragment and not parsed_href.path and parsed_href.fragment not in ids:
                add("medium", "QA", "BROKEN_PAGE_ANCHOR", rel, "Same-page anchor target does not exist.", evidence=f"line {line}: {href}")
            if attrs.get("target", "").lower() == "_blank":
                rels = set(attrs.get("rel", "").lower().split())
                if not {"noopener", "noreferrer"}.issubset(rels):
                    add(
                        "high",
                        "Security",
                        "TARGET_BLANK_WITHOUT_NOOPENER",
                        rel,
                        "target=_blank link is missing rel=noopener noreferrer.",
                        evidence=f"line {line}: {href}",
                        fixable=True,
                    )
            if href.startswith("http://"):
                add("medium", "Security", "INSECURE_HTTP_LINK", rel, "HTTP link found. Prefer HTTPS.", evidence=f"line {line}: {href}")
            if not internal_target_exists(root, page.path, href, base_url):
                add("high", "QA", "BROKEN_INTERNAL_LINK", rel, "Internal link target does not resolve.", evidence=f"line {line}: {href}")
            target_path = link_target_path(root, page.path, href, base_url)
            if target_path:
                incoming_links.add(rel_path(target_path, root))
            if href.startswith("mailto:") and "@" not in href:
                add("medium", "QA", "INVALID_MAILTO_LINK", rel, "mailto link does not contain an email address.", evidence=f"line {line}: {href}")
            if href.startswith("tel:") and len(re.sub(r"\D", "", href)) < 7:
                add("medium", "QA", "INVALID_TEL_LINK", rel, "tel link does not contain enough digits to be usable.", evidence=f"line {line}: {href}")
            if any(word in href.lower() for word in {"drive.google.com", "dropbox.com", "onedrive.live.com"}) and "privacy" not in lower_html:
                add("low", "Security", "PUBLIC_SHARED_FILE_LINK", rel, "Public shared-file link found. Verify the linked file is intended and privacy-reviewed.", evidence=f"line {line}: {href}")

        for attrs, line in all_tags(page, "form"):
            action = attrs.get("action", "").strip()
            if not action:
                add("high", "Forms & Lead Capture", "FORM_MISSING_ACTION", rel, "Form is missing an action URL.", evidence=f"line {line}")
            elif action.startswith("http://"):
                add("high", "Security", "FORM_INSECURE_ACTION", rel, "Form action uses HTTP.", evidence=f"line {line}: {action}")
            elif LOCAL_OR_STAGING_PATTERN.search(action):
                add("high", "Forms & Lead Capture", "FORM_STAGING_ACTION", rel, "Form action appears to use a local, staging, preview, test, or example endpoint.", evidence=f"line {line}: {action}")
            method = attrs.get("method", "get").lower()
            if method == "get":
                add(
                    "medium",
                    "Legal, Privacy & Compliance",
                    "FORM_GET_METHOD",
                    rel,
                    "Form uses GET. Verify personal data is not exposed in URLs.",
                    evidence=f"line {line}",
                )
            if "novalidate" in attrs:
                add("medium", "Forms & Lead Capture", "FORM_NOVALIDATE", rel, "Form disables native validation. Verify accessible custom validation is implemented.", evidence=f"line {line}")
            if "privacy" not in lower_html:
                add("medium", "Legal, Privacy & Compliance", "FORM_WITHOUT_PRIVACY_REFERENCE", rel, "Form page does not mention or link to privacy expectations.", evidence=f"line {line}")

        has_submit_control = any(
            (tag == "button" and attrs.get("type", "submit").lower() == "submit")
            or (tag == "input" and attrs.get("type", "").lower() == "submit")
            for tag, attrs, _ in page.tags
        )
        if any(tag == "form" for tag, _, _ in page.tags) and not has_submit_control:
            add("high", "Forms & Lead Capture", "FORM_MISSING_SUBMIT", rel, "A form exists but no submit control was detected.")

        label_for = {
            attrs.get("for", "")
            for attrs, _ in all_tags(page, "label")
            if attrs.get("for")
        }
        for tag_name in {"input", "select", "textarea"}:
            for attrs, line in all_tags(page, tag_name):
                input_type = attrs.get("type", "").lower()
                if input_type in {"hidden", "submit", "button", "reset", "image"}:
                    continue
                control_id = attrs.get("id", "")
                has_name = bool(attrs.get("aria-label") or attrs.get("aria-labelledby") or (control_id and control_id in label_for))
                if not has_name:
                    add(
                        "high",
                        "Accessibility",
                        "FORM_CONTROL_MISSING_LABEL",
                        rel,
                        f"{tag_name} control is missing an associated label or accessible name.",
                        evidence=f"line {line}: {attrs.get('name', control_id)}",
                    )
                name_hint = (attrs.get("name", "") + " " + attrs.get("id", "") + " " + attrs.get("placeholder", "")).lower()
                if tag_name == "input":
                    input_type = attrs.get("type", "text").lower()
                    if "email" in name_hint and input_type != "email":
                        add("medium", "Forms & Lead Capture", "EMAIL_INPUT_WRONG_TYPE", rel, "Email field should use type=email for validation and mobile keyboards.", evidence=f"line {line}")
                    if any(word in name_hint for word in {"phone", "tel", "whatsapp"}) and input_type != "tel":
                        add("low", "Forms & Lead Capture", "PHONE_INPUT_WRONG_TYPE", rel, "Phone field should usually use type=tel for mobile keyboards.", evidence=f"line {line}")
                    if "url" in name_hint and input_type != "url":
                        add("low", "Forms & Lead Capture", "URL_INPUT_WRONG_TYPE", rel, "URL field should usually use type=url.", evidence=f"line {line}")
                    if any(word in name_hint for word in {"name", "email", "phone", "tel", "address"}) and not attrs.get("autocomplete"):
                        add("low", "Forms & Lead Capture", "INPUT_MISSING_AUTOCOMPLETE", rel, "Common personal-information field is missing autocomplete guidance.", evidence=f"line {line}")
        required_count = sum(1 for tag, attrs, _ in page.tags if tag in {"input", "select", "textarea"} and "required" in attrs)
        field_count = sum(1 for tag, attrs, _ in page.tags if tag in {"input", "select", "textarea"} and attrs.get("type", "").lower() not in {"hidden", "submit", "button", "reset", "image"})
        if any(tag == "form" for tag, _, _ in page.tags) and field_count > 0 and required_count == 0:
            add("low", "Forms & Lead Capture", "FORM_NO_REQUIRED_FIELDS", rel, "Form has fields but no required fields. Verify this is intentional and validation is clear.")

        for attrs, text, line in page.parser.buttons:
            if not normalize_space(text) and not attrs.get("aria-label") and not attrs.get("aria-labelledby") and not attrs.get("title"):
                add("high", "Accessibility", "BUTTON_MISSING_NAME", rel, "Button has no accessible name.", evidence=f"line {line}")
            if not attrs.get("type"):
                add("low", "Front-End Development", "BUTTON_MISSING_TYPE", rel, "Button is missing explicit type.", evidence=f"line {line}")
            if text.lower() in GENERIC_BUTTON_TEXT:
                add("low", "Conversion Rate Optimisation", "GENERIC_BUTTON_TEXT", rel, "Button text is generic. Use specific action language where possible.", evidence=f"line {line}: {text}")

        for attrs, line in all_tags(page, "iframe"):
            src = attrs.get("src", "")
            if not attrs.get("title"):
                add("high", "Accessibility", "IFRAME_MISSING_TITLE", rel, "iframe is missing a descriptive title.", evidence=f"line {line}: {src}")
            if src.startswith("http://"):
                add("high", "Security", "IFRAME_INSECURE_SRC", rel, "iframe source uses HTTP.", evidence=f"line {line}: {src}")
            if attrs.get("loading", "").lower() not in {"lazy", "eager"}:
                add("low", "Performance Optimisation", "IFRAME_LOADING_UNSPECIFIED", rel, "iframe loading behavior is not specified.", evidence=f"line {line}: {src}")
            if "width" not in attrs or "height" not in attrs:
                add("medium", "Performance Optimisation", "IFRAME_MISSING_DIMENSIONS", rel, "iframe is missing width and/or height attributes. Reserve layout space to prevent shifts.", evidence=f"line {line}: {src}")

        for attrs, line in all_tags(page, "video"):
            if "autoplay" in attrs and "muted" not in attrs:
                add("high", "Accessibility", "VIDEO_AUTOPLAY_WITH_SOUND", rel, "Video autoplays without muted attribute.", evidence=f"line {line}")
            if "autoplay" in attrs and not attrs.get("poster"):
                add("low", "Performance Optimisation", "VIDEO_MISSING_POSTER", rel, "Autoplay/background video should have a poster fallback.", evidence=f"line {line}")
            if "controls" not in attrs and "autoplay" not in attrs:
                add("medium", "Accessibility", "VIDEO_WITHOUT_CONTROLS", rel, "Video lacks controls. Verify controls or an accessible alternative exist.", evidence=f"line {line}")

        for attrs, line in all_tags(page, "audio"):
            if "autoplay" in attrs:
                add("high", "Accessibility", "AUDIO_AUTOPLAY", rel, "Audio should not autoplay unexpectedly.", evidence=f"line {line}")
            if "controls" not in attrs:
                add("medium", "Accessibility", "AUDIO_WITHOUT_CONTROLS", rel, "Audio lacks controls.", evidence=f"line {line}")

        for attrs, text, line in page.parser.scripts:
            script_type = attrs.get("type", "").lower()
            if script_type == "application/ld+json":
                try:
                    json.loads(text)
                except json.JSONDecodeError as exc:
                    add("high", "SEO", "INVALID_JSON_LD", rel, "JSON-LD structured data is invalid JSON.", evidence=f"line {line}: {exc}")
            src = attrs.get("src", "")
            parsed_src = urlparse(src)
            if parsed_src.scheme in {"http", "https"} and parsed_src.netloc and not attrs.get("integrity"):
                add(
                    "low",
                    "Security",
                    "EXTERNAL_SCRIPT_WITHOUT_SRI",
                    rel,
                    "External script does not use subresource integrity. Some analytics and embeds cannot use SRI; document the exception.",
                    evidence=f"line {line}: {src}",
                )

        for attrs, line in page.parser.head_scripts:
            if attrs.get("src") and not any(key in attrs for key in {"defer", "async"}) and attrs.get("type", "").lower() != "module":
                add(
                    "medium",
                    "Performance Optimisation",
                    "BLOCKING_HEAD_SCRIPT",
                    rel,
                    "Script in head may block rendering because it lacks defer, async, or type=module.",
                    evidence=f"line {line}: {attrs.get('src')}",
                )

        if page.path.name != "404.html" and not has_cta(page):
            add("low", "Conversion Rate Optimisation", "NO_DETECTABLE_CTA", rel, "No obvious CTA, form, or contact route was detected. Verify the page has a clear next step.")
        if looks_like_contact_page(page) and not has_contact_route(page):
            add("high", "Conversion Rate Optimisation", "CONTACT_PAGE_WITHOUT_CONTACT_ROUTE", rel, "Contact-like page has no detected form, email, phone, WhatsApp, booking, or calendar route.")

        if re.search(r"\son[a-z]+\s*=", page.html, flags=re.IGNORECASE):
            add("medium", "Security", "INLINE_EVENT_HANDLER", rel, "Inline event handlers were found.")
        if re.search(r"\beval\s*\(", page.html):
            add("high", "Security", "EVAL_USAGE", rel, "eval() usage was found.")
        if re.search(r"\bdocument\.write\s*\(", page.html):
            add("high", "Security", "DOCUMENT_WRITE_USAGE", rel, "document.write() usage was found.")
        if re.search(r"\.innerHTML\s*=", page.html):
            add("medium", "Security", "INNER_HTML_ASSIGNMENT", rel, "innerHTML assignment was found. Verify input is trusted or sanitized.")
        if "localstorage" in lower_html or "sessionstorage" in lower_html:
            add(
                "medium",
                "Legal, Privacy & Compliance",
                "BROWSER_STORAGE_USAGE",
                rel,
                "Browser storage usage found. Verify privacy notice and consent requirements.",
            )

    for title, files in titles.items():
        if title and len(files) > 1:
            add("medium", "SEO", "DUPLICATE_TITLE", ", ".join(files), "Multiple pages share the same title.", evidence=title)
    for description, files in descriptions.items():
        if description and len(files) > 1:
            add("medium", "SEO", "DUPLICATE_META_DESCRIPTION", ", ".join(files), "Multiple pages share the same meta description.", evidence=description)

    for page in pages:
        if page.path.name == "404.html" or is_homepage(page.path, root):
            continue
        if page.rel not in incoming_links:
            add(
                "medium",
                "Information Architecture",
                "ORPHAN_PAGE_RISK",
                page.rel,
                "No internal link to this page was detected. Verify navigation, footer, sitemap, and contextual discovery.",
            )

    domains = collect_third_party_domains(pages)
    for domain in sorted(domains):
        if any(hint in domain for hint in TRACKING_HINTS):
            add(
                "medium",
                "Tracking Analytics",
                "TRACKING_DOMAIN_FOUND",
                ".",
                "Tracking or analytics domain found. Verify consent, privacy notice, and performance impact.",
                evidence=domain,
            )
        elif domain in KNOWN_CDN_HINTS:
            add(
                "low",
                "Asset Management",
                "EXTERNAL_CDN_FOUND",
                ".",
                "External CDN dependency found. Verify license, privacy, SRI, and self-hosting option.",
                evidence=domain,
            )

    tracking_detected = has_tracking(all_texts, domains)
    forms_detected = has_forms(pages)
    if forms_detected or tracking_detected:
        if not any((root / name).exists() for name in {"privacy.html", "privacy/index.html", "privacy-policy.html"}):
            add(
                "high",
                "Legal, Privacy & Compliance",
                "MISSING_PRIVACY_PAGE",
                ".",
                "Forms or tracking were detected but no obvious privacy page was found.",
                fixable=True,
            )
    if tracking_detected:
        if not any((root / name).exists() for name in {"cookie-policy.html", "cookies.html", "cookies/index.html"}):
            add(
                "medium",
                "Legal, Privacy & Compliance",
                "MISSING_COOKIE_PAGE",
                ".",
                "Tracking was detected but no obvious cookie notice/page was found.",
                fixable=True,
            )
        combined = "\n".join(all_texts).lower()
        if "consent" not in combined and "cookie" not in combined:
            add(
                "medium",
                "Tracking Analytics",
                "TRACKING_WITHOUT_CONSENT_REFERENCE",
                ".",
                "Tracking was detected but no consent or cookie reference was found in deployable pages.",
            )

    return issues


def severity_rank(severity: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(severity, 5)


def print_text_report(issues: list[Issue]) -> None:
    if not issues:
        print("No issues found by static audit. Manual checklist review is still required.")
        print("Manual review still required:")
        for item in MANUAL_REVIEW_REQUIRED:
            print(f"  - {item}")
        return
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    summary = ", ".join(f"{name}: {counts[name]}" for name in ["critical", "high", "medium", "low", "info"] if counts.get(name))
    print(f"Static audit findings: {summary}")
    print()
    for issue in sorted(issues, key=lambda item: (severity_rank(item.severity), item.category, item.file, item.code)):
        fix = " fixable" if issue.fixable else ""
        print(f"[{issue.severity.upper()}]{fix} {issue.category} {issue.code}")
        print(f"  file: {issue.file}")
        print(f"  {issue.message}")
        if issue.evidence:
            print(f"  evidence: {issue.evidence}")
        if issue.how_to_fix:
            print(f"  how to fix: {issue.how_to_fix}")
        print()
    print("Manual review still required:")
    for item in MANUAL_REVIEW_REQUIRED:
        print(f"  - {item}")


def report_payload(issues: list[Issue]) -> dict[str, object]:
    counts = Counter(issue.severity for issue in issues)
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "issue_count": len(issues),
        "fixable_issue_count": sum(1 for issue in issues if issue.fixable),
        "counts_by_severity": {name: counts.get(name, 0) for name in ["critical", "high", "medium", "low", "info"]},
        "manual_review_required": MANUAL_REVIEW_REQUIRED,
        "issues": [asdict(issue) for issue in issues],
    }


def write_report(issues: list[Issue], out_path: Path) -> None:
    payload = report_payload(issues)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def render_markdown_report(issues: list[Issue], root: Path, base_url: str | None = None) -> str:
    counts = Counter(issue.severity for issue in issues)
    lines = [
        "# Static Site Quality Report",
        "",
        f"- Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Target folder: `{root}`",
    ]
    if base_url:
        lines.append(f"- Base URL: {base_url}")
    lines.extend(
        [
            f"- Total findings: {len(issues)}",
            f"- Fixable findings: {sum(1 for issue in issues if issue.fixable)}",
            "",
            "## Severity Summary",
            "",
        ]
    )
    for severity in ["critical", "high", "medium", "low", "info"]:
        lines.append(f"- {severity}: {counts.get(severity, 0)}")
    lines.extend(["", "## Findings", ""])
    if not issues:
        lines.append("No automated findings. Manual checklist review is still required.")
    for issue in sorted(issues, key=lambda item: (severity_rank(item.severity), item.category, item.file, item.code)):
        fixable = "yes" if issue.fixable else "no"
        lines.extend(
            [
                f"### {issue.severity.upper()} - {issue.category} - {issue.code}",
                "",
                f"- File: `{issue.file}`",
                f"- Fixable by script: {fixable}",
                f"- Problem: {issue.message}",
            ]
        )
        if issue.evidence:
            lines.append(f"- Evidence: `{issue.evidence}`")
        if issue.how_to_fix:
            lines.append(f"- How to fix: {issue.how_to_fix}")
        lines.append("")
    lines.extend(["## Manual Review Still Required", ""])
    for item in MANUAL_REVIEW_REQUIRED:
        lines.append(f"- [ ] {item}")
    lines.extend(
        [
            "",
            "## Recommended Next Commands",
            "",
            "```bash",
            "python3 premium-static-site-system/tools/static_site_quality.py fix <site-folder> --base-url <https://domain.example> --site-name \"<Site Name>\"",
            "python3 premium-static-site-system/tools/static_site_quality.py audit <site-folder> --base-url <https://domain.example> --report-md quality-report.md --out quality-report.json",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def update_html(source: str, path: Path, root: Path, base_url: str | None, site_name: str, default_lang: str) -> str:
    changed = source
    if not re.match(r"\s*<!doctype\s+html\b", changed, flags=re.IGNORECASE):
        changed = "<!doctype html>\n" + changed.lstrip()

    html_match = find_tag_open(changed, "html")
    if html_match:
        tag = html_match.group(0)
        if not has_attr(tag, "lang"):
            changed = changed[: html_match.start()] + set_or_add_attr(tag, "lang", default_lang) + changed[html_match.end() :]
    else:
        changed = re.sub(r"<!doctype html>\s*", f"<!doctype html>\n<html lang=\"{html.escape(default_lang)}\">\n", changed, count=1, flags=re.IGNORECASE)
        if not re.search(r"</html\s*>", changed, flags=re.IGNORECASE):
            changed += "\n</html>\n"

    head_inserts: list[str] = []
    if not re.search(r"<meta\b[^>]*\bcharset\s*=", changed, flags=re.IGNORECASE):
        head_inserts.append('<meta charset="utf-8">')
    if not re.search(r"<meta\b[^>]*\bname\s*=\s*['\"]viewport['\"]", changed, flags=re.IGNORECASE):
        head_inserts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    if head_inserts:
        changed = insert_after_head_open(changed, "\n".join(head_inserts))

    page_label = guess_page_label(path.relative_to(root))
    if not re.search(r"<title\b[^>]*>.*?</title\s*>", changed, flags=re.IGNORECASE | re.DOTALL):
        title = f"{page_label} | {site_name}" if site_name else page_label
        changed = insert_before_head_close(changed, f"<title>{html.escape(title)}</title>")

    if base_url and not re.search(r"<link\b[^>]*\brel\s*=\s*['\"][^'\"]*\bcanonical\b", changed, flags=re.IGNORECASE):
        changed = insert_before_head_close(changed, f'<link rel="canonical" href="{html.escape(page_url(root, path, base_url), quote=True)}">')

    if path.name == "index.html":
        if not re.search(r"<meta\b[^>]*\bproperty\s*=\s*['\"]og:title['\"]", changed, flags=re.IGNORECASE):
            changed = insert_before_head_close(changed, f'<meta property="og:title" content="{html.escape(site_name or page_label, quote=True)}">')
        if base_url and not re.search(r"<meta\b[^>]*\bproperty\s*=\s*['\"]og:url['\"]", changed, flags=re.IGNORECASE):
            changed = insert_before_head_close(changed, f'<meta property="og:url" content="{html.escape(page_url(root, path, base_url), quote=True)}">')
        if not re.search(r"<meta\b[^>]*\bname\s*=\s*['\"]twitter:card['\"]", changed, flags=re.IGNORECASE):
            changed = insert_before_head_close(changed, '<meta name="twitter:card" content="summary_large_image">')

    def patch_anchor(match: re.Match[str]) -> str:
        tag = match.group(0)
        if re.search(r"\starget\s*=\s*(['\"])_blank\1", tag, flags=re.IGNORECASE):
            return append_rel_values(tag, {"noopener", "noreferrer"})
        return tag

    changed = re.sub(r"<a\b[^>]*>", patch_anchor, changed, flags=re.IGNORECASE | re.DOTALL)

    image_index = 0

    def patch_img(match: re.Match[str]) -> str:
        nonlocal image_index
        image_index += 1
        tag = match.group(0)
        patched = tag
        if not has_attr(patched, "decoding"):
            patched = set_or_add_attr(patched, "decoding", "async")
        if not has_attr(patched, "loading"):
            patched = set_or_add_attr(patched, "loading", "eager" if image_index == 1 else "lazy")
        src_match = re.search(r"\ssrc\s*=\s*(['\"])(.*?)\1", patched, flags=re.IGNORECASE | re.DOTALL)
        if src_match and (not has_attr(patched, "width") or not has_attr(patched, "height")):
            local = local_asset_path(root, path, src_match.group(2), base_url)
            if local and local.exists():
                dims = image_dimensions(local)
                if dims:
                    width, height = dims
                    if not has_attr(patched, "width"):
                        patched = set_or_add_attr(patched, "width", str(width))
                    if not has_attr(patched, "height"):
                        patched = set_or_add_attr(patched, "height", str(height))
        return patched

    changed = re.sub(r"<img\b[^>]*>", patch_img, changed, flags=re.IGNORECASE | re.DOTALL)
    return changed


def sitemap_urls(root: Path, base_url: str) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    for path in iter_html_files(root):
        rel = rel_path(path, root)
        if rel in {"404.html"} or rel.endswith("/404.html"):
            continue
        text = read_text(path).lower()
        if re.search(r"<meta\b[^>]*name\s*=\s*['\"]robots['\"][^>]*content\s*=\s*['\"][^'\"]*noindex", text):
            continue
        lastmod = dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).date().isoformat()
        urls.append((page_url(root, path, base_url), lastmod))
    return urls


def render_sitemap(root: Path, base_url: str) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in sitemap_urls(root, base_url):
        lines.extend(
            [
                "  <url>",
                f"    <loc>{html.escape(loc)}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_robots(base_url: str) -> str:
    return "\n".join(["User-agent: *", "Allow: /", f"Sitemap: {base_url.rstrip('/')}/sitemap.xml", ""]) + "\n"


def render_404(site_name: str) -> str:
    title = f"Page not found | {site_name}" if site_name else "Page not found"
    heading = "Page not found"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{html.escape(title)}</title>
  <style>
    body {{ margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.5; color: #111827; background: #ffffff; }}
    main {{ width: min(42rem, calc(100% - 2rem)); margin: 15vh auto; }}
    a {{ color: #0f766e; }}
    a:focus-visible {{ outline: 3px solid #0f766e; outline-offset: 3px; }}
  </style>
</head>
<body>
  <main>
    <h1>{heading}</h1>
    <p>The requested page could not be found.</p>
    <p><a href="/">Return to the homepage</a></p>
  </main>
</body>
</html>
"""


def render_headers() -> str:
    return """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  X-Frame-Options: SAMEORIGIN
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; img-src 'self' data: https:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-src 'self'
"""


def render_security_headers_example() -> str:
    return """# Static hosting security header baseline

Apply equivalent headers in the chosen static host. Tighten Content-Security-Policy
after inventorying every required script, style, font, image, form, analytics, and
embed endpoint.

X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; img-src 'self' data: https:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-src 'self'

Optional after confirming all subdomains use HTTPS:
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
"""


def render_manifest(site_name: str) -> str:
    payload = {
        "name": site_name or "Static Site",
        "short_name": site_name or "Site",
        "start_url": "/",
        "display": "minimal-ui",
        "background_color": "#ffffff",
        "theme_color": "#111827",
        "icons": [],
    }
    return json.dumps(payload, indent=2) + "\n"


def render_a11y_css() -> str:
    return """:root {
  color-scheme: light;
}

.skip-link {
  position: absolute;
  inset-block-start: 0.5rem;
  inset-inline-start: 0.5rem;
  z-index: 1000;
  transform: translateY(-150%);
  padding: 0.75rem 1rem;
  color: #ffffff;
  background: #111827;
  text-decoration: none;
}

.skip-link:focus {
  transform: translateY(0);
}

:focus-visible {
  outline: 3px solid #0f766e;
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
"""


def render_consent_js() -> str:
    return """/*
  Portable consent-aware analytics loader.
  Replace ANALYTICS_LOADER with a function that loads the approved analytics tool.
  Do not load non-essential analytics or marketing scripts before consent where
  consent is legally required.
*/
(function () {
  const STORAGE_KEY = "site_consent_v1";

  function getConsent() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (_) {
      return {};
    }
  }

  function setConsent(value) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      analytics: Boolean(value.analytics),
      marketing: Boolean(value.marketing),
      updatedAt: new Date().toISOString()
    }));
    window.dispatchEvent(new CustomEvent("site-consent-change", { detail: getConsent() }));
  }

  function loadAnalyticsWhenAllowed() {
    const consent = getConsent();
    if (!consent.analytics || window.__siteAnalyticsLoaded) return;
    window.__siteAnalyticsLoaded = true;
    if (typeof window.ANALYTICS_LOADER === "function") {
      window.ANALYTICS_LOADER();
    }
  }

  window.SiteConsent = { get: getConsent, set: setConsent, loadAnalyticsWhenAllowed };
  window.addEventListener("site-consent-change", loadAnalyticsWhenAllowed);
  loadAnalyticsWhenAllowed();
}());
"""


def render_privacy_page(site_name: str) -> str:
    name = html.escape(site_name or "This website")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Privacy Policy | {name}</title>
  <meta name="robots" content="noindex">
</head>
<body>
  <main>
    <h1>Privacy Policy</h1>
    <p><strong>Legal review required before publication.</strong> This template must be replaced with a policy that matches the site, business, jurisdictions, forms, analytics, embeds, and processors.</p>
    <h2>Data Collected</h2>
    <p>Document contact forms, analytics, server logs, cookies, local storage, embeds, and external processors.</p>
    <h2>Purpose</h2>
    <p>Document why each data category is collected and how long it is retained.</p>
    <h2>Processors</h2>
    <p>List hosting, analytics, form, email, map, video, CDN, and booking providers.</p>
    <h2>User Choices</h2>
    <p>Document consent choices, opt-out methods, rights requests, and contact details.</p>
    <h2>Updates</h2>
    <p>Record the effective date and update process.</p>
  </main>
</body>
</html>
"""


def render_cookie_page(site_name: str) -> str:
    name = html.escape(site_name or "This website")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cookie Notice | {name}</title>
  <meta name="robots" content="noindex">
</head>
<body>
  <main>
    <h1>Cookie Notice</h1>
    <p><strong>Legal review required before publication.</strong> Replace this template with a notice that matches the actual cookies, storage, analytics, embeds, and consent behavior.</p>
    <h2>Strictly Necessary Storage</h2>
    <p>List storage required to provide a user-requested service.</p>
    <h2>Analytics Storage</h2>
    <p>List analytics tools, identifiers, retention, and consent requirements.</p>
    <h2>Marketing Storage</h2>
    <p>List marketing pixels or state that none are used.</p>
    <h2>Change Preferences</h2>
    <p>Explain how users can change or withdraw choices.</p>
  </main>
</body>
</html>
"""


def render_terms_page(site_name: str) -> str:
    name = html.escape(site_name or "This website")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Terms | {name}</title>
</head>
<body>
  <main>
    <h1>Terms</h1>
    <p><strong>Legal review required before publication.</strong> Replace this template with terms, disclaimers, payment rules, refund rules, professional notices, and jurisdiction-specific requirements that match the site.</p>
    <h2>Website Use</h2>
    <p>Document acceptable use, content ownership, and limitations.</p>
    <h2>Services, Products, Or Inquiries</h2>
    <p>Document what users can expect after contacting, booking, buying, or submitting an inquiry.</p>
    <h2>Disclaimers</h2>
    <p>Document regulated, professional, medical, financial, legal, education, or industry-specific disclaimers where needed.</p>
    <h2>Contact</h2>
    <p>Provide a current contact route for legal questions.</p>
  </main>
</body>
</html>
"""


def render_accessibility_page(site_name: str) -> str:
    name = html.escape(site_name or "This website")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Accessibility | {name}</title>
</head>
<body>
  <main>
    <h1>Accessibility Statement</h1>
    <p><strong>Review required before publication.</strong> Replace this template with an honest statement that matches the site's tested accessibility status.</p>
    <h2>Target Standard</h2>
    <p>State the practical target, such as WCAG 2.2 AA, and list the pages or journeys tested.</p>
    <h2>Known Limitations</h2>
    <p>Document unresolved barriers, third-party embed limitations, PDFs, videos, or content that still needs improvement.</p>
    <h2>Feedback</h2>
    <p>Provide an email, phone, or form route for users who encounter accessibility barriers.</p>
    <h2>Testing</h2>
    <p>Record manual keyboard testing, screen reader checks, zoom checks, reduced-motion checks, and free automated tools used.</p>
  </main>
</body>
</html>
"""


def render_html_sitemap(root: Path, base_url: str | None, site_name: str) -> str:
    name = html.escape(site_name or "Static Site")
    links = []
    for path in iter_html_files(root):
        rel = rel_path(path, root)
        if rel == "404.html" or rel.endswith("/404.html"):
            continue
        href = "/" + rel
        if rel.endswith("index.html"):
            href = "/" + rel[: -len("index.html")]
        label = html.escape(guess_page_label(path.relative_to(root)))
        if base_url:
            href = page_url(root, path, base_url)
        links.append(f'      <li><a href="{html.escape(href, quote=True)}">{label}</a></li>')
    body_links = "\n".join(links) or "      <li><a href=\"/\">Home</a></li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sitemap | {name}</title>
  <meta name="description" content="Human-readable sitemap for {name}.">
</head>
<body>
  <main>
    <h1>Sitemap</h1>
    <nav aria-label="Sitemap">
      <ul>
{body_links}
      </ul>
    </nav>
  </main>
</body>
</html>
"""


def render_tracking_plan_template() -> str:
    return """# Analytics And Tracking Plan

Free/open-source-friendly static site tracking plan. Keep this file current with the deployed site.

## Tool
- Analytics tool:
- Self-hosted or hosted free tier:
- Cookie-free mode:
- Consent requirement:
- Dashboard owner:

## Primary Conversions
- [ ] form_submit
- [ ] booking_click
- [ ] quote_request
- [ ] whatsapp_click
- [ ] email_click
- [ ] phone_click

## Secondary Events
- [ ] cta_click
- [ ] form_start
- [ ] form_error
- [ ] outbound_click
- [ ] download_click
- [ ] scroll_depth
- [ ] faq_open
- [ ] video_play
- [ ] language_switch
- [ ] 404_view

## Privacy Rules
- [ ] No names, emails, phone numbers, addresses, payment data, form messages, health, legal, or financial details are sent to analytics.
- [ ] Failed form attempts are not counted as successful leads.
- [ ] CTA clicks are separated from confirmed form submissions.
- [ ] Tracking respects consent and matches the privacy policy.
"""


def render_launch_qa_template() -> str:
    return """# Launch QA Evidence

Use this as the human evidence file beside automated reports.

## Automated Reports
- [ ] JSON audit attached:
- [ ] Markdown audit attached:
- [ ] Fix dry-run reviewed:
- [ ] Fix write run reviewed:

## Manual Journeys
- [ ] Homepage to contact works.
- [ ] Service or offer page to contact works.
- [ ] Portfolio/case study to contact works where relevant.
- [ ] Blog/article to service/contact works where relevant.
- [ ] 404 recovery works.
- [ ] Mobile menu to contact works.

## Manual QA
- [ ] Keyboard navigation checked.
- [ ] 200% zoom checked.
- [ ] Mobile small/large checked.
- [ ] Tablet checked.
- [ ] Desktop/wide checked.
- [ ] Chrome, Safari, Firefox, and Edge checked where available.
- [ ] Forms submitted on live domain.
- [ ] Analytics events verified on live domain.
- [ ] Sitemap, robots, canonical, social preview, favicon, and 404 checked live.
"""


def render_monitoring_plan_template() -> str:
    return """# Monitoring And Maintenance Plan

## Owners
- Site owner:
- Repository owner:
- Domain/DNS owner:
- Hosting owner:
- Form recipient:
- Analytics owner:
- Emergency contact:

## Free/Open-Source-Friendly Monitoring
- [ ] Uptime for homepage and contact page.
- [ ] HTTPS certificate status.
- [ ] Domain expiry.
- [ ] Form delivery.
- [ ] Analytics page views and conversions.
- [ ] 404 paths.
- [ ] Broken links.
- [ ] Search indexing/sitemap status.
- [ ] Performance regression after releases.

## Review Schedule
- Weekly:
- Monthly:
- Quarterly:

## Incident Response
- Rollback process:
- DNS recovery:
- Form failure process:
- Secret exposure process:
- Broken launch process:
"""

def render_security_txt(site_name: str) -> str:
    contact = "mailto:security@example.com"
    return f"""Contact: {contact}
Preferred-Languages: en
Canonical: /.well-known/security.txt
Policy: /security-policy
# Replace the contact value and policy URL before publishing for {site_name or "this site"}.
"""


def write_file(path: Path, content: str, write: bool, force: bool, actions: list[FixAction]) -> None:
    if path.exists() and not force:
        actions.append(FixAction(rel_display(path), "skip existing file", False, "use --force to replace"))
        return
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    actions.append(FixAction(rel_display(path), "write file", write, "created" if not path.exists() or write else "planned"))


def rel_display(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def fix_site(
    root: Path,
    base_url: str | None,
    site_name: str,
    default_lang: str,
    write: bool,
    force: bool,
    scaffold_only: bool = False,
) -> list[FixAction]:
    root = root.resolve()
    actions: list[FixAction] = []
    preexisting_html_paths = set(iter_html_files(root))
    if base_url:
        write_file(root / "robots.txt", render_robots(base_url), write, force, actions)
    write_file(root / "404.html", render_404(site_name), write, force, actions)
    write_file(root / "_headers", render_headers(), write, force, actions)
    write_file(root / "security-headers.example", render_security_headers_example(), write, force, actions)
    write_file(root / "site.webmanifest", render_manifest(site_name), write, force, actions)
    write_file(root / "assets" / "css" / "a11y-base.css", render_a11y_css(), write, force, actions)
    write_file(root / "assets" / "js" / "consent-analytics.js", render_consent_js(), write, force, actions)
    write_file(root / "privacy.html", render_privacy_page(site_name), write, force, actions)
    if not any((root / name).exists() for name in {"cookie-policy.html", "cookies.html", "cookies/index.html"}):
        write_file(root / "cookie-policy.html", render_cookie_page(site_name), write, force, actions)
    write_file(root / "terms.html", render_terms_page(site_name), write, force, actions)
    write_file(root / "accessibility.html", render_accessibility_page(site_name), write, force, actions)
    write_file(root / "sitemap.html", render_html_sitemap(root, base_url, site_name), write, force, actions)
    write_file(root / "docs" / "analytics-tracking-plan.md", render_tracking_plan_template(), write, force, actions)
    write_file(root / "docs" / "launch-qa-evidence.md", render_launch_qa_template(), write, force, actions)
    write_file(root / "docs" / "monitoring-maintenance-plan.md", render_monitoring_plan_template(), write, force, actions)
    write_file(root / ".well-known" / "security.txt", render_security_txt(site_name), write, force, actions)
    if base_url:
        write_file(root / "sitemap.xml", render_sitemap(root, base_url), write, force, actions)

    if scaffold_only:
        return actions

    html_paths_to_update = iter_html_files(root)
    for path in html_paths_to_update:
        original = read_text(path)
        updated = update_html(original, path, root, base_url, site_name, default_lang)
        if updated != original:
            if write:
                if not force and path in preexisting_html_paths:
                    backup = root / ".site-quality-backups" / path.relative_to(root)
                    if not backup.exists():
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(path, backup)
                path.write_text(updated, encoding="utf-8")
            actions.append(
                FixAction(
                    rel_path(path, root),
                    "update html metadata/links/images",
                    write,
                    "doctype/lang/meta/canonical/target-blank/image loading where applicable",
                )
            )
    return actions


def print_fix_report(actions: list[FixAction], write: bool) -> None:
    mode = "written" if write else "planned"
    print(f"Fix actions {mode}: {len(actions)}")
    print()
    for action in actions:
        status = "written" if action.written else "dry-run"
        print(f"[{status}] {action.file}: {action.action}")
        if action.detail:
            print(f"  {action.detail}")


def load_config(path: Path | None) -> dict[str, str]:
    if not path:
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Could not load config {path}: {exc}") from exc


def normalize_base_url(value: str | None) -> str | None:
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("--base-url must be an absolute http or https URL")
    return value.rstrip("/")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit and safely fix static HTML/CSS/JS websites.")
    parser.add_argument("--config", type=Path, help="Optional JSON config with baseUrl, siteName, and defaultLang.")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Audit a static site folder.")
    audit.add_argument("root", type=Path)
    audit.add_argument("--base-url")
    audit.add_argument("--format", choices={"text", "json", "markdown"}, default="text")
    audit.add_argument("--out", type=Path, help="Write JSON report to this path.")
    audit.add_argument("--report-md", type=Path, help="Write a human-readable Markdown report to this path.")
    audit.add_argument("--fail-on", choices={"critical", "high", "medium", "low"}, help="Exit non-zero if any issue at or above this severity exists.")

    fix = sub.add_parser("fix", help="Preview or write safe mechanical fixes.")
    fix.add_argument("root", type=Path)
    fix.add_argument("--base-url")
    fix.add_argument("--site-name", default="")
    fix.add_argument("--default-lang", default="en")
    fix.add_argument("--write", action="store_true", help="Write changes. Without this flag, the command is dry-run only.")
    fix.add_argument("--force", action="store_true", help="Replace existing generated files and skip backups.")

    scaffold = sub.add_parser("scaffold", help="Create only support files such as sitemap, robots, headers, consent, and policy templates.")
    scaffold.add_argument("root", type=Path)
    scaffold.add_argument("--base-url")
    scaffold.add_argument("--site-name", default="")
    scaffold.add_argument("--default-lang", default="en")
    scaffold.add_argument("--write", action="store_true")
    scaffold.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args.config)

    base_url = normalize_base_url(getattr(args, "base_url", None) or config.get("baseUrl"))
    site_name = getattr(args, "site_name", "") or config.get("siteName", "")
    default_lang = getattr(args, "default_lang", "en") or config.get("defaultLang", "en")
    root = args.root.resolve()

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Target folder does not exist or is not a directory: {root}")

    if args.command == "audit":
        issues = audit_site(root, base_url)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            write_report(issues, args.out)
        if args.report_md:
            args.report_md.parent.mkdir(parents=True, exist_ok=True)
            args.report_md.write_text(render_markdown_report(issues, root, base_url), encoding="utf-8")
        if args.format == "json":
            print(json.dumps(report_payload(issues), indent=2))
        elif args.format == "markdown":
            print(render_markdown_report(issues, root, base_url))
        else:
            print_text_report(issues)
        if args.fail_on:
            threshold = severity_rank(args.fail_on)
            if any(severity_rank(issue.severity) <= threshold for issue in issues):
                return 1
        return 0

    if args.command == "fix":
        actions = fix_site(root, base_url, site_name, default_lang, args.write, args.force, scaffold_only=False)
        print_fix_report(actions, args.write)
        return 0

    if args.command == "scaffold":
        actions = fix_site(root, base_url, site_name, default_lang, args.write, args.force, scaffold_only=True)
        print_fix_report(actions, args.write)
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
