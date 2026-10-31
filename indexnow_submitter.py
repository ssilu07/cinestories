"""
CinematicBites / MoviePulse IndexNow & Fast-Indexing Submitter
Instantly notifies search engines (Microsoft Bing, Yandex, Seznam, Naver, Google)
when new Google AMP stories and in-depth articles are published or updated.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Optional

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from config import DOMAIN_NAME, DIST_DIR, ASSETS_DIR

# Default 32-character hexadecimal IndexNow Key
INDEXNOW_KEY = "c1ne570r1e5b17e58d21abf59e4b4f6c"


def ensure_indexnow_key_file(key: str = INDEXNOW_KEY) -> Path:
    """Ensures the IndexNow verification key file exists in dist/ and assets/."""
    key_filename = f"{key}.txt"

    # Save in dist (deployed root)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    dist_key_path = DIST_DIR / key_filename
    dist_key_path.write_text(key, encoding="utf-8")

    # Also save in assets for safety
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    assets_key_path = ASSETS_DIR / key_filename
    assets_key_path.write_text(key, encoding="utf-8")

    return dist_key_path


def get_latest_urls(limit: int = 50) -> List[str]:
    """Retrieves high-priority URLs (homepage, discover, recent stories and articles)."""
    urls = [
        f"{DOMAIN_NAME}/",
        f"{DOMAIN_NAME}/discover/",
        f"{DOMAIN_NAME}/feed.xml",
        f"{DOMAIN_NAME}/sitemap.xml",
    ]

    # Add recent stories
    stories_json = DIST_DIR / "stories.json"
    if stories_json.exists():
        try:
            data = json.loads(stories_json.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data[:limit]:
                    slug = item.get("slug")
                    if slug:
                        urls.append(f"{DOMAIN_NAME}/stories/{slug}/")
        except Exception as e:
            print(f"[!] Notice reading stories.json for IndexNow: {e}")

    # Add recent articles
    articles_json = DIST_DIR / "articles.json"
    if articles_json.exists():
        try:
            data = json.loads(articles_json.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data[:limit]:
                    slug = item.get("movie", {}).get("slug") or item.get("slug")
                    if slug:
                        urls.append(f"{DOMAIN_NAME}/articles/{slug}/")
        except Exception as e:
            print(f"[!] Notice reading articles.json for IndexNow: {e}")

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)

    return deduped


def ping_sitemaps(domain: str = DOMAIN_NAME):
    """Pings Google and Bing with the current sitemap."""
    sitemap_url = f"{domain}/sitemap.xml"
    ping_endpoints = [
        f"https://www.bing.com/ping?sitemap={sitemap_url}",
        f"https://www.google.com/ping?sitemap={sitemap_url}"
    ]
    for endpoint in ping_endpoints:
        try:
            req = urllib.request.Request(endpoint, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=8) as res:
                print(f"[✔] Sitemap Pinged: {endpoint} -> HTTP {res.getcode()}")
        except Exception as e:
            print(f"[~] Sitemap ping notice ({endpoint}): {e}")


def submit_to_indexnow(urls: Optional[List[str]] = None, key: str = INDEXNOW_KEY) -> bool:
    """
    Submits URLs directly to the IndexNow protocol API for instant search engine indexing.
    """
    ensure_indexnow_key_file(key)

    if urls is None:
        urls = get_latest_urls()

    if not urls:
        print("[!] No URLs found to submit to IndexNow.")
        return False

    host = DOMAIN_NAME.replace("https://", "").replace("http://", "").split("/")[0]
    key_location = f"{DOMAIN_NAME}/{key}.txt"

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }

    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow"
    ]
    success_any = False

    for endpoint in endpoints:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "CinematicBites-IndexNow-Agent/1.0",
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        print(f"\n[⚡] Submitting {len(urls)} URLs to IndexNow ({endpoint})...")
        print(f" • Host: {host}")
        print(f" • Key Location: {key_location}")

        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                status = response.getcode()
                if status in (200, 202):
                    print(f"[✔] IndexNow Success! HTTP {status} (URLs submitted to Bing, Yandex, Seznam & Naver)")
                    success_any = True
                else:
                    print(f"[!] IndexNow returned unexpected HTTP {status}")
        except urllib.error.HTTPError as e:
            print(f"[!] HTTP Error during IndexNow submission: {e.code} - {e.reason}")
        except Exception as e:
            print(f"[!] Error connecting to IndexNow endpoint: {e}")

    # Also trigger sitemap pings
    ping_sitemaps(DOMAIN_NAME)

    return success_any


def main():
    print("=" * 60)
    print("🎬 CINEMATICBITES: INDEXNOW & FAST-INDEXING SUBMITTER")
    print("=" * 60)
    urls = get_latest_urls(limit=100)
    print(f"Found {len(urls)} high-priority URLs ready for immediate submission.")
    submit_to_indexnow(urls=urls)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
