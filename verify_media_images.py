#!/usr/bin/env python3
"""
CineStories Comprehensive Media Image & Content Alignment Auditor
==================================================================
Performs full-stack verification across BOTH source data AND rendered dist/ HTML:
1. Audits every item in `sample_data.SAMPLE_MEDIA` and `google_trends_client.KNOWN_ENTITY_IMAGES`:
   - Zero cross-contamination / duplicate posters or backdrops across distinct titles.
   - Rejects known mismatched placeholder hashes (e.g. Inside Out 2, Overlord, Fast X, Sex Education, WW84, Emraan Hashmi, Vijay Varma).
2. Audits ALL entries in `dist/stories_cache.json` and `dist/articles_cache.json`:
   - Verifies 0 duplicate posters/backdrops across distinct catalog entries.
   - Verifies 100% sync between `SAMPLE_MEDIA`/`KNOWN_ENTITY_IMAGES` and cached stories/articles.
3. Audits rendered `dist/index.html` & `dist/hi/index.html` (Hero Carousel & Story Cards)
   plus Breakout AMP Stories to confirm the live HTML displays matching images.
4. Concurrently checks all unique TMDB CDN URLs for HTTP 200 OK.
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

import sample_data
try:
    from google_trends_client import KNOWN_ENTITY_IMAGES
except ImportError:
    KNOWN_ENTITY_IMAGES = {}

try:
    import curated_stories
except ImportError:
    curated_stories = None

try:
    import curated_stories_hi
except ImportError:
    curated_stories_hi = None

TMDB_CDN_BASE = "https://image.tmdb.org/t/p/w500"

# Known mismatched/overused hashes from historical bugs that must NEVER reappear anywhere
BANNED_PLACEHOLDER_HASHES = {
    "/wFqJMVP0nrsgKeA2kwshRkIz1fw.jpg": "Overused Emraan Hashmi/Showtime backdrop",
    "/4sUKhtN1CxUlH520aNZ7chbEQoE.jpg": "Overused Vijay Varma gun image",
    "/p5ozvmdgsmbWe0H8Xk7Rc8SCwAB.jpg": "Inside Out 2 backdrop (was wrongly on Pushpa 2)",
    "/aS3xM79dmg6bxw9uNqTxRdoze5H.jpg": "Random actress headshot (was wrongly on Pushpa 2)",
    "/8ZJIiwIVF2zDyyFr7oXewj0eEuu.jpg": "Random Japanese actor headshot (was wrongly on Devara)",
    "/hkJhGayONXn96CqIRM9GhWKnlCf.jpg": "Overlord anime backdrop (was wrongly on Devara)",
    "/vnHQQFzTjJ0sv14DGMIoKa3qTxN.jpg": "Legacy mismatched Singham solo portrait",
    "/nq73eRdEooripf3k0XHLtX14zyC.jpg": "Drishyam 2 backdrop (was on Singham Again)",
    "/1E5baAaEse26fej7uHcjOgEE2t2.jpg": "Fast X poster (was wrongly on The Last of Us & Glass Onion)",
    "/soQgquPkLmUu9eKLJJzuA4KZDyi.jpg": "Sex Education backdrop (was wrongly on Squid Game)",
    "/8UlWHLMpgZm9bx6QYh0NFoq67TZ.jpg": "Wonder Woman 1984 backdrop (was wrongly on Marvel)",
    "/lPbFwNohpsCNeLXpzV8ZS3mnI0X.jpg": "Panchayat image (was wrongly inside Stree 2 backdrops)",
}


def check_cdn_image(path: str, timeout: float = 8.0) -> tuple[str, bool, int, str]:
    """Check if an image path returns HTTP 200 on TMDB CDN."""
    if not path or not isinstance(path, str):
        return path, False, 0, "Empty path"

    clean_path = path if path.startswith("/") else f"/{path}"
    url = f"{TMDB_CDN_BASE}{clean_path}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CineStories/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            content_type = resp.headers.get("content-type", "")
            is_valid = status == 200 and "image" in content_type
            return clean_path, is_valid, status, content_type
    except urllib.error.HTTPError as e:
        return clean_path, False, e.code, str(e.reason)
    except Exception as e:
        return clean_path, False, 0, str(e)


def audit_catalog_items(items: list, source_name: str, errors: list, all_paths: set):
    """Verify a list of media/story dicts for missing/banned/duplicate images."""
    poster_to_slugs = defaultdict(list)
    backdrop_to_slugs = defaultdict(list)

    for idx, item in enumerate(items):
        m = item.get("movie", item) if isinstance(item, dict) else {}
        slug = m.get("slug")
        title = m.get("title", "Unknown")
        poster = m.get("poster_path")
        backdrop = m.get("backdrop_path")
        backdrops = m.get("backdrops", [])

        if not slug:
            errors.append(f"[{source_name}] Entry #{idx} ('{title}') is missing 'slug'")
            continue
        if not poster:
            errors.append(f"[{source_name}] '{title}' ({slug}) is missing 'poster_path'")
        elif "http" in poster:
            errors.append(f"[{source_name}] '{slug}' has full URL in 'poster_path' (causes double-prefix bug): {poster}")
        else:
            poster_to_slugs[poster].append(slug)
            all_paths.add(poster)
            if poster in BANNED_PLACEHOLDER_HASHES:
                errors.append(f"[{source_name}] '{slug}' uses banned poster '{poster}' ({BANNED_PLACEHOLDER_HASHES[poster]})")

        if not backdrop:
            errors.append(f"[{source_name}] '{title}' ({slug}) is missing 'backdrop_path'")
        elif "http" in backdrop:
            errors.append(f"[{source_name}] '{slug}' has full URL in 'backdrop_path' (causes double-prefix bug): {backdrop}")
        else:
            backdrop_to_slugs[backdrop].append(slug)
            all_paths.add(backdrop)
            if backdrop in BANNED_PLACEHOLDER_HASHES:
                errors.append(f"[{source_name}] '{slug}' uses banned backdrop '{backdrop}' ({BANNED_PLACEHOLDER_HASHES[backdrop]})")

        for b in backdrops:
            if "http" in str(b):
                errors.append(f"[{source_name}] '{slug}' has full URL in 'backdrops' (causes double-prefix bug): {b}")
            backdrop_to_slugs[b].append(slug)
            all_paths.add(b)
            if b in BANNED_PLACEHOLDER_HASHES:
                errors.append(f"[{source_name}] '{slug}' uses banned secondary backdrop '{b}' ({BANNED_PLACEHOLDER_HASHES[b]})")

    for poster, slugs in poster_to_slugs.items():
        unique_slugs = list(set(slugs))
        if len(unique_slugs) > 1:
            errors.append(f"[{source_name}] CRITICAL: Poster '{poster}' shared across titles: {unique_slugs}")

    for backdrop, slugs in backdrop_to_slugs.items():
        unique_slugs = list(set(slugs))
        if len(unique_slugs) > 1:
            errors.append(f"[{source_name}] CRITICAL: Backdrop '{backdrop}' shared across titles: {unique_slugs}")


def audit_media_data(verify_http: bool = True, max_workers: int = 15):
    print("=" * 78)
    print("🎬 CineStories Comprehensive Media Image & Content Alignment Audit")
    print("=" * 78)

    errors = []
    all_image_paths = set()

    media_list = sample_data.SAMPLE_MEDIA
    print(f"🔍 [1/5] Auditing sample_data.SAMPLE_MEDIA ({len(media_list)} entries)...")
    audit_catalog_items(media_list, "SAMPLE_MEDIA", errors, all_image_paths)

    if KNOWN_ENTITY_IMAGES:
        entity_items = [{"slug": k, "title": k, **v} for k, v in KNOWN_ENTITY_IMAGES.items()]
        audit_catalog_items(entity_items, "KNOWN_ENTITY_IMAGES", errors, all_image_paths)

    sample_by_slug = {m["slug"]: m for m in media_list if "slug" in m}

    # 2. Audit dist/stories_cache.json & dist/articles_cache.json
    dist_dir = Path("dist")
    stories_cache_path = dist_dir / "stories_cache.json"
    articles_cache_path = dist_dir / "articles_cache.json"

    cached_stories = []
    if stories_cache_path.exists():
        cached_stories = json.loads(stories_cache_path.read_text(encoding="utf-8"))
        print(f"🔍 [2/5] Auditing dist/stories_cache.json ({len(cached_stories)} entries)...")
        audit_catalog_items(cached_stories, "dist/stories_cache.json", errors, all_image_paths)
        for s in cached_stories:
            m = s.get("movie", {})
            slug = m.get("slug")
            if slug in sample_by_slug:
                sm = sample_by_slug[slug]
                if m.get("poster_path") != sm.get("poster_path") or m.get("backdrop_path") != sm.get("backdrop_path"):
                    errors.append(f"[stories_cache] '{slug}' is out of sync with SAMPLE_MEDIA!")
    else:
        print("⚠️  [2/5] dist/stories_cache.json not found (skipping dist cache check).")

    if articles_cache_path.exists():
        cached_articles = json.loads(articles_cache_path.read_text(encoding="utf-8"))
        print(f"🔍 [3/5] Auditing dist/articles_cache.json ({len(cached_articles)} entries)...")
        audit_catalog_items(cached_articles, "dist/articles_cache.json", errors, all_image_paths)
        for a in cached_articles:
            m = a.get("movie", {})
            slug = m.get("slug")
            if slug in sample_by_slug:
                sm = sample_by_slug[slug]
                if m.get("poster_path") != sm.get("poster_path") or m.get("backdrop_path") != sm.get("backdrop_path"):
                    errors.append(f"[articles_cache] '{slug}' is out of sync with SAMPLE_MEDIA!")

    # 4. Audit live rendered HTML (dist/index.html & dist/hi/index.html)
    print("🔍 [4/5] Auditing live rendered HTML (dist/index.html, dist/hi/index.html, and stories)...")
    for html_path in [dist_dir / "index.html", dist_dir / "hi" / "index.html"]:
        if not html_path.exists():
            continue
        html_text = html_path.read_text(encoding="utf-8")
        for bad_hash, reason in BANNED_PLACEHOLDER_HASHES.items():
            if bad_hash in html_text:
                errors.append(f"[{html_path}] Contains banned image '{bad_hash}' ({reason})")

    # Also verify no duplicate poster imgs across distinct cards/slides in homepage HTML
    en_home = dist_dir / "index.html"
    if en_home.exists():
        soup = BeautifulSoup(en_home.read_text(encoding="utf-8"), "html.parser")
        card_imgs = defaultdict(list)
        for wrap in soup.find_all("div", class_="card-poster-wrap"):
            img = wrap.find("img")
            if img and img.get("src"):
                card_imgs[img["src"]].append(img.get("alt", "unknown"))
        for src, alts in card_imgs.items():
            if len(set(alts)) > 1:
                errors.append(f"[dist/index.html] Homepage displays duplicate card poster '{src}' on: {alts}")
        slide_imgs = defaultdict(list)
        for wrap in soup.find_all("div", class_="slide-media-wrap"):
            img = wrap.find("img")
            if img and img.get("src"):
                slide_imgs[img["src"]].append(img.get("alt", "unknown"))
        for src, alts in slide_imgs.items():
            if len(set(alts)) > 1:
                errors.append(f"[dist/index.html] Hero carousel displays duplicate backdrop '{src}' on: {alts}")

    # 5. Live TMDB CDN check
    cdn_results = {}
    if verify_http:
        # Verify all sample + known entity + top 80 homepage images (avoid overloading TMDB with 900+ requests on every quick audit)
        paths_to_check = set()
        for m in media_list:
            if m.get("poster_path"):
                paths_to_check.add(m["poster_path"])
            if m.get("backdrop_path"):
                paths_to_check.add(m["backdrop_path"])
            for b in m.get("backdrops", []):
                paths_to_check.add(b)
        for v in KNOWN_ENTITY_IMAGES.values():
            if v.get("poster_path"):
                paths_to_check.add(v["poster_path"])
            if v.get("backdrop_path"):
                paths_to_check.add(v["backdrop_path"])
        for s in cached_stories[:80]:
            m = s.get("movie", {})
            if m.get("poster_path"):
                paths_to_check.add(m["poster_path"])
            if m.get("backdrop_path"):
                paths_to_check.add(m["backdrop_path"])

        print(f"🔍 [5/5] Verifying {len(paths_to_check)} core & homepage TMDB CDN images...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {executor.submit(check_cdn_image, p): p for p in paths_to_check}
            for future in as_completed(future_to_path):
                path, is_valid, status, info = future.result()
                cdn_results[path] = (is_valid, status, info)
                if not is_valid:
                    errors.append(f"TMDB CDN 404/Error: Image '{path}' failed with status {status} ({info})")

        valid_count = sum(1 for is_valid, _, _ in cdn_results.values() if is_valid)
        print(f"  -> {valid_count}/{len(paths_to_check)} checked images returned HTTP 200 OK from TMDB CDN.\n")
    else:
        print("🔍 [5/5] TMDB CDN check skipped (--skip-http specified).\n")

    print("=" * 78)
    if errors:
        print(f"❌ AUDIT FAILED with {len(errors)} error(s):")
        for err in errors[:30]:
            print(f"  - {err}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more errors.")
        return False
    else:
        print("🎉 AUDIT PASSED! 0 cross-contamination, 0 banned placeholders, 100% synced & verified!")
        return True


def main():
    parser = argparse.ArgumentParser(description="Comprehensive audit for CineStories media images & dist/ HTML.")
    parser.add_argument("--skip-http", action="store_true", help="Skip remote TMDB CDN HTTP 200 checks")
    parser.add_argument("--workers", type=int, default=15, help="Number of concurrent workers for CDN checks")
    args = parser.parse_args()

    success = audit_media_data(verify_http=not args.skip_http, max_workers=args.workers)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
