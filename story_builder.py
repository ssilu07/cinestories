"""
AMP Story HTML Builder module for CineStories.
Renders 100% AMP-valid, standalone Google Web Stories adhering strictly to
the Google AMP Web Story specifications and SEO Discover guidelines.
"""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from config import (
    DOMAIN_NAME,
    PUBLISHER_NAME,
    get_publisher_logo_url,
    TMDB_IMAGE_ORIGINAL,
    TMDB_IMAGE_POSTER
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
    --card-bg: rgba(10, 14, 23, 0.82);
    --border-subtle: rgba(255, 255, 255, 0.14);
    --text-main: #ffffff;
    --text-muted: #cbd5e1;
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
      rgba(9, 11, 16, 0.35) 0%,
      rgba(9, 11, 16, 0.1) 30%,
      rgba(9, 11, 16, 0.75) 70%,
      rgba(9, 11, 16, 0.96) 100%
    );
    pointer-events: none;
  }
  .content-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    height: 100%;
    padding: 24px 20px 48px;
    box-sizing: border-box;
  }
  .content-card {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 22px 20px;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.55);
  }
  .badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary) 0%, var(--gold) 100%);
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
  }
  .category-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    color: #f1f5f9;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 3px 8px;
    border-radius: 6px;
    margin-left: 6px;
    vertical-align: middle;
  }
  .slide-title {
    font-size: 24px;
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 10px 0;
    color: #ffffff;
    letter-spacing: -0.3px;
  }
  .cover-title {
    font-size: 30px;
    font-weight: 900;
    line-height: 1.15;
    margin: 0 0 12px 0;
    color: #ffffff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
  }
  .slide-text {
    font-size: 15px;
    line-height: 1.5;
    color: var(--text-muted);
    margin: 0 0 14px 0;
  }
  .meta-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
  }
  .chip {
    font-size: 11px;
    font-weight: 600;
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.1);
    padding: 4px 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .chip-rating {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border-color: rgba(245, 158, 11, 0.3);
  }
  .pulse-indicator {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--primary);
    margin-right: 6px;
    vertical-align: middle;
  }
"""

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
        f"{TMDB_IMAGE_ORIGINAL}{b}" if b.startswith("/") else b
        for b in raw_backdrops
    ] if raw_backdrops else [poster_portrait]

    # Published timestamp in ISO 8601
    now_iso = datetime.now(timezone.utc).isoformat()

    # Schema.org JSON-LD
    schema_data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": story_url,
        "headline": story_data.get("title", movie.get("title")),
        "image": [poster_portrait, poster_landscape],
        "datePublished": now_iso,
        "dateModified": now_iso,
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
                  <div class="content-card" animate-in="fade-in">
                    <div>
                      <span class="badge"><span class="pulse-indicator"></span>{badge_text}</span>
                      <span class="category-pill">{category_name}</span>
                    </div>
                    <h1 class="cover-title" animate-in="fly-in-bottom" animate-in-delay="0.15s">{html.escape(movie.get('title', ''))}</h1>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.25s">{slide_body}</p>
                    <div class="meta-chips">
                      <span class="chip">📅 {html.escape(str(movie.get('release_date', 'Coming Soon')))}</span>
                      <span class="chip chip-rating">★ {html.escape(str(movie.get('vote_average', '8.0')))}</span>
                      <span class="chip">⏱ {html.escape(str(movie.get('runtime', '120')))}m</span>
                    </div>
                  </div>
                </div>
              </amp-story-grid-layer>
            </amp-story-page>
            """
        elif is_last:
            # Final Slide: CTA slide
            cta_text = html.escape(slide.get("cta_text") or "Check Showtimes & Tickets")
            cta_url = html.escape(slide.get("cta_url") or f"https://www.themoviedb.org/movie/{movie.get('id')}")

            slide_content = f"""
            <amp-story-page id="{page_id}">
              <amp-story-grid-layer template="fill">
                <amp-img src="{image_url}" width="720" height="1280" layout="fill" alt="{image_alt}"></amp-img>
                <div class="scrim-overlay"></div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical">
                <div class="content-wrapper">
                  <div class="content-card" animate-in="fade-in">
                    <span class="badge">{badge_text}</span>
                    <h2 class="slide-title" animate-in="fly-in-bottom" animate-in-delay="0.1s">{slide_heading}</h2>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.2s">{slide_body}</p>
                    <div class="meta-chips">
                      <span class="chip">🎬 {html.escape(movie.get('director', 'Acclaimed Director'))}</span>
                      <span class="chip">🍿 TMDB #{movie.get('id')}</span>
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
                  <div class="content-card" animate-in="fade-in">
                    <span class="badge">{badge_text}</span>
                    <h2 class="slide-title" animate-in="fly-in-bottom" animate-in-delay="0.1s">{slide_heading}</h2>
                    <p class="slide-text" animate-in="fly-in-bottom" animate-in-delay="0.2s">{slide_body}</p>
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

      {slides_combined}

    </amp-story>
  </body>
</html>
"""
    return html_document
