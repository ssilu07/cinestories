"""
TMDB API Client module for CineStories.
Fetches Hollywood Movies, Blockbuster TV Series, and Cult Classics
with full credits, seasons, and backdrops.
"""

import re
import requests
from typing import List, Dict, Any, Optional
from config import TMDB_API_KEY, TMDB_IMAGE_ORIGINAL, TMDB_IMAGE_POSTER
from sample_data import SAMPLE_MEDIA

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def slugify(text: str) -> str:
    """Generate a clean, SEO-friendly URL slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text or "story"

class TMDBClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or TMDB_API_KEY).strip()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "CineStories/1.0 (WebStoriesBot; +https://cinestories.pages.dev)"
        })
        
        # Determine if api_key is a v4 Bearer token (JWT format) or standard v3 key
        if self.api_key and self.api_key.startswith("eyJ"):
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
            self.auth_params = {}
        elif self.api_key:
            self.auth_params = {"api_key": self.api_key}
        else:
            self.auth_params = {}

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not self.has_api_key:
            return None
        
        url = f"{TMDB_BASE_URL}{endpoint}"
        query = {**self.auth_params, **(params or {})}
        
        try:
            resp = self.session.get(url, params=query, timeout=12)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"[TMDB] Warning: {endpoint} returned status {resp.status_code}: {resp.text[:120]}")
                return None
        except Exception as e:
            print(f"[TMDB] Error connecting to {endpoint}: {e}")
            return None

    def get_items_by_category(self, category: str, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Fetch items by category: 'trending', 'series', 'cult_classic', 'upcoming', 'now_playing'.
        """
        endpoint_map = {
            "upcoming": ("/movie/upcoming", "movie"),
            "now_playing": ("/movie/now_playing", "movie"),
            "trending": ("/trending/movie/week", "movie"),
            "series": ("/trending/tv/week", "tv"),
            "popular_series": ("/tv/popular", "tv"),
            "cult_classic": ("/movie/top_rated", "movie"),
            "streaming_charts": ("/trending/tv/week", "tv"),
            "theories_easter_eggs": ("/trending/movie/week", "movie"),
            "where_are_they_now": ("/tv/popular", "tv"),
            "steamy_thrillers": ("/discover/movie?with_genres=53,10749", "movie")
        }

        endpoint, media_type = endpoint_map.get(category, ("/trending/movie/week", "movie"))
        
        if self.has_api_key:
            data = self._get(endpoint, {"language": "en-US", "page": 1})
            if data and "results" in data:
                items = data["results"][:limit]
                detailed_items = []
                for item in items:
                    if media_type == "tv":
                        detailed = self.get_tv_details(item["id"], category=category)
                    else:
                        detailed = self.get_movie_details(item["id"], category=category)
                    if detailed:
                        detailed_items.append(detailed)
                if detailed_items:
                    return detailed_items

        # Fallback to sample dataset
        print(f"[TMDB] Using built-in sample data for category: '{category}'")
        filtered = [m for m in SAMPLE_MEDIA if m.get("category") == category]
        if not filtered:
            filtered = SAMPLE_MEDIA
        return filtered[:limit]

    def get_movie_details(self, movie_id: int, category: str = "trending") -> Optional[Dict[str, Any]]:
        """Fetch details for a movie."""
        data = self._get(f"/movie/{movie_id}", {
            "append_to_response": "credits,images",
            "include_image_language": "en,null"
        })
        
        if not data:
            return None

        director = "Acclaimed Filmmaker"
        crew = data.get("credits", {}).get("crew", [])
        for member in crew:
            if member.get("job") == "Director":
                director = member.get("name", director)
                break

        cast_list = data.get("credits", {}).get("cast", [])
        top_cast = [c.get("name") for c in cast_list[:6] if c.get("name")]

        raw_backdrops = data.get("images", {}).get("backdrops", [])
        backdrops = [b.get("file_path") for b in raw_backdrops if b.get("file_path")]
        primary_backdrop = data.get("backdrop_path")
        if primary_backdrop and primary_backdrop not in backdrops:
            backdrops.insert(0, primary_backdrop)
        if not backdrops and data.get("poster_path"):
            backdrops.append(data.get("poster_path"))

        genres = [g.get("name") for g in data.get("genres", []) if g.get("name")]
        title = data.get("title") or data.get("original_title") or "Untitled Movie"

        return {
            "id": data.get("id"),
            "title": title,
            "original_title": data.get("original_title", title),
            "slug": slugify(title),
            "media_type": "movie",
            "release_date": data.get("release_date", "Coming Soon"),
            "overview": data.get("overview", "A cinematic Hollywood spectacle."),
            "tagline": data.get("tagline", ""),
            "genres": genres,
            "runtime": data.get("runtime", 120),
            "seasons": None,
            "vote_average": round(data.get("vote_average", 0.0), 1),
            "vote_count": data.get("vote_count", 0),
            "category": category,
            "director": director,
            "top_cast": top_cast,
            "poster_path": data.get("poster_path", ""),
            "backdrop_path": primary_backdrop or (backdrops[0] if backdrops else ""),
            "backdrops": backdrops[:8]
        }

    def get_tv_details(self, tv_id: int, category: str = "series") -> Optional[Dict[str, Any]]:
        """Fetch details for a TV Series / Show."""
        data = self._get(f"/tv/{tv_id}", {
            "append_to_response": "credits,images",
            "include_image_language": "en,null"
        })
        
        if not data:
            return None

        # Extract creators / showrunner
        creators = [c.get("name") for c in data.get("created_by", []) if c.get("name")]
        creator_name = ", ".join(creators) if creators else "Visionary Showrunner"

        cast_list = data.get("credits", {}).get("cast", [])
        top_cast = [c.get("name") for c in cast_list[:6] if c.get("name")]

        raw_backdrops = data.get("images", {}).get("backdrops", [])
        backdrops = [b.get("file_path") for b in raw_backdrops if b.get("file_path")]
        primary_backdrop = data.get("backdrop_path")
        if primary_backdrop and primary_backdrop not in backdrops:
            backdrops.insert(0, primary_backdrop)
        if not backdrops and data.get("poster_path"):
            backdrops.append(data.get("poster_path"))

        genres = [g.get("name") for g in data.get("genres", []) if g.get("name")]
        title = data.get("name") or data.get("original_name") or "Hit TV Series"
        seasons = data.get("number_of_seasons", 1)
        runtime_list = data.get("episode_run_time") or []
        runtime = runtime_list[0] if runtime_list else 50

        return {
            "id": data.get("id"),
            "title": title,
            "original_title": data.get("original_name", title),
            "slug": slugify(title),
            "media_type": "tv",
            "release_date": data.get("first_air_date", "TV Series"),
            "overview": data.get("overview", "A binge-worthy television phenomenon."),
            "tagline": data.get("tagline", ""),
            "genres": genres,
            "runtime": runtime,
            "seasons": seasons,
            "vote_average": round(data.get("vote_average", 0.0), 1),
            "vote_count": data.get("vote_count", 0),
            "category": "series",
            "director": f"{creator_name} (Creator)",
            "top_cast": top_cast,
            "poster_path": data.get("poster_path", ""),
            "backdrop_path": primary_backdrop or (backdrops[0] if backdrops else ""),
            "backdrops": backdrops[:8]
        }

    def fetch_feed(self, categories: Optional[List[str]] = None, per_category: int = 15) -> List[Dict[str, Any]]:
        """
        Fetch combined unique movies and TV series across requested categories.
        """
        cats = categories or [
            "streaming_charts",
            "theories_easter_eggs",
            "where_are_they_now",
            "series",
            "trending",
            "cult_classic",
            "upcoming"
        ]
        all_items = []
        seen_ids = set()

        for cat in cats:
            items = self.get_items_by_category(cat, limit=per_category)
            for item in items:
                unique_key = f"{item.get('media_type', 'movie')}_{item.get('id')}"
                if unique_key not in seen_ids:
                    seen_ids.add(unique_key)
                    all_items.append(item)

        return all_items
