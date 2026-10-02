"""
AI Generation Layer for CineStories.
Transforms raw TMDB movie metadata into punchy, mobile-optimized AMP Story slides
using Google Gemini API with Structured Outputs.
"""

import json
import os
import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from config import GEMINI_API_KEY, GEMINI_MODEL, DOMAIN_NAME
from curated_stories import CURATED_STORIES

# Structured Output Schemas
class SlideData(BaseModel):
    id: str = Field(description="Unique slide page ID, e.g. 'page-1', 'page-2'")
    badge: str = Field(description="Short uppercase kicker/badge (e.g., 'THE PREMISE', 'STAR POWER', 'BEHIND THE LENS', 'INSIDER TRIVIA', 'FAN THEORIES', 'DON'T MISS')")
    title: str = Field(description="Snappy headline for the slide, under 35 characters")
    text: str = Field(description="Bite-sized story text. STRICTLY maximum 40 words. Engaging, snackable, spoiler-free.")
    backdrop_index: int = Field(description="0-based index of backdrop image to display from the backdrops list")
    cta_text: Optional[str] = Field(default=None, description="Optional call-to-action button text, used on the final slide")
    cta_url: Optional[str] = Field(default=None, description="Optional CTA outlink URL")

class WebStoryData(BaseModel):
    title: str = Field(description="Catchy SEO Title under 70 characters optimized for Google Discover & Search CTR")
    seo_description: str = Field(description="SEO meta description under 155 characters summarizing the story")
    slides: List[SlideData] = Field(description="Sequence of 5 to 7 slides following the mandatory narrative arc")

class AIGenerator:
    def __init__(self, api_key: Optional[str] = None, model: str = GEMINI_MODEL):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model = model
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print(f"[AI] Initialized Google GenAI client with model: {self.model}")
            except Exception as e:
                print(f"[AI] Warning: Failed to initialize Google GenAI SDK: {e}")
                self.client = None

    @property
    def is_available(self) -> bool:
        return self.client is not None

    def generate_story(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured story content for a movie.
        Uses Gemini API if available, otherwise falls back to deterministic smart synthesizer.
        """
        if self.is_available:
            try:
                story = self._generate_with_gemini(movie)
                if story and len(story.get("slides", [])) >= 5:
                    return story
            except Exception as e:
                print(f"[AI] Gemini generation failed for '{movie.get('title')}': {e}. Falling back to rule-based synthesizer.")

        return self._generate_fallback(movie)

    def _generate_with_gemini(self, movie: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call Gemini API with structured output prompting."""
        prompt = f"""
You are an expert Hollywood entertainment journalist and mobile visual storytelling editor.
Transform the following raw movie data into an AMP Web Story designed for maximum engagement on Google Discover.

MOVIE DATA:
- Title: {movie.get('title')}
- Release Date: {movie.get('release_date')}
- Tagline: {movie.get('tagline') or 'N/A'}
- Genres: {', '.join(movie.get('genres', []))}
- Director: {movie.get('director')}
- Top Cast: {', '.join(movie.get('top_cast', []))}
- Overview: {movie.get('overview')}
- Audience Rating: {movie.get('vote_average')}/10 ({movie.get('vote_count')} votes)
- Runtime: {movie.get('runtime')} mins
- Category: {movie.get('category')}
- Available Backdrops Count: {len(movie.get('backdrops', []))}

STRICT EDITORIAL & AMP COMPLIANCE RULES:
1. Story Title: Catchy, high-CTR SEO title under 70 characters (e.g. "Dune Part Two: 5 Mind-Blowing Secrets You Missed").
2. Number of Slides: Produce between 5 and 7 slides total.
3. Slide Sequence:
   - Slide 1 (Cover): Movie title, release status, and an irresistible curiosity hook.
   - Slide 2: Plot premise / Core conflict (spoiler-free, snappy).
   - Slide 3: Cast highlight / Star performances & director vision.
   - Slide 4: Behind-the-scenes trivia / visual spectacle / stunt facts.
   - Slide 5: Fan theories / critical buzz / cultural impact.
   - Slide 6 or 7 (Final Slide): Call-to-action slide (e.g., "Check upcoming showtimes", "Add to watchlist").
4. WORD LIMIT: Each slide's text MUST be STRICTLY UNDER 40 WORDS. Bite-sized, snackable, punchy.
5. Provide a valid 'backdrop_index' for each slide (integers between 0 and {max(0, len(movie.get('backdrops', [])) - 1)}).
6. Set 'cta_text' on the final slide (e.g., "Get Tickets & Showtimes") and 'cta_url' to "https://www.themoviedb.org/movie/{movie.get('id')}".
"""

        candidate_models = [self.model]
        for fallback in ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        for m in candidate_models:
            # 1. Try Interactions API (Gemini 3 SDK)
            try:
                interaction = self.client.interactions.create(
                    model=m,
                    input=prompt,
                    response_format=[
                        {
                            "type": "text",
                            "mime_type": "application/json",
                            "schema": WebStoryData.model_json_schema(),
                        }
                    ],
                )
                raw_text = interaction.output_text
                if raw_text:
                    data = json.loads(raw_text)
                    print(f"[AI] Successfully synthesized story with model: {m} (Interactions API)")
                    return self._sanitize_story_data(data, movie)
            except Exception as e_interact:
                pass

            # 2. Try models.generate_content
            try:
                response = self.client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": WebStoryData,
                    }
                )
                if response and response.text:
                    data = json.loads(response.text)
                    print(f"[AI] Successfully synthesized story with model: {m} (generate_content)")
                    return self._sanitize_story_data(data, movie)
            except Exception as e_gen:
                pass

            # 3. Direct REST API fallback
            try:
                import requests
                rest_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
                rest_payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "responseSchema": WebStoryData.model_json_schema()
                    }
                }
                resp = requests.post(rest_url, json=rest_payload, timeout=20)
                if resp.status_code == 200:
                    cand = resp.json().get("candidates", [])[0]
                    content_text = cand.get("content", {}).get("parts", [])[0].get("text", "")
                    if content_text:
                        data = json.loads(content_text)
                        print(f"[AI] Successfully synthesized story with model: {m} (REST API)")
                        return self._sanitize_story_data(data, movie)
            except Exception:
                pass

        print(f"[AI] All candidate models exhausted for '{movie.get('title')}'. Falling back to rule-based narrative synthesizer.")
        return None

    def _sanitize_story_data(self, data: Dict[str, Any], movie: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure title length, word limits, and slide constraints are strictly met."""
        title = data.get("title", f"{movie.get('title')}: Everything You Need To Know")[:70].strip()
        seo_description = data.get("seo_description", movie.get("overview", "")[:150]).strip()
        
        raw_slides = data.get("slides", [])
        clean_slides = []
        max_backdrops = max(1, len(movie.get("backdrops", [])))

        for i, s in enumerate(raw_slides):
            words = s.get("text", "").split()
            # Enforce 40 words max per AMP Web Story guidelines
            if len(words) > 40:
                truncated_text = " ".join(words[:40]) + "..."
            else:
                truncated_text = " ".join(words)

            backdrop_idx = s.get("backdrop_index", i % max_backdrops)
            if not isinstance(backdrop_idx, int) or backdrop_idx >= max_backdrops:
                backdrop_idx = i % max_backdrops

            clean_slides.append({
                "id": f"page-{i+1}",
                "badge": s.get("badge", f"HIGHLIGHT #{i+1}").upper(),
                "title": s.get("title", f"Slide {i+1}")[:45],
                "text": truncated_text,
                "backdrop_index": backdrop_idx,
                "cta_text": s.get("cta_text"),
                "cta_url": s.get("cta_url") or f"https://www.themoviedb.org/movie/{movie.get('id')}"
            })

        # Ensure final slide has CTA
        if clean_slides and not clean_slides[-1].get("cta_text"):
            clean_slides[-1]["cta_text"] = "Explore Full Details & Tickets"
            clean_slides[-1]["cta_url"] = f"https://www.themoviedb.org/movie/{movie.get('id')}"

        return {
            "title": title,
            "seo_description": seo_description,
            "movie": movie,
            "slides": clean_slides
        }

    def _generate_fallback(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic, high-quality story synthesizer with punchy, viral headlines.
        """
        slug = movie.get("slug", "")
        if slug in CURATED_STORIES:
            curated = CURATED_STORIES[slug]
            max_backdrops = max(1, len(movie.get("backdrops", [])))
            slides = []
            for s in curated.get("slides", []):
                slide_copy = dict(s)
                slide_copy["backdrop_index"] = slide_copy.get("backdrop_index", 0) % max_backdrops
                slides.append(slide_copy)
            return {
                "title": curated.get("title", movie.get("hook_title", movie.get("title"))),
                "seo_description": curated.get("seo_description", movie.get("overview", "")[:150]),
                "movie": movie,
                "slides": slides
            }

        title = movie.get("hook_title") or f"{movie.get('title')}: The Untold Story & Secrets"[:68]
        release_date = movie.get("release_date", "Trending")
        director = movie.get("director", "Visionary Creator")
        cast = movie.get("top_cast", ["Hollywood Stars"])
        cast_str = ", ".join(cast[:3]) if cast else "An all-star cast"
        tagline = movie.get("tagline") or f"Experience the global phenomenon of {movie.get('title')}."
        genres = ", ".join(movie.get("genres", ["Cinema"]))
        rating = movie.get("vote_average", 8.4)
        overview = movie.get("overview", "")
        max_backdrops = max(1, len(movie.get("backdrops", [])))
        is_tv = movie.get("media_type") == "tv"
        is_cult = movie.get("category") == "cult_classic"

        # Punchy badge
        if is_tv:
            badge_1 = "🔥 BINGE PHENOMENON"
            badge_2 = "THE MASTERMIND PLOT"
        elif is_cult:
            badge_1 = "💀 CULT LEGEND"
            badge_2 = "THE TERRIFYING PREMISE"
        else:
            badge_1 = "⚡ BLOCKBUSTER ALERT"
            badge_2 = "THE EPIC CONFLICT"

        # Truncate overview for slide 2 under 36 words
        ov_words = overview.split()
        if len(ov_words) > 34:
            plot_text = " ".join(ov_words[:34]) + "..."
        else:
            plot_text = " ".join(ov_words) if ov_words else f"A pulse-pounding masterpiece in {genres}."

        slides = [
            # Slide 1: Cover Hook
            {
                "id": "page-1",
                "badge": badge_1,
                "title": movie.get("title")[:35],
                "text": f"{tagline} Rated {rating}/10 with millions of obsessed fans worldwide. Here is why you cannot look away.",
                "backdrop_index": 0,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 2: Plot hook
            {
                "id": "page-2",
                "badge": badge_2,
                "title": "Shocking Twist Ahead",
                "text": plot_text,
                "backdrop_index": 1 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 3: Cast highlight
            {
                "id": "page-3",
                "badge": "STAR POWER",
                "title": "Powerhouse Ensemble",
                "text": f"Led by {cast_str}, the film boasts phenomenal on-screen chemistry and career-defining performances directed by {director}.",
                "backdrop_index": 2 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 4: Behind the scenes / Spectacle
            {
                "id": "page-4",
                "badge": "BEHIND THE LENS",
                "title": f"Directed by {director}",
                "text": f"Filmmaker {director} pushed cinematic boundaries with practical stunts and groundbreaking IMAX visuals for total audience immersion.",
                "backdrop_index": 3 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 5: Critical Reception & Buzz
            {
                "id": "page-5",
                "badge": "AUDIENCE REACTION",
                "title": f"Rated {rating}/10 on TMDB",
                "text": f"With an impressive {rating}/10 community score, fans and critics hail it as one of the year's standout theatrical events.",
                "backdrop_index": 4 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 6: Final CTA slide
            {
                "id": "page-6",
                "badge": "YOUR TICKET",
                "title": "Catch It On The Big Screen",
                "text": f"Ready to dive into {movie.get('title')}? Discover showtimes, official trailers, and cast interviews today.",
                "backdrop_index": 0,
                "cta_text": "Check Showtimes & Full Details",
                "cta_url": f"https://www.themoviedb.org/movie/{movie.get('id')}"
            }
        ]

        return {
            "title": title,
            "seo_description": f"Discover {movie.get('title')}: cast, plot, behind-the-scenes trivia, and audience buzz in this visual AMP Web Story.",
            "movie": movie,
            "slides": slides
        }
