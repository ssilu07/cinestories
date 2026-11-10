"""
AI Generation Layer for CineStories.
Transforms raw TMDB movie metadata into punchy, mobile-optimized AMP Story slides
using Google Gemini API with Structured Outputs.
"""

import json
import os
import re
import time
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DOMAIN_NAME,
    API_PACING_SECONDS,
    MIN_ARTICLE_WORDS
)
from curated_stories import CURATED_STORIES
from curated_articles import CURATED_ARTICLES

# Structured Output Schemas
class PollData(BaseModel):
    id: str = Field(description="Unique poll ID, e.g. 'poll-slug-climax'")
    type: str = Field(default="binary", description="Poll type, always 'binary'")
    prompt: str = Field(description="High-engagement binary controversy question under 45 characters, e.g. 'Did he survive the climax?' or 'Was the twist staged?'")
    option1: str = Field(description="Option 1 text under 20 characters, e.g. 'Yes, survived 🔥' or 'Real truth'")
    option2: str = Field(description="Option 2 text under 20 characters, e.g. 'No, hallucination 💀' or 'Staged drama'")

class SlideData(BaseModel):
    id: str = Field(description="Unique slide page ID, e.g. 'page-1', 'page-2'")
    badge: str = Field(description="High-voltage viral kicker badge with emoji (e.g., '🔥 CLIMAX TWIST', '⚡ ENDING DECODED', '🔍 CLUE #1', '❓ BURNING MYSTERY', '💡 THE DECODED TRUTH', '🎬 POST-CREDITS LORE', '🩸 TRUE STORY FACTS', '🗳️ FAN VERDICT POLL')")
    title: str = Field(description="Curiosity-inducing headline under 35 characters that commands reader attention")
    text: str = Field(description="Bite-sized story text revealing scene clues, twists, or theories. STRICTLY maximum 40 words.")
    backdrop_index: int = Field(description="0-based index of backdrop image to display from the backdrops list")
    poll: Optional[PollData] = Field(default=None, description="Interactive binary poll on the final slide (mandatory for the final slide)")
    cta_text: Optional[str] = Field(default=None, description="Optional call-to-action button text, used on the final slide")
    cta_url: Optional[str] = Field(default=None, description="Optional CTA outlink URL")

class WebStoryData(BaseModel):
    title: str = Field(description="Irresistible high-CTR viral headline under 70 characters adhering to post-viewing curiosity formulas")
    seo_description: str = Field(description="SEO meta description under 155 characters teasing the climax clues and ending breakdown")
    slides: List[SlideData] = Field(description="Sequence of 6 to 8 slides following the 8-slide viral retention arc")

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
    who_should_watch: Optional[str] = Field(default=None, description="1 punchy sentence explaining who will love this movie/show")
    skip_if: Optional[str] = Field(default=None, description="1 honest sentence on who should skip this")

def generate_high_ctr_headline(movie: Dict[str, Any]) -> str:
    """
    Generate irresistible, high-CTR, curiosity-inducing headlines for Google Discover & Search.
    Directly aligns with audience post-viewing search psychology: ending explained, hidden clues,
    betrayals, and real story vs fiction.
    """
    if movie.get("hook_title"):
        return movie["hook_title"]

    raw_title = movie.get("title", "Blockbuster")
    clean_title = raw_title.split(":")[0].strip() if ":" in raw_title and len(raw_title) > 26 else raw_title
    category = movie.get("category", "")
    genres = [g.lower() for g in movie.get("genres", [])]
    media_type = movie.get("media_type", "movie")

    is_animation = any("animat" in g for g in genres)
    is_thriller = any(g in ["thriller", "mystery", "crime", "horror"] for g in genres)
    is_sci_fi = any(g in ["science fiction", "sci-fi", "action", "fantasy"] for g in genres)
    is_series = media_type == "tv" or category in ["series", "popular_series", "streaming_charts", "ott_blockbusters"]
    is_netflix = category == "netflix_hits"
    is_classic = category in ["cult_classic", "where_are_they_now"]

    seed = sum(ord(c) for c in raw_title)

    if is_thriller:
        options = [
            f"{clean_title} Ending Explained: The Climax Twist Decoded 🔍",
            f"Who Really Pulled The Trigger in {clean_title}? 3 Clues You Missed 🕵️‍♂️",
            f"{clean_title}: The Shocking Climax & Hidden Motive Decoded 💥",
            f"The Horrific True Story Behind {clean_title}: Real Facts vs Drama 🩸",
            f"What Really Happened at the End of {clean_title}? Decoded ⚡"
        ]
    elif is_netflix or is_series:
        options = [
            f"{clean_title} Ending Explained: The Climax Clues You Missed 📺",
            f"Why They Betrayed Everyone in {clean_title}: The Hidden Deal 💥",
            f"{clean_title} Season Finale Decoded: What That Final Scene Means ⚡",
            f"The 1 Insane Clue In {clean_title} That Fans Completely Missed 🤯",
            f"{clean_title} Season 2 Roadmap: Release Date, Cast & Unresolved Clues 🔥"
        ]
    elif is_sci_fi:
        options = [
            f"{clean_title} Post-Credits Scene Decoded: Major Sequel Clues 🎬",
            f"{clean_title} Ending Explained: The Multiverse Secret Decoded ⚡",
            f"Did They Actually Survive? {clean_title} Climax Theory Explained 🚀",
            f"The 1 Hidden Detail in {clean_title} That Changes Everything 🤯",
            f"{clean_title}: 5 Mind-Blowing Clues & Climax Secrets Decoded 💥"
        ]
    elif is_animation:
        options = [
            f"{clean_title} Ending & Post-Credits Secrets: What Fans Missed 🎨",
            f"Why Audiences Are Obsessed with {clean_title}: Climax Decoded ✨",
            f"{clean_title}: The Secret Easter Eggs Hiding in Plain Sight 🍿"
        ]
    elif is_classic:
        options = [
            f"Why {clean_title} Remains An Unbeatable Masterpiece Decades Later 🎬",
            f"The Mind-Bending Secret Behind {clean_title}'s Famous Climax ⚡",
            f"{clean_title}: The Real Story & BTS Secrets Behind the Cult Hit 💀"
        ]
    else:
        options = [
            f"{clean_title} Ending Explained: The Climax & Final Twists Decoded 🎬",
            f"Why {clean_title} Left Audiences Stunned: Clues Decoded ⚡",
            f"What Really Happened at the Climax of {clean_title}? 🔍",
            f"{clean_title}: The Secret Behind The Film's Biggest Revelation 🍿"
        ]

    chosen = options[seed % len(options)]
    return chosen[:72]


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
        """Call Gemini API with structured output prompting enforcing the viral retention arc."""
        prompt = f"""
You are an investigative Hollywood entertainment journalist and viral visual storytelling editor for Google Discover & Search.
DO NOT write a boring Wikipedia synopsis, generic premise overview, or standard movie review.
The fundamental engine of Google Discover virality is POST-VIEWING AUDIENCE OBSESSION:
Viewers have just watched the movie or show on Netflix, Prime Video, Disney+, or in theaters, and are frantically searching for:
- "Ending Explained"
- "Who really did it?"
- "What did that final scene mean?"
- "The subtle clues & easter eggs 99% missed"
- "Is it based on a real story?"
- "Season 2 / Sequel roadmap"

ENTERTAINMENT ASSET:
- Title: {movie.get('title')}
- Release Date: {movie.get('release_date')}
- Tagline: {movie.get('tagline') or 'N/A'}
- Genres: {', '.join(movie.get('genres', []))}
- Director/Showrunner: {movie.get('director')}
- Top Cast: {', '.join(movie.get('top_cast', []))}
- Overview: {movie.get('overview')}
- Audience Rating: {movie.get('vote_average')}/10 ({movie.get('vote_count')} votes)
- Runtime/Seasons: {movie.get('runtime')} mins / {movie.get('seasons') or 1} seasons
- Category: {movie.get('category')}
- Available Backdrops Count: {len(movie.get('backdrops', []))}

MANDATORY 7 TO 8 SLIDE VIRAL RETENTION ARC:
Every Web Story MUST follow this high-retention narrative arc:
- Slide 1 (Cover Hook): High-voltage curiosity hook commanding attention. Badge: '🔥 CLIMAX TWIST' or '⚡ ENDING DECODED' or '👑 THE SHOCKING BETRAYAL'.
- Slide 2 (The Burning Mystery / Conflict): The exact moment or conflict that left audiences gasping and asking questions. Badge: '❓ BURNING MYSTERY' or '🕵️ WHAT WE SAW'.
- Slide 3 (Clue #1 / The Hidden Detail): A subtle visual, dialogue, or narrative clue that casual viewers missed. Badge: '🔍 CLUE #1: [Brief Detail]'.
- Slide 4 (Clue #2 / The Motive or Real Truth): The deeper motive, secret pact, or real-life counterpart behind the event. Badge: '🧩 CLUE #2: [Brief Detail]' or '🩸 TRUE STORY FACTS'.
- Slide 5 (The Decoded Climax): The canonical truth or director's explanation resolving the twist. Badge: '💡 THE DECODED TRUTH' or '💥 CLIMAX EXPLAINED'.
- Slide 6 (Franchise Future / Sequel Roadmap): What comes next (Season 2/sequel status, filming updates, release window). Badge: '🎬 SEQUEL ROADMAP' or '📺 NEXT SEASON CLUES'.
- Slide 7 (Fan Controversy / Unresolved Question): The lingering debate dividing viewers online. Badge: '🤯 UNANSWERED QUESTION'.
- Slide 8 (Interactive Fan Verdict Poll): Mandatory binary poll slide! Badge: '🗳️ FAN VERDICT POLL'.
  - Provide a valid 'poll' object with a high-controversy binary question (prompt under 45 chars, e.g. "Did they survive?", "Was it staged?", "Loved the ending?"), option1 (e.g. "Yes, 100% 🔥"), option2 (e.g. "No, staged 👎").
  - Set 'cta_text' to "Read Next Story ➔".

STRICT AMP & QUALITY RULES:
1. WORD LIMIT: Each slide's text MUST be STRICTLY UNDER 40 WORDS. Bite-sized, fast-paced, punchy.
2. Story Title: Irresistible high-CTR title under 70 characters following viral curiosity formulas (e.g., "[Title] Ending Explained: The Climax Twist & 3 Clues Decoded ⚡").
3. Slide Titles: Under 35 characters.
4. Backdrop Index: Valid integer between 0 and {max(0, len(movie.get('backdrops', [])) - 1)}.
5. FORBIDDEN WORDS: Never use "delve", "testament to", "tapestry", "in a world where", "masterclass", "beacon", "it goes without saying".
"""

        # Enforce rate-limit pacing to avoid bursts and 429 quota exhaustion
        time.sleep(API_PACING_SECONDS)

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
        """Ensure title length, word limits, slide constraints, and interactive binary polls are strictly met."""
        title = data.get("title") or generate_high_ctr_headline(movie)
        title = title[:70].strip()
        seo_description = data.get("seo_description", movie.get("overview", "")[:150]).strip()
        
        raw_slides = data.get("slides", [])
        clean_slides = []
        max_backdrops = max(1, len(movie.get("backdrops", [])))
        clean_title = movie.get("title", "this title").split(":")[0].strip()
        slug = movie.get("slug", "story")

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

            badge_text = s.get("badge") or f"HIGHLIGHT #{i+1}"
            badge_text = badge_text.upper().strip()

            slide_dict = {
                "id": f"page-{i+1}",
                "badge": badge_text,
                "title": s.get("title", f"Slide {i+1}")[:45],
                "text": truncated_text,
                "backdrop_index": backdrop_idx,
                "cta_text": s.get("cta_text"),
                "cta_url": None
            }

            # Preserve or validate poll object if present
            if s.get("poll"):
                poll_raw = s.get("poll")
                if isinstance(poll_raw, dict):
                    slide_dict["poll"] = {
                        "id": poll_raw.get("id") or f"poll-{slug}-{i+1}",
                        "type": "binary",
                        "prompt": str(poll_raw.get("prompt", f"Did you like the {clean_title} climax?"))[:45],
                        "option1": str(poll_raw.get("option1", "Loved it 🔥"))[:20],
                        "option2": str(poll_raw.get("option2", "Disappointed 👎"))[:20]
                    }

            clean_slides.append(slide_dict)

        # Guarantee final slide has viral badge, interactive binary poll, and seamless next story CTA
        if clean_slides:
            final_slide = clean_slides[-1]
            if not final_slide.get("badge") or "HIGHLIGHT" in final_slide.get("badge", ""):
                final_slide["badge"] = "🗳️ FAN VERDICT POLL"
            if not final_slide.get("poll"):
                final_slide["poll"] = {
                    "id": f"poll-{slug}-verdict",
                    "type": "binary",
                    "prompt": f"Did the {clean_title} ending satisfy you?"[:45],
                    "option1": "Genius twist 🔥",
                    "option2": "Felt rushed 👎"
                }
            final_slide["cta_text"] = "Read Next Story ➔"
            final_slide["cta_url"] = None

        return {
            "title": title,
            "seo_description": seo_description,
            "movie": movie,
            "slides": clean_slides
        }

    def _generate_fallback(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic, viral hook storytelling synthesizer.
        Produces a high-retention 7-slide story with cliffhanger decoders and interactive binary poll.
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

        title = generate_high_ctr_headline(movie)
        clean_title = movie.get("title", "this title").split(":")[0].strip()
        director = movie.get("director", "The Filmmakers")
        cast = movie.get("top_cast", ["The ensemble cast"])
        cast_str = ", ".join(cast[:3]) if cast else "The lead stars"
        genres = ", ".join(movie.get("genres", ["Cinema"]))
        rating = movie.get("vote_average", 8.2)
        overview = movie.get("overview", "")
        max_backdrops = max(1, len(movie.get("backdrops", [])))
        category = movie.get("category", "")
        is_tv = movie.get("media_type") == "tv" or category in ["series", "popular_series", "streaming_charts", "ott_blockbusters"]

        # Truncate overview for slide 2 under 34 words
        ov_words = overview.split()
        if len(ov_words) > 32:
            plot_text = " ".join(ov_words[:32]) + "..."
        else:
            plot_text = " ".join(ov_words) if ov_words else f"A pulse-pounding masterpiece in {genres}."

        slides = [
            # Slide 1: Cover Hook
            {
                "id": "page-1",
                "badge": "⚡ ENDING DECODED",
                "title": f"The Climax Of {clean_title}"[:35],
                "text": f"The breathtaking finale of {clean_title} left audiences stunned with burning questions. What really happened in that final scene? Here is the decoded truth.",
                "backdrop_index": 0,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 2: The Burning Mystery
            {
                "id": "page-2",
                "badge": "❓ BURNING MYSTERY",
                "title": "The Unseen Conflict",
                "text": f"{plot_text} Behind the visual chaos lies a deeper psychological confrontation that re-contextualizes the entire storyline.",
                "backdrop_index": 1 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 3: Clue #1
            {
                "id": "page-3",
                "badge": "🔍 CLUE #1: HIDDEN MOTIVE",
                "title": "Secrets in Plain Sight",
                "text": f"Led by {cast_str}, subtle dialogue cues in the second act secretly telegraphed the climactic betrayal long before the final sequence.",
                "backdrop_index": 2 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 4: Clue #2
            {
                "id": "page-4",
                "badge": "🧩 CLUE #2: DIRECTOR'S VISION",
                "title": f"Crafted by {director}",
                "text": f"Director {director} placed intentional visual easter eggs and shadow play throughout key scenes, foreshadowing the inevitable twist.",
                "backdrop_index": 3 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 5: The Decoded Truth
            {
                "id": "page-5",
                "badge": "💡 THE DECODED TRUTH",
                "title": "What The Climax Confirms",
                "text": f"The closing moments resolve the immediate stakes while revealing that the true fallout is only just beginning for the surviving characters.",
                "backdrop_index": 4 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 6: Franchise Future / Sequel Roadmap
            {
                "id": "page-6",
                "badge": "🎬 WHAT COMES NEXT",
                "title": "Sequel & Franchise Lore" if not is_tv else "Next Season Roadmap",
                "text": f"Holding an impressive {rating}/10 score, fan communities are already dissecting plot clues that point directly to the next installment.",
                "backdrop_index": 5 % max_backdrops,
                "cta_text": None,
                "cta_url": None
            },
            # Slide 7: Interactive Binary Poll Slide
            {
                "id": "page-7",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "What Is Your Verdict?",
                "text": f"Did the climax of {clean_title} satisfy you, or did it leave you needing answers? Cast your vote below.",
                "backdrop_index": 0,
                "poll": {
                    "id": f"poll-{slug}-verdict",
                    "type": "binary",
                    "prompt": f"Did the {clean_title} ending satisfy you?"[:45],
                    "option1": "Genius twist 🔥",
                    "option2": "Felt rushed 👎"
                },
                "cta_text": "Read Next Story ➔",
                "cta_url": None
            }
        ]

        return {
            "title": title,
            "seo_description": f"Full {clean_title} climax breakdown: ending explained, hidden clues decoded, {cast_str} performances, and sequel prospects.",
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

GOOGLE DISCOVER & SEARCH INTENT EDITORIAL GUIDELINES:
1. Headline: Irresistible, high-CTR, curiosity-inducing and authentic under 75 characters. Crucially, tailor the angle to the movie's genre/theme to match actual Google Search queries:
   - Mystery / Thriller / Crime / Drama: Focus on "Ending Explained & Plot Twist Breakdown" or "What Really Happened".
   - Documentary / Biography / True Story: Focus on "True Story Behind [Title]: Real Life Facts vs Fiction".
   - Animation / Family / Comedy: Focus on "[Title] Review, Cast & Ending Breakdown: Worth Watching?".
   - Superhero / Sci-Fi / Action: Focus on "Easter Eggs, Ending Explained & Mind-Blowing Theories".
2. Meta Description: Direct and engaging, under 155 characters. Must mention the title, key hook (ending breakdown, major plot twist, cast highlight, or honest review).
3. Key Takeaways: Exactly 3 to 4 punchy bullet points summarizing key facts for readers.
4. Sections: Exactly 4 rich, distinct editorial sections (70-130 words each):
   - Section 1: Plot Premise & Core Narrative Setup (Clear breakdown of the main storyline).
   - Section 2: Climax & Ending Explained (Crucial for Search rankings: Explain the ending, final resolution, or shocking twists).
   - Section 3: Cast Performances & Behind-The-Scenes Secrets (Highlight top cast actors by name and production craft).
   - Section 4: Critical Review, Age Rating & Watch Guide (Honest review, age rating suitability, streaming/theatrical verdict).
5. Verdict Summary: 1-2 punchy concluding sentences with a recommendation.
6. Reading Time: 3 or 4 minutes.
7. Who Should Watch: 1 honest sentence on which fans or viewers will love this most.
8. Skip If: 1 candid sentence on who might want to pass.

HUMAN EDITORIAL TOUCH & ANTI-SPAM PROTOCOL:
- ABSOLUTELY NO generic AI clichés: Never use "delve into", "testament to", "tapestry of", "in a world where", "masterclass in modern visual storytelling", "beacon", "it goes without saying".
- UNIQUE SECTIONS: Do NOT repeat boilerplate phrases between sections. Each section must cover a completely unique angle.
- JOURNALISTIC DEPTH: Speak directly to film enthusiasts like a veteran entertainment critic (Rolling Stone, Variety, Collider). Give balanced, nuanced perspectives.
"""
        # Enforce rate-limit pacing to avoid quota exhaustion
        time.sleep(API_PACING_SECONDS)

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
        Deterministic, rich editorial synthesizer for Google Discover & Search articles.
        Generates 400+ words of structured journalism with distinct, non-repetitive, search-intent sections.
        """
        slug = movie.get("slug", "")
        if slug in CURATED_ARTICLES:
            art = dict(CURATED_ARTICLES[slug])
            art["movie"] = movie
            return art
        title = movie.get("title", "Featured Film")
        director = movie.get("director") or "Acclaimed Filmmakers"
        top_cast = movie.get("top_cast", [])
        cast_str = ", ".join(top_cast[:3]) if top_cast else "an acclaimed ensemble"
        rating = movie.get("vote_average", 7.8)
        genres = movie.get("genres", ["Cinema"])
        genre_str = " & ".join(genres[:2])
        overview = movie.get("overview") or f"{title} continues to captivate global audiences with its gripping storyline and exceptional performances."
        category = movie.get("category", "trending")

        # Genre & Search Intent Classification
        genres_lower = [g.lower() for g in genres]
        is_animation = any("animat" in g for g in genres_lower)
        is_thriller = any(g in ["thriller", "mystery", "crime", "horror"] for g in genres_lower)
        is_documentary = any(g in ["documentary", "history", "biography"] for g in genres_lower)
        is_comedy_romance = any(g in ["comedy", "romance"] for g in genres_lower)

        # High-CTR, Search-Intent Driven Headlines
        if story and story.get("title"):
            headline = story.get("title")
        else:
            headline = generate_high_ctr_headline(movie)

        # Safe ratings representation
        has_valid_rating = isinstance(rating, (int, float)) and rating > 0.0
        rating_text = f"holding a certified {rating}/10 community rating" if has_valid_rating else "generating tremendous pre-release excitement across film circles"

        # Search-intent focused dynamic meta description (under 155 chars)
        meta_desc = f"Full {title} breakdown: ending explained, complete plot summary, {cast_str} performances, age rating, and honest review verdict."
        if len(meta_desc) > 155:
            meta_desc = meta_desc[:152] + "..."

        # Key Takeaways
        takeaways = [
            f"Powerhouse Cast: Led by {cast_str} under the direction of {director}.",
            f"Audience Reception: Currently {rating_text} with strong community buzz.",
            f"Genre Highlights: Compelling {genre_str} storytelling with memorable character arcs.",
            f"Watch Format: Available for full cinematic analysis and visual slide exploration."
        ]

        # Tailor sections specifically to search queries
        if is_animation:
            prod_craft = f"Directed by {director}, the animation blends expressive visual design with vibrant comedic timing. The voice work featuring {cast_str} injects authentic charm into every scene, making it appealing for both younger audiences and animation enthusiasts."
            ending_text = f"The climax of {title} ties together its high-spirited journey with heart and humor. As the central conflict reaches its peak, the characters must rely on quick thinking and teamwork, delivering a satisfying and uplifting resolution."
        elif is_documentary:
            prod_craft = f"Filmmaker {director} presents meticulous investigative research, combining archival depth with compelling real-life testimony. The production balances candid revelations with journalistic integrity to separate truth from sensation."
            ending_text = f"The ending of {title} brings critical revelations into focus, shedding light on the real-world impact and unanswered questions that continue to provoke debate long after the credits roll."
        elif is_thriller:
            prod_craft = f"Under {director}'s tight direction, {title} sustains unrelenting psychological tension. Meticulous cinematography, shadowy visual framing, and a sharp score keep viewers glued through every escalating confrontation."
            ending_text = f"The ending of {title} delivers a shocking final twist that flips earlier narrative assumptions on their head. Key character motivations are re-contextualized in the closing moments, leaving audiences eager to re-watch the clues."
        else:
            prod_craft = f"Under {director}'s steady direction, {title} balances immersive storytelling with nuanced character beats. Standout performances from {cast_str} elevate the production, bringing emotional weight to key turning points."
            ending_text = f"The ending of {title} resolves its central stakes with a memorable narrative payoff, balancing emotional closure with thought-provoking takeaways that linger well beyond the final scene."

        sections = [
            {
                "heading": f"{title} Plot: Story Premise & Key Narrative Arcs",
                "content": f"{overview} From the opening sequence, audiences are drawn into an engaging journey where unexpected developments continually test the limits and resolve of its central characters."
            },
            {
                "heading": f"{title} Ending Explained: What Happened in the Climax?",
                "content": ending_text
            },
            {
                "heading": f"Cast Highlights & Behind-the-Scenes Facts",
                "content": f"The dynamic chemistry among {cast_str} serves as the emotional backbone of the production. {prod_craft}"
            },
            {
                "heading": f"{title} Review, Age Rating & Watch Guide",
                "content": f"With audiences {rating_text}, {title} stands out as a rewarding watch for {genre_str} fans. Whether you're seeking gripping plot twists or memorable character moments, it is a recommended addition to your streaming watchlist."
            }
        ]

        verdict = f"{title} delivers a rewarding watch for fans of {genre_str}. Anchored by strong turns from {cast_str} and focused direction by {director}, it is an essential entry for your watchlist."
        who_should_watch = f"Fans of high-stakes {genre_str} entertainment who appreciate memorable ensemble acting and sharp direction by {director}."
        skip_if = f"Viewers looking for breezy, lighthearted comedy or those sensitive to tense, high-pressure conflict."

        return {
            "headline": headline[:75],
            "meta_description": meta_desc,
            "key_takeaways": takeaways,
            "sections": sections,
            "verdict_summary": verdict,
            "reading_time_mins": 3,
            "who_should_watch": who_should_watch,
            "skip_if": skip_if,
            "movie": movie
        }

    @staticmethod
    def validate_content_quality(story: Optional[Dict[str, Any]], article: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Anti-Spam & Google Quality Guard:
        Verifies that generated story and article meet Google Discover standards
        and will not trigger low-value or duplicate content filters.
        """
        issues = []
        if story:
            slides = story.get("slides", [])
            if len(slides) < 5:
                issues.append(f"Story has only {len(slides)} slides (minimum 5 required).")
            for i, s in enumerate(slides):
                word_count = len(s.get("text", "").split())
                if word_count > 40:
                    issues.append(f"Slide {i+1} exceeds 40 words ({word_count} words).")

        if article:
            headline = article.get("headline", "")
            if len(headline) > 95:
                issues.append(f"Headline is too long ({len(headline)} chars; maximum 95).")
            sections = article.get("sections", [])
            if len(sections) < 3:
                issues.append(f"Article has fewer than 3 sections ({len(sections)}).")

            # Check for repetitive identical phrases across sections
            section_texts = [sec.get("content", "") for sec in sections]
            for i in range(len(section_texts)):
                for j in range(i + 1, len(section_texts)):
                    words_i = section_texts[i].split()
                    for k in range(len(words_i) - 8):
                        chunk = " ".join(words_i[k:k+9])
                        if chunk in section_texts[j]:
                            issues.append(f"Repetitive text detected between sections {i+1} and {j+1}: '{chunk[:40]}...'")
                            break

            total_words = sum(len(sec.get("content", "").split()) for sec in sections)
            if total_words < 200:
                issues.append(f"Article is too short ({total_words} words; minimum 200 required).")

        return len(issues) == 0, issues
