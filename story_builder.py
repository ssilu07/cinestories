"""
AMP Story HTML Builder module for CineStories.
Renders 100% AMP-valid, standalone Google Web Stories adhering strictly to
the Google AMP Web Story specifications and SEO Discover guidelines.
Supports English ("en") and Hindi ("hi") with bilingual hreflang annotations
and Devanagari typography rendering without clipping or layout shifts.
"""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from config import (
    DOMAIN_NAME,
    PUBLISHER_NAME,
    get_publisher_logo_url,
    TMDB_IMAGE_ORIGINAL,
    TMDB_IMAGE_BACKDROP,
    TMDB_IMAGE_POSTER,
    GA_MEASUREMENT_ID,
    ADSENSE_CLIENT_ID,
    get_amp_story_ads_tags
)

# Mandatory AMP boilerplate CSS
AMP_BOILERPLATE = (
    "<style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;"
    "-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;"
    "-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;"
    "animation:-amp-start 8s steps(1,end) 0s 1 normal both}"
    "@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}"
    "@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}"
    "@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}"
    "@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}"
    "@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style>"
    "<noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>"
)

# Custom AMP styles (Strictly NO !important)
AMP_CUSTOM_CSS = """
  :root {
    --primary: #e11d48;
    --primary-glow: rgba(225, 29, 72, 0.4);
    --gold: #f59e0b;
    --bg-dark: #090b10;
    --card-bg: rgba(10, 14, 24, 0.90);
    --border-subtle: rgba(255, 255, 255, 0.16);
    --text-main: #ffffff;
    --text-muted: #e2e8f0;
  }
  amp-story {
    font-family: 'Outfit', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text-main);
  }
  amp-story-page {
    background-color: var(--bg-dark);
  }
  .scrim-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      180deg,
      rgba(9, 11, 16, 0.65) 0%,
      rgba(9, 11, 16, 0.15) 18%,
      rgba(9, 11, 16, 0.0) 35%,
      rgba(9, 11, 16, 0.3) 55%,
      rgba(9, 11, 16, 0.82) 78%,
      rgba(9, 11, 16, 0.98) 100%
    );
    pointer-events: none;
  }
  amp-story-grid-layer[template="vertical"] {
    align-content: stretch;
    grid-template-rows: 1fr;
    padding: 0;
  }
  .content-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    padding: max(22px, env(safe-area-inset-top, 22px)) clamp(8px, 2.6vw, 16px) max(12px, env(safe-area-inset-bottom, 12px));
    box-sizing: border-box;
    pointer-events: none;
    width: 100%;
    max-width: 520px;
    margin: 0 auto;
  }
  .final-slide-wrapper {
    padding-bottom: max(58px, calc(env(safe-area-inset-bottom, 0px) + 54px));
  }
  .story-top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: auto;
    padding-right: clamp(52px, 14vw, 76px);
    box-sizing: border-box;
    z-index: 10;
    pointer-events: auto;
    gap: 8px;
  }
  .story-close-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(9, 11, 16, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.28);
    color: #ffffff;
    padding: clamp(4px, 1.2vw, 6px) clamp(8px, 2vw, 12px);
    border-radius: 999px;
    text-decoration: none;
    font-size: clamp(11px, 2.6vw, 12.5px);
    font-weight: 700;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6);
    flex-shrink: 0;
  }
  .story-close-btn svg {
    color: #fda4af;
    flex-shrink: 0;
  }
  .story-brand-badge {
    font-size: clamp(9px, 2.2vw, 10.5px);
    font-weight: 700;
    color: #fbbf24;
    background: rgba(9, 11, 16, 0.82);
    padding: 3.5px clamp(7px, 1.8vw, 10px);
    border-radius: 999px;
    border: 1px solid rgba(251, 191, 36, 0.3);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-shrink: 0;
  }
  .content-card {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-subtle);
    border-radius: clamp(12px, 3.4vw, 18px);
    padding: clamp(8px, 2.2vw, 14px) clamp(10px, 2.6vw, 15px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.72), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    margin-top: auto;
    margin-bottom: 2px;
    pointer-events: auto;
    width: 100%;
    box-sizing: border-box;
    max-height: min(84%, 560px);
    overflow-y: auto;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .content-card::-webkit-scrollbar {
    display: none;
  }
  .badge-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: clamp(3px, 1vw, 6px);
  }
  .badge {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, var(--primary) 0%, var(--gold) 100%);
    color: #ffffff;
    font-size: clamp(8.5px, 2vw, 10px);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: clamp(0.4px, 0.15vw, 0.8px);
    padding: 2px clamp(6px, 1.5vw, 9px);
    border-radius: 999px;
    margin-bottom: 0;
    white-space: nowrap;
    line-height: 1.2;
  }
  .category-pill {
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.14);
    color: #f1f5f9;
    font-size: clamp(8px, 1.8vw, 9px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    padding: 1.5px 6px;
    border-radius: 6px;
    margin-left: 0;
    vertical-align: middle;
    white-space: nowrap;
    line-height: 1.2;
  }
  .slide-title {
    font-size: clamp(15px, 3.8vw, 20px);
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 clamp(3px, 1vw, 6px) 0;
    color: #ffffff;
    letter-spacing: -0.2px;
    overflow-wrap: break-word;
    word-break: break-word;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 4;
    overflow: hidden;
  }
  .cover-title {
    font-size: clamp(17px, 4.4vw, 23px);
    font-weight: 900;
    line-height: 1.22;
    margin: 0 0 clamp(3px, 1vw, 6px) 0;
    color: #ffffff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
    overflow-wrap: break-word;
    word-break: break-word;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 4;
    overflow: hidden;
  }
  .slide-text {
    font-size: clamp(11.5px, 2.7vw, 13.5px);
    line-height: 1.40;
    color: var(--text-muted);
    margin: 0 0 clamp(4px, 1.2vw, 8px) 0;
    overflow-wrap: break-word;
    word-break: break-word;
    hyphens: auto;
  }
  .final-slide-card .slide-title {
    font-size: clamp(14px, 3.5vw, 17px);
    line-height: 1.22;
    margin: 0 0 clamp(2px, 0.8vw, 4px) 0;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
  }
  .final-slide-card .slide-text {
    font-size: clamp(11px, 2.5vw, 12.5px);
    line-height: 1.32;
    margin: 0 0 clamp(3px, 1vw, 5px) 0;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  amp-story-interactive-binary-poll {
    --interactive-accent-color: var(--primary);
    --interactive-prompt-text-color: #ffffff;
    --interactive-prompt-background: rgba(255, 255, 255, 0.08);
    --interactive-prompt-alignment: center;
    font-size: clamp(10px, 2.4vw, 12px);
    margin: clamp(3px, 1vw, 6px) 0;
    width: 100%;
    max-width: 100%;
    display: block;
    box-sizing: border-box;
  }
  .meta-chips {
    display: flex;
    flex-wrap: wrap;
    gap: clamp(3px, 1vw, 5px);
    margin-top: clamp(3px, 1vw, 6px);
  }
  .chip {
    display: inline-flex;
    align-items: center;
    font-size: clamp(9px, 2vw, 10px);
    font-weight: 600;
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.1);
    padding: 2px clamp(5px, 1.2vw, 7px);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    white-space: nowrap;
    line-height: 1.2;
  }
  .chip-rating {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border-color: rgba(245, 158, 11, 0.35);
  }
  .pulse-indicator {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: var(--primary);
    margin-right: 4px;
    vertical-align: middle;
  }
  .final-nav-buttons {
    display: flex;
    gap: 6px;
    margin-top: clamp(4px, 1.2vw, 8px);
    flex-wrap: nowrap;
    align-items: center;
    width: 100%;
  }
  .btn-next-story {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    background: linear-gradient(135deg, var(--primary) 0%, #f43f5e 100%);
    color: #ffffff;
    text-decoration: none;
    font-size: clamp(10.5px, 2.4vw, 12px);
    font-weight: 800;
    padding: 6px clamp(7px, 1.8vw, 11px);
    border-radius: 999px;
    box-shadow: 0 4px 12px var(--primary-glow);
    flex: 1 1 0;
    min-width: 0;
    letter-spacing: 0.2px;
    box-sizing: border-box;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .btn-read-article {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    background: rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    text-decoration: none;
    font-size: clamp(10px, 2.2vw, 11.5px);
    font-weight: 600;
    padding: 6px clamp(7px, 1.8vw, 10px);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-sizing: border-box;
    flex: 1 1 0;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .final-nav-row {
    margin-top: clamp(3px, 1vw, 5px);
    padding-top: clamp(3px, 1vw, 5px);
    border-top: 1px solid rgba(255, 255, 255, 0.10);
    text-align: center;
  }
  .final-legal-row {
    margin-top: clamp(2px, 0.8vw, 4px);
    padding-top: clamp(2px, 0.8vw, 4px);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  .final-legal-row a {
    color: #94a3b8;
    text-decoration: none;
    font-size: clamp(8.5px, 2vw, 9.5px);
    font-weight: 500;
  }
  .final-legal-row a:hover {
    color: #ffffff;
  }
  .btn-return-home {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    color: #38bdf8;
    text-decoration: none;
    font-size: clamp(10.5px, 2.3vw, 12px);
    font-weight: 700;
  }

  /* MEDIA QUERIES FOR MULTI-TIER VIEWPORT RESILIENCE */
  @media (max-width: 360px) {
    .content-wrapper {
      padding-left: 6px;
      padding-right: 6px;
    }
    .content-card {
      padding: 6px 8px;
      border-radius: 11px;
      max-height: 86%;
    }
    .story-top-bar {
      padding-right: 48px;
    }
    .story-close-btn span, .story-close-btn b {
      display: none;
    }
    .story-close-btn {
      padding: 5px;
      border-radius: 50%;
    }
    .btn-next-story, .btn-read-article {
      padding: 5px 6px;
      font-size: 10px;
    }
  }

  @media (max-height: 680px) {
    .content-wrapper {
      padding-top: max(14px, env(safe-area-inset-top, 14px));
      padding-bottom: max(8px, env(safe-area-inset-bottom, 8px));
    }
    .final-slide-wrapper {
      padding-bottom: max(54px, calc(env(safe-area-inset-bottom, 0px) + 50px));
    }
    .content-card {
      padding: 6px 10px;
      border-radius: 12px;
      max-height: 86%;
    }
    .cover-title {
      font-size: 15px;
      margin-bottom: 2px;
    }
    .slide-title {
      font-size: 14px;
      margin-bottom: 2px;
    }
    .slide-text {
      font-size: 11px;
      line-height: 1.34;
      margin-bottom: 3px;
    }
    .final-slide-card .slide-title {
      font-size: 13.5px;
      margin-bottom: 2px;
    }
    .final-slide-card .slide-text {
      font-size: 10.5px;
      line-height: 1.28;
      margin-bottom: 2px;
    }
    amp-story-interactive-binary-poll {
      font-size: 9.5px;
      margin: 2px 0;
    }
    .badge {
      font-size: 8px;
      padding: 1.5px 5px;
    }
    .category-pill {
      font-size: 7.5px;
      padding: 1.5px 4px;
    }
    .meta-chips {
      gap: 2.5px;
      margin-top: 3px;
    }
    .chip {
      padding: 1.5px 4px;
      font-size: 8.5px;
    }
    .final-nav-buttons {
      margin-top: 3px;
      gap: 4px;
    }
    .btn-next-story {
      padding: 5px 7px;
      font-size: 10.5px;
    }
    .btn-read-article {
      padding: 5px 6px;
      font-size: 10px;
    }
    .final-nav-row {
      margin-top: 2px;
      padding-top: 2px;
    }
  }

  @media (max-height: 560px) {
    .content-wrapper {
      padding-top: max(10px, env(safe-area-inset-top, 10px));
      padding-bottom: max(6px, env(safe-area-inset-bottom, 6px));
    }
    .final-slide-wrapper {
      padding-bottom: max(48px, calc(env(safe-area-inset-bottom, 0px) + 44px));
    }
    .content-card {
      padding: 4px 7px;
      max-height: 88%;
      border-radius: 10px;
    }
    .cover-title, .slide-title {
      font-size: 12.5px;
      line-height: 1.18;
      margin-bottom: 2px;
    }
    .slide-text {
      font-size: 9.5px;
      line-height: 1.28;
      margin-bottom: 2px;
    }
    .final-slide-card .slide-title {
      font-size: 12px;
      line-height: 1.18;
    }
    .final-slide-card .slide-text {
      font-size: 9.5px;
      line-height: 1.24;
    }
    amp-story-interactive-binary-poll {
      font-size: 9px;
      margin: 2px 0;
    }
    .pulse-indicator {
      display: none;
    }
    .final-nav-buttons {
      margin-top: 2px;
      gap: 4px;
    }
    .btn-next-story, .btn-read-article {
      padding: 4px 5px;
      font-size: 9.5px;
    }
  }

  @media (min-height: 800px) {
    .content-card {
      max-height: 76%;
    }
    .slide-text {
      line-height: 1.44;
    }
  }
"""

_STORY_CATALOG_CACHE = None

def get_next_story_info(current_slug: str, domain: str = DOMAIN_NAME, lang: str = "en") -> Tuple[str, str]:
    """
    Returns (next_story_url, next_story_title) for seamless inter-story chaining on CineStories.
    """
    global _STORY_CATALOG_CACHE
    prefix = "/hi" if lang == "hi" else ""

    if lang == "hi":
        from config import TARGET_BREAKOUT_SLUGS
        slugs = TARGET_BREAKOUT_SLUGS
        if current_slug in slugs:
            curr_idx = slugs.index(current_slug)
            next_slug = slugs[(curr_idx + 1) % len(slugs)]
            try:
                from curated_stories_hi import CURATED_STORIES_HI
                next_title = CURATED_STORIES_HI.get(next_slug, {}).get("title", "अगली कहानी")
            except Exception:
                next_title = "अगली कहानी"
            return f"{domain}/hi/stories/{next_slug}/", next_title
        return f"{domain}/hi/stories/{slugs[0]}/", "अगली कहानी"

    if _STORY_CATALOG_CACHE is None:
        cache_path = Path("dist/stories_cache.json")
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    _STORY_CATALOG_CACHE = json.load(f)
            except Exception:
                _STORY_CATALOG_CACHE = []
        else:
            _STORY_CATALOG_CACHE = []

    if _STORY_CATALOG_CACHE:
        slugs = [s.get("movie", {}).get("slug") for s in _STORY_CATALOG_CACHE if s.get("movie", {}).get("slug")]
        if current_slug in slugs:
            curr_idx = slugs.index(current_slug)
            next_idx = (curr_idx + 1) % len(slugs)
            next_s = _STORY_CATALOG_CACHE[next_idx]
            n_slug = next_s.get("movie", {}).get("slug")
            n_title = next_s.get("movie", {}).get("title") or next_s.get("title", "Next Story")
            return f"{domain}{prefix}/stories/{n_slug}/", n_title
        elif slugs:
            first_s = _STORY_CATALOG_CACHE[0]
            f_slug = first_s.get("movie", {}).get("slug")
            f_title = first_s.get("movie", {}).get("title") or first_s.get("title", "Next Story")
            return f"{domain}{prefix}/stories/{f_slug}/", f_title

    return f"{domain}{prefix}/discover/", ("ट्रेंडिंग कहानियाँ" if lang == "hi" else "Trending Stories")

def build_amp_story_html(story_data: Dict[str, Any], domain: str = DOMAIN_NAME, lang: str = "en") -> str:
    """
    Renders 100% AMP-valid HTML for an AMP Web Story.
    Supports English ("en") and Hindi ("hi") with bilingual hreflang tags,
    crisp Devanagari typography, and strict card containment.
    """
    is_hi = (lang == "hi")
    prefix = "/hi" if is_hi else ""
    html_lang = "hi" if is_hi else "en"
    in_lang = "hi-IN" if is_hi else "en-US"

    movie = story_data.get("movie", {})
    slug = movie.get("slug", "story")
    story_url = f"{domain}{prefix}/stories/{slug}/"
    en_story_url = f"{domain}/stories/{slug}/"
    hi_story_url = f"{domain}/hi/stories/{slug}/"

    story_title = html.escape(story_data.get("title", f"{movie.get('title')}: Web Story"))
    seo_desc = html.escape(story_data.get("seo_description", movie.get("overview", "")))
    publisher = html.escape(PUBLISHER_NAME)
    publisher_logo = get_publisher_logo_url(domain)
    ads_head_script, ads_story_tag = get_amp_story_ads_tags()

    # Portrait poster: 3:4 or 2:3 aspect ratio, min 640x853 px
    poster_path = movie.get("poster_path")
    if poster_path:
        poster_portrait = f"{TMDB_IMAGE_POSTER}{poster_path}"
        poster_square = f"{TMDB_IMAGE_POSTER}{poster_path}"
    else:
        poster_portrait = f"{domain}/assets/logo.png"
        poster_square = f"{domain}/assets/logo.png"

    # Landscape poster: 16:9 backdrop
    primary_backdrop = movie.get("backdrop_path")
    if primary_backdrop:
        poster_landscape = f"{TMDB_IMAGE_ORIGINAL}{primary_backdrop}"
    else:
        poster_landscape = poster_portrait

    # Backdrops list for slide visuals
    raw_backdrops = movie.get("backdrops", [])
    if not raw_backdrops and primary_backdrop:
        raw_backdrops = [primary_backdrop]
    if not raw_backdrops and poster_path:
        raw_backdrops = [poster_path]

    backdrop_urls = [
        f"{TMDB_IMAGE_BACKDROP}{b}" if b.startswith("/") else b
        for b in raw_backdrops
    ] if raw_backdrops else [poster_portrait]

    # Published timestamp in ISO 8601
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pub_iso = story_data.get("date_published") or story_data.get("published_at") or now_iso
    mod_iso = story_data.get("date_modified") or story_data.get("modified_at") or pub_iso

    # Schema.org JSON-LD (NewsArticle & BreadcrumbList for AMP Stories)
    home_breadcrumb = "होम" if is_hi else "Home"
    stories_breadcrumb = "वेब स्टोरीज़" if is_hi else "Web Stories"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "NewsArticle",
                "@id": f"{story_url}#story",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": story_url
                },
                "headline": story_data.get("title", movie.get("title")),
                "image": [poster_portrait, poster_landscape],
                "datePublished": pub_iso,
                "dateModified": mod_iso,
                "inLanguage": in_lang,
                "author": {
                    "@type": "Organization",
                    "name": "CineStories Editorial Board",
                    "url": f"{domain}/about/"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": PUBLISHER_NAME,
                    "url": f"{domain}/",
                    "logo": {
                        "@type": "ImageObject",
                        "url": publisher_logo
                    }
                },
                "description": story_data.get("seo_description", movie.get("overview", ""))
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{story_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": home_breadcrumb,
                        "item": f"{domain}{prefix}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": stories_breadcrumb,
                        "item": f"{domain}{prefix}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": story_data.get("title", movie.get("title")),
                        "item": story_url
                    }
                ]
            }
        ]
    }
    schema_json = json.dumps(schema_data, indent=2)

    # Check for interactive poll elements across slides
    has_interactive = any(bool(s.get("poll")) for s in story_data.get("slides", []))
    interactive_head_script = (
        '    <script async custom-element="amp-story-interactive" src="https://cdn.ampproject.org/v0/amp-story-interactive-0.1.js"></script>'
        if has_interactive else ""
    )

    # Localized labels
    close_text = "बंद करें" if is_hi else "Close"
    close_aria = "कहानी बंद करके होम पर जाएँ" if is_hi else "Close story and return home"
    home_target = f"{prefix}/" if prefix else "/"

    # Generate slides
    slides = story_data.get("slides", [])
    slides_html_parts = []

    for idx, slide in enumerate(slides):
        page_id = f"slide-{idx + 1}"
        is_first = (idx == 0)
        is_last = (idx == len(slides) - 1)

        b_idx = slide.get("backdrop_index", idx) % len(backdrop_urls)
        image_url = backdrop_urls[b_idx]
        image_alt = html.escape(f"{movie.get('title')} - {slide.get('title', 'Scene')}")

        badge_text = html.escape(slide.get("badge", "स्पॉटलाइट" if is_hi else "SPOTLIGHT"))
        slide_heading = html.escape(slide.get("title", ""))
        slide_body = html.escape(slide.get("text", ""))

        raw_cat = movie.get("category", "trending")
        category_name = raw_cat.replace("_", " ")
        if is_hi:
            if raw_cat == "streaming_charts":
                category_name = "साप्ताहिक टॉप 10"
            elif raw_cat == "theories_easter_eggs":
                category_name = "थ्योरीज़ व राज़"
            elif raw_cat == "where_are_they_now":
                category_name = "अब कहाँ हैं?"
            elif raw_cat == "series":
                category_name = "टीवी सीरीज़"
            elif raw_cat == "cult_classic":
                category_name = "कल्ट क्लासिक"

        time_chip = f"📺 {movie.get('seasons')} Seasons" if movie.get("seasons") else f"⏱ {movie.get('runtime', 120)}m"

        top_bar_html = f"""
                  <div class="story-top-bar">
                    <a href="{home_target}" class="story-close-btn" role="button" aria-label="{close_aria}">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                      <b>{close_text}</b>
                    </a>
                    <a href="/about/" class="story-brand-badge" style="text-decoration: none;" aria-label="About {publisher}">⚡ {publisher}</a>
                  </div>
        """

        poll_info = slide.get("poll")
        poll_html = ""
        if poll_info:
            p_id = html.escape(str(poll_info.get("id") or f"poll-{movie.get('slug', 'story')}-{idx + 1}"))
            p_prompt = html.escape(str(poll_info.get("prompt") or ("आपकी क्या राय है?" if is_hi else "What is your verdict?")))
            p_opt1 = html.escape(str(poll_info.get("option1") or ("हाँ" if is_hi else "Yes")))
            p_opt2 = html.escape(str(poll_info.get("option2") or ("नहीं" if is_hi else "No")))
            p_endpoint = f"{domain}/api/poll"
            poll_html = f"""
                    <amp-story-interactive-binary-poll
                      id="{p_id}"
                      endpoint="{p_endpoint}"
                      prompt-text="{p_prompt}"
                      option-1-text="{p_opt1}"
                      option-2-text="{p_opt2}"
                      theme="dark"
                      chip-style="shadow"
                      option-1-confetti="🔥"
                      option-2-confetti="🍿">
                    </amp-story-interactive-binary-poll>"""

        if is_first:
            # Slide 1: Cover slide
            slide_content = f"""
            <amp-story-page id="{page_id}">
              <amp-story-grid-layer template="fill">
                <amp-img src="{image_url}" width="720" height="1280" layout="fill" alt="{image_alt}"></amp-img>
                <div class="scrim-overlay"></div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical">
                <div class="content-wrapper">
{top_bar_html}
                  <div class="content-card" animate-in="fade-in">
                    <div class="badge-row">
                      <span class="badge"><i class="pulse-indicator"></i>{badge_text}</span>
                      <span class="category-pill">{category_name}</span>
                    </div>
                    <h1 class="cover-title" animate-in="fly-in-bottom" animate-in-delay="0.15s">{html.escape(movie.get('title', ''))}</h1>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.25s">{slide_body}</p>
                    <div class="meta-chips">
                      <div class="chip">📅 {html.escape(str(movie.get('release_date', 'Coming Soon')))}</div>
                      <div class="chip chip-rating">★ {html.escape(str(movie.get('vote_average', '8.0')))}</div>
                      <div class="chip">{html.escape(time_chip)}</div>
                    </div>
                  </div>
                </div>
              </amp-story-grid-layer>
            </amp-story-page>
            """
        elif is_last:
            # Final Slide: Inter-story chaining & Next Story on site
            movie_slug = movie.get("slug", "")
            next_url = story_data.get("next_story_url")
            next_title = story_data.get("next_story_title")
            article_url = f"{domain}{prefix}/articles/{movie_slug}/" if movie_slug else f"{domain}{prefix}/discover/"

            if not next_url:
                next_url, next_title = get_next_story_info(movie_slug, domain=domain, lang=lang)

            cta_url = html.escape(next_url)
            if is_hi:
                cta_text = f"अगली कहानी: {next_title} ➔" if next_title and len(f"अगली कहानी: {next_title} ➔") <= 38 else "अगली कहानी पढ़ें ➔"
            else:
                cta_text = f"Read Next: {next_title} ➔" if next_title and len(f"Read Next: {next_title} ➔") <= 38 else "Read Next Story ➔"

            final_title = slide.get("title") or (f"अगली कहानी: {next_title}" if is_hi else f"Up Next: {next_title}")
            final_text = slide.get("text") or (
                "अगली ट्रेंडिंग विजुअल कहानी देखने के लिए नीचे टैप करें, या पूरा आर्टिकल पढ़ें।"
                if is_hi else
                "Tap below to keep the momentum going with our next trending visual story, or dive into the full article."
            )

            # Replace any external TMDB references in slide text
            if "themoviedb.org" in final_text or "showtimes" in final_text.lower():
                final_text = (
                    "अगली ट्रेंडिंग वेब स्टोरी देखने के लिए नीचे टैप करें, या पूरा आर्टिकल पढ़ें।"
                    if is_hi else
                    "Swipe up or tap below to explore our next trending cinematic web story, or read the full article."
                )

            next_btn_label = "अगली कहानी" if is_hi else "Read Next Story"
            article_btn_label = "पूरा आर्टिकल" if is_hi else "Full Article"
            home_btn_label = "सभी कहानियाँ देखें" if is_hi else "Explore All Stories"
            legal_about = "हमारे बारे में" if is_hi else "About"
            legal_editorial = "संपादकीय" if is_hi else "Editorial"
            legal_privacy = "गोपनीयता" if is_hi else "Privacy"
            legal_terms = "नियम" if is_hi else "Terms"
            legal_contact = "संपर्क" if is_hi else "Contact"

            slide_content = f"""
            <amp-story-page id="{page_id}">
              <amp-story-grid-layer template="fill">
                <amp-img src="{image_url}" width="720" height="1280" layout="fill" alt="{image_alt}"></amp-img>
                <div class="scrim-overlay"></div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical">
                <div class="content-wrapper final-slide-wrapper">
{top_bar_html}
                  <div class="content-card final-slide-card" animate-in="fade-in">
                    <div class="badge-row">
                      <span class="badge">{badge_text}</span>
                      <span class="category-pill">{category_name}</span>
                    </div>
                    <h2 class="slide-title" animate-in="fly-in-bottom" animate-in-delay="0.1s">{html.escape(final_title)}</h2>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.2s">{html.escape(final_text)}</p>
{poll_html}
                    <div class="final-nav-buttons">
                      <a href="{cta_url}" class="btn-next-story">
                        <b>{next_btn_label}</b>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                      </a>
                      <a href="{article_url}" class="btn-read-article">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                        <b>{article_btn_label}</b>
                      </a>
                    </div>
                    <div class="final-nav-row">
                      <a href="{home_target}" class="btn-return-home">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                        <b>{home_btn_label}</b>
                      </a>
                    </div>
                    <div class="final-legal-row">
                      <a href="/about/">{legal_about}</a>
                      <a href="/editorial/">{legal_editorial}</a>
                      <a href="/privacy/">{legal_privacy}</a>
                      <a href="/terms/">{legal_terms}</a>
                      <a href="/contact/">{legal_contact}</a>
                    </div>
                  </div>
                </div>
              </amp-story-grid-layer>
              <amp-story-page-outlink layout="nodisplay">
                <a href="{cta_url}">{cta_text}</a>
              </amp-story-page-outlink>
            </amp-story-page>
            """
        else:
            # Middle slides (2 to N-1)
            cast_preview = ""
            if idx == 2 and movie.get("top_cast") and not is_hi:
                cast_preview = "".join([f'<span class="chip">👤 {html.escape(c)}</span>' for c in movie.get("top_cast")[:3]])
                cast_preview = f'<div class="meta-chips">{cast_preview}</div>'

            slide_content = f"""
            <amp-story-page id="{page_id}">
              <amp-story-grid-layer template="fill">
                <amp-img src="{image_url}" width="720" height="1280" layout="fill" alt="{image_alt}"></amp-img>
                <div class="scrim-overlay"></div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical">
                <div class="content-wrapper">
{top_bar_html}
                  <div class="content-card" animate-in="fade-in">
                    <div class="badge-row">
                      <span class="badge">{badge_text}</span>
                    </div>
                    <h2 class="slide-title" animate-in="fly-in-bottom" animate-in-delay="0.1s">{slide_heading}</h2>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.2s">{slide_body}</p>
{poll_html}
                    {cast_preview}
                  </div>
                </div>
              </amp-story-grid-layer>
            </amp-story-page>
            """
        slides_html_parts.append(slide_content.strip())

    slides_combined = "\n    ".join(slides_html_parts)

    html_document = f"""<!doctype html>
<html ⚡ lang="{html_lang}">
  <head>
    <meta charset="utf-8">
    <title>{story_title}</title>
    <link rel="canonical" href="{story_url}">
    
    <!-- Bidirectional Hreflangs -->
    <link rel="alternate" hreflang="en" href="{en_story_url}">
    <link rel="alternate" hreflang="hi" href="{hi_story_url}">
    <link rel="alternate" hreflang="x-default" href="{en_story_url}">

    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <meta name="description" content="{seo_desc}">

    <!-- Open Graph & Social -->
    <meta property="og:title" content="{story_title}">
    <meta property="og:description" content="{seo_desc}">
    <meta property="og:image" content="{poster_portrait}">
    <meta property="og:url" content="{story_url}">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{pub_iso}">
    <meta property="article:modified_time" content="{mod_iso}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{story_title}">
    <meta name="twitter:description" content="{seo_desc}">
    <meta name="twitter:image" content="{poster_portrait}">

    <!-- Google Fonts with Devanagari -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">

    <!-- AMP Core and Story Extension Scripts -->
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
    <script async custom-element="amp-analytics" src="https://cdn.ampproject.org/v0/amp-analytics-0.1.js"></script>
{interactive_head_script}
{ads_head_script}

    <!-- AMP Boilerplate CSS -->
    {AMP_BOILERPLATE}

    <!-- Custom AMP CSS -->
    <style amp-custom>
{AMP_CUSTOM_CSS}
    </style>

    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
{schema_json}
    </script>
  </head>
  <body>
    <amp-story
      standalone
      title="{story_title}"
      publisher="{publisher}"
      publisher-logo-src="{publisher_logo}"
      poster-portrait-src="{poster_portrait}"
      poster-square-src="{poster_square}"
      poster-landscape-src="{poster_landscape}">

      <amp-analytics type="gtag">
        <script type="application/json">
        {{
          "vars": {{
            "gtag_id": "{GA_MEASUREMENT_ID}",
            "config": {{
              "{GA_MEASUREMENT_ID}": {{ "groups": "default" }}
            }}
          }}
        }}
        </script>
      </amp-analytics>
{ads_story_tag}

      {slides_combined}

    </amp-story>
  </body>
</html>
"""
    return html_document
