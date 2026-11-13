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
    TMDB_IMAGE_POSTER,
    TMDB_IMAGE_BACKDROP,
    get_ga_script,
    get_adsense_script
)

# Canonical 10 Breakout Viral Spotlight Slugs pinned in the Hero Carousel
VIRAL_SPOTLIGHT_SLUGS: List[str] = [
    "panchayat-season-3",
    "mirzapur-season-3",
    "stree-2",
    "kalki-2898-ad",
    "sector-36",
    "do-patti",
    "devara-part-1",
    "pushpa-2-the-rule",
    "squid-game-season-2",
    "singham-again"
]

def build_homepage_html(stories: List[Dict[str, Any]], domain: str = DOMAIN_NAME, lang: str = "en") -> str:
    """
    Renders the modern, dark cinema-themed landing page.
    """
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    total_stories = len(stories)
    streaming_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "streaming_charts")
    netflix_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "netflix_hits")
    theories_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "theories_easter_eggs")
    sitcoms_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "where_are_they_now")
    series_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "series")
    trending_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "trending")
    cult_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "cult_classic")
    upcoming_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "upcoming")
    steamy_count = sum(1 for s in stories if s.get("movie", {}).get("category") == "steamy_thrillers")

    # Localization navigation paths
    nav_home = "/hi/" if lang == "hi" else "/"
    nav_discover = "/hi/discover/" if lang == "hi" else "/discover/"
    nav_about = "/hi/about/" if lang == "hi" else "/about/"
    nav_editorial = "/hi/editorial/" if lang == "hi" else "/editorial/"
    nav_contact = "/hi/contact/" if lang == "hi" else "/contact/"
    nav_privacy = "/hi/privacy/" if lang == "hi" else "/privacy/"
    nav_terms = "/hi/terms/" if lang == "hi" else "/terms/"
    nav_home_label = "होम" if lang == "hi" else "Home"
    nav_discover_label = "डिस्कवर" if lang == "hi" else "Discover Feed"
    nav_about_label = "हमारे बारे में" if lang == "hi" else "About Us"
    nav_editorial_label = "संपादकीय" if lang == "hi" else "Editorial"
    nav_contact_label = "संपर्क" if lang == "hi" else "Contact"
    nav_privacy_label = "गोपनीयता नीति" if lang == "hi" else "Privacy Policy"
    nav_terms_label = "नियम व शर्तें" if lang == "hi" else "Terms of Service"
    brand_subtitle = "गूगल एएमपी वेब स्टोरीज़" if lang == "hi" else "AMP Web Stories"
    en_target = "/"
    hi_target = "/hi/"
    canonical_url = f"{domain}/hi/" if lang == "hi" else f"{domain}/"

    # Pin breakout viral stories for the Hero Carousel using VIRAL_SPOTLIGHT_SLUGS
    story_map: Dict[str, Dict[str, Any]] = {}
    for s in stories:
        m = s.get("movie", {}) if isinstance(s.get("movie"), dict) else {}
        s_slug = m.get("slug") or s.get("slug")
        if s_slug and s_slug not in story_map:
            story_map[s_slug] = s

    # 1. Pinned breakout stories in canonical order matching VIRAL_SPOTLIGHT_SLUGS
    pinned_stories: List[Dict[str, Any]] = [
        story_map[slug] for slug in VIRAL_SPOTLIGHT_SLUGS if slug in story_map
    ]

    # 2. Backfill with remaining stories if fewer than 10 breakout stories are present
    pinned_slug_set = {
        (s.get("movie", {}).get("slug") or s.get("slug"))
        for s in pinned_stories
    }
    remaining_stories = [
        s for s in stories
        if (s.get("movie", {}).get("slug") or s.get("slug")) not in pinned_slug_set
    ]
    featured_stories = (pinned_stories + remaining_stories)[:10]
    ordered_stories = pinned_stories + remaining_stories

    # Prepare cards data
    cards_data = []
    for s in ordered_stories:
        m = s.get("movie", {})
        slug = m.get("slug", "story")
        poster = m.get("poster_path")
        poster_url = f"{TMDB_IMAGE_POSTER}{poster}" if poster else f"{domain}/assets/logo.png"
        backdrop = m.get("backdrop_path")
        backdrop_url = f"{TMDB_IMAGE_POSTER}{backdrop}" if backdrop else poster_url
        title = s.get("title") or m.get("hook_title") or m.get("title", "")
        teaser = m.get("catchy_teaser") or s.get("seo_description", "")
        card_story_url = f"/hi/stories/{slug}/" if lang == "hi" else f"/stories/{slug}/"
        
        cards_data.append({
            "title": title,
            "movie_title": m.get("title", ""),
            "slug": slug,
            "url": card_story_url,
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

    # Breakout Viral Hero Carousel generation (pinned 10 breakout viral stories)
    carousel_slides_parts = []
    carousel_dots_parts = []

    for idx, s in enumerate(featured_stories):
        active_class = "active" if idx == 0 else ""
        m = s.get("movie", {})
        slug = m.get("slug", "")
        m_title = html.escape(m.get("title", ""))
        headline = html.escape(s.get("title") or m.get("hook_title") or m.get("title", ""))
        teaser = html.escape(m.get("catchy_teaser") or s.get("seo_description", ""))
        b_path = m.get("backdrop_path")
        b_url = f"{TMDB_IMAGE_BACKDROP}{b_path}" if b_path and b_path.startswith("/") else (b_path or f"{domain}/assets/logo.png")
        cat = m.get("category", "trending")
        
        if "netflix" in cat or any(k in slug for k in ["squid", "sector", "patti"]):
            platform = "NETFLIX"
        elif any(k in slug for k in ["panchayat", "mirzapur", "singham"]):
            platform = "PRIME VIDEO"
        elif any(k in slug for k in ["stree", "pushpa", "devara", "kalki"]):
            platform = "JIOCINEMA / THEATERS"
        else:
            platform = cat.replace("_", " ").upper()

        primary_story_href = f"/hi/stories/{slug}/" if lang == "hi" else f"/stories/{slug}/"
        secondary_article_href = f"/hi/articles/{slug}/" if lang == "hi" else f"/articles/{slug}/"

        slide_html = f"""
        <div class="carousel-slide {active_class}" data-slide-index="{idx}">
          <div class="slide-media-wrap">
            <img src="{b_url}" alt="{m_title}" class="slide-bg" loading="{'eager' if idx == 0 else 'lazy'}" width="1280" height="720">
            <div class="slide-scrim"></div>
          </div>
          <div class="slide-content">
            <div class="slide-badges">
              <span class="viral-glow-badge">{'🔥 वायरल स्टोरी' if lang == 'hi' else '🔥 BREAKOUT VIRAL HOOK'}</span>
              <span class="platform-badge">{platform}</span>
              <span class="platform-badge">★ {m.get('vote_average', 8.5)}</span>
            </div>
            <h3 class="slide-headline">{headline}</h3>
            <p class="slide-teaser">{teaser}</p>
            <div class="slide-actions">
              <a href="{primary_story_href}" class="btn-carousel-primary card-link" aria-label="{'वेब स्टोरी देखें' if lang == 'hi' else f'Watch Web Story for {m_title}'}">
                <span>{'⚡ वेब स्टोरी देखें' if lang == 'hi' else '⚡ Watch Web Story'}</span>
              </a>
              <a href="{secondary_article_href}" class="btn-carousel-secondary" aria-label="{'पूरा आर्टिकल पढ़ें' if lang == 'hi' else f'Read full article for {m_title}'}">
                <span>{'📖 पूरा आर्टिकल पढ़ें' if lang == 'hi' else '📖 Read Climax Breakdown'}</span>
              </a>
            </div>
          </div>
        </div>"""
        carousel_slides_parts.append(slide_html)
        carousel_dots_parts.append(f'<button class="carousel-dot {active_class}" data-index="{idx}" aria-label="Slide {idx + 1}"></button>')

    carousel_slides_html = "\n".join(carousel_slides_parts)
    carousel_indicators_html = "\n".join(carousel_dots_parts)

    hero_carousel_html = f"""
    <!-- Breakout Viral Hero Carousel -->
    <div class="hero-carousel-container" id="heroCarousel" aria-roledescription="carousel" aria-label="Trending Breakout Stories">
      <div class="carousel-track" id="carouselTrack">
        {carousel_slides_html}
      </div>

      <!-- Navigation Arrows -->
      <button class="carousel-arrow prev-arrow" id="carouselPrev" aria-label="Previous story">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <button class="carousel-arrow next-arrow" id="carouselNext" aria-label="Next story">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
      </button>

      <!-- Carousel Pagination Indicators -->
      <div class="carousel-indicators" id="carouselIndicators">
        {carousel_indicators_html}
      </div>
    </div>
    """

    cards_json = json.dumps(cards_data)

    cards_html_list = []
    for c in cards_data:
        if c["category"] == "streaming_charts":
            category_label = "Weekly Top 10"
        elif c["category"] == "netflix_hits":
            category_label = "Netflix Hits"
        elif c["category"] == "theories_easter_eggs":
            category_label = "Marvel & DC Theories"
        elif c["category"] == "where_are_they_now":
            category_label = "Where Are They Now?"
        elif c["category"] == "series":
            category_label = "TV Series"
        elif c["category"] == "cult_classic":
            category_label = "Cult Classic"
        elif c["category"] == "steamy_thrillers":
            category_label = "Bold & Steamy"
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
                <div class="card-top-actions">
                  <span class="rating-badge">★ {c['rating']}</span>
                  <button class="card-share-btn" onclick="event.preventDefault(); event.stopPropagation(); shareStory('{c['url']}', '{html.escape(c['title'])}', event)" aria-label="Share story" title="Quick Share">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                  </button>
                </div>
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

    # Schema.org WebSite & Organization structured data
    schema_website_org = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{domain}/#website",
                "url": f"{domain}/",
                "name": SITE_NAME,
                "description": "Visual Google AMP Web Stories & In-Depth Entertainment Journalism",
                "publisher": {
                    "@id": f"{domain}/#organization"
                },
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": f"{domain}/discover/?q={{search_term_string}}"
                    },
                    "query-input": "required name=search_term_string"
                },
                "inLanguage": "hi-IN" if lang == "hi" else "en-US"
            },
            {
                "@type": "Organization",
                "@id": f"{domain}/#organization",
                "name": "CineStories",
                "legalName": "CineStories Digital Media Network",
                "url": f"{domain}/",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{domain}/assets/logo.png",
                    "width": 512,
                    "height": 512
                },
                "publishingPrinciples": f"{domain}/editorial/",
                "sameAs": [
                    "https://twitter.com/CineStories",
                    "https://t.me/CineStories"
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "editorial inquiries",
                    "email": "editorial@cinestories.online",
                    "availableLanguage": ["English", "Hindi"]
                }
            }
        ]
    }
    schema_json = json.dumps(schema_website_org, indent=2)

    html_content = f"""<!doctype html>
<html lang="{ 'hi' if lang == 'hi' else 'en' }">
<head>
{get_ga_script()}
{get_adsense_script()}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{SITE_NAME} | {SITE_TAGLINE}</title>
  <meta name="description" content="Discover automated, 100% AMP-compliant visual Web Stories for upcoming, trending, and now-playing movies. Powered by TMDB and Gemini AI.">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="en" href="{domain}/">
  <link rel="alternate" hreflang="hi" href="{domain}/hi/">
  <link rel="alternate" hreflang="x-default" href="{domain}/">
  <link rel="icon" type="image/svg+xml" href="{domain}/assets/favicon.svg">
  <meta name="google-site-verification" content="8Brds5ztSCZ-SIMPzuc_bVipCi_wCcAMmhfNX7GhNDw">

  <!-- Open Graph / Social -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{SITE_NAME} | {SITE_TAGLINE}">
  <meta property="og:description" content="Experience movie stories in Google AMP Web Story format. Bite-sized, cinematic visual entertainment guides.">
  <meta property="og:image" content="{domain}/assets/logo.png">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --bg: #090b10;
      --surface: #10141f;
      --surface-border: rgba(255, 255, 255, 0.08);
      --primary: #e11d48;
      --primary-hover: #f43f5e;
      --primary-glow: rgba(225, 29, 72, 0.4);
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
      font-family: 'Outfit', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Tactile Micro-Interactions & Focus States */
    :where(button, .btn, .filter-chip, .filter-btn, .lang-opt, .btn-carousel-primary, .btn-carousel-secondary, .card-share-btn):active {{
      transform: scale(0.97);
    }}

    .story-card:active {{
      transform: scale(0.985);
    }}

    :where(a, button, input, [tabindex]):focus-visible {{
      outline: 2px solid var(--accent-gold);
      outline-offset: 2px;
    }}

    /* Top Navigation Bar: Mobile Optimized (360px-420px) */
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
      text-decoration: none;
      color: var(--text);
      min-width: 0;
      flex-shrink: 0;
    }}

    .brand-logo {{
      width: 38px;
      height: 38px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.35);
      flex-shrink: 0;
    }}

    .brand-text {{
      display: flex;
      flex-direction: column;
      min-width: 0;
    }}

    .brand-text h1 {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.1;
      white-space: nowrap;
    }}

    .brand-text p {{
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
        border-radius: 8px;
      }}
      .brand-text h1 {{
        font-size: 16px;
      }}
      .brand-text p {{
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

    .btn-discover-nav {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 12.5px;
      font-weight: 700;
      border-radius: 999px;
      text-decoration: none;
      transition: var(--transition);
      cursor: pointer;
      border: 1px solid rgba(245, 158, 11, 0.45);
      color: #fbbf24;
      background: rgba(245, 158, 11, 0.1);
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .btn-discover-nav:hover {{
      background: rgba(245, 158, 11, 0.2);
      color: #fff;
    }}

    @media (max-width: 380px) {{
      .btn-discover-nav .btn-text {{
        display: none;
      }}
      .btn-discover-nav {{
        padding: 6px 10px;
      }}
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

    @media (max-width: 640px) {{
      .amp-pill, .btn-sitemap {{
        display: none !important;
      }}
    }}

    /* Hero Section */
    .hero {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 40px 24px 28px;
      width: 100%;
    }}

    @media (max-width: 480px) {{
      .hero {{
        padding: 24px 16px 20px;
      }}
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
      font-size: clamp(28px, 5vw, 54px);
      font-weight: 900;
      letter-spacing: -1.5px;
      line-height: 1.1;
      margin-bottom: 14px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
      font-size: clamp(14px, 2vw, 17px);
      color: var(--text-muted);
      max-width: 680px;
      line-height: 1.6;
      margin-bottom: 24px;
    }}

    /* Controls Area: Search & Horizontal Scroll-Snap Filter Rail */
    .controls-area {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 32px;
    }}

    .search-wrap {{
      display: flex;
      justify-content: flex-end;
      width: 100%;
    }}

    .search-box {{
      position: relative;
      width: 100%;
      max-width: 380px;
    }}

    .search-box input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: #fff;
      padding: 10px 16px 10px 40px;
      font-size: 13.5px;
      border-radius: 999px;
      outline: none;
      font-family: inherit;
      transition: var(--transition);
    }}

    .search-box input:focus {{
      border-color: var(--primary);
      background: rgba(255, 255, 255, 0.1);
      box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.2);
    }}

    .search-box svg {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }}

    /* Horizontal Scroll-Snap Filter Rail */
    .filter-rail-wrapper {{
      position: relative;
      width: 100%;
      overflow: hidden;
    }}

    .filter-pills {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
    }}

    .filter-rail {{
      display: flex !important;
      flex-wrap: nowrap !important;
      gap: 8px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      padding: 4px 2px 10px;
      width: 100%;
      box-sizing: border-box;
    }}

    .filter-rail::-webkit-scrollbar {{
      display: none;
    }}

    .filter-chip {{
      flex: 0 0 auto;
      scroll-snap-align: start;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      color: var(--text-muted);
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 700;
      border-radius: 999px;
      cursor: pointer;
      white-space: nowrap;
      font-family: inherit;
      transition: transform 0.15s ease, background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      user-select: none;
      -webkit-user-select: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .filter-chip:hover {{
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .filter-chip.active {{
      background: linear-gradient(135deg, var(--primary) 0%, #be123c 100%);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 4px 14px var(--primary-glow);
    }}

    .filter-chip:active {{
      transform: scale(0.97);
    }}

    .filter-chip:focus-visible {{
      outline: 2px solid var(--accent-gold);
      outline-offset: 2px;
    }}

    .chip-icon {{
      font-size: 13px;
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

    .badge-steamy_thrillers {{
      background: linear-gradient(135deg, #e11d48, #db2777);
      color: #fff;
      box-shadow: 0 2px 10px rgba(225, 29, 72, 0.4);
    }}

    .badge-netflix_hits {{
      background: linear-gradient(135deg, #e50914, #b20710);
      color: #fff;
      font-weight: 700;
      box-shadow: 0 2px 10px rgba(229, 9, 20, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.2);
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
    /* Hero Carousel Styling */
    .hero-carousel-container {{
      position: relative;
      width: 100%;
      border-radius: var(--radius-lg);
      overflow: hidden;
      margin-top: 24px;
      margin-bottom: 32px;
      border: 1px solid rgba(225, 29, 72, 0.35);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(225, 29, 72, 0.2);
      aspect-ratio: 16 / 9;
      max-height: 520px;
      background: var(--surface);
    }}

    .carousel-track {{
      position: relative;
      width: 100%;
      height: 100%;
    }}

    .carousel-slide {{
      position: absolute;
      inset: 0;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.6s;
      display: flex;
      align-items: flex-end;
      padding: clamp(20px, 4vw, 44px);
      box-sizing: border-box;
    }}

    .carousel-slide.active {{
      opacity: 1;
      visibility: visible;
      z-index: 2;
    }}

    .slide-media-wrap {{
      position: absolute;
      inset: 0;
      z-index: 0;
    }}

    .slide-bg {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 25%;
    }}

    .slide-scrim {{
      position: absolute;
      inset: 0;
      background: linear-gradient(
        180deg,
        rgba(9, 11, 16, 0.1) 0%,
        rgba(9, 11, 16, 0.4) 40%,
        rgba(9, 11, 16, 0.88) 75%,
        rgba(9, 11, 16, 0.98) 100%
      );
    }}

    .slide-content {{
      position: relative;
      z-index: 3;
      max-width: 820px;
    }}

    .slide-badges {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .viral-glow-badge {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 5px 12px;
      border-radius: 999px;
      background: linear-gradient(135deg, #e11d48, #f59e0b);
      color: #fff;
      box-shadow: 0 2px 14px rgba(225, 29, 72, 0.5);
    }}

    .platform-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #f8fafc;
    }}

    .slide-headline {{
      font-size: clamp(20px, 3.2vw, 34px);
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -0.6px;
      color: #ffffff;
      margin-bottom: 10px;
      text-shadow: 0 2px 12px rgba(0, 0, 0, 0.8);
    }}

    .slide-teaser {{
      font-size: clamp(13px, 1.8vw, 15px);
      color: #cbd5e1;
      line-height: 1.5;
      margin-bottom: 20px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      max-width: 680px;
    }}

    .slide-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .btn-carousel-primary {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      background: var(--primary);
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      border-radius: 999px;
      text-decoration: none;
      box-shadow: 0 4px 16px var(--primary-glow);
      transition: transform 0.2s, background 0.2s;
    }}

    .btn-carousel-primary:hover {{
      background: var(--primary-hover);
      transform: translateY(-2px);
    }}

    .btn-carousel-secondary {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 20px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #fff;
      font-size: 14px;
      font-weight: 600;
      border-radius: 999px;
      text-decoration: none;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: all 0.2s;
    }}

    .btn-carousel-secondary:hover {{
      background: rgba(255, 255, 255, 0.18);
    }}

    .carousel-arrow {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      z-index: 5;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(9, 11, 16, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: all 0.2s;
    }}

    .carousel-arrow:hover {{
      background: var(--primary);
      border-color: var(--primary);
      transform: translateY(-50%) scale(1.08);
    }}

    .prev-arrow {{ left: 16px; }}
    .next-arrow {{ right: 16px; }}

    .carousel-indicators {{
      position: absolute;
      bottom: 16px;
      right: 24px;
      z-index: 5;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .carousel-dot {{
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.3);
      cursor: pointer;
      transition: all 0.3s ease;
      border: none;
      padding: 0;
    }}

    .carousel-dot.active {{
      width: 26px;
      background: var(--primary);
      box-shadow: 0 0 10px var(--primary-glow);
    }}

    @media (max-width: 640px) {{
      .hero-carousel-container {{
        aspect-ratio: 4 / 5;
        max-height: none;
      }}
      .carousel-arrow {{
        display: none;
      }}
      .slide-content {{
        padding-bottom: 24px;
      }}
      .carousel-indicators {{
        left: 20px;
        right: auto;
        bottom: 14px;
      }}
    }}

    /* Card Top Actions & Quick Share */
    .card-top-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .card-share-btn {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: rgba(9, 11, 16, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
      padding: 0;
    }}

    .card-share-btn:hover {{
      background: var(--primary);
      border-color: var(--primary);
      transform: scale(1.1);
    }}

    .card-share-btn:active {{
      transform: scale(0.92);
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
      max-width: 358px;
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
  </style>
</head>
<body>

  <!-- Navigation Bar: Streamlined Mobile Header (360px-420px) -->
  <header class="navbar">
    <div class="nav-container">
      <a href="{nav_home}" class="brand-wrap" aria-label="CineStories Home">
        <img src="/assets/logo.png" alt="CineStories Logo" class="brand-logo" width="38" height="38">
        <div class="brand-text">
          <h1 class="brand-title">CineStories</h1>
          <p>{brand_subtitle}</p>
        </div>
      </a>

      <div class="nav-actions">
        <nav class="lang-switcher" data-component="lang-switcher" aria-label="Select language">
          <a href="{en_target}" class="lang-opt {'active' if lang == 'en' else ''}" data-lang="en" aria-label="Switch to English" onclick="setLanguagePreference('en')">🇺🇸 EN</a>
          <a href="{hi_target}" class="lang-opt {'active' if lang == 'hi' else ''}" data-lang="hi" aria-label="Switch to Hindi" onclick="setLanguagePreference('hi')">🇮🇳 हिं</a>
        </nav>
        <div class="nav-links-legal">
          <a href="{nav_about}" class="nav-link-item">{nav_about_label}</a>
          <a href="{nav_editorial}" class="nav-link-item">{nav_editorial_label}</a>
          <a href="{nav_contact}" class="nav-link-item">{nav_contact_label}</a>
        </div>
        <a href="{nav_discover}" class="btn-discover-nav" aria-label="Discover Feed">
          <span>📰</span>
          <span class="btn-text">{nav_discover_label}</span>
        </a>
        <span class="amp-pill">⚡ 100% AMP</span>
        <a href="/sitemap.xml" class="btn btn-outline btn-sitemap" target="_blank" rel="noopener">
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

    {hero_carousel_html}

    <!-- Controls Bar: Search & Horizontal Scroll-Snap Filter Rail -->
    <div class="controls-area">
      <div class="search-wrap">
        <div class="search-box">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="searchInput" placeholder="Search stories, titles, actors..." aria-label="Search stories">
        </div>
      </div>

      <div class="filter-rail-wrapper">
        <div class="filter-pills filter-rail" role="tablist" aria-label="Filter stories by category" tabindex="0">
          <button class="filter-btn filter-chip active" data-filter="all" role="tab" aria-selected="true">
            <span class="chip-icon">🔥</span> All ({total_stories})
          </button>
          <button class="filter-btn filter-chip" data-filter="netflix_hits" role="tab" aria-selected="false">
            <span class="chip-icon">🔴</span> Netflix ({netflix_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="streaming_charts" role="tab" aria-selected="false">
            <span class="chip-icon">🍿</span> Weekly Top 10 ({streaming_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="theories_easter_eggs" role="tab" aria-selected="false">
            <span class="chip-icon">🦸</span> Marvel &amp; DC ({theories_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="where_are_they_now" role="tab" aria-selected="false">
            <span class="chip-icon">✨</span> Where Are They Now? ({sitcoms_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="series" role="tab" aria-selected="false">
            <span class="chip-icon">📺</span> TV Series ({series_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="trending" role="tab" aria-selected="false">
            <span class="chip-icon">⚡</span> Trending ({trending_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="cult_classic" role="tab" aria-selected="false">
            <span class="chip-icon">🎬</span> Cult Classics ({cult_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="steamy_thrillers" role="tab" aria-selected="false">
            <span class="chip-icon">🔥</span> Bold Thrillers ({steamy_count})
          </button>
          <button class="filter-btn filter-chip" data-filter="upcoming" role="tab" aria-selected="false">
            <span class="chip-icon">⏳</span> Upcoming ({upcoming_count})
          </button>
        </div>
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
      <nav class="lang-switcher" data-component="lang-switcher" aria-label="Select language">
        <a href="{en_target}" class="lang-opt {'active' if lang == 'en' else ''}" data-lang="en" aria-label="Switch to English" onclick="setLanguagePreference('en')">🇺🇸 EN</a>
        <a href="{hi_target}" class="lang-opt {'active' if lang == 'hi' else ''}" data-lang="hi" aria-label="Switch to Hindi" onclick="setLanguagePreference('hi')">🇮🇳 हिं</a>
      </nav>
      <div class="footer-links" role="navigation" aria-label="Footer Navigation">
        <a href="{nav_home}">{nav_home_label}</a>
        <a href="{nav_discover}">{nav_discover_label}</a>
        <a href="{nav_about}">{nav_about_label}</a>
        <a href="{nav_editorial}">{nav_editorial_label}</a>
        <a href="{nav_privacy}">{nav_privacy_label}</a>
        <a href="{nav_terms}">{nav_terms_label}</a>
        <a href="{nav_contact}">{nav_contact_label}</a>
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

  <!-- Toast Notification & Confetti Sparks -->
  <div id="toastNotification" class="toast-notification" role="region" aria-label="Notifications" aria-live="polite">
    <div class="toast-content">
      <span class="toast-icon" id="toastIcon">🎉</span>
      <div class="toast-text">
        <div class="toast-title" id="toastTitle">Story Link Copied!</div>
        <div class="toast-desc" id="toastDesc">Share with friends to spread the cinematic buzz.</div>
      </div>
      <button class="toast-close" id="toastClose" aria-label="Dismiss notification">&times;</button>
    </div>
    <div class="toast-progress"></div>
  </div>

  <!-- Instant Filtering, Search, Modal & Micro-Interactions Script -->
  <script>
    const filterBtns = document.querySelectorAll('.filter-chip, .filter-btn');
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

      if (emptyState) {{
        emptyState.style.display = (visibleCount === 0) ? 'block' : 'none';
      }}
    }}

    filterBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterBtns.forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        btn.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
        activeFilter = btn.getAttribute('data-filter');
        applyFilters();
      }});
    }});

    if (searchInput) {{
      searchInput.addEventListener('input', (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        applyFilters();
      }});
    }}

    // Story Modal Lightbox Logic
    const storyModal = document.getElementById('storyModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const storyIframe = document.getElementById('storyIframe');

    function openStoryModal(url) {{
      if (!storyIframe || !storyModal) return;
      storyIframe.src = url;
      storyModal.classList.add('active');
      storyModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      history.pushState({{ modalOpen: true }}, '', url);
    }}

    function closeStoryModal() {{
      if (!storyModal || !storyIframe) return;
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

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeStoryModal);
    if (modalBackdrop) modalBackdrop.addEventListener('click', closeStoryModal);

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape' && storyModal && storyModal.classList.contains('active')) {{
        closeStoryModal();
      }}
    }});

    window.addEventListener('popstate', () => {{
      if (storyModal && storyModal.classList.contains('active')) {{
        storyModal.classList.remove('active');
        storyModal.setAttribute('aria-hidden', 'true');
        if (storyIframe) storyIframe.src = '';
        document.body.style.overflow = '';
      }}
    }});

    // Hero Carousel Engine
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const carouselDots = document.querySelectorAll('.carousel-dot');
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');
    let currentSlide = 0;
    let autoSlideTimer = null;

    function goToSlide(index) {{
      if (!carouselSlides.length) return;
      carouselSlides[currentSlide].classList.remove('active');
      if (carouselDots[currentSlide]) carouselDots[currentSlide].classList.remove('active');
      currentSlide = (index + carouselSlides.length) % carouselSlides.length;
      carouselSlides[currentSlide].classList.add('active');
      if (carouselDots[currentSlide]) carouselDots[currentSlide].classList.add('active');
    }}

    function nextCarouselSlide() {{ goToSlide(currentSlide + 1); }}
    function prevCarouselSlide() {{ goToSlide(currentSlide - 1); }}

    if (prevBtn) prevBtn.addEventListener('click', () => {{ prevCarouselSlide(); resetTimer(); }});
    if (nextBtn) nextBtn.addEventListener('click', () => {{ nextCarouselSlide(); resetTimer(); }});

    carouselDots.forEach((dot, idx) => {{
      dot.addEventListener('click', () => {{ goToSlide(idx); resetTimer(); }});
    }});

    function startTimer() {{
      autoSlideTimer = setInterval(nextCarouselSlide, 5000);
    }}
    function resetTimer() {{
      clearInterval(autoSlideTimer);
      startTimer();
    }}
    startTimer();

    // Touch Swipe Support
    let touchStartX = 0;
    const carouselEl = document.getElementById('heroCarousel');
    if (carouselEl) {{
      carouselEl.addEventListener('touchstart', (e) => {{
        touchStartX = e.changedTouches[0].screenX;
        clearInterval(autoSlideTimer);
      }}, {{ passive: true }});

      carouselEl.addEventListener('touchend', (e) => {{
        const touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 50) nextCarouselSlide();
        else if (touchEndX - touchStartX > 50) prevCarouselSlide();
        startTimer();
      }}, {{ passive: true }});

      carouselEl.addEventListener('mouseenter', () => clearInterval(autoSlideTimer));
      carouselEl.addEventListener('mouseleave', () => startTimer());
    }}

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
      toastTimer = window['setTimeout'](() => {{
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
      const emojis = ['✨', '🔥', '🍿', '⚡', '🎉', '⭐'];
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
        spark.addEventListener('animationend', () => spark.remove());
      }}
    }}

    function shareStory(url, title, e) {{
      const fullUrl = window.location.origin + url;
      const clientX = e ? e.clientX : window.innerWidth / 2;
      const clientY = e ? e.clientY : window.innerHeight / 2;
      
      if (navigator.share && window.innerWidth <= 768) {{
        navigator.share({{
          title: title,
          url: fullUrl
        }}).then(() => {{
          celebrateSparkles(clientX, clientY);
          showToast('Shared Successfully!', 'Thanks for spreading the word!');
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
          showToast('Story Link Copied!', 'Share on WhatsApp, Twitter, or Pinterest!');
        }}).catch(() => {{
          showToast('Link Ready', text);
        }});
      }} else {{
        showToast('Link Ready', text);
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
    return html_content

def generate_homepage(stories: List[Dict[str, Any]], domain: str = DOMAIN_NAME, output_dir: Path = DIST_DIR, lang: str = "en") -> str:
    """Build and save dist/index.html (or dist/hi/index.html) and dist/stories.json."""
    html_str = build_homepage_html(stories, domain=domain, lang=lang)
    target_dir = output_dir if lang == "en" else output_dir / "hi"
    target_dir.mkdir(parents=True, exist_ok=True)
    index_file = target_dir / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_str)

    # Save stories.json manifest (prioritizing pinned breakout titles)
    story_map_m: Dict[str, Dict[str, Any]] = {}
    for s in stories:
        m = s.get("movie", {}) if isinstance(s.get("movie"), dict) else {}
        s_slug = m.get("slug") or s.get("slug")
        if s_slug and s_slug not in story_map_m:
            story_map_m[s_slug] = s
    pinned_m = [story_map_m[slug] for slug in VIRAL_SPOTLIGHT_SLUGS if slug in story_map_m]
    pinned_set_m = {(s.get("movie", {}).get("slug") or s.get("slug")) for s in pinned_m}
    ordered_manifest = pinned_m + [s for s in stories if (s.get("movie", {}).get("slug") or s.get("slug")) not in pinned_set_m]

    manifest_data = {
        "site_name": SITE_NAME,
        "domain": domain,
        "lang": lang,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_stories": len(stories),
        "stories": [
            {
                "id": s.get("movie", {}).get("id"),
                "slug": s.get("movie", {}).get("slug"),
                "title": s.get("title"),
                "url": f"{domain}/stories/{s.get('movie', {}).get('slug')}/" if lang == "en" else f"{domain}/hi/stories/{s.get('movie', {}).get('slug')}/",
                "category": s.get("movie", {}).get("category"),
                "release_date": s.get("movie", {}).get("release_date"),
                "rating": s.get("movie", {}).get("vote_average")
            }
            for s in ordered_manifest
        ]
    }
    with open(target_dir / "stories.json", "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    print(f"[Homepage] Generated portal homepage at {index_file} ({len(stories)} stories, lang={lang})")
    return html_str
