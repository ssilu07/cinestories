"""
CineStories Multi-Tier Geo-Location Detection, Language Routing & Tactile Switcher Engine.
Implements the 4-tier geo-detection cascade:
  - Tier 1: User explicit choice (Query param > Manual flag > Stored choice in Cookie/LocalStorage)
  - Tier 2: Edge CDN Headers (CF-IPCountry, x-vercel-ip-country, CloudFront-Viewer-Country)
  - Tier 3: Zero-latency client heuristics (Timezone: Asia/Kolkata, navigator.languages: hi)
  - Tier 4: Safe default fallback to English ('en')

Also provides:
  - Accessible, tactile segmented manual language switcher component [ 🇺🇸 EN | 🇮🇳 हिं ]
  - Reciprocal bidirectional hreflang and canonical link injection
  - Client-side zero-latency redirect script for non-AMP pages
"""

import re
from typing import Dict, Any, Tuple, Optional

# Constants
VALID_LANGS = {"en", "hi"}
INDIAN_TIMEZONES = {"Asia/Kolkata", "Asia/Calcutta", "IST"}
COOKIE_MAX_AGE = 31536000  # 1 year in seconds

# Client-Side Inline Geo-Routing Script (Inserted in <head> of all non-AMP HTML pages)
CLIENT_GEO_ROUTING_SCRIPT = """<script>
(function() {
  try {
    var searchParams = new URLSearchParams(window.location.search);
    var simGeo = (searchParams.get('simulate_geo') || '').trim().toUpperCase();
    var langParam = (searchParams.get('lang') || '').trim().toLowerCase();
    var path = window.location.pathname || '/';
    var isHindiPath = path === '/hi' || path === '/hi/' || path.indexOf('/hi/') === 0;

    function getCookie(name) {
      var match = document.cookie.match(new RegExp('(?:^|;\\\\s*)' + name + '=([^;]*)'));
      return match ? decodeURIComponent(match[1]) : null;
    }

    function doRedirect(targetLang) {
      var targetPath;
      if (targetLang === 'hi') {
        if (!isHindiPath) {
          targetPath = '/hi' + (path === '/' ? '/' : path);
          window.location.replace(targetPath + window.location.search + window.location.hash);
        }
      } else if (targetLang === 'en') {
        if (isHindiPath) {
          targetPath = path.replace(/^\\/hi(\\/|$)/, '/') || '/';
          window.location.replace(targetPath + window.location.search + window.location.hash);
        }
      }
    }

    // Tier 1a: Test Query Parameter Override (?simulate_geo=IN/US or ?lang=hi/en)
    if (simGeo) {
      if (simGeo === 'IN') {
        doRedirect('hi');
        return;
      } else if (/^[A-Z]{2}$/.test(simGeo)) {
        doRedirect('en');
        return;
      }
    }

    if (langParam === 'hi' || langParam === 'en') {
      doRedirect(langParam);
      return;
    }

    // Detect if Edge IP country changed (e.g. user toggled VPN between India and US/Tier-1)
    var edgeCountry = (getCookie('cinestories_edge_country') || '').trim().toUpperCase();
    if (edgeCountry) {
      var lastEdgeCountry = localStorage.getItem('cinestories_last_edge_country') || '';
      if (lastEdgeCountry && lastEdgeCountry !== edgeCountry) {
        localStorage.removeItem('cinestories_lang_manual');
        localStorage.removeItem('cinestories_lang');
        document.cookie = 'cinestories_lang_manual=; Path=/; Max-Age=0; SameSite=Lax';
        document.cookie = 'cinestories_lang=; Path=/; Max-Age=0; SameSite=Lax';
      }
      localStorage.setItem('cinestories_last_edge_country', edgeCountry);
    }

    // Tier 1b: Explicit User Choice with Manual Flag
    var manualFlag = localStorage.getItem('cinestories_lang_manual') || getCookie('cinestories_lang_manual');
    var isManual = (manualFlag === 'true');
    if (isManual) {
      var savedLang = (localStorage.getItem('cinestories_lang') || getCookie('cinestories_lang') || '').trim().toLowerCase();
      if (savedLang === 'hi' || savedLang === 'en') {
        doRedirect(savedLang);
        return;
      }
    }

    // Tier 1c: Stored choice without manual flag
    var storedLang = (localStorage.getItem('cinestories_lang') || getCookie('cinestories_lang') || '').trim().toLowerCase();
    if (storedLang === 'hi' || storedLang === 'en') {
      doRedirect(storedLang);
      return;
    }

    // Tier 2: Edge CDN IP Country Cookie (set by Vercel x-vercel-ip-country header)
    if (edgeCountry === 'IN') {
      doRedirect('hi');
      return;
    } else if (edgeCountry && edgeCountry !== 'IN') {
      doRedirect('en');
      return;
    }

    // Tier 3: Zero-Latency Client Heuristics
    // 3a. Timezone inspection
    var tz = '';
    try {
      tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    } catch (e) {}

    var indianTimezones = ['Asia/Kolkata', 'Asia/Calcutta', 'IST'];
    if (indianTimezones.indexOf(tz) !== -1) {
      doRedirect('hi');
      return;
    }

    // 3b. Navigator languages
    var navLangs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < navLangs.length; i++) {
      var l = (navLangs[i] || '').trim().toLowerCase();
      if (l === 'hi' || l.indexOf('hi-') === 0 || l.indexOf('hi_') === 0) {
        doRedirect('hi');
        return;
      }
    }

    // Tier 4: Safe Fallback to English
    if (isHindiPath && !isManual && !storedLang) {
      // Keep on Hindi page if specifically visited without overriding
    }
  } catch (err) {
    // Fail silently without interrupting page render
  }
})();
</script>"""

# Client script for manual toggle persistence
CLIENT_SWITCHER_JS = """<script>
function setLanguagePreference(targetLang) {
  try {
    localStorage.setItem('cinestories_lang', targetLang);
    localStorage.setItem('cinestories_lang_manual', 'true');
    var maxAge = 31536000;
    document.cookie = 'cinestories_lang=' + encodeURIComponent(targetLang) + '; Path=/; Max-Age=' + maxAge + '; SameSite=Lax';
    document.cookie = 'cinestories_lang_manual=true; Path=/; Max-Age=' + maxAge + '; SameSite=Lax';
  } catch (e) {}
}
</script>"""

# Language Switcher CSS Styles
LANGUAGE_SWITCHER_CSS = """
/* Tactile Segmented Language Switcher Pill */
.lang-switcher {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  padding: 3px;
  gap: 2px;
  user-select: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  vertical-align: middle;
}

.lang-switcher:hover {
  border-color: rgba(255, 255, 255, 0.22);
}

.lang-switcher .lang-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-decoration: none;
  color: #94a3b8;
  background: transparent;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  line-height: 1.2;
}

.lang-switcher .lang-pill .flag-icon {
  font-size: 13px;
  line-height: 1;
}

.lang-switcher .lang-pill .lang-text {
  font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
  text-transform: uppercase;
}

.lang-switcher .lang-pill:hover:not(.active) {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-0.5px);
}

.lang-switcher .lang-pill:active {
  transform: scale(0.95);
}

.lang-switcher .lang-pill.active {
  background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(225, 29, 72, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.25);
  cursor: default;
}

.lang-switcher .lang-divider {
  color: rgba(255, 255, 255, 0.2);
  font-size: 11px;
  font-weight: 300;
  display: none; /* Segmented layout uses pill padding instead of divider */
}

/* AMP Story specific language switcher pill (No JS, pure CSS) */
.amp-story-lang-switcher {
  position: absolute;
  top: 14px;
  right: 14px;
  z-index: 100;
  display: inline-flex;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  padding: 3px;
}

.amp-story-lang-switcher .lang-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  text-decoration: none;
  color: #cbd5e1;
}

.amp-story-lang-switcher .lang-pill.active {
  background: #e11d48;
  color: #ffffff;
}
"""


def get_geo_detection_script() -> str:
    """Returns the zero-latency client-side geo-detection script for <head>."""
    return CLIENT_GEO_ROUTING_SCRIPT


def get_switcher_styles() -> str:
    """Returns the CSS styles for the segmented language switcher."""
    return f"<style>{LANGUAGE_SWITCHER_CSS}</style>"


def get_switcher_script() -> str:
    """Returns the JS persistence helper for manual language switches."""
    return CLIENT_SWITCHER_JS


def normalize_paths(current_path: str) -> Tuple[str, str]:
    """
    Given any current path (English or Hindi), returns normalized (en_path, hi_path).
    e.g. '/' -> ('/', '/hi/')
    '/discover/' -> ('/discover/', '/hi/discover/')
    '/hi/discover/' -> ('/discover/', '/hi/discover/')
    '/articles/stree-2/' -> ('/articles/stree-2/', '/hi/articles/stree-2/')
    '/hi/articles/stree-2/' -> ('/articles/stree-2/', '/hi/articles/stree-2/')
    """
    clean = current_path.strip()
    if not clean.startswith('/'):
        clean = '/' + clean

    # Strip /hi or /hi/ prefix
    if clean == '/hi' or clean == '/hi/':
        en_path = '/'
    elif clean.startswith('/hi/'):
        en_path = clean[3:]
    else:
        en_path = clean

    # Ensure trailing slash for directory paths
    if not en_path.endswith('/') and '.' not in en_path.split('/')[-1]:
        en_path += '/'

    hi_path = '/hi' + ('' if en_path == '/' else en_path)
    if not hi_path.endswith('/') and '.' not in hi_path.split('/')[-1]:
        hi_path += '/'

    return en_path, hi_path


def render_language_switcher(current_path: str = "/", lang: str = "en", is_amp: bool = False) -> str:
    """
    Renders the tactile segmented pill [ 🇺🇸 EN | 🇮🇳 हिं ] for header, footer, or AMP stories.
    Active state is highlighted with tactile feedback.
    Non-AMP links invoke setLanguagePreference(lang) onclick.
    """
    en_path, hi_path = normalize_paths(current_path)

    en_active = "active" if lang == "en" else ""
    hi_active = "active" if lang == "hi" else ""

    en_aria = ' aria-current="page"' if lang == "en" else ""
    hi_aria = ' aria-current="page"' if lang == "hi" else ""

    if is_amp:
        # AMP-compliant: NO onclick handler, pure anchor tags
        return f"""<nav class="lang-switcher amp-story-lang-switcher" data-component="lang-switcher" aria-label="Select language">
  <a href="{en_path}" class="lang-pill {en_active}"{en_aria} aria-label="Switch to English edition">
    <span class="flag-icon">🇺🇸</span>
    <span class="lang-text">EN</span>
  </a>
  <span class="lang-divider" aria-hidden="true">|</span>
  <a href="{hi_path}" class="lang-pill {hi_active}"{hi_aria} aria-label="हिंदी संस्करण चुनें">
    <span class="flag-icon">🇮🇳</span>
    <span class="lang-text">हिं</span>
  </a>
</nav>"""
    else:
        # Standard web page with tactile JS persistence
        return f"""<nav class="lang-switcher" data-component="lang-switcher" aria-label="Select language">
  <a href="{en_path}" class="lang-pill {en_active}"{en_aria} onclick="setLanguagePreference('en')" aria-label="Switch to English edition">
    <span class="flag-icon">🇺🇸</span>
    <span class="lang-text">EN</span>
  </a>
  <span class="lang-divider" aria-hidden="true">|</span>
  <a href="{hi_path}" class="lang-pill {hi_active}"{hi_aria} onclick="setLanguagePreference('hi')" aria-label="हिंदी संस्करण चुनें">
    <span class="flag-icon">🇮🇳</span>
    <span class="lang-text">हिं</span>
  </a>
</nav>"""


def generate_hreflang_tags(current_path: str, domain: str = "https://cinematicbites.com") -> str:
    """
    Generates reciprocal alternate hreflang and x-default link tags.
    """
    base_domain = domain.rstrip('/')
    en_path, hi_path = normalize_paths(current_path)

    en_url = f"{base_domain}{en_path}"
    hi_url = f"{base_domain}{hi_path}"

    return (
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="hi" href="{hi_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{en_url}">'
    )


def resolve_geo_language(
    query_params: dict = None,
    cookies: dict = None,
    local_storage: dict = None,
    edge_headers: dict = None,
    client_heuristics: dict = None,
    current_path: str = "/"
) -> dict:
    """
    4-Tier Geo-Detection Cascade Simulator and Server-Side Resolver.
    Follows identical contracts to test_geo_routing_i18n.py GeoRoutingSimulator.
    """
    query_params = query_params or {}
    cookies = cookies or {}
    local_storage = local_storage or {}
    edge_headers = edge_headers or {}
    client_heuristics = client_heuristics or {}

    # Tier 1: Explicit User Choice
    # 1a. Test Query Parameter Override: ?simulate_geo=IN/US or ?lang=hi/en
    raw_sim_geo = query_params.get("simulate_geo", "").strip().upper()
    if raw_sim_geo:
        if raw_sim_geo == "IN":
            return _format_decision("hi", tier=1, reason="simulate_geo=IN", current_path=current_path)
        elif re.match(r"^[A-Z]{2}$", raw_sim_geo):
            return _format_decision("en", tier=1, reason=f"simulate_geo={raw_sim_geo}", current_path=current_path)

    raw_lang_param = query_params.get("lang", "").strip().lower()
    if raw_lang_param in VALID_LANGS:
        return _format_decision(raw_lang_param, tier=1, reason=f"query_param_lang={raw_lang_param}", current_path=current_path)

    # 1b. Manual User Switcher Override: cinestories_lang_manual === 'true'
    manual_storage = local_storage.get("cinestories_lang_manual", "").strip().lower() == "true"
    manual_cookie = cookies.get("cinestories_lang_manual", "").strip().lower() == "true"
    is_manual = manual_storage or manual_cookie

    if is_manual:
        saved_lang = (local_storage.get("cinestories_lang") or cookies.get("cinestories_lang") or "").strip().lower()
        if saved_lang in VALID_LANGS:
            return _format_decision(saved_lang, tier=1, reason="manual_user_override", is_manual=True, current_path=current_path)

    # 1c. Non-manual stored choice (only if no edge headers present)
    stored_lang = (local_storage.get("cinestories_lang") or cookies.get("cinestories_lang") or "").strip().lower()
    if stored_lang in VALID_LANGS and not edge_headers:
        return _format_decision(stored_lang, tier=1, reason="stored_user_choice", current_path=current_path)

    # Tier 2: Edge CDN Headers
    normalized_headers = {k.lower(): str(v).strip().upper() for k, v in edge_headers.items()}
    country_header = (
        normalized_headers.get("cf-ipcountry")
        or normalized_headers.get("x-vercel-ip-country")
        or normalized_headers.get("cloudfront-viewer-country")
    )
    if country_header:
        if country_header == "IN":
            return _format_decision("hi", tier=2, reason=f"edge_cdn_country={country_header}", current_path=current_path)
        elif re.match(r"^[A-Z]{2}$", country_header):
            return _format_decision("en", tier=2, reason=f"edge_cdn_country={country_header}", current_path=current_path)

    # Tier 3: Zero-Latency Client Heuristics
    tz = client_heuristics.get("timezone", "").strip()
    if tz in INDIAN_TIMEZONES:
        return _format_decision("hi", tier=3, reason=f"timezone={tz}", current_path=current_path)

    nav_langs = client_heuristics.get("languages", [])
    if isinstance(nav_langs, str):
        nav_langs = [nav_langs]
    for l in nav_langs:
        clean_l = str(l).strip().lower()
        if clean_l == "hi" or clean_l.startswith("hi-") or clean_l.startswith("hi_"):
            return _format_decision("hi", tier=3, reason=f"navigator_lang={clean_l}", current_path=current_path)

    # Tier 4: Safe Fallback
    return _format_decision("en", tier=4, reason="safe_fallback_default", current_path=current_path)


def _format_decision(lang: str, tier: int, reason: str, is_manual: bool = False, current_path: str = "/") -> dict:
    is_hindi_path = current_path.startswith("/hi/") or current_path == "/hi"
    should_redirect = False
    target_path = current_path

    if lang == "hi" and not is_hindi_path:
        should_redirect = True
        target_path = "/hi" + ("" if current_path == "/" else current_path)
    elif lang == "en" and is_hindi_path:
        should_redirect = True
        target_path = re.sub(r"^/hi(/|$)", "/", current_path)

    return {
        "lang": lang,
        "tier": tier,
        "reason": reason,
        "is_manual": is_manual,
        "should_redirect": should_redirect,
        "target_path": target_path
    }
