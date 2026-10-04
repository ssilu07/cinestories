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
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "https://cinestories-omega.vercel.app").rstrip("/")
SITE_NAME = os.getenv("SITE_NAME", "MoviePulse")
SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Visual Web Stories for Movie Lovers")
PUBLISHER_NAME = os.getenv("PUBLISHER_NAME", "MoviePulse")
PUBLISHER_LOGO_PATH = "/assets/logo.png"

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

# Pipeline defaults
STORIES_PER_CATEGORY_LIMIT = int(os.getenv("STORIES_PER_CATEGORY_LIMIT", "10"))
MAX_TOTAL_STORIES = int(os.getenv("MAX_TOTAL_STORIES", "25"))

# Ensure base dist directories exist
DIST_DIR.mkdir(parents=True, exist_ok=True)
STORIES_DIR.mkdir(parents=True, exist_ok=True)
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DISCOVER_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
