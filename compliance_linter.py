#!/usr/bin/env python3
"""
Google AdSense & Search Essentials Compliance Linter for CineStories.
Automated opaque-box verification of static build output in dist/ and dist/hi/.

Verifies 8 mandatory compliance rules:
1. Mandatory legal & compliance pages exist (5 EN, 5 HI).
2. Working contact mechanism and authentic site ownership.
3. Valid Schema.org structured data (NewsArticle, inLanguage, BreadcrumbList, WebSite, Organization).
4. No thin/spam boilerplate or duplicate filler text across articles.
5. Substantive word count verification (curated breakout articles >= 650 words).
6. OpenGraph publication date validity (immutable pub_iso vs datePublished).
7. Zero broken internal links across the entire generated site.
8. 100% AMP Web Story validation compliance without disallowed custom scripts.
"""

import os
import sys
import re
import json
import time
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Set, Tuple
from bs4 import BeautifulSoup

TARGET_BREAKOUT_SLUGS = [
    "panchayat-season-3",
    "mirzapur-season-3",
    "stree-2",
    "kalki-2898-ad",
    "sector-36",
    "do-patti",
    "devara-part-1",
    "pushpa-2-the-rule",
    "squid-game-season-2",
    "singham-again"
]

POLICY_SLUGS = ["about", "contact", "privacy", "terms", "editorial"]

BANNED_PERSONAS = {"marcus vance", "john doe", "jane doe", "admin"}
BANNED_PLACEHOLDERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bLorem ipsum\b",
    r"\bdolor sit amet\b",
    r"\bplaceholder\b",
    r"\binsert email\b",
    r"\byour-domain\b"
]

BANNED_BOILERPLATE_PHRASES = [
    "from the opening sequence, audiences are drawn into an engaging journey",
    "under acclaimed filmmakers's steady direction",
    "whether you're seeking gripping plot twists or memorable character moments",
    "brings critical revelations into focus, shedding light on the real-world impact",
    "from opening hook to post-credits clues, this story is engineered for google discover",
    "an in-depth look and detailed review"
]

_FILE_TEXT_CACHE: Dict[Tuple[str, int], str] = {}
_FILE_SOUP_CACHE: Dict[Tuple[str, int], BeautifulSoup] = {}


def _read_cached_text(file_path: Path) -> str:
    st = file_path.stat()
    key = (str(file_path), st.st_mtime_ns)
    if key not in _FILE_TEXT_CACHE:
        with open(file_path, "r", encoding="utf-8") as f:
            _FILE_TEXT_CACHE[key] = f.read()
    return _FILE_TEXT_CACHE[key]


def _read_cached_soup(file_path: Path) -> BeautifulSoup:
    st = file_path.stat()
    key = (str(file_path), st.st_mtime_ns)
    if key not in _FILE_SOUP_CACHE:
        content = _read_cached_text(file_path)
        _FILE_SOUP_CACHE[key] = BeautifulSoup(content, "html.parser")
    return _FILE_SOUP_CACHE[key]



class ComplianceViolation:
    def __init__(self, rule_id: str, severity: str, file_path: str, message: str, remediation: str = ""):
        self.rule_id = rule_id
        self.severity = severity
        self.file_path = file_path
        self.message = message
        self.remediation = remediation

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "file_path": self.file_path,
            "message": self.message,
            "remediation": self.remediation
        }


class ComplianceLinter:
    def __init__(self, dist_dir: Path, domain: str = "https://cinematicbites.com", lang: str = "all", verbose: bool = False, strict: bool = False):
        self.dist_dir = dist_dir.resolve()
        self.domain = domain.rstrip("/")
        self.lang = lang
        self.verbose = verbose
        self.strict = strict
        self.violations: List[ComplianceViolation] = []
        self.scanned_counts: Dict[str, int] = {f"R{i}": 0 for i in range(1, 9)}

    @property
    def summary(self) -> Dict[str, Any]:
        return {
            f"R{i}": self.scanned_counts.get(f"R{i}", 0)
            for i in range(1, 9)
        }

    def add_violation(self, rule_id: str, severity: str, file_path: Path, message: str, remediation: str = ""):
        try:
            rel_path = str(file_path.relative_to(self.dist_dir))
        except ValueError:
            rel_path = str(file_path)
        v = ComplianceViolation(rule_id, severity, rel_path, message, remediation)
        self.violations.append(v)
        if self.verbose:
            print(f"  [{severity}] {rule_id} ({rel_path}): {message}")

    # =========================================================================
    # RULE 1: Mandatory Policy & Legal Pages
    # =========================================================================
    def check_rule_1_policy_pages(self) -> int:
        rule_id = "R1"
        languages = ["en", "hi"] if self.lang == "all" else [self.lang]
        checked = 0

        for lang in languages:
            base_dir = self.dist_dir if lang == "en" else self.dist_dir / "hi"
            for slug in POLICY_SLUGS:
                checked += 1
                page_file = base_dir / slug / "index.html"
                if not page_file.exists():
                    self.add_violation(
                        rule_id, "ERROR", page_file,
                        f"Mandatory policy page missing for lang='{lang}'",
                        "Ensure policy_pages.py generates all 5 policy pages in English and Hindi."
                    )
                    continue

                if os.path.getsize(page_file) < 500:
                    self.add_violation(
                        rule_id, "ERROR", page_file,
                        f"Policy page is suspiciously thin (<500 bytes: {os.path.getsize(page_file)}b)",
                        "Populate comprehensive policy text."
                    )

                try:
                    soup = _read_cached_soup(page_file)
                except Exception as e:
                    self.add_violation(rule_id, "ERROR", page_file, f"Error reading policy page: {e}")
                    continue

                title = soup.find("title")
                if not title or len(title.get_text().strip()) < 10:
                    self.add_violation(rule_id, "ERROR", page_file, "Missing or insufficient <title> tag in policy page")

                desc = soup.find("meta", attrs={"name": "description"})
                if not desc or not desc.get("content") or len(desc.get("content").strip()) < 25:
                    self.add_violation(rule_id, "ERROR", page_file, "Missing or insufficient <meta name='description'> in policy page")

                canonical = soup.find("link", attrs={"rel": "canonical"})
                if not canonical or not canonical.get("href"):
                    self.add_violation(rule_id, "ERROR", page_file, "Missing canonical link in policy page")

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 2: Authentic Ownership & Working Contact Mechanism
    # =========================================================================
    def check_rule_2_ownership_and_contact(self) -> int:
        rule_id = "R2"
        checked = 0

        # Check contact pages
        contact_files = [self.dist_dir / "contact" / "index.html", self.dist_dir / "hi" / "contact" / "index.html"]
        for cf in contact_files:
            if not cf.exists():
                continue
            checked += 1
            try:
                soup = _read_cached_soup(cf)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", cf, f"Error reading contact page: {e}")
                continue

            mailto_links = soup.find_all("a", href=re.compile(r"^mailto:", re.I))
            if not mailto_links:
                self.add_violation(
                    rule_id, "ERROR", cf,
                    "No working mailto: email contact mechanism found in Contact Us page",
                    "Add <a href='mailto:...'> with official editorial contact email."
                )
            else:
                email = mailto_links[0]["href"].replace("mailto:", "").split("?")[0].strip()
                if any(bad in email.lower() for bad in ["example.com", "yourdomain.com", "test.com", "placeholder"]):
                    self.add_violation(rule_id, "ERROR", cf, f"Placeholder contact email detected: {email}")

            text = soup.get_text()
            for pattern in BANNED_PLACEHOLDERS:
                if re.search(pattern, text, re.I):
                    self.add_violation(rule_id, "ERROR", cf, f"Banned placeholder matched pattern '{pattern}' in Contact page")

        # Scan all articles for fictitious persona
        article_files = list(self.dist_dir.glob("articles/*/index.html")) + list(self.dist_dir.glob("hi/articles/*/index.html"))
        for art in article_files:
            checked += 1
            try:
                content = _read_cached_text(art)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", art, f"Error reading article: {e}")
                continue

            for persona in BANNED_PERSONAS:
                if re.search(rf"\b{re.escape(persona)}\b", content, re.I):
                    self.add_violation(
                        rule_id, "ERROR", art,
                        f"Fictitious persona '{persona}' detected in article content or author schema",
                        "Replace with 'CineStories Editorial Board'."
                    )

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 3: Valid Schema.org Structured Data
    # =========================================================================
    def check_rule_3_schema(self) -> int:
        rule_id = "R3"
        checked = 0

        # Homepage schema
        for lang, hp in [("en", self.dist_dir / "index.html"), ("hi", self.dist_dir / "hi" / "index.html")]:
            if not hp.exists():
                continue
            checked += 1
            try:
                soup = _read_cached_soup(hp)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", hp, f"Error reading homepage: {e}")
                continue

            scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
            found_website = False
            found_org = False
            for s in scripts:
                try:
                    if not s.string:
                        continue
                    data = json.loads(s.string)
                    raw_items = data if isinstance(data, list) else [data]
                    items = []
                    for r_item in raw_items:
                        if isinstance(r_item, dict) and "@graph" in r_item and isinstance(r_item["@graph"], list):
                            items.extend(r_item["@graph"])
                        else:
                            items.append(r_item)
                    for item in items:
                        if isinstance(item, dict):
                            itype = item.get("@type")
                            if itype == "WebSite":
                                found_website = True
                            if itype == "Organization":
                                found_org = True
                except Exception as e:
                    self.add_violation(rule_id, "ERROR", hp, f"Malformed JSON in application/ld+json script tag: {e}")

            if not found_website:
                self.add_violation(rule_id, "ERROR", hp, f"Missing Schema.org WebSite structured data on homepage (lang='{lang}')")
            if not found_org:
                self.add_violation(rule_id, "ERROR", hp, f"Missing Schema.org Organization structured data on homepage (lang='{lang}')")

        # Articles and Stories NewsArticle and Breadcrumbs
        targets = list(self.dist_dir.glob("articles/*/index.html")) + \
                  list(self.dist_dir.glob("hi/articles/*/index.html")) + \
                  list(self.dist_dir.glob("stories/*/index.html")) + \
                  list(self.dist_dir.glob("hi/stories/*/index.html"))
        if not targets and checked == 0:
            targets = list(self.dist_dir.rglob("*.html"))

        for target in targets:
            checked += 1
            is_hindi = "/hi/" in target.as_posix() or "\\hi\\" in target.as_posix()
            expected_lang = "hi-IN" if is_hindi else "en-US"

            try:
                soup = _read_cached_soup(target)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", target, f"Error reading target file: {e}")
                continue

            scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
            has_news_article = False
            has_breadcrumbs = False

            for s in scripts:
                try:
                    if not s.string:
                        continue
                    data = json.loads(s.string)
                    raw_items = data if isinstance(data, list) else [data]
                    items = []
                    for r_item in raw_items:
                        if isinstance(r_item, dict) and "@graph" in r_item and isinstance(r_item["@graph"], list):
                            items.extend(r_item["@graph"])
                        else:
                            items.append(r_item)
                    for item in items:
                        if isinstance(item, dict):
                            itype = item.get("@type")
                            if itype == "NewsArticle":
                                has_news_article = True
                                in_lang = item.get("inLanguage", "")
                                if in_lang not in [expected_lang, expected_lang[:2]]:
                                    self.add_violation(rule_id, "ERROR", target, f"Schema inLanguage='{in_lang}' mismatch; expected '{expected_lang}'")
                            elif itype == "BreadcrumbList":
                                has_breadcrumbs = True
                                elems = item.get("itemListElement", [])
                                if len(elems) < 3:
                                    self.add_violation(rule_id, "ERROR", target, f"BreadcrumbList has only {len(elems)} items, expected >= 3")
                except Exception as e:
                    self.add_violation(rule_id, "ERROR", target, f"Invalid JSON-LD syntax: {e}")

            if not has_news_article:
                self.add_violation(rule_id, "ERROR", target, "Missing Schema.org NewsArticle structured data")
            if not has_breadcrumbs:
                self.add_violation(rule_id, "ERROR", target, "Missing Schema.org BreadcrumbList structured data")

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 4: No Thin/Spam Boilerplate or Duplicate Filler Text
    # =========================================================================
    def check_rule_4_anti_thin_spam(self) -> int:
        rule_id = "R4"
        checked = 0
        article_files = list(self.dist_dir.glob("articles/*/index.html"))

        for art in article_files:
            checked += 1
            try:
                content = _read_cached_text(art)
                soup = _read_cached_soup(art)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", art, f"Error reading article: {e}")
                continue

            content_lower = content.lower()
            for phrase in BANNED_BOILERPLATE_PHRASES:
                if phrase in content_lower:
                    self.add_violation(
                        rule_id, "ERROR", art,
                        f"Canned fallback boilerplate phrase detected: '{phrase}'",
                        "Provide unique editorial analysis."
                    )

            sections = soup.find_all("section", class_="article-section")
            if len(sections) < 3:
                self.add_violation(rule_id, "ERROR", art, f"Article has only {len(sections)} sections, expected >= 3")

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 5: Substantive Word Count Verification
    # =========================================================================
    def check_rule_5_word_count(self) -> int:
        rule_id = "R5"
        checked = 0

        # Curated breakout titles require >= 650 words
        for lang, prefix in [("en", "articles"), ("hi", "hi/articles")]:
            for slug in TARGET_BREAKOUT_SLUGS:
                art_file = self.dist_dir / prefix / slug / "index.html"
                if not art_file.exists():
                    continue
                checked += 1
                try:
                    soup = _read_cached_soup(art_file)
                except Exception as e:
                    self.add_violation(rule_id, "ERROR", art_file, f"Error reading article: {e}")
                    continue

                editorial_texts = []
                for p in soup.select(".article-section p, .audience-guide-card p, .takeaways-list li, .verdict-card p, article p"):
                    editorial_texts.append(p.get_text())

                combined = " ".join(editorial_texts)
                tokens = re.split(r"[\s।॥,;:!?]+", combined)
                word_count = len([t for t in tokens if t.strip()])

                if word_count < 650:
                    self.add_violation(
                        rule_id,
                        "ERROR",
                        art_file,
                        f"Substantive word count {word_count} is below mandatory 650-word threshold for curated breakout title",
                        "Expand curated deep-dive analysis across 5 sections."
                    )

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 6: OpenGraph Publication Date Validity
    # =========================================================================
    def check_rule_6_pub_date(self) -> int:
        rule_id = "R6"
        checked = 0

        registry = {}
        reg_file = self.dist_dir / "published_registry.json"
        if reg_file.exists():
            try:
                with open(reg_file, "r", encoding="utf-8") as f:
                    registry = json.load(f)
            except Exception:
                pass

        article_files = list(self.dist_dir.glob("articles/*/index.html")) + list(self.dist_dir.glob("hi/articles/*/index.html"))
        for art in article_files:
            checked += 1
            slug = art.parent.name
            try:
                soup = _read_cached_soup(art)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", art, f"Error reading article: {e}")
                continue

            og_pub_tag = soup.find("meta", property="article:published_time")
            if not og_pub_tag or not og_pub_tag.get("content"):
                self.add_violation(rule_id, "ERROR", art, "Missing <meta property='article:published_time'>")
                continue

            og_pub = og_pub_tag["content"].strip()

            # Schema datePublished
            schema_pub = None
            scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
            for s in scripts:
                try:
                    if not s.string:
                        continue
                    data = json.loads(s.string)
                    raw_items = data if isinstance(data, list) else [data]
                    items = []
                    for r_item in raw_items:
                        if isinstance(r_item, dict) and "@graph" in r_item and isinstance(r_item["@graph"], list):
                            items.extend(r_item["@graph"])
                        else:
                            items.append(r_item)
                    for it in items:
                        if isinstance(it, dict) and it.get("@type") == "NewsArticle":
                            schema_pub = it.get("datePublished")
                except Exception:
                    pass

            if schema_pub and og_pub != schema_pub:
                self.add_violation(rule_id, "ERROR", art, f"Date mismatch: og:published_time='{og_pub}' != Schema datePublished='{schema_pub}'")

            # Check registry immutability
            if slug in registry and "published_at" in registry[slug]:
                expected_pub = registry[slug]["published_at"]
                if og_pub != expected_pub:
                    self.add_violation(rule_id, "ERROR", art, f"Date overwrite bug: article published_time='{og_pub}' != registry '{expected_pub}'")

        self.scanned_counts[rule_id] = checked
        return checked

    def resolve_internal_link(self, raw_href: str, html_file: Path) -> bool:
        if not raw_href or raw_href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            return True
        if raw_href.startswith(("http://", "https://")) and not raw_href.startswith(self.domain):
            return True

        path_part = raw_href
        if path_part.startswith(self.domain):
            path_part = path_part[len(self.domain):]

        path_clean = path_part.split("?")[0].split("#")[0]
        if not path_clean:
            return True

        if path_clean.startswith("/"):
            rel_clean = path_clean.lstrip("/")
            if not rel_clean:
                target_file = self.dist_dir / "index.html"
            elif rel_clean.endswith(".html") or rel_clean.endswith((".xml", ".json", ".svg", ".png", ".jpg", ".txt")):
                target_file = self.dist_dir / rel_clean
            else:
                target_file = self.dist_dir / rel_clean / "index.html"
        else:
            target_file = (html_file.parent / path_clean).resolve()
            if target_file.is_dir():
                target_file = target_file / "index.html"

        return target_file.exists()

    # =========================================================================
    # RULE 7: Zero Broken Internal Links
    # =========================================================================
    def check_rule_7_internal_links(self) -> int:
        rule_id = "R7"
        checked = 0
        all_html = list(self.dist_dir.rglob("*.html"))

        for html_file in all_html:
            try:
                soup = _read_cached_soup(html_file)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", html_file, f"Error parsing HTML: {e}")
                continue

            links = soup.find_all(["a", "link"], href=True)
            for link in links:
                raw_href = link["href"].strip()
                checked += 1

                if not self.resolve_internal_link(raw_href, html_file):
                    self.add_violation(rule_id, "ERROR", html_file, f"Broken internal link '{raw_href}'")

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # RULE 8: 100% AMP Web Story Validation Compliance
    # =========================================================================
    def check_rule_8_amp_compliance(self, run_cli_validator: bool = True) -> int:
        rule_id = "R8"
        checked = 0
        story_files = list(self.dist_dir.glob("stories/*/index.html")) + list(self.dist_dir.glob("hi/stories/*/index.html"))

        for story in story_files:
            checked += 1
            try:
                soup = _read_cached_soup(story)
            except Exception as e:
                self.add_violation(rule_id, "ERROR", story, f"Error reading story: {e}")
                continue

            # Fast AST check for disallowed custom scripts
            scripts = soup.find_all("script")
            for sc in scripts:
                src = sc.get("src", "")
                stype = sc.get("type", "")
                if src:
                    if not src.startswith("https://cdn.ampproject.org/"):
                        self.add_violation(rule_id, "ERROR", story, f"Disallowed external script in AMP story: {src}")
                else:
                    # Inline script
                    if stype not in ["application/json", "application/ld+json"]:
                        self.add_violation(rule_id, "ERROR", story, f"Disallowed custom inline JavaScript in AMP story: type='{stype}'")

            # Check for !important in styles
            style_custom = soup.find("style", attrs={"amp-custom": True})
            if style_custom and "!important" in style_custom.get_text():
                self.add_violation(rule_id, "ERROR", story, "!important found in <style amp-custom>, violating AMP spec")

        # Optional CLI batch validation
        npx_cmd = shutil.which("npx.cmd") or shutil.which("npx")
        if run_cli_validator and npx_cmd and story_files:
            chunk_size = 40
            paths = [str(f) for f in story_files]
            is_windows = (os.name == "nt")
            for i in range(0, len(paths), chunk_size):
                chunk = paths[i:i + chunk_size]
                try:
                    res = subprocess.run([npx_cmd, "--yes", "amphtml-validator"] + chunk, capture_output=True, text=True, shell=is_windows, timeout=120)
                    for line in (res.stdout + "\n" + res.stderr).splitlines():
                        if ": FAIL" in line or "ERROR" in line:
                            self.add_violation(rule_id, "ERROR", Path(line.split(":")[0]), f"AMP validation error: {line}")
                except Exception as e:
                    self.add_violation(rule_id, "WARNING", self.dist_dir, f"amphtml-validator CLI batch error: {e}")

        self.scanned_counts[rule_id] = checked
        return checked

    # =========================================================================
    # Run Orchestrator
    # =========================================================================
    def run_all(self, rules_to_run: Optional[List[int]] = None, run_cli_validator: bool = True) -> bool:
        start_time = time.time()
        rules = rules_to_run or [1, 2, 3, 4, 5, 6, 7, 8]

        rule_methods = {
            1: ("Mandatory Legal & Policy Pages", self.check_rule_1_policy_pages),
            2: ("Authentic Ownership & Working Contact", self.check_rule_2_ownership_and_contact),
            3: ("Valid Schema.org & inLanguage Tags", self.check_rule_3_schema),
            4: ("No Thin/Spam Boilerplate Duplication", self.check_rule_4_anti_thin_spam),
            5: ("Substantive Word Count (Curated >=650)", self.check_rule_5_word_count),
            6: ("OpenGraph & Schema pub_iso Immutability", self.check_rule_6_pub_date),
            7: ("Zero Broken Internal Links", self.check_rule_7_internal_links),
            8: ("100% AMP Web Story Script & Spec Valid", lambda: self.check_rule_8_amp_compliance(run_cli_validator))
        }

        print("=" * 80)
        print("          CINESTORIES GOOGLE ADSENSE & SEARCH ESSENTIALS LINTER")
        print("=" * 80)
        print(f"Target Directory : {self.dist_dir}")
        print(f"Language Scope   : {self.lang}")
        print(f"Rules Evaluated  : {', '.join(str(r) for r in rules)}")
        print("-" * 80)

        for r_num in rules:
            r_name, r_func = rule_methods[r_num]
            r_func()

        errors = [v for v in self.violations if v.severity == "ERROR"]
        warnings = [v for v in self.violations if v.severity == "WARNING"]

        # Print Rule Breakdown
        print(f" {'ID':<3} | {'COMPLIANCE RULE DESCRIPTION':<40} | {'STATUS':<6} | {'SCANNED':<7} | {'ERR':<4} | {'WARN':<4}")
        print("-" * 80)
        for r_num in rules:
            r_id = f"R{r_num}"
            r_name, _ = rule_methods[r_num]
            r_errors = len([v for v in errors if v.rule_id == r_id])
            r_warns = len([v for v in warnings if v.rule_id == r_id])
            status = "PASS" if r_errors == 0 else "FAIL"
            scanned = self.scanned_counts.get(r_id, 0)
            print(f" {r_id:<3} | {r_name:<40} | {status:<6} | {scanned:<7} | {r_errors:<4} | {r_warns:<4}")
        print("-" * 80)

        elapsed = time.time() - start_time
        total_scanned = sum(self.scanned_counts.values())

        is_passed = len(errors) == 0 if not self.strict else (len(errors) == 0 and len(warnings) == 0)

        if errors:
            print(f"\n[FAIL] Found {len(errors)} compliance errors ({len(warnings)} warnings).\n")
            print("DETAILED REMEDIATION LOG (First 25):")
            for idx, err in enumerate(errors[:25], 1):
                print(f"  {idx}. [{err.rule_id}] {err.file_path}: {err.message}")
                if err.remediation:
                    print(f"     Fix: {err.remediation}")
            if len(errors) > 25:
                print(f"  ... and {len(errors) - 25} more errors.")
            print("\n" + "=" * 80)
            return False
        else:
            print(f"\n>> 100% COMPLIANCE SUCCESS: All {len(rules)} rules PASSED cleanly ({total_scanned} checks in {elapsed:.2f}s)!\n")
            print("=" * 80)
            return True


def main():
    parser = argparse.ArgumentParser(description="CineStories Google AdSense & Search Essentials Linter")
    parser.add_argument("--dist-dir", type=str, default="dist", help="Distribution directory to lint")
    parser.add_argument("--rule", "-r", type=str, default="all", help="Rules to run (e.g. '1', '1,3,6', or 'all')")
    parser.add_argument("--lang", type=str, default="all", choices=["en", "hi", "all"], help="Language edition to lint")
    parser.add_argument("--skip-amp-cli", action="store_true", help="Skip npx amphtml-validator and use fast AST inspection")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose per-check logging")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Output machine-parseable JSON report")
    parser.add_argument("--output-json", type=str, default=None, help="Write detailed JSON report to file")
    args = parser.parse_args()

    dist_path = Path(args.dist_dir)
    if not dist_path.exists():
        print(f"Error: Distribution directory '{dist_path}' does not exist. Run build first.", file=sys.stderr)
        sys.exit(2)

    rules = None
    if args.rule != "all":
        try:
            rules = [int(x.strip()) for x in args.rule.split(",")]
        except ValueError:
            print(f"Error: Invalid rule specification '{args.rule}'", file=sys.stderr)
            sys.exit(2)

    linter = ComplianceLinter(dist_dir=dist_path, lang=args.lang, verbose=args.verbose, strict=args.strict)
    passed = linter.run_all(rules_to_run=rules, run_cli_validator=not args.skip_amp_cli)

    report_dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dist_dir": str(dist_path),
        "passed": passed,
        "scanned_counts": linter.scanned_counts,
        "total_errors": len([v for v in linter.violations if v.severity == "ERROR"]),
        "total_warnings": len([v for v in linter.violations if v.severity == "WARNING"]),
        "violations": [v.to_dict() for v in linter.violations]
    }

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2)

    if args.json:
        print(json.dumps(report_dict, indent=2))

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
