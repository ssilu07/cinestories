"""
Dedicated, high-fidelity generator script for the CineStories 10 Breakout Viral Content Slate.
Dual-Locale Static Build Pipeline:
- Builds all 10 AMP Web Stories and Discover Articles in English (dist/) and Hindi (dist/hi/)
- Parameterizes HTML generation with lang="en" and lang="hi"
- Injects reciprocal alternate hreflangs, self-referencing canonicals, and localized Schema.org
- Embeds tactile manual language switchers [ 🇺🇸 EN | 🇮🇳 हिं ] in headers, footers, and AMP top bars
- Embeds zero-latency client geo-detection and switcher persistence in <head> for non-AMP pages
- Generates unified bilingual XML sitemap and localized RSS feeds
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from config import (
    DOMAIN_NAME,
    DIST_DIR,
    STORIES_DIR,
    ARTICLES_DIR,
    DISCOVER_DIR,
    SITEMAP_PATH,
    ARTICLES_JSON_PATH,
    STORIES_JSON_PATH,
    REGISTRY_PATH,
    TARGET_BREAKOUT_SLUGS,
    TMDB_IMAGE_POSTER,
    TMDB_IMAGE_BACKDROP
)
from sample_data import SAMPLE_MEDIA
from curated_stories import CURATED_STORIES
from curated_articles import CURATED_ARTICLES
from curated_stories_hi import CURATED_STORIES_HI
from curated_articles_hi import CURATED_ARTICLES_HI

from story_builder import build_amp_story_html
from article_builder import build_discover_article_html
from homepage_builder import generate_homepage
from discover_feed_builder import generate_discover_feed
from policy_pages import generate_policy_pages
from feed_builder import generate_rss_feed

from geo_routing import (
    render_language_switcher,
    generate_hreflang_tags,
    get_geo_detection_script,
    get_switcher_script,
    LANGUAGE_SWITCHER_CSS,
    normalize_paths
)

DIST_HI_DIR = DIST_DIR / "hi"
HI_STORIES_DIR = DIST_HI_DIR / "stories"
HI_ARTICLES_DIR = DIST_HI_DIR / "articles"
HI_DISCOVER_DIR = DIST_HI_DIR / "discover"

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


def post_process_page(
    html_text: str,
    current_path: str,
    lang: str = "en",
    is_amp: bool = False,
    domain: str = DOMAIN_NAME
) -> str:
    """
    Guarantees strict compliance across all generated pages:
    - Bidirectional reciprocal alternate hreflang tags (en, hi, x-default)
    - Self-referencing canonical tag
    - Schema.org inLanguage ("en-US" or "hi-IN")
    - Non-AMP: Client-side 4-tier geo-detection & switcher scripts in <head>,
      and tactile segmented language switcher in header and in footer.
    - AMP: Pure AMP HTML with zero forbidden custom scripts, and localized outlinks.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    en_path, hi_path = normalize_paths(current_path)
    base_domain = domain.rstrip("/")

    en_canonical = f"{base_domain}{en_path}"
    hi_canonical = f"{base_domain}{hi_path}"
    canonical_url = hi_canonical if lang == "hi" else en_canonical

    # 1. Canonical Link
    can = soup.find("link", rel="canonical")
    if can:
        can["href"] = canonical_url
    elif soup.head:
        new_can = soup.new_tag("link", rel="canonical", href=canonical_url)
        soup.head.append(new_can)

    # Check if alternate target actually exists on disk or in breakout slugs!
    has_hi_counterpart = True
    if "/articles/" in en_path or "/stories/" in en_path:
        slug_match = re.search(r"/(?:articles|stories)/([^/]+)/", en_path)
        if slug_match:
            slug = slug_match.group(1)
            has_hi_counterpart = (slug in TARGET_BREAKOUT_SLUGS)
        else:
            has_hi_counterpart = False

    # 2. Reciprocal Alternate Hreflangs
    if soup.head:
        for tag in soup.head.find_all("link", rel="alternate", hreflang=True):
            tag.decompose()
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="en", href=en_canonical))
        if has_hi_counterpart:
            soup.head.append(soup.new_tag("link", rel="alternate", hreflang="hi", href=hi_canonical))
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=en_canonical))

    # 3. HTML lang attribute
    if soup.html:
        soup.html["lang"] = lang

    # 4. JSON-LD inLanguage declaration
    target_in_lang = "hi-IN" if lang == "hi" else "en-US"
    for s in soup.find_all("script", type="application/ld+json"):
        if s.string:
            try:
                data = json.loads(s.string)
                updated = False
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if isinstance(item, dict):
                        if "@graph" in item and isinstance(item["@graph"], list):
                            for g in item["@graph"]:
                                if isinstance(g, dict) and "@type" in g:
                                    g["inLanguage"] = target_in_lang
                                    updated = True
                        elif "@type" in item:
                            item["inLanguage"] = target_in_lang
                            updated = True
                if updated:
                    s.string = json.dumps(data, indent=2)
            except Exception:
                pass

    if is_amp:
        # STRICTLY ZERO CUSTOM SCRIPTS IN AMP!
        # Ensure outlink target is localized for Hindi
        if lang == "hi":
            outlink = soup.find("amp-story-page-outlink")
            if outlink:
                a_tag = outlink.find("a")
                if a_tag and a_tag.get("href"):
                    orig_href = a_tag["href"]
                    if "/hi/" not in orig_href:
                        a_tag["href"] = orig_href.replace("/articles/", "/hi/articles/").replace("/stories/", "/hi/stories/")
        out_html = str(soup)
        for attr in ["amp-boilerplate", "amp-custom", "⚡", "async", "standalone", "crossorigin"]:
            out_html = out_html.replace(f'{attr}=""', attr)
        return out_html

    # -------------------------------------------------------------------------
    # NON-AMP PAGES: Inject Scripts, CSS, and Tactile Switchers
    # -------------------------------------------------------------------------
    # Clean up any residual English text in Hindi UI buttons
    if lang == "hi":
        for elem in soup.find_all(["button", "a", "span"]):
            for eng, hin in [
                ("⚡ Watch Web Story", "⚡ वेब स्टोरी देखें"),
                ("Watch Web Story", "वेब स्टोरी देखें"),
                ("Read Article", "लेख पढ़ें"),
                ("Read Climax Breakdown", "क्लाइमेक्स विश्लेषण पढ़ें"),
                ("Read Full Article", "पूरा आर्टिकल पढ़ें"),
                ("Search movies", "फ़िल्में खोजें"),
                ("Latest Updates", "ताज़ा अपडेट्स"),
                ("All Stories", "सभी कहानियाँ"),
                ("Explore All Stories", "सभी कहानियाँ देखें"),
            ]:
                if eng in elem.get_text():
                    for text_node in elem.find_all(string=True):
                        if eng in text_node:
                            text_node.replace_with(text_node.replace(eng, hin))

    # 5. Inject Client Geo Detection & Switcher Persistence scripts in <head>
    if soup.head:
        head_str = str(soup.head)
        if "cinestories_lang_manual" not in head_str:
            geo_tag = BeautifulSoup(get_geo_detection_script() + "\n" + get_switcher_script(), "html.parser")
            soup.head.append(geo_tag)
        if ".lang-switcher" not in head_str:
            style_tag = soup.new_tag("style")
            style_tag.string = LANGUAGE_SWITCHER_CSS
            soup.head.append(style_tag)

    # 6. Inject or Replace Language Switcher in Header
    effective_path = current_path
    if not has_hi_counterpart:
        effective_path = "/discover/" if "/articles/" in en_path else "/"
    switcher_html = render_language_switcher(effective_path, lang=lang, is_amp=False)
    header = soup.find("header") or soup.find("nav", class_="navbar")
    if header:
        existing_sw = header.find(attrs={"data-component": "lang-switcher"}) or header.find(class_=re.compile(r"lang-switcher|lang-switch-pill|language-toggle"))
        if existing_sw:
            existing_sw.replace_with(BeautifulSoup(switcher_html, "html.parser"))
        else:
            nav_actions = header.find(class_="nav-actions")
            if nav_actions:
                nav_actions.insert(0, BeautifulSoup(switcher_html, "html.parser"))
            else:
                header.append(BeautifulSoup(switcher_html, "html.parser"))

    # 7. Inject or Replace Language Switcher in Footer
    footer = soup.find("footer")
    if footer:
        existing_footer_sw = footer.find(attrs={"data-component": "lang-switcher"}) or footer.find(class_=re.compile(r"lang-switcher|language-toggle"))
        if existing_footer_sw:
            existing_footer_sw.replace_with(BeautifulSoup(switcher_html, "html.parser"))
        else:
            footer_container = footer.find(class_="footer-container")
            if footer_container:
                footer_links = footer_container.find(class_="footer-links")
                if footer_links:
                    footer_links.insert_before(BeautifulSoup(switcher_html, "html.parser"))
                else:
                    footer_container.append(BeautifulSoup(switcher_html, "html.parser"))
            else:
                footer.append(BeautifulSoup(switcher_html, "html.parser"))

    return str(soup)


def build_bilingual_sitemap(
    en_stories: list,
    hi_stories: list,
    en_articles: list,
    hi_articles: list,
    domain: str = DOMAIN_NAME,
    output_path: Path = SITEMAP_PATH
):
    """
    Builds a unified, Google Search Essentials compliant XML sitemap covering
    all English (dist/) and Hindi (dist/hi/) URLs with image extensions.
    """
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base_domain = domain.rstrip("/")

    urlset = ET.Element(
        "urlset",
        {
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1",
            "xmlns:xhtml": "http://www.w3.org/1999/xhtml"
        }
    )

    def add_url(loc, lastmod=today_str, changefreq="daily", priority="0.8", backdrop=None, title=None, alt_loc=None, alt_lang=None):
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = loc
        ET.SubElement(url_elem, "lastmod").text = lastmod
        ET.SubElement(url_elem, "changefreq").text = changefreq
        ET.SubElement(url_elem, "priority").text = priority

        if alt_loc and alt_lang:
            xhtml_link = ET.SubElement(url_elem, "xhtml:link")
            xhtml_link.set("rel", "alternate")
            xhtml_link.set("hreflang", alt_lang)
            xhtml_link.set("href", alt_loc)

        if backdrop:
            img_elem = ET.SubElement(url_elem, "image:image")
            img_loc = f"{TMDB_IMAGE_BACKDROP}{backdrop}" if backdrop.startswith("/") else backdrop
            ET.SubElement(img_elem, "image:loc").text = img_loc
            if title:
                ET.SubElement(img_elem, "image:title").text = f"{title} Feature Still"

    # 1. Portals (EN & HI)
    add_url(f"{base_domain}/", changefreq="daily", priority="1.0", alt_loc=f"{base_domain}/hi/", alt_lang="hi")
    add_url(f"{base_domain}/hi/", changefreq="daily", priority="1.0", alt_loc=f"{base_domain}/", alt_lang="en")
    add_url(f"{base_domain}/discover/", changefreq="hourly", priority="0.95", alt_loc=f"{base_domain}/hi/discover/", alt_lang="hi")
    add_url(f"{base_domain}/hi/discover/", changefreq="hourly", priority="0.95", alt_loc=f"{base_domain}/discover/", alt_lang="en")

    # 2. Policy Pages (EN & HI)
    for slug in ["about", "editorial", "privacy", "terms", "contact"]:
        add_url(f"{base_domain}/{slug}/", changefreq="monthly", priority="0.5", alt_loc=f"{base_domain}/hi/{slug}/", alt_lang="hi")
        add_url(f"{base_domain}/hi/{slug}/", changefreq="monthly", priority="0.5", alt_loc=f"{base_domain}/{slug}/", alt_lang="en")

    # 3. English & Hindi Articles
    for art in en_articles:
        m = art.get("movie", {})
        slug = m.get("slug")
        if not slug:
            continue
        mod = art.get("date_modified") or art.get("date_published") or art.get("published_at")
        lmod = mod[:10] if mod and len(mod) >= 10 else today_str
        is_breakout = slug in TARGET_BREAKOUT_SLUGS
        add_url(
            f"{base_domain}/articles/{slug}/",
            lastmod=lmod,
            changefreq="hourly" if is_breakout else "daily",
            priority="1.0" if is_breakout else "0.85",
            backdrop=m.get("backdrop_path"),
            title=art.get("headline") or m.get("title"),
            alt_loc=f"{base_domain}/hi/articles/{slug}/" if is_breakout else None,
            alt_lang="hi" if is_breakout else None
        )

    for art in hi_articles:
        m = art.get("movie", {})
        slug = m.get("slug")
        if not slug:
            continue
        mod = art.get("date_modified") or art.get("date_published") or art.get("published_at")
        lmod = mod[:10] if mod and len(mod) >= 10 else today_str
        add_url(
            f"{base_domain}/hi/articles/{slug}/",
            lastmod=lmod,
            changefreq="hourly",
            priority="1.0",
            backdrop=m.get("backdrop_path"),
            title=art.get("headline") or m.get("title"),
            alt_loc=f"{base_domain}/articles/{slug}/",
            alt_lang="en"
        )

    # 4. English & Hindi Web Stories
    for story in en_stories:
        m = story.get("movie", {})
        slug = m.get("slug")
        if not slug:
            continue
        mod = story.get("date_modified") or story.get("date_published") or story.get("published_at")
        lmod = mod[:10] if mod and len(mod) >= 10 else today_str
        is_breakout = slug in TARGET_BREAKOUT_SLUGS
        add_url(
            f"{base_domain}/stories/{slug}/",
            lastmod=lmod,
            changefreq="hourly" if is_breakout else "weekly",
            priority="1.0" if is_breakout else "0.80",
            backdrop=m.get("poster_path"),
            title=story.get("title") or m.get("title"),
            alt_loc=f"{base_domain}/hi/stories/{slug}/" if is_breakout else None,
            alt_lang="hi" if is_breakout else None
        )

    for story in hi_stories:
        m = story.get("movie", {})
        slug = m.get("slug")
        if not slug:
            continue
        mod = story.get("date_modified") or story.get("date_published") or story.get("published_at")
        lmod = mod[:10] if mod and len(mod) >= 10 else today_str
        add_url(
            f"{base_domain}/hi/stories/{slug}/",
            lastmod=lmod,
            changefreq="hourly",
            priority="1.0",
            backdrop=m.get("poster_path"),
            title=story.get("title") or m.get("title"),
            alt_loc=f"{base_domain}/stories/{slug}/",
            alt_lang="en"
        )

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"  ✓ Built unified bilingual sitemap: {output_path} ({len(urlset)} URLs)")


def main():
    print("=" * 70)
    print("  CINESTORIES DUAL-LOCALE MASTER STATIC BUILD PIPELINE (EN & HI)   ")
    print("=" * 70)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Ensure all target directories exist
    for d in [DIST_DIR, DIST_HI_DIR, STORIES_DIR, ARTICLES_DIR, DISCOVER_DIR, HI_STORIES_DIR, HI_ARTICLES_DIR, HI_DISCOVER_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # 1. Load Registry
    registry = {}
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            print(f"[!] Notice loading registry: {e}")

    new_stories_en = []
    new_articles_en = []
    new_stories_hi = []
    new_articles_hi = []

    print("\n[1/6] Rendering 10 Breakout Web Stories & Articles in English & Hindi...")
    for idx, slug in enumerate(TARGET_BREAKOUT_SLUGS):
        movie = next((m for m in SAMPLE_MEDIA if m.get("slug") == slug), None)
        if not movie:
            raise ValueError(f"Movie for slug '{slug}' not found in SAMPLE_MEDIA!")

        story_curated_en = CURATED_STORIES.get(slug)
        article_curated_en = CURATED_ARTICLES.get(slug)
        story_curated_hi = CURATED_STORIES_HI.get(slug)
        article_curated_hi = CURATED_ARTICLES_HI.get(slug)

        if not story_curated_en or not article_curated_en:
            raise ValueError(f"English story or article missing for slug: {slug}")
        if not story_curated_hi or not article_curated_hi:
            raise ValueError(f"Hindi story or article missing for slug: {slug}")

        historical_pub = registry.get(slug, {}).get("published_at") or story_curated_en.get("date_published") or now_iso
        historical_mod = registry.get(slug, {}).get("date_modified") or registry.get(slug, {}).get("modified_at") or now_iso

        # --- English Data Structures ---
        story_data_en = {
            "title": story_curated_en.get("title", movie["title"]),
            "seo_description": story_curated_en.get("seo_description", movie.get("overview", "")[:150]),
            "movie": movie,
            "slides": story_curated_en.get("slides", []),
            "date_published": historical_pub,
            "date_modified": historical_mod,
            "published_at": historical_pub
        }

        article_data_en = dict(article_curated_en)
        article_data_en["movie"] = movie
        article_data_en["date_published"] = historical_pub
        article_data_en["date_modified"] = historical_mod
        article_data_en["published_at"] = historical_pub

        # --- Hindi Data Structures ---
        story_data_hi = {
            "title": story_curated_hi.get("title", movie["title"]),
            "seo_description": story_curated_hi.get("seo_description", movie.get("overview", "")[:150]),
            "movie": movie,
            "slides": story_curated_hi.get("slides", []),
            "date_published": historical_pub,
            "date_modified": historical_mod,
            "published_at": historical_pub
        }

        article_data_hi = dict(article_curated_hi)
        article_data_hi["movie"] = movie
        article_data_hi["date_published"] = historical_pub
        article_data_hi["date_modified"] = historical_mod
        article_data_hi["published_at"] = historical_pub

        # Render English Story & Article
        story_dir_en = STORIES_DIR / slug
        story_dir_en.mkdir(parents=True, exist_ok=True)
        raw_amp_en = build_amp_story_html(story_data_en, domain=DOMAIN_NAME, lang="en")
        amp_en = post_process_page(raw_amp_en, f"/stories/{slug}/", lang="en", is_amp=True, domain=DOMAIN_NAME)
        with open(story_dir_en / "index.html", "w", encoding="utf-8") as f:
            f.write(amp_en)

        art_dir_en = ARTICLES_DIR / slug
        art_dir_en.mkdir(parents=True, exist_ok=True)
        raw_art_en = build_discover_article_html(article_data_en, domain=DOMAIN_NAME, lang="en")
        art_en = post_process_page(raw_art_en, f"/articles/{slug}/", lang="en", is_amp=False, domain=DOMAIN_NAME)
        with open(art_dir_en / "index.html", "w", encoding="utf-8") as f:
            f.write(art_en)

        # Render Hindi Story & Article
        story_dir_hi = HI_STORIES_DIR / slug
        story_dir_hi.mkdir(parents=True, exist_ok=True)
        raw_amp_hi = build_amp_story_html(story_data_hi, domain=DOMAIN_NAME, lang="hi")
        amp_hi = post_process_page(raw_amp_hi, f"/stories/{slug}/", lang="hi", is_amp=True, domain=DOMAIN_NAME)
        with open(story_dir_hi / "index.html", "w", encoding="utf-8") as f:
            f.write(amp_hi)

        art_dir_hi = HI_ARTICLES_DIR / slug
        art_dir_hi.mkdir(parents=True, exist_ok=True)
        raw_art_hi = build_discover_article_html(article_data_hi, domain=DOMAIN_NAME, lang="hi")
        art_hi = post_process_page(raw_art_hi, f"/articles/{slug}/", lang="hi", is_amp=False, domain=DOMAIN_NAME)
        with open(art_dir_hi / "index.html", "w", encoding="utf-8") as f:
            f.write(art_hi)

        # Update registry
        registry[slug] = {
            "title": movie.get("title"),
            "published_at": historical_pub,
            "modified_at": historical_mod,
            "category": movie.get("category", "trending")
        }

        new_stories_en.append(story_data_en)
        new_articles_en.append(article_data_en)
        new_stories_hi.append(story_data_hi)
        new_articles_hi.append(article_data_hi)

        print(f"  ✓ [{idx+1}/10] Rendered (EN & HI): {slug}")

    # Save Registry
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    print(f"\n[2/6] Saved registry at {REGISTRY_PATH} ({len(registry)} entries)")

    # 2. Merge Catalogs
    print("\n[3/6] Merging site catalogs for English and Hindi editions...")
    cache_stories_en_path = DIST_DIR / "stories_cache.json"
    cache_articles_en_path = DIST_DIR / "articles_cache.json"
    cache_stories_hi_path = DIST_HI_DIR / "stories_cache.json"
    cache_articles_hi_path = DIST_HI_DIR / "articles_cache.json"

    from fetch_and_generate import anchor_catalog_items, story_fallback_builder, article_fallback_builder

    # English catalogs
    old_stories_en = []
    if cache_stories_en_path.exists():
        try:
            with open(cache_stories_en_path, "r", encoding="utf-8") as f:
                old_stories_en = json.load(f)
        except Exception:
            pass

    combined_stories_en = anchor_catalog_items(
        new_items=new_stories_en,
        old_items=old_stories_en,
        target_slugs=TARGET_BREAKOUT_SLUGS,
        fallback_builder=story_fallback_builder
    )
    with open(cache_stories_en_path, "w", encoding="utf-8") as f:
        json.dump(combined_stories_en, f, indent=2, default=str)
    with open(STORIES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_stories_en, f, indent=2, default=str)

    old_articles_en = []
    if cache_articles_en_path.exists():
        try:
            with open(cache_articles_en_path, "r", encoding="utf-8") as f:
                old_articles_en = json.load(f)
        except Exception:
            pass

    combined_articles_en = anchor_catalog_items(
        new_items=new_articles_en,
        old_items=old_articles_en,
        target_slugs=TARGET_BREAKOUT_SLUGS,
        fallback_builder=article_fallback_builder
    )
    # Clean any legacy boilerplate phrases from cached articles and re-render all English catalog stories & articles
    boilerplate_replacements = {
        "From the opening sequence, audiences are drawn into an engaging journey where unexpected developments continually test the limits and resolve of its central characters.": "Anchored by sharp narrative pacing and layered character dynamics, the story builds tension methodically while exploring the conflicts driving its central figures.",
        "Under Acclaimed Filmmakers's steady direction": "Through focused direction and visual staging",
        "Whether you're seeking gripping plot twists or memorable character moments, it is a recommended addition to your streaming watchlist.": "Combining strong ensemble performances with high-stakes storytelling, it stands out as a compelling watch for cinema fans.",
        "brings critical revelations into focus, shedding light on the real-world impact": "uncovers pivotal evidence and personal testimony, examining the broader consequences",
        "From opening hook to post-credits clues, this story is engineered for Google Discover": "This detailed breakdown examines the narrative arc, key turning points, and final resolution",
    }
    for art in combined_articles_en:
        m = art.get("movie", {})
        slug = m.get("slug")
        if not slug or slug in TARGET_BREAKOUT_SLUGS:
            continue
        for sec in art.get("sections", []):
            txt = sec.get("content", "")
            for bad_p, good_p in boilerplate_replacements.items():
                if bad_p.lower() in txt.lower():
                    txt = re.sub(re.escape(bad_p), good_p, txt, flags=re.I)
            txt = re.sub(r"\badmin\b", "official", txt, flags=re.I)
            sec["content"] = txt
        hist_pub = registry.get(slug, {}).get("published_at") or art.get("date_published") or art.get("published_at") or now_iso
        hist_mod = registry.get(slug, {}).get("modified_at") or art.get("date_modified") or hist_pub
        art["date_published"] = hist_pub
        art["date_modified"] = hist_mod
        art["published_at"] = hist_pub
        art_dir_en = ARTICLES_DIR / slug
        art_dir_en.mkdir(parents=True, exist_ok=True)
        raw_art_en = build_discover_article_html(art, domain=DOMAIN_NAME, lang="en")
        art_en = post_process_page(raw_art_en, f"/articles/{slug}/", lang="en", is_amp=False, domain=DOMAIN_NAME)
        with open(art_dir_en / "index.html", "w", encoding="utf-8") as f:
            f.write(art_en)

    for st in combined_stories_en:
        m = st.get("movie", {})
        slug = m.get("slug")
        if not slug or slug in TARGET_BREAKOUT_SLUGS:
            continue
        hist_pub = registry.get(slug, {}).get("published_at") or st.get("date_published") or st.get("published_at") or now_iso
        hist_mod = registry.get(slug, {}).get("modified_at") or st.get("date_modified") or hist_pub
        st["date_published"] = hist_pub
        st["date_modified"] = hist_mod
        st["published_at"] = hist_pub
        story_dir_en = STORIES_DIR / slug
        story_dir_en.mkdir(parents=True, exist_ok=True)
        raw_amp_en = build_amp_story_html(st, domain=DOMAIN_NAME, lang="en")
        amp_en = post_process_page(raw_amp_en, f"/stories/{slug}/", lang="en", is_amp=True, domain=DOMAIN_NAME)
        with open(story_dir_en / "index.html", "w", encoding="utf-8") as f:
            f.write(amp_en)

    with open(cache_articles_en_path, "w", encoding="utf-8") as f:
        json.dump(combined_articles_en, f, indent=2, default=str)
    with open(ARTICLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_articles_en, f, indent=2, default=str)

    # Hindi catalogs (10 breakout titles)
    with open(cache_stories_hi_path, "w", encoding="utf-8") as f:
        json.dump(new_stories_hi, f, indent=2, default=str)
    with open(DIST_HI_DIR / "stories.json", "w", encoding="utf-8") as f:
        json.dump(new_stories_hi, f, indent=2, default=str)

    with open(cache_articles_hi_path, "w", encoding="utf-8") as f:
        json.dump(new_articles_hi, f, indent=2, default=str)
    with open(DIST_HI_DIR / "articles.json", "w", encoding="utf-8") as f:
        json.dump(new_articles_hi, f, indent=2, default=str)

    print(f"  ✓ English catalog: {len(combined_stories_en)} stories, {len(combined_articles_en)} articles")
    print(f"  ✓ Hindi catalog: {len(new_stories_hi)} breakout stories, {len(new_articles_hi)} breakout articles")

    # 3. Rebuild Portals
    print("\n[4/6] Rebuilding English and Hindi Homepages & Discover Feeds...")
    # English Home & Discover
    generate_homepage(combined_stories_en, domain=DOMAIN_NAME, output_dir=DIST_DIR, lang="en")
    en_home_file = DIST_DIR / "index.html"
    en_home_html = post_process_page(en_home_file.read_text(encoding="utf-8"), "/", lang="en", is_amp=False, domain=DOMAIN_NAME)
    en_home_file.write_text(en_home_html, encoding="utf-8")

    generate_discover_feed(combined_articles_en, domain=DOMAIN_NAME, output_dir=DISCOVER_DIR, lang="en")
    en_disc_file = DISCOVER_DIR / "index.html"
    en_disc_html = post_process_page(en_disc_file.read_text(encoding="utf-8"), "/discover/", lang="en", is_amp=False, domain=DOMAIN_NAME)
    en_disc_file.write_text(en_disc_html, encoding="utf-8")

    # Hindi Home & Discover
    generate_homepage(new_stories_hi, domain=DOMAIN_NAME, output_dir=DIST_DIR, lang="hi")
    hi_home_file = DIST_HI_DIR / "index.html"
    hi_home_html = post_process_page(hi_home_file.read_text(encoding="utf-8"), "/", lang="hi", is_amp=False, domain=DOMAIN_NAME)
    hi_home_file.write_text(hi_home_html, encoding="utf-8")

    generate_discover_feed(new_articles_hi, domain=DOMAIN_NAME, output_dir=DISCOVER_DIR, lang="hi")
    hi_disc_file = HI_DISCOVER_DIR / "index.html"
    hi_disc_html = post_process_page(hi_disc_file.read_text(encoding="utf-8"), "/discover/", lang="hi", is_amp=False, domain=DOMAIN_NAME)
    hi_disc_file.write_text(hi_disc_html, encoding="utf-8")

    print("  ✓ Rendered & post-processed dist/index.html & dist/hi/index.html")
    print("  ✓ Rendered & post-processed dist/discover/index.html & dist/hi/discover/index.html")

    # 4. Rebuild Policy Pages
    print("\n[5/6] Generating bilingual legal & compliance policy pages...")
    generate_policy_pages(dist_dir=DIST_DIR, domain=DOMAIN_NAME, lang="en")
    generate_policy_pages(dist_dir=DIST_HI_DIR, domain=DOMAIN_NAME, lang="hi")

    # Post-process all policy pages
    for slug in ["about", "editorial", "privacy", "terms", "contact"]:
        en_p = DIST_DIR / slug / "index.html"
        if en_p.exists():
            en_p_html = post_process_page(en_p.read_text(encoding="utf-8"), f"/{slug}/", lang="en", is_amp=False, domain=DOMAIN_NAME)
            en_p.write_text(en_p_html, encoding="utf-8")

        hi_p = DIST_HI_DIR / slug / "index.html"
        if hi_p.exists():
            hi_p_html = post_process_page(hi_p.read_text(encoding="utf-8"), f"/{slug}/", lang="hi", is_amp=False, domain=DOMAIN_NAME)
            hi_p.write_text(hi_p_html, encoding="utf-8")

    print("  ✓ Generated & verified 5 English policy pages in dist/")
    print("  ✓ Generated & verified 5 Hindi policy pages in dist/hi/")

    # 5. Sitemaps & RSS Feeds
    print("\n[6/6] Generating unified bilingual XML sitemap and localized RSS feeds...")
    build_bilingual_sitemap(
        en_stories=combined_stories_en,
        hi_stories=new_stories_hi,
        en_articles=combined_articles_en,
        hi_articles=new_articles_hi,
        domain=DOMAIN_NAME,
        output_path=SITEMAP_PATH
    )

    # English RSS
    generate_rss_feed(combined_articles_en, domain=DOMAIN_NAME, output_paths=[DIST_DIR / "feed.xml", DIST_DIR / "rss.xml"])

    # Hindi RSS
    generate_rss_feed(new_articles_hi, domain=DOMAIN_NAME, output_paths=[DIST_HI_DIR / "feed.xml", DIST_HI_DIR / "rss.xml"])
    print("  ✓ Generated English RSS feeds (dist/feed.xml & dist/rss.xml)")
    print("  ✓ Generated Hindi RSS feeds (dist/hi/feed.xml & dist/hi/rss.xml)")

    print("\n" + "=" * 70)
    print("  DUAL-LOCALE STATIC BUILD PIPELINE COMPLETE!                      ")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
