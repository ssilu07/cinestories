"""
AMP Story HTML Builder module for CineStories.
Renders 100% AMP-valid, standalone Google Web Stories adhering strictly to
the Google AMP Web Story specifications and SEO Discover guidelines.
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
    --card-bg: rgba(10, 14, 24, 0.88);
    --border-subtle: rgba(255, 255, 255, 0.16);
    --text-main: #ffffff;
    --text-muted: #e2e8f0;
  }
  amp-story {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
    padding: max(20px, env(safe-area-inset-top, 20px)) clamp(10px, 3.2vw, 16px) max(14px, env(safe-area-inset-bottom, 14px));
    box-sizing: border-box;
    pointer-events: none;
    width: 100%;
    max-width: 520px;
    margin: 0 auto;
  }
  .final-slide-wrapper {
    padding-bottom: max(48px, calc(env(safe-area-inset-bottom, 0px) + 48px));
  }
  .story-top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: auto;
    padding-right: 44px;
    box-sizing: border-box;
    z-index: 10;
    pointer-events: auto;
    gap: 8px;
  }
  .story-close-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(9, 11, 16, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.28);
    color: #ffffff;
    padding: 6px 12px 6px 9px;
    border-radius: 999px;
    text-decoration: none;
    font-size: clamp(11.5px, 2.8vw, 13px);
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
    font-size: clamp(9.5px, 2.4vw, 11px);
    font-weight: 700;
    color: #fbbf24;
    background: rgba(9, 11, 16, 0.78);
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(251, 191, 36, 0.3);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .content-card {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-subtle);
    border-radius: clamp(14px, 3.8vw, 20px);
    padding: clamp(11px, 2.8vw, 16px) clamp(12px, 3vw, 16px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.72), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    margin-top: auto;
    margin-bottom: 2px;
    pointer-events: auto;
    width: 100%;
    box-sizing: border-box;
    max-height: min(64%, 490px);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .content-card::-webkit-scrollbar {
    display: none;
  }
  .final-nav-buttons {
    display: flex;
    gap: 8px;
    margin-top: clamp(6px, 1.5vw, 10px);
    flex-wrap: wrap;
    align-items: center;
  }
  .btn-next-story {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: linear-gradient(135deg, var(--primary) 0%, #f43f5e 100%);
    color: #ffffff;
    text-decoration: none;
    font-size: clamp(12px, 2.7vw, 13px);
    font-weight: 800;
    padding: 7px clamp(12px, 2.6vw, 15px);
    border-radius: 999px;
    box-shadow: 0 4px 12px var(--primary-glow);
    flex: 1 1 140px;
    min-width: 120px;
    letter-spacing: 0.3px;
    box-sizing: border-box;
  }
  .btn-read-article {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    background: rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    text-decoration: none;
    font-size: clamp(11.5px, 2.5vw, 12.5px);
    font-weight: 600;
    padding: 6.5px clamp(10px, 2.2vw, 13px);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-sizing: border-box;
    white-space: nowrap;
  }
  .final-nav-row {
    margin-top: clamp(6px, 1.4vw, 8px);
    padding-top: clamp(5px, 1.2vw, 8px);
    border-top: 1px solid rgba(255, 255, 255, 0.12);
  }
  .btn-return-home {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #38bdf8;
    text-decoration: none;
    font-size: clamp(11.5px, 2.6vw, 12.5px);
    font-weight: 700;
  }
  .badge-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: clamp(4px, 1.2vw, 7px);
  }
  .badge {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, var(--primary) 0%, var(--gold) 100%);
    color: #ffffff;
    font-size: clamp(9px, 2.2vw, 10.5px);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: clamp(0.5px, 0.2vw, 1px);
    padding: 2.5px clamp(7px, 1.8vw, 10px);
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
    font-size: clamp(8.5px, 2vw, 9.5px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    padding: 2px 7px;
    border-radius: 6px;
    margin-left: 0;
    vertical-align: middle;
    white-space: nowrap;
    line-height: 1.2;
  }
  .slide-title {
    font-size: clamp(16px, 4.2vw, 21px);
    font-weight: 800;
    line-height: 1.24;
    margin: 0 0 clamp(4px, 1.2vw, 8px) 0;
    color: #ffffff;
    letter-spacing: -0.2px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }
  .cover-title {
    font-size: clamp(18px, 4.8vw, 24px);
    font-weight: 900;
    line-height: 1.2;
    margin: 0 0 clamp(4px, 1.2vw, 8px) 0;
    color: #ffffff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }
  .slide-text {
    font-size: clamp(12.5px, 3.1vw, 14px);
    line-height: 1.42;
    color: var(--text-muted);
    margin: 0 0 clamp(6px, 1.5vw, 10px) 0;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 5;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .meta-chips {
    display: flex;
    flex-wrap: wrap;
    gap: clamp(4px, 1.2vw, 6px);
    margin-top: clamp(4px, 1.2vw, 8px);
  }
  .chip {
    display: inline-flex;
    align-items: center;
    font-size: clamp(9.5px, 2.3vw, 10.5px);
    font-weight: 600;
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.1);
    padding: 2.5px clamp(6px, 1.5vw, 8px);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    white-space: nowrap;
    line-height: 1.25;
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
    margin-right: 5px;
    vertical-align: middle;
  }
  @media (max-width: 360px) {
    .content-wrapper {
      padding-left: 8px;
      padding-right: 8px;
    }
    .content-card {
      padding: 9px 10px;
      border-radius: 12px;
      max-height: 68%;
    }
    .story-top-bar {
      padding-right: 32px;
    }
    .story-close-btn span {
      display: none;
    }
    .story-close-btn {
      padding: 5px;
      border-radius: 50%;
    }
    .btn-next-story {
      font-size: 11.5px;
      padding: 6px 10px;
    }
    .btn-read-article {
      font-size: 11px;
      padding: 5.5px 8px;
    }
  }
  @media (max-height: 680px) {
    .content-wrapper {
      padding-top: max(16px, env(safe-area-inset-top, 16px));
      padding-bottom: max(10px, env(safe-area-inset-bottom, 10px));
    }
    .final-slide-wrapper {
      padding-bottom: max(42px, calc(env(safe-area-inset-bottom, 0px) + 42px));
    }
    .content-card {
      padding: 9px 11px;
      border-radius: 13px;
      max-height: 68%;
    }
    .cover-title {
      font-size: 17px;
      margin-bottom: 3px;
    }
    .slide-title {
      font-size: 15px;
      margin-bottom: 3px;
    }
    .slide-text {
      font-size: 11.5px;
      line-height: 1.35;
      -webkit-line-clamp: 4;
      margin-bottom: 5px;
    }
    .badge {
      font-size: 8.5px;
      padding: 2px 6px;
    }
    .category-pill {
      font-size: 8px;
      padding: 2px 5px;
    }
    .meta-chips {
      gap: 3px;
      margin-top: 4px;
    }
    .chip {
      padding: 2px 5px;
      font-size: 9px;
    }
  }
  @media (min-height: 800px) {
    .content-card {
      max-height: 60%;
    }
    .slide-text {
      -webkit-line-clamp: 5;
    }
  }
"""

_STORY_CATALOG_CACHE = None

def get_next_story_info(current_slug: str, domain: str = DOMAIN_NAME) -> Tuple[str, str]:
    """
    Returns (next_story_url, next_story_title) for seamless inter-story chaining on cinematicbites.com.
    """
    global _STORY_CATALOG_CACHE
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
            return f"{domain}/stories/{n_slug}/", n_title
        elif slugs:
            first_s = _STORY_CATALOG_CACHE[0]
            f_slug = first_s.get("movie", {}).get("slug")
            f_title = first_s.get("movie", {}).get("title") or first_s.get("title", "Next Story")
            return f"{domain}/stories/{f_slug}/", f_title

    return f"{domain}/discover/", "Trending Stories"

def build_amp_story_html(story_data: Dict[str, Any], domain: str = DOMAIN_NAME) -> str:
    """
    Renders 100% AMP-valid HTML for an AMP Web Story.
    """
    movie = story_data.get("movie", {})
    slug = movie.get("slug", "story")
    story_url = f"{domain}/stories/{slug}/"
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
    now_iso = datetime.now(timezone.utc).isoformat()
    pub_iso = story_data.get("date_published") or story_data.get("published_at") or now_iso
    mod_iso = story_data.get("date_modified") or story_data.get("modified_at") or pub_iso

    # Schema.org JSON-LD
    schema_data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": story_url,
        "headline": story_data.get("title", movie.get("title")),
        "image": [poster_portrait, poster_landscape],
        "datePublished": pub_iso,
        "dateModified": mod_iso,
        "author": {
            "@type": "Organization",
            "name": PUBLISHER_NAME,
            "url": domain
        },
        "publisher": {
            "@type": "Organization",
            "name": PUBLISHER_NAME,
            "logo": {
                "@type": "ImageObject",
                "url": publisher_logo
            }
        },
        "description": story_data.get("seo_description", movie.get("overview", ""))
    }
    schema_json = json.dumps(schema_data, indent=2)

    # Check for interactive poll elements across slides
    has_interactive = any(bool(s.get("poll")) for s in story_data.get("slides", []))
    interactive_head_script = (
        '    <script async custom-element="amp-story-interactive" src="https://cdn.ampproject.org/v0/amp-story-interactive-0.1.js"></script>'
        if has_interactive else ""
    )

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

        badge_text = html.escape(slide.get("badge", "SPOTLIGHT"))
        slide_heading = html.escape(slide.get("title", ""))
        slide_body = html.escape(slide.get("text", ""))

        category_name = movie.get("category", "trending").replace("_", " ")
        time_chip = f"📺 {movie.get('seasons')} Seasons" if movie.get("seasons") else f"⏱ {movie.get('runtime', 120)}m"

        top_bar_html = f"""
                  <div class="story-top-bar">
                    <a href="/" class="story-close-btn" role="button" aria-label="Close story and return home">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                      <span>Close</span>
                    </a>
                    <span class="story-brand-badge">⚡ {publisher}</span>
                  </div>
        """

        poll_info = slide.get("poll")
        poll_html = ""
        if poll_info:
            p_id = html.escape(str(poll_info.get("id") or f"poll-{movie.get('slug', 'story')}-{idx + 1}"))
            p_prompt = html.escape(str(poll_info.get("prompt") or "What is your verdict?"))
            p_opt1 = html.escape(str(poll_info.get("option1") or "Yes"))
            p_opt2 = html.escape(str(poll_info.get("option2") or "No"))
            p_endpoint = f"{domain}/api/poll"
            poll_html = f"""
                    <amp-story-interactive-binary-poll
                      id="{p_id}"
                      endpoint="{p_endpoint}"
                      prompt-text="{p_prompt}"
                      option-1-text="{p_opt1}"
                      option-2-text="{p_opt2}">
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
                      <span class="badge"><span class="pulse-indicator"></span>{badge_text}</span>
                      <span class="category-pill">{category_name}</span>
                    </div>
                    <h1 class="cover-title" animate-in="fly-in-bottom" animate-in-delay="0.15s">{html.escape(movie.get('title', ''))}</h1>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.25s">{slide_body}</p>
                    <div class="meta-chips">
                      <span class="chip">📅 {html.escape(str(movie.get('release_date', 'Coming Soon')))}</span>
                      <span class="chip chip-rating">★ {html.escape(str(movie.get('vote_average', '8.0')))}</span>
                      <span class="chip">{html.escape(time_chip)}</span>
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
            article_url = f"{domain}/articles/{movie_slug}/" if movie_slug else f"{domain}/discover/"

            if not next_url:
                next_url, next_title = get_next_story_info(movie_slug, domain=domain)

            # Never link to themoviedb.org or external sites
            cta_url = html.escape(next_url)
            cta_text = f"Read Next: {next_title} ➔" if next_title and len(f"Read Next: {next_title} ➔") <= 38 else "Read Next Story ➔"

            final_title = slide.get("title") or f"Up Next: {next_title}"
            final_text = slide.get("text") or "Tap below to keep the momentum going with our next trending visual story, or dive into the full article."

            # Replace any external TMDB references in slide text
            if "themoviedb.org" in final_text or "showtimes" in final_text.lower():
                final_text = "Swipe up or tap below to explore our next trending cinematic web story, or read the full article."

            slide_content = f"""
            <amp-story-page id="{page_id}">
              <amp-story-grid-layer template="fill">
                <amp-img src="{image_url}" width="720" height="1280" layout="fill" alt="{image_alt}"></amp-img>
                <div class="scrim-overlay"></div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical">
                <div class="content-wrapper final-slide-wrapper">
{top_bar_html}
                  <div class="content-card" animate-in="fade-in">
                    <div class="badge-row">
                      <span class="badge">{badge_text}</span>
                      <span class="category-pill">{category_name}</span>
                    </div>
                    <h2 class="slide-title" animate-in="fly-in-bottom" animate-in-delay="0.1s">{html.escape(final_title)}</h2>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.2s">{html.escape(final_text)}</p>
{poll_html}
                    <div class="final-nav-buttons">
                      <a href="{cta_url}" class="btn-next-story">
                        <span>Read Next Story</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                      </a>
                      <a href="{article_url}" class="btn-read-article">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                        <span>Full Article</span>
                      </a>
                    </div>
                    <div class="final-nav-row">
                      <a href="/" class="btn-return-home">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                        <span>Explore All Stories</span>
                      </a>
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
            if idx == 2 and movie.get("top_cast"):
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
<html ⚡ lang="en">
  <head>
    <meta charset="utf-8">
    <title>{story_title}</title>
    <link rel="canonical" href="{story_url}">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <meta name="description" content="{seo_desc}">

    <!-- Open Graph & Social -->
    <meta property="og:title" content="{story_title}">
    <meta property="og:description" content="{seo_desc}">
    <meta property="og:image" content="{poster_portrait}">
    <meta property="og:url" content="{story_url}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{story_title}">
    <meta name="twitter:description" content="{seo_desc}">
    <meta name="twitter:image" content="{poster_portrait}">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">

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
