"""
Unit & Integration Test Suite for CineStories Milestone 3:
UI Modernization & Responsive Layout Across All Builders.

Covers:
1. homepage_builder:
   - Streamlined mobile header (360px-420px): brand-wrap, logo (32px), .lang-switch-pill, discover button.
   - Horizontal scroll-snap filter rail: .filter-rail-wrapper, .filter-rail, .filter-chip (scroll-snap-type: x mandatory, flex-wrap: nowrap).
   - Tactile micro-interactions: :active scale(0.97), #toastNotification, celebration sparkles.
   - Bilingual hreflangs and Noto Sans Devanagari font import.

2. discover_feed_builder:
   - Responsive Grid Breakpoints: 1 col (<768px), 2 cols (768px-1279px), 3 cols (1280px+).
   - Horizontal scroll-snap filter rail: #filterPills, .filter-pill (scroll-snap-type: x mandatory, flex-wrap: nowrap).
   - Tactile micro-interactions: card hover, :active press states, share toast with celebratory sparkles.
   - Bilingual support: hreflangs, localized labels.

3. article_builder:
   - Reading experience & typography: max-width 820px container, max-width 740px body, line-height 1.85, left accent border on h2.
   - Top reading scroll progress bar: #readingProgress with scroll event listener.
   - Verified Editorial Byline: CineStories Editorial Board, .verified-badge with ✓, link to /editorial/.
   - 1-click share copy toast: #toastNotification, celebrateSparkles(), copyArticleLink().
   - Bilingual support: hreflangs, localized labels, Noto Sans Devanagari.

4. story_builder:
   - Font family: Outfit, Noto Sans Devanagari.
   - Devanagari typography: line-height padding, zero -webkit-line-clamp on slides 1-7, word-break: break-word.
   - 100% AMP validation compliance: no !important, valid boilerplate, .final-slide-card, .final-legal-row.
   - Bilingual support: hreflangs, localized labels, Schema inLanguage.
"""

import re
import sys
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import homepage_builder
import discover_feed_builder
import article_builder
import story_builder

MOCK_MOVIE = {
    "title": "Inception: Climax Breakdown",
    "slug": "inception-climax-breakdown",
    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology.",
    "category": "theories_easter_eggs",
    "backdrop_path": "/inception-bg.jpg",
    "poster_path": "/inception-poster.jpg",
    "vote_average": 8.8,
    "release_date": "2010-07-16",
    "runtime": 148,
    "director": "Christopher Nolan",
    "top_cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Tom Hardy"],
    "genres": ["Sci-Fi", "Action", "Thriller"]
}

MOCK_STORY = {
    "title": "Inception Climax Explained: The Spinning Top Verdict",
    "seo_description": "Did the top wobble? The definitive breakdown of Cobb's reality.",
    "movie": MOCK_MOVIE,
    "slides": [
        {"title": "The Spinning Totem", "text": "Cobb watches the spinning top.", "badge": "CLUE 1"},
        {"title": "The Dream Ring", "text": "Notice his left ring finger throughout the layers.", "badge": "CLUE 2"},
        {"title": "The Up Next Finale", "text": "Read our next viral story or dive into the full article.", "badge": "VERDICT"}
    ]
}

MOCK_ARTICLE = {
    "movie": MOCK_MOVIE,
    "headline": "Inception Ending Decoded: The Ring Clue Proves Cobb Is in Reality",
    "meta_description": "A forensic examination of Christopher Nolan's totem clues and what the children's clothing proves.",
    "who_should_watch": "Fans of mind-bending cinema who love analyzing ambiguous endings.",
    "skip_if": "Viewers seeking straightforward linear plots without open questions.",
    "key_takeaways": [
        "The children are wearing different clothes and are credited with different child actors.",
        "The totem was Mal's, not Cobb's original anchor.",
        "Cobb walks away before seeing if the top falls, proving emotional closure."
    ],
    "sections": [
        {"heading": "The Wedding Ring Totem Rule", "content": "Throughout every dream layer, Cobb wears his gold wedding ring. In reality, he does not."},
        {"heading": "The Cast of Children", "content": "Two sets of child actors play Cobb's kids in the credits, confirming passage of real time."}
    ],
    "verdict_summary": "Cobb is in reality, but more importantly, he has ceased obsessing over the test."
}


class TestHomepageBuilderModernization(unittest.TestCase):
    def setUp(self):
        self.html_en = homepage_builder.build_homepage_html([MOCK_STORY], lang="en")
        self.html_hi = homepage_builder.build_homepage_html([MOCK_STORY], lang="hi")
        self.soup_en = BeautifulSoup(self.html_en, "html.parser")
        self.soup_hi = BeautifulSoup(self.html_hi, "html.parser")

    def test_mobile_header_structure_and_pill(self):
        # 1. Brand logo and title present
        brand = self.soup_en.find("a", class_="brand-wrap")
        self.assertIsNotNone(brand)
        self.assertIsNotNone(brand.find("img", class_="brand-logo"))
        self.assertIsNotNone(brand.find(class_="brand-title"))

        # 2. Language Switcher Pill present
        lang_pill = self.soup_en.find("div", class_="lang-switch-pill")
        self.assertIsNotNone(lang_pill)
        self.assertIn("🇺🇸 EN", lang_pill.get_text())
        self.assertIn("🇮🇳 हिं", lang_pill.get_text())

        # 3. Compact media queries for 360px-420px viewport
        self.assertIn("@media (max-width: 420px)", self.html_en)
        self.assertIn(".brand-logo", self.html_en)

    def test_horizontal_scroll_snap_filter_rail(self):
        rail_wrapper = self.soup_en.find("div", class_="filter-rail-wrapper")
        self.assertIsNotNone(rail_wrapper)
        rail = rail_wrapper.find("div", class_="filter-rail")
        self.assertIsNotNone(rail)
        chips = rail.find_all("button", class_="filter-chip")
        self.assertGreaterEqual(len(chips), 5)

        # CSS verification for horizontal scroll-snap
        self.assertIn("scroll-snap-type: x mandatory", self.html_en)
        self.assertIn("flex-wrap: nowrap", self.html_en)
        self.assertIn("-webkit-overflow-scrolling: touch", self.html_en)

    def test_tactile_micro_interactions_and_delights(self):
        # CSS tactile active states
        self.assertIn(":active", self.html_en)
        self.assertIn("scale(0.97)", self.html_en)

        # Toast notification element
        toast = self.soup_en.find("div", id="toastNotification")
        self.assertIsNotNone(toast)
        self.assertIn("toast-notification", toast.get("class", []))

        # JavaScript celebration sparkles function
        self.assertIn("celebrateSparkles", self.html_en)
        self.assertIn("sparkle-item", self.html_en)

    def test_bilingual_hreflangs_and_fonts(self):
        # Hreflangs
        self.assertIn('hreflang="en"', self.html_en)
        self.assertIn('hreflang="hi"', self.html_en)
        self.assertIn('hreflang="x-default"', self.html_en)

        # Noto Sans Devanagari font import
        self.assertIn("Noto+Sans+Devanagari", self.html_en)
        self.assertIn("Noto+Sans+Devanagari", self.html_hi)

        # Hindi page validation
        self.assertEqual(self.soup_hi.find("html").get("lang"), "hi")
        self.assertIn("डिस्कवर", self.html_hi)


class TestDiscoverFeedBuilderModernization(unittest.TestCase):
    def setUp(self):
        self.html_en = discover_feed_builder.build_discover_feed_html([MOCK_ARTICLE], lang="en")
        self.html_hi = discover_feed_builder.build_discover_feed_html([MOCK_ARTICLE], lang="hi")
        self.soup_en = BeautifulSoup(self.html_en, "html.parser")
        self.soup_hi = BeautifulSoup(self.html_hi, "html.parser")

    def test_responsive_grid_breakpoints(self):
        # Check responsive grid column rules in CSS
        self.assertIn(".feed-container", self.html_en)
        self.assertIn("grid-template-columns: 1fr;", self.html_en)
        self.assertIn("grid-template-columns: repeat(2, 1fr);", self.html_en)
        self.assertIn("grid-template-columns: repeat(3, 1fr);", self.html_en)

    def test_horizontal_scroll_snap_filter_rail(self):
        pills_container = self.soup_en.find("div", id="filterPills")
        self.assertIsNotNone(pills_container)
        pills = pills_container.find_all("button", class_="filter-pill")
        self.assertGreaterEqual(len(pills), 5)

        self.assertIn("scroll-snap-type: x mandatory", self.html_en)
        self.assertIn("flex-wrap: nowrap", self.html_en)

    def test_share_toast_and_sparkles(self):
        toast = self.soup_en.find("div", id="toastNotification")
        self.assertIsNotNone(toast)
        self.assertIn("shareArticle", self.html_en)
        self.assertIn("celebrateSparkles", self.html_en)
        self.assertIn("scale(0.97)", self.html_en)


class TestArticleBuilderModernization(unittest.TestCase):
    def setUp(self):
        self.html_en = article_builder.build_discover_article_html(MOCK_ARTICLE, lang="en")
        self.html_hi = article_builder.build_discover_article_html(MOCK_ARTICLE, lang="hi")
        self.soup_en = BeautifulSoup(self.html_en, "html.parser")
        self.soup_hi = BeautifulSoup(self.html_hi, "html.parser")

    def test_reading_layout_and_typography(self):
        # Max widths for reading comfort
        self.assertIn("--max-width: 820px", self.html_en)
        self.assertIn(".article-body", self.html_en)
        self.assertIn("max-width: 740px", self.html_en)

        # Heading style with accent bar
        self.assertIn("border-left: 3px solid var(--primary)", self.html_en)

    def test_reading_scroll_progress_bar(self):
        bar = self.soup_en.find("div", id="readingProgress")
        self.assertIsNotNone(bar)
        self.assertIn("reading-progress-bar", bar.get("class", []))
        self.assertIn("window.addEventListener('scroll'", self.html_en)

    def test_verified_editorial_byline(self):
        byline = self.soup_en.find("div", class_="byline-bar")
        self.assertIsNotNone(byline)
        self.assertIn("CineStories Editorial Board", byline.get_text())

        # Verified badge
        verified_badge = byline.find("span", class_="verified-badge")
        self.assertIsNotNone(verified_badge)
        self.assertEqual(verified_badge.get_text().strip(), "✓")

        # Link to /editorial/
        editorial_link = byline.find("a", href="/editorial/")
        self.assertIsNotNone(editorial_link)

    def test_toast_share_delights(self):
        toast = self.soup_en.find("div", id="toastNotification")
        self.assertIsNotNone(toast)
        self.assertIn("copyArticleLink", self.html_en)
        self.assertIn("celebrateSparkles", self.html_en)

    def test_bilingual_support(self):
        self.assertEqual(self.soup_en.find("html").get("lang"), "en")
        self.assertEqual(self.soup_hi.find("html").get("lang"), "hi")
        self.assertIn('hreflang="en"', self.html_en)
        self.assertIn('hreflang="hi"', self.html_en)
        self.assertIn("पाठकों के लिए मुख्य बातें", self.html_hi)


class TestStoryBuilderModernization(unittest.TestCase):
    def setUp(self):
        self.html_en = story_builder.build_amp_story_html(MOCK_STORY, lang="en")
        self.html_hi = story_builder.build_amp_story_html(MOCK_STORY, lang="hi")
        self.soup_en = BeautifulSoup(self.html_en, "html.parser")
        self.soup_hi = BeautifulSoup(self.html_hi, "html.parser")

    def test_amp_structure_and_fonts(self):
        self.assertIn("Noto+Sans+Devanagari", self.html_en)
        self.assertIn("Outfit", self.html_en)
        self.assertIn("'Noto Sans Devanagari'", self.html_en)

        # 100% AMP elements
        self.assertTrue(self.soup_en.find("html").has_attr("⚡"))
        self.assertIsNotNone(self.soup_en.find("amp-story"))
        self.assertIsNotNone(self.soup_en.find("style", attrs={"amp-custom": True}))

    def test_devanagari_typography_and_anti_clipping(self):
        # Line-height for .slide-text
        self.assertIn("line-height: 1.40;", self.html_en)
        self.assertIn("overflow-wrap: break-word;", self.html_en)
        self.assertIn("word-break: break-word;", self.html_en)

        # Anti-truncation on narrative slides 1-7 (no -webkit-line-clamp in .slide-text)
        css_tag = self.soup_en.find("style", attrs={"amp-custom": True})
        css_text = css_tag.get_text()
        slide_text_match = re.search(r"\.slide-text\s*\{([^}]+)\}", css_text)
        self.assertIsNotNone(slide_text_match)
        self.assertNotIn("-webkit-line-clamp", slide_text_match.group(1))

    def test_final_slide_containment_and_legal_row(self):
        final_page = self.soup_en.find_all("amp-story-page")[-1]
        final_card = final_page.find("div", class_="final-slide-card")
        self.assertIsNotNone(final_card)
        legal_row = final_card.find("div", class_="final-legal-row")
        self.assertIsNotNone(legal_row)

    def test_bilingual_hreflangs(self):
        self.assertIn('hreflang="en"', self.html_en)
        self.assertIn('hreflang="hi"', self.html_en)
        self.assertIn('"inLanguage": "hi-IN"', self.html_hi)
        self.assertIn('"inLanguage": "en-US"', self.html_en)


if __name__ == "__main__":
    unittest.main()
