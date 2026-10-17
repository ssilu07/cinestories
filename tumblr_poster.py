"""
Tumblr Automated Poster for CineStories.
Automatically formats and publishes visually rich movie photo posts to sumits7196.tumblr.com
with click-through links, synopsis, AI highlights, ratings, and targeted hashtags.

Usage:
    python tumblr_poster.py [--limit 2] [--state published] [--dry-run]
"""

import argparse
import html
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import (
    DOMAIN_NAME,
    DIST_DIR,
    STORIES_DIR,
    ARTICLES_DIR,
    ARTICLES_JSON_PATH,
    STORIES_JSON_PATH,
    TMDB_IMAGE_POSTER,
    TMDB_IMAGE_BACKDROP,
    TUMBLR_BLOG_NAME,
    TUMBLR_CONSUMER_KEY,
    TUMBLR_CONSUMER_SECRET,
    TUMBLR_OAUTH_TOKEN,
    TUMBLR_OAUTH_SECRET,
    TUMBLR_POST_STATE,
    TUMBLR_DAILY_POST_LIMIT,
    TUMBLR_REGISTRY_PATH,
)


def load_json(filepath: Path) -> List[Dict[str, Any]]:
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[WARN] Error reading {filepath}: {e}")
        return []

def load_tumblr_registry() -> Dict[str, Any]:
    """Load records of previously published Tumblr posts to avoid duplicate posting."""
    if TUMBLR_REGISTRY_PATH.exists():
        try:
            with open(TUMBLR_REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load tumblr_published.json, initializing new: {e}")
    return {"published_movies": {}, "last_updated": None}

def save_tumblr_registry(registry: Dict[str, Any]):
    """Persist published ledger to dist/tumblr_published.json."""
    registry["last_updated"] = datetime.now(timezone.utc).isoformat()
    try:
        with open(TUMBLR_REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save tumblr registry: {e}")

def format_tumblr_caption(article: Dict[str, Any], domain: str) -> str:
    """Format rich HTML caption tailored for Tumblr's movie audience."""
    movie = article.get("movie", {})
    title = movie.get("title") or "Movie Highlight"
    year = (movie.get("release_date") or "")[:4]
    rating = movie.get("vote_average", 0)
    genres = ", ".join(movie.get("genres", []))
    tagline = movie.get("tagline", "").strip()
    overview = movie.get("overview", "").strip()
    takeaways = article.get("key_takeaways", [])
    director = movie.get("director", "").strip()
    top_cast = movie.get("top_cast", [])[:3]
    slug = movie.get("slug", "")

    story_url = f"{domain}/stories/{slug}/"
    article_url = f"{domain}/articles/{slug}/"

    lines = []
    # Header
    title_display = f"{title} ({year})" if year else title
    lines.append(f"<h2>🎬 <b>{html.escape(title_display)}</b></h2>")

    # Metadata badges
    meta_parts = []
    if rating:
        meta_parts.append(f"⭐ <b>Rating:</b> {rating:.1f}/10")
    if genres:
        meta_parts.append(f"🎭 <b>Genre:</b> {html.escape(genres)}")
    if meta_parts:
        lines.append(f"<p>{' &nbsp;|&nbsp; '.join(meta_parts)}</p>")

    # Tagline quote
    if tagline:
        lines.append(f"<blockquote><i>“{html.escape(tagline)}”</i></blockquote>")

    # Overview
    if overview:
        short_overview = overview if len(overview) <= 280 else overview[:277] + "..."
        lines.append(f"<p>{html.escape(short_overview)}</p>")

    # Key Takeaways / Highlights
    if takeaways:
        lines.append("<p><b>✨ Key Highlights:</b></p><ul>")
        for point in takeaways[:3]:
            lines.append(f"<li>{html.escape(point)}</li>")
        lines.append("</ul>")

    # Cast & Director
    credits = []
    if director:
        credits.append(f"🎬 Directed by <b>{html.escape(director)}</b>")
    if top_cast:
        credits.append(f"🌟 Starring <b>{html.escape(', '.join(top_cast))}</b>")
    if credits:
        lines.append(f"<p>{'<br>'.join(credits)}</p>")

    # Call To Action links
    lines.append("<hr>")
    lines.append(f'<p>⚡ <b>Experience the Full Visual Web Story:</b><br><a href="{story_url}">👉 Click here to watch {html.escape(title)} Web Story</a></p>')
    lines.append(f'<p>📖 <b>Deep-Dive Article & Trivia:</b><br><a href="{article_url}">Read full analysis on CineStories</a></p>')

    return "\n".join(lines)

def build_tumblr_tags(article: Dict[str, Any]) -> List[str]:
    """Generate high-engagement Tumblr tags optimized for Tier-1 (US/UK/CA) movie fandoms."""
    movie = article.get("movie", {})
    # Core Tier-1 trending entertainment tags on Tumblr
    tags = [
        "movies",
        "cinema",
        "films",
        "cinephile",
        "letterboxd",
        "what to watch",
        "movie recommendation",
        "film review",
        "cinestories"
    ]

    title = movie.get("title")
    if title:
        tags.append(title.lower())

    for genre in movie.get("genres", []):
        tags.append(genre.lower())
        tags.append(f"{genre.lower()} movies")

    for actor in movie.get("top_cast", [])[:2]:
        tags.append(actor.lower())

    director = movie.get("director")
    if director:
        tags.append(director.lower())

    # De-duplicate while preserving order
    seen = set()
    cleaned_tags = []
    for t in tags:
        t_clean = t.strip().replace("#", "")
        if t_clean and t_clean not in seen:
            seen.add(t_clean)
            cleaned_tags.append(t_clean)

    return cleaned_tags[:15]  # Tumblr supports up to 20 tags

def get_image_url(movie: Dict[str, Any]) -> Optional[str]:
    """Select verified high-res image URL (poster or backdrop) for Tumblr photo post."""
    poster_path = movie.get("poster_path")
    backdrop_path = movie.get("backdrop_path")

    # Prefer high-res portrait poster for Tumblr visual feed
    if poster_path and isinstance(poster_path, str) and poster_path.strip():
        return f"{TMDB_IMAGE_POSTER}{poster_path}" if poster_path.startswith("/") else poster_path
    if backdrop_path and isinstance(backdrop_path, str) and backdrop_path.strip():
        return f"{TMDB_IMAGE_BACKDROP}{backdrop_path}" if backdrop_path.startswith("/") else backdrop_path
    return None


def post_to_tumblr(
    client,
    blog_name: str,
    image_url: str,
    caption: str,
    click_through_url: str,
    tags: List[str],
    state: str = "published"
) -> Dict[str, Any]:
    """Publish a photo post to Tumblr using pytumblr client."""
    return client.create_photo(
        blog_name,
        state=state,
        tags=tags,
        caption=caption,
        source=image_url,
        link=click_through_url
    )

def main():
    parser = argparse.ArgumentParser(description="CineStories Tumblr Auto-Poster")
    parser.add_argument("--limit", type=int, default=TUMBLR_DAILY_POST_LIMIT, help="Max posts to publish in this run")
    parser.add_argument("--state", type=str, default=TUMBLR_POST_STATE, choices=["published", "queue", "draft"], help="Post state")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without posting")
    parser.add_argument("--slug", type=str, help="Post a specific movie by slug")
    args = parser.parse_args()

    print("=" * 60)
    print("  CineStories - Tumblr Auto-Poster (sumits7196)")
    print("=" * 60)

    # Check for Tumblr credentials
    if not args.dry_run and not (TUMBLR_CONSUMER_KEY and TUMBLR_CONSUMER_SECRET and TUMBLR_OAUTH_TOKEN and TUMBLR_OAUTH_SECRET):
        print("[NOTICE] Tumblr API credentials not fully configured.")
        print("To enable auto-posting, set TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET,")
        print("TUMBLR_OAUTH_TOKEN, and TUMBLR_OAUTH_SECRET in .env or GitHub Secrets.")
        print("Run 'python tumblr_auth.py' to generate your OAuth tokens easily.")
        print("[EXIT] Skipping Tumblr posting gracefully.")
        sys.exit(0)

    client = None
    if not args.dry_run:
        try:
            import pytumblr
            client = pytumblr.TumblrRestClient(
                TUMBLR_CONSUMER_KEY,
                TUMBLR_CONSUMER_SECRET,
                TUMBLR_OAUTH_TOKEN,
                TUMBLR_OAUTH_SECRET
            )
        except ImportError:
            print("[ERROR] pytumblr is not installed. Run: pip install pytumblr")
            sys.exit(1)

    # Load articles
    articles = load_json(ARTICLES_JSON_PATH)
    if not articles:
        print(f"[WARN] No articles found at {ARTICLES_JSON_PATH}. Run fetch_and_generate.py first.")
        sys.exit(0)

    registry = load_tumblr_registry()
    published_set = set(registry.get("published_movies", {}).keys())

    # Candidate selection
    candidates = []
    for art in articles:
        movie = art.get("movie", {})
        slug = movie.get("slug")
        if not slug:
            continue
        if args.slug and slug != args.slug:
            continue
        if slug in published_set and not args.slug:
            continue

        # STRICT RULE: Must exist on the website (story or article in dist)
        story_exists = (STORIES_DIR / slug / "index.html").exists()
        article_exists = (ARTICLES_DIR / slug / "index.html").exists()
        if not story_exists and not article_exists:
            # Skip if content not generated on the site yet
            continue

        # STRICT RULE: Must have verified high-res image
        img_url = get_image_url(movie)
        if not img_url or not (img_url.startswith("http://") or img_url.startswith("https://")):
            continue

        candidates.append((art, img_url))


    if not candidates:
        print("[INFO] No new unposted movies found for Tumblr. All up to date!")
        sys.exit(0)

    to_post = candidates[:args.limit]
    print(f"[INFO] Selected {len(to_post)} candidate movie(s) to post (State: {args.state}, Dry Run: {args.dry_run})")

    posted_count = 0
    for idx, (art, img_url) in enumerate(to_post, 1):
        movie = art.get("movie", {})
        title = movie.get("title", "Unknown")
        slug = movie.get("slug")
        click_url = f"{DOMAIN_NAME}/stories/{slug}/"
        caption = format_tumblr_caption(art, DOMAIN_NAME)
        tags = build_tumblr_tags(art)

        print(f"\n[{idx}/{len(to_post)}] Processing '{title}' (slug: {slug})...")
        print(f"  • Image: {img_url}")
        print(f"  • Tags: {', '.join(tags[:6])}...")

        if args.dry_run:
            print("  [DRY-RUN] Post prepared successfully. Preview caption:")
            print("  " + caption.replace("\n", "\n  ")[:250] + "...")
            continue

        try:
            resp = post_to_tumblr(
                client=client,
                blog_name=TUMBLR_BLOG_NAME,
                image_url=img_url,
                caption=caption,
                click_through_url=click_url,
                tags=tags,
                state=args.state
            )

            post_id = resp.get("id") or resp.get("id_string")
            if post_id:
                print(f"  🎉 [SUCCESS] Published to Tumblr! Post ID: {post_id}")
                registry["published_movies"][slug] = {
                    "id": post_id,
                    "title": title,
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "state": args.state,
                    "url": f"https://{TUMBLR_BLOG_NAME}.tumblr.com/post/{post_id}"
                }
                posted_count += 1
            else:
                print(f"  [WARN] Unexpected Tumblr response: {resp}")

        except Exception as e:
            print(f"  [ERROR] Failed to post '{title}' to Tumblr: {e}")

        # Rate pacing
        if idx < len(to_post):
            time.sleep(3)

    if not args.dry_run and posted_count > 0:
        save_tumblr_registry(registry)
        print(f"\n[DONE] Successfully posted {posted_count} story/stories to Tumblr ({TUMBLR_BLOG_NAME})!")

if __name__ == "__main__":
    main()
