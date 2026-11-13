"""
Article Builder module for CineStories / MoviePulse.
Renders standalone, responsive, ultra-fast loading Discover-optimized article HTML pages:
dist/articles/[slug]/index.html and dist/hi/articles/[slug]/index.html

Strictly compliant with Google Discover guidelines:
1. max-image-preview:large robots meta tag
2. High-res 1200px+ landscape images (TMDB w1280)
3. Schema.org NewsArticle JSON-LD structured data
4. Mobile-first, high contrast typography with cross-linking to Web Stories
5. Viral-grade tactile micro-delights (toast notification, celebratory sparkles)
"""

import html
import json
from urllib.parse import quote
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from config import (
    DOMAIN_NAME,
    SITE_NAME,
    PUBLISHER_NAME,
    TMDB_IMAGE_BACKDROP,
    TMDB_IMAGE_POSTER,
    get_publisher_logo_url,
    get_ga_script,
    get_adsense_script
)

def build_discover_article_html(
    article: Dict[str, Any],
    domain: str = DOMAIN_NAME,
    related_articles: List[Dict[str, Any]] = None,
    lang: str = "en"
) -> str:
    """
    Renders a Google Discover-optimized article HTML document.
    Supports English ("en") and Hindi ("hi") with bidirectional hreflangs,
    streamlined mobile header, reading progress bar, verified editorial byline,
    and celebratory copy-to-clipboard toast delight.
    """
    is_hi = (lang == "hi")
    html_lang = "hi" if is_hi else "en"
    og_locale = "hi_IN" if is_hi else "en_US"
    in_lang = "hi-IN" if is_hi else "en-US"

    movie = article.get("movie", {})
    slug = movie.get("slug", "movie-article")
    movie_title = movie.get("title", "Featured Story")
    headline = article.get("headline") or f"{movie_title}: Everything You Need To Know"
    meta_desc = article.get("meta_description") or movie.get("overview", "")[:155]
    category = movie.get("category", "trending")
    category_label = category.replace("_", " ").title()
    if category == "streaming_charts":
        category_label = "साप्ताहिक टॉप 10" if is_hi else "Weekly Top 10"
    elif category == "theories_easter_eggs":
        category_label = "मार्वल व डीसी थ्योरीज़" if is_hi else "Marvel & DC Theories"
    elif category == "where_are_they_now":
        category_label = "अब कहाँ हैं सितारे?" if is_hi else "Where Are They Now?"
    elif category == "series":
        category_label = "टीवी सीरीज़" if is_hi else "TV Series"
    elif category == "cult_classic":
        category_label = "कल्ट क्लासिक" if is_hi else "Cult Classic"
    elif category == "steamy_thrillers":
        category_label = "बोल्ड व थ्रिलर" if is_hi else "Bold & Steamy Thrillers"

    # Images
    backdrop_path = movie.get("backdrop_path")
    poster_path = movie.get("poster_path")
    backdrop_url = f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path else f"{domain}/assets/logo.png"
    poster_url = f"{TMDB_IMAGE_POSTER}{poster_path}" if poster_path else backdrop_url
    logo_url = get_publisher_logo_url(domain)

    # Dates
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pub_iso = article.get("date_published") or article.get("published_at") or today_iso
    mod_iso = article.get("date_modified") or article.get("modified_at") or pub_iso
    try:
        dt = datetime.fromisoformat(pub_iso.replace("Z", "+00:00"))
        date_display = dt.strftime("%B %d, %Y")
    except Exception:
        date_display = datetime.now(timezone.utc).strftime("%B %d, %Y")

    release_date = movie.get("release_date", "Coming Soon")
    rating = movie.get("vote_average", 0.0)
    runtime = movie.get("runtime", 120)
    seasons = movie.get("seasons")
    director = movie.get("director", "Unknown")
    top_cast = movie.get("top_cast", [])
    cast_str = ", ".join(top_cast[:4]) if top_cast else ("मुख्य कलाकार" if is_hi else "Ensemble Cast")
    genres = movie.get("genres", ["Entertainment"])
    genres_str = " • ".join(genres[:3])
    reading_time = article.get("reading_time_mins", 3)

    # Localized routing
    prefix = "/hi" if is_hi else ""
    canonical_url = f"{domain}{prefix}/articles/{slug}/"
    story_url = f"{prefix}/stories/{slug}/"
    home_url = f"{prefix}/"
    discover_url = f"{prefix}/discover/"
    en_article_url = f"{domain}/articles/{slug}/"
    hi_article_url = f"{domain}/hi/articles/{slug}/"

    share_text = f"{headline} - Read full breakdown on CineStories" if not is_hi else f"{headline} - सिनेस्टोरीज़ पर पूरा विश्लेषण पढ़ें"
    encoded_share_text = quote(share_text)
    encoded_url = quote(canonical_url)
    encoded_headline = quote(headline)
    encoded_backdrop = quote(backdrop_url)

    # Localized labels
    home_label = "होम" if is_hi else "Home"
    discover_label = "डिस्कवर" if is_hi else "Discover"
    discover_btn_label = "📰 डिस्कवर फीड" if is_hi else "📰 Discover Feed"
    story_btn_label = "⚡ वेब स्टोरी" if is_hi else "⚡ Web Story"
    about_label = "हमारे बारे में" if is_hi else "About Us"
    editorial_label = "संपादकीय नीति" if is_hi else "Editorial"
    contact_label = "संपर्क" if is_hi else "Contact"
    read_time_label = f"⏱ {reading_time} मिनट पठन" if is_hi else f"⏱ {reading_time} min read"
    author_role = "प्रमाणित फैक्ट-चेक विश्लेषण" if is_hi else "Fact-Checked &amp; Verified"
    who_label = "✓ किसे पसंद आएगी:" if is_hi else "✓ Who Will Love This:"
    skip_label = "⚠️ किसे छोड़नी चाहिए:" if is_hi else "⚠️ Who Should Pass:"
    takeaways_heading = "पाठकों के लिए मुख्य बातें" if is_hi else "Key Takeaways for Readers"
    verdict_badge = "संपादक की राय" if is_hi else "EDITOR'S TAKE"
    story_callout_h4 = "⚡ दृश्य वेब स्टोरी उपलब्ध है" if is_hi else "⚡ Visual Web Story Available"
    story_callout_p = "समय कम है? इस कहानी को तेज, 6-स्लाइड इंटरएक्टिव गूगल एएमपी वेब स्टोरी के रूप में देखें।" if is_hi else "Short on time? Experience this story as a fast, interactive 6-slide Google AMP Web Story."
    launch_story_btn_text = "वेब स्टोरी देखें" if is_hi else "Tap to Launch Web Story"
    viral_h4 = "⚡ क्लाइमेक्स विवरण दोस्तों के साथ साझा करें" if is_hi else "⚡ Share The Climax Clues With Your Friends"
    viral_p = "क्या उन्हें यह महत्वपूर्ण विवरण याद नहीं रहा? इस समीक्षा को सीधे अपने व्हाट्सएप ग्रुप पर भेजें।" if is_hi else "Think they missed this ending detail? Send this breakdown directly to your WhatsApp group or Pinterest board."
    wa_share_label = "💬 व्हाट्सएप पर साझा करें" if is_hi else "💬 Share on WhatsApp"
    pin_share_label = "📌 पिंटरेस्ट पर सेव करें" if is_hi else "📌 Save to Pinterest"
    copy_share_label = "📋 लिंक कॉपी करें" if is_hi else "📋 Copy Link"
    toast_copy_msg = "आर्टिकल लिंक कॉपी हो गया! 🎉" if is_hi else "Article link copied to clipboard! 🎉"
    related_title = "गूगल डिस्कवर में ट्रेंडिंग" if is_hi else "Trending in Google Discover"

    # JSON-LD Schema (NewsArticle & BreadcrumbList for Discover)
    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "NewsArticle",
                "@id": f"{canonical_url}#article",
                "isPartOf": {
                    "@type": "WebPage",
                    "@id": canonical_url
                },
                "headline": headline[:110],
                "description": meta_desc,
                "image": [
                    backdrop_url,
                    poster_url
                ],
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
                        "url": logo_url,
                        "width": 512,
                        "height": 512
                    }
                },
                "articleSection": category_label,
                "keywords": [movie_title] + genres + ["Google Discover", "Cinema", "Web Stories"]
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": home_label,
                        "item": f"{domain}{prefix}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": discover_label,
                        "item": f"{domain}{prefix}/discover/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": headline[:60],
                        "item": canonical_url
                    }
                ]
            }
        ]
    }
    schema_json = json.dumps(schema_data, indent=2)

    # Human Editorial Audience Guide
    who_watch = article.get("who_should_watch")
    skip_if = article.get("skip_if")
    if not who_watch:
        who_watch = f"Fans of gripping {genres_str} entertainment who appreciate standout performances from {cast_str} and tight direction by {director}."
    if not skip_if:
        skip_if = "Viewers looking for breezy background comedy or those sensitive to intense, high-pressure conflict."

    audience_guide_html = f"""
    <div class="audience-guide-card">
      <div class="guide-tag">🎯 AUDIENCE &amp; WATCHLIST GUIDE</div>
      <div class="guide-row">
        <div class="guide-col">
          <span class="guide-label green">{who_label}</span>
          <p>{html.escape(who_watch)}</p>
        </div>
        <div class="guide-col">
          <span class="guide-label amber">{skip_label}</span>
          <p>{html.escape(skip_if)}</p>
        </div>
      </div>
    </div>
    """

    # Key Takeaways HTML
    takeaways = article.get("key_takeaways", [])
    takeaways_items = "".join([f"<li>{html.escape(t)}</li>" for t in takeaways]) if takeaways else ""
    takeaways_html = f"""
    <div class="takeaways-box">
      <div class="takeaways-header">
        <span class="takeaways-icon">⚡</span>
        <h3>{takeaways_heading}</h3>
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
      <div class="verdict-tag">{verdict_badge}</div>
      <p>{html.escape(verdict)}</p>
    </div>
    """ if verdict else ""

    # Related articles
    if not related_articles:
        try:
            if is_hi:
                from curated_articles_hi import CURATED_ARTICLES_HI
                related_articles = [
                    {
                        "movie": {"slug": s, "title": CURATED_ARTICLES_HI[s].get("headline", s), "category": "trending"},
                        "headline": CURATED_ARTICLES_HI[s].get("headline", s)
                    }
                    for s in list(CURATED_ARTICLES_HI.keys()) if s != slug
                ][:3]
            else:
                from curated_articles import CURATED_ARTICLES
                related_articles = [
                    {
                        "movie": {"slug": s, "title": CURATED_ARTICLES[s].get("headline", s), "category": "trending"},
                        "headline": CURATED_ARTICLES[s].get("headline", s)
                    }
                    for s in list(CURATED_ARTICLES.keys())[:10] if s != slug
                ][:3]
        except Exception:
            related_articles = []

    related_html_list = []
    if related_articles:
        for rel in related_articles[:3]:
            r_movie = rel.get("movie", {})
            r_slug = r_movie.get("slug", "")
            r_title = rel.get("headline") or r_movie.get("title", "")
            r_thumb = f"{TMDB_IMAGE_BACKDROP}{r_movie.get('backdrop_path')}" if r_movie.get('backdrop_path') else f"{domain}/assets/logo.png"
            related_html_list.append(f"""
            <a href="{prefix}/articles/{r_slug}/" class="related-card">
              <img src="{r_thumb}" alt="{html.escape(r_title)}" loading="lazy" width="280" height="158">
              <div class="related-info">
                <h4>{html.escape(r_title)}</h4>
                <span>{r_movie.get('category', 'trending').replace('_', ' ').title()} • 3 min read</span>
              </div>
            </a>
            """)
    related_section = f"""
    <div class="related-section related-articles">
      <h3 class="section-title">{related_title}</h3>
      <div class="related-grid">
        {"".join(related_html_list)}
      </div>
    </div>
    """ if related_html_list else ""

    # Language Switcher Pill Markup
    if is_hi:
        lang_switch_html = f"""
        <div class="lang-switch-pill" role="group" aria-label="Language Selector">
          <a href="/articles/{slug}/" class="lang-pill" aria-label="Read in English">🇺🇸 EN</a>
          <span class="lang-pill active" aria-current="page">🇮🇳 हिं</span>
        </div>
        """
    else:
        lang_switch_html = f"""
        <div class="lang-switch-pill" role="group" aria-label="Language Selector">
          <span class="lang-pill active" aria-current="page">🇺🇸 EN</span>
          <a href="/hi/articles/{slug}/" class="lang-pill" aria-label="हिंदी में पढ़ें">🇮🇳 हिं</a>
        </div>
        """

    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
{get_ga_script()}
{get_adsense_script()}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(headline)} | {SITE_NAME}</title>
  
  <!-- Critical Google Discover Meta Tag -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="description" content="{html.escape(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
  
  <!-- Bidirectional Hreflangs -->
  <link rel="alternate" hreflang="en" href="{en_article_url}">
  <link rel="alternate" hreflang="hi" href="{hi_article_url}">
  <link rel="alternate" hreflang="x-default" href="{en_article_url}">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{html.escape(headline)}">
  <meta property="og:description" content="{html.escape(meta_desc)}">
  <meta property="og:image" content="{backdrop_url}">
  <meta property="og:image:secure_url" content="{backdrop_url}">
  <meta property="og:image:width" content="1280">
  <meta property="og:image:height" content="720">
  <meta property="og:image:alt" content="{html.escape(movie_title)} Cover">
  <meta property="article:published_time" content="{pub_iso}">
  <meta property="article:modified_time" content="{mod_iso}">
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
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

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
      --max-width: 820px;
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
      line-height: 1.8;
      font-size: 18px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    /* Top Reading Scroll Progress Bar */
    .reading-progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), var(--accent-gold));
      z-index: 1000;
      width: 0%;
      transition: width 0.1s linear;
    }}

    /* Top Navigation Bar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 12px 16px;
    }}

    .nav-container {{
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}

    .brand-logo {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: block;
    }}

    .brand-title {{
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.5px;
      white-space: nowrap;
    }}

    .brand-tag {{
      font-size: 9.5px;
      color: var(--accent-gold);
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
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

    /* Language Switcher Pill */
    .lang-switch-pill {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      border-radius: 999px;
      padding: 2px 4px;
      gap: 2px;
      flex-shrink: 0;
    }}

    .lang-pill {{
      font-size: 12px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 999px;
      color: var(--text-muted);
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
      display: inline-block;
      line-height: 1.2;
    }}

    .lang-pill:hover {{
      color: #fff;
    }}

    .lang-pill:active {{
      transform: scale(0.96);
    }}

    .lang-pill.active {{
      background: var(--primary);
      color: #fff;
      box-shadow: 0 2px 8px var(--primary-glow);
    }}

    .nav-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      transition: all 0.15s ease;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      white-space: nowrap;
    }}

    .nav-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .nav-btn:active {{
      transform: scale(0.97);
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

    @media (max-width: 768px) {{
      .nav-link-desktop {{
        display: none !important;
      }}
      .brand-tag {{
        display: none;
      }}
    }}

    @media (max-width: 420px) {{
      .navbar {{
        padding: 8px 10px;
      }}
      .nav-container {{
        gap: 6px;
      }}
      .brand-logo {{
        width: 30px;
        height: 30px;
      }}
      .brand-title {{
        font-size: 16px;
      }}
      .lang-pill {{
        font-size: 11px;
        padding: 3px 6px;
      }}
      .nav-btn {{
        padding: 6px 10px;
        font-size: 12px;
      }}
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
    .author-meta, .article-meta {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .byline-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      padding-bottom: 24px;
      margin-bottom: 28px;
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
      color: #fff;
      flex-shrink: 0;
    }}

    .author-details h4 {{
      font-size: 15px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .author-details p {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .verified-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #38bdf8;
      color: #0b0f19;
      font-size: 10px;
      font-weight: 900;
    }}

    .share-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .share-btn {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      border-radius: 999px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      text-decoration: none;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }}

    .share-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }}

    .share-btn:active {{
      transform: scale(0.96);
    }}

    .share-whatsapp {{
      color: #25d366;
      border-color: rgba(37, 211, 102, 0.35);
      background: rgba(37, 211, 102, 0.08);
    }}
    .share-whatsapp:hover {{
      background: #25d366;
      color: #0b0f19;
    }}

    .share-pinterest {{
      color: #f43f5e;
      border-color: rgba(244, 63, 94, 0.35);
      background: rgba(244, 63, 94, 0.08);
    }}
    .share-pinterest:hover {{
      background: #e60023;
      color: #fff;
    }}

    .share-telegram {{
      color: #38bdf8;
      border-color: rgba(56, 189, 248, 0.35);
      background: rgba(56, 189, 248, 0.08);
    }}
    .share-telegram:hover {{
      background: #0284c7;
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
      transition: transform 0.15s, box-shadow 0.15s;
      white-space: nowrap;
    }}

    .launch-story-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(225, 29, 72, 0.6);
    }}

    .launch-story-btn:active {{
      transform: scale(0.97);
    }}

    /* Key Takeaways Box */
    .takeaways-box {{
      background: linear-gradient(135deg, rgba(21, 26, 40, 0.95), rgba(16, 20, 31, 0.9));
      border-left: 4px solid var(--accent-gold);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 24px;
      margin-bottom: 36px;
      border-top: 1px solid var(--surface-border);
      border-right: 1px solid var(--surface-border);
      border-bottom: 1px solid var(--surface-border);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
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

    /* Article Body Sections - Enhanced Reading Experience */
    .article-body {{
      max-width: 740px;
      margin: 0 auto 36px;
    }}

    .article-section {{
      margin-bottom: 32px;
    }}

    .article-section h2 {{
      font-size: clamp(20px, 3vw, 26px);
      font-weight: 800;
      color: #ffffff;
      margin-top: 32px;
      margin-bottom: 14px;
      letter-spacing: -0.5px;
      line-height: 1.35;
      border-left: 3px solid var(--primary);
      padding-left: 14px;
    }}

    .article-section p {{
      color: #cbd5e1;
      line-height: 1.85;
      margin-bottom: 18px;
      font-size: 17.5px;
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

    /* Audience Guide Card (Human Editorial Touch) */
    .audience-guide-card {{
      background: linear-gradient(135deg, rgba(16, 20, 31, 0.95), rgba(21, 26, 40, 0.95));
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: var(--radius-md);
      padding: 22px;
      margin: 28px 0;
    }}
    .guide-tag {{
      display: inline-block;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      background: rgba(245, 158, 11, 0.18);
      color: var(--accent-gold);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 3px 10px;
      border-radius: 4px;
      margin-bottom: 14px;
    }}
    .guide-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}
    .guide-label {{
      font-size: 13px;
      font-weight: 700;
      display: block;
      margin-bottom: 6px;
    }}
    .guide-label.green {{
      color: #34d399;
    }}
    .guide-label.amber {{
      color: #fbbf24;
    }}
    .guide-col p {{
      font-size: 15px;
      color: #cbd5e1;
      line-height: 1.6;
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

    /* Viral Share Box */
    .viral-share-box {{
      margin: 36px 0;
      padding: 24px;
      background: linear-gradient(135deg, rgba(225, 29, 72, 0.12) 0%, rgba(245, 158, 11, 0.09) 100%);
      border: 1px solid rgba(225, 29, 72, 0.3);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .viral-share-text h4 {{
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin: 0 0 6px 0;
    }}

    .viral-share-text p {{
      font-size: 13.5px;
      color: var(--text-muted);
      margin: 0;
      line-height: 1.5;
    }}

    .viral-share-btns {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .btn-share-wa {{
      background: #25d366;
      color: #0b0f19;
      padding: 9px 18px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 800;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35);
      transition: transform 0.15s ease;
    }}
    .btn-share-wa:hover {{
      transform: translateY(-2px);
    }}
    .btn-share-wa:active {{
      transform: scale(0.97);
    }}

    .btn-share-pin {{
      background: #e60023;
      color: #fff;
      padding: 9px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: transform 0.15s ease;
    }}
    .btn-share-pin:hover {{
      transform: translateY(-2px);
    }}
    .btn-share-pin:active {{
      transform: scale(0.97);
    }}

    .btn-share-tg {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 9px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: transform 0.15s ease;
    }}
    .btn-share-tg:hover {{
      background: #38bdf8;
      color: #000;
    }}
    .btn-share-tg:active {{
      transform: scale(0.97);
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

    .related-card:active {{
      transform: scale(0.98);
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

    /* Toast Notification */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(16, 20, 31, 0.95);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(225, 29, 72, 0.4);
      color: #fff;
      padding: 12px 20px;
      border-radius: 999px;
      font-size: 13.5px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
      z-index: 9999;
      transform: translateY(100px);
      opacity: 0;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
      pointer-events: none;
    }}

    .toast-notification.show {{
      transform: translateY(0);
      opacity: 1;
    }}

    /* Sparkles */
    .sparkle-particle {{
      position: fixed;
      width: 7px;
      height: 7px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 10001;
      animation: sparkleAnim 0.8s ease-out forwards;
    }}

    @keyframes sparkleAnim {{
      0% {{
        transform: scale(0.4) translateY(0);
        opacity: 1;
      }}
      100% {{
        transform: scale(1.6) translateY(-40px);
        opacity: 0;
      }}
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
      .article-section h2 {{
        font-size: 20px;
      }}
      .article-section p {{
        font-size: 16.5px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Reading Scroll Progress Bar -->
  <div id="readingProgress" class="reading-progress-bar" aria-hidden="true"></div>

  <!-- Navigation -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="{home_url}" class="brand-wrap" aria-label="{SITE_NAME} Home">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo" width="36" height="36">
        <div>
          <div class="brand-title">{SITE_NAME}</div>
          <div class="brand-tag">DISCOVER &amp; STORIES</div>
        </div>
      </a>
      <div class="nav-links">
        <a href="/about/" class="nav-link-item nav-link-desktop">{about_label}</a>
        <a href="/editorial/" class="nav-link-item nav-link-desktop">{editorial_label}</a>
        <a href="/contact/" class="nav-link-item nav-link-desktop">{contact_label}</a>
        {lang_switch_html}
        <a href="{discover_url}" class="nav-btn" aria-label="Chrome Discover Feed">{discover_btn_label}</a>
        <a href="{story_url}" class="nav-btn nav-btn-primary" aria-label="Watch AMP Story">{story_btn_label}</a>
      </div>
    </div>
  </nav>

  <!-- Main Article Body -->
  <main class="article-container">
    
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="{home_url}">{home_label}</a>
      <span>›</span>
      <a href="{discover_url}">{discover_label}</a>
      <span>›</span>
      <a href="{discover_url}?category={category}">{category_label}</a>
      <span>›</span>
      <span>{html.escape(movie_title)}</span>
    </div>

    <!-- Header Meta Badges -->
    <div class="article-header-meta">
      <span class="category-badge">{category_label}</span>
      <span class="read-time-pill">{read_time_label}</span>
      <span class="read-time-pill">📅 {date_display}</span>
    </div>

    <!-- Main Headline -->
    <h1 class="article-headline">{html.escape(headline)}</h1>

    <!-- Byline & Social Share -->
    <div class="byline-bar">
      <div class="author-info">
        <a href="/about/" class="author-avatar" title="CineStories Editorial Board" style="text-decoration: none;">EB</a>
        <div class="author-details">
          <h4>
            <a href="/about/" style="color: inherit; text-decoration: none;">CineStories Editorial Board</a>
            <span class="verified-badge" title="Verified Human Review" aria-label="Verified Human Review">✓</span>
          </h4>
          <p><a href="/editorial/" style="color: var(--text-muted); text-decoration: underline; text-decoration-color: rgba(255,255,255,0.2);">🛡️ {author_role}</a></p>
        </div>
      </div>
      <div class="share-actions">
        <a class="share-btn share-whatsapp" href="https://api.whatsapp.com/send?text={encoded_share_text}%20{encoded_url}" target="_blank" rel="noopener">💬 WhatsApp</a>
        <a class="share-btn share-pinterest" href="https://pinterest.com/pin/create/button/?url={encoded_url}&media={encoded_backdrop}&description={encoded_headline}" target="_blank" rel="noopener">📌 Pin</a>
        <a class="share-btn share-telegram" href="https://t.me/share/url?url={encoded_url}&text={encoded_share_text}" target="_blank" rel="noopener">✈️ Telegram</a>
        <a class="share-btn" href="https://twitter.com/intent/tweet?text={encoded_headline}&url={encoded_url}" target="_blank" rel="noopener">🐦 Tweet</a>
        <button class="share-btn" onclick="copyArticleLink()" aria-label="Copy article link to clipboard">{copy_share_label}</button>
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
        <h4>{story_callout_h4}</h4>
        <p>{story_callout_p}</p>
      </div>
      <a href="{story_url}" class="launch-story-btn">
        <span>{launch_story_btn_text}</span>
        <span>👉</span>
      </a>
    </div>

    <!-- Key Takeaways Box (Google Discover Engagement Booster) -->
    {takeaways_html}

    <!-- Human Editorial Audience Guide (E-E-A-T & Reader Value) -->
    {audience_guide_html}

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

    <!-- Viral Share Box (Drive High-Engagement Referral Loops) -->
    <div class="viral-share-box">
      <div class="viral-share-text">
        <h4>{viral_h4}</h4>
        <p>{viral_p}</p>
      </div>
      <div class="viral-share-btns">
        <a class="btn-share-wa" href="https://api.whatsapp.com/send?text={encoded_share_text}%20{encoded_url}" target="_blank" rel="noopener">
          <span>{wa_share_label}</span>
        </a>
        <a class="btn-share-pin" href="https://pinterest.com/pin/create/button/?url={encoded_url}&media={encoded_backdrop}&description={encoded_headline}" target="_blank" rel="noopener">
          <span>{pin_share_label}</span>
        </a>
        <a class="btn-share-tg" href="https://t.me/share/url?url={encoded_url}&text={encoded_share_text}" target="_blank" rel="noopener">
          <span>✈️ Telegram</span>
        </a>
      </div>
    </div>

    <!-- Related Articles -->
    {related_section}

  </main>

  <!-- Toast Notification & Celebratory Feedback -->
  <div id="toastNotification" class="toast-notification" role="status" aria-live="polite">
    <span>✨</span>
    <span>{toast_copy_msg}</span>
  </div>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-links" role="navigation" aria-label="Footer Navigation">
        <a href="{home_url}">{home_label}</a>
        <a href="{discover_url}">{discover_label}</a>
        <a href="/about/">{about_label}</a>
        <a href="/editorial/">{editorial_label}</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms of Service</a>
        <a href="/contact/">{contact_label}</a>
        <a href="/sitemap.xml">XML Sitemap</a>
      </div>
      <p>© {datetime.now(timezone.utc).year} {PUBLISHER_NAME}. Independent entertainment analysis. Movie metadata &amp; imagery powered by TMDB.</p>
    </div>
  </footer>

  <script>
    function copyArticleLink() {{
      var url = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(url).then(showToast).catch(function() {{ fallbackCopy(url); }});
      }} else {{
        fallbackCopy(url);
      }}
    }}
    function fallbackCopy(text) {{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {{
        document.execCommand('copy');
        showToast();
      }} catch (e) {{
        prompt('Copy link:', text);
      }}
      document.body.removeChild(ta);
    }}
    function showToast() {{
      var toast = document.getElementById('toastNotification');
      if (toast) {{
        toast.classList.add('show');
        celebrateSparkles();
        setTimeout(function() {{ toast.classList.remove('show'); }}, 3000);
      }}
    }}
    function celebrateSparkles() {{
      for (var i = 0; i < 12; i++) {{
        var s = document.createElement('div');
        s.className = 'sparkle-particle';
        s.style.left = (Math.random() * 80 + 10) + 'vw';
        s.style.top = (Math.random() * 60 + 20) + 'vh';
        s.style.backgroundColor = ['#e11d48', '#f59e0b', '#38bdf8', '#34d399'][Math.floor(Math.random() * 4)];
        document.body.appendChild(s);
        (function(el) {{
          setTimeout(function() {{ if (el.parentNode) el.parentNode.removeChild(el); }}, 800);
        }})(s);
      }}
    }}
    window.addEventListener('scroll', function() {{
      var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      var bar = document.getElementById("readingProgress");
      if (bar) bar.style.width = scrolled + "%";
    }}, {{ passive: true }});
  </script>

</body>
</html>
"""
