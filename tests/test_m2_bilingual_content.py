"""
Unit & Integration Test Suite for CineStories Milestone 2:
Bilingual Content Pipeline & Editorial Depth Layer.

Validates:
1. i18n.py translation completeness, 100% key parity, and graceful fallback.
2. curated_stories_hi.py slide constraints (<40 words/slide, Devanagari text, 6-8 slides).
3. curated_articles_hi.py editorial depth (>650 words across 5 required sections).
4. curated_articles.py editorial depth (>650 words across 5 sections, 0 banned phrases).
"""

import re
import sys
import unittest
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from compliance_linter import TARGET_BREAKOUT_SLUGS, BANNED_BOILERPLATE_PHRASES


class TestI18nLocalization(unittest.TestCase):
    def setUp(self):
        import i18n
        self.i18n = i18n

    def test_module_has_translations_and_helper(self):
        self.assertTrue(hasattr(self.i18n, "TRANSLATIONS"))
        self.assertTrue(callable(getattr(self.i18n, "get_translation", None)))

    def test_key_parity_between_en_and_hi(self):
        en_keys = set(self.i18n.TRANSLATIONS.get("en", {}).keys())
        hi_keys = set(self.i18n.TRANSLATIONS.get("hi", {}).keys())
        self.assertGreater(len(en_keys), 50, "i18n dictionary should have substantial entries")
        self.assertEqual(en_keys, hi_keys, f"Key parity mismatch between en and hi: {en_keys ^ hi_keys}")

    def test_navigation_items_coverage(self):
        required_nav = [
            "Home", "Discover", "Stories", "Articles", "About Us",
            "Contact Us", "Privacy Policy", "Terms of Service",
            "Editorial Policy", "Switch Language"
        ]
        for item in required_nav:
            self.assertIn(item, self.i18n.TRANSLATIONS["en"])
            hi_val = self.i18n.get_translation(item, "hi")
            self.assertNotEqual(hi_val, item, f"Navigation item '{item}' was not localized in Hindi")
            self.assertTrue(re.search(r"[\u0900-\u097F]", hi_val), f"'{item}' Hindi translation lacks Devanagari: {hi_val}")

    def test_categories_coverage(self):
        required_cats = [
            "All", "Bollywood", "Hollywood", "Action", "Drama",
            "Thriller", "Horror", "Comedy", "Sci-Fi", "Romance"
        ]
        for cat in required_cats:
            self.assertIn(cat, self.i18n.TRANSLATIONS["en"])
            hi_val = self.i18n.get_translation(cat, "hi")
            self.assertTrue(re.search(r"[\u0900-\u097F]", hi_val), f"Category '{cat}' lacks Devanagari: {hi_val}")

    def test_buttons_and_placeholders_coverage(self):
        required_ui = [
            "Read Article", "Watch Web Story", "Latest Updates",
            "Search movies...", "Share", "Copy Link", "Copied!",
            "CineStories Editorial Board"
        ]
        for ui in required_ui:
            self.assertIn(ui, self.i18n.TRANSLATIONS["en"])
            hi_val = self.i18n.get_translation(ui, "hi")
            self.assertTrue(re.search(r"[\u0900-\u097F]", hi_val), f"UI element '{ui}' lacks Devanagari: {hi_val}")

    def test_graceful_fallback_behavior(self):
        # Fallback to English for missing language
        self.assertEqual(self.i18n.get_translation("Home", "es"), "Home")
        self.assertEqual(self.i18n.get_translation("Home", "de"), "Home")
        # Fallback to key itself for missing key
        self.assertEqual(self.i18n.get_translation("completely_unknown_key_xyz", "hi"), "completely_unknown_key_xyz")
        # Non-string safe handling
        self.assertEqual(self.i18n.get_translation(None, "hi"), "")


class TestCuratedStoriesHindi(unittest.TestCase):
    def setUp(self):
        import curated_stories_hi
        self.stories = curated_stories_hi.CURATED_STORIES_HI

    def test_all_10_breakout_slugs_present(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            self.assertIn(slug, self.stories, f"Missing breakout story slug: {slug}")

    def test_slide_count_per_story(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            slides = self.stories[slug].get("slides", [])
            self.assertTrue(6 <= len(slides) <= 8, f"Story '{slug}' has {len(slides)} slides (expected 6-8)")

    def test_amp_slide_word_count_strictly_under_40(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            slides = self.stories[slug].get("slides", [])
            for idx, slide in enumerate(slides):
                text = slide.get("text", "")
                words = len(text.split())
                self.assertLess(
                    words, 40,
                    f"Story '{slug}' slide {idx + 1} exceeds 40-word limit: ({words} words): '{text}'"
                )

    def test_authentic_devanagari_prose(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            story = self.stories[slug]
            title = story.get("title", "")
            self.assertTrue(re.search(r"[\u0900-\u097F]", title), f"Story title '{title}' lacks Devanagari")
            for idx, slide in enumerate(story.get("slides", [])):
                stext = slide.get("text", "")
                dev_chars = len(re.findall(r"[\u0900-\u097F]", stext))
                self.assertGreater(dev_chars, 10, f"Slide {idx + 1} in '{slug}' lacks Devanagari content")

    def test_visual_framing_and_cta_elements(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            story = self.stories[slug]
            slides = story.get("slides", [])
            final_slide = slides[-1]
            self.assertIn("badge", slides[0])
            self.assertIn("backdrop_index", slides[0])
            self.assertTrue("cta_text" in final_slide or "poll" in final_slide)


class TestCuratedArticlesHindi(unittest.TestCase):
    def setUp(self):
        import curated_articles_hi
        self.articles = curated_articles_hi.CURATED_ARTICLES_HI

    def test_all_10_breakout_slugs_present(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            self.assertIn(slug, self.articles, f"Missing breakout article slug: {slug}")

    def test_five_thematic_sections_present(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            sections = art.get("sections", [])
            self.assertEqual(len(sections), 5, f"Article '{slug}' has {len(sections)} sections, expected exactly 5")
            for sec in sections:
                h = sec.get("heading", "")
                self.assertTrue(re.search(r"[\u0900-\u097F]", h), f"Section heading in '{slug}' lacks Devanagari: '{h}'")

    def test_word_count_exceeds_650_words(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            texts = [s.get("content", "") for s in art.get("sections", [])]
            texts.extend(art.get("key_takeaways", []))
            texts.append(art.get("verdict_summary", ""))
            texts.append(art.get("who_should_watch", ""))
            texts.append(art.get("skip_if", ""))
            combined = " ".join(texts)
            tokens = [t for t in re.split(r"[\s।॥,;:!?]+", combined) if t.strip()]
            self.assertGreaterEqual(
                len(tokens), 650,
                f"Article '{slug}' word count {len(tokens)} is below mandatory 650 threshold"
            )

    def test_authentic_devanagari_depth(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            combined = " ".join([s.get("content", "") for s in art.get("sections", [])])
            dev_chars = len(re.findall(r"[\u0900-\u097F]", combined))
            self.assertGreater(dev_chars, 2000, f"Article '{slug}' lacks deep Devanagari prose ({dev_chars} chars)")


class TestCuratedArticlesEnglishDepth(unittest.TestCase):
    def setUp(self):
        import curated_articles
        self.articles = curated_articles.CURATED_ARTICLES

    def test_all_10_breakout_slugs_present(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            self.assertIn(slug, self.articles, f"Missing English breakout article slug: {slug}")

    def test_five_thematic_sections_present(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            sections = art.get("sections", [])
            self.assertEqual(len(sections), 5, f"English article '{slug}' has {len(sections)} sections, expected exactly 5")

    def test_word_count_exceeds_650_words(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            texts = [s.get("content", "") for s in art.get("sections", [])]
            texts.extend(art.get("key_takeaways", []))
            texts.append(art.get("verdict_summary", ""))
            texts.append(art.get("who_should_watch", ""))
            texts.append(art.get("skip_if", ""))
            combined = " ".join(texts)
            tokens = [t for t in re.split(r"[\s।॥,;:!?]+", combined) if t.strip()]
            self.assertGreaterEqual(
                len(tokens), 650,
                f"English article '{slug}' word count {len(tokens)} is below mandatory 650 threshold"
            )

    def test_zero_canned_boilerplate_phrases(self):
        for slug in TARGET_BREAKOUT_SLUGS:
            art = self.articles[slug]
            texts = [s.get("content", "") for s in art.get("sections", [])]
            texts.extend(art.get("key_takeaways", []))
            texts.append(art.get("verdict_summary", ""))
            combined = " ".join(texts).lower()
            for phrase in BANNED_BOILERPLATE_PHRASES:
                self.assertNotIn(
                    phrase.lower(), combined,
                    f"English article '{slug}' contains banned boilerplate phrase: '{phrase}'"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
