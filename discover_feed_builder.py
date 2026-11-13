"""
Discover Feed Builder module for CineStories / MoviePulse.
Generates dist/discover/index.html: a mobile-first, high-engagement Google Chrome Discover-style feed
showcasing rich cinema articles with 1200px+ imagery, snappy headlines, and quick-launch Web Story links.
"""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from config import (
    DOMAIN_NAME,
    SITE_NAME,
    PUBLISHER_NAME,
    DISCOVER_DIR,
    TMDB_IMAGE_BACKDROP,
    TMDB_IMAGE_POSTER,
    get_ga_script,
    get_adsense_script
)

def build_discover_feed_html(
    articles: List[Dict[str, Any]],
    domain: str = DOMAIN_NAME,
    lang: str = "en"
) -> str:
    """
    Renders the Google Chrome Discover-style feed landing page.
    """
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    total_articles = len(articles)
    netflix_count = sum(1 for a in articles if a.get("movie", {}).get("category") == "netflix_hits")

    # Localization navigation paths
    nav_home = "/hi/" if lang == "hi" else "/"
    nav_discover = "/hi/discover/" if lang == "hi" else "/discover/"
    nav_about = "/hi/about/" if lang == "hi" else "/about/"
    nav_editorial = "/hi/editorial/" if lang == "hi" else "/editorial/"
    nav_contact = "/hi/contact/" if lang == "hi" else "/contact/"
    nav_privacy = "/hi/privacy/" if lang == "hi" else "/privacy/"
    nav_terms = "/hi/terms/" if lang == "hi" else "/terms/"
    en_target = "/discover/"
    hi_target = "/hi/discover/"
    canonical_url = f"{domain}/hi/discover/" if lang == "hi" else f"{domain}/discover/"

    feed_cards_data = []
    for art in articles:
        movie = art.get("movie", {})
        slug = movie.get("slug", "story")
        headline = art.get("headline") or f"{movie.get('title')}: Everything You Need To Know"
        meta_desc = art.get("meta_description") or movie.get("overview", "")[:140]
        category = movie.get("category", "trending")
        
        backdrop_path = movie.get("backdrop_path")
        poster_path = movie.get("poster_path")
        backdrop_url = f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path else f"{domain}/assets/logo.png"
        poster_url = f"{TMDB_IMAGE_POSTER}{poster_path}" if poster_path else backdrop_url

        rating = movie.get("vote_average", 0.0)
        reading_time = art.get("reading_time_mins", 3)

        card_art_url = f"/hi/articles/{slug}/" if lang == "hi" else f"/articles/{slug}/"
        card_sty_url = f"/hi/stories/{slug}/" if lang == "hi" else f"/stories/{slug}/"

        feed_cards_data.append({
            "headline": headline,
            "movie_title": movie.get("title", ""),
            "slug": slug,
            "article_url": card_art_url,
            "story_url": card_sty_url,
            "backdrop_url": backdrop_url,
            "poster_url": poster_url,
            "description": meta_desc,
            "category": category,
            "rating": rating,
            "reading_time": reading_time,
            "release_date": movie.get("release_date", "Coming Soon")
        })

    cards_json = json.dumps(feed_cards_data)

    VIRAL_SPOTLIGHT_SLUGS = {
        'panchayat-season-3', 'mirzapur-season-3', 'stree-2', 'kalki-2898-ad',
        'sector-36', 'do-patti', 'devara-part-1', 'pushpa-2-the-rule',
        'squid-game-season-2', 'singham-again'
    }

    cards_html_list = []
    for c in feed_cards_data:
        cat = c["category"]
        if cat == "netflix_hits":
            cat_label = "Netflix Hits"
        elif cat == "streaming_charts":
            cat_label = "Weekly Top 10"
        elif cat == "theories_easter_eggs":
            cat_label = "Marvel & DC Theories"
        elif cat == "where_are_they_now":
            cat_label = "Where Are They Now?"
        elif cat == "series":
            cat_label = "TV Series"
        elif cat == "cult_classic":
            cat_label = "Cult Classic"
        elif cat == "steamy_thrillers":
            cat_label = "Bold & Steamy"
        else:
            cat_label = cat.replace("_", " ").title()

        is_spotlight = c["slug"] in VIRAL_SPOTLIGHT_SLUGS
        spotlight_class = " spotlight-card" if is_spotlight else ""
        spotlight_tag = '<span class="spotlight-tag">🔥 BREAKING CLIMAX DECODER</span>\n              ' if is_spotlight else ""

        card_html = f"""
        <article class="discover-card{spotlight_class}" data-category="{cat}" data-title="{html.escape(c['headline'].lower())}" data-movie="{html.escape(c['movie_title'].lower())}">
          <a href="{c['article_url']}" class="card-media-link" aria-label="{html.escape(c['headline'])}">
            <div class="card-img-wrap">
              <img src="{c['backdrop_url']}" alt="{html.escape(c['headline'])}" class="card-img" loading="lazy" width="600" height="338">
              {spotlight_tag}<span class="card-cat-badge">{cat_label}</span>
              <span class="card-rating-badge">★ {c['rating']}</span>
            </div>
          </a>
          <div class="card-content">
            <div class="card-meta">
              <div class="publisher-meta">
                <img src="/assets/logo.png" alt="{SITE_NAME}" class="pub-logo" width="20" height="20">
                <span class="pub-name">{SITE_NAME}</span>
                <span class="dot-separator">•</span>
                <span class="time-ago">Today</span>
              </div>
              <button class="share-icon-btn" onclick="shareArticle('{c['article_url']}', '{html.escape(c['headline'])}', event)" aria-label="Share article" title="Share this article">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </button>
            </div>
            
            <h2 class="card-title">
              <a href="{c['article_url']}">{html.escape(c['headline'])}</a>
            </h2>

            <p class="card-snippet">{html.escape(c['description'])}</p>

            <div class="card-footer-actions">
              <a href="{c['article_url']}" class="btn-read">
                <span>📖 Read Article</span>
                <span class="read-duration">{c['reading_time']} min</span>
              </a>
              <a href="{c['story_url']}" class="btn-story" title="Launch fast AMP Web Story">
                <span>⚡ Web Story</span>
              </a>
            </div>
          </div>
        </article>
        """
        cards_html_list.append(card_html)

    cards_html = "\n".join(cards_html_list)

    return f"""<!doctype html>
<html lang="{ 'hi' if lang == 'hi' else 'en' }">
<head>
{get_ga_script()}
{get_adsense_script()}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Google Discover Feed | {SITE_NAME} Cinema News & Deep Dives</title>
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="description" content="Explore real-time cinema news, box office breakdowns, fan theories, and streaming hits in our Google Discover entertainment feed.">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="en" href="{domain}/discover/">
  <link rel="alternate" hreflang="hi" href="{domain}/hi/discover/">
  <link rel="alternate" hreflang="x-default" href="{domain}/discover/">
  
  <meta property="og:type" content="website">
  <meta property="og:title" content="Google Discover Feed | {SITE_NAME}">
  <meta property="og:description" content="Daily trending movies, TV series analysis, and visual entertainment stories.">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{domain}/assets/logo.png">

  <!-- Favicon & Fonts -->
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg: #090b10;
      --surface: #10141f;
      --surface-card: #151a28;
      --surface-border: rgba(255, 255, 255, 0.1);
      --primary: #e11d48;
      --primary-hover: #f43f5e;
      --primary-glow: rgba(225, 29, 72, 0.4);
      --accent-gold: #f59e0b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Outfit', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    /* Tactile Micro-Interactions & Active States */
    :where(button, .nav-btn, .filter-pill, .btn-read, .btn-story, .share-icon-btn, .lang-opt):active {{
      transform: scale(0.97);
    }}

    .discover-card:active {{
      transform: scale(0.985);
    }}

    :where(a, button, input, [tabindex]):focus-visible {{
      outline: 2px solid var(--accent-gold);
      outline-offset: 2px;
    }}

    /* Top Navbar: Mobile Streamlined (360px-420px) */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 12px 20px;
      transition: background 0.2s ease;
    }}

    @media (max-width: 480px) {{
      .navbar {{
        padding: 10px 12px;
      }}
    }}

    .nav-container {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: nowrap;
      min-width: 0;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
      flex-shrink: 0;
    }}

    .brand-logo {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
      flex-shrink: 0;
    }}

    .brand-title {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.1;
      white-space: nowrap;
    }}

    .brand-tag {{
      font-size: 10px;
      color: var(--accent-gold);
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    @media (max-width: 420px) {{
      .brand-wrap {{
        gap: 8px;
      }}
      .brand-logo {{
        width: 32px;
        height: 32px;
      }}
      .brand-title {{
        font-size: 16px;
      }}
      .brand-tag {{
        display: none;
      }}
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      flex-wrap: nowrap;
    }}

    .lang-switch-pill {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      padding: 2px;
      gap: 2px;
      flex-shrink: 0;
    }}

    .lang-opt {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 999px;
      color: var(--text-muted);
      text-decoration: none;
      transition: all 0.15s ease;
      white-space: nowrap;
      user-select: none;
      -webkit-user-select: none;
    }}

    .lang-opt:hover {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.1);
    }}

    .lang-opt.active {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(225, 29, 72, 0.5);
    }}

    .lang-opt:active {{
      transform: scale(0.95);
    }}

    @media (max-width: 380px) {{
      .lang-opt {{
        padding: 3px 6px;
        font-size: 10px;
      }}
    }}

    .nav-links-legal {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .nav-link-item {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 8px;
      transition: color 0.2s ease;
    }}

    .nav-link-item:hover {{
      color: #fff;
    }}

    @media (max-width: 768px) {{
      .nav-links-legal {{
        display: none !important;
      }}
    }}

    .nav-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      transition: all 0.2s ease;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .nav-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .nav-btn-active {{
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }}

    @media (max-width: 380px) {{
      .nav-btn .btn-text {{
        display: none;
      }}
      .nav-btn {{
        padding: 6px 10px;
      }}
    }}

    /* Discover Hero Banner */
    .discover-header {{
      max-width: 1280px;
      margin: 28px auto 16px;
      padding: 0 24px;
      width: 100%;
    }}

    @media (max-width: 480px) {{
      .discover-header {{
        margin: 18px auto 12px;
        padding: 0 16px;
      }}
    }}

    .discover-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(135deg, rgba(225, 29, 72, 0.15), rgba(245, 158, 11, 0.15));
      border: 1px solid rgba(245, 158, 11, 0.3);
      color: var(--accent-gold);
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }}

    .discover-title {{
      font-size: clamp(24px, 4vw, 36px);
      font-weight: 900;
      letter-spacing: -0.8px;
      line-height: 1.2;
      margin-bottom: 8px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .discover-subtitle {{
      font-size: clamp(13.5px, 2vw, 15px);
      color: var(--text-muted);
      max-width: 680px;
    }}

    /* Filter & Search Controls */
    .feed-controls {{
      max-width: 1280px;
      margin: 0 auto 28px;
      padding: 0 24px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    @media (max-width: 480px) {{
      .feed-controls {{
        padding: 0 16px;
        margin-bottom: 20px;
      }}
    }}

    .search-box-wrap {{
      width: 100%;
      display: flex;
      justify-content: flex-end;
    }}

    .search-box {{
      width: 100%;
      max-width: 380px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 999px;
      padding: 10px 18px;
      color: #fff;
      font-size: 13.5px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}

    .search-box:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.2);
    }}

    /* Horizontal Scroll-Snap Filter Rail */
    .filter-rail-wrapper {{
      position: relative;
      width: 100%;
      overflow: hidden;
    }}

    .filter-pills {{
      display: flex !important;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      padding: 4px 2px 8px;
      width: 100%;
      box-sizing: border-box;
    }}

    .filter-pills::-webkit-scrollbar {{
      display: none;
    }}

    .filter-pill {{
      flex: 0 0 auto;
      scroll-snap-align: start;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 700;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: transform 0.15s ease, background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      user-select: none;
      -webkit-user-select: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .filter-pill:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .filter-pill.active {{
      background: linear-gradient(135deg, var(--primary) 0%, #be123c 100%);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 2px 10px var(--primary-glow);
    }}

    .filter-pill:active {{
      transform: scale(0.97);
    }}

    .filter-pill:focus-visible {{
      outline: 2px solid var(--accent-gold);
      outline-offset: 2px;
    }}

    /* Responsive Grid Breakpoints:
       Mobile (<768px): 1 column
       Tablet (768px-1279px): 2 columns
       Desktop (1280px+): 3 columns
    */
    .feed-container {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px 64px;
      width: 100%;
      display: grid;
      grid-template-columns: 1fr;
      gap: 24px;
    }}

    @media (max-width: 767px) {{
      .feed-container {{
        max-width: 680px;
        padding: 0 16px 48px;
        grid-template-columns: 1fr;
        gap: 20px;
      }}
    }}

    @media (min-width: 768px) and (max-width: 1279px) {{
      .feed-container {{
        grid-template-columns: repeat(2, 1fr);
        max-width: 980px;
        gap: 24px;
      }}
    }}

    @media (min-width: 1280px) {{
      .feed-container {{
        grid-template-columns: repeat(3, 1fr);
        max-width: 1280px;
        gap: 28px;
      }}
    }}

    .discover-card {{
      background: var(--surface-card);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
      display: flex;
      flex-direction: column;
      height: 100%;
    }}

    .discover-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(225, 29, 72, 0.4);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45), 0 0 20px rgba(225, 29, 72, 0.15);
    }}

    .discover-card.spotlight-card {{
      border: 1px solid rgba(225, 29, 72, 0.45);
      box-shadow: 0 10px 32px rgba(225, 29, 72, 0.2), 0 0 20px rgba(225, 29, 72, 0.12);
    }}

    .spotlight-tag {{
      position: absolute;
      top: 12px;
      left: 12px;
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 4px 10px;
      border-radius: 999px;
      background: linear-gradient(135deg, #e11d48, #f59e0b);
      color: #fff;
      box-shadow: 0 2px 10px rgba(225, 29, 72, 0.5);
      z-index: 2;
    }}

    .discover-card.spotlight-card .card-cat-badge {{
      left: auto;
      right: 12px;
    }}

    .card-media-link {{
      display: block;
      position: relative;
    }}

    .card-img-wrap {{
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      background: var(--surface);
      overflow: hidden;
    }}

    .card-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .discover-card:hover .card-img {{
      transform: scale(1.04);
    }}

    .card-cat-badge {{
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(9, 11, 16, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fda4af;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .card-rating-badge {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: rgba(9, 11, 16, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(245, 158, 11, 0.3);
      color: var(--accent-gold);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
    }}

    .card-content {{
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .publisher-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: var(--text-dim);
    }}

    .pub-logo {{
      width: 18px;
      height: 18px;
      border-radius: 4px;
    }}

    .pub-name {{
      font-weight: 700;
      color: var(--text-muted);
    }}

    .dot-separator {{
      color: var(--text-dim);
    }}

    .share-icon-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: var(--text-dim);
      cursor: pointer;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: all 0.2s ease;
      padding: 0;
    }}

    .share-icon-btn:hover {{
      color: #fff;
      background: var(--primary);
      border-color: var(--primary);
      transform: scale(1.1);
    }}

    .share-icon-btn:active {{
      transform: scale(0.92);
    }}

    .card-title {{
      font-size: clamp(17px, 2.5vw, 20px);
      font-weight: 800;
      line-height: 1.35;
      letter-spacing: -0.4px;
      margin-bottom: 10px;
    }}

    .card-title a:hover {{
      color: #fda4af;
    }}

    .card-snippet {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 18px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-footer-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-top: 14px;
      border-top: 1px solid var(--surface-border);
      margin-top: auto;
    }}

    .btn-read {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      background: var(--primary);
      padding: 8px 16px;
      border-radius: 999px;
      box-shadow: 0 2px 10px var(--primary-glow);
      transition: background 0.2s, transform 0.15s ease;
    }}

    .btn-read:hover {{
      background: var(--primary-hover);
    }}

    .read-duration {{
      font-size: 11px;
      opacity: 0.85;
      font-weight: 500;
    }}

    .btn-story {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent-gold);
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 7px 14px;
      border-radius: 999px;
      transition: all 0.2s;
    }}

    .btn-story:hover {{
      background: rgba(245, 158, 11, 0.25);
    }}

    .no-results {{
      text-align: center;
      padding: 48px 16px;
      color: var(--text-dim);
      font-size: 15px;
      display: none;
      grid-column: 1 / -1;
    }}

    /* Toast Notification */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      background: rgba(16, 20, 31, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(225, 29, 72, 0.45);
      border-radius: 14px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65), 0 0 24px rgba(225, 29, 72, 0.25);
      padding: 14px 18px;
      max-width: 360px;
      width: calc(100vw - 32px);
      box-sizing: border-box;
      transform: translateY(120%) scale(0.95);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
    }}

    .toast-notification.show {{
      transform: translateY(0) scale(1);
      opacity: 1;
      pointer-events: auto;
    }}

    @media (max-width: 480px) {{
      .toast-notification {{
        right: 16px;
        left: 16px;
        bottom: 16px;
        width: auto;
      }}
    }}

    .toast-content {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .toast-icon {{
      font-size: 24px;
      flex-shrink: 0;
      animation: popCelebrate 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes popCelebrate {{
      0% {{ transform: scale(0.5) rotate(-20deg); }}
      50% {{ transform: scale(1.3) rotate(15deg); }}
      100% {{ transform: scale(1) rotate(0deg); }}
    }}

    .toast-text {{
      flex: 1;
      min-width: 0;
    }}

    .toast-title {{
      font-size: 14px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
    }}

    .toast-desc {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.3;
      margin-top: 2px;
    }}

    .toast-close {{
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 20px;
      cursor: pointer;
      padding: 0 4px;
      line-height: 1;
      border-radius: 4px;
      transition: color 0.15s;
      flex-shrink: 0;
    }}

    .toast-close:hover {{
      color: #fff;
    }}

    .toast-progress {{
      position: absolute;
      bottom: 0;
      left: 14px;
      right: 14px;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), var(--accent-gold));
      border-radius: 999px;
      transform-origin: left;
    }}

    .toast-notification.show .toast-progress {{
      animation: toastTimer 3.5s linear forwards;
    }}

    @keyframes toastTimer {{
      from {{ transform: scaleX(1); }}
      to {{ transform: scaleX(0); }}
    }}

    /* Sparkle Fly Animation */
    .sparkle-item {{
      position: fixed;
      pointer-events: none;
      z-index: 10000;
      font-size: 18px;
      animation: sparkleFly 0.75s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      user-select: none;
    }}

    @keyframes sparkleFly {{
      0% {{
        transform: translate(0, 0) scale(0.6);
        opacity: 1;
      }}
      100% {{
        transform: translate(var(--dx), var(--dy)) scale(1.3);
        opacity: 0;
      }}
    }}

    /* Footer */
    .footer {{
      background: #06070a;
      border-top: 1px solid var(--surface-border);
      padding: 36px 20px;
      margin-top: auto;
      font-size: 13px;
      color: var(--text-dim);
    }}

    .footer-container {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      text-align: center;
    }}

    .footer-links {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 16px;
    }}

    .footer-links a:hover {{
      color: var(--text);
    }}
  </style>
</head>
<body>

  <!-- Top Navbar: Streamlined Mobile Header (360px-420px) -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="{nav_home}" class="brand-wrap" aria-label="{SITE_NAME} Home">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo" width="36" height="36">
        <div>
          <div class="brand-title">{SITE_NAME}</div>
          <div class="brand-tag">GOOGLE DISCOVER FEED</div>
        </div>
      </a>
      <div class="nav-actions">
        <div class="lang-switch-pill" role="group" aria-label="Language Switcher">
          <a href="{en_target}" class="lang-opt {'active' if lang == 'en' else ''}" data-lang="en" aria-label="Switch to English">🇺🇸 EN</a>
          <a href="{hi_target}" class="lang-opt {'active' if lang == 'hi' else ''}" data-lang="hi" aria-label="Switch to Hindi">🇮🇳 हिं</a>
        </div>
        <div class="nav-links-legal">
          <a href="{nav_about}" class="nav-link-item">About Us</a>
          <a href="{nav_editorial}" class="nav-link-item">Editorial</a>
          <a href="{nav_contact}" class="nav-link-item">Contact</a>
        </div>
        <a href="{nav_home}" class="nav-btn" aria-label="Web Stories">
          <span>⚡</span>
          <span class="btn-text">Web Stories</span>
        </a>
        <a href="{nav_discover}" class="nav-btn nav-btn-active" aria-label="Discover Feed">
          <span>📰</span>
          <span class="btn-text">Discover Feed</span>
        </a>
      </div>
    </div>
  </nav>

  <!-- Feed Header -->
  <header class="discover-header">
    <div class="discover-pill">⚡ Chrome Discover Portal</div>
    <h1 class="discover-title">Entertainment &amp; Cinema Feed</h1>
    <p class="discover-subtitle">Discover-optimized deep dives, hidden movie easter eggs, weekly streaming charts, and viral entertainment stories.</p>
  </header>

  <!-- Filter & Search Controls -->
  <div class="feed-controls">
    <div class="search-box-wrap">
      <input type="text" id="searchInput" class="search-box" placeholder="🔍 Search Discover articles, titles, easter eggs..." aria-label="Search articles">
    </div>
    
    <div class="filter-rail-wrapper">
      <div class="filter-pills" id="filterPills" role="tablist" aria-label="Category Filters" tabindex="0">
        <button class="filter-pill active" data-filter="all" role="tab" aria-selected="true">🔥 All ({total_articles})</button>
        <button class="filter-pill" data-filter="netflix_hits" role="tab" aria-selected="false">🔴 Netflix ({netflix_count})</button>
        <button class="filter-pill" data-filter="streaming_charts" role="tab" aria-selected="false">🍿 Streaming Charts</button>
        <button class="filter-pill" data-filter="theories_easter_eggs" role="tab" aria-selected="false">🦸 Marvel &amp; DC Theories</button>
        <button class="filter-pill" data-filter="where_are_they_now" role="tab" aria-selected="false">✨ Where Are They Now?</button>
        <button class="filter-pill" data-filter="series" role="tab" aria-selected="false">📺 TV Series</button>
        <button class="filter-pill" data-filter="cult_classic" role="tab" aria-selected="false">🎬 Cult Classics</button>
        <button class="filter-pill" data-filter="steamy_thrillers" role="tab" aria-selected="false">🔥 Bold Thrillers</button>
        <button class="filter-pill" data-filter="upcoming" role="tab" aria-selected="false">⚡ Upcoming</button>
      </div>
    </div>
  </div>

  <!-- Cards Feed (Chrome Discover Style: Responsive 1 / 2 / 3 Column Grid) -->
  <main class="feed-container" id="feedContainer">
    {cards_html}
    <div id="noResults" class="no-results">
      <p>No articles found matching your filter or search query.</p>
    </div>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-links" role="navigation" aria-label="Footer Navigation">
        <a href="{nav_home}">Home</a>
        <a href="{nav_discover}">Discover Feed</a>
        <a href="{nav_about}">About Us</a>
        <a href="{nav_editorial}">Editorial Policy</a>
        <a href="{nav_privacy}">Privacy Policy</a>
        <a href="{nav_terms}">Terms of Service</a>
        <a href="{nav_contact}">Contact Us</a>
        <a href="/sitemap.xml">XML Sitemap</a>
      </div>
      <p>© {datetime.now(timezone.utc).year} {PUBLISHER_NAME}. Optimized for Google Chrome Discover &amp; Google Search.</p>
    </div>
  </footer>

  <!-- Toast Notification & Confetti Sparks -->
  <div id="toastNotification" class="toast-notification" role="region" aria-label="Notifications" aria-live="polite">
    <div class="toast-content">
      <span class="toast-icon" id="toastIcon">🎉</span>
      <div class="toast-text">
        <div class="toast-title" id="toastTitle">Article Link Copied!</div>
        <div class="toast-desc" id="toastDesc">Share this breakdown with your movie circle.</div>
      </div>
      <button class="toast-close" id="toastClose" aria-label="Dismiss notification">&times;</button>
    </div>
    <div class="toast-progress"></div>
  </div>

  <script>
    // Toast & Celebration Engine
    const toastNotification = document.getElementById('toastNotification');
    const toastTitle = document.getElementById('toastTitle');
    const toastDesc = document.getElementById('toastDesc');
    const toastClose = document.getElementById('toastClose');
    let toastTimer = null;

    function showToast(title, desc, icon = '🎉') {{
      if (!toastNotification) return;
      if (toastTitle) toastTitle.textContent = title;
      if (toastDesc) toastDesc.textContent = desc;
      const iconEl = document.getElementById('toastIcon');
      if (iconEl) iconEl.textContent = icon;
      toastNotification.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{
        hideToast();
      }}, 3500);
    }}

    function hideToast() {{
      if (toastNotification) {{
        toastNotification.classList.remove('show');
      }}
    }}

    if (toastClose) {{
      toastClose.addEventListener('click', hideToast);
    }}

    function celebrateSparkles(x, y) {{
      const emojis = ['✨', '🔥', '🍿', '⚡', '🎉', '🎬'];
      const count = 12;
      for (let i = 0; i < count; i++) {{
        const spark = document.createElement('span');
        spark.className = 'sparkle-item';
        spark.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        spark.style.left = (x || window.innerWidth / 2) + 'px';
        spark.style.top = (y || window.innerHeight / 2) + 'px';
        
        const angle = (Math.PI * 2 * i) / count;
        const velocity = 50 + Math.random() * 60;
        const destX = Math.cos(angle) * velocity;
        const destY = Math.sin(angle) * velocity - 20;
        
        spark.style.setProperty('--dx', `${{destX}}px`);
        spark.style.setProperty('--dy', `${{destY}}px`);
        
        document.body.appendChild(spark);
        setTimeout(() => spark.remove(), 750);
      }}
    }}

    function shareArticle(url, title, e) {{
      const fullUrl = window.location.origin + url;
      const clientX = e ? e.clientX : window.innerWidth / 2;
      const clientY = e ? e.clientY : window.innerHeight / 2;
      
      if (navigator.share && window.innerWidth <= 768) {{
        navigator.share({{
          title: title,
          url: fullUrl
        }}).then(() => {{
          celebrateSparkles(clientX, clientY);
          showToast('Shared Successfully!', 'Thanks for spreading the cinema news!');
        }}).catch(() => {{
          copyToClipboard(fullUrl, clientX, clientY);
        }});
      }} else {{
        copyToClipboard(fullUrl, clientX, clientY);
      }}
    }}

    function copyToClipboard(text, x, y) {{
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => {{
          celebrateSparkles(x, y);
          showToast('Article Link Copied!', 'Share on WhatsApp, Twitter, or Pinterest!');
        }}).catch(() => {{
          showToast('Link Ready', text);
        }});
      }} else {{
        showToast('Link Ready', text);
      }}
    }}

    // Filter & Search Logic
    const searchInput = document.getElementById('searchInput');
    const filterPills = document.querySelectorAll('.filter-pill');
    const cards = document.querySelectorAll('.discover-card');
    const noResults = document.getElementById('noResults');

    let currentFilter = 'all';
    let searchQuery = '';

    function applyFilters() {{
      let visibleCount = 0;
      cards.forEach(card => {{
        const cat = card.getAttribute('data-category');
        const title = card.getAttribute('data-title') || '';
        const movie = card.getAttribute('data-movie') || '';

        const matchesCat = (currentFilter === 'all') || (cat === currentFilter);
        const matchesQuery = (!searchQuery) || title.includes(searchQuery) || movie.includes(searchQuery);

        if (matchesCat && matchesQuery) {{
          card.style.display = 'flex';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      if (noResults) {{
        noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      }}
    }}

    filterPills.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterPills.forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        btn.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
        currentFilter = btn.getAttribute('data-filter');
        applyFilters();
      }});
    }});

    if (searchInput) {{
      searchInput.addEventListener('input', (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        applyFilters();
      }});
    }}

    // URL parameter support (?category=streaming_charts)
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('category');
    if (catParam) {{
      const targetPill = document.querySelector(`.filter-pill[data-filter="${{catParam}}"]`);
      if (targetPill) {{
        targetPill.click();
      }}
    }}

    // Manual Language Switcher Persistence
    document.querySelectorAll('.lang-opt').forEach(opt => {{
      opt.addEventListener('click', () => {{
        const selectedLang = opt.getAttribute('data-lang');
        try {{
          localStorage.setItem('cinestories_lang', selectedLang);
          localStorage.setItem('cinestories_lang_manual', 'true');
          document.cookie = `cinestories_lang=${{selectedLang}}; Path=/; Max-Age=31536000; SameSite=Lax`;
        }} catch (err) {{}}
      }});
    }});
  </script>
</body>
</html>
"""

def generate_discover_feed(
    articles: List[Dict[str, Any]],
    domain: str = DOMAIN_NAME,
    output_dir: Path = DISCOVER_DIR,
    lang: str = "en"
) -> str:
    """
    Renders and writes dist/discover/index.html (or dist/hi/discover/index.html).
    """
    target_dir = output_dir if lang == "en" else output_dir.parent / "hi" / "discover"
    target_dir.mkdir(parents=True, exist_ok=True)
    feed_html = build_discover_feed_html(articles, domain=domain, lang=lang)
    output_path = target_dir / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(feed_html)
    print(f"[Discover] Successfully created Chrome Discover feed: {output_path} ({len(articles)} articles, lang={lang})")
    return feed_html
