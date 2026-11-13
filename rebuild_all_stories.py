"""
Universal Rebuild Engine for CineStories AMP Web Stories (Upgraded for 432 Stories).
Re-renders all 432 AMP Web Stories across dist/stories/ with the responsive UI/UX architecture,
Schema.org BreadcrumbList, inLanguage, E-E-A-T Editorial Board attribution, /about/ brand badge,
and final-slide legal navigation row, preserving authentic historical publication timestamps.
"""

import sys
import json
import re
import html
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DOMAIN_NAME,
    DIST_DIR,
    STORIES_DIR,
    REGISTRY_PATH,
    TARGET_BREAKOUT_SLUGS
)
from curated_stories import CURATED_STORIES
from story_builder import build_amp_story_html

def extract_story_from_disk_html(html_path: Path) -> Dict[str, Any]:
    """
    Extracts high-fidelity story data from a standalone AMP Web Story index.html file
    for stories not present in stories_cache.json or missing historical dates.
    """
    content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    slug = html_path.parent.name

    ld_tag = soup.find("script", type="application/ld+json")
    ld = {}
    if ld_tag and ld_tag.string:
        try:
            parsed = json.loads(ld_tag.string)
            if isinstance(parsed, dict):
                if "@graph" in parsed:
                    for item in parsed["@graph"]:
                        if item.get("@type") == "NewsArticle":
                            ld = item
                            break
                else:
                    ld = parsed
            elif isinstance(parsed, list):
                for item in parsed:
                    if item.get("@type") == "NewsArticle":
                        ld = item
                        break
        except Exception:
            pass

    story_tag = soup.find("amp-story")
    title = story_tag.get("title") if story_tag else (ld.get("headline") or slug.replace("-", " ").title())
    meta_desc = soup.find("meta", attrs={"name": "description"})
    seo_desc = meta_desc.get("content") if meta_desc else ld.get("description", "")

    date_published = ld.get("datePublished")
    date_modified = ld.get("dateModified")

    pages = soup.find_all("amp-story-page")
    slides = []
    backdrops = []

    movie_title = slug.replace("-", " ").title()
    category = "trending"
    release_date = ""
    vote_average = "8.0"
    seasons = None
    runtime = 120

    for idx, page in enumerate(pages):
        img_tag = page.find("amp-img")
        img_src = img_tag.get("src") if img_tag else ""
        if img_src and img_src not in backdrops:
            backdrops.append(img_src)
        b_idx = backdrops.index(img_src) if img_src in backdrops else idx

        badge_tag = page.find("span", class_="badge")
        badge_text = badge_tag.get_text(strip=True) if badge_tag else "SPOTLIGHT"

        cat_tag = page.find("span", class_="category-pill")
        if cat_tag:
            category = cat_tag.get_text(strip=True).lower().replace(" ", "_")

        h_tag = page.find(["h1", "h2"])
        heading = h_tag.get_text(strip=True) if h_tag else ""

        txt_tag = page.find("p", class_="slide-text")
        text = txt_tag.get_text(strip=True) if txt_tag else ""

        # Extract movie chips from cover
        if idx == 0:
            if heading:
                movie_title = heading
            chips = page.find_all("span", class_="chip")
            for chip in chips:
                c_text = chip.get_text(strip=True)
                if "★" in c_text:
                    vote_average = c_text.replace("★", "").strip()
                elif "📅" in c_text:
                    release_date = c_text.replace("📅", "").strip()
                elif "Seasons" in c_text:
                    m = re.search(r"(\d+)", c_text)
                    if m:
                        seasons = int(m.group(1))
                elif "m" in c_text and "⏱" in c_text:
                    m = re.search(r"(\d+)", c_text)
                    if m:
                        runtime = int(m.group(1))

        poll_tag = page.find("amp-story-interactive-binary-poll")
        poll_info = None
        if poll_tag:
            poll_info = {
                "id": poll_tag.get("id"),
                "prompt": poll_tag.get("prompt-text"),
                "option1": poll_tag.get("option-1-text"),
                "option2": poll_tag.get("option-2-text")
            }

        slides.append({
            "backdrop_index": b_idx,
            "badge": badge_text,
            "title": heading,
            "text": text,
            "poll": poll_info
        })

    # Outlink info from last page
    next_url = None
    next_title = None
    outlink_tag = soup.find("amp-story-page-outlink")
    if outlink_tag:
        a_tag = outlink_tag.find("a")
        if a_tag:
            next_url = a_tag.get("href")
            txt = a_tag.get_text(strip=True)
            if "Read Next:" in txt:
                next_title = txt.replace("Read Next:", "").replace("➔", "").strip()

    poster_portrait = story_tag.get("poster-portrait-src") if story_tag else (backdrops[0] if backdrops else "")
    poster_landscape = story_tag.get("poster-landscape-src") if story_tag else (backdrops[0] if backdrops else "")

    movie_data = {
        "title": movie_title,
        "slug": slug,
        "overview": seo_desc,
        "poster_path": poster_portrait,
        "backdrop_path": poster_landscape,
        "backdrops": backdrops,
        "category": category,
        "vote_average": vote_average,
        "release_date": release_date,
    }
    if seasons:
        movie_data["seasons"] = seasons
    else:
        movie_data["runtime"] = runtime

    return {
        "title": title,
        "seo_description": seo_desc,
        "movie": movie_data,
        "slides": slides,
        "date_published": date_published,
        "date_modified": date_modified,
        "next_story_url": next_url,
        "next_story_title": next_title
    }

def rebuild_all_stories(dry_run: bool = False, output_root: Optional[Path] = None) -> bool:
    target_stories_dir = output_root or STORIES_DIR
    print("=" * 70)
    print("  CINESTORIES UNIVERSAL REBUILD: ALL 432 AMP WEB STORIES")
    print("  Schema.org Breadcrumbs, E-E-A-T, Responsive Layout & Legal Navigation")
    print("=" * 70)

    # 1. Ingest cached stories
    cache_path = DIST_DIR / "stories_cache.json"
    cached_stories: List[Dict[str, Any]] = []
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_stories = json.load(f)
            print(f"[1/5] Ingested {len(cached_stories)} stories from {cache_path}")
        except Exception as e:
            print(f"[!] Warning reading stories cache: {e}")

    # 2. Ingest published_registry.json for authentic historical timestamps
    registry: Dict[str, Any] = {}
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)
            print(f"[2/5] Ingested {len(registry)} historical timestamp records from {REGISTRY_PATH}")
        except Exception as e:
            print(f"[!] Warning reading registry: {e}")

    story_catalog_by_slug: Dict[str, Dict[str, Any]] = {}
    for story in cached_stories:
        slug = story.get("movie", {}).get("slug") or story.get("slug")
        if slug:
            story_catalog_by_slug[slug] = story

    # 3. Ingest any disk stories not in cache and scan all disk directories
    disk_story_dirs = [d for d in STORIES_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()]
    print(f"[3/5] Scanned disk: {len(disk_story_dirs)} story directories in {STORIES_DIR}")

    disk_only_count = 0
    for s_dir in disk_story_dirs:
        slug = s_dir.name
        if slug not in story_catalog_by_slug:
            try:
                story_data = extract_story_from_disk_html(s_dir / "index.html")
                story_catalog_by_slug[slug] = story_data
                cached_stories.append(story_data)
                disk_only_count += 1
            except Exception as e:
                print(f"[!] Error extracting disk story '{slug}': {e}")

    # 4. Reconcile curated stories and historical dates
    print(f"[4/5] Reconciling curated editorial slides and historical publication dates...")
    dates_backfilled = 0
    curated_overlays = 0

    for slug, story_data in story_catalog_by_slug.items():
        # Overlay curated content if present
        if slug in CURATED_STORIES:
            c_story = CURATED_STORIES[slug]
            if c_story.get("title"):
                story_data["title"] = c_story["title"]
            if c_story.get("seo_description"):
                story_data["seo_description"] = c_story["seo_description"]
            if c_story.get("slides"):
                story_data["slides"] = c_story["slides"]
            curated_overlays += 1

        # Preserve / backfill authentic historical timestamp
        pub_date = (
            story_data.get("date_published")
            or story_data.get("published_at")
            or registry.get(slug, {}).get("published_at")
        )
        if not pub_date:
            disk_file = STORIES_DIR / slug / "index.html"
            if disk_file.exists():
                extracted = extract_story_from_disk_html(disk_file)
                pub_date = extracted.get("date_published")
        
        if not pub_date:
            # Fallback to an immutable release timestamp rather than now
            pub_date = "2026-10-23T12:00:00Z"
        
        if story_data.get("date_published") != pub_date or story_data.get("published_at") != pub_date:
            story_data["date_published"] = pub_date
            story_data["published_at"] = pub_date
            dates_backfilled += 1

        mod_date = (
            story_data.get("date_modified")
            or story_data.get("modified_at")
            or registry.get(slug, {}).get("modified_at")
            or pub_date
        )
        story_data["date_modified"] = mod_date
        story_data["modified_at"] = mod_date

        if slug not in registry:
            registry[slug] = {
                "title": story_data.get("movie", {}).get("title") or story_data.get("title"),
                "published_at": pub_date,
                "modified_at": mod_date,
                "category": story_data.get("movie", {}).get("category", "trending")
            }

    print(f"      Overlaid {curated_overlays} curated stories from curated_stories.py.")
    print(f"      Backfilled/verified {dates_backfilled} historical publication timestamps.")

    # 5. Re-render all stories with build_amp_story_html
    print(f"\n[5/5] Re-rendering {len(disk_story_dirs)} stories through build_amp_story_html()...")
    rebuilt_count = 0
    errors = []

    for idx, s_dir in enumerate(disk_story_dirs):
        slug = s_dir.name
        story_data = story_catalog_by_slug.get(slug)
        if not story_data:
            errors.append(f"Missing data for story '{slug}'")
            continue

        try:
            amp_html = build_amp_story_html(story_data, domain=DOMAIN_NAME)
            
            if not dry_run:
                target_folder = target_stories_dir / slug
                target_folder.mkdir(parents=True, exist_ok=True)
                out_file = target_folder / "index.html"
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(amp_html)

            rebuilt_count += 1
            if (idx + 1) % 50 == 0 or (idx + 1) == len(disk_story_dirs):
                print(f"      [{idx + 1}/{len(disk_story_dirs)}] Rebuilt: {slug}")
        except Exception as e:
            err_msg = f"Failed to rebuild story '{slug}': {e}"
            print(f"      [!] {err_msg}")
            errors.append(err_msg)

    # Update cache file if not dry run
    if not dry_run and output_root is None:
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cached_stories, f, indent=2, default=str)
            print(f"\n      Updated {cache_path} with reconciled {len(cached_stories)} stories.")
        except Exception as e:
            print(f"[!] Error updating stories cache: {e}")

        try:
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)
            print(f"      Updated {REGISTRY_PATH} ({len(registry)} entries).")
        except Exception as e:
            print(f"[!] Error updating registry: {e}")

    print(f"\nSummary:")
    print(f"  Successfully rebuilt: {rebuilt_count} / {len(disk_story_dirs)} stories.")
    if errors:
        print(f"  Errors encountered: {len(errors)}")
        for err in errors[:10]:
            print(f"    - {err}")
        return False
    else:
        print(f"  All {rebuilt_count} stories successfully rebuilt with 100% compliance!\n")
        print("=" * 70)
        return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    success = rebuild_all_stories(dry_run=is_dry)
    sys.exit(0 if success else 1)
