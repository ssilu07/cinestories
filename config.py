"""
Configuration module for CineStories / MoviePulse Web Stories generator.
Loads environment variables and provides centralized settings.
Automated Pipeline v1.1.1
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"

# Load .env file if present
load_dotenv(dotenv_path=ENV_PATH)

# Domain & Site identity
# Trailing slash is removed for consistent path joining
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "https://cinematicbites.com").rstrip("/")
if "vercel.app" in DOMAIN_NAME:
    DOMAIN_NAME = "https://cinematicbites.com"
SITE_NAME = os.getenv("SITE_NAME", "MoviePulse")
SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Visual Web Stories for Movie Lovers")
PUBLISHER_NAME = os.getenv("PUBLISHER_NAME", "MoviePulse")
PUBLISHER_LOGO_PATH = "/assets/logo.png"

# Google Analytics 4 (GA4)
GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "G-5T9C99C0KF").strip()

# IndexNow Instant Indexing Protocol (Bing, Yandex, Naver)
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "c1ne570r1e5b17e58d21abf59e4b4f6c").strip()

def get_ga_script(measurement_id: str = GA_MEASUREMENT_ID) -> str:
    """Return standard GA4 gtag.js snippet for non-AMP pages."""
    if not measurement_id:
        return ""
    return f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{measurement_id}');
  </script>"""

# Google AdSense
ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID", "").strip()

def get_adsense_script(client_id: str = ADSENSE_CLIENT_ID) -> str:
    """Return standard Google AdSense script snippet for non-AMP pages."""
    if not client_id:
        return ""
    pub_id = client_id if client_id.startswith("ca-pub-") else f"ca-pub-{client_id}"
    return f"""  <!-- Google AdSense -->\n  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub_id}" crossorigin="anonymous"></script>"""

def get_amp_story_ads_tags(client_id: str = ADSENSE_CLIENT_ID) -> tuple:
    """Return (head_script, body_tag) for AMP Story Auto Ads."""
    if not client_id:
        return ("", "")
    pub_id = client_id if client_id.startswith("ca-pub-") else f"ca-pub-{client_id}"
    head_script = '    <script async custom-element="amp-story-auto-ads" src="https://cdn.ampproject.org/v0/amp-story-auto-ads-0.1.js"></script>'
    body_tag = f"""      <amp-story-auto-ads>
        <script type="application/json">
        {{{{
          "ad-attributes": {{{{
            "type": "adsense",
            "data-ad-client": "{pub_id}"
          }}}}
        }}}}
        </script>
      </amp-story-auto-ads>"""
    return (head_script, body_tag)

def get_publisher_logo_url(domain: str = DOMAIN_NAME) -> str:
    """Return absolute 1:1 publisher logo URL satisfying AMP spec."""
    return f"{domain}{PUBLISHER_LOGO_PATH}"

# API Keys
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

# TMDB Image Base URLs
TMDB_IMAGE_ORIGINAL = "https://image.tmdb.org/t/p/original"
TMDB_IMAGE_BACKDROP = "https://image.tmdb.org/t/p/w1280"
TMDB_IMAGE_POSTER = "https://image.tmdb.org/t/p/w780"
TMDB_IMAGE_THUMB = "https://image.tmdb.org/t/p/w500"

# Directories
DIST_DIR = ROOT_DIR / "dist"
STORIES_DIR = DIST_DIR / "stories"
ARTICLES_DIR = DIST_DIR / "articles"
DISCOVER_DIR = DIST_DIR / "discover"
ASSETS_DIR = DIST_DIR / "assets"
SITEMAP_PATH = DIST_DIR / "sitemap.xml"
STORIES_JSON_PATH = DIST_DIR / "stories.json"
ARTICLES_JSON_PATH = DIST_DIR / "articles.json"

# Pipeline & Anti-Spam safety limits
# Google Discover recommends high quality & consistency over mass volume
DAILY_PUBLISH_LIMIT = int(os.getenv("DAILY_PUBLISH_LIMIT", "4"))
STORIES_PER_CATEGORY_LIMIT = int(os.getenv("STORIES_PER_CATEGORY_LIMIT", "2"))
MAX_TOTAL_STORIES = int(os.getenv("MAX_TOTAL_STORIES", "100"))
MIN_ARTICLE_WORDS = int(os.getenv("MIN_ARTICLE_WORDS", "350"))
API_PACING_SECONDS = float(os.getenv("API_PACING_SECONDS", "2.0"))

# Registry for deduplication (prevents re-generating same articles daily)
REGISTRY_PATH = DIST_DIR / "published_registry.json"

# Tumblr Integration Settings
TUMBLR_BLOG_NAME = os.getenv("TUMBLR_BLOG_NAME", "sumits7196").strip()
TUMBLR_CONSUMER_KEY = os.getenv("TUMBLR_CONSUMER_KEY", "").strip()
TUMBLR_CONSUMER_SECRET = os.getenv("TUMBLR_CONSUMER_SECRET", "").strip()
TUMBLR_OAUTH_TOKEN = os.getenv("TUMBLR_OAUTH_TOKEN", "").strip()
TUMBLR_OAUTH_SECRET = os.getenv("TUMBLR_OAUTH_SECRET", "").strip()
TUMBLR_POST_STATE = os.getenv("TUMBLR_POST_STATE", "published").strip()  # 'published' or 'queue'
TUMBLR_DAILY_POST_LIMIT = int(os.getenv("TUMBLR_DAILY_POST_LIMIT", "2"))
TUMBLR_REGISTRY_PATH = DIST_DIR / "tumblr_published.json"

# Ensure base dist directories exist
DIST_DIR.mkdir(parents=True, exist_ok=True)
STORIES_DIR.mkdir(parents=True, exist_ok=True)
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DISCOVER_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

