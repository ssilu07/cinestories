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

class ArticleSection(BaseModel):
    heading: str = Field(description="Snappy section subheading under 50 characters")
    content: str = Field(description="Paragraph of rich editorial commentary (60-120 words)")

class DiscoverArticleData(BaseModel):
    headline: str = Field(description="Catchy, high-CTR Google Discover headline under 75 characters")
    meta_description: str = Field(description="SEO meta description under 155 characters summarizing the article")
    key_takeaways: List[str] = Field(description="3 to 4 punchy bullet points summarizing key facts for readers")
    sections: List[ArticleSection] = Field(description="3 to 4 rich editorial sections covering plot twists, casting, trivia, and reception")
    verdict_summary: str = Field(description="Editor's final takeaway / streaming or theater verdict")
    reading_time_mins: int = Field(default=3, description="Estimated reading time in minutes (usually 3 or 4)")

class AIGenerator:
    def __init__(self, api_key: Optional[str] = None, model: str = GEMINI_MODEL):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model = model
        self.client = None
        self.ai_disabled = False

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
        return self.client is not None and not self.ai_disabled

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

CATEGORY-SPECIFIC EDITORIAL ANGLE:
- If Category is 'streaming_charts': Focus on weekly US & UK streaming viewership ranks (Netflix/HBO/Prime), million hours viewed, chart dominance, and why audiences can't stop binging.
- If Category is 'theories_easter_eggs': Focus on post-credit scene breakdown, hidden comic easter eggs, Marvel/DC multiverse connections, villain reveals, and Secret Wars / DCU fan theories.
- If Category is 'where_are_they_now': Focus on popular 90s/2000s sitcom stars, then-vs-now transformations, career shifts, secret hobbies (e.g. racing, directing, writing), net worth, and life today.

STRICT EDITORIAL & AMP COMPLIANCE RULES:
1. Story Title: Catchy, high-CTR SEO title under 70 characters with emojis (e.g. "Top 10 Streaming Hits This Week in US/UK 🍿📊", "Marvel Post-Credits: 6 Insane Easter Eggs 🦸‍♂️⚡", "Friends: Where Are The Central Perk Stars Today? ☕✨").
2. Number of Slides: Produce between 5 and 7 slides total.
3. Slide Sequence:
   - Slide 1 (Cover): Title, category context, and an irresistible curiosity hook.
   - Slide 2: Core premise / #1 streaming rank / first big easter egg / lead sitcom star update.
   - Slide 3: Major highlight / key characters or chart-toppers / director or actor transformation.
   - Slide 4: Behind-the-scenes trivia / shock theory / wild career transition.
   - Slide 5: Cultural impact / fan community debate / lasting legacy.
   - Slide 6 or 7 (Final Slide): Call-to-action slide (e.g., "Explore Weekly Streaming Charts", "See All Marvel Theories", "Watch Sitcom Retrospectives").
4. WORD LIMIT: Each slide's text MUST be STRICTLY UNDER 40 WORDS. Bite-sized, snackable, punchy.
5. Provide a valid 'backdrop_index' for each slide (integers between 0 and {max(0, len(movie.get('backdrops', [])) - 1)}).
6. Set 'cta_text' on the final slide and 'cta_url' to "https://www.themoviedb.org/movie/{movie.get('id')}" or "https://www.themoviedb.org/tv/{movie.get('id')}".
"""

        models_to_try = [self.model]
        if "gemini-2.5-flash" not in models_to_try:
            models_to_try.append("gemini-2.5-flash")

        for m in models_to_try:
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
                    print(f"[AI] Successfully synthesized story with model: {m}")
                    return self._sanitize_story_data(data, movie)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "401" in err_str or "API_KEY_INVALID" in err_str:
                    print(f"[AI] Gemini quota limit or auth error ({e}). Disabling AI for remaining stories to ensure fast generation.")
                    self.ai_disabled = True
                    return None
                print(f"[AI] Notice: Generation with {m} failed: {e}")

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
        category = movie.get("category", "")
        is_tv = movie.get("media_type") == "tv"
        is_cult = category == "cult_classic"
        is_streaming = category == "streaming_charts"
        is_theories = category == "theories_easter_eggs"
        is_sitcom = category == "where_are_they_now"

        # Punchy badge
        if is_streaming:
            badge_1 = "📊 WEEKLY LEADERBOARD"
            badge_2 = "STREAMING #1 BREAKDOWN"
        elif is_theories:
            badge_1 = "🦸‍♂️ MULTIVERSE DECODED"
            badge_2 = "THE POST-CREDIT CLUE"
        elif is_sitcom:
            badge_1 = "🕰️ WHERE ARE THEY NOW?"
            badge_2 = "THE ICONIC ERA"
        elif is_tv:
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

    def generate_article(self, movie: Dict[str, Any], story: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate structured Google Discover article for a movie.
        Uses Gemini API if available, otherwise falls back to smart editorial synthesizer.
        """
        if self.is_available:
            try:
                article = self._generate_article_with_gemini(movie, story)
                if article and len(article.get("sections", [])) >= 3:
                    article["movie"] = movie
                    return article
            except Exception as e:
                print(f"[AI] Gemini article generation failed for '{movie.get('title')}': {e}. Falling back to rule-based synthesizer.")

        return self._generate_article_fallback(movie, story)

    def _generate_article_with_gemini(self, movie: Dict[str, Any], story: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Call Gemini API with structured output prompting for Google Discover Article."""
        story_highlights = ""
        if story and story.get("slides"):
            story_highlights = "\n".join([f"- Slide {i+1}: {s.get('title')} - {s.get('text')}" for i, s in enumerate(story.get("slides", []))])

        prompt = f"""
You are an expert Hollywood entertainment journalist and SEO specialist writing for Google Chrome Discover.
Transform the following raw movie data and story highlights into an engaging, high-CTR Google Discover news article.

MOVIE DATA:
- Title: {movie.get('title')}
- Release Date: {movie.get('release_date')}
- Tagline: {movie.get('tagline') or 'N/A'}
- Genres: {', '.join(movie.get('genres', []))}
- Director: {movie.get('director')}
- Top Cast: {', '.join(movie.get('top_cast', []))}
- Overview: {movie.get('overview')}
- Audience Rating: {movie.get('vote_average')}/10
- Category: {movie.get('category')}

STORY HIGHLIGHTS:
{story_highlights}

GOOGLE DISCOVER EDITORIAL GUIDELINES:
1. Headline: Irresistible, curiosity-inducing, authentic under 75 characters (e.g. "Inside The Professor's Ultimate Heist: 5 Tactics You Missed 💰").
2. Meta Description: Under 155 characters summarizing the key hook.
3. Key Takeaways: Exactly 3 to 4 punchy bullet points summarizing key facts for readers.
4. Sections: Exactly 3 to 4 rich editorial sections covering the premise, star performances, behind-the-scenes secrets, and cultural impact (60-120 words each).
5. Verdict Summary: 1-2 punchy concluding sentences with a recommendation.
6. Reading Time: 3 or 4 minutes.
"""
        models_to_try = [self.model]
        if "gemini-2.5-flash" not in models_to_try:
            models_to_try.append("gemini-2.5-flash")

        for m in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": DiscoverArticleData,
                    }
                )
                if response and response.text:
                    data = json.loads(response.text)
                    print(f"[AI] Successfully synthesized Discover article with model: {m}")
                    return data
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "401" in err_str or "API_KEY_INVALID" in err_str:
                    print(f"[AI] Gemini quota limit or auth error ({e}). Disabling AI for remaining articles.")
                    self.ai_disabled = True
                    return None
                print(f"[AI] Notice: Article generation with {m} failed: {e}")

        return None

    def _generate_article_fallback(self, movie: Dict[str, Any], story: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Deterministic, rich editorial synthesizer for Google Discover articles.
        Generates 400+ words of structured journalism with bullet takeaways and sections.
        """
        title = movie.get("title", "Featured Film")
        director = movie.get("director") or "Visionary Filmmakers"
        top_cast = movie.get("top_cast", [])
        cast_str = ", ".join(top_cast[:3]) if top_cast else "an acclaimed ensemble"
        rating = movie.get("vote_average", 7.8)
        genres = movie.get("genres", ["Cinema"])
        genre_str = " & ".join(genres[:2])
        overview = movie.get("overview") or f"{title} continues to captivate global audiences with its gripping storyline and exceptional performances."
        category = movie.get("category", "trending")

        # Use story title / hook if present
        headline = None
        if story and story.get("title"):
            headline = story.get("title")
        elif movie.get("hook_title"):
            headline = movie.get("hook_title")
        else:
            if category == "streaming_charts":
                headline = f"Why {title} Is Dominating Global Streaming Charts This Week 🍿"
            elif category == "theories_easter_eggs":
                headline = f"{title}: 5 Mind-Blowing Easter Eggs & Theories Explained ⚡"
            elif category == "where_are_they_now":
                headline = f"Where Are The Stars of {title} Today? The Shocking Journey ✨"
            else:
                headline = f"{title} Deep Dive: Cast, Hidden Clues & What Critics Are Saying 🎬"

        # Key Takeaways
        takeaways = [
            f"Powerhouse Cast: Led by {cast_str} under the direction of {director}.",
            f"Audience Reception: Currently certified with an impressive {rating}/10 community rating.",
            f"Genre Highlights: A masterclass in {genre_str} storytelling with unforgettable character arcs.",
            f"Watch Format: Available for full cinematic analysis and visual slide exploration."
        ]

        # Sections
        sections = []
        if story and len(story.get("slides", [])) >= 4:
            slides = story.get("slides", [])
            for s in slides[:4]:
                sections.append({
                    "heading": s.get("title", "Key Story Highlight"),
                    "content": f"{s.get('text')} As the story unfolds, the creative decisions made by the filmmakers provide a masterclass in modern visual storytelling that keeps viewers on the edge of their seats."
                })
        else:
            sections = [
                {
                    "heading": f"The High-Stakes Narrative of {title}",
                    "content": f"{overview} What sets this apart is how effectively the script balances intense narrative momentum with nuanced character beats, making every revelation hit with maximum impact."
                },
                {
                    "heading": f"Star Power: {cast_str}",
                    "content": f"The dynamic chemistry between {cast_str} elevates the production into top-tier cinematic territory. Under {director}'s precise direction, each actor brings genuine emotional weight to their respective roles, creating moments that resonate far beyond the final credits."
                },
                {
                    "heading": "Behind The Lens & Technical Precision",
                    "content": f"From intricate production design to a propulsive soundscape, {title} showcases meticulous craftsmanship. Filmmakers favored immersive visual palettes and practical effects where possible, creating a tangible sense of authenticity."
                },
                {
                    "heading": "Cultural Buzz & Why Audiences Are Obsessed",
                    "content": f"With an outstanding {rating}/10 audience score, the title has sparked spirited debates across social media, Reddit discussion threads, and critic roundtables. It represents a bold statement for contemporary {genre_str} entertainment."
                }
            ]

        verdict = f"{title} is an absolute triumph for fans of {genre_str}. With stellar performances from {cast_str} and sharp direction by {director}, it is an essential entry for your watchlist."

        return {
            "headline": headline[:75],
            "meta_description": f"Explore {title}: cast highlights, hidden trivia, critical reception, and streaming breakdown.",
            "key_takeaways": takeaways,
            "sections": sections,
            "verdict_summary": verdict,
            "reading_time_mins": 3,
            "movie": movie
        }
