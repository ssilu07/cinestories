# CineStories ⚡
> **End-to-End Automated Movie & Entertainment Google AMP Web Stories Platform**  
> Powered by **The Movie Database (TMDB) API**, **Google Gemini AI**, and **100% AMP-Valid Story Engine**.

[![AMP Validated](https://img.shields.io/badge/AMP-100%25%20Valid-005af0?style=for-the-badge&logo=amp&logoColor=white)](https://amp.dev)
[![Gemini 3.8 Flash](https://img.shields.io/badge/AI-Gemini%203.8%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![TMDB Powered](https://img.shields.io/badge/TMDB-API%20v3%2Fv4-01d277?style=for-the-badge&logo=themoviedatabase&logoColor=white)](https://www.themoviedb.org)
[![Deploy to Cloudflare / Vercel](https://img.shields.io/badge/Deploy-Cloudflare%20%7C%20Vercel-black?style=for-the-badge&logo=cloudflare&logoColor=orange)](https://pages.cloudflare.com)

---

## 📖 Table of Contents
1. [Overview & Architecture](#-overview--architecture)
2. [Google AMP Compliance & Google Discover SEO](#-google-amp-compliance--google-discover-seo)
3. [Key Features](#-key-features)
4. [Project Structure](#-project-structure)
5. [Quickstart & Setup](#-quickstart--setup)
6. [Pipeline Usage (CLI)](#-pipeline-usage-cli)
7. [Automated CI/CD & Deployment](#-automated-cicd--deployment)
8. [AMP Verification & Testing](#-amp-verification--testing)
9. [Configuration Reference](#-configuration-reference)

---

## 🚀 Overview & Architecture

**CineStories** is a production-grade, headless static site generator that continuously monitors upcoming releases, now-playing box office hits, and weekly trending films from The Movie Database (TMDB). It synthesizes punchy, snackable editorial narratives using the **Google Gemini API (`gemini-3.8-flash`)** and compiles them into **100% AMP-valid standalone Web Stories** along with an automated XML sitemap and a responsive visual portal.

```
                    ┌────────────────────────────────────────┐
                    │               DATA SOURCE              │
                    │      The Movie Database (TMDB) API     │
                    │   /movie/upcoming  /movie/now_playing  │
                    │        /trending/movie/week            │
                    └───────────────────┬────────────────────┘
                                        │ (Movie metadata & high-res backdrops)
                                        ▼
                    ┌────────────────────────────────────────┐
                    │          AI SYNTHESIS LAYER            │
                    │     Google Gemini (gemini-3.8-flash)   │
                    │  Structured Outputs (Pydantic Schema)  │
                    │  - Max 40 words/slide narrative arc   │
                    │  - Curiosity hooks & trivia extraction │
                    └───────────────────┬────────────────────┘
                                        │ (5-7 Slide narrative objects)
                                        ▼
                    ┌────────────────────────────────────────┐
                    │           STATIC GENERATOR             │
                    │  - 100% AMP Story Engine (v0.js)       │
                    │  - Dark Cinema Scrim Layers            │
                    │  - Schema.org NewsArticle JSON-LD      │
                    │  - dist/stories/[slug]/index.html      │
                    │  - dist/index.html (Visual Portal)     │
                    │  - dist/sitemap.xml (Automated Sitemap)│
                    └───────────────────┬────────────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
              ┌─────────────────────┐       ┌─────────────────────┐
              │  Cloudflare Pages   │       │   Vercel Platform   │
              │  Edge CDN & Caching │       │  Edge Network & CDN │
              └─────────────────────┘       └─────────────────────┘
```

---

## ⚡ Google AMP Compliance & Google Discover SEO

Every generated Web Story strictly complies with the official [Google AMP Web Story Specifications](https://amp.dev/documentation/guides-and-tutorials/start/visual_story/) and [Google Search & Discover Guidelines](https://developers.google.com/search/docs/appearance/web-stories):

| Requirement | Implementation Detail | Compliance Status |
| :--- | :--- | :---: |
| **Document Type** | `<!doctype html>` followed by `<html ⚡ lang="en">` | ✅ 100% |
| **Required Meta** | `<meta charset="utf-8">` and mobile viewport tag | ✅ 100% |
| **Self-Referencing Canonical** | `<link rel="canonical" href="https://yourdomain.com/stories/[slug]/">` | ✅ 100% |
| **Official Boilerplate CSS** | Exact AMP start keyframe animation and noscript fallback | ✅ 100% |
| **AMP Scripts** | `<script async src="https://cdn.ampproject.org/v0.js"></script>`<br>`<script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>` | ✅ 100% |
| **Publisher Identity** | `publisher="MoviePulse"` with 512x512 px square logo (minimum required: 96x96 px) | ✅ 100% |
| **Portrait Poster** | TMDB `w780` high-res poster (780x1170 px, exceeds minimum 640x853 px 3:4 requirement) | ✅ 100% |
| **Slide Count** | Exactly 5 to 7 slides per story (`<amp-story-page>`) | ✅ 100% |
| **Word Limit** | Strictly under **40 words per slide** for maximum mobile readability | ✅ 100% |
| **Layer Architecture** | Background `<amp-story-grid-layer template="fill">`<br>Text `<amp-story-grid-layer template="vertical">` with dark semi-transparent scrim | ✅ 100% |
| **Call to Action** | Official `<amp-story-page-outlink layout="nodisplay">` CTA on final slide | ✅ 100% |
| **Structured Data** | Schema.org `NewsArticle` JSON-LD with author, publisher, and image metadata | ✅ 100% |

---

## ✨ Key Features

- **Automated Multi-Category Ingestion**: Scrapes `/movie/upcoming`, `/movie/now_playing`, and `/trending/movie/week` including directors, top cast, runtimes, and high-res backdrops in single batched calls.
- **AI-Powered Structured Storytelling**: Uses Google's official `google-genai` SDK with JSON schema enforcement to produce 5-7 slides following the proven narrative arc:
  - *Slide 1*: Cover hook with title, release date, and premise.
  - *Slide 2*: Core plot setup (strictly spoiler-free).
  - *Slide 3*: Star cast ensemble & director vision.
  - *Slide 4*: Behind-the-scenes trivia & technical feats.
  - *Slide 5*: Audience reception & community buzz.
  - *Slide 6/7*: Call-to-action outlink for tickets & showtimes.
- **Built-in Resilient Fallback Engine**: If API keys or network are unavailable, automatically synthesizes rich demo stories from genuine TMDB datasets without failing builds.
- **Dynamic Visual Portal**: Modern, responsive `dist/index.html` featuring interactive category filtering (All, Trending, Upcoming, Now Playing), real-time search, TMDB ratings, and direct links to stories.
- **SEO-Optimized XML Sitemap**: Generates `dist/sitemap.xml` with Google image extensions (`image:image`, `image:loc`, `image:title`) and updates `<lastmod>` on every run.
- **Automated CI/CD**: Pre-configured GitHub Actions workflow runs on a daily cron schedule, commits generated static assets to the repo, and deploys directly to Cloudflare Pages or Vercel.

---

## 📁 Project Structure

```
CineStories/
├── config.py                 # Central settings & environment loader
├── fetch_and_generate.py     # Main CLI pipeline orchestrator
├── tmdb_client.py            # TMDB API client with credits & backdrop extraction
├── ai_generator.py           # Gemini 3.8 Flash structured generation & fallback
├── story_builder.py          # 100% AMP Web Story HTML renderer
├── homepage_builder.py       # Responsive visual landing page generator
├── sitemap_builder.py        # Automated XML sitemap builder
├── validator.py              # Automated AMP validation test runner
├── sample_data.py            # High-fidelity movie sample dataset
├── generate_assets.py        # Generates 512x512 publisher logo with Pillow
├── serve.py                  # Local dev preview server (port 8000)
├── requirements.txt          # Python dependencies
├── package.json              # npm scripts and dev tools
├── vercel.json               # Vercel deployment configuration
├── .env.example              # Example environment variables
├── .github/
│   └── workflows/
│       └── deploy.yml        # Daily cron & auto-deploy GitHub Actions workflow
├── assets/                   # Source logo and favicon assets
└── dist/                     # Deployable static output directory
    ├── index.html            # Visual portal homepage
    ├── sitemap.xml           # Automated XML sitemap
    ├── robots.txt            # Search engine directives
    ├── stories.json          # Stories manifest
    ├── _headers              # Cloudflare Pages caching rules
    ├── assets/               # Logo and favicons
    └── stories/              # Standalone AMP stories
        ├── dune-part-two/
        │   └── index.html
        ├── deadpool-and-wolverine/
        │   └── index.html
        └── ...
```

---

## 🛠️ Quickstart & Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-username/CineStories.git
cd CineStories

# Set up Python virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python requirements
pip install -r requirements.txt

# Install Node dependencies (for AMP validator)
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```ini
# Domain where stories will be hosted (no trailing slash)
DOMAIN_NAME=https://cinestories.pages.dev

# The Movie Database (TMDB) API Key (v3 key or v4 read token)
# https://www.themoviedb.org/settings/api
TMDB_API_KEY=your_tmdb_api_key_here

# Google Gemini API Key
# https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here

# Model selection
GEMINI_MODEL=gemini-3.8-flash
```

---

## 💻 Pipeline Usage (CLI)

### Full Automated Generation Pipeline
Runs live TMDB data fetching, Gemini AI slide generation, renders static AMP stories, generates homepage and sitemap, and validates AMP compliance:

```bash
python fetch_and_generate.py
```

### Offline / Demo Mode (No API keys required)
Uses built-in high-fidelity movie records to generate a complete working portal instantly:

```bash
python fetch_and_generate.py --demo
```

### CLI Command Options

```bash
python fetch_and_generate.py \
  --domain "https://cinestories.pages.dev" \
  --category "all" \
  --count 5 \
  --validate
```

Flags:
- `--domain <url>`: Override deployment domain for canonical tags.
- `--category <all|trending|upcoming|now_playing>`: Scope movies to a single category.
- `--count <n>`: Number of movies to fetch per category (default: 5).
- `--no-validate`: Skip AMP validator step.
- `--demo`: Force offline mock data generation.

### Local Preview Server
Start the local HTTP preview server to explore stories in your browser:

```bash
python serve.py
# Open http://localhost:8000 in your browser
```

---

## 🧪 AMP Verification & Testing

Every story generated by CineStories is tested against the official Google AMP HTML Validator.

Run the test suite across all generated stories:

```bash
python validator.py
```

Or run via `npx` directly:

```bash
npx amphtml-validator dist/stories/*/index.html
```

Expected Output:
```
=======================================================
       AMP HTML COMPLIANCE VALIDATION SUITE            
=======================================================
Validating 6 story files with amphtml-validator...

  [PASS] /stories/deadpool-and-wolverine/index.html
  [PASS] /stories/dune-part-two/index.html
  [PASS] /stories/gladiator-ii/index.html
  [PASS] /stories/inside-out-2/index.html
  [PASS] /stories/oppenheimer/index.html
  [PASS] /stories/wicked/index.html

Validation Summary: 6 PASSED | 0 FAILED (Total: 6)
>> 100% AMP VALIDATION SUCCESS: All stories comply with Google Web Story specifications!
```

---

## 🚢 Automated CI/CD & Deployment

### GitHub Actions Workflow (`.github/workflows/deploy.yml`)

The platform includes a zero-maintenance GitHub Actions pipeline that:
1. Runs automatically on a daily cron schedule (`0 6 * * *` at 06:00 UTC).
2. Can be manually triggered via `workflow_dispatch` with custom parameters.
3. Fetches new movies, generates slides with Gemini AI, and tests AMP compliance.
4. Auto-commits updated stories and sitemaps back to your repository.
5. Deploys the static `dist/` directory to **Cloudflare Pages** or **Vercel**.

#### Required GitHub Secrets

Add these secrets under **Settings > Secrets and variables > Actions**:

| Secret Name | Description | Required For |
| :--- | :--- | :---: |
| `TMDB_API_KEY` | TMDB API Key or v4 Read Access Token | Live movie data |
| `GEMINI_API_KEY` | Google Gemini API Key | Live AI slide generation |
| `DOMAIN_NAME` | Deployment domain (e.g. `https://cinestories.pages.dev`) | Canonical & SEO URLs |
| `CLOUDFLARE_API_TOKEN` | *(Optional)* Cloudflare API Token | Cloudflare Pages deployment |
| `CLOUDFLARE_ACCOUNT_ID`| *(Optional)* Cloudflare Account ID | Cloudflare Pages deployment |
| `VERCEL_TOKEN` | *(Optional)* Vercel API Token | Vercel deployment |

---

## ⚙️ Configuration Reference

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DOMAIN_NAME` | `https://cinestories.pages.dev` | Base domain for canonical links and sitemap |
| `SITE_NAME` | `MoviePulse` | Portal title and branding |
| `SITE_TAGLINE` | `Visual Web Stories for Movie Lovers` | Portal description and meta tags |
| `PUBLISHER_NAME` | `MoviePulse` | AMP story publisher attribute |
| `TMDB_API_KEY` | `""` | The Movie Database API Key |
| `GEMINI_API_KEY` | `""` | Google Gemini API Key |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Gemini model identifier |
| `STORIES_PER_CATEGORY_LIMIT` | `5` | Maximum stories generated per category |
| `MAX_TOTAL_STORIES` | `15` | Total stories threshold per batch run |

---

## 📄 License & Attribution

- Built under the MIT License.
- **TMDB Attribution**: This product uses the TMDB API but is not endorsed or certified by TMDB.
- **Google AMP**: Follows the Google AMP Project and Web Story 1.0 open-source specifications.
