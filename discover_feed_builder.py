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
    TMDB_IMAGE_POSTER
)

def build_discover_feed_html(
    articles: List[Dict[str, Any]],
    domain: str = DOMAIN_NAME
) -> str:
    """
    Renders the Google Chrome Discover-style feed landing page.
    """
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    total_articles = len(articles)

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

        feed_cards_data.append({
            "headline": headline,
            "movie_title": movie.get("title", ""),
            "slug": slug,
            "article_url": f"/articles/{slug}/",
            "story_url": f"/stories/{slug}/",
            "backdrop_url": backdrop_url,
            "poster_url": poster_url,
            "description": meta_desc,
            "category": category,
            "rating": rating,
            "reading_time": reading_time,
            "release_date": movie.get("release_date", "Coming Soon")
        })

    cards_json = json.dumps(feed_cards_data)

    cards_html_list = []
    for c in feed_cards_data:
        cat = c["category"]
        if cat == "streaming_charts":
            cat_label = "Weekly Top 10"
        elif cat == "theories_easter_eggs":
            cat_label = "Marvel & DC Theories"
        elif cat == "where_are_they_now":
            cat_label = "Where Are They Now?"
        elif cat == "series":
            cat_label = "TV Series"
        elif cat == "cult_classic":
            cat_label = "Cult Classic"
        else:
            cat_label = cat.replace("_", " ").title()

        card_html = f"""
        <article class="discover-card" data-category="{cat}" data-title="{html.escape(c['headline'].lower())}" data-movie="{html.escape(c['movie_title'].lower())}">
          <a href="{c['article_url']}" class="card-media-link" aria-label="{html.escape(c['headline'])}">
            <div class="card-img-wrap">
              <img src="{c['backdrop_url']}" alt="{html.escape(c['headline'])}" class="card-img" loading="lazy" width="600" height="338">
              <span class="card-cat-badge">{cat_label}</span>
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
              <button class="share-icon-btn" onclick="shareArticle('{c['article_url']}', '{html.escape(c['headline'])}')" title="Share this article">
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
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google Discover Feed | {SITE_NAME} Cinema News & Deep Dives</title>
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="description" content="Explore real-time cinema news, box office breakdowns, fan theories, and streaming hits in our Google Discover entertainment feed.">
  <link rel="canonical" href="{domain}/discover/">
  
  <meta property="og:type" content="website">
  <meta property="og:title" content="Google Discover Feed | {SITE_NAME}">
  <meta property="og:description" content="Daily trending movies, TV series analysis, and visual entertainment stories.">
  <meta property="og:url" content="{domain}/discover/">
  <meta property="og:image" content="{domain}/assets/logo.png">

  <!-- Favicon & Fonts -->
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

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
      --feed-width: 680px;
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
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    /* Header */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.9);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 14px 20px;
    }}

    .nav-container {{
      max-width: 1100px;
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
      gap: 10px;
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

    .nav-btn-active {{
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }}

    /* Discover Hero Banner */
    .discover-header {{
      max-width: var(--feed-width);
      margin: 28px auto 16px;
      padding: 0 16px;
      width: 100%;
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
      font-size: clamp(24px, 4vw, 34px);
      font-weight: 900;
      letter-spacing: -0.8px;
      line-height: 1.2;
      margin-bottom: 8px;
    }}

    .discover-subtitle {{
      font-size: 15px;
      color: var(--text-muted);
    }}

    /* Search & Filter Bar */
    .feed-controls {{
      max-width: var(--feed-width);
      margin: 0 auto 24px;
      padding: 0 16px;
      width: 100%;
    }}

    .search-box {{
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 12px 18px;
      color: #fff;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      margin-bottom: 16px;
    }}

    .search-box:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.2);
    }}

    .filter-pills {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
      scrollbar-width: none;
    }}

    .filter-pills::-webkit-scrollbar {{
      display: none;
    }}

    .filter-pill {{
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }}

    .filter-pill:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}

    .filter-pill.active {{
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 2px 8px var(--primary-glow);
    }}

    /* Chrome Discover Feed Cards */
    .feed-container {{
      max-width: var(--feed-width);
      margin: 0 auto;
      padding: 0 16px 64px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    .discover-card {{
      background: var(--surface-card);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }}

    .discover-card:hover {{
      transform: translateY(-3px);
      border-color: rgba(255, 255, 255, 0.2);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
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
      transition: transform 0.3s ease;
    }}

    .discover-card:hover .card-img {{
      transform: scale(1.02);
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
      background: transparent;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      padding: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      transition: color 0.2s;
    }}

    .share-icon-btn:hover {{
      color: var(--text);
    }}

    .card-title {{
      font-size: clamp(18px, 3vw, 21px);
      font-weight: 800;
      line-height: 1.35;
      letter-spacing: -0.4px;
      margin-bottom: 10px;
    }}

    .card-title a:hover {{
      color: #fda4af;
    }}

    .card-snippet {{
      font-size: 14px;
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
      transition: background 0.2s;
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
      max-width: 1100px;
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

  <!-- Top Navbar -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="/" class="brand-wrap">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo" width="36" height="36">
        <div>
          <div class="brand-title">{SITE_NAME}</div>
          <div class="brand-tag">GOOGLE DISCOVER FEED</div>
        </div>
      </a>
      <div class="nav-links">
        <a href="/" class="nav-btn">⚡ Web Stories</a>
        <a href="/discover/" class="nav-btn nav-btn-active">📰 Discover Feed</a>
      </div>
    </div>
  </nav>

  <!-- Feed Header -->
  <header class="discover-header">
    <div class="discover-pill">⚡ Chrome Discover Portal</div>
    <h1 class="discover-title">Entertainment & Cinema Feed</h1>
    <p class="discover-subtitle">Discover-optimized deep dives, hidden movie easter eggs, weekly streaming charts, and viral entertainment stories.</p>
  </header>

  <!-- Filter & Search Controls -->
  <div class="feed-controls">
    <input type="text" id="searchInput" class="search-box" placeholder="🔍 Search Discover articles, titles, easter eggs..." aria-label="Search articles">
    
    <div class="filter-pills" id="filterPills">
      <button class="filter-pill active" data-filter="all">🔥 All ({total_articles})</button>
      <button class="filter-pill" data-filter="streaming_charts">🍿 Streaming Charts</button>
      <button class="filter-pill" data-filter="theories_easter_eggs">🦸 Marvel & DC Theories</button>
      <button class="filter-pill" data-filter="where_are_they_now">✨ Where Are They Now?</button>
      <button class="filter-pill" data-filter="series">📺 TV Series</button>
      <button class="filter-pill" data-filter="cult_classic">🎬 Cult Classics</button>
      <button class="filter-pill" data-filter="upcoming">⚡ Upcoming</button>
    </div>
  </div>

  <!-- Cards Feed (Chrome Discover Style) -->
  <main class="feed-container" id="feedContainer">
    {cards_html}
    <div id="noResults" class="no-results">
      <p>No articles found matching your filter or search query.</p>
    </div>
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
      <p>© {datetime.now(timezone.utc).year} {PUBLISHER_NAME}. Optimized for Google Chrome Discover & Google Search.</p>
    </div>
  </footer>

  <script>
    function shareArticle(url, title) {{
      const fullUrl = window.location.origin + url;
      if (navigator.share) {{
        navigator.share({{
          title: title,
          url: fullUrl
        }}).catch(() => {{}});
      }} else {{
        navigator.clipboard.writeText(fullUrl).then(() => {{
          alert('Article link copied to clipboard!');
        }});
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
          card.style.display = 'block';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }}

    filterPills.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterPills.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.getAttribute('data-filter');
        applyFilters();
      }});
    }});

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value.toLowerCase().trim();
      applyFilters();
    }});

    // URL parameter support (?category=streaming_charts)
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('category');
    if (catParam) {{
      const targetPill = document.querySelector(`.filter-pill[data-filter="${{catParam}}"]`);
      if (targetPill) {{
        targetPill.click();
      }}
    }}
  </script>
</body>
</html>
"""

def generate_discover_feed(
    articles: List[Dict[str, Any]],
    domain: str = DOMAIN_NAME,
    output_dir: Path = DISCOVER_DIR
) -> str:
    """
    Renders and writes dist/discover/index.html.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    feed_html = build_discover_feed_html(articles, domain=domain)
    output_path = output_dir / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(feed_html)
    print(f"[Discover] Successfully created Chrome Discover feed: {output_path} ({len(articles)} articles)")
    return feed_html
