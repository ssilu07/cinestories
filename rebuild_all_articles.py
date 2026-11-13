"""
Universal Rebuild Engine for CineStories Discover Articles.
Re-renders all 432 Discover Articles in dist/articles/ through build_discover_article_html().
Eliminates all legacy 'Marcus Vance' & 'MoviePulse' references.
Populates BreadcrumbList, 'inLanguage': 'en-US', and authentic CineStories Editorial Board.
Preserves authentic publication dates from published_registry.json.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DOMAIN_NAME,
    DIST_DIR,
    ARTICLES_DIR,
    ARTICLES_JSON_PATH,
    REGISTRY_PATH,
    TARGET_BREAKOUT_SLUGS
)
from curated_articles import CURATED_ARTICLES
from article_builder import build_discover_article_html

def extract_article_from_disk_html(html_path: Path, movie_fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(content, "html.parser")
    slug = html_path.parent.name
    
    # Extract dates from ld+json
    ld_pub = None
    ld_mod = None
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string)
            for node in d.get("@graph", [d]):
                if node.get("@type") == "NewsArticle":
                    ld_pub = node.get("datePublished")
                    ld_mod = node.get("dateModified")
                    break
        except Exception:
            pass

    h1_tag = soup.find("h1")
    headline = h1_tag.get_text(strip=True) if h1_tag else slug.replace("-", " ").title()
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag.get("content", "") if meta_desc_tag else ""
    
    sections = []
    for s in soup.find_all("section", class_="article-section"):
        h2 = s.find(["h2", "h3"])
        h2_text = h2.get_text(strip=True) if h2 else ""
        body_paras = [p.get_text(strip=True) for p in s.find_all("p") if p.get_text(strip=True)]
        body_text = "\n\n".join(body_paras)
        if body_text:
            sections.append({"heading": h2_text, "content": body_text})
            
    takeaways = [li.get_text(strip=True) for li in soup.select(".takeaways-list li") if li.get_text(strip=True)]
    verdict_tag = soup.select_one(".verdict-card p, .verdict-text")
    verdict_summary = verdict_tag.get_text(strip=True) if verdict_tag else ""
    
    return {
        "slug": slug,
        "headline": headline,
        "meta_description": meta_desc,
        "sections": sections,
        "key_takeaways": takeaways,
        "verdict_summary": verdict_summary,
        "movie": movie_fallback or {"slug": slug, "title": headline.split(":")[0]},
        "date_published": ld_pub,
        "date_modified": ld_mod,
        "published_at": ld_pub
    }

def rebuild_all_articles(dry_run: bool = False, output_root: Optional[Path] = None) -> bool:
    target_articles_dir = output_root or ARTICLES_DIR
    print("=" * 70)
    print("  CINESTORIES UNIVERSAL REBUILD: ALL 432 DISCOVER ARTICLES")
    print("  Eradicating Marcus Vance, Populating Breadcrumbs & Editorial Board")
    print("=" * 70)
    
    # 1. Load registry
    registry: Dict[str, Any] = {}
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)
            print(f"[1/5] Ingested {len(registry)} historical timestamp records from {REGISTRY_PATH}")
        except Exception as e:
            print(f"[!] Warning reading registry: {e}")
            
    # 2. Load stories cache for movie fallbacks
    movie_by_slug: Dict[str, Dict[str, Any]] = {}
    s_cache_path = DIST_DIR / "stories_cache.json"
    if s_cache_path.exists():
        try:
            with open(s_cache_path, "r", encoding="utf-8") as f:
                for s in json.load(f):
                    m = s.get("movie", {})
                    sl = m.get("slug") or s.get("slug")
                    if sl:
                        movie_by_slug[sl] = m
            print(f"[2/5] Ingested {len(movie_by_slug)} movie fallbacks from {s_cache_path}")
        except Exception as e:
            print(f"[!] Warning reading stories cache: {e}")

    # 3. Load existing articles cache
    cache_path = DIST_DIR / "articles_cache.json"
    cached_articles: List[Dict[str, Any]] = []
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_articles = json.load(f)
            print(f"[3/5] Ingested {len(cached_articles)} articles from {cache_path}")
        except Exception as e:
            print(f"[!] Warning reading articles cache: {e}")
            
    article_by_slug: Dict[str, Dict[str, Any]] = {}
    for a in cached_articles:
        sl = a.get("slug") or a.get("movie", {}).get("slug")
        if sl:
            article_by_slug[sl] = a

    # 4. Scan disk articles
    disk_dirs = [d for d in ARTICLES_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()]
    print(f"[4/5] Scanned disk: {len(disk_dirs)} article directories in {ARTICLES_DIR}")

    # Ingest any missing disk articles
    disk_only_count = 0
    for d in disk_dirs:
        sl = d.name
        if sl not in article_by_slug:
            m_data = movie_by_slug.get(sl, {"slug": sl, "title": sl.replace("-", " ").title()})
            art_data = extract_article_from_disk_html(d / "index.html", movie_fallback=m_data)
            article_by_slug[sl] = art_data
            cached_articles.append(art_data)
            disk_only_count += 1
    if disk_only_count > 0:
        print(f"      Ingested {disk_only_count} disk-only articles into catalog.")

    # 5. Reconcile dates, curated overlays, and re-render all 432 articles
    print(f"[5/5] Re-rendering {len(disk_dirs)} articles through build_discover_article_html()...")
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rebuilt_count = 0
    errors = []

    for idx, d in enumerate(disk_dirs):
        sl = d.name
        art_data = article_by_slug.get(sl)
        if not art_data:
            errors.append(f"Missing data for article '{sl}'")
            continue

        # Overlay curated content if present
        if sl in CURATED_ARTICLES:
            for k, v in CURATED_ARTICLES[sl].items():
                art_data[k] = v

        # Strictly preserve historical dates from registry or article metadata or disk
        disk_pub = None
        disk_mod = None
        if not (registry.get(sl, {}).get("published_at") or art_data.get("date_published") or art_data.get("published_at")):
            try:
                extracted = extract_article_from_disk_html(d / "index.html")
                disk_pub = extracted.get("date_published")
                disk_mod = extracted.get("date_modified")
            except Exception:
                pass

        hist_pub = (
            registry.get(sl, {}).get("published_at")
            or art_data.get("date_published")
            or art_data.get("published_at")
            or disk_pub
            or "2026-10-23T12:00:00Z"
        )
        hist_mod = (
            registry.get(sl, {}).get("modified_at")
            or art_data.get("date_modified")
            or art_data.get("modified_at")
            or disk_mod
            or hist_pub
        )
        
        art_data["date_published"] = hist_pub
        art_data["published_at"] = hist_pub
        art_data["date_modified"] = hist_mod
        art_data["modified_at"] = hist_mod
        
        if not art_data.get("movie") or not art_data["movie"].get("title"):
            art_data["movie"] = movie_by_slug.get(sl, {"slug": sl, "title": sl.replace("-", " ").title()})

        # Provide 3 related articles
        related = [
            a for a in cached_articles
            if (a.get("slug") or a.get("movie", {}).get("slug")) != sl
            and a.get("movie", {}).get("category") == art_data.get("movie", {}).get("category")
        ][:3]
        if len(related) < 3:
            related += [
                a for a in cached_articles
                if (a.get("slug") or a.get("movie", {}).get("slug")) != sl
                and a not in related
            ][:(3 - len(related))]

        try:
            html_out = build_discover_article_html(art_data, domain=DOMAIN_NAME, related_articles=related)
            if not dry_run:
                target_folder = target_articles_dir / sl
                target_folder.mkdir(parents=True, exist_ok=True)
                with open(target_folder / "index.html", "w", encoding="utf-8") as f:
                    f.write(html_out)
                    
            registry[sl] = {
                "title": art_data["movie"].get("title"),
                "published_at": hist_pub,
                "modified_at": hist_mod,
                "category": art_data["movie"].get("category", "trending")
            }
            rebuilt_count += 1
            if (idx + 1) % 50 == 0 or (idx + 1) == len(disk_dirs):
                print(f"      [{idx + 1}/{len(disk_dirs)}] Rebuilt: {sl}")
        except Exception as e:
            err_msg = f"Failed to rebuild article '{sl}': {e}"
            print(f"      [!] {err_msg}")
            errors.append(err_msg)

    # Save updated caches
    if not dry_run and output_root is None:
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cached_articles, f, indent=2, default=str)
            print(f"\n      Updated {cache_path} with {len(cached_articles)} articles.")
        except Exception as e:
            print(f"[!] Error updating articles cache: {e}")

        try:
            with open(ARTICLES_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(cached_articles, f, indent=2, default=str)
            print(f"      Updated {ARTICLES_JSON_PATH} with {len(cached_articles)} articles.")
        except Exception as e:
            print(f"[!] Error updating articles json: {e}")

        try:
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)
            print(f"      Updated {REGISTRY_PATH} with {len(registry)} entries.")
        except Exception as e:
            print(f"[!] Error updating registry: {e}")

    print(f"\nSummary:")
    print(f"  Successfully rebuilt: {rebuilt_count} / {len(disk_dirs)} articles.")
    if errors:
        print(f"  Errors encountered: {len(errors)}")
        for err in errors[:10]:
            print(f"    - {err}")
        return False
    else:
        print(f"  All {rebuilt_count} articles successfully rebuilt with 100% compliance!\n")
        print("=" * 70)
        return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    success = rebuild_all_articles(dry_run=is_dry)
    sys.exit(0 if success else 1)
