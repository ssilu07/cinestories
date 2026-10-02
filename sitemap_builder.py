"""
Automated XML Sitemap Builder for CineStories.
Generates a valid sitemap.xml adhering to Sitemaps XML protocol 0.9 with image extension.
Includes Homepage, Discover Feed, Web Stories, Discover Articles, and Legal pages.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import DOMAIN_NAME, SITEMAP_PATH, TMDB_IMAGE_POSTER, TMDB_IMAGE_BACKDROP

def generate_sitemap(
    stories: List[Dict[str, Any]],
    articles: Optional[List[Dict[str, Any]]] = None,
    domain: str = DOMAIN_NAME,
    output_path: Path = SITEMAP_PATH
) -> str:
    """
    Build dist/sitemap.xml containing the portal home, discover feed, stories, and articles.
    """
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urlset = ET.Element(
        "urlset",
        {
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1"
        }
    )

    # 1. Homepage URL
    home_url = ET.SubElement(urlset, "url")
    ET.SubElement(home_url, "loc").text = f"{domain}/"
    ET.SubElement(home_url, "lastmod").text = today_str
    ET.SubElement(home_url, "changefreq").text = "daily"
    ET.SubElement(home_url, "priority").text = "1.0"

    # 2. Google Discover Feed Portal URL
    discover_url = ET.SubElement(urlset, "url")
    ET.SubElement(discover_url, "loc").text = f"{domain}/discover/"
    ET.SubElement(discover_url, "lastmod").text = today_str
    ET.SubElement(discover_url, "changefreq").text = "hourly"
    ET.SubElement(discover_url, "priority").text = "0.95"

    # 3. Google Discover Article URLs
    if articles:
        for article in articles:
            movie = article.get("movie", {})
            slug = movie.get("slug")
            if not slug:
                continue

            art_loc = f"{domain}/articles/{slug}/"
            url_elem = ET.SubElement(urlset, "url")
            ET.SubElement(url_elem, "loc").text = art_loc
            ET.SubElement(url_elem, "lastmod").text = today_str
            ET.SubElement(url_elem, "changefreq").text = "daily"
            ET.SubElement(url_elem, "priority").text = "0.85"

            # 1280px Backdrop Image tag for Google Chrome Discover
            backdrop_path = movie.get("backdrop_path")
            if backdrop_path:
                img_elem = ET.SubElement(url_elem, "image:image")
                img_loc = f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path.startswith("/") else backdrop_path
                ET.SubElement(img_elem, "image:loc").text = img_loc
                ET.SubElement(img_elem, "image:title").text = f"{article.get('headline') or movie.get('title', 'Movie')} Feature Still"

    # 4. Individual Web Story URLs
    for story in stories:
        movie = story.get("movie", {})
        slug = movie.get("slug")
        if not slug:
            continue

        story_loc = f"{domain}/stories/{slug}/"
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = story_loc
        ET.SubElement(url_elem, "lastmod").text = today_str
        ET.SubElement(url_elem, "changefreq").text = "weekly"
        ET.SubElement(url_elem, "priority").text = "0.80"

        # Poster Image tag for Web Story
        poster_path = movie.get("poster_path")
        if poster_path:
            img_elem = ET.SubElement(url_elem, "image:image")
            img_loc = f"{TMDB_IMAGE_POSTER}{poster_path}" if poster_path.startswith("/") else poster_path
            ET.SubElement(img_elem, "image:loc").text = img_loc
            ET.SubElement(img_elem, "image:title").text = f"{movie.get('title', 'Movie')} Web Story Poster"

    # 5. Policy & Legal Pages
    legal_pages = ["about", "editorial", "privacy", "terms", "contact"]
    for page in legal_pages:
        legal_url = ET.SubElement(urlset, "url")
        ET.SubElement(legal_url, "loc").text = f"{domain}/{page}/"
        ET.SubElement(legal_url, "lastmod").text = today_str
        ET.SubElement(legal_url, "changefreq").text = "monthly"
        ET.SubElement(legal_url, "priority").text = "0.50"

    # Format XML with indentation
    ET.indent(urlset, space="  ", level=0)
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str = xml_declaration + ET.tostring(urlset, encoding="unicode")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    total_urls = 2 + (len(articles) if articles else 0) + len(stories) + len(legal_pages)
    print(f"[Sitemap] Successfully updated sitemap: {output_path} ({total_urls} URLs)")
    return xml_str

if __name__ == "__main__":
    from sample_data import SAMPLE_MOVIES
    dummy_stories = [{"movie": m, "title": m["title"]} for m in SAMPLE_MOVIES]
    generate_sitemap(dummy_stories)
