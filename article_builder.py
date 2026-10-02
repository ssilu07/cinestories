"""
Article Builder module for CineStories / MoviePulse.
Renders standalone, responsive, ultra-fast loading Discover-optimized article HTML pages:
dist/articles/[slug]/index.html

Strictly compliant with Google Discover guidelines:
1. max-image-preview:large robots meta tag
2. High-res 1200px+ landscape images (TMDB w1280)
3. Schema.org NewsArticle JSON-LD structured data
4. Mobile-first, high contrast typography with cross-linking to Web Stories
"""

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from config import (
    DOMAIN_NAME,
    SITE_NAME,
    PUBLISHER_NAME,
    TMDB_IMAGE_BACKDROP,
    TMDB_IMAGE_POSTER,
    get_publisher_logo_url
)

def build_discover_article_html(
    article: Dict[str, Any],
    domain: str = DOMAIN_NAME,
    related_articles: List[Dict[str, Any]] = None
) -> str:
    """
    Renders a Google Discover-optimized article HTML document.
    """
    movie = article.get("movie", {})
    slug = movie.get("slug", "movie-article")
    movie_title = movie.get("title", "Featured Story")
    headline = article.get("headline") or f"{movie_title}: Everything You Need To Know"
    meta_desc = article.get("meta_description") or movie.get("overview", "")[:155]
    category = movie.get("category", "trending")
    category_label = category.replace("_", " ").title()
    if category == "streaming_charts":
        category_label = "Weekly Top 10"
    elif category == "theories_easter_eggs":
        category_label = "Marvel & DC Theories"
    elif category == "where_are_they_now":
        category_label = "Where Are They Now?"
    elif category == "series":
        category_label = "TV Series"
    elif category == "cult_classic":
        category_label = "Cult Classic"
    elif category == "steamy_thrillers":
        category_label = "Bold & Steamy Thrillers"

    # Images
    backdrop_path = movie.get("backdrop_path")
    poster_path = movie.get("poster_path")
    backdrop_url = f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path else f"{domain}/assets/logo.png"
    poster_url = f"{TMDB_IMAGE_POSTER}{poster_path}" if poster_path else backdrop_url
    logo_url = get_publisher_logo_url(domain)

    # Dates
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_display = datetime.now(timezone.utc).strftime("%B %d, %Y")
    release_date = movie.get("release_date", "Coming Soon")
    rating = movie.get("vote_average", 0.0)
    runtime = movie.get("runtime", 120)
    seasons = movie.get("seasons")
    director = movie.get("director", "Unknown")
    top_cast = movie.get("top_cast", [])
    cast_str = ", ".join(top_cast[:4]) if top_cast else "Ensemble Cast"
    genres = movie.get("genres", ["Entertainment"])
    genres_str = " • ".join(genres[:3])
    reading_time = article.get("reading_time_mins", 3)

    article_url = f"{domain}/articles/{slug}/"
    story_url = f"{domain}/stories/{slug}/"

    # JSON-LD Schema (NewsArticle for Discover)
    schema_data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": article_url
        },
        "headline": headline[:110],
        "description": meta_desc,
        "image": [
            backdrop_url,
            poster_url
        ],
        "datePublished": today_iso,
        "dateModified": today_iso,
        "author": {
            "@type": "Person",
            "name": f"{SITE_NAME} Editorial Desk",
            "url": f"{domain}/about/"
        },
        "publisher": {
            "@type": "Organization",
            "name": PUBLISHER_NAME,
            "logo": {
                "@type": "ImageObject",
                "url": logo_url,
                "width": 512,
                "height": 512
            }
        },
        "articleSection": category_label,
        "keywords": [movie_title] + genres + ["Google Discover", "Cinema", "Web Stories"]
    }
    schema_json = json.dumps(schema_data, indent=2)

    # Key Takeaways HTML
    takeaways = article.get("key_takeaways", [])
    takeaways_items = "".join([f"<li>{html.escape(t)}</li>" for t in takeaways]) if takeaways else ""
    takeaways_html = f"""
    <div class="takeaways-box">
      <div class="takeaways-header">
        <span class="takeaways-icon">⚡</span>
        <h3>Key Takeaways for Readers</h3>
      </div>
      <ul class="takeaways-list">
        {takeaways_items}
      </ul>
    </div>
    """ if takeaways_items else ""

    # Sections HTML
    sections = article.get("sections", [])
    sections_html = []
    for sec in sections:
        h = html.escape(sec.get("heading", ""))
        c = html.escape(sec.get("content", ""))
        sections_html.append(f"""
        <section class="article-section">
          <h2>{h}</h2>
          <p>{c}</p>
        </section>
        """)
    sections_rendered = "\n".join(sections_html)

    # Verdict summary
    verdict = article.get("verdict_summary", "")
    verdict_html = f"""
    <div class="verdict-card">
      <div class="verdict-tag">EDITOR'S TAKE</div>
      <p>{html.escape(verdict)}</p>
    </div>
    """ if verdict else ""

    # Related articles
    related_html_list = []
    if related_articles:
        for rel in related_articles[:3]:
            r_movie = rel.get("movie", {})
            r_slug = r_movie.get("slug", "")
            r_title = rel.get("headline") or r_movie.get("title", "")
            r_thumb = f"{TMDB_IMAGE_BACKDROP}{r_movie.get('backdrop_path')}" if r_movie.get('backdrop_path') else f"{domain}/assets/logo.png"
            related_html_list.append(f"""
            <a href="/articles/{r_slug}/" class="related-card">
              <img src="{r_thumb}" alt="{html.escape(r_title)}" loading="lazy" width="280" height="158">
              <div class="related-info">
                <h4>{html.escape(r_title)}</h4>
                <span>{r_movie.get('category', 'trending').replace('_', ' ').title()} • 3 min read</span>
              </div>
            </a>
            """)
    related_section = f"""
    <div class="related-section">
      <h3 class="section-title">Trending in Google Discover</h3>
      <div class="related-grid">
        {"".join(related_html_list)}
      </div>
    </div>
    """ if related_html_list else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(headline)} | {SITE_NAME}</title>
  
  <!-- Critical Google Discover Meta Tag -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="description" content="{html.escape(meta_desc)}">
  <link rel="canonical" href="{article_url}">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:url" content="{article_url}">
  <meta property="og:title" content="{html.escape(headline)}">
  <meta property="og:description" content="{html.escape(meta_desc)}">
  <meta property="og:image" content="{backdrop_url}">
  <meta property="og:image:secure_url" content="{backdrop_url}">
  <meta property="og:image:width" content="1280">
  <meta property="og:image:height" content="720">
  <meta property="og:image:alt" content="{html.escape(movie_title)} Cover">
  <meta property="article:published_time" content="{today_iso}">
  <meta property="article:modified_time" content="{today_iso}">
  <meta property="article:section" content="{category_label}">
  
  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@{SITE_NAME}">
  <meta name="twitter:title" content="{html.escape(headline)}">
  <meta name="twitter:description" content="{html.escape(meta_desc)}">
  <meta name="twitter:image" content="{backdrop_url}">

  <!-- Favicon & Fonts -->
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Structured Data JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>

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
      --max-width: 840px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.75;
      font-size: 18px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    /* Top Navigation Bar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 14px 20px;
    }}

    .nav-container {{
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand-logo {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
    }}

    .brand-title {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}

    .brand-tag {{
      font-size: 10px;
      color: var(--accent-gold);
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .nav-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      transition: all 0.2s ease;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
    }}

    .nav-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .nav-btn-primary {{
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 4px 12px var(--primary-glow);
    }}

    .nav-btn-primary:hover {{
      background: var(--primary-hover);
    }}

    /* Main Article Container */
    .article-container {{
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 32px 20px 64px;
      width: 100%;
      flex: 1;
    }}

    /* Breadcrumbs */
    .breadcrumbs {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 13px;
      color: var(--text-dim);
      margin-bottom: 20px;
    }}

    .breadcrumbs a:hover {{
      color: var(--text);
    }}

    /* Meta Badges */
    .article-header-meta {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
    }}

    .category-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(225, 29, 72, 0.18);
      color: #fda4af;
      border: 1px solid rgba(225, 29, 72, 0.35);
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .read-time-pill {{
      font-size: 13px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    /* Headline */
    .article-headline {{
      font-size: clamp(26px, 4vw, 42px);
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -0.8px;
      color: #ffffff;
      margin-bottom: 18px;
    }}

    /* Author & Date Byline */
    .byline-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      padding-bottom: 24px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--surface-border);
    }}

    .author-info {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .author-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--primary), var(--accent-gold));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 16px;
    }}

    .author-details h4 {{
      font-size: 15px;
      font-weight: 700;
    }}

    .author-details p {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .share-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .share-btn {{
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .share-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    /* Hero Backdrop Image (Google Discover 1200px+ format) */
    .hero-media-wrap {{
      position: relative;
      border-radius: var(--radius-lg);
      overflow: hidden;
      margin-bottom: 32px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
      border: 1px solid var(--surface-border);
      aspect-ratio: 16 / 9;
      background-color: var(--surface);
    }}

    .hero-media-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .hero-caption {{
      padding: 10px 16px;
      font-size: 12px;
      color: var(--text-dim);
      background: var(--surface);
      border-top: 1px solid var(--surface-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Web Story Callout Banner */
    .story-callout {{
      background: linear-gradient(135deg, rgba(225, 29, 72, 0.15), rgba(245, 158, 11, 0.15));
      border: 1px solid rgba(225, 29, 72, 0.4);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 36px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .story-callout-text h4 {{
      font-size: 16px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }}

    .story-callout-text p {{
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    .launch-story-btn {{
      background: linear-gradient(135deg, var(--primary), #be123c);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      padding: 10px 20px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 14px var(--primary-glow);
      transition: transform 0.2s, box-shadow 0.2s;
      white-space: nowrap;
    }}

    .launch-story-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(225, 29, 72, 0.6);
    }}

    /* Key Takeaways Box */
    .takeaways-box {{
      background: var(--surface-card);
      border-left: 4px solid var(--accent-gold);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 24px;
      margin-bottom: 36px;
      border-top: 1px solid var(--surface-border);
      border-right: 1px solid var(--surface-border);
      border-bottom: 1px solid var(--surface-border);
    }}

    .takeaways-header {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }}

    .takeaways-header h3 {{
      font-size: 17px;
      font-weight: 800;
      color: var(--accent-gold);
      letter-spacing: -0.3px;
    }}

    .takeaways-list {{
      list-style-type: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .takeaways-list li {{
      font-size: 16px;
      color: #e2e8f0;
      position: relative;
      padding-left: 24px;
      line-height: 1.6;
    }}

    .takeaways-list li::before {{
      content: "✔";
      position: absolute;
      left: 0;
      color: var(--accent-gold);
      font-weight: 900;
      font-size: 14px;
    }}

    /* Article Body Sections */
    .article-section {{
      margin-bottom: 36px;
    }}

    .article-section h2 {{
      font-size: clamp(20px, 3vw, 26px);
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 14px;
      letter-spacing: -0.5px;
      line-height: 1.3;
    }}

    .article-section p {{
      color: #cbd5e1;
      line-height: 1.8;
      margin-bottom: 16px;
    }}

    /* Movie Specs Card */
    .specs-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 24px;
      margin: 36px 0;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 18px;
    }}

    .spec-item h5 {{
      font-size: 11px;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}

    .spec-item p {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }}

    /* Verdict Card */
    .verdict-card {{
      background: linear-gradient(135deg, rgba(16, 20, 31, 0.95), rgba(21, 26, 40, 0.95));
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 24px;
      margin: 36px 0;
      position: relative;
    }}

    .verdict-tag {{
      display: inline-block;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      background: var(--primary);
      color: #fff;
      padding: 3px 10px;
      border-radius: 4px;
      margin-bottom: 10px;
    }}

    .verdict-card p {{
      font-size: 16px;
      color: #e2e8f0;
      font-style: italic;
      line-height: 1.7;
    }}

    /* Related Grid */
    .related-section {{
      margin-top: 56px;
      padding-top: 36px;
      border-top: 1px solid var(--surface-border);
    }}

    .section-title {{
      font-size: 20px;
      font-weight: 800;
      margin-bottom: 20px;
      color: #fff;
    }}

    .related-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
    }}

    .related-card {{
      background: var(--surface-card);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      overflow: hidden;
      transition: transform 0.2s, border-color 0.2s;
      display: flex;
      flex-direction: column;
    }}

    .related-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(225, 29, 72, 0.5);
    }}

    .related-card img {{
      width: 100%;
      height: 140px;
      object-fit: cover;
    }}

    .related-info {{
      padding: 14px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .related-info h4 {{
      font-size: 14px;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 8px;
      color: #fff;
    }}

    .related-info span {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    /* Footer */
    .footer {{
      background: #06070a;
      border-top: 1px solid var(--surface-border);
      padding: 40px 20px;
      margin-top: auto;
      font-size: 13px;
      color: var(--text-dim);
    }}

    .footer-container {{
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
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

    @media (max-width: 640px) {{
      body {{
        font-size: 17px;
      }}
      .article-container {{
        padding: 20px 16px 48px;
      }}
      .hero-media-wrap {{
        border-radius: var(--radius-md);
        margin-bottom: 24px;
      }}
      .specs-card {{
        grid-template-columns: 1fr 1fr;
      }}
    }}
  </style>
</head>
<body>

  <!-- Navigation -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="/" class="brand-wrap" aria-label="{SITE_NAME} Home">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo" width="36" height="36">
        <div>
          <div class="brand-title">{SITE_NAME}</div>
          <div class="brand-tag">DISCOVER & STORIES</div>
        </div>
      </a>
      <div class="nav-links">
        <a href="/discover/" class="nav-btn" aria-label="Chrome Discover Feed">📰 Discover Feed</a>
        <a href="{story_url}" class="nav-btn nav-btn-primary" aria-label="Watch AMP Story">⚡ Web Story</a>
      </div>
    </div>
  </nav>

  <!-- Main Article Body -->
  <main class="article-container">
    
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="/">Home</a>
      <span>›</span>
      <a href="/discover/">Discover</a>
      <span>›</span>
      <a href="/discover/?category={category}">{category_label}</a>
      <span>›</span>
      <span>{html.escape(movie_title)}</span>
    </div>

    <!-- Header Meta Badges -->
    <div class="article-header-meta">
      <span class="category-badge">{category_label}</span>
      <span class="read-time-pill">⏱ {reading_time} min read</span>
      <span class="read-time-pill">📅 {date_display}</span>
    </div>

    <!-- Main Headline -->
    <h1 class="article-headline">{html.escape(headline)}</h1>

    <!-- Byline & Social Share -->
    <div class="byline-bar">
      <div class="author-info">
        <div class="author-avatar">M</div>
        <div class="author-details">
          <h4>{SITE_NAME} Editorial Desk</h4>
          <p>Verified Cinema & Streaming Analysis</p>
        </div>
      </div>
      <div class="share-actions">
        <button class="share-btn" onclick="navigator.clipboard.writeText(window.location.href); alert('Link copied to clipboard!');">📋 Copy Link</button>
        <a class="share-btn" href="https://twitter.com/intent/tweet?text={html.escape(headline)}&url={article_url}" target="_blank" rel="noopener">🐦 Tweet</a>
      </div>
    </div>

    <!-- 1200px+ High Res Hero Image for Google Discover -->
    <figure class="hero-media-wrap">
      <img src="{backdrop_url}" alt="{html.escape(movie_title)}" width="1280" height="720" fetchpriority="high">
      <div class="hero-caption">
        <span>Featured Still: {html.escape(movie_title)}</span>
        <span>Source: TMDB API</span>
      </div>
    </figure>

    <!-- Interactive Cross-Link to Web Story -->
    <div class="story-callout">
      <div class="story-callout-text">
        <h4>⚡ Visual Web Story Available</h4>
        <p>Short on time? Experience this story as a fast, interactive 6-slide Google AMP Web Story.</p>
      </div>
      <a href="{story_url}" class="launch-story-btn">
        <span>Tap to Launch Web Story</span>
        <span>👉</span>
      </a>
    </div>

    <!-- Key Takeaways Box (Google Discover Engagement Booster) -->
    {takeaways_html}

    <!-- Article Sections -->
    <article class="article-body">
      {sections_rendered}
    </article>

    <!-- Movie Specifications / Metadata Card -->
    <div class="specs-card">
      <div class="spec-item">
        <h5>Release Date</h5>
        <p>{release_date}</p>
      </div>
      <div class="spec-item">
        <h5>Audience Rating</h5>
        <p>★ {rating} / 10</p>
      </div>
      <div class="spec-item">
        <h5>Director / Creator</h5>
        <p>{director}</p>
      </div>
      <div class="spec-item">
        <h5>Format / Length</h5>
        <p>{"📺 " + str(seasons) + " Seasons" if seasons else f"⏱ {runtime} mins"}</p>
      </div>
      <div class="spec-item" style="grid-column: 1 / -1;">
        <h5>Starring Cast</h5>
        <p>{cast_str}</p>
      </div>
    </div>

    <!-- Editorial Verdict -->
    {verdict_html}

    <!-- Related Articles -->
    {related_section}

  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-links">
        <a href="/">Home</a>
        <a href="/discover/">Discover Feed</a>
        <a href="/about/">About Us</a>
        <a href="/editorial/">Editorial Policy</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms of Service</a>
        <a href="/contact/">Contact Us</a>
        <a href="/sitemap.xml">XML Sitemap</a>
      </div>
      <p>© {datetime.now(timezone.utc).year} {PUBLISHER_NAME}. Independent entertainment analysis. Movie metadata & imagery powered by TMDB.</p>
    </div>
  </footer>

</body>
</html>
"""
