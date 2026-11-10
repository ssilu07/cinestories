"""
Dedicated, high-fidelity generator script for the CineStories 10 Breakout Viral Content Slate.
Builds all 10 AMP Web Stories, Discover Articles, updates caches/registries, and regenerates
the visual homepage, Discover feed, XML sitemap, and RSS feeds.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

from config import (
    DOMAIN_NAME,
    DIST_DIR,
    STORIES_DIR,
    ARTICLES_DIR,
    DISCOVER_DIR,
    SITEMAP_PATH,
    ARTICLES_JSON_PATH,
    STORIES_JSON_PATH,
    REGISTRY_PATH
)
from sample_data import SAMPLE_MEDIA
from curated_stories import CURATED_STORIES
from curated_articles import CURATED_ARTICLES
from story_builder import build_amp_story_html
from article_builder import build_discover_article_html
from homepage_builder import generate_homepage
from discover_feed_builder import generate_discover_feed
from sitemap_builder import generate_sitemap
from feed_builder import generate_rss_feed

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

def main():
    print("=" * 65)
    print("STARTING CINESTORIES VIRAL CONTENT SLATE GENERATION")
    print("=" * 65)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Load registry
    registry = {}
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            print(f"[!] Notice loading registry: {e}")

    new_stories = []
    new_articles = []

    print(f"\n[1/5] Authoring & rendering 10 breakout Web Stories & Articles...")
    for idx, slug in enumerate(TARGET_BREAKOUT_SLUGS):
        movie = next((m for m in SAMPLE_MEDIA if m.get("slug") == slug), None)
        if not movie:
            raise ValueError(f"Movie for slug '{slug}' not found in SAMPLE_MEDIA!")

        story_curated = CURATED_STORIES.get(slug)
        if not story_curated:
            raise ValueError(f"Story for slug '{slug}' not found in CURATED_STORIES!")

        article_curated = CURATED_ARTICLES.get(slug)
        if not article_curated:
            raise ValueError(f"Article for slug '{slug}' not found in CURATED_ARTICLES!")

        # Build story data structure
        story_data = {
            "title": story_curated.get("title", movie["title"]),
            "seo_description": story_curated.get("seo_description", movie.get("overview", "")[:150]),
            "movie": movie,
            "slides": story_curated.get("slides", []),
            "date_published": now_iso,
            "date_modified": now_iso,
            "published_at": now_iso
        }

        # Build article data structure
        article_data = dict(article_curated)
        article_data["movie"] = movie
        article_data["date_published"] = now_iso
        article_data["date_modified"] = now_iso
        article_data["published_at"] = now_iso

        # Render Standalone AMP Web Story HTML
        story_dir = STORIES_DIR / slug
        story_dir.mkdir(parents=True, exist_ok=True)
        amp_html = build_amp_story_html(story_data, domain=DOMAIN_NAME)
        with open(story_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Render Standalone Discover Article HTML
        art_dir = ARTICLES_DIR / slug
        art_dir.mkdir(parents=True, exist_ok=True)
        art_html = build_discover_article_html(article_data, domain=DOMAIN_NAME)
        with open(art_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(art_html)

        # Update registry
        registry[slug] = {
            "title": movie.get("title"),
            "published_at": now_iso,
            "modified_at": now_iso,
            "category": movie.get("category", "trending")
        }

        new_stories.append(story_data)
        new_articles.append(article_data)
        print(f"  ✓ [{idx+1}/10] Rendered: /stories/{slug}/ & /articles/{slug}/")

    # Save registry
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    print(f"\n[2/5] Saved updated registry at {REGISTRY_PATH} ({len(registry)} entries)")

    # 2. Merge catalogs (prepending the 10 breakout titles)
    print("\n[3/5] Prepending 10 breakout titles at index 0..9 in site catalogs...")
    cache_stories_path = DIST_DIR / "stories_cache.json"
    cache_articles_path = DIST_DIR / "articles_cache.json"

    # Merge stories
    combined_stories = list(new_stories)
    seen_story_slugs = set(TARGET_BREAKOUT_SLUGS)
    if cache_stories_path.exists():
        try:
            with open(cache_stories_path, "r", encoding="utf-8") as f:
                old_stories = json.load(f)
            for s in old_stories:
                s_slug = s.get("movie", {}).get("slug")
                if s_slug and s_slug not in seen_story_slugs:
                    combined_stories.append(s)
                    seen_story_slugs.add(s_slug)
        except Exception as e:
            print(f"[!] Warning reading old stories cache: {e}")

    with open(cache_stories_path, "w", encoding="utf-8") as f:
        json.dump(combined_stories, f, indent=2, default=str)

    # Merge articles
    combined_articles = list(new_articles)
    seen_art_slugs = set(TARGET_BREAKOUT_SLUGS)
    if cache_articles_path.exists():
        try:
            with open(cache_articles_path, "r", encoding="utf-8") as f:
                old_articles = json.load(f)
            for a in old_articles:
                a_slug = a.get("movie", {}).get("slug")
                if a_slug and a_slug not in seen_art_slugs:
                    combined_articles.append(a)
                    seen_art_slugs.add(a_slug)
        except Exception as e:
            print(f"[!] Warning reading old articles cache: {e}")

    with open(cache_articles_path, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, default=str)
    with open(ARTICLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, default=str)

    print(f"  ✓ Updated stories_cache.json: {len(combined_stories)} total stories")
    print(f"  ✓ Updated articles_cache.json: {len(combined_articles)} total articles")

    # 3. Rebuild Portals, Sitemap, Feeds
    print("\n[4/5] Rebuilding Homepage, Discover Feed, Sitemap, and RSS Feeds...")
    generate_homepage(combined_stories, domain=DOMAIN_NAME, output_dir=DIST_DIR)
    generate_discover_feed(combined_articles, domain=DOMAIN_NAME, output_dir=DISCOVER_DIR)
    generate_sitemap(combined_stories, articles=combined_articles, domain=DOMAIN_NAME, output_path=SITEMAP_PATH)
    generate_rss_feed(combined_articles, domain=DOMAIN_NAME)
    print("  ✓ Rebuilt dist/index.html with Hero Carousel")
    print("  ✓ Rebuilt dist/discover/index.html with Spotlight Badges")
    print("  ✓ Rebuilt dist/sitemap.xml with priority 1.0 & hourly changefreq")
    print("  ✓ Rebuilt dist/feed.xml and dist/rss.xml")

    print("\n" + "=" * 65)
    print("VIRAL CONTENT SLATE GENERATION COMPLETE!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
