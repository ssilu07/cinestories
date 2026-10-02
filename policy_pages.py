"""
Policy and Legal Pages Generator for CineStories.
Generates essential AdSense-compliant pages:
1. About Us (/about/)
2. Privacy Policy (/privacy/)
3. Terms of Service & Disclaimer (/terms/)
4. Contact Us (/contact/)
"""

from pathlib import Path
from datetime import datetime, timezone
from config import DOMAIN_NAME, SITE_NAME, DIST_DIR

def get_page_layout(title: str, description: str, slug: str, content_html: str, domain: str = DOMAIN_NAME) -> str:
    """Standard layout for legal & informational pages matching dark cinema theme."""
    year = datetime.now(timezone.utc).year
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{domain}/{slug}/">
  <link rel="icon" type="image/svg+xml" href="{domain}/assets/favicon.svg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg: #090b10;
      --surface: #10141f;
      --surface-border: rgba(255, 255, 255, 0.08);
      --primary: #e11d48;
      --accent-gold: #f59e0b;
      --text: #ffffff;
      --text-muted: #94a3b8;
      --radius-lg: 20px;
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

    .btn-home {{
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
      transition: background 0.2s ease;
    }}

    .btn-home:hover {{
      background: rgba(225, 29, 72, 0.2);
      border-color: var(--primary);
    }}

    .main-content {{
      max-width: 900px;
      margin: 40px auto 60px;
      padding: 0 24px;
      flex-grow: 1;
      width: 100%;
    }}

    .page-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      padding: 40px 36px;
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
      margin: 32px 0 12px;
      border-bottom: 1px solid var(--surface-border);
      padding-bottom: 8px;
    }}

    .content-body h3 {{
      font-size: 16px;
      font-weight: 700;
      color: #e2e8f0;
      margin: 20px 0 8px;
    }}

    .content-body p {{
      color: var(--text-muted);
      margin-bottom: 16px;
      font-size: 15px;
    }}

    .content-body ul {{
      margin: 0 0 20px 24px;
      color: var(--text-muted);
      font-size: 15px;
    }}

    .content-body li {{
      margin-bottom: 8px;
    }}

    .content-body a {{
      color: #38bdf8;
      text-decoration: underline;
    }}

    .callout-box {{
      background: rgba(225, 29, 72, 0.1);
      border-left: 4px solid var(--primary);
      padding: 16px 20px;
      border-radius: var(--radius-sm);
      margin: 24px 0;
      font-size: 14px;
      color: #cbd5e1;
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
    }}

    .footer-links a:hover {{
      color: #fff;
    }}
  </style>
</head>
<body>

  <header class="navbar">
    <div class="nav-container">
      <a href="/" class="brand-wrap">
        <img src="/assets/logo.png" alt="{SITE_NAME}" class="brand-logo">
        <div class="brand-text">
          <h1>{SITE_NAME}</h1>
        </div>
      </a>
      <a href="/" class="btn-home">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        <span>Back to Stories</span>
      </a>
    </div>
  </header>

  <main class="main-content">
    <article class="page-card">
      <div class="page-kicker">Legal &amp; Policy</div>
      <h1 class="page-title">{title}</h1>
      <div class="content-body">
        {content_html}
      </div>
    </article>
  </main>

  <footer class="footer">
    <div class="footer-container">
      <p style="font-size: 13px; color: var(--text-muted);">&copy; {year} {SITE_NAME}. All rights reserved.</p>
      <div class="footer-links">
        <a href="/about/">About Us</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms &amp; Disclaimer</a>
        <a href="/contact/">Contact Us</a>
        <a href="/sitemap.xml">Sitemap</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""

def generate_policy_pages(dist_dir: Path = DIST_DIR, domain: str = DOMAIN_NAME):
    """Render all 4 policy pages into dist/about/, dist/privacy/, dist/terms/, dist/contact/."""
    pages = {
        "about": {
            "title": "About Us",
            "description": f"Learn about {SITE_NAME}, an autonomous visual Google AMP Web Stories platform dedicated to Hollywood blockbusters, TV series, and cult classics.",
            "content": f"""
            <p>Welcome to <strong>{SITE_NAME}</strong> (hosted at <a href="{domain}/">{domain}</a>), a cutting-edge visual entertainment platform dedicated to delivering bite-sized, mobile-optimized <strong>Google AMP Web Stories</strong> for cinema enthusiasts, binge-watchers, and pop-culture fans worldwide.</p>

            <h2>Our Mission</h2>
            <p>The modern entertainment landscape moves at lightning speed. With hundreds of movies and television shows premiering every month across streaming services and theatrical screens, movie lovers need snackable, visually engaging, and insightful summaries without spoilers.</p>
            <p>Our mission is to transform raw cinematic data into rich, tap-friendly visual stories that you can enjoy in 60 seconds on any smartphone, tablet, or desktop browser.</p>

            <h2>What We Cover</h2>
            <ul>
              <li><strong>Binge TV Series &amp; Shows:</strong> Global phenomena like <em>Money Heist</em>, <em>Stranger Things</em>, <em>The Boys</em>, <em>Breaking Bad</em>, <em>Wednesday</em>, and <em>Game of Thrones</em>.</li>
              <li><strong>Trending Blockbusters:</strong> New theatrical and streaming releases including Marvel hits, <em>John Wick</em>, <em>Dune</em>, and upcoming spectacles.</li>
              <li><strong>Cult Classics &amp; Franchises:</strong> Iconic mind-bending cinema like <em>Interstellar</em>, <em>Inception</em>, <em>The Dark Knight</em>, and <em>Final Destination</em>.</li>
            </ul>

            <h2>Technology &amp; Editorial Standards</h2>
            <p><strong>{SITE_NAME}</strong> leverages verified data from <strong>The Movie Database (TMDB)</strong> and synthesizes high-CTR narrative hooks using advanced generative AI architectures (Google Gemini). Every story is strictly crafted to comply with the official <strong>Google AMP Web Story 1.0 Specification</strong>, ensuring instant loading speeds, zero bloat, and optimal readability on Google Discover and mobile search.</p>

            <div class="callout-box">
              <strong>TMDB Attribution:</strong> This product uses the TMDB API but is not endorsed or certified by TMDB. All movie posters, backdrops, and character names remain the intellectual property of their respective studios and production companies.
            </div>

            <h2>Connect With Us</h2>
            <p>Have questions, story requests, or feedback? Feel free to reach out via our <a href="/contact/">Contact Us page</a>.</p>
            """
        },
        "privacy": {
            "title": "Privacy Policy",
            "description": f"Privacy Policy for {SITE_NAME}. Explains how we collect, use, and protect your information, including Google AdSense cookies and analytics.",
            "content": f"""
            <p><em>Last updated: October 2026</em></p>
            <p>At <strong>{SITE_NAME}</strong>, accessible from <a href="{domain}/">{domain}</a>, one of our main priorities is the privacy of our visitors. This Privacy Policy document outlines the types of information that is collected and recorded by {SITE_NAME} and how we use it.</p>

            <h2>Information We Collect</h2>
            <p>Like most modern web platforms, {SITE_NAME} collects non-personally identifiable information that web browsers and servers typically make available, such as:</p>
            <ul>
              <li>Browser type and language preference</li>
              <li>Referring website and exit pages</li>
              <li>Date and time of each visitor request</li>
              <li>Internet Protocol (IP) addresses for geolocation and fraud prevention</li>
            </ul>

            <h2>Cookies and Web Beacons</h2>
            <p>{SITE_NAME} uses standard cookies to store information about visitors' preferences and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type or other information.</p>

            <h2>Google DoubleClick DART Cookie &amp; AdSense</h2>
            <p>Google is one of the third-party vendors on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to our site and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy at the following URL: <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">https://policies.google.com/technologies/ads</a>.</p>

            <h2>Our Advertising Partners</h2>
            <p>Some of advertisers on our site may use cookies and web beacons. Our advertising partners include:</p>
            <ul>
              <li><strong>Google AdSense / Google Ad Manager:</strong> Privacy Policy available at <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">https://policies.google.com/privacy</a></li>
            </ul>
            <p>Third-party ad servers or ad networks use technologies like cookies, JavaScript, or Web Beacons that are used in their respective advertisements and links that appear on {SITE_NAME}, which are sent directly to users' browser.</p>

            <h2>CCPA Privacy Rights (Do Not Sell My Personal Information)</h2>
            <p>Under the CCPA, California consumers have the right to:</p>
            <ul>
              <li>Request that a business disclose the categories and specific pieces of personal data collected.</li>
              <li>Request that a business delete any personal data collected about the consumer.</li>
              <li>Request that a business not sell the consumer's personal data.</li>
            </ul>

            <h2>GDPR Data Protection Rights</h2>
            <p>Every European user is entitled to the right to access, rectify, erase, restrict processing, and object to processing of their personal data.</p>

            <h2>Children's Information</h2>
            <p>{SITE_NAME} does not knowingly collect any Personal Identifiable Information from children under the age of 13. If you think that your child provided this kind of information on our website, we strongly encourage you to contact us immediately.</p>

            <h2>Contact Us</h2>
            <p>If you have additional questions or require more information about our Privacy Policy, do not hesitate to contact us at <a href="/contact/">our Contact page</a>.</p>
            """
        },
        "terms": {
            "title": "Terms of Service &amp; Disclaimer",
            "description": f"Terms of Service, DMCA Disclaimer, and Fair Use statement for {SITE_NAME}.",
            "content": f"""
            <p><em>Last updated: October 2026</em></p>
            <p>By accessing and using <strong>{SITE_NAME}</strong> (<a href="{domain}/">{domain}</a>), you accept and agree to be bound by the terms and provision of this agreement.</p>

            <h2>1. Informational &amp; Entertainment Purpose</h2>
            <p>All content provided on {SITE_NAME}, including AMP Web Stories, text summaries, trivia, and reviews, is for entertainment, commentary, criticism, and educational purposes only.</p>

            <h2>2. Fair Use &amp; Intellectual Property Disclaimer</h2>
            <p>All movie and television show titles, character names, stills, posters, and trademarks referenced on this website are the property of their respective copyright owners, film distributors, and studios (e.g., Netflix, Warner Bros., Disney, Paramount, Universal, HBO, Sony).</p>
            <p>The use of images and excerpts on this platform constitutes a <strong>Fair Use</strong> under Title 17 U.S.C. Section 107 of the United States Copyright Act for transformative purposes such as critique, commentary, news reporting, and education.</p>

            <h2>3. TMDB API Attribution</h2>
            <p>{SITE_NAME} uses metadata, images, and ratings provided by The Movie Database (TMDB) API. This website is not endorsed, certified, or sponsored by TMDB.</p>

            <h2>4. Disclaimer of Warranties</h2>
            <p>The materials on {SITE_NAME} are provided on an 'as is' basis. {SITE_NAME} makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property.</p>

            <h2>5. DMCA / Takedown Notice</h2>
            <p>If you are a copyright owner or an agent thereof and believe that any content hosted on {SITE_NAME} infringes upon your copyright, please contact us with the specific URL and proof of ownership. We will promptly remove or disable access to the infringing material within 48 hours.</p>

            <h2>6. Changes to Terms</h2>
            <p>{SITE_NAME} reserves the right to revise these terms of service at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms.</p>
            """
        },
        "contact": {
            "title": "Contact Us",
            "description": f"Get in touch with the editorial team at {SITE_NAME} for inquiries, DMCA notices, or partnership requests.",
            "content": f"""
            <p>We welcome feedback, story suggestions, partnership proposals, and press inquiries. Please use the contact details below to reach our editorial and technical team.</p>

            <h2>Contact Information</h2>
            <div class="callout-box">
              <p><strong>Official Email:</strong> <a href="mailto:sumits7196@gmail.com" style="color: #fff; font-weight: 700;">sumits7196@gmail.com</a></p>
              <p style="margin-top: 6px;"><strong>Response Time:</strong> Typically within 24 to 48 business hours.</p>
            </div>

            <h2>What You Can Contact Us For:</h2>
            <ul>
              <li><strong>Content Feedback &amp; Suggestions:</strong> Let us know if you'd like to see a specific Hollywood movie or TV series covered in our Web Stories format.</li>
              <li><strong>Copyright &amp; DMCA Notices:</strong> If you are a copyright holder and wish to request material modification or removal, please provide specific links.</li>
              <li><strong>Advertising &amp; Sponsorships:</strong> Inquiries regarding sponsored Web Stories, brand partnerships, or advertising integrations.</li>
              <li><strong>Technical Issues:</strong> Report broken links, playback issues, or display glitches on mobile or desktop devices.</li>
            </ul>

            <h2>Mailing Address &amp; Digital Office</h2>
            <p>{SITE_NAME} Digital Media Network<br>
            Online Publishing &amp; Visual Journalism Platform<br>
            Website: <a href="{domain}/">{domain}</a></p>
            """
        }
    }

    for slug, data in pages.items():
        page_dir = dist_dir / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        html_output = get_page_layout(
            title=data["title"],
            description=data["description"],
            slug=slug,
            content_html=data["content"],
            domain=domain
        )
        file_path = page_dir / "index.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"[Policy] Generated legal page: {file_path}")

if __name__ == "__main__":
    generate_policy_pages()
