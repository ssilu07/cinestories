"""
TMDB API Client module for CineStories.
Fetches upcoming, now playing, and trending movies with full credits and backdrops.
"""

import re
import requests
from typing import List, Dict, Any, Optional
from config import TMDB_API_KEY, TMDB_IMAGE_ORIGINAL, TMDB_IMAGE_POSTER
from sample_data import SAMPLE_MOVIES

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

    def get_movies_by_category(self, category: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch movies by category: 'upcoming', 'now_playing', or 'trending'.
        """
        endpoint_map = {
            "upcoming": "/movie/upcoming",
            "now_playing": "/movie/now_playing",
            "trending": "/trending/movie/week"
        }

        endpoint = endpoint_map.get(category, "/trending/movie/week")
        
        if self.has_api_key:
            data = self._get(endpoint, {"language": "en-US", "page": 1})
            if data and "results" in data:
                movies = data["results"][:limit]
                detailed_movies = []
                for m in movies:
                    detailed = self.get_movie_details(m["id"], category=category)
                    if detailed:
                        detailed_movies.append(detailed)
                if detailed_movies:
                    return detailed_movies

        # Fallback to high-fidelity sample data if no key or API call failed
        print(f"[TMDB] Using built-in sample data for category: '{category}'")
        filtered = [m for m in SAMPLE_MOVIES if m.get("category") == category]
        if not filtered:
            filtered = SAMPLE_MOVIES
        return filtered[:limit]

    def get_movie_details(self, movie_id: int, category: str = "trending") -> Optional[Dict[str, Any]]:
        """
        Fetch complete details, credits (director, top cast), and backdrops in 1 call.
        """
        data = self._get(f"/movie/{movie_id}", {
            "append_to_response": "credits,images",
            "include_image_language": "en,null"
        })
        
        if not data:
            return None

        # Extract director
        director = "Acclaimed Filmmaker"
        crew = data.get("credits", {}).get("crew", [])
        for member in crew:
            if member.get("job") == "Director":
                director = member.get("name", director)
                break

        # Extract top 6 cast
        cast_list = data.get("credits", {}).get("cast", [])
        top_cast = [c.get("name") for c in cast_list[:6] if c.get("name")]

        # Extract high quality backdrops
        raw_backdrops = data.get("images", {}).get("backdrops", [])
        backdrops = [b.get("file_path") for b in raw_backdrops if b.get("file_path")]
        
        # Primary backdrop fallback
        primary_backdrop = data.get("backdrop_path")
        if primary_backdrop and primary_backdrop not in backdrops:
            backdrops.insert(0, primary_backdrop)
        
        # If no backdrops, use poster as last resort
        if not backdrops and data.get("poster_path"):
            backdrops.append(data.get("poster_path"))

        genres = [g.get("name") for g in data.get("genres", []) if g.get("name")]

        title = data.get("title") or data.get("original_title") or "Untitled Movie"
        slug = slugify(title)

        return {
            "id": data.get("id"),
            "title": title,
            "original_title": data.get("original_title", title),
            "slug": slug,
            "release_date": data.get("release_date", "Coming Soon"),
            "overview": data.get("overview", "An upcoming cinematic spectacle."),
            "tagline": data.get("tagline", ""),
            "genres": genres,
            "runtime": data.get("runtime", 120),
            "vote_average": round(data.get("vote_average", 0.0), 1),
            "vote_count": data.get("vote_count", 0),
            "category": category,
            "director": director,
            "top_cast": top_cast,
            "poster_path": data.get("poster_path", ""),
            "backdrop_path": primary_backdrop or (backdrops[0] if backdrops else ""),
            "backdrops": backdrops[:8]
        }

    def fetch_feed(self, categories: Optional[List[str]] = None, per_category: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch combined unique movies across requested categories.
        """
        cats = categories or ["trending", "upcoming", "now_playing"]
        all_movies = []
        seen_ids = set()

        for cat in cats:
            movies = self.get_movies_by_category(cat, limit=per_category)
            for m in movies:
                m_id = m.get("id")
                if m_id not in seen_ids:
                    seen_ids.add(m_id)
                    all_movies.append(m)

        return all_movies
