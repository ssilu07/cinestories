"""
TMDB API Client module for CineStories.
Fetches Hollywood Movies, Blockbuster TV Series, and Cult Classics
with full credits, seasons, and backdrops.
"""

import re
import time
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

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Execute resilient GET request to TMDB API with exponential backoff retry.
        Guarantees pipeline never crashes on intermittent 429 rate-limits or 5xx server glitches.
        """
        if not self.has_api_key:
            return None
        
        url = f"{TMDB_BASE_URL}{endpoint}"
        query = {**self.auth_params, **(params or {})}
        
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, params=query, timeout=15)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429 or resp.status_code >= 500:
                    wait_time = (2 ** attempt) + 1
                    print(f"[TMDB] Rate-limit/Server status {resp.status_code} on {endpoint}. Backing off for {wait_time}s (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"[TMDB] Warning: {endpoint} returned status {resp.status_code}: {resp.text[:120]}")
                    return None
            except requests.exceptions.RequestException as e:
                wait_time = (2 ** attempt) + 1
                print(f"[TMDB] Connection error on {endpoint}: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            except Exception as e:
                print(f"[TMDB] Unexpected error connecting to {endpoint}: {e}")
                return None
        
        print(f"[TMDB] Failed to fetch {endpoint} after {max_retries} attempts.")
        return None

    def get_items_by_category(self, category: str, limit: int = 15, exclude_slugs: Optional[set] = None) -> List[Dict[str, Any]]:
        """
        Fetch items by category: 'trending', 'series', 'cult_classic', 'upcoming', 'now_playing'.
        Optionally skips items whose slugs are already in exclude_slugs to save API budget and avoid duplicates.
        """
        endpoint_map = {
            "upcoming": ("/movie/upcoming", "movie", {}),
            "now_playing": ("/movie/now_playing", "movie", {}),
            "trending": ("/trending/movie/day", "movie", {}),
            "series": ("/tv/popular", "tv", {}),
            "popular_series": ("/tv/popular", "tv", {}),
            "cult_classic": ("/movie/top_rated", "movie", {}),
            "streaming_charts": ("/trending/tv/week", "tv", {}),
            "theories_easter_eggs": ("/discover/movie", "movie", {"with_genres": "878,28", "sort_by": "popularity.desc"}),
            "where_are_they_now": ("/discover/tv", "tv", {"sort_by": "vote_count.desc", "first_air_date.lte": "2018-01-01"}),
            "steamy_thrillers": ("/discover/movie", "movie", {"with_genres": "53,10749", "sort_by": "popularity.desc"})
        }

        entry = endpoint_map.get(category, ("/trending/movie/day", "movie", {}))
        endpoint = entry[0]
        media_type = entry[1]
        extra_params = entry[2] if len(entry) > 2 else {}
        
        if self.has_api_key:
            detailed_items = []
            max_pages = 10  # Search up to 10 pages deep to find fresh, unposted titles
            for page in range(1, max_pages + 1):
                req_params = {"language": "en-US", "page": page}
                req_params.update(extra_params)
                data = self._get(endpoint, req_params)
                if not data or "results" not in data or not data["results"]:
                    break
                items = data["results"]
                for item in items:
                    cand_name = item.get("title") or item.get("name") or ""
                    cand_slug = slugify(cand_name)
                    if exclude_slugs and cand_slug in exclude_slugs:
                        continue
                    if media_type == "tv":
                        detailed = self.get_tv_details(item["id"], category=category)
                    else:
                        detailed = self.get_movie_details(item["id"], category=category)
                    if detailed:
                        detailed_items.append(detailed)
                        if len(detailed_items) >= limit:
                            break
                if len(detailed_items) >= limit:
                    break
                if page >= data.get("total_pages", 1):
                    break

            if detailed_items:
                return detailed_items

        # Fallback to sample dataset
        print(f"[TMDB] Using built-in sample data for category: '{category}'")
        filtered = [m for m in SAMPLE_MEDIA if m.get("category") == category]
        if not filtered:
            filtered = SAMPLE_MEDIA
        if exclude_slugs:
            filtered = [m for m in filtered if m.get("slug") not in exclude_slugs]

        # If all sample media are already published, create fresh numbered variants in demo mode
        if not filtered and exclude_slugs:
            import copy
            base_items = [m for m in SAMPLE_MEDIA if m.get("category") == category] or SAMPLE_MEDIA
            filtered = []
            for m in base_items[:limit]:
                m_copy = copy.deepcopy(m)
                v_num = 2
                while f"{m_copy['slug']}-vol-{v_num}" in exclude_slugs:
                    v_num += 1
                m_copy["slug"] = f"{m_copy['slug']}-vol-{v_num}"
                m_copy["title"] = f"{m_copy['title']} (Part {v_num})"
                filtered.append(m_copy)

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

    def fetch_feed(self, categories: Optional[List[str]] = None, per_category: int = 15, exclude_slugs: Optional[set] = None) -> List[Dict[str, Any]]:
        """
        Fetch combined unique movies and TV series across requested categories.
        Skips titles in exclude_slugs to ensure only fresh, unpublished content is fetched.
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
            items = self.get_items_by_category(cat, limit=per_category, exclude_slugs=exclude_slugs)
            for item in items:
                unique_key = f"{item.get('media_type', 'movie')}_{item.get('id')}"
                if unique_key not in seen_ids:
                    seen_ids.add(unique_key)
                    all_items.append(item)

        return all_items
