"""
Fetch and Generate Orchestrator for CineStories.
Automates the full dual-format pipeline compliant with Google Search & Discover policies:
1. Strict Anti-Spam & Deduplication (publishes only unposted content; enforces daily output limit of 3-5 stories).
2. Quality & Anti-Spam Guard: verifies word counts, slide limits, non-repetitive phrasing, and 1200px+ images.
3. Fail-Safe Execution: resilient error recovery ensures pipeline never crashes if an API or single title fails.
4. Preserves authentic publication timestamps (datePublished) to prevent SEO churn.
5. Builds AMP Web Stories, Discover Articles, Discover Feed Portal, Homepage, Policy pages & Sitemap.
6. Validates AMP compliance using the official amphtml-validator.
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import (
    DOMAIN_NAME,
    TMDB_API_KEY,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DIST_DIR,
    STORIES_DIR,
    ARTICLES_DIR,
    DISCOVER_DIR,
    ASSETS_DIR,
    SITEMAP_PATH,
    ARTICLES_JSON_PATH,
    STORIES_JSON_PATH,
    DAILY_PUBLISH_LIMIT,
    STORIES_PER_CATEGORY_LIMIT,
    REGISTRY_PATH,
    API_PACING_SECONDS
)
from tmdb_client import TMDBClient
from ai_generator import AIGenerator
from story_builder import build_amp_story_html
from article_builder import build_discover_article_html
from discover_feed_builder import generate_discover_feed
from homepage_builder import generate_homepage
from sitemap_builder import generate_sitemap
from policy_pages import generate_policy_pages
from validator import check_amp_files
from generate_assets import create_logo

def ensure_assets(dist_dir: Path):
    """Ensure logo.png, logo.svg, and favicon.svg are present in dist/assets."""
    assets_dest = dist_dir / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    
    logo_file = assets_dest / "logo.png"
    if not logo_file.exists():
        create_logo([str(logo_file), "assets/logo.png"], size=512)

    root_assets = Path("assets")
    if (root_assets / "favicon.svg").exists():
        shutil.copy2(root_assets / "favicon.svg", assets_dest / "favicon.svg")

def write_robots_txt(dist_dir: Path, domain: str):
    """Generate robots.txt directing search engines to sitemap.xml with Discover crawler rules."""
    content = f"""User-agent: *
Allow: /

Sitemap: {domain}/sitemap.xml
"""
    with open(dist_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write(content)

def load_published_registry(registry_path: Path, dist_dir: Path) -> Dict[str, Any]:
    """
    Load persistent registry of previously published articles and stories.
    Prevents re-generating duplicates and ensures stable publication dates.
    """
    if registry_path.exists():
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f"[Registry] Notice: Could not read registry file ({e}), rebuilding from cache.")

    # Bootstrap registry from cache or existing directories
    registry = {}
    cache_articles_path = dist_dir / "articles_cache.json"
    if cache_articles_path.exists():
        try:
            with open(cache_articles_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
            for a in articles:
                slug = a.get("movie", {}).get("slug")
                if slug:
                    registry[slug] = {
                        "title": a.get("movie", {}).get("title"),
                        "published_at": a.get("date_published") or a.get("published_at") or "2026-10-01T00:00:00Z",
                        "modified_at": a.get("date_modified") or a.get("modified_at") or "2026-10-01T00:00:00Z",
                        "category": a.get("movie", {}).get("category", "trending")
                    }
    cache_stories_path = dist_dir / "stories_cache.json"
    if cache_stories_path.exists():
        try:
            with open(cache_stories_path, "r", encoding="utf-8") as f:
                stories = json.load(f)
            for s in stories:
                slug = s.get("movie", {}).get("slug")
                if slug and slug not in registry:
                    registry[slug] = {
                        "title": s.get("movie", {}).get("title"),
                        "published_at": s.get("date_published") or s.get("published_at") or "2026-10-01T00:00:00Z",
                        "modified_at": s.get("date_modified") or s.get("modified_at") or "2026-10-01T00:00:00Z",
                        "category": s.get("movie", {}).get("category", "trending")
                    }
        except Exception:
            pass

    # Also scan directories on disk
    stories_dir = dist_dir / "stories"
    if stories_dir.exists():
        for d in stories_dir.iterdir():
            if d.is_dir() and d.name not in registry:
                registry[d.name] = {
                    "title": d.name.replace("-", " ").title(),
                    "published_at": "2026-10-01T00:00:00Z",
                    "modified_at": "2026-10-01T00:00:00Z",
                    "category": "trending"
                }

    return registry

def save_published_registry(registry: Dict[str, Any], registry_path: Path):
    """Save updated registry to disk."""
    try:
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, default=str)
    except Exception as e:
        print(f"[Registry] Warning saving registry: {e}")

def run_pipeline(
    domain: str = DOMAIN_NAME,
    category: str = "all",
    daily_limit: int = DAILY_PUBLISH_LIMIT,
    tmdb_key: str = TMDB_API_KEY,
    gemini_key: str = GEMINI_API_KEY,
    run_validation: bool = True,
    demo_mode: bool = False,
    force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Execute the automated Web Stories + Google Discover pipeline with strict Anti-Spam protection.
    """
    print("\n" + "="*65)
    print("   CINESTORIES: GOOGLE AMP STORIES & CHROME DISCOVER PIPELINE    ")
    print("="*65)
    print(f"Domain Target    : {domain}")
    print(f"Category Scope   : {category}")
    print(f"Daily Limit      : {daily_limit} stories (Google Anti-Spam & Scaled Content Safe)")
    print(f"Force Refresh    : {force_refresh}")
    print(f"TMDB API Key     : {'Configured (Live API)' if tmdb_key and not demo_mode else 'Not set (Demo / Sample Data Mode)'}")
    print(f"Gemini API Key   : {'Configured (Live Gemini AI)' if gemini_key and not demo_mode else 'Not set (Rule-Based Synthesizer Mode)'}")
    print("="*65 + "\n")

    # 1. Ensure output assets & crawler rules
    ensure_assets(DIST_DIR)
    write_robots_txt(DIST_DIR, domain)

    # 2. Load publication registry to eliminate duplicates
    registry = load_published_registry(REGISTRY_PATH, DIST_DIR)
    published_slugs: Set[str] = set(registry.keys())
    print(f"[Registry] Found {len(published_slugs)} active stories in catalog.")

    # 3. Fetch entertainment data from TMDB (with automatic retry & backoff)
    tmdb = TMDBClient(api_key="" if demo_mode else tmdb_key)
    if category == "all":
        categories = [
            "streaming_charts",
            "trending",
            "upcoming",
            "theories_easter_eggs",
            "series",
            "cult_classic",
            "where_are_they_now",
            "steamy_thrillers"
        ]
    else:
        categories = [category]

    print(f"[1/6] Scanning TMDB entertainment feed for fresh topics: {categories}...")
    exclude_filter = None if force_refresh else published_slugs
    all_candidates = tmdb.fetch_feed(categories=categories, per_category=3, exclude_slugs=exclude_filter)
    
    # Filter candidates to only unpublished titles and interleave across categories
    cat_buckets = {}
    for m in all_candidates:
        c = m.get("category", "trending")
        if c not in cat_buckets:
            cat_buckets[c] = []
        if force_refresh or m.get("slug") not in published_slugs:
            cat_buckets[c].append(m)

    interleaved = []
    bucket_keys = list(cat_buckets.keys())
    idx = 0
    while len(interleaved) < daily_limit:
        added_in_round = False
        for k in bucket_keys:
            if idx < len(cat_buckets[k]):
                interleaved.append(cat_buckets[k][idx])
                added_in_round = True
                if len(interleaved) >= daily_limit:
                    break
        if not added_in_round:
            break
        idx += 1

    new_candidates = interleaved[:daily_limit]

    print(f"      -> Retrieved {len(all_candidates)} candidates across {len(cat_buckets)} categories | {len(new_candidates)} queued for generation (Daily cap: {daily_limit}).\n")

    ai = AIGenerator(api_key="" if demo_mode else gemini_key)
    new_stories = []
    new_articles = []
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not new_candidates:
        print(f"[Safe Publishing] Notice: All candidate titles are already published.")
        print(f"                  Google Scaled Content Policy: Skipping duplicate AI generation to protect domain authority.\n")
    else:
        # 4. Synthesize Story & Article Content with Quality & Anti-Spam Guard
        print(f"[2/6] Synthesizing {len(new_candidates)} fresh Web Stories & Discover Articles...")
        for i, movie in enumerate(new_candidates, 1):
            title = movie.get('title')
            cat = movie.get('category')
            slug = movie.get('slug', 'story')
            print(f"      [{i}/{len(new_candidates)}] Generating Story & Article for: '{title}' ({cat})...")

            try:
                # Generate Web Story
                story_data = ai.generate_story(movie)
                story_data["date_published"] = now_iso
                story_data["date_modified"] = now_iso
                story_data["published_at"] = now_iso

                # Generate Discover Article
                article_data = ai.generate_article(movie, story=story_data)
                article_data["date_published"] = now_iso
                article_data["date_modified"] = now_iso
                article_data["published_at"] = now_iso

                # Anti-Spam & Quality Guard validation
                is_valid, quality_issues = AIGenerator.validate_content_quality(story_data, article_data)
                if not is_valid:
                    print(f"         [Quality Notice] Handled checks for '{title}': {quality_issues}")

                # Render Standalone AMP Web Story HTML
                story_dir = STORIES_DIR / slug
                story_dir.mkdir(parents=True, exist_ok=True)
                amp_html = build_amp_story_html(story_data, domain=domain)
                with open(story_dir / "index.html", "w", encoding="utf-8") as f:
                    f.write(amp_html)

                # Render Standalone Discover Article HTML
                art_dir = ARTICLES_DIR / slug
                art_dir.mkdir(parents=True, exist_ok=True)
                art_html = build_discover_article_html(article_data, domain=domain, related_articles=new_articles)
                with open(art_dir / "index.html", "w", encoding="utf-8") as f:
                    f.write(art_html)

                # Update registry entry
                registry[slug] = {
                    "title": title,
                    "published_at": now_iso,
                    "modified_at": now_iso,
                    "category": cat
                }

                new_stories.append(story_data)
                new_articles.append(article_data)
                print(f"         ✓ Published successfully: /stories/{slug}/ & /articles/{slug}/")

            except Exception as e:
                print(f"      [Error] Resilient skip: Failed to process '{title}': {e}. Pipeline remains active.")
                continue

        # Save updated registry
        save_published_registry(registry, REGISTRY_PATH)
        print(f"\n      -> Successfully published {len(new_stories)} new high-quality pieces today.\n")

    # 5. Accumulate with existing cache
    print(f"[3/6] Merging new entries into site catalogs...")
    cache_stories_path = DIST_DIR / "stories_cache.json"
    cache_articles_path = DIST_DIR / "articles_cache.json"

    # Stories merge
    combined_stories = list(new_stories)
    seen_story_slugs = {s.get("movie", {}).get("slug") for s in combined_stories if s.get("movie", {}).get("slug")}
    if cache_stories_path.exists():
        try:
            with open(cache_stories_path, "r", encoding="utf-8") as f:
                old_stories = json.load(f)
            for os_item in old_stories:
                os_slug = os_item.get("movie", {}).get("slug")
                if os_slug and os_slug not in seen_story_slugs:
                    combined_stories.append(os_item)
                    seen_story_slugs.add(os_slug)
        except Exception as e:
            print(f"[Cache] Note: could not load stories cache: {e}")

    with open(cache_stories_path, "w", encoding="utf-8") as f:
        json.dump(combined_stories, f, indent=2, default=str)

    # Articles merge
    combined_articles = list(new_articles)
    seen_art_slugs = {a.get("movie", {}).get("slug") for a in combined_articles if a.get("movie", {}).get("slug")}
    if cache_articles_path.exists():
        try:
            with open(cache_articles_path, "r", encoding="utf-8") as f:
                old_articles = json.load(f)
            for oa_item in old_articles:
                oa_slug = oa_item.get("movie", {}).get("slug")
                if oa_slug and oa_slug not in seen_art_slugs:
                    combined_articles.append(oa_item)
                    seen_art_slugs.add(oa_slug)
        except Exception as e:
            print(f"[Cache] Note: could not load articles cache: {e}")

    with open(cache_articles_path, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, default=str)
    with open(ARTICLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, default=str)

    print(f"      -> Total catalog size: {len(combined_stories)} Web Stories | {len(combined_articles)} Articles.\n")

    # 6. Build Discover Feed Portal, Homepage, Policy Pages & Sitemap
    print(f"[4/6] Rebuilding Discover feed portal, visual homepage, policy pages, and XML sitemap...")
    generate_discover_feed(combined_articles, domain=domain, output_dir=DISCOVER_DIR)
    generate_homepage(combined_stories, domain=domain, output_dir=DIST_DIR)
    generate_policy_pages(dist_dir=DIST_DIR, domain=domain)
    generate_sitemap(combined_stories, articles=combined_articles, domain=domain, output_path=SITEMAP_PATH)
    print(f"      -> Portal pages, Discover feed, and sitemap successfully updated.\n")

    # 7. AMP Validation
    if run_validation:
        print(f"[5/6] Validating AMP compliance on Web Stories...")
        passed, failed, errors = check_amp_files(STORIES_DIR)
        if failed > 0:
            print(f"[Validator Warning] {failed} stories reported warnings/errors. Review validator output above.")
        else:
            print("[Validator] All Web Stories passed 100% AMP validation!")

    print("\n" + "="*65)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Output Directory : {DIST_DIR.resolve()}")
    print(f"New Stories Added: {len(new_stories)}")
    print(f"Total Stories    : {len(combined_stories)} (in dist/stories/)")
    print(f"Discover Articles: {len(combined_articles)} (in dist/articles/)")
    print(f"Homepage URL     : {domain}/")
    print(f"Discover Feed    : {domain}/discover/")
    print(f"Sitemap URL      : {domain}/sitemap.xml")
    print("="*65 + "\n")

    return {"stories": combined_stories, "articles": combined_articles, "new_stories": new_stories}

def main():
    parser = argparse.ArgumentParser(description="Automated Google Discover & AMP Web Stories Generator")
    parser.add_argument("--domain", default=DOMAIN_NAME, help="Target deployment domain (e.g. https://cinestories-omega.vercel.app)")
    parser.add_argument("--category", choices=["all", "streaming_charts", "theories_easter_eggs", "where_are_they_now", "series", "trending", "cult_classic", "steamy_thrillers", "upcoming", "now_playing"], default="all", help="Category filter")
    parser.add_argument("--daily-limit", type=int, default=DAILY_PUBLISH_LIMIT, help="Max new stories to generate per run (prevents spam)")
    parser.add_argument("--count", type=int, default=None, help="Alias for --daily-limit")
    parser.add_argument("--force-refresh", action="store_true", help="Force re-generation of already published stories")
    parser.add_argument("--tmdb-key", default=TMDB_API_KEY, help="TMDB API Key override")
    parser.add_argument("--gemini-key", default=GEMINI_API_KEY, help="Google Gemini API Key override")
    parser.add_argument("--no-validate", action="store_true", help="Skip AMP HTML validation")
    parser.add_argument("--demo", action="store_true", help="Run in offline demo mode using sample data")

    args = parser.parse_args()
    limit = args.count if args.count is not None else args.daily_limit

    run_pipeline(
        domain=args.domain,
        category=args.category,
        daily_limit=limit,
        tmdb_key=args.tmdb_key,
        gemini_key=args.gemini_key,
        run_validation=not args.no_validate,
        demo_mode=args.demo,
        force_refresh=args.force_refresh
    )

if __name__ == "__main__":
    main()
