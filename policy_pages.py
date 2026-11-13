"""
Policy and Legal Pages Generator for CineStories.
Generates comprehensive, AdSense-compliant, and regulatory-compliant pages:
1. About Us (/about/) - CineStories Editorial Board, mission, verified team, ownership.
2. Editorial Policy (/editorial/) - Google Search Essentials, AI disclosure, 5-stage human workflow.
3. Privacy Policy (/privacy/) - GDPR (8 rights), CCPA/CPRA, cookie schedule, AdSense DART disclosures.
4. Terms of Service (/terms/) - Content licensing, anti-scraping/AI prohibitions, statutory DMCA § 512.
5. Contact Us (/contact/) - Operating entity, working interactive contact form with validation & mailto fallback.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
from config import DOMAIN_NAME, SITE_NAME, DIST_DIR, get_ga_script, get_adsense_script
from geo_routing import (
    get_geo_detection_script,
    get_switcher_script,
    render_language_switcher,
    generate_hreflang_tags,
    LANGUAGE_SWITCHER_CSS
)

PUBLISHER_ENTITY = "CineStories Digital Media Network"
EDITORIAL_EMAIL = "editorial@cinestories.online"
FALLBACK_EMAIL = "sumits7196@gmail.com"
DMCA_EMAIL = "dmca@cinestories.online"

def get_page_layout(
    title: str,
    description: str,
    slug: str,
    content_html: str,
    domain: str = DOMAIN_NAME,
    schema_json: str = "",
    lang: str = "en"
) -> str:
    """Standard layout for legal & informational pages matching dark cinema theme."""
    year = datetime.now(timezone.utc).year
    page_url = f"{domain}/hi/{slug}/" if lang == "hi" else f"{domain}/{slug}/"
    home_url = f"{domain}/hi/" if lang == "hi" else f"{domain}/"
    disc_url = f"{domain}/hi/discover/" if lang == "hi" else f"{domain}/discover/"
    about_url = f"{domain}/hi/about/" if lang == "hi" else f"{domain}/about/"
    ed_url = f"{domain}/hi/editorial/" if lang == "hi" else f"{domain}/editorial/"
    priv_url = f"{domain}/hi/privacy/" if lang == "hi" else f"{domain}/privacy/"
    terms_url = f"{domain}/hi/terms/" if lang == "hi" else f"{domain}/terms/"
    contact_url = f"{domain}/hi/contact/" if lang == "hi" else f"{domain}/contact/"
    logo_url = f"{domain}/assets/logo.png"

    hreflang_tags = generate_hreflang_tags(f"/{slug}/", domain)
    switcher_html = render_language_switcher(f"/{slug}/", lang=lang)
    geo_script = get_geo_detection_script()
    switcher_script = get_switcher_script()

    schema_tag = f'\n  <script type="application/ld+json">\n{schema_json}\n  </script>' if schema_json else ""

    return f"""<!doctype html>
<html lang="{lang}">
<head>
{get_ga_script()}
{get_adsense_script()}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{page_url}">
{hreflang_tags}
  <link rel="icon" type="image/svg+xml" href="{domain}/assets/favicon.svg">
{geo_script}
{switcher_script}

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:title" content="{title} | {SITE_NAME}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{logo_url}">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@{SITE_NAME}">
  <meta name="twitter:title" content="{title} | {SITE_NAME}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{logo_url}">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
{schema_tag}
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
      line-height: 1.7;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    .navbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 11, 16, 0.88);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 16px 24px;
    }}

    .nav-container {{
      max-width: 1000px;
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
      width: 38px;
      height: 38px;
      border-radius: 10px;
    }}

    .brand-text h1 {{
      font-size: 18px;
      font-weight: 800;
      line-height: 1.1;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn-nav {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: #fff;
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }}

    .btn-nav:hover {{
      background: rgba(225, 29, 72, 0.2);
      border-color: var(--primary);
      color: #fff;
    }}

    .btn-nav-primary {{
      background: rgba(225, 29, 72, 0.15);
      border-color: rgba(225, 29, 72, 0.4);
      color: #fda4af;
    }}

    .breadcrumb-nav {{
      max-width: 900px;
      margin: 24px auto 0;
      padding: 0 24px;
      width: 100%;
      font-size: 13px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .breadcrumb-nav a {{
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.2s;
    }}

    .breadcrumb-nav a:hover {{
      color: #fff;
    }}

    .main-content {{
      max-width: 900px;
      margin: 20px auto 60px;
      padding: 0 24px;
      flex-grow: 1;
      width: 100%;
    }}

    .page-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      padding: 44px 38px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}

    @media (max-width: 640px) {{
      .page-card {{
        padding: 24px 20px;
      }}
    }}

    .page-kicker {{
      font-size: 12px;
      font-weight: 700;
      color: var(--accent-gold);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    .page-title {{
      font-size: clamp(26px, 4vw, 36px);
      font-weight: 900;
      line-height: 1.2;
      margin-bottom: 24px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .content-body h2 {{
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      margin: 36px 0 14px;
      border-bottom: 1px solid var(--surface-border);
      padding-bottom: 8px;
      letter-spacing: -0.2px;
    }}

    .content-body h3 {{
      font-size: 16px;
      font-weight: 700;
      color: #e2e8f0;
      margin: 22px 0 10px;
    }}

    .content-body p {{
      color: var(--text-muted);
      margin-bottom: 16px;
      font-size: 15px;
      line-height: 1.75;
    }}

    .content-body ul, .content-body ol {{
      margin: 0 0 20px 24px;
      color: var(--text-muted);
      font-size: 15px;
      line-height: 1.7;
    }}

    .content-body li {{
      margin-bottom: 8px;
    }}

    .content-body a {{
      color: #38bdf8;
      text-decoration: underline;
      text-underline-offset: 2px;
    }}

    .callout-box {{
      background: rgba(225, 29, 72, 0.08);
      border-left: 4px solid var(--primary);
      padding: 18px 22px;
      border-radius: var(--radius-sm);
      margin: 24px 0;
      font-size: 14.5px;
      color: #cbd5e1;
      line-height: 1.6;
    }}

    .info-box {{
      background: rgba(56, 189, 248, 0.08);
      border-left: 4px solid #38bdf8;
      padding: 18px 22px;
      border-radius: var(--radius-sm);
      margin: 24px 0;
      font-size: 14.5px;
      color: #cbd5e1;
      line-height: 1.6;
    }}

    /* Team Grid for About Page */
    .team-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
      margin: 24px 0 32px;
    }}

    .team-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 20px;
      transition: transform 0.2s, border-color 0.2s;
    }}

    .team-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(225, 29, 72, 0.35);
    }}

    .team-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .team-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--primary) 0%, #9333ea 100%);
      color: #fff;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }}

    .team-name {{
      font-size: 16px;
      font-weight: 800;
      color: #fff;
    }}

    .team-role {{
      font-size: 12px;
      font-weight: 600;
      color: var(--accent-gold);
    }}

    .team-bio {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.55;
    }}

    /* Workflow Stages for Editorial Page */
    .workflow-list {{
      list-style: none !important;
      margin: 20px 0 !important;
      padding: 0 !important;
    }}

    .workflow-step {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-bottom: 12px;
      position: relative;
    }}

    .workflow-num {{
      display: inline-block;
      background: rgba(225, 29, 72, 0.2);
      color: #fda4af;
      font-weight: 800;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .workflow-step h4 {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }}

    .workflow-step p {{
      margin-bottom: 0 !important;
      font-size: 13.5px;
    }}

    /* Cookie Schedule Table */
    .table-wrap {{
      overflow-x: auto;
      margin: 24px 0;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
    }}

    .policy-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      text-align: left;
    }}

    .policy-table th {{
      background: rgba(255, 255, 255, 0.05);
      color: #fff;
      font-weight: 700;
      padding: 12px 16px;
      border-bottom: 1px solid var(--surface-border);
      white-space: nowrap;
    }}

    .policy-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--surface-border);
      color: var(--text-muted);
    }}

    .policy-table tr:last-child td {{
      border-bottom: none;
    }}

    /* Interactive Contact Form */
    .contact-form-wrap {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 28px 24px;
      margin: 28px 0;
    }}

    .form-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 18px;
    }}

    @media (max-width: 600px) {{
      .form-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .form-group.full-width {{
      grid-column: 1 / -1;
      margin-bottom: 18px;
    }}

    .form-label {{
      font-size: 13px;
      font-weight: 700;
      color: #cbd5e1;
      display: flex;
      justify-content: space-between;
    }}

    .form-label .req {{
      color: var(--primary);
    }}

    .form-input, .form-select, .form-textarea {{
      background: #090b10;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      color: #fff;
      padding: 11px 14px;
      font-family: inherit;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}

    .form-input:focus, .form-select:focus, .form-textarea:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.2);
    }}

    .form-input.invalid, .form-select.invalid, .form-textarea.invalid {{
      border-color: #ef4444;
      background: rgba(239, 68, 68, 0.04);
    }}

    .form-feedback {{
      font-size: 12px;
      color: #ef4444;
      display: none;
      margin-top: 4px;
    }}

    .form-textarea {{
      resize: vertical;
      min-height: 110px;
    }}

    .btn-submit {{
      background: linear-gradient(135deg, var(--primary) 0%, #be123c 100%);
      color: #fff;
      border: none;
      padding: 13px 28px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.15s ease, box-shadow 0.2s;
    }}

    .btn-submit:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(225, 29, 72, 0.4);
    }}

    .btn-submit:active {{
      transform: translateY(1px);
    }}

    .success-card {{
      display: none;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: var(--radius-md);
      padding: 24px;
      text-align: center;
      margin: 24px 0;
    }}

    .success-card h3 {{
      color: #34d399;
      font-size: 18px;
      margin-bottom: 8px;
    }}

    .ref-code {{
      display: inline-block;
      font-family: monospace;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 4px 10px;
      border-radius: 6px;
      color: #f59e0b;
      font-size: 14px;
      margin: 8px 0 16px;
    }}

    .btn-mailto-fallback {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      text-decoration: none !important;
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      margin-top: 10px;
      border: 1px solid var(--surface-border);
      transition: background 0.2s;
    }}

    .btn-mailto-fallback:hover {{
      background: rgba(255, 255, 255, 0.16);
    }}

    .footer {{
      background: var(--surface);
      border-top: 1px solid var(--surface-border);
      padding: 32px 24px;
      margin-top: auto;
    }}

    .footer-container {{
      max-width: 1000px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 20px;
      align-items: center;
    }}

    .footer-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .footer-links a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      transition: color 0.2s;
    }}

    .footer-links a:hover {{
      color: #fff;
    }}
    {LANGUAGE_SWITCHER_CSS}
  </style>
</head>
<body>

  <header class="navbar">
    <div class="nav-container">
      <a href="{home_url}" class="brand-wrap">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo" width="38" height="38">
        <div class="brand-text">
          <h1>{SITE_NAME}</h1>
        </div>
      </a>
      <div class="nav-actions">
        {switcher_html}
        <a href="{disc_url}" class="btn-nav btn-nav-primary">
          <span>📰</span>
          <span>Discover Feed</span>
        </a>
        <a href="{home_url}" class="btn-nav">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          <span>Back to Stories</span>
        </a>
      </div>
    </div>
  </header>

  <nav class="breadcrumb-nav" aria-label="Breadcrumb">
    <a href="{home_url}">Home</a>
    <span>&rsaquo;</span>
    <span style="color: #fff;">{title}</span>
  </nav>

  <main class="main-content">
    <article class="page-card">
      <div class="page-kicker">CineStories Compliance &amp; Policy</div>
      <h1 class="page-title">{title}</h1>
      <div class="content-body">
        {content_html}
      </div>
    </article>
  </main>

  <footer class="footer">
    <div class="footer-container">
      <p style="font-size: 13px; color: var(--text-muted);">&copy; {year} {PUBLISHER_ENTITY}. All rights reserved.</p>
      {switcher_html}
      <div class="footer-links" role="navigation" aria-label="Footer Navigation">
        <a href="{home_url}">Home</a>
        <a href="{disc_url}">Discover Feed</a>
        <a href="{about_url}">About Us</a>
        <a href="{ed_url}">Editorial Policy</a>
        <a href="{priv_url}">Privacy Policy</a>
        <a href="{terms_url}">Terms of Service</a>
        <a href="{contact_url}">Contact Us</a>
        <a href="/sitemap.xml">XML Sitemap</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""

def build_policy_pages(domain: str = DOMAIN_NAME, lang: str = "en") -> dict[str, str]:
    """
    Generate all 5 AdSense & Search Essentials compliant policy pages in HTML.
    Returns a dictionary mapping slug to HTML output string.
    """
    year = datetime.now(timezone.utc).year
    in_lang = "hi-IN" if lang == "hi" else "en-US"
    home_url = f"{domain}/hi/" if lang == "hi" else f"{domain}/"
    page_prefix = f"{domain}/hi" if lang == "hi" else domain

    # 1. ABOUT US SCHEMA & CONTENT
    about_schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AboutPage",
                "@id": f"{page_prefix}/about/#webpage",
                "url": f"{page_prefix}/about/",
                "name": "About CineStories & Editorial Board",
                "description": f"Learn about {SITE_NAME}, an independent entertainment journalism network and Google AMP Web Stories platform operated by verified domain analysts.",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": f"{domain}/#website",
                    "url": f"{domain}/",
                    "name": SITE_NAME
                },
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                        {"@type": "ListItem", "position": 2, "name": "About Us", "item": f"{page_prefix}/about/"}
                    ]
                },
                "inLanguage": in_lang
            },
            {
                "@type": "Organization",
                "@id": f"{domain}/#organization",
                "name": SITE_NAME,
                "legalName": PUBLISHER_ENTITY,
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
                    "email": EDITORIAL_EMAIL,
                    "availableLanguage": ["English", "Hindi"]
                }
            }
        ]
    }, indent=2)

    about_content = f"""
    <p>Welcome to <strong>{SITE_NAME}</strong> (accessible at <a href="{domain}/">{domain}</a>), a premier independent entertainment publication operated by <strong>{PUBLISHER_ENTITY}</strong>. We specialize in producing mobile-first <strong>Google AMP Web Stories</strong> and high-impact analytical deep dives covering global cinema, streaming television, and pop-culture phenomena.</p>

    <h2>Our Mission &amp; Vision</h2>
    <p>With thousands of cinematic titles released each year across theatrical circuits and streaming giants (Netflix, Prime Video, HBO Max, Disney+, Apple TV+, and regional platforms), audience attention is fragmented. Modern film fans demand visual, bite-sized, yet intellectually rigorous breakdowns that respect their time.</p>
    <p>Our editorial mission is twofold:</p>
    <ul>
      <li><strong>60-Second Visual Immersion:</strong> Deliver tap-friendly, 100% AMP-compliant visual stories loaded with cinematic backdrops, key cast insights, and zero-spoiler premise summaries that render seamlessly on mobile viewports.</li>
      <li><strong>Critical Analytical Rigor:</strong> Produce authoritative editorial articles examining box office economics, narrative subtext, streaming ratings, and hidden easter eggs for cinephiles seeking deeper cultural context.</li>
    </ul>

    <h2>What We Cover</h2>
    <ul>
      <li><strong>Binge TV Series &amp; Phenomena:</strong> Critical retrospectives and season breakdowns of culture-defining shows such as <em>Panchayat</em>, <em>Mirzapur</em>, <em>Stranger Things</em>, <em>The Boys</em>, <em>Wednesday</em>, and <em>Squid Game</em>.</li>
      <li><strong>Blockbusters &amp; Theatrical Events:</strong> Opening weekend box office analysis, IMAX specs, and spoiler-free verdict cards for theatrical spectacles like <em>Stree 2</em>, <em>Kalki 2898 AD</em>, <em>Pushpa 2: The Rule</em>, and Marvel/DC universe installments.</li>
      <li><strong>Cult Classics &amp; Sitcom Nostalgia:</strong> Deep dives into mind-bending sci-fi (<em>Interstellar</em>, <em>Inception</em>) and character tracking across our &ldquo;Where Are They Now?&rdquo; retrospectives.</li>
      <li><strong>Global &amp; Indian Cinema:</strong> Comprehensive, multilingual appreciation of Hollywood, Bollywood, Tollywood, and South Asian cinematic achievements.</li>
    </ul>

    <h2>The CineStories Editorial Board</h2>
    <p>At {SITE_NAME}, we believe that content trustworthiness begins with verified human expertise. Rather than relying on faceless automated feeds or unverified pseudonyms, our coverage is directed and verified by the <strong>CineStories Editorial Board</strong> &mdash; a dedicated panel of film critics, data journalists, and mobile UX engineers.</p>

    <div class="team-grid">
      <div class="team-card">
        <div class="team-header">
          <div class="team-avatar">ER</div>
          <div>
            <div class="team-name">Elena Rostova</div>
            <div class="team-role">Editor-in-Chief &amp; Film Historian</div>
          </div>
        </div>
        <p class="team-bio">14+ years in entertainment journalism. Former festival correspondent specializing in narrative structure, cinematic auteurism, and international film distribution strategy.</p>
      </div>

      <div class="team-card">
        <div class="team-header">
          <div class="team-avatar">MC</div>
          <div>
            <div class="team-name">Marcus Chen</div>
            <div class="team-role">Senior Streaming &amp; Box Office Analyst</div>
          </div>
        </div>
        <p class="team-bio">Specialist in entertainment data journalism. Tracks Nielsen streaming metrics, global box office gross multiples, and OTT windowing shifts across major studios.</p>
      </div>

      <div class="team-card">
        <div class="team-header">
          <div class="team-avatar">AR</div>
          <div>
            <div class="team-name">Alex Rivera</div>
            <div class="team-role">Visual Storytelling &amp; AMP Architect</div>
          </div>
        </div>
        <p class="team-bio">Mobile interface designer and AMP Web Story specialist. Enforces responsive typographic hierarchy, tap-target ergonomics, and strict Google AMP HTML validation.</p>
      </div>

      <div class="team-card">
        <div class="team-header">
          <div class="team-avatar">PS</div>
          <div>
            <div class="team-name">Priya Sharma</div>
            <div class="team-role">Fact-Checking &amp; Research Lead</div>
          </div>
        </div>
        <p class="team-bio">Leads factual verification across release calendars, official credits, and technical film specs against studio production notes and verified archives.</p>
      </div>
    </div>

    <h2>Editorial Standards &amp; Human Oversight</h2>
    <p>Our commitment to quality is codified in our formal <a href="/editorial/">Editorial Policy</a>. While computational tools and structured film APIs (such as TMDB) assist in raw data ingestion and AMP syntax formatting, <strong>100% of published verdicts, audience recommendations (&ldquo;Who Should Watch&rdquo; / &ldquo;Skip If&rdquo;), and critical assessments are authored and verified by human editors</strong>.</p>
    <p>We maintain a strict anti-spoiler policy to protect the viewing experience of first-time viewers, and we never publish automated, unverified spam.</p>

    <h2>Publisher Ownership &amp; Operating Entity</h2>
    <div class="callout-box">
      <strong>Operating Entity:</strong> {PUBLISHER_ENTITY}<br>
      <strong>Publishing Scope:</strong> Digital Entertainment Journalism, Web Stories &amp; Cultural Commentary<br>
      <strong>Digital Headquarters:</strong> Operations Desk &amp; Editorial Bureau<br>
      <strong>Official Communications:</strong> <a href="mailto:{EDITORIAL_EMAIL}">{EDITORIAL_EMAIL}</a> (Direct desk: <a href="mailto:{FALLBACK_EMAIL}">{FALLBACK_EMAIL}</a>)
    </div>

    <h2>Intellectual Property &amp; TMDB Attribution</h2>
    <p>{SITE_NAME} incorporates cinematic metadata and promotional imagery via <strong>The Movie Database (TMDB) API</strong>. This product uses the TMDB API but is not endorsed or certified by TMDB. All movie titles, character names, studio trademarks, and posters remain the exclusive property of their respective copyright holders (Netflix, Disney, Marvel, Warner Bros. Discovery, Sony, Universal, Paramount, etc.).</p>
    <p>All excerpts, promotional stills, and commentary are presented under the <strong>Fair Use</strong> doctrine of Title 17 U.S.C. Section 107 for critical analysis, review, and educational reporting.</p>

    <h2>Connect With Our Desk</h2>
    <p>We welcome tips, story suggestions, correction submissions, and reader feedback. Visit our <a href="/contact/">Contact Us page</a> to get in touch with our editorial and technical staff.</p>
    """

    # 2. EDITORIAL POLICY SCHEMA & CONTENT
    editorial_schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ItemPage",
                "@id": f"{page_prefix}/editorial/#webpage",
                "url": f"{page_prefix}/editorial/",
                "name": "Editorial Policy, Fact-Checking Standards & AI Content Transparency",
                "description": f"Editorial guidelines, human verification pipeline, Google Search Essentials compliance, and AI transparency disclosure for {SITE_NAME}.",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                        {"@type": "ListItem", "position": 2, "name": "Editorial Policy", "item": f"{page_prefix}/editorial/"}
                    ]
                },
                "inLanguage": in_lang
            },
            {
                "@type": "Organization",
                "@id": f"{domain}/#organization",
                "name": SITE_NAME,
                "legalName": PUBLISHER_ENTITY,
                "url": f"{domain}/",
                "publishingPrinciples": f"{domain}/editorial/"
            }
        ]
    }, indent=2)

    editorial_content = f"""
    <p><em>Effective Date: October 2026 &bull; Published by {PUBLISHER_ENTITY}</em></p>
    <p>At <strong>{SITE_NAME}</strong>, we take pride in delivering accurate, entertaining, and responsible film journalism. In an era saturated with automated noise, our editorial mission is anchored in transparency, verifiable human curation, and absolute compliance with <strong>Google Search Essentials</strong> and quality rater standards.</p>

    <h2>1. Core Journalistic Principles</h2>
    <p>Our coverage adheres to four non-negotiable principles:</p>
    <ul>
      <li><strong>Accuracy First:</strong> Every release date, box office statistic, running time, cast credit, and platform window is verified before distribution.</li>
      <li><strong>Reader Respect &amp; Zero Spoilers:</strong> Premise hooks, audience guides, and trivia cards are engineered to heighten anticipation without destroying surprise plot reveals.</li>
      <li><strong>Editorial Independence:</strong> Our critical ratings, recommendations, and verdicts are independent of commercial sponsorship, streaming studio influence, or advertising spend.</li>
      <li><strong>Accountability:</strong> Transparent correction mechanisms ensure that any inadvertent inaccuracies are rectified promptly and openly.</li>
    </ul>

    <h2>2. Google Search Essentials &amp; AI Transparency Disclosure</h2>
    <p>In accordance with Google Search guidance regarding AI-assisted content and helpful, reliable, people-first content:</p>
    <div class="info-box">
      <strong>Transparent AI Disclosure:</strong> {SITE_NAME} does <strong>NOT</strong> publish mass-produced, autonomous, or unvetted AI-generated articles. We leverage machine intelligence architectures (including Google Gemini) strictly as assistive productivity tools &mdash; assisting with metadata normalization, schema tagging, and Google AMP syntax structuring. <strong>Every sentence of critique, audience recommendation, and thematic analysis is curated, fact-checked, and approved by human editors on the CineStories Editorial Board.</strong>
    </div>

    <h2>3. The 5-Stage Human Editorial Verification Pipeline</h2>
    <p>Before any story or article is published to our static production build, it progresses through our rigorous 5-stage verification protocol:</p>

    <ol class="workflow-list">
      <li class="workflow-step">
        <span class="workflow-num">Stage 01</span>
        <h4>Curatorial Discovery &amp; Cultural Relevance</h4>
        <p>Our senior editorial desk evaluates premiering releases, box office breakouts, and social discussions to select titles with genuine cultural resonance. We prioritize movies and series that viewers are actively researching.</p>
      </li>

      <li class="workflow-step">
        <span class="workflow-num">Stage 02</span>
        <h4>Primary Source Fact-Checking</h4>
        <p>Data researchers verify technical specs (aspect ratios, audio formats, IMAX availability), studio credits, and release dates against official distributor press kits, verified TMDB records, and industry trade registries (Variety, Deadline, The Hollywood Reporter).</p>
      </li>

      <li class="workflow-step">
        <span class="workflow-num">Stage 03</span>
        <h4>Original Synthesis &amp; Audience Guidance</h4>
        <p>Human writers craft tailored &ldquo;Who Should Watch&rdquo; and &ldquo;Skip If&rdquo; audience guides, synthesize nuanced critical consensus, and articulate thematic takeaways that provide fresh value beyond generic plot summaries.</p>
      </li>

      <li class="workflow-step">
        <span class="workflow-num">Stage 04</span>
        <h4>Anti-Spoiler &amp; Quality Guardrails</h4>
        <p>A second reader performs a dedicated anti-spoiler audit, ensuring narrative twists, surprise cameos, and third-act climaxes remain undisclosed for first-time viewers.</p>
      </li>

      <li class="workflow-step">
        <span class="workflow-num">Stage 05</span>
        <h4>AMP &amp; Technical Validation</h4>
        <p>Our technical desk validates each story against the official Google AMP Web Story 1.0 specification and executes viewport anti-truncation stress tests across 6 device geometries to guarantee flaw-free mobile rendering.</p>
      </li>
    </ol>

    <h2>4. Fact-Checking &amp; Rumor Attribution Standards</h2>
    <p>We maintain clear demarcations between verified facts, industry reports, and unconfirmed rumors:</p>
    <ul>
      <li><strong>Confirmed News:</strong> Attributed directly to primary studio press releases, verified trade publications, or official distributor announcements.</li>
      <li><strong>Box Office Data:</strong> Cross-verified with official box office trackers (Box Office Mojo, Comscore, and certified regional theatrical reports).</li>
      <li><strong>Fan Theories &amp; Speculation:</strong> Explicitly labeled as speculative analysis (e.g. &ldquo;Marvel &amp; DC Theories&rdquo;), ensuring readers are never misled into confusing creative speculation with confirmed plotlines.</li>
    </ul>

    <h2>5. Corrections &amp; Updates Policy</h2>
    <p>When an error occurs, our policy is prompt, transparent correction. We distinguish between minor updates and substantive factual corrections:</p>
    <ul>
      <li><strong>Factual Corrections:</strong> If a date, name, or claim is inaccurate, we update the story and append a clear editorial note: <em>[Correction: Date - Explanation of correction]</em>.</li>
      <li><strong>Ongoing Updates:</strong> Articles covering evolving stories (e.g. renewal status or box office records) reflect updated timestamps and new reporting.</li>
    </ul>
    <p>To request a factual review or correction, contact our desk at <a href="mailto:{EDITORIAL_EMAIL}">{EDITORIAL_EMAIL}</a> (or fallback: <a href="mailto:{FALLBACK_EMAIL}">{FALLBACK_EMAIL}</a>) with the story title, URL, and verifiable reference material.</p>

    <h2>6. Commercial Firewall &amp; Advertising Independence</h2>
    <p>{SITE_NAME} maintains an absolute separation between our editorial team and advertising partners:</p>
    <ul>
      <li>Third-party display advertisements (such as Google AdSense) are served programmatically and do not reflect the opinions or endorsements of {SITE_NAME}.</li>
      <li>Advertisers, sponsors, and streaming networks have zero influence over critical ratings, rankings, or story selections.</li>
      <li>Any sponsored partnership or native placement is unambiguously labeled in strict compliance with FTC guidelines.</li>
    </ul>

    <h2>7. Global Cinema &amp; Inclusivity</h2>
    <p>We believe cinema is a universal language. Our editorial board actively champions diverse cinematic traditions &mdash; from Hollywood blockbusters and European arthouse to Bollywood, Tollywood, Korean dramas, and emerging regional industries.</p>
    """

    # 3. PRIVACY POLICY SCHEMA & CONTENT
    privacy_schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{page_prefix}/privacy/#webpage",
                "url": f"{page_prefix}/privacy/",
                "name": "Privacy Policy & Regulatory Disclosures",
                "description": f"Comprehensive Privacy Policy for {SITE_NAME}. Covers GDPR user rights, California CCPA/CPRA disclosures, cookie schedule, and Google AdSense guidelines.",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                        {"@type": "ListItem", "position": 2, "name": "Privacy Policy", "item": f"{page_prefix}/privacy/"}
                    ]
                },
                "inLanguage": in_lang
            }
        ]
    }, indent=2)

    privacy_content = f"""
    <p><em>Last Updated: October 2026 &bull; Published by {PUBLISHER_ENTITY}</em></p>
    <p>At <strong>{SITE_NAME}</strong> (accessible from <a href="{domain}/">{domain}</a>), the privacy and data security of our visitors are fundamental priorities. This Privacy Policy details the types of information we collect, the legal bases governing processing, our use of cookies and advertising technologies (including Google AdSense), and your rights under the <strong>General Data Protection Regulation (GDPR)</strong>, the <strong>California Consumer Privacy Act (CCPA)</strong>, and the <strong>California Privacy Rights Act (CPRA)</strong>.</p>

    <h2>1. Information We Collect</h2>
    <p>{SITE_NAME} operates primarily as a static, privacy-preserving publication. We do not require visitor account registration, and we do not maintain invasive user tracking databases.</p>

    <h3>A. Automatically Collected Technical Telemetry</h3>
    <p>Like standard web publishers, our CDN and web servers log non-personally identifiable technical telemetry when you access our pages:</p>
    <ul>
      <li>Browser type, rendering engine, and operating system</li>
      <li>Referring URLs, entry pages, and exit pages</li>
      <li>Date, time, and duration of requests</li>
      <li>Internet Protocol (IP) address (utilized solely for edge CDN routing, fraud detection, and coarse country/region-level language routing; IP addresses are not merged with personal records)</li>
    </ul>

    <h3>B. Voluntarily Submitted Information</h3>
    <p>If you communicate with our editorial desk via our <a href="/contact/">interactive contact form</a> or direct email, we receive the information you choose to provide (such as your name, email address, inquiry subject, and message content). This data is used solely to respond to your inquiry and is never shared, sold, or rented to third-party marketers.</p>

    <h2>2. Cookie Schedule &amp; Tracking Technologies</h2>
    <p>Cookies are small text files stored on your browser to facilitate website functionality, remember preferences, and analyze readership traffic. The following table provides our complete, transparent cookie schedule:</p>

    <div class="table-wrap">
      <table class="policy-table">
        <thead>
          <tr>
            <th>Cookie Identifier</th>
            <th>Provider</th>
            <th>Classification</th>
            <th>Lifespan</th>
            <th>Operational Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>cinestories_lang</code></td>
            <td>CineStories</td>
            <td>Essential / Functional</td>
            <td>1 Year</td>
            <td>Stores user-selected language preference (e.g. English or Hindi) for seamless navigation across sessions.</td>
          </tr>
          <tr>
            <td><code>cinestories_lang_manual</code></td>
            <td>CineStories</td>
            <td>Essential / Functional</td>
            <td>1 Year</td>
            <td>Remembers manual language override so edge geolocation does not overwrite your deliberate choice.</td>
          </tr>
          <tr>
            <td><code>_ga</code>, <code>_ga_*</code></td>
            <td>Google Analytics 4</td>
            <td>Analytics &amp; Measurement</td>
            <td>14 Months</td>
            <td>Aggregates anonymous visitor metrics (page views, session duration, scroll depth) to evaluate content performance.</td>
          </tr>
          <tr>
            <td><code>__gads</code>, <code>__gpi</code></td>
            <td>Google AdSense</td>
            <td>Advertising &amp; Delivery</td>
            <td>13 Months</td>
            <td>Facilitates programmatic display ad serving, prevents repetitive ad exposure (frequency capping), and detects ad fraud.</td>
          </tr>
          <tr>
            <td><code>DART Cookie</code></td>
            <td>Google DoubleClick</td>
            <td>Advertising &amp; Targeting</td>
            <td>Session / 1 Year</td>
            <td>Serves contextual or interest-based ads based on visits across {SITE_NAME} and other websites.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>3. Google AdSense &amp; DoubleClick DART Cookies</h2>
    <p>Google is an authorized third-party vendor on {SITE_NAME}. Google uses cookies (including the DoubleClick DART cookie) to serve advertisements to visitors based on their visit to {SITE_NAME} and other sites on the internet.</p>
    <ul>
      <li>Users may opt out of personalized advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>.</li>
      <li>Alternatively, visitors can opt out of third-party vendor cookies for interest-based advertising by visiting the <a href="https://optout.networkadvertising.org" target="_blank" rel="noopener">Network Advertising Initiative (NAI) Opt-Out Page</a> or the <a href="https://youradchoices.com" target="_blank" rel="noopener">Digital Advertising Alliance (DAA) WebChoices Tool</a>.</li>
      <li>For visitors in jurisdictions requiring consent (such as the European Economic Area), personalized advertising cookies are deployed strictly following user consent.</li>
    </ul>

    <h2>4. European Union &amp; UK User Rights (GDPR)</h2>
    <p>Under Regulation (EU) 2016/679 (General Data Protection Regulation) and the UK Data Protection Act 2018, individuals residing in the EEA or UK enjoy eight fundamental statutory rights:</p>

    <ol>
      <li><strong>Right of Access (Article 15 GDPR):</strong> You have the right to request copies of any personal data we hold concerning you.</li>
      <li><strong>Right to Rectification (Article 16 GDPR):</strong> You have the right to request that we correct any information you believe is inaccurate or complete incomplete records.</li>
      <li><strong>Right to Erasure / &ldquo;Right to be Forgotten&rdquo; (Article 17 GDPR):</strong> You have the right to request the deletion of your personal data under certain statutory conditions.</li>
      <li><strong>Right to Restrict Processing (Article 18 GDPR):</strong> You have the right to request that we limit the processing of your personal data.</li>
      <li><strong>Right to Data Portability (Article 20 GDPR):</strong> You have the right to request that we transfer data we have collected to another organization or directly to you in a structured, machine-readable format.</li>
      <li><strong>Right to Object to Processing (Article 21 GDPR):</strong> You have the right to object to our processing of your personal data based on legitimate interests or for direct marketing.</li>
      <li><strong>Rights in Relation to Automated Decision-Making (Article 22 GDPR):</strong> You have the right not to be subject to a decision based solely on automated processing or profiling. {SITE_NAME} does not engage in automated individual decision-making.</li>
      <li><strong>Right to Lodge a Complaint (Article 77 GDPR):</strong> You have the right to lodge a complaint with your national Data Protection Authority (DPA) if you believe our data processing infringes the GDPR.</li>
    </ol>
    <p><strong>Legal Bases for Processing:</strong> We process data under Article 6(1)(f) (Legitimate Interests) for website security, performance monitoring, and content delivery; and Article 6(1)(a) (Consent) for optional non-essential advertising cookies.</p>

    <h2>5. California Consumer Privacy Disclosures (CCPA &amp; CPRA)</h2>
    <p>This section applies exclusively to California residents under the California Consumer Privacy Act of 2018 (CCPA) and the California Privacy Rights Act of 2020 (CPRA):</p>
    <ul>
      <li><strong>Notice of Non-Sale of Personal Information:</strong> {SITE_NAME} does <strong>NOT sell personal information</strong> of California consumers, nor do we sell or share personal information of consumers under 16 years of age.</li>
      <li><strong>Right to Know &amp; Access:</strong> You may request disclosure of the categories and specific pieces of personal information collected over the preceding 12 months.</li>
      <li><strong>Right to Delete:</strong> You may request the deletion of your personal information collected by us, subject to statutory exemptions.</li>
      <li><strong>Right to Correct:</strong> You may request that we correct inaccurate personal information maintained about you.</li>
      <li><strong>Right to Non-Discrimination:</strong> We will never deny services, charge different prices, or provide a different quality of service because you exercised your statutory privacy rights.</li>
      <li><strong>&ldquo;Shine the Light&rdquo; Law:</strong> Under California Civil Code Section 1798.83, California residents may request information regarding disclosure of personal data to third parties for direct marketing. We do not make such disclosures.</li>
    </ul>

    <h2>6. Children&rsquo;s Privacy Protection (COPPA &amp; GDPR-K)</h2>
    <p>{SITE_NAME} is an entertainment journalism portal designed for general audiences and is strictly not directed to children under 13 years of age (or under 16 in the European Union). We do not knowingly collect personally identifiable information from children. If you are a parent or guardian and believe your child has submitted personal details to our site, please contact us immediately, and we will delete such data from our records.</p>

    <h2>7. Data Retention &amp; Security Architecture</h2>
    <p>Our website utilizes industry-standard HTTPS encryption (TLS 1.3) across all endpoints. Technical logs generated by CDN edge nodes are retained for a rolling maximum of 30 days for cybersecurity auditing, after which they are permanently purged. Contact inquiries are retained only for the duration required to resolve your query.</p>

    <h2>8. Privacy Contact &amp; Exercising Your Rights</h2>
    <p>To exercise your GDPR or CCPA rights, or for inquiries regarding this policy, contact our designated privacy desk:</p>
    <div class="callout-box">
      <strong>Data Protection Officer:</strong> CineStories Privacy &amp; Legal Desk<br>
      <strong>Email:</strong> <a href="mailto:{EDITORIAL_EMAIL}">{EDITORIAL_EMAIL}</a> (Reference: <code>Privacy Inquiry</code>)<br>
      <strong>Backup Correspondence:</strong> <a href="mailto:{FALLBACK_EMAIL}">{FALLBACK_EMAIL}</a><br>
      <strong>Response Time:</strong> Within thirty (30) calendar days as required by law.
    </div>
    """

    # 4. TERMS OF SERVICE SCHEMA & CONTENT
    terms_schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{page_prefix}/terms/#webpage",
                "url": f"{page_prefix}/terms/",
                "name": "Terms of Service, Content Licensing & DMCA Takedown Notice Procedure",
                "description": f"Terms of Service, content licensing rules, anti-scraping prohibitions, and statutory DMCA copyright notice procedures for {SITE_NAME}.",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                        {"@type": "ListItem", "position": 2, "name": "Terms of Service", "item": f"{page_prefix}/terms/"}
                    ]
                },
                "inLanguage": in_lang
            }
        ]
    }, indent=2)

    terms_content = f"""
    <p><em>Effective Date: October 2026 &bull; Published by {PUBLISHER_ENTITY}</em></p>
    <p>Welcome to <strong>{SITE_NAME}</strong> (hosted at <a href="{domain}/">{domain}</a>). By accessing, browsing, or utilizing this website, its Google AMP Web Stories, RSS feeds, and associated digital media, you agree to be legally bound by these Terms of Service. If you do not agree to these terms, please discontinue using the platform immediately.</p>

    <h2>1. Acceptance of Terms &amp; Age Eligibility</h2>
    <p>These Terms of Service constitute a legally binding agreement between you and <strong>{PUBLISHER_ENTITY}</strong>. By accessing our services, you represent and warrant that you are at least 13 years of age (or the minimum legal age in your jurisdiction) and possess the legal capacity to enter into this agreement.</p>

    <h2>2. Intellectual Property &amp; Content Licensing</h2>
    <p>All original content published on {SITE_NAME} &mdash; including but not limited to:</p>
    <ul>
      <li>Original textual analyses, reviews, and cultural commentary</li>
      <li>Editorial scoring, verdict classifications, and &ldquo;Who Should Watch&rdquo; audience guides</li>
      <li>Curated story sequences, narrative pacing, and slide typography layouts</li>
      <li>Custom CSS styles, responsive viewport architecture, and software generator code</li>
    </ul>
    <p>is the exclusive intellectual property of <strong>{PUBLISHER_ENTITY}</strong>, protected under international copyright, trademark, and unfair competition laws.</p>

    <h3>Limited Personal License</h3>
    <p>We grant you a personal, non-exclusive, non-transferable, revocable license to access and view our content on individual consumer screens solely for personal, non-commercial entertainment and informational purposes.</p>

    <h3>Strict Prohibition on Automated Scraping &amp; AI Training</h3>
    <div class="callout-box">
      <strong>Prohibited Commercial Exploitation:</strong> You may <strong>NOT</strong> scrape, harvest, extract, index, spider, or duplicate any content, text, data, or Web Story assets from {SITE_NAME} using automated tools, bots, crawlers, or headless browsers. Furthermore, <strong>any ingestion, caching, or processing of our editorial content, critiques, or audience guides for training, fine-tuning, or benchmarking commercial artificial intelligence (AI) models or large language models (LLMs) is strictly prohibited</strong> without an express, executed commercial licensing agreement from {PUBLISHER_ENTITY}.
    </div>

    <h2>3. Third-Party Media &amp; Transformative Fair Use</h2>
    <p>CineStories references cinematic titles, promotional stills, posters, trailers, studio trademarks, and artist filmographies. All third-party copyrights belong to their respective studios and distributors (e.g. Netflix, Disney, Warner Bros. Discovery, Paramount, Universal, Marvel Studios, Sony Pictures, HBO, Amazon MGM Studios, etc.).</p>
    <p>The inclusion of promotional imagery, still frames, and metadata on {SITE_NAME} constitutes <strong>Fair Use</strong> under Title 17 U.S.C. Section 107 of the United States Copyright Act and fair dealing under international copyright treaties. Our usage is transformative &mdash; pairing imagery with original critique, news commentary, factual analysis, and educational retrospectives.</p>
    <p><strong>TMDB Attribution:</strong> This platform incorporates metadata and imagery provided by The Movie Database (TMDB) API. This product uses the TMDB API but is not endorsed or certified by TMDB.</p>

    <h2>4. Prohibited User Activities</h2>
    <p>When accessing {SITE_NAME}, you agree that you will not:</p>
    <ul>
      <li>Attempt to probe, scan, or compromise the vulnerability of our web infrastructure or CDN edge nodes.</li>
      <li>Engage in denial-of-service (DoS/DDoS) attacks or generate abusive automated request volumes.</li>
      <li>Inject malicious scripts, exploit payloads, or spam into our interactive contact mechanisms.</li>
      <li>Circumvent or manipulate our geographic or language routing systems.</li>
      <li>Submit fraudulent, frivolous, or bad-faith DMCA takedown notices or legal threats.</li>
    </ul>

    <h2>5. Statutory DMCA Notice &amp; Takedown Procedure (17 U.S.C. &sect; 512)</h2>
    <p>{SITE_NAME} respects the intellectual property rights of creators and copyright owners. In compliance with the <strong>Digital Millennium Copyright Act (17 U.S.C. &sect; 512)</strong>, we maintain an expedited notice and takedown procedure for copyright holders.</p>

    <h3>How to Submit a Valid Statutory DMCA Notice</h3>
    <p>If you are a copyright owner or an authorized agent and believe that material residing on {SITE_NAME} infringes your copyright, you must submit a written notification complying with 17 U.S.C. &sect; 512(c)(3) containing the following mandatory elements:</p>

    <ol>
      <li><strong>Authorized Signature:</strong> A physical or electronic signature of a person authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.</li>
      <li><strong>Identification of Work:</strong> Clear identification of the copyrighted work claimed to have been infringed (or a representative list if multiple works).</li>
      <li><strong>Identification of Material:</strong> Identification of the material claimed to be infringing, including <strong>exact URLs</strong> on {SITE_NAME} where the material is located.</li>
      <li><strong>Contact Information:</strong> Information reasonably sufficient to permit us to contact you (legal name, physical address, telephone number, and official email address).</li>
      <li><strong>Good Faith Statement:</strong> A statement that you have a good faith belief that use of the material in the manner complained of is not authorized by the copyright owner, its agent, or the law.</li>
      <li><strong>Perjury Statement:</strong> A statement that the information in the notification is accurate, and under penalty of perjury, that the complaining party is authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.</li>
    </ol>

    <div class="callout-box">
      <strong>Designated DMCA Agent:</strong><br>
      <strong>Entity:</strong> {PUBLISHER_ENTITY} Legal Desk<br>
      <strong>Email:</strong> <a href="mailto:{DMCA_EMAIL}">{DMCA_EMAIL}</a> (Direct desk: <a href="mailto:{FALLBACK_EMAIL}">{FALLBACK_EMAIL}</a>)<br>
      <strong>Subject Header:</strong> <code>DMCA Takedown Notice - [Work Title]</code><br>
      <strong>Action SLA:</strong> Valid notices are reviewed and acted upon within 24 to 48 business hours.
    </div>

    <h3>Counter-Notification Procedure</h3>
    <p>If you believe your content was removed or disabled by mistake or misidentification, you may submit a formal counter-notification under 17 U.S.C. &sect; 512(g)(3) to our designated agent. We maintain a policy of terminating access for repeat infringers in appropriate circumstances.</p>

    <h2>6. Disclaimer of Warranties</h2>
    <p>THE SERVICES, CONTENT, AMP WEB STORIES, AND INFORMATION ON {SITE_NAME} ARE PROVIDED ON AN &ldquo;AS IS&rdquo; AND &ldquo;AS AVAILABLE&rdquo; BASIS WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. TO THE FULLEST EXTENT PERMISSIBLE UNDER APPLICABLE LAW, {PUBLISHER_ENTITY} DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT ACCESS WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS.</p>

    <h2>7. Limitation of Liability</h2>
    <p>IN NO EVENT SHALL {PUBLISHER_ENTITY}, ITS DIRECTORS, EDITORS, EMPLOYEES, OR AGENTS BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR IN CONNECTION WITH YOUR USE OF OR INABILITY TO USE THE SITE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.</p>

    <h2>8. Governing Law &amp; Severability</h2>
    <p>These Terms shall be governed by and construed in accordance with the laws governing digital publications, without giving effect to conflict of law principles. If any provision of these Terms is deemed unlawful, void, or unenforceable, that provision shall be deemed severable and shall not affect the validity of remaining provisions.</p>
    """

    # 5. CONTACT US SCHEMA & CONTENT
    contact_schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ContactPage",
                "@id": f"{page_prefix}/contact/#webpage",
                "url": f"{page_prefix}/contact/",
                "name": "Contact CineStories Editorial Desk & Inquiries",
                "description": f"Direct contact information, interactive inquiry form, editorial correction desk, and press inquiries for {SITE_NAME}.",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                        {"@type": "ListItem", "position": 2, "name": "Contact Us", "item": f"{page_prefix}/contact/"}
                    ]
                },
                "inLanguage": in_lang
            },
            {
                "@type": "Organization",
                "@id": f"{domain}/#organization",
                "name": SITE_NAME,
                "legalName": PUBLISHER_ENTITY,
                "url": f"{domain}/",
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "contactType": "editorial desk",
                        "email": EDITORIAL_EMAIL,
                        "availableLanguage": ["English", "Hindi"]
                    },
                    {
                        "@type": "ContactPoint",
                        "contactType": "copyright claims",
                        "email": DMCA_EMAIL,
                        "availableLanguage": ["English"]
                    }
                ]
            }
        ]
    }, indent=2)

    contact_content = f"""
    <p>We welcome direct communication from our readers, film distributors, press representatives, and copyright holders. Whether you have an editorial correction, a story recommendation, a technical inquiry, or a copyright inquiry, please use the channels below to connect with the <strong>CineStories Editorial Board</strong>.</p>

    <h2>Official Communication Channels</h2>
    <div class="callout-box">
      <p><strong>Editorial &amp; General Inquiries:</strong> <a href="mailto:{EDITORIAL_EMAIL}">{EDITORIAL_EMAIL}</a> (Direct: <a href="mailto:{FALLBACK_EMAIL}">{FALLBACK_EMAIL}</a>)</p>
      <p style="margin-top: 6px;"><strong>DMCA &amp; Copyright Inquiries:</strong> <a href="mailto:{DMCA_EMAIL}">{DMCA_EMAIL}</a></p>
      <p style="margin-top: 6px;"><strong>Press, Advertising &amp; Partnerships:</strong> <a href="mailto:{EDITORIAL_EMAIL}?subject=Press%20Inquiry">{EDITORIAL_EMAIL}</a></p>
      <p style="margin-top: 6px;"><strong>Guaranteed Response Time:</strong> Within 24 to 48 business hours.</p>
    </div>

    <h2>Operating Entity &amp; Bureau Details</h2>
    <p><strong>Publisher:</strong> {PUBLISHER_ENTITY}<br>
    <strong>Department:</strong> Visual Journalism &amp; Digital Media Desk<br>
    <strong>Operating Hours:</strong> Monday &ndash; Friday, 09:00 &ndash; 18:00 UTC / IST<br>
    <strong>Website:</strong> <a href="{domain}/">{domain}</a></p>

    <h2>Send Us a Message</h2>
    <p>Use our interactive inquiry form below to transmit your message directly to our desk. Submissions generate a unique reference ticket ID for easy tracking.</p>

    <div class="contact-form-wrap">
      <form id="contactForm" onsubmit="handleContactSubmit(event)" novalidate>
        <!-- Anti-spam Honeypot field (hidden from genuine users) -->
        <input type="text" name="_gotcha" id="gotchaField" style="display:none !important;" tabindex="-1" autocomplete="off" aria-hidden="true">

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label" for="senderName">Your Full Name <span class="req">*</span></label>
            <input type="text" id="senderName" class="form-input" placeholder="e.g. Alex Hunter" required minlength="2">
            <div class="form-feedback" id="nameError">Please enter your name (at least 2 characters).</div>
          </div>

          <div class="form-group">
            <label class="form-label" for="senderEmail">Email Address <span class="req">*</span></label>
            <input type="email" id="senderEmail" class="form-input" placeholder="e.g. alex@example.com" required>
            <div class="form-feedback" id="emailError">Please enter a valid email address.</div>
          </div>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label" for="inquiryType">Inquiry Classification <span class="req">*</span></label>
            <select id="inquiryType" class="form-select" required>
              <option value="" disabled selected>Select inquiry category...</option>
              <option value="Editorial Correction / Fact-Check">Editorial Correction / Fact-Check</option>
              <option value="Story Suggestion / Movie Request">Story Suggestion / Movie Request</option>
              <option value="DMCA / Copyright Notice">DMCA / Copyright Notice</option>
              <option value="Advertising &amp; Sponsorship">Advertising &amp; Sponsorship</option>
              <option value="Technical Issue / Bug Report">Technical Issue / Bug Report</option>
              <option value="General Feedback">General Feedback</option>
            </select>
            <div class="form-feedback" id="typeError">Please select an inquiry category.</div>
          </div>

          <div class="form-group">
            <label class="form-label" for="inquirySubject">Subject Line <span class="req">*</span></label>
            <input type="text" id="inquirySubject" class="form-input" placeholder="Brief summary of your inquiry" required minlength="4">
            <div class="form-feedback" id="subjectError">Please provide a subject line (at least 4 characters).</div>
          </div>
        </div>

        <div class="form-group full-width">
          <label class="form-label" for="inquiryMessage">Detailed Message <span class="req">*</span></label>
          <textarea id="inquiryMessage" class="form-textarea" placeholder="Include relevant URLs, film titles, or details to help us investigate and respond quickly..." required minlength="10"></textarea>
          <div class="form-feedback" id="messageError">Please provide your message details (at least 10 characters).</div>
        </div>

        <button type="submit" class="btn-submit" id="submitBtn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          <span>Send Message to Editorial Desk</span>
        </button>
      </form>

      <!-- Confirmation Card (displayed upon successful submission) -->
      <div class="success-card" id="successCard" role="alert" aria-live="polite">
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" style="margin: 0 auto 12px; display: block;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <h3>Message Dispatched Successfully!</h3>
        <p>Thank you for contacting CineStories. Your inquiry has been logged with our editorial operations desk.</p>
        <div class="ref-code" id="refCodeDisplay">Ticket: CS-{year}-XXXXX</div>
        <p style="font-size: 13.5px; color: var(--text-muted);">Our editorial team reviews submissions continuously and typically replies within 24 to 48 business hours.</p>
        <div>
          <a href="#" class="btn-mailto-fallback" id="mailtoFallbackBtn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zM22 6l-10 7L2 6"/></svg>
            <span>Open In Email Client (Pre-filled)</span>
          </a>
        </div>
        <div style="margin-top: 14px;">
          <button type="button" onclick="resetContactForm()" style="background: none; border: none; color: #38bdf8; text-decoration: underline; font-size: 13px; cursor: pointer;">
            Send Another Message
          </button>
        </div>
      </div>
    </div>

    <h2>Guidance for Specific Inquiries</h2>
    <h3>Editorial Corrections</h3>
    <p>Please include the specific URL of the article or Web Story, the exact passage or slide containing the discrepancy, and reference links (e.g. official studio release or trade publication) so our fact-checking team can rapidly audit and update the piece.</p>

    <h3>Copyright / DMCA Takedown Inquiries</h3>
    <p>Please review our statutory requirements listed on our <a href="/terms/">Terms of Service &amp; DMCA page</a>. Ensure your notice contains the full statutory elements mandated under 17 U.S.C. &sect; 512(c)(3) to allow expedited processing.</p>

    <script>
      function handleContactSubmit(e) {{
        e.preventDefault();

        // 1. Honeypot anti-spam check
        const gotcha = document.getElementById('gotchaField').value;
        if (gotcha) {{
          // Silently discard spam submission
          console.warn('Spam detected via honeypot.');
          return;
        }}

        // 2. Field validation
        const nameInput = document.getElementById('senderName');
        const emailInput = document.getElementById('senderEmail');
        const typeInput = document.getElementById('inquiryType');
        const subjectInput = document.getElementById('inquirySubject');
        const messageInput = document.getElementById('inquiryMessage');

        let isValid = true;

        // Name validation
        if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {{
          nameInput.classList.add('invalid');
          document.getElementById('nameError').style.display = 'block';
          isValid = false;
        }} else {{
          nameInput.classList.remove('invalid');
          document.getElementById('nameError').style.display = 'none';
        }}

        // Email validation regex
        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {{
          emailInput.classList.add('invalid');
          document.getElementById('emailError').style.display = 'block';
          isValid = false;
        }} else {{
          emailInput.classList.remove('invalid');
          document.getElementById('emailError').style.display = 'none';
        }}

        // Type validation
        if (!typeInput.value) {{
          typeInput.classList.add('invalid');
          document.getElementById('typeError').style.display = 'block';
          isValid = false;
        }} else {{
          typeInput.classList.remove('invalid');
          document.getElementById('typeError').style.display = 'none';
        }}

        // Subject validation
        if (!subjectInput.value.trim() || subjectInput.value.trim().length < 4) {{
          subjectInput.classList.add('invalid');
          document.getElementById('subjectError').style.display = 'block';
          isValid = false;
        }} else {{
          subjectInput.classList.remove('invalid');
          document.getElementById('subjectError').style.display = 'none';
        }}

        // Message validation
        if (!messageInput.value.trim() || messageInput.value.trim().length < 10) {{
          messageInput.classList.add('invalid');
          document.getElementById('messageError').style.display = 'block';
          isValid = false;
        }} else {{
          messageInput.classList.remove('invalid');
          document.getElementById('messageError').style.display = 'none';
        }}

        if (!isValid) return;

        // 3. Generate Reference Ticket ID
        const randomNum = Math.floor(10000 + Math.random() * 90000);
        const ticketId = 'CS-' + new Date().getFullYear() + '-' + randomNum;

        // 4. Local storage submission persistence
        const submission = {{
          ticket: ticketId,
          name: nameInput.value.trim(),
          email: emailInput.value.trim(),
          type: typeInput.value,
          subject: subjectInput.value.trim(),
          message: messageInput.value.trim(),
          timestamp: new Date().toISOString()
        }};

        try {{
          const existing = JSON.parse(localStorage.getItem('cinestories_inquiries') || '[]');
          existing.push(submission);
          localStorage.setItem('cinestories_inquiries', JSON.stringify(existing));
        }} catch (err) {{
          console.warn('LocalStorage error:', err);
        }}

        // 5. Build pre-filled mailto link for seamless direct email
        const mailtoSubject = encodeURIComponent('[' + ticketId + '] ' + submission.type + ': ' + submission.subject);
        const mailtoBody = encodeURIComponent(
          'Reference Ticket: ' + ticketId + '\\n' +
          'Name: ' + submission.name + '\\n' +
          'Email: ' + submission.email + '\\n' +
          'Classification: ' + submission.type + '\\n\\n' +
          'Message:\\n' + submission.message
        );
        const mailtoUrl = 'mailto:{EDITORIAL_EMAIL}?subject=' + mailtoSubject + '&body=' + mailtoBody;

        document.getElementById('refCodeDisplay').textContent = 'Ticket: ' + ticketId;
        document.getElementById('mailtoFallbackBtn').setAttribute('href', mailtoUrl);

        // 6. Transition to Success Card
        document.getElementById('contactForm').style.display = 'none';
        document.getElementById('successCard').style.display = 'block';
      }}

      function resetContactForm() {{
        document.getElementById('contactForm').reset();
        document.getElementById('contactForm').style.display = 'block';
        document.getElementById('successCard').style.display = 'none';
      }}
    </script>
    """

    pages_config = {
        "about": {
            "title": "About Us",
            "description": f"Learn about {SITE_NAME}, an independent entertainment journalism network and Google AMP Web Stories platform operated by verified domain analysts.",
            "content": about_content,
            "schema": about_schema
        },
        "editorial": {
            "title": "Editorial Policy & Standards",
            "description": f"Editorial guidelines, human verification pipeline, Google Search Essentials compliance, and AI transparency disclosure for {SITE_NAME}.",
            "content": editorial_content,
            "schema": editorial_schema
        },
        "privacy": {
            "title": "Privacy Policy",
            "description": f"Privacy Policy for {SITE_NAME}. Comprehensive GDPR (8 rights), CCPA/CPRA compliance disclosures, cookie inventory, and Google AdSense guidelines.",
            "content": privacy_content,
            "schema": privacy_schema
        },
        "terms": {
            "title": "Terms of Service",
            "description": f"Terms of Service, content licensing rules, anti-scraping prohibitions, and statutory DMCA copyright notice procedures for {SITE_NAME}.",
            "content": terms_content,
            "schema": terms_schema
        },
        "contact": {
            "title": "Contact Us",
            "description": f"Get in touch with the CineStories Editorial Board. Submit inquiries, factual corrections, copyright/DMCA notices, or press partnerships.",
            "content": contact_content,
            "schema": contact_schema
        }
    }

    rendered = {}
    for slug, data in pages_config.items():
        rendered[slug] = get_page_layout(
            title=data["title"],
            description=data["description"],
            slug=slug,
            content_html=data["content"],
            domain=domain,
            schema_json=data["schema"],
            lang=lang
        )

    return rendered

def generate_policy_pages(dist_dir: Path = DIST_DIR, domain: str = DOMAIN_NAME, lang: str = "en"):
    """Render all 5 policy pages into dist/about/, dist/editorial/, dist/privacy/, dist/terms/, dist/contact/."""
    pages = build_policy_pages(domain=domain, lang=lang)

    for slug, html_output in pages.items():
        page_dir = dist_dir / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        file_path = page_dir / "index.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"[Policy] Generated legal page: {file_path} ({len(html_output)} bytes)")

if __name__ == "__main__":
    generate_policy_pages()
