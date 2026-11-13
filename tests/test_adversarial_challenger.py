"""
Adversarial Verification Suite for CineStories Test Infrastructure & Linter
Empirical checks for:
1. CLI parameter fuzzing and unhandled exceptions
2. ComplianceLinter rule sensitivity (R1 - R8)
3. GeoRoutingSimulator edge cases, type corruption, and redirect paths
4. Master E2E runner orchestration and stress test wiring
"""

import os
import sys
import json
import re
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from compliance_linter import ComplianceLinter, ComplianceViolation
from test_geo_routing_i18n import GeoRoutingSimulator


class TestComplianceLinterSensitivity(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dist_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_r1_missing_policy_pages(self):
        linter = ComplianceLinter(dist_dir=self.dist_path, lang="en")
        linter.check_rule_1_policy_pages()
        errors = [v for v in linter.violations if v.rule_id == "R1"]
        self.assertEqual(len(errors), 5)
        self.assertTrue(all("Mandatory policy page missing" in e.message for e in errors))

    def test_r1_thin_policy_page(self):
        about_dir = self.dist_path / "about"
        about_dir.mkdir(parents=True)
        (about_dir / "index.html").write_text("<html><head><title>About Us Page Title</title><meta name='description' content='Valid description with sufficient characters here.'><link rel='canonical' href='/about/'></head><body>Thin</body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path, lang="en")
        linter.check_rule_1_policy_pages()
        thin_errors = [v for v in linter.violations if "suspiciously thin" in v.message]
        self.assertEqual(len(thin_errors), 1)

    def test_r2_missing_mailto_and_placeholder_email(self):
        contact_dir = self.dist_path / "contact"
        contact_dir.mkdir(parents=True)
        # Without mailto
        (contact_dir / "index.html").write_text("<html><body>Contact Us</body></html>", encoding="utf-8")
        linter1 = ComplianceLinter(dist_dir=self.dist_path)
        linter1.check_rule_2_ownership_and_contact()
        self.assertTrue(any("No working mailto:" in v.message for v in linter1.violations))

        # With placeholder email
        (contact_dir / "index.html").write_text("<html><body><a href='mailto:admin@example.com'>Email</a></body></html>", encoding="utf-8")
        linter2 = ComplianceLinter(dist_dir=self.dist_path)
        linter2.check_rule_2_ownership_and_contact()
        self.assertTrue(any("Placeholder contact email" in v.message for v in linter2.violations))

    def test_r2_banned_persona_in_article(self):
        art_dir = self.dist_path / "articles" / "test-film"
        art_dir.mkdir(parents=True)
        (art_dir / "index.html").write_text("<html><body><p>Review by Marcus Vance</p></body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path)
        linter.check_rule_2_ownership_and_contact()
        persona_errs = [v for v in linter.violations if "marcus vance" in v.message]
        self.assertEqual(len(persona_errs), 1)

    def test_r3_homepage_missing_website_org_schema(self):
        hp = self.dist_path / "index.html"
        hp.write_text("<html><head></head><body>CineStories</body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path, lang="en")
        linter.check_rule_3_schema()
        r3_errs = [v for v in linter.violations if v.rule_id == "R3"]
        self.assertTrue(any("Missing Schema.org WebSite" in v.message for v in r3_errs))
        self.assertTrue(any("Missing Schema.org Organization" in v.message for v in r3_errs))

    def test_r3_article_missing_news_article_and_breadcrumbs(self):
        art = self.dist_path / "articles" / "film1" / "index.html"
        art.parent.mkdir(parents=True)
        art.write_text("<html><head></head><body>Film content</body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path, lang="en")
        linter.check_rule_3_schema()
        self.assertTrue(any("Missing Schema.org NewsArticle" in v.message for v in linter.violations))
        self.assertTrue(any("Missing Schema.org BreadcrumbList" in v.message for v in linter.violations))

    def test_r3_inlanguage_mismatch(self):
        art = self.dist_path / "articles" / "film1" / "index.html"
        art.parent.mkdir(parents=True)
        schema_json = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "inLanguage": "fr-FR"
        }
        art.write_text(f"<html><head><script type='application/ld+json'>{json.dumps(schema_json)}</script></head><body></body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path, lang="en")
        linter.check_rule_3_schema()
        self.assertTrue(any("Schema inLanguage='fr-FR' mismatch" in v.message for v in linter.violations))

    def test_r4_banned_boilerplate_and_section_count(self):
        art = self.dist_path / "articles" / "film1" / "index.html"
        art.parent.mkdir(parents=True)
        art.write_text("<html><body>under acclaimed filmmakers's steady direction<section class='article-section'>S1</section></body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path)
        linter.check_rule_4_anti_thin_spam()
        self.assertTrue(any("Canned fallback boilerplate phrase" in v.message for v in linter.violations))
        self.assertTrue(any("has only 1 sections, expected >= 3" in v.message for v in linter.violations))

    def test_r5_breakout_article_word_count_below_650(self):
        art = self.dist_path / "articles" / "stree-2" / "index.html"
        art.parent.mkdir(parents=True)
        art.write_text("<html><body><article><p>Short paragraph with twenty words only here to test threshold.</p></article></body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path)
        linter.check_rule_5_word_count()
        self.assertTrue(any("below mandatory 650-word threshold" in v.message for v in linter.violations))

    def test_r6_date_mismatch_and_missing_og_pub(self):
        art = self.dist_path / "articles" / "film1" / "index.html"
        art.parent.mkdir(parents=True)
        # Missing og tag
        art.write_text("<html><head></head><body></body></html>", encoding="utf-8")
        linter1 = ComplianceLinter(dist_dir=self.dist_path)
        linter1.check_rule_6_pub_date()
        self.assertTrue(any("Missing <meta property='article:published_time'>" in v.message for v in linter1.violations))

        # Mismatch with schema datePublished
        art.write_text("<html><head><meta property='article:published_time' content='2026-01-01T00:00:00Z'><script type='application/ld+json'>{\"@type\": \"NewsArticle\", \"datePublished\": \"2026-02-01T00:00:00Z\"}</script></head><body></body></html>", encoding="utf-8")
        linter2 = ComplianceLinter(dist_dir=self.dist_path)
        linter2.check_rule_6_pub_date()
        self.assertTrue(any("Date mismatch:" in v.message for v in linter2.violations))

    def test_r7_broken_internal_links(self):
        hp = self.dist_path / "index.html"
        hp.write_text("<html><body><a href='/non-existent-page/'>Broken</a><a href='missing.html'>Also Broken</a></body></html>", encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path)
        linter.check_rule_7_internal_links()
        broken = [v for v in linter.violations if v.rule_id == "R7"]
        self.assertEqual(len(broken), 2)

    def test_r8_amp_story_disallowed_scripts_and_important(self):
        story = self.dist_path / "stories" / "story1" / "index.html"
        story.parent.mkdir(parents=True)
        story.write_text("""
        <html>
        <head>
            <style amp-custom>p { font-size: 16px !important; }</style>
            <script src="https://evil-analytics.com/tracker.js"></script>
            <script>var bad = 1;</script>
        </head>
        <body></body>
        </html>
        """, encoding="utf-8")
        linter = ComplianceLinter(dist_dir=self.dist_path)
        linter.check_rule_8_amp_compliance(run_cli_validator=False)
        r8_errs = [v for v in linter.violations if v.rule_id == "R8"]
        self.assertTrue(any("Disallowed external script" in v.message for v in r8_errs))
        self.assertTrue(any("Disallowed custom inline JavaScript" in v.message for v in r8_errs))
        self.assertTrue(any("!important found in <style amp-custom>" in v.message for v in r8_errs))


class TestGeoRoutingSimulatorDefects(unittest.TestCase):
    """Adversarial stress-testing of GeoRoutingSimulator."""

    def test_none_value_handling_crash_audit(self):
        """Verifies whether None in input dictionaries crashes the simulator."""
        input_corruptions = [
            ("query_params simulate_geo=None", {"query_params": {"simulate_geo": None}}),
            ("query_params lang=None", {"query_params": {"lang": None}}),
            ("local_storage cinestories_lang_manual=None", {"local_storage": {"cinestories_lang_manual": None}}),
            ("cookies cinestories_lang_manual=None", {"cookies": {"cinestories_lang_manual": None}}),
            ("edge_headers CF-IPCountry=None", {"edge_headers": {"CF-IPCountry": None}}),
            ("client_heuristics timezone=None", {"client_heuristics": {"timezone": None}}),
            ("client_heuristics languages=None", {"client_heuristics": {"languages": None}}),
            ("current_path=None", {"current_path": None}),
        ]
        crashes = []
        for desc, kwargs in input_corruptions:
            try:
                GeoRoutingSimulator.resolve_language(**kwargs)
            except Exception as e:
                crashes.append((desc, type(e).__name__, str(e)))

        print(f"\n[GEO SIMULATOR AUDIT] None-value crashes detected: {len(crashes)} of {len(input_corruptions)}")
        for desc, err_type, err_msg in crashes:
            print(f"  - {desc}: {err_type} - {err_msg}")

        # Documenting that these crashes exist as findings
        self.assertGreater(len(crashes), 0, "Expected crashes on unhandled None values")

    def test_boolean_type_corruption_crash_audit(self):
        """Verifies whether parsed boolean in cookies/storage crashes the simulator."""
        try:
            GeoRoutingSimulator.resolve_language(cookies={"cinestories_lang_manual": True})
            crashed = False
        except AttributeError:
            crashed = True
        self.assertTrue(crashed, "Expected AttributeError on boolean cookies/storage value")

    def test_relative_path_redirect_missing_slash_audit(self):
        """Verifies path calculation bug when current_path lacks leading slash."""
        res = GeoRoutingSimulator.resolve_language(
            query_params={"simulate_geo": "IN"},
            current_path="articles/stree-2/"
        )
        self.assertEqual(res["target_path"], "/hiarticles/stree-2/", "Confirming missing slash defect")


class TestComplianceLinterCliDefects(unittest.TestCase):
    """Adversarial testing of ComplianceLinter CLI."""

    def test_unhandled_keyerror_on_out_of_range_rule(self):
        linter = ComplianceLinter(dist_dir=Path("dist"))
        with self.assertRaises(KeyError):
            linter.run_all(rules_to_run=[99], run_cli_validator=False)

    def test_unhandled_keyerror_on_zero_rule(self):
        linter = ComplianceLinter(dist_dir=Path("dist"))
        with self.assertRaises(KeyError):
            linter.run_all(rules_to_run=[0], run_cli_validator=False)


if __name__ == "__main__":
    unittest.main()
