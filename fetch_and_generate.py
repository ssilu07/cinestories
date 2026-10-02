"""
Fetch and Generate Orchestrator for CineStories.
Automates the full pipeline:
1. Fetches top upcoming, now_playing, and trending movies from TMDB API.
2. Synthesizes high-engagement, mobile-optimized story slides via Gemini API (with structured outputs).
3. Renders 100% AMP-valid standalone Web Story HTML files to dist/stories/[slug]/index.html.
4. Updates dist/sitemap.xml with proper Google Web Story and image tags.
5. Renders a responsive visual portal at dist/index.html.
6. Validates AMP compliance using the official amphtml-validator.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Any

from config import (
    DOMAIN_NAME,
    TMDB_API_KEY,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DIST_DIR,
    STORIES_DIR,
    ASSETS_DIR,
    SITEMAP_PATH,
    STORIES_PER_CATEGORY_LIMIT
)
from tmdb_client import TMDBClient
from ai_generator import AIGenerator
from story_builder import build_amp_story_html
from homepage_builder import generate_homepage
from sitemap_builder import generate_sitemap
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
    """Generate robots.txt directing search engines to sitemap.xml."""
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
) -> List[Dict[str, Any]]:
    """
    Execute the end-to-end automated story generation pipeline.
    """
    print("\n" + "="*60)
    print("      CINESTORIES: GOOGLE AMP WEB STORIES GENERATOR      ")
    print("="*60)
    print(f"Domain Target    : {domain}")
    print(f"Category Scope   : {category}")
    print(f"Per-Category Max : {count_per_cat}")
    print(f"TMDB API Key     : {'Configured (Live API)' if tmdb_key and not demo_mode else 'Not set (Demo / Sample Data Mode)'}")
    print(f"Gemini API Key   : {'Configured (Live Gemini AI)' if gemini_key and not demo_mode else 'Not set (Rule-Based Synthesizer Mode)'}")
    print("="*60 + "\n")

    # 1. Ensure output assets
    ensure_assets(DIST_DIR)
    write_robots_txt(DIST_DIR, domain)

    # 2. Fetch movies & TV series
    tmdb = TMDBClient(api_key="" if demo_mode else tmdb_key)
    if category == "all":
        categories = ["series", "trending", "cult_classic", "upcoming"]
    else:
        categories = [category]

    print(f"[1/5] Fetching entertainment data for categories: {categories}...")
    movies = tmdb.fetch_feed(categories=categories, per_category=count_per_cat)
    print(f"      -> Retrieved {len(movies)} unique titles (Movies & TV Series).\n")

    if not movies:
        print("[Error] No movies found to process.")
        return []

    # 3. AI Generation
    print(f"[2/5] Synthesizing AMP story slides with AI generator...")
    ai = AIGenerator(api_key="" if demo_mode else gemini_key)
    stories = []

    for i, movie in enumerate(movies, 1):
        print(f"      [{i}/{len(movies)}] Generating narrative for: '{movie.get('title')}' ({movie.get('category')})...")
        story_data = ai.generate_story(movie)
        stories.append(story_data)
    print(f"      -> Generated {len(stories)} stories.\n")

    # 4. Render AMP HTML
    print(f"[3/5] Rendering standalone 100% AMP-valid HTML documents...")
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

    # 5. Build Homepage & Sitemap
    print(f"[4/5] Building visual homepage and XML sitemap...")
    generate_homepage(stories, domain=domain, output_dir=DIST_DIR)
    generate_sitemap(stories, domain=domain, output_path=SITEMAP_PATH)
    print(f"      -> Portal homepage and sitemap updated.\n")

    # 6. AMP Validation
    if run_validation:
        print(f"[5/5] Running automated AMP validation on all generated files...")
        passed, failed, errors = check_amp_files(STORIES_DIR)
        if failed > 0:
            print(f"[Validator Warning] {failed} stories failed validation. Review logs above.")
        else:
            print("[Validator] All generated stories passed 100% AMP validation!")

    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Output Directory: {DIST_DIR.resolve()}")
    print(f"Total Stories   : {len(stories)}")
    print(f"Homepage URL    : {domain}/")
    print(f"Sitemap URL     : {domain}/sitemap.xml")
    print("="*60 + "\n")

    return stories

def main():
    parser = argparse.ArgumentParser(description="Automated AMP Movie Web Stories Generator")
    parser.add_argument("--domain", default=DOMAIN_NAME, help="Target deployment domain (e.g. https://cinestories.pages.dev)")
    parser.add_argument("--category", choices=["all", "series", "trending", "cult_classic", "upcoming", "now_playing"], default="all", help="Category filter")
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
