# E2E Test Infra: CineStories Modernization, Compliance & Geo-Segmentation

## Test Philosophy
- **Requirement-Driven**: Derived strictly from `ORIGINAL_REQUEST.md` and `PROJECT.md`, opaque-box, verifying user-facing behavior and artifacts without coupling to internal generator implementation details.
- **Methodology**: Systematic 4-tier testing hierarchy (Category-Partition, Boundary Value Analysis, Pairwise Combinatorial Testing, Real-World Workload Testing) plus dedicated automated compliance linting and geo-routing verification.
- **Fail-Fast & Exit Semantics**: Every test tool and runner strictly exits `0` on 100% pass and non-zero (`1`) on any failure (including compliance linter violations by default), emitting formatted console output and machine-parseable JSON reports. For intermediate development, `--allow-compliance-failures` permits running unit tests while isolating upstream content compliance blockers.

---

## Feature Inventory & Test Tier Mapping

| # | Feature | Scope / Source | Tier 1 (Coverage) | Tier 2 (Boundary) | Tier 3 (Pairwise) | Tier 4 (Scenario) |
|---|---------|---------------|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
| 1 | Responsive Mobile Header & Navigation | R1 (360-420px viewports) | 5 tests | 5 tests | ✓ | ✓ |
| 2 | Horizontal Scroll-Snap Filter Rail | R1 (Category chips) | 5 tests | 5 tests | ✓ | ✓ |
| 3 | Responsive Tablet & Desktop Grids | R1 (>=768px viewports) | 5 tests | 5 tests | ✓ | ✓ |
| 4 | Tactile Micro-Interactions & Delights | R1, rules (toasts, press) | 5 tests | 5 tests | ✓ | ✓ |
| 5 | Mandatory Compliance Pages (5 Pages) | R2 (About, Privacy, etc.) | 5 tests | 5 tests | ✓ | ✓ |
| 6 | Editorial Authorship & E-E-A-T Transparency | R2 (CineStories Board) | 5 tests | 5 tests | ✓ | ✓ |
| 7 | Publication Date Fix | R2 (`pub_iso` immutable) | 5 tests | 5 tests | ✓ | ✓ |
| 8 | Schema.org Structured Metadata | R2 (`NewsArticle`, `Breadcrumbs`) | 5 tests | 5 tests | ✓ | ✓ |
| 9 | Content Depth Upgrade & Anti-Thin Filter | R2 (>=650 words) | 5 tests | 5 tests | ✓ | ✓ |
| 10 | Centralized UI Localization Dictionary | R4 (`i18n.py` parity) | 5 tests | 5 tests | ✓ | ✓ |
| 11 | Authentic Hindi Breakout Stories (10 Titles) | R4 (Devanagari AMP) | 5 tests | 5 tests | ✓ | ✓ |
| 12 | Authentic Hindi Breakout Articles (10 Titles) | R4 (Devanagari >650w) | 5 tests | 5 tests | ✓ | ✓ |
| 13 | Multi-Tier Geo-Location Detection | R3 (4-tier cascade) | 5 tests | 5 tests | ✓ | ✓ |
| 14 | Tactile Manual Language Switcher | R3 (`[ 🇺🇸 EN \| 🇮🇳 हिं ]`) | 5 tests | 5 tests | ✓ | ✓ |
| 15 | Persistent Manual Preference Override | R3 (Cookie + Storage) | 5 tests | 5 tests | ✓ | ✓ |
| 16 | Dual-Locale Static Build Pipeline | R3, R4 (`dist/` + `dist/hi/`) | 5 tests | 5 tests | ✓ | ✓ |
| 17 | Test Harness Line 203 Assertion Fix | AC (`>= 416` stories) | 5 tests | 5 tests | ✓ | ✓ |
| 18 | Automated Policy & Compliance Linter | R2, AC (`compliance_linter.py`) | 5 tests | 5 tests | ✓ | ✓ |
| 19 | Automated Geo-Routing & I18n Test Suite | R3, AC (`test_geo_routing_i18n.py`) | 5 tests | 5 tests | ✓ | ✓ |
| 20 | 100% AMP Validation & Stress Hardening | AC (`validator.py`, stress) | 5 tests | 5 tests | ✓ | ✓ |

### Calculated Coverage Thresholds
- **Total Identified Features ($N$)**: 20
- **Tier 1 (Feature Coverage)**: $\ge 5 \times 20 = 100\text{ test cases}$ (5 per feature F1-F20)
- **Tier 2 (Boundary & Corner Cases)**: $\ge 5 \times 20 = 100\text{ test cases}$ (5 per feature F1-F20)
- **Tier 3 (Cross-Feature Pairwise Interactions)**: $\ge 20\text{ pairwise test cases}$
- **Tier 4 (Real-World Application Scenarios)**: $\ge \max(5, \lfloor 20 / 2 \rfloor) = 10\text{ application-level test scenarios}$
- **4-Tier Dedicated E2E Test Cases**: Exactly **230 test cases**
- **Geo-Routing & I18n Automated Suite**: Exactly **57 test cases** across 10 classes
- **Grand Total Automated Tests**: **287 test cases** ($230 + 57$) plus 8 compliance rules

---

## Test Architecture & Suite Components

The CineStories E2E Test Suite consists of three primary automated pillars:

### Pillar 1: Automated Policy & Compliance Linter (`compliance_linter.py`)
Verifies all 8 Google AdSense & Search Essentials rules against generated `dist/` and `dist/hi/` artifacts:
1. **Rule 1**: Mandatory legal & compliance pages exist (About Us, Contact Us, Privacy Policy, Terms of Service, Editorial & AI Disclosure) in English (`dist/`) and Hindi (`dist/hi/`) (10 total pages).
2. **Rule 2**: Working contact mechanism (`mailto:` with valid domain) and authentic site ownership ("CineStories Editorial Board", zero fictitious personas).
3. **Rule 3**: Valid Schema.org structured data (`NewsArticle` with `inLanguage`, `BreadcrumbList`, `WebSite`, `Organization`).
4. **Rule 4**: Anti-thin / anti-duplicate boilerplate filter across articles.
5. **Rule 5**: Substantive word count verification (curated deep-dive articles >= 650 words across 5 sections).
6. **Rule 6**: OpenGraph publication date validity (immutable `pub_iso` matches `datePublished` and `published_registry.json`).
7. **Rule 7**: Zero broken internal links across the entire generated site.
8. **Rule 8**: 100% AMP Web Story validation compliance with zero disallowed custom scripts.

### Pillar 2: Automated Geo-Routing & I18n Test Suite (`test_geo_routing_i18n.py`)
Verifies regional content routing, language switching, and dual-locale integrity across 10 test classes (57 test cases):
- **Tier 1 Explicit User Choice**: 8 test cases (cookie, localStorage, query param, edge header precedence).
- **Tier 2 Edge CDN Headers**: 7 test cases (Cloudflare, Vercel, AWS CloudFront, Fastly).
- **Tier 3 Client Heuristics**: 8 test cases (Intl timezone, navigator.languages, zero-latency detection).
- **Tier 4 Safe Fallback**: 4 test cases (unknown locales, malformed payloads default to `en`).
- **Adversarial & Corner Cases**: 7 test cases (storage exceptions, conflicting inputs, XSS injection).
- **Bidirectional `hreflang`**: 5 test cases (reciprocal en/hi/x-default alternate links).
- **Language Switcher UI & State**: 5 test cases (DOM markup, tactile attributes, persistent storage).
- **Hindi Localization Integrity**: 5 test cases (Devanagari \u0900-\u097F characters, key parity).
- **AMP Story Integrity**: 4 test cases (zero custom JS scripts in `/hi/stories/`).
- **Client Geo Script Structure**: 4 test cases (vanilla JS routing script syntax and loading).

### Pillar 3: 4-Tier Automated E2E Test Suite & Master Runner (`tests/test_e2e_4tiers.py` & `run_e2e_tests.py`)
- **`tests/test_e2e_4tiers.py`**: Executes the 230 formal opaque-box test cases across Tiers 1-4.
- **`run_e2e_tests.py`**: Master test runner orchestrating:
  1. `compliance_linter.py --dist-dir dist` (with default strict pass/fail semantics)
  2. `test_geo_routing_i18n.py` (57 tests)
  3. `tests/test_e2e_4tiers.py` (230 tests across 4 tiers)
  4. `validator.py` (AMP Web Story validation)
  5. `adversarial_carousel_stress_test.py`
  6. `adversarial_viewport_text_stress_test.py` (with line 203 fix)
- Emits structured report to `dist/e2e_report.json`.

---

## Real-World Application Scenarios (Tier 4)

| # | Scenario ID | Description | Features Exercised | Pass Criteria |
|---|-------------|-------------|---------------------|---------------|
| 1 | T4-01 | Indian mobile user arriving on homepage | F1, F13, F14, F15, F16 | Auto-detected as Indian -> `/hi/` loaded -> Devanagari navigation -> cookie set |
| 2 | T4-02 | US desktop user exploring discover feed | F3, F13, F14, F16 | English edition loaded -> 3-column responsive grid -> categories filter correctly |
| 3 | T4-03 | Indian user reading deep Hindi article & switching to English | F11, F12, F14, F15 | Toggles switcher pill to EN -> navigated to mirror EN article -> preference persisted |
| 4 | T4-04 | Search crawler indexing bilingual alternate links | F8, F10, F16 | All pages contain reciprocal `hreflang` (en, hi, x-default) and matching canonicals |
| 5 | T4-05 | AdSense compliance crawler auditing legal pages & E-E-A-T | F5, F6, F7, F8, F9 | All 5 legal pages exist in EN & HI, valid contact email, CineStories Editorial Board |
| 6 | T4-06 | User launching AMP Web Story and navigating to deep article | F4, F11, F12, F20 | Valid AMP story -> final slide outlink navigates to full article in same language |
| 7 | T4-07 | Category rail filtering and active chip state | F2, F4, F10 | Category chips scroll smoothly, active chip reflects query, works across EN & HI |
| 8 | T4-08 | Mobile user on narrow 360px viewport | F1, F4, F14 | Brand logo, search, and language switcher fit on single header bar without wrapping |
| 9 | T4-09 | Historical article date immutability check | F6, F7, F8 | OpenGraph `article:published_time` equals Schema `datePublished` and registry date |
| 10 | T4-10 | Hostile input & fallback resilience | F13, F14, F15 | Malformed cookies, unknown geo codes, or XSS query params safely default to EN |

---

## Execution Commands

```bash
# Run complete test suite (all tiers + linters with strict exit semantics)
python run_e2e_tests.py

# Run permissive development mode (runs linter, records violations, but allows unit test pass)
python run_e2e_tests.py --allow-compliance-failures

# Skip compliance linter entirely
python run_e2e_tests.py --skip-compliance

# Run specific tier
python run_e2e_tests.py --tier 1
python run_e2e_tests.py --tier 2
python run_e2e_tests.py --tier 3
python run_e2e_tests.py --tier 4

# Run with stress tests and AMP validation
python run_e2e_tests.py --include-stress --include-amp

# Run compliance linter directly
python compliance_linter.py --dist-dir dist

# Run geo-routing and i18n test suite directly
python test_geo_routing_i18n.py

# Run 4-tier test suite via unittest directly
python -m unittest tests/test_e2e_4tiers.py

# Generate JSON report for CI/CD
python run_e2e_tests.py --json-report dist/e2e_report.json
```
