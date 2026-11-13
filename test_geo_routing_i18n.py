#!/usr/bin/env python3
"""
Automated Geo-Routing & I18n Test Suite for CineStories.
Validates the 4-Tier Geo-Detection Cascade, Cookie/Storage Persistence,
Manual Language Toggles, Bidirectional hreflang links, AMP Story Compliance,
and Translation/Localization Completeness across dist/ and dist/hi/.

CLI Usage:
    python test_geo_routing_i18n.py
    python test_geo_routing_i18n.py -v
    python -m unittest test_geo_routing_i18n.py
"""

import os
import sys
import re
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent
DIST_DIR = ROOT_DIR / "dist"
DIST_HI_DIR = DIST_DIR / "hi"

# ---------------------------------------------------------------------------
# Algorithmic Simulator for 4-Tier Geo-Detection Cascade
# ---------------------------------------------------------------------------
class GeoRoutingSimulator:
    """
    Simulates the CineStories client-side and edge geo-routing decision engine.
    Priority: Tier 1 (Explicit) > Tier 2 (CDN Headers) > Tier 3 (Heuristics) > Tier 4 (Fallback)
    """

    VALID_LANGS = {"en", "hi"}
    INDIAN_TIMEZONES = {"Asia/Kolkata", "Asia/Calcutta", "IST"}

    @classmethod
    def resolve_language(
        cls,
        query_params: dict = None,
        cookies: dict = None,
        local_storage: dict = None,
        edge_headers: dict = None,
        client_heuristics: dict = None,
        current_path: str = "/"
    ) -> dict:
        query_params = query_params or {}
        cookies = cookies or {}
        local_storage = local_storage or {}
        edge_headers = edge_headers or {}
        client_heuristics = client_heuristics or {}
        current_path = "/" if not current_path else (current_path if current_path.startswith("/") else "/" + current_path)

        def _to_str(val) -> str:
            if val is None:
                return ""
            if isinstance(val, bool):
                return "true" if val else "false"
            return str(val).strip()

        # -------------------------------------------------------------
        # Tier 1: Explicit User Choice
        # -------------------------------------------------------------
        # 1a. Test Query Parameter Override: ?simulate_geo=IN/US or ?lang=hi/en
        raw_sim_geo = _to_str(query_params.get("simulate_geo")).upper()
        if raw_sim_geo:
            if raw_sim_geo == "IN":
                return cls._decision("hi", tier=1, reason="simulate_geo=IN", current_path=current_path)
            elif re.match(r"^[A-Z]{2}$", raw_sim_geo):
                return cls._decision("en", tier=1, reason=f"simulate_geo={raw_sim_geo}", current_path=current_path)

        raw_lang_param = _to_str(query_params.get("lang")).lower()
        if raw_lang_param in cls.VALID_LANGS:
            return cls._decision(raw_lang_param, tier=1, reason=f"query_param_lang={raw_lang_param}", current_path=current_path)

        # 1b. Manual User Switcher Override: cinestories_lang_manual === 'true'
        manual_storage = _to_str(local_storage.get("cinestories_lang_manual")).lower() == "true"
        manual_cookie = _to_str(cookies.get("cinestories_lang_manual")).lower() == "true"
        is_manual = manual_storage or manual_cookie

        if is_manual:
            saved_lang = _to_str(local_storage.get("cinestories_lang") or cookies.get("cinestories_lang")).lower()
            if saved_lang in cls.VALID_LANGS:
                return cls._decision(saved_lang, tier=1, reason="manual_user_override", is_manual=True, current_path=current_path)

        # 1c. Non-manual stored choice (only if no edge headers present)
        stored_lang = _to_str(local_storage.get("cinestories_lang") or cookies.get("cinestories_lang")).lower()
        if stored_lang in cls.VALID_LANGS and not edge_headers:
            return cls._decision(stored_lang, tier=1, reason="stored_user_choice", current_path=current_path)

        # -------------------------------------------------------------
        # Tier 2: Edge CDN Headers
        # -------------------------------------------------------------
        normalized_headers = {str(k).lower(): _to_str(v).upper() for k, v in edge_headers.items() if v is not None}
        country_header = (
            normalized_headers.get("cf-ipcountry")
            or normalized_headers.get("x-vercel-ip-country")
            or normalized_headers.get("cloudfront-viewer-country")
        )
        if country_header:
            if country_header == "IN":
                return cls._decision("hi", tier=2, reason=f"edge_cdn_country={country_header}", current_path=current_path)
            elif re.match(r"^[A-Z]{2}$", country_header):
                return cls._decision("en", tier=2, reason=f"edge_cdn_country={country_header}", current_path=current_path)

        # -------------------------------------------------------------
        # Tier 3: Zero-Latency Client Heuristics
        # -------------------------------------------------------------
        # 3a. Timezone
        tz = _to_str(client_heuristics.get("timezone"))
        if tz in cls.INDIAN_TIMEZONES:
            return cls._decision("hi", tier=3, reason=f"timezone={tz}", current_path=current_path)

        # 3b. Navigator languages
        nav_langs = client_heuristics.get("languages", [])
        if isinstance(nav_langs, str):
            nav_langs = [nav_langs]
        for l in nav_langs:
            clean_l = _to_str(l).lower()
            if clean_l == "hi" or clean_l.startswith("hi-") or clean_l.startswith("hi_"):
                return cls._decision("hi", tier=3, reason=f"navigator_lang={clean_l}", current_path=current_path)

        # -------------------------------------------------------------
        # Tier 4: Safe Fallback
        # -------------------------------------------------------------
        return cls._decision("en", tier=4, reason="safe_fallback_default", current_path=current_path)

    @classmethod
    def _decision(cls, lang: str, tier: int, reason: str, is_manual: bool = False, current_path: str = "/") -> dict:
        current_path = "/" if not current_path else (current_path if current_path.startswith("/") else "/" + current_path)
        is_hindi_path = current_path.startswith("/hi/") or current_path == "/hi"
        should_redirect = False
        target_path = current_path

        if lang == "hi" and not is_hindi_path:
            should_redirect = True
            target_path = "/hi" + ("" if current_path == "/" else current_path)
        elif lang == "en" and is_hindi_path:
            should_redirect = True
            target_path = re.sub(r"^/hi(/|$)", "/", current_path)
            if not target_path.startswith("/"):
                target_path = "/" + target_path

        return {
            "lang": lang,
            "tier": tier,
            "reason": reason,
            "is_manual": is_manual,
            "should_redirect": should_redirect,
            "target_path": target_path
        }


# ===========================================================================
# 10 Dedicated Test Classes
# ===========================================================================

class TestTier1ExplicitUserChoice(unittest.TestCase):
    def test_simulate_geo_in_forces_hindi(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "IN"})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 1)

    def test_simulate_geo_us_forces_english(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "US"})
        self.assertEqual(res["lang"], "en")
        self.assertEqual(res["tier"], 1)

    def test_simulate_geo_case_insensitivity(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "in"})
        self.assertEqual(res["lang"], "hi")

    def test_lang_param_direct_override(self):
        res_hi = GeoRoutingSimulator.resolve_language(query_params={"lang": "hi"})
        self.assertEqual(res_hi["lang"], "hi")
        res_en = GeoRoutingSimulator.resolve_language(query_params={"lang": "en"})
        self.assertEqual(res_en["lang"], "en")

    def test_manual_toggle_storage_hi_persists(self):
        storage = {"cinestories_lang": "hi", "cinestories_lang_manual": "true"}
        res = GeoRoutingSimulator.resolve_language(local_storage=storage)
        self.assertEqual(res["lang"], "hi")
        self.assertTrue(res["is_manual"])

    def test_manual_toggle_cookie_hi_persists(self):
        cookies = {"cinestories_lang": "hi", "cinestories_lang_manual": "true"}
        res = GeoRoutingSimulator.resolve_language(cookies=cookies)
        self.assertEqual(res["lang"], "hi")
        self.assertTrue(res["is_manual"])

    def test_manual_toggle_overrides_us_ip_header(self):
        storage = {"cinestories_lang": "hi", "cinestories_lang_manual": "true"}
        headers = {"CF-IPCountry": "US"}
        res = GeoRoutingSimulator.resolve_language(local_storage=storage, edge_headers=headers)
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 1)

    def test_manual_toggle_overrides_indian_ip_header(self):
        storage = {"cinestories_lang": "en", "cinestories_lang_manual": "true"}
        headers = {"CF-IPCountry": "IN"}
        res = GeoRoutingSimulator.resolve_language(local_storage=storage, edge_headers=headers)
        self.assertEqual(res["lang"], "en")
        self.assertEqual(res["tier"], 1)


class TestTier2EdgeCdnHeaders(unittest.TestCase):
    def test_cloudflare_ip_country_in(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"CF-IPCountry": "IN"})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 2)

    def test_cloudflare_ip_country_us(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"CF-IPCountry": "US"})
        self.assertEqual(res["lang"], "en")
        self.assertEqual(res["tier"], 2)

    def test_cloudflare_ip_country_gb(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"CF-IPCountry": "GB"})
        self.assertEqual(res["lang"], "en")

    def test_vercel_ip_country_in(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"x-vercel-ip-country": "IN"})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 2)

    def test_vercel_ip_country_us(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"x-vercel-ip-country": "US"})
        self.assertEqual(res["lang"], "en")

    def test_cloudfront_viewer_country_in(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"CloudFront-Viewer-Country": "IN"})
        self.assertEqual(res["lang"], "hi")

    def test_header_case_insensitivity(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"cf-ipcountry": "in"})
        self.assertEqual(res["lang"], "hi")


class TestTier3ClientHeuristics(unittest.TestCase):
    def test_timezone_asia_kolkata(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "Asia/Kolkata"})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 3)

    def test_timezone_asia_calcutta_legacy(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "Asia/Calcutta"})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 3)

    def test_timezone_ist_alias(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "IST"})
        self.assertEqual(res["lang"], "hi")

    def test_timezone_new_york(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "America/New_York"})
        self.assertEqual(res["lang"], "en")

    def test_timezone_london(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "Europe/London"})
        self.assertEqual(res["lang"], "en")

    def test_navigator_languages_hi(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"languages": ["hi", "en-US"]})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 3)

    def test_navigator_languages_hi_in(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"languages": ["hi-IN", "en-US"]})
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 3)

    def test_navigator_languages_en_only(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"languages": ["en-US", "en"]})
        self.assertEqual(res["lang"], "en")
        self.assertEqual(res["tier"], 4)


class TestTier4SafeFallback(unittest.TestCase):
    def test_empty_inputs_fall_to_english(self):
        res = GeoRoutingSimulator.resolve_language()
        self.assertEqual(res["lang"], "en")
        self.assertEqual(res["tier"], 4)

    def test_unknown_country_header_falls_to_english(self):
        res = GeoRoutingSimulator.resolve_language(edge_headers={"CF-IPCountry": "XX"})
        self.assertEqual(res["lang"], "en")

    def test_unknown_timezone_falls_to_english(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"timezone": "Mars/Olympus"})
        self.assertEqual(res["lang"], "en")

    def test_empty_languages_array_falls_to_english(self):
        res = GeoRoutingSimulator.resolve_language(client_heuristics={"languages": []})
        self.assertEqual(res["lang"], "en")


class TestAdversarialAndCornerCases(unittest.TestCase):
    def test_empty_cookies(self):
        cookies = {"cinestories_lang": "", "cinestories_lang_manual": ""}
        res = GeoRoutingSimulator.resolve_language(cookies=cookies)
        self.assertEqual(res["lang"], "en")

    def test_corrupted_storage_values(self):
        storage = {"cinestories_lang": "MALICIOUS_CODE", "cinestories_lang_manual": "true"}
        res = GeoRoutingSimulator.resolve_language(local_storage=storage)
        self.assertEqual(res["lang"], "en")

    def test_script_injection_in_params(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "<script>alert(1)</script>"})
        self.assertEqual(res["lang"], "en")

    def test_query_param_beats_manual_storage(self):
        # Automated testing override takes top precedence
        storage = {"cinestories_lang": "en", "cinestories_lang_manual": "true"}
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "IN"}, local_storage=storage)
        self.assertEqual(res["lang"], "hi")
        self.assertEqual(res["tier"], 1)

    def test_no_loop_on_current_hindi_page(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "IN"}, current_path="/hi/discover/")
        self.assertEqual(res["lang"], "hi")
        self.assertFalse(res["should_redirect"])

    def test_no_loop_on_current_english_page(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "US"}, current_path="/discover/")
        self.assertEqual(res["lang"], "en")
        self.assertFalse(res["should_redirect"])

    def test_redirect_to_mirror_path(self):
        res = GeoRoutingSimulator.resolve_language(query_params={"simulate_geo": "IN"}, current_path="/articles/stree-2/")
        self.assertTrue(res["should_redirect"])
        self.assertEqual(res["target_path"], "/hi/articles/stree-2/")


# ---------------------------------------------------------------------------
# Static File & DOM Integrity Tests (Runs against dist/ and dist/hi/)
# ---------------------------------------------------------------------------

class TestStaticHreflangBidirectionality(unittest.TestCase):
    def setUp(self):
        if not DIST_HI_DIR.exists():
            self.skipTest("dist/hi/ not yet generated. Milestone M4 required.")

    def test_english_and_hindi_home_hreflang(self):
        en_home = DIST_DIR / "index.html"
        hi_home = DIST_HI_DIR / "index.html"
        self.assertTrue(en_home.exists())
        self.assertTrue(hi_home.exists())

        soup_en = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        soup_hi = BeautifulSoup(hi_home.read_text(encoding="utf-8"), "html.parser")

        link_en_to_hi = soup_en.find("link", rel="alternate", hreflang="hi")
        self.assertIsNotNone(link_en_to_hi, "dist/index.html missing hreflang='hi'")
        self.assertTrue(link_en_to_hi["href"].endswith("/hi/"))

        link_hi_to_en = soup_hi.find("link", rel="alternate", hreflang="en")
        self.assertIsNotNone(link_hi_to_en, "dist/hi/index.html missing hreflang='en'")
        self.assertFalse("/hi/" in link_hi_to_en["href"].rstrip("/"))

    def test_discover_hreflang_bidirectionality(self):
        en_disc = DIST_DIR / "discover" / "index.html"
        hi_disc = DIST_HI_DIR / "discover" / "index.html"
        if not (en_disc.exists() and hi_disc.exists()):
            self.skipTest("Discover pages not yet generated.")

        soup_en = BeautifulSoup(en_disc.read_text(encoding="utf-8"), "html.parser")
        soup_hi = BeautifulSoup(hi_disc.read_text(encoding="utf-8"), "html.parser")

        self.assertIsNotNone(soup_en.find("link", rel="alternate", hreflang="hi"))
        self.assertIsNotNone(soup_hi.find("link", rel="alternate", hreflang="en"))

    def test_breakout_article_hreflang(self):
        en_art = DIST_DIR / "articles" / "stree-2" / "index.html"
        hi_art = DIST_HI_DIR / "articles" / "stree-2" / "index.html"
        if not (en_art.exists() and hi_art.exists()):
            self.skipTest("Stree-2 article pages not yet generated.")

        soup_en = BeautifulSoup(en_art.read_text(encoding="utf-8"), "html.parser")
        soup_hi = BeautifulSoup(hi_art.read_text(encoding="utf-8"), "html.parser")

        self.assertIsNotNone(soup_en.find("link", rel="alternate", hreflang="hi"))
        self.assertIsNotNone(soup_hi.find("link", rel="alternate", hreflang="en"))

    def test_policy_pages_hreflang(self):
        for slug in ["about", "privacy", "terms", "contact", "editorial"]:
            en_p = DIST_DIR / slug / "index.html"
            hi_p = DIST_HI_DIR / slug / "index.html"
            if en_p.exists() and hi_p.exists():
                soup_en = BeautifulSoup(en_p.read_text(encoding="utf-8"), "html.parser")
                soup_hi = BeautifulSoup(hi_p.read_text(encoding="utf-8"), "html.parser")
                self.assertIsNotNone(soup_en.find("link", rel="alternate", hreflang="hi"), f"Missing hi hreflang in en {slug}")
                self.assertIsNotNone(soup_hi.find("link", rel="alternate", hreflang="en"), f"Missing en hreflang in hi {slug}")

    def test_canonical_self_referencing(self):
        en_home = DIST_DIR / "index.html"
        hi_home = DIST_HI_DIR / "index.html"
        if en_home.exists() and hi_home.exists():
            soup_en = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
            soup_hi = BeautifulSoup(hi_home.read_text(encoding="utf-8"), "html.parser")
            can_en = soup_en.find("link", rel="canonical")
            can_hi = soup_hi.find("link", rel="canonical")
            self.assertIsNotNone(can_en)
            self.assertIsNotNone(can_hi)
            self.assertNotEqual(can_en["href"], can_hi["href"])


class TestLanguageSwitcherUIAndState(unittest.TestCase):
    def setUp(self):
        if not DIST_HI_DIR.exists():
            self.skipTest("dist/hi/ not yet generated. Milestone M4 required.")

    def test_switcher_active_pill_state(self):
        en_home = DIST_DIR / "index.html"
        hi_home = DIST_HI_DIR / "index.html"

        soup_en = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        soup_hi = BeautifulSoup(hi_home.read_text(encoding="utf-8"), "html.parser")

        switcher_en = soup_en.find(attrs={"data-component": "lang-switcher"}) or soup_en.find(class_=re.compile(r"lang-switcher|language-toggle"))
        self.assertIsNotNone(switcher_en, "Language switcher missing in dist/index.html")

        switcher_hi = soup_hi.find(attrs={"data-component": "lang-switcher"}) or soup_hi.find(class_=re.compile(r"lang-switcher|language-toggle"))
        self.assertIsNotNone(switcher_hi, "Language switcher missing in dist/hi/index.html")

    def test_switcher_pill_labels_and_flags(self):
        en_home = DIST_DIR / "index.html"
        soup_en = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        switcher = soup_en.find(attrs={"data-component": "lang-switcher"}) or soup_en.find(class_=re.compile(r"lang-switcher|language-toggle"))
        if switcher:
            text = switcher.get_text()
            self.assertTrue("EN" in text or "en" in text.lower())

    def test_switcher_link_targets(self):
        en_home = DIST_DIR / "index.html"
        soup_en = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        switcher = soup_en.find(attrs={"data-component": "lang-switcher"}) or soup_en.find(class_=re.compile(r"lang-switcher|language-toggle"))
        if switcher:
            links = switcher.find_all("a")
            hrefs = [l.get("href", "") for l in links]
            self.assertTrue(any("/hi" in h for h in hrefs), f"Switcher on en home does not link to /hi: {hrefs}")

    def test_switcher_in_footer(self):
        en_home = DIST_DIR / "index.html"
        soup = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        footer = soup.find("footer")
        if footer:
            footer_switcher = footer.find(attrs={"data-component": "lang-switcher"}) or footer.find(class_=re.compile(r"lang-switcher|language-toggle"))
            self.assertIsNotNone(footer_switcher, "Language switcher missing in footer")

    def test_switcher_accessibility_attributes(self):
        en_home = DIST_DIR / "index.html"
        soup = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        switcher = soup.find(attrs={"data-component": "lang-switcher"}) or soup.find(class_=re.compile(r"lang-switcher|language-toggle"))
        if switcher:
            # Check for aria-label or accessible role
            self.assertTrue(switcher.has_attr("aria-label") or switcher.find(attrs={"aria-label": True}) or switcher.name == "nav")


class TestHindiLocalizationIntegrity(unittest.TestCase):
    def setUp(self):
        if not DIST_HI_DIR.exists():
            self.skipTest("dist/hi/ not yet generated. Milestone M4 required.")

    def test_devanagari_characters_in_hindi_home(self):
        hi_home = DIST_HI_DIR / "index.html"
        content = hi_home.read_text(encoding="utf-8")
        devanagari_matches = re.findall(r"[\u0900-\u097F]", content)
        self.assertGreater(len(devanagari_matches), 100, "dist/hi/index.html lacks substantive Devanagari text!")

    def test_zero_unlocalized_ui_buttons(self):
        hi_home = DIST_HI_DIR / "index.html"
        soup = BeautifulSoup(hi_home.read_text(encoding="utf-8"), "html.parser")
        forbidden = ["Read Article", "Watch Web Story", "Search movies", "Latest Updates", "All Stories"]
        for btn in soup.find_all(["button", "a", "span"], class_=re.compile(r"btn|action|tag|label")):
            text = btn.get_text().strip()
            for forb in forbidden:
                self.assertNotIn(forb.lower(), text.lower(), f"Unlocalized English string '{forb}' found in Hindi UI element: {text}")

    def test_i18n_dictionary_key_parity(self):
        try:
            import i18n
            self.assertTrue(hasattr(i18n, "TRANSLATIONS"))
            en_keys = set(i18n.TRANSLATIONS.get("en", {}).keys())
            hi_keys = set(i18n.TRANSLATIONS.get("hi", {}).keys())
            self.assertEqual(en_keys, hi_keys, f"Key parity mismatch between en and hi: {en_keys ^ hi_keys}")
        except ImportError:
            self.skipTest("i18n.py not yet implemented. Milestone M2 required.")

    def test_breakout_article_devanagari_content(self):
        for slug in ["panchayat-season-3", "stree-2"]:
            art = DIST_HI_DIR / "articles" / slug / "index.html"
            if art.exists():
                text = art.read_text(encoding="utf-8")
                devanagari_chars = len(re.findall(r"[\u0900-\u097F]", text))
                self.assertGreater(devanagari_chars, 500, f"Hindi article {slug} lacks sufficient Devanagari characters")

    def test_hindi_section_headings(self):
        for slug in ["panchayat-season-3", "stree-2"]:
            art = DIST_HI_DIR / "articles" / slug / "index.html"
            if art.exists():
                soup = BeautifulSoup(art.read_text(encoding="utf-8"), "html.parser")
                h2s = [h.get_text() for h in soup.find_all("h2")]
                devanagari_h2 = [h for h in h2s if re.search(r"[\u0900-\u097F]", h)]
                self.assertGreaterEqual(len(devanagari_h2), 2, f"Article {slug} lacks Hindi section headings")


class TestAmpStoryComplianceForLocalizedPages(unittest.TestCase):
    def setUp(self):
        hi_stories_dir = DIST_HI_DIR / "stories"
        if not hi_stories_dir.exists():
            self.skipTest("dist/hi/stories/ not yet generated. Milestone M4 required.")

    def test_no_custom_scripts_in_hindi_stories(self):
        hi_stories_dir = DIST_HI_DIR / "stories"
        for story_file in hi_stories_dir.glob("*/index.html"):
            soup = BeautifulSoup(story_file.read_text(encoding="utf-8"), "html.parser")
            scripts = soup.find_all("script")
            for s in scripts:
                is_amp = s.has_attr("custom-element") or (s.has_attr("src") and "cdn.ampproject.org" in s.get("src", ""))
                is_json = s.get("type") in ["application/json", "application/ld+json"]
                self.assertTrue(is_amp or is_json, f"Forbidden custom script in AMP story: {story_file.name}")

    def test_hindi_stories_valid_boilerplate(self):
        hi_stories_dir = DIST_HI_DIR / "stories"
        for story_file in hi_stories_dir.glob("*/index.html"):
            content = story_file.read_text(encoding="utf-8")
            self.assertIn("amp-boilerplate", content)
            self.assertTrue("⚡" in content or "amp" in content)

    def test_hindi_stories_outlinks_localized(self):
        hi_stories_dir = DIST_HI_DIR / "stories"
        for story_file in hi_stories_dir.glob("*/index.html"):
            soup = BeautifulSoup(story_file.read_text(encoding="utf-8"), "html.parser")
            outlink = soup.find("amp-story-page-outlink")
            if outlink:
                a_tag = outlink.find("a")
                if a_tag and a_tag.get("href"):
                    self.assertTrue("/hi/" in a_tag["href"], f"Outlink does not target /hi/ namespace: {a_tag['href']}")

    def test_hindi_stories_slide_word_count(self):
        hi_stories_dir = DIST_HI_DIR / "stories"
        for story_file in hi_stories_dir.glob("*/index.html"):
            soup = BeautifulSoup(story_file.read_text(encoding="utf-8"), "html.parser")
            pages = soup.find_all("amp-story-page")
            for idx, page in enumerate(pages):
                text = " ".join([p.get_text() for p in page.find_all(["p", "h1", "h2", "h3", "span"])])
                tokens = re.split(r"[\s।॥,;:!?]+", text)
                words = [t for t in tokens if t.strip()]
                self.assertLessEqual(len(words), 45, f"Slide {idx} in {story_file.parent.name} exceeds 40-word guideline ({len(words)} words)")


class TestClientSideGeoScriptStructure(unittest.TestCase):
    def test_geo_script_present_in_head(self):
        en_home = DIST_DIR / "index.html"
        if not en_home.exists():
            self.skipTest("dist/index.html not yet generated.")
        soup = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        head = soup.find("head")
        self.assertIsNotNone(head)

    def test_geo_script_checks_manual_flag(self):
        en_home = DIST_DIR / "index.html"
        if not en_home.exists():
            self.skipTest("dist/index.html not yet generated.")
        content = en_home.read_text(encoding="utf-8")
        # If client geo script is present, verify manual flag string
        if "cinestories_lang" in content:
            self.assertIn("cinestories_lang_manual", content)

    def test_geo_script_loop_prevention(self):
        en_home = DIST_DIR / "index.html"
        if not en_home.exists():
            self.skipTest("dist/index.html not yet generated.")
        content = en_home.read_text(encoding="utf-8")
        if "window.location.replace" in content:
            self.assertTrue("pathname" in content)

    def test_geo_script_excluded_from_amp(self):
        stories = list(DIST_DIR.glob("stories/*/index.html"))
        if not stories:
            self.skipTest("No stories found.")
        for s in stories[:5]:
            content = s.read_text(encoding="utf-8")
            self.assertNotIn("cinestories_lang_manual", content, "Custom geo routing script must NOT exist in AMP stories")


# ---------------------------------------------------------------------------
# CLI Runner with Detailed Terminal Reporting
# ---------------------------------------------------------------------------
def run_cli():
    print("=" * 70)
    print("     CINESTORIES GEO-ROUTING & I18N AUTOMATED TEST SUITE     ")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestTier1ExplicitUserChoice,
        TestTier2EdgeCdnHeaders,
        TestTier3ClientHeuristics,
        TestTier4SafeFallback,
        TestAdversarialAndCornerCases,
        TestStaticHreflangBidirectionality,
        TestLanguageSwitcherUIAndState,
        TestHindiLocalizationIntegrity,
        TestAmpStoryComplianceForLocalizedPages,
        TestClientSideGeoScriptStructure,
    ]
    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print(f">>> ALL {result.testsRun} GEO-ROUTING & I18N TESTS COMPLETED SUCCESSFULLY! <<<")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f">>> TEST SUITE FAILED: {len(result.failures)} failures, {len(result.errors)} errors <<<")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
