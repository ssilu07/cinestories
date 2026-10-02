"""
Homepage Builder module for CineStories.
Generates dist/index.html: a modern, mobile-friendly, responsive portal
showcasing all generated AMP Web Stories with interactive filtering and search.
"""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from config import (
    DOMAIN_NAME,
    SITE_NAME,
    SITE_TAGLINE,
    DIST_DIR,
    TMDB_IMAGE_POSTER
)

def build_homepage_html(stories: List[Dict[str, Any]], domain: str = DOMAIN_NAME) -> str:
    """
    Renders the modern, dark cinema-themed landing page.
    """
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    total_stories = len(stories)
    streaming_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "streaming_charts")
    theories_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "theories_easter_eggs")
    sitcoms_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "where_are_they_now")
    series_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "series")
    trending_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "trending")
    cult_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "cult_classic")
    upcoming_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "upcoming")

    # Prepare cards data
    cards_data = []
    for s in stories:
        m = s.get("movie", {})
        slug = m.get("slug", "story")
        poster = m.get("poster_path")
        poster_url = f"{TMDB_IMAGE_POSTER}{poster}" if poster else f"{domain}/assets/logo.png"
        backdrop = m.get("backdrop_path")
        backdrop_url = f"{TMDB_IMAGE_POSTER}{backdrop}" if backdrop else poster_url
        title = s.get("title") or m.get("hook_title") or m.get("title", "")
        teaser = m.get("catchy_teaser") or s.get("seo_description", "")
        
        cards_data.append({
            "title": title,
            "movie_title": m.get("title", ""),
            "slug": slug,
            "url": f"/stories/{slug}/",
            "poster_url": poster_url,
            "backdrop_url": backdrop_url,
            "teaser": teaser,
            "media_type": m.get("media_type", "movie"),
            "category": m.get("category", "trending"),
            "release_date": m.get("release_date", "Coming Soon"),
            "rating": m.get("vote_average", 0.0),
            "runtime": m.get("runtime", 120),
            "seasons": m.get("seasons"),
            "director": m.get("director", ""),
            "genres": m.get("genres", []),
            "slides_count": len(s.get("slides", []))
        })

    cards_json = json.dumps(cards_data)

    cards_html_list = []
    for c in cards_data:
        if c["category"] == "streaming_charts":
            category_label = "Weekly Top 10"
        elif c["category"] == "theories_easter_eggs":
            category_label = "Marvel & DC Theories"
        elif c["category"] == "where_are_they_now":
            category_label = "Where Are They Now?"
        elif c["category"] == "series":
            category_label = "TV Series"
        elif c["category"] == "cult_classic":
            category_label = "Cult Classic"
        else:
            category_label = c["category"].replace("_", " ").title()

        badge_class = f"badge-{c['category']}"
        genres_str = " • ".join(c["genres"][:2]) if c["genres"] else ("TV Drama" if c["media_type"] == "tv" else "Cinema")
        time_info = f"📺 {c['seasons']} Seasons" if c.get("seasons") else f"⏱ {c['runtime']}m"

        card_html = f"""
        <article class="story-card" data-category="{c['category']}" data-title="{html.escape(c['title'].lower())}" data-movie="{html.escape(c['movie_title'].lower())}" data-rating="{c['rating']}">
          <a href="{c['url']}" class="card-link" aria-label="Read story for {html.escape(c['movie_title'])}">
            <div class="card-poster-wrap">
              <img src="{c['poster_url']}" alt="{html.escape(c['movie_title'])}" class="card-poster" loading="lazy" width="300" height="450" onerror="this.onerror=null;this.src='{c['backdrop_url']}';">
              <div class="card-overlay-gradient"></div>
              
              <div class="card-top-badges">
                <span class="category-badge {badge_class}">{category_label}</span>
                <span class="rating-badge">★ {c['rating']}</span>
              </div>

              <div class="card-bottom-info">
                <div class="card-kicker">
                  <span class="movie-name-tag">{html.escape(c['movie_title'])}</span>
                  <span class="slides-counter"><span class="amp-icon">⚡</span> {c['slides_count']} Slides</span>
                </div>
                <h3 class="card-title">{html.escape(c['title'])}</h3>
                <p class="card-teaser">{html.escape(c['teaser'])}</p>
                <div class="card-meta">
                  <span>{html.escape(c['release_date'][:4] if len(c['release_date']) >= 4 else c['release_date'])}</span>
                  <span>•</span>
                  <span>{html.escape(time_info)}</span>
                </div>
                <div class="read-prompt">
                  <span>Tap to open Web Story</span>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </div>
              </div>
            </div>
          </a>
        </article>
        """
        cards_html_list.append(card_html.strip())

    cards_grid_html = "\n".join(cards_html_list)

    html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{SITE_NAME} | {SITE_TAGLINE}</title>
  <meta name="description" content="Discover automated, 100% AMP-compliant visual Web Stories for upcoming, trending, and now-playing movies. Powered by TMDB and Gemini AI.">
  <link rel="canonical" href="{domain}/">
  <link rel="icon" type="image/svg+xml" href="{domain}/assets/favicon.svg">
  <meta name="google-site-verification" content="XMDt3lDT2kpdjLlHlxQCSn5EcJcH2yw8f6nLjhLgN7g">

  <!-- Open Graph / Social -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{domain}/">
  <meta property="og:title" content="{SITE_NAME} | {SITE_TAGLINE}">
  <meta property="og:description" content="Experience movie stories in Google AMP Web Story format. Bite-sized, cinematic visual entertainment guides.">
  <meta property="og:image" content="{domain}/assets/logo.png">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg: #090b10;
      --surface: #10141f;
      --surface-border: rgba(255, 255, 255, 0.08);
      --primary: #e11d48;
      --primary-hover: #f43f5e;
      --accent-gold: #f59e0b;
      --text: #ffffff;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --radius-lg: 20px;
      --radius-md: 12px;
      --radius-sm: 8px;
      --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Top Navigation Bar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 16px 24px;
    }}

    .nav-container {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text);
    }}

    .brand-logo {{
      width: 42px;
      height: 42px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.35);
    }}

    .brand-text h1 {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.1;
    }}

    .brand-text p {{
      font-size: 11px;
      color: var(--accent-gold);
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      text-decoration: none;
      transition: var(--transition);
      cursor: pointer;
    }}

    .btn-outline {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid var(--surface-border);
    }}

    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}

    .amp-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(225, 29, 72, 0.15);
      border: 1px solid rgba(225, 29, 72, 0.3);
      color: #fda4af;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
    }}

    /* Hero Section */
    .hero {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 48px 24px 32px;
      width: 100%;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(135deg, rgba(225, 29, 72, 0.2), rgba(245, 158, 11, 0.2));
      border: 1px solid rgba(245, 158, 11, 0.3);
      color: var(--accent-gold);
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}

    .hero-title {{
      font-size: clamp(32px, 5vw, 54px);
      font-weight: 900;
      letter-spacing: -1.5px;
      line-height: 1.1;
      margin-bottom: 16px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
      font-size: 17px;
      color: var(--text-muted);
      max-width: 680px;
      line-height: 1.6;
      margin-bottom: 28px;
    }}

    /* Filters Bar */
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 32px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 12px 16px;
    }}

    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .filter-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 999px;
      cursor: pointer;
      transition: var(--transition);
      font-family: inherit;
    }}

    .filter-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }}

    .filter-btn.active {{
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 14px rgba(225, 29, 72, 0.4);
    }}

    .search-box {{
      position: relative;
      min-width: 240px;
      flex-grow: 1;
      max-width: 360px;
    }}

    .search-box input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: #fff;
      padding: 9px 16px 9px 38px;
      font-size: 13px;
      border-radius: 999px;
      outline: none;
      font-family: inherit;
      transition: var(--transition);
    }}

    .search-box input:focus {{
      border-color: var(--primary);
      background: rgba(255, 255, 255, 0.1);
    }}

    .search-box svg {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }}

    /* Stories Grid */
    .stories-section {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px 64px;
      width: 100%;
      flex-grow: 1;
    }}

    .stories-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 24px;
    }}

    /* Story Card */
    .story-card {{
      position: relative;
      border-radius: var(--radius-lg);
      overflow: hidden;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      transition: var(--transition);
    }}

    .story-card:hover {{
      transform: translateY(-6px);
      border-color: rgba(225, 29, 72, 0.4);
      box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.6), 0 0 25px -5px rgba(225, 29, 72, 0.25);
    }}

    .card-link {{
      text-decoration: none;
      color: inherit;
      display: block;
    }}

    .card-poster-wrap {{
      position: relative;
      width: 100%;
      aspect-ratio: 2 / 3;
      overflow: hidden;
      background: #141824;
    }}

    .card-poster {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .story-card:hover .card-poster {{
      transform: scale(1.05);
    }}

    .card-overlay-gradient {{
      position: absolute;
      inset: 0;
      background: linear-gradient(
        180deg,
        rgba(9, 11, 16, 0.2) 0%,
        rgba(9, 11, 16, 0.05) 30%,
        rgba(9, 11, 16, 0.65) 60%,
        rgba(9, 11, 16, 0.98) 100%
      );
    }}

    .card-top-badges {{
      position: absolute;
      top: 14px;
      left: 14px;
      right: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 2;
    }}

    .category-badge {{
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 4px 10px;
      border-radius: 999px;
      backdrop-filter: blur(8px);
    }}

    .badge-streaming_charts {{
      background: linear-gradient(135deg, #e50914, #7928ca);
      color: #fff;
      box-shadow: 0 2px 10px rgba(229, 9, 20, 0.4);
    }}

    .badge-theories_easter_eggs {{
      background: linear-gradient(135deg, #f59e0b, #dc2626);
      color: #fff;
      box-shadow: 0 2px 10px rgba(245, 158, 11, 0.4);
    }}

    .badge-where_are_they_now {{
      background: linear-gradient(135deg, #06b6d4, #f97316);
      color: #fff;
      box-shadow: 0 2px 10px rgba(6, 182, 212, 0.4);
    }}

    .badge-trending {{
      background: rgba(225, 29, 72, 0.85);
      color: #fff;
    }}

    .badge-series {{
      background: linear-gradient(135deg, #0284c7, #8b5cf6);
      color: #fff;
    }}

    .badge-cult_classic {{
      background: linear-gradient(135deg, #ea580c, #b91c1c);
      color: #fff;
    }}

    .badge-upcoming {{
      background: rgba(147, 51, 234, 0.85);
      color: #fff;
    }}

    .badge-now_playing {{
      background: rgba(16, 185, 129, 0.85);
      color: #fff;
    }}

    .rating-badge {{
      font-size: 11px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(0, 0, 0, 0.65);
      padding: 4px 8px;
      border-radius: 6px;
      border: 1px solid rgba(251, 191, 36, 0.3);
      backdrop-filter: blur(8px);
    }}

    .card-bottom-info {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 18px;
      z-index: 2;
    }}

    .card-kicker {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 6px;
    }}

    .movie-name-tag {{
      font-size: 11px;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 60%;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.9);
    }}

    .slides-counter {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-gold);
    }}

    .amp-icon {{
      color: #facc15;
    }}

    .card-title {{
      font-size: 17px;
      font-weight: 800;
      line-height: 1.3;
      color: #fff;
      margin-bottom: 6px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.9);
    }}

    .card-teaser {{
      font-size: 12px;
      line-height: 1.4;
      color: #cbd5e1;
      margin-bottom: 10px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      font-weight: 500;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }}

    .card-meta {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .read-prompt {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 700;
      color: #fff;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      transition: var(--transition);
    }}

    .story-card:hover .read-prompt {{
      color: #fb7185;
    }}

    .read-prompt svg {{
      transition: transform 0.2s ease;
    }}

    .story-card:hover .read-prompt svg {{
      transform: translateX(4px);
    }}

    /* Empty state */
    .empty-state {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
      display: none;
    }}

    .empty-state h3 {{
      font-size: 20px;
      color: #fff;
      margin-bottom: 8px;
    }}

    /* Footer */
    .footer {{
      background: var(--surface);
      border-top: 1px solid var(--surface-border);
      padding: 40px 24px 32px;
      margin-top: auto;
    }}

    .footer-container {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 24px;
      align-items: center;
    }}

    .footer-left p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    .footer-tmdb-notice {{
      font-size: 12px;
      color: var(--text-dim);
      margin-top: 4px;
    }}

    .footer-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .footer-links a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      transition: color 0.2s ease;
    }}

    .footer-links a:hover {{
      color: #fff;
    }}

    /* Fullscreen Story Modal Lightbox */
    .story-modal {{
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      opacity: 0;
      transition: opacity 0.25s ease;
    }}

    .story-modal.active {{
      display: flex;
      opacity: 1;
    }}

    .modal-backdrop {{
      position: absolute;
      inset: 0;
      cursor: pointer;
    }}

    .modal-container {{
      position: relative;
      width: 100%;
      max-width: 440px;
      height: 92vh;
      max-height: 880px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.9), 0 0 40px rgba(225, 29, 72, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: #090b10;
      z-index: 2;
    }}

    @media (max-width: 600px) {{
      .modal-container {{
        max-width: 100%;
        height: 100%;
        max-height: 100vh;
        border-radius: 0;
        border: none;
      }}
    }}

    .modal-close-btn {{
      position: absolute;
      top: 16px;
      right: 16px;
      z-index: 30;
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.35);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
      transition: transform 0.2s ease, background 0.2s ease, border-color 0.2s ease;
    }}

    .modal-close-btn:hover {{
      background: var(--primary);
      border-color: var(--primary);
      transform: scale(1.08);
    }}

    .modal-close-btn:active {{
      transform: scale(0.92);
    }}

    #storyIframe {{
      width: 100%;
      height: 100%;
      border: none;
      display: block;
      background: #090b10;
    }}
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="navbar">
    <div class="nav-container">
      <a href="/" class="brand-wrap">
        <img src="/assets/logo.png" alt="{SITE_NAME} Logo" class="brand-logo">
        <div class="brand-text">
          <h1>{SITE_NAME}</h1>
          <p>AMP Web Stories</p>
        </div>
      </a>

      <div class="nav-actions">
        <span class="amp-pill">⚡ 100% AMP Valid</span>
        <a href="/sitemap.xml" class="btn btn-outline" target="_blank" rel="noopener">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zM22 6l-10 7L2 6"/></svg>
          Sitemap
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Header -->
  <section class="hero">
    <div class="hero-badge">⚡ Discover-Ready Entertainment Stories</div>
    <h2 class="hero-title">Bite-Sized Cinema Stories.<br>Built For The Mobile Screen.</h2>
    <p class="hero-subtitle">
      Explore immersive, fast-loading Google AMP Web Stories. Discover weekly Netflix, HBO &amp; Prime Top 10 releases (US/UK), deep Marvel &amp; DC post-credit theories, and nostalgic &ldquo;Where Are They Now?&rdquo; sitcom retrospectives.
    </p>

    <!-- Controls Bar: Filter Pills & Search -->
    <div class="controls-bar">
      <div class="filter-pills" role="tablist">
        <button class="filter-btn active" data-filter="all">All Stories ({total_stories})</button>
        <button class="filter-btn" data-filter="streaming_charts">Weekly Top 10 ({streaming_count})</button>
        <button class="filter-btn" data-filter="theories_easter_eggs">Marvel &amp; DC Theories ({theories_count})</button>
        <button class="filter-btn" data-filter="where_are_they_now">Where Are They Now? ({sitcoms_count})</button>
        <button class="filter-btn" data-filter="series">TV Series ({series_count})</button>
        <button class="filter-btn" data-filter="trending">Trending Movies ({trending_count})</button>
        <button class="filter-btn" data-filter="cult_classic">Cult &amp; Franchises ({cult_count})</button>
        <button class="filter-btn" data-filter="upcoming">Upcoming ({upcoming_count})</button>
      </div>

      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="searchInput" placeholder="Search by movie or genre..." aria-label="Search stories">
      </div>
    </div>
  </section>

  <!-- Stories Grid Section -->
  <main class="stories-section">
    <div class="stories-grid" id="storiesGrid">
      {cards_grid_html}
      <div class="empty-state" id="emptyState">
        <h3>No matching stories found</h3>
        <p>Try searching for a different movie title or clearing filters.</p>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-left">
        <p>&copy; {datetime.now(timezone.utc).year} {SITE_NAME}. Generated with Google AMP Story 1.0 &amp; Gemini AI.</p>
        <p class="footer-tmdb-notice">This product uses the TMDB API but is not endorsed or certified by TMDB.</p>
      </div>
      <div class="footer-links">
        <a href="/about/">About Us</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms &amp; Disclaimer</a>
        <a href="/contact/">Contact Us</a>
        <a href="/sitemap.xml">XML Sitemap</a>
      </div>
    </div>
  </footer>

  <!-- Fullscreen Story Modal Lightbox -->
  <div class="story-modal" id="storyModal" aria-hidden="true" role="dialog" aria-label="Web Story Viewer">
    <div class="modal-backdrop" id="modalBackdrop"></div>
    <div class="modal-container">
      <button class="modal-close-btn" id="modalCloseBtn" aria-label="Close Web Story">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <iframe id="storyIframe" src="" title="Web Story Viewer" allow="autoplay; fullscreen"></iframe>
    </div>
  </div>

  <!-- Instant Filtering, Search & Modal Script -->
  <script>
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.story-card');
    const emptyState = document.getElementById('emptyState');

    let activeFilter = 'all';
    let searchQuery = '';

    function applyFilters() {{
      let visibleCount = 0;
      cards.forEach(card => {{
        const category = card.getAttribute('data-category');
        const title = card.getAttribute('data-title') || '';
        const movie = card.getAttribute('data-movie') || '';

        const matchesCat = (activeFilter === 'all' || category === activeFilter);
        const matchesQuery = (!searchQuery || title.includes(searchQuery) || movie.includes(searchQuery));

        if (matchesCat && matchesQuery) {{
          card.style.display = '';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      emptyState.style.display = (visibleCount === 0) ? 'block' : 'none';
    }}

    filterBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.getAttribute('data-filter');
        applyFilters();
      }});
    }});

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value.toLowerCase().trim();
      applyFilters();
    }});

    // Story Modal Lightbox Logic
    const storyModal = document.getElementById('storyModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const storyIframe = document.getElementById('storyIframe');

    function openStoryModal(url) {{
      storyIframe.src = url;
      storyModal.classList.add('active');
      storyModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      history.pushState({{ modalOpen: true }}, '', url);
    }}

    function closeStoryModal() {{
      storyModal.classList.remove('active');
      storyModal.setAttribute('aria-hidden', 'true');
      storyIframe.src = '';
      document.body.style.overflow = '';
      if (history.state && history.state.modalOpen) {{
        history.back();
      }}
    }}

    document.querySelectorAll('.card-link').forEach(link => {{
      link.addEventListener('click', (e) => {{
        if (e.ctrlKey || e.metaKey || e.button === 1) return;
        e.preventDefault();
        const url = link.getAttribute('href');
        openStoryModal(url);
      }});
    }});

    modalCloseBtn.addEventListener('click', closeStoryModal);
    modalBackdrop.addEventListener('click', closeStoryModal);

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape' && storyModal.classList.contains('active')) {{
        closeStoryModal();
      }}
    }});

    window.addEventListener('popstate', () => {{
      if (storyModal.classList.contains('active')) {{
        storyModal.classList.remove('active');
        storyModal.setAttribute('aria-hidden', 'true');
        storyIframe.src = '';
        document.body.style.overflow = '';
      }}
    }});
  </script>
</body>
</html>
"""
    return html_content

def generate_homepage(stories: List[Dict[str, Any]], domain: str = DOMAIN_NAME, output_dir: Path = DIST_DIR) -> str:
    """Build and save dist/index.html and dist/stories.json."""
    html_str = build_homepage_html(stories, domain=domain)
    output_dir.mkdir(parents=True, exist_ok=True)
    index_file = output_dir / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_str)

    # Save stories.json manifest
    manifest_data = {
        "site_name": SITE_NAME,
        "domain": domain,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_stories": len(stories),
        "stories": [
            {
                "id": s.get("movie", {}).get("id"),
                "slug": s.get("movie", {}).get("slug"),
                "title": s.get("title"),
                "url": f"{domain}/stories/{s.get('movie', {}).get('slug')}/",
                "category": s.get("movie", {}).get("category"),
                "release_date": s.get("movie", {}).get("release_date"),
                "rating": s.get("movie", {}).get("vote_average")
            }
            for s in stories
        ]
    }
    with open(output_dir / "stories.json", "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    print(f"[Homepage] Generated portal homepage at {index_file} ({len(stories)} stories)")
    return html_str
