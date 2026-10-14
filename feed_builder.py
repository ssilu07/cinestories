"""
RSS 2.0 Feed Builder for Google Publisher Center and News Aggregators.
Generates dist/feed.xml and dist/rss.xml adhering to RSS 2.0 / Google News RSS specifications.
"""

import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET

from config import DOMAIN_NAME, DIST_DIR, SITE_NAME, SITE_TAGLINE, TMDB_IMAGE_BACKDROP

FEED_PATH = DIST_DIR / "feed.xml"
RSS_PATH = DIST_DIR / "rss.xml"

def generate_rss_feed(
    articles: Optional[List[Dict[str, Any]]] = None,
    domain: str = DOMAIN_NAME,
    output_paths: Optional[List[Path]] = None
) -> str:
    """
    Generate valid RSS 2.0 feed containing latest articles for Google Publisher Center.
    """
    if output_paths is None:
        output_paths = [FEED_PATH, RSS_PATH]

    if articles is None:
        articles_json_path = DIST_DIR / "articles.json"
        if articles_json_path.exists():
            with open(articles_json_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
        else:
            articles = []

    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:atom": "http://www.w3.org/2005/Atom",
        "xmlns:media": "http://search.yahoo.com/mrss/",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
    })

    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"{SITE_NAME} | {SITE_TAGLINE}"
    ET.SubElement(channel, "link").text = f"{domain}/"
    ET.SubElement(channel, "description").text = f"Visual Web Stories and cinema deep dives from {SITE_NAME}."
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now(timezone.utc))

    # Atom self link
    atom_link = ET.SubElement(channel, "atom:link", {
        "href": f"{domain}/feed.xml",
        "rel": "self",
        "type": "application/rss+xml"
    })

    # Logo image
    image_elem = ET.SubElement(channel, "image")
    ET.SubElement(image_elem, "url").text = f"{domain}/assets/logo.png"
    ET.SubElement(image_elem, "title").text = SITE_NAME
    ET.SubElement(image_elem, "link").text = f"{domain}/"

    # Add article items
    for article in articles[:50]:  # Up to 50 latest items
        movie = article.get("movie", {})
        slug = movie.get("slug")
        if not slug:
            continue

        item_url = f"{domain}/articles/{slug}/"
        headline = article.get("headline") or movie.get("title") or "Entertainment Story"
        description = article.get("meta_description") or article.get("verdict_summary") or headline

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = headline
        ET.SubElement(item, "link").text = item_url
        ET.SubElement(item, "description").text = description

        # GUID
        guid = ET.SubElement(item, "guid", {"isPermaLink": "true"})
        guid.text = item_url

        # Publication date
        date_str = article.get("date_published") or article.get("published_at")
        try:
            if date_str:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                dt = datetime.now(timezone.utc)
        except Exception:
            dt = datetime.now(timezone.utc)
        ET.SubElement(item, "pubDate").text = format_datetime(dt)

        # Media enclosure
        backdrop_path = movie.get("backdrop_path")
        if backdrop_path:
            img_url = f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path.startswith("/") else backdrop_path
            ET.SubElement(item, "media:content", {
                "url": img_url,
                "medium": "image",
                "type": "image/jpeg"
            })
            ET.SubElement(item, "enclosure", {
                "url": img_url,
                "type": "image/jpeg",
                "length": "0"
            })

    ET.indent(rss, space="  ", level=0)
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + ET.tostring(rss, encoding="unicode")

    for path in output_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"[RSS Feed] Successfully wrote {path} ({min(len(articles), 50)} items)")

    return xml_str

if __name__ == "__main__":
    generate_rss_feed()
