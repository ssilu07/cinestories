"""
Fetch and Generate Orchestrator for CineStories.
Automates the full dual-format pipeline:
1. Fetches top upcoming, streaming, and trending movies/shows from TMDB API.
2. Synthesizes high-engagement AMP Web Story slides via Gemini AI (with structured outputs).
3. Synthesizes 1200px+ Google Chrome Discover news articles with takeaways and deep-dive analysis.
4. Renders 100% AMP-valid standalone Web Story HTML files to dist/stories/[slug]/index.html.
5. Renders standalone Google Discover articles to dist/articles/[slug]/index.html.
6. Generates a mobile-first Google Chrome Discover feed at dist/discover/index.html.
7. Updates dist/sitemap.xml with both Web Stories and Discover articles (with image tags).
8. Renders the responsive visual portal at dist/index.html and legal policy pages.
9. Validates AMP compliance using the official amphtml-validator.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Any

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
    STORIES_PER_CATEGORY_LIMIT
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

def run_pipeline(
    domain: str = DOMAIN_NAME,
    category: str = "all",
    count_per_cat: int = STORIES_PER_CATEGORY_LIMIT,
    tmdb_key: str = TMDB_API_KEY,
    gemini_key: str = GEMINI_API_KEY,
    run_validation: bool = True,
    demo_mode: bool = False
) -> Dict[str, Any]:
    """
    Execute the end-to-end automated Web Stories + Google Discover pipeline.
    """
    print("\n" + "="*65)
    print("   CINESTORIES: GOOGLE AMP STORIES & CHROME DISCOVER PIPELINE    ")
    print("="*65)
    print(f"Domain Target    : {domain}")
    print(f"Category Scope   : {category}")
    print(f"Per-Category Max : {count_per_cat}")
    print(f"TMDB API Key     : {'Configured (Live API)' if tmdb_key and not demo_mode else 'Not set (Demo / Sample Data Mode)'}")
    print(f"Gemini API Key   : {'Configured (Live Gemini AI)' if gemini_key and not demo_mode else 'Not set (Rule-Based Synthesizer Mode)'}")
    print("="*65 + "\n")

    # 1. Ensure output assets
    ensure_assets(DIST_DIR)
    write_robots_txt(DIST_DIR, domain)

    # 2. Fetch movies & TV series
    tmdb = TMDBClient(api_key="" if demo_mode else tmdb_key)
    if category == "all":
        categories = [
            "streaming_charts",
            "theories_easter_eggs",
            "where_are_they_now",
            "series",
            "trending",
            "cult_classic",
            "steamy_thrillers",
            "upcoming"
        ]
    else:
        categories = [category]

    print(f"[1/6] Fetching entertainment data for categories: {categories}...")
    movies = tmdb.fetch_feed(categories=categories, per_category=count_per_cat)
    print(f"      -> Retrieved {len(movies)} unique titles (Movies & TV Series).\n")

    if not movies:
        print("[Error] No movies found to process.")
        return {"stories": [], "articles": []}

    # 3. AI Generation (Stories + Discover Articles)
    print(f"[2/6] Synthesizing AMP story slides & Google Discover articles with AI generator...")
    ai = AIGenerator(api_key="" if demo_mode else gemini_key)
    stories = []
    articles = []

    for i, movie in enumerate(movies, 1):
        title = movie.get('title')
        cat = movie.get('category')
        print(f"      [{i}/{len(movies)}] Generating Story & Discover Article for: '{title}' ({cat})...")
        
        # Web Story
        story_data = ai.generate_story(movie)
        stories.append(story_data)

        # Discover Article
        article_data = ai.generate_article(movie, story=story_data)
        articles.append(article_data)

    print(f"      -> Generated {len(stories)} Web Stories and {len(articles)} Discover Articles.\n")

    # 4. Render Standalone AMP Web Stories
    print(f"[3/6] Rendering standalone 100% AMP-valid HTML documents...")
    for story in stories:
        movie = story.get("movie", {})
        slug = movie.get("slug", "story")
        story_dir = STORIES_DIR / slug
        story_dir.mkdir(parents=True, exist_ok=True)

        amp_html = build_amp_story_html(story, domain=domain)
        html_file = story_dir / "index.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

    print(f"      -> Successfully saved {len(stories)} stories into dist/stories/<slug>/index.html\n")

    # 5. Render Standalone Google Discover Articles
    print(f"[4/6] Rendering standalone Google Discover article pages (1200px+ hero images)...")
    for i, article in enumerate(articles):
        movie = article.get("movie", {})
        slug = movie.get("slug", "article")
        art_dir = ARTICLES_DIR / slug
        art_dir.mkdir(parents=True, exist_ok=True)

        # Pass other articles as related recommendations
        related = [a for j, a in enumerate(articles) if j != i]
        art_html = build_discover_article_html(article, domain=domain, related_articles=related)
        html_file = art_dir / "index.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(art_html)

    # 5. Accumulate with existing cache
    cache_stories_path = DIST_DIR / "stories_cache.json"
    cache_articles_path = DIST_DIR / "articles_cache.json"

    combined_stories = list(stories)
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

    combined_articles = list(articles)
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

    # Save JSON feed for articles
    with open(ARTICLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, default=str)

    print(f"      -> Successfully saved {len(articles)} new Discover articles ({len(combined_articles)} total in catalog)\n")

    # 6. Build Discover Feed Portal, Homepage, Policy Pages & Sitemap
    print(f"[5/6] Building Chrome Discover feed, visual homepage, policy pages, and XML sitemap...")
    generate_discover_feed(combined_articles, domain=domain, output_dir=DISCOVER_DIR)
    generate_homepage(combined_stories, domain=domain, output_dir=DIST_DIR)
    generate_policy_pages(dist_dir=DIST_DIR, domain=domain)
    generate_sitemap(combined_stories, articles=combined_articles, domain=domain, output_path=SITEMAP_PATH)
    print(f"      -> Discover feed ({len(combined_articles)} articles), homepage ({len(combined_stories)} stories), policy pages, and sitemap updated.\n")

    # 7. AMP Validation
    if run_validation:
        print(f"[6/6] Running automated AMP validation on all generated Web Stories...")
        passed, failed, errors = check_amp_files(STORIES_DIR)
        if failed > 0:
            print(f"[Validator Warning] {failed} stories failed validation. Review logs above.")
        else:
            print("[Validator] All generated Web Stories passed 100% AMP validation!")

    print("\n" + "="*65)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Output Directory : {DIST_DIR.resolve()}")
    print(f"Total Stories    : {len(stories)} (in dist/stories/)")
    print(f"Discover Articles: {len(articles)} (in dist/articles/)")
    print(f"Homepage URL     : {domain}/")
    print(f"Discover Feed    : {domain}/discover/")
    print(f"Sitemap URL      : {domain}/sitemap.xml")
    print("="*65 + "\n")

    return {"stories": stories, "articles": articles}

def main():
    parser = argparse.ArgumentParser(description="Automated AMP Movie Web Stories & Discover Articles Generator")
    parser.add_argument("--domain", default=DOMAIN_NAME, help="Target deployment domain (e.g. https://cinestories.pages.dev)")
    parser.add_argument("--category", choices=["all", "streaming_charts", "theories_easter_eggs", "where_are_they_now", "series", "trending", "cult_classic", "steamy_thrillers", "upcoming", "now_playing"], default="all", help="Category filter")
    parser.add_argument("--count", type=int, default=STORIES_PER_CATEGORY_LIMIT, help="Number of movies per category")
    parser.add_argument("--tmdb-key", default=TMDB_API_KEY, help="TMDB API Key override")
    parser.add_argument("--gemini-key", default=GEMINI_API_KEY, help="Google Gemini API Key override")
    parser.add_argument("--no-validate", action="store_true", help="Skip AMP HTML validation")
    parser.add_argument("--demo", action="store_true", help="Run in offline demo mode using sample data and rule synthesizer")

    args = parser.parse_args()

    run_pipeline(
        domain=args.domain,
        category=args.category,
        count_per_cat=args.count,
        tmdb_key=args.tmdb_key,
        gemini_key=args.gemini_key,
        run_validation=not args.no_validate,
        demo_mode=args.demo
    )

if __name__ == "__main__":
    main()
