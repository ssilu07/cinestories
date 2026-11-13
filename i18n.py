"""
CineStories Centralized UI Localization & Translation Layer.
Provides high-fidelity, culturally resonant translations for English ('en') and Hindi ('hi').
Maintains 100% key parity between locales with graceful fallback.
"""

from typing import Dict, Any

# Primary translation entries: (key, english_value, hindi_value)
_TRANSLATION_PAIRS = [
    # Navigation Items
    ("Home", "Home", "होम"),
    ("Discover", "Discover", "डिस्कवर"),
    ("Stories", "Stories", "स्टोरीज़"),
    ("Articles", "Articles", "आर्टिकल्स"),
    ("About Us", "About Us", "हमारे बारे में"),
    ("Contact Us", "Contact Us", "संपर्क करें"),
    ("Contact", "Contact", "संपर्क"),
    ("Privacy Policy", "Privacy Policy", "गोपनीयता नीति"),
    ("Terms of Service", "Terms of Service", "सेवा की शर्तें"),
    ("Editorial Policy", "Editorial Policy", "संपादकीय नीति"),
    ("Editorial", "Editorial", "संपादकीय"),
    ("Switch Language", "Switch Language", "भाषा बदलें"),
    ("Select Language", "Select Language", "भाषा चुनें"),
    ("English", "English", "अंग्रेज़ी"),
    ("Hindi", "Hindi", "हिंदी"),

    # Semantic Navigation Keys
    ("nav_home", "Home", "होम"),
    ("nav_discover", "Discover", "डिस्कवर"),
    ("nav_stories", "Stories", "स्टोरीज़"),
    ("nav_articles", "Articles", "आर्टिकल्स"),
    ("nav_about", "About Us", "हमारे बारे में"),
    ("nav_contact", "Contact Us", "संपर्क करें"),
    ("nav_privacy", "Privacy Policy", "गोपनीयता नीति"),
    ("nav_terms", "Terms of Service", "सेवा की शर्तें"),
    ("nav_editorial", "Editorial Policy", "संपादकीय नीति"),
    ("nav_language_toggle", "Switch Language", "भाषा बदलें"),
    ("nav_switch_lang", "Switch Language", "भाषा बदलें"),

    # Categories
    ("All", "All", "सभी"),
    ("Bollywood", "Bollywood", "बॉलीवुड"),
    ("Hollywood", "Hollywood", "हॉलीवुड"),
    ("Action", "Action", "एक्शन"),
    ("Drama", "Drama", "ड्रामा"),
    ("Thriller", "Thriller", "थ्रिलर"),
    ("Horror", "Horror", "हॉरर"),
    ("Comedy", "Comedy", "कॉमेडी"),
    ("Sci-Fi", "Sci-Fi", "साइंस-फ़िक्शन"),
    ("Romance", "Romance", "रोमांस"),
    ("Entertainment", "Entertainment", "मनोरंजन"),

    # Semantic Category Keys
    ("cat_all", "All", "सभी"),
    ("cat_bollywood", "Bollywood", "बॉलीवुड"),
    ("cat_hollywood", "Hollywood", "हॉलीवुड"),
    ("cat_action", "Action", "एक्शन"),
    ("cat_drama", "Drama", "ड्रामा"),
    ("cat_thriller", "Thriller", "थ्रिलर"),
    ("cat_horror", "Horror", "हॉरर"),
    ("cat_comedy", "Comedy", "कॉमेडी"),
    ("cat_scifi", "Sci-Fi", "साइंस-फ़िक्शन"),
    ("cat_romance", "Romance", "रोमांस"),

    # Slug & System Category Mappings
    ("trending", "Trending Movies", "ट्रेंडिंग फ़िल्में"),
    ("netflix_hits", "Netflix Hits", "नेटफ्लिक्स हिट्स"),
    ("streaming_charts", "Weekly Top 10", "साप्ताहिक टॉप 10"),
    ("theories_easter_eggs", "Marvel & DC Theories", "मार्वल और डीसी थ्योरीज़"),
    ("where_are_they_now", "Where Are They Now?", "अब कहाँ हैं वो कलाकार?"),
    ("series", "TV Series", "टीवी सीरीज़"),
    ("cult_classic", "Cult & Franchises", "कल्ट और फ़्रैंचाइज़ी"),
    ("steamy_thrillers", "Bold & Steamy Thrillers", "बोल्ड और स्टीमी थ्रिलर्स"),
    ("upcoming", "Upcoming", "आगामी"),

    # Filter Labels
    ("All Stories", "All Stories", "सभी कहानियाँ"),
    ("Weekly Top 10", "Weekly Top 10", "साप्ताहिक टॉप 10"),
    ("Marvel & DC Theories", "Marvel & DC Theories", "मार्वल और डीसी थ्योरीज़"),
    ("Where Are They Now?", "Where Are They Now?", "अब कहाँ हैं वो कलाकार?"),
    ("TV Series", "TV Series", "टीवी सीरीज़"),
    ("Trending Movies", "Trending Movies", "ट्रेंडिंग फ़िल्में"),
    ("Cult & Franchises", "Cult & Franchises", "कल्ट और फ़्रैंचाइज़ी"),
    ("Bold & Steamy Thrillers", "Bold & Steamy Thrillers", "बोल्ड और स्टीमी थ्रिलर्स"),
    ("Upcoming", "Upcoming", "आगामी फ़िल्में"),

    # Search Placeholders & UI
    ("Search movies...", "Search movies...", "फ़िल्में खोजें..."),
    ("Search by movie or genre...", "Search by movie or genre...", "फ़िल्में या जॉनर खोजें..."),
    ("Search stories", "Search stories", "कहानियाँ खोजें"),
    ("Search articles...", "Search articles...", "लेख खोजें..."),
    ("search_placeholder", "Search by movie or genre...", "फ़िल्में या जॉनर खोजें..."),
    ("search_stories_placeholder", "Search stories...", "कहानियाँ खोजें..."),
    ("No results found", "No results found", "कोई परिणाम नहीं मिला"),
    ("Filter by category", "Filter by category", "श्रेणी के अनुसार फ़िल्टर करें"),

    # Interactive Buttons & CTAs
    ("Read Article", "Read Article", "लेख पढ़ें"),
    ("Watch Web Story", "Watch Web Story", "वेब स्टोरी देखें"),
    ("Latest Updates", "Latest Updates", "नवीनतम अपडेट"),
    ("Share", "Share", "शेयर करें"),
    ("Copy Link", "Copy Link", "लिंक कॉपी करें"),
    ("Copied!", "Copied!", "कॉपी हो गया!"),
    ("Link Copied!", "Link Copied!", "लिंक कॉपी हो गया!"),
    ("View Web Story", "View Web Story", "वेब स्टोरी देखें"),
    ("Read Full Breakdown", "Read Full Breakdown", "पूरा विश्लेषण पढ़ें"),
    ("Read Deep-Dive Analysis", "Read Deep-Dive Analysis", "विस्तृत समीक्षा पढ़ें"),
    ("Explore Stories", "Explore Stories", "कहानियाँ देखें"),
    ("Explore Articles", "Explore Articles", "लेख पढ़ें"),
    ("Previous", "Previous", "पिछला"),
    ("Next", "Next", "अगला"),
    ("Previous story", "Previous story", "पिछली कहानी"),
    ("Next story", "Next story", "अगली कहानी"),
    ("Back to Stories", "Back to Stories", "वापस कहानियों पर"),
    ("Back to Discover", "Back to Discover", "वापस डिस्कवर पर"),
    ("Back to Home", "Back to Home", "वापस होम पर"),
    ("View All", "View All", "सभी देखें"),

    # Semantic Button Keys
    ("btn_read_article", "Read Article", "लेख पढ़ें"),
    ("btn_watch_story", "Watch Web Story", "वेब स्टोरी देखें"),
    ("btn_share", "Share", "शेयर करें"),
    ("btn_copy_link", "Copy Link", "लिंक कॉपी करें"),
    ("btn_copied", "Copied!", "कॉपी हो गया!"),
    ("btn_explore_stories", "Explore Stories", "कहानियाँ देखें"),
    ("btn_previous", "Previous", "पिछला"),
    ("btn_next", "Next", "अगला"),

    # Bylines, Metadata, & Editorial Standards
    ("CineStories Editorial Board", "CineStories Editorial Board", "सिनेस्टोरीज़ संपादकीय मंडल"),
    ("Published on", "Published on", "प्रकाशित"),
    ("Updated on", "Updated on", "अपडेट किया गया"),
    ("min read", "min read", "मिनट का पठन"),
    ("Editor's Take", "Editor's Take", "संपादकीय राय"),
    ("Audience & Watchlist Guide", "Audience & Watchlist Guide", "दर्शक और वॉचलिस्ट गाइड"),
    ("Who Will Love This", "Who Will Love This", "किन्हें पसंद आएगी"),
    ("Who Should Pass", "Who Should Pass", "किन्हें छोड़नी चाहिए"),
    ("Key Takeaways", "Key Takeaways", "मुख्य बातें"),
    ("Key Takeaways for Readers", "Key Takeaways for Readers", "पाठकों के लिए मुख्य बातें"),
    ("Trending in Google Discover", "Trending in Google Discover", "गूगल डिस्कवर में ट्रेंडिंग"),
    ("Cast", "Cast", "कलाकार"),
    ("Director", "Director", "निर्देशक"),
    ("Genres", "Genres", "जॉनर"),
    ("Release Date", "Release Date", "रिलीज़ की तारीख"),
    ("Runtime", "Runtime", "अवधि"),
    ("Rating", "Rating", "रेटिंग"),
    ("Seasons", "Seasons", "सीज़न"),
    ("Episodes", "Episodes", "एपिसोड"),
    ("Trending Now", "Trending Now", "अभी ट्रेंडिंग"),
    ("Featured Story", "Featured Story", "विशेष स्टोरी"),
    ("Breaking Insights", "Breaking Insights", "विशेष इनसाइट्स"),
    ("Related Articles", "Related Articles", "संबंधित लेख"),
    ("Related Stories", "Related Stories", "संबंधित कहानियाँ"),
    ("All Rights Reserved", "All Rights Reserved", "सर्वाधिकार सुरक्षित"),

    # Semantic Metadata Keys
    ("meta_editorial_board", "CineStories Editorial Board", "सिनेस्टोरीज़ संपादकीय मंडल"),
    ("meta_published_on", "Published on", "प्रकाशित"),
    ("meta_updated_on", "Updated on", "अपडेट किया गया"),
    ("meta_min_read", "min read", "मिनट का पठन"),
    ("meta_editors_take", "Editor's Take", "संपादकीय राय"),
    ("meta_audience_guide", "Audience & Watchlist Guide", "दर्शक और वॉचलिस्ट गाइड"),
    ("meta_who_love", "Who Will Love This", "किन्हें पसंद आएगी"),
    ("meta_who_pass", "Who Should Pass", "किन्हें छोड़नी चाहिए"),
    ("meta_key_takeaways", "Key Takeaways", "मुख्य बातें"),
    ("meta_cast", "Cast", "कलाकार"),
    ("meta_director", "Director", "निर्देशक"),
    ("meta_genres", "Genres", "जॉनर"),
    ("meta_release_date", "Release Date", "रिलीज़ की तारीख"),
    ("meta_runtime", "Runtime", "अवधि"),
    ("meta_rating", "Rating", "रेटिंग"),

    # Story Specific Badges & Headings
    ("CLIFFHANGER CLIMAX", "CLIFFHANGER CLIMAX", "क्लाइमेक्स रहस्य"),
    ("THE BURNING MYSTERY", "THE BURNING MYSTERY", "अनसुलझा सवाल"),
    ("THE DECODED TRUTH", "THE DECODED TRUTH", "डिकोड हुआ सच"),
    ("VILLAGE POLITICS", "VILLAGE POLITICS", "गाँव की राजनीति"),
    ("SEASON ROADMAP", "SEASON ROADMAP", "अगले सीज़न का रास्ता"),
    ("FAN VERDICT POLL", "FAN VERDICT POLL", "दर्शकों की राय"),
    ("THE HIDDEN DETAILS", "THE HIDDEN DETAILS", "छिपे हुए राज़"),
    ("BOX OFFICE PHENOMENON", "BOX OFFICE PHENOMENON", "बॉक्स ऑफिस धमाका"),
    ("MYTHOLOGICAL ROOTS", "MYTHOLOGICAL ROOTS", "पौराणिक संदर्भ"),
    ("CRIME INVESTIGATION", "CRIME INVESTIGATION", "अपराध और जाँच"),
    ("PSYCHOLOGICAL THRILLER", "PSYCHOLOGICAL THRILLER", "मनोवैज्ञानिक थ्रिलर"),
    ("HIGH-OCTANE ACTION", "HIGH-OCTANE ACTION", "दमदार एक्शन"),
    ("SURVIVAL GAME", "SURVIVAL GAME", "जिंदगी और मौत का खेल"),
    ("COP UNIVERSE SPECTACLE", "COP UNIVERSE SPECTACLE", "कॉप यूनिवर्स का महामुकाबला"),

    # Footer and Legal Disclosures
    ("site_tagline", "High-Impact Cinema Journalism & Visual Web Stories", "उच्च-स्तरीय सिनेमा पत्रकारिता और विजुअल वेब स्टोरीज़"),
    ("footer_disclaimer", "Independent entertainment analysis and visual storytelling under fair use standards.", "उचित उपयोग मानकों के तहत स्वतंत्र मनोरंजन विश्लेषण और दृश्य पत्रकारिता।"),
    ("copyright_notice", "© 2026 CineStories. All rights reserved.", "© 2026 सिनेस्टोरीज़। सर्वाधिकार सुरक्षित।")
]

# Build translation dictionary with guaranteed key parity
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {},
    "hi": {}
}

for key, en_text, hi_text in _TRANSLATION_PAIRS:
    TRANSLATIONS["en"][key] = en_text
    TRANSLATIONS["hi"][key] = hi_text


def get_translation(key: str, lang: str = "en", default: str = None, **kwargs) -> str:
    """
    Retrieves the localized UI string for a given key.
    
    Args:
        key: The lookup key (either semantic e.g. 'nav_home' or exact UI label e.g. 'Home').
        lang: Target language code ('en' or 'hi'). Defaults to 'en'.
        default: Optional fallback string if key is not found.
        **kwargs: Optional interpolation values for {var} placeholders.
        
    Returns:
        The localized string. Falls back gracefully to English if the translation
        is missing in the requested language, or to default/key if not found.
    """
    if not isinstance(key, str) or not key.strip():
        return default if default is not None else ("CineStories" if key is None else "")
    
    lang_code = (lang or "en").strip().lower().split("-")[0].split("_")[0]
    
    # 1. Exact match in requested locale
    if lang_code in TRANSLATIONS and key in TRANSLATIONS[lang_code]:
        res = TRANSLATIONS[lang_code][key]
    # 2. Fallback to English dictionary
    elif key in TRANSLATIONS.get("en", {}):
        res = TRANSLATIONS["en"][key]
    else:
        res = default if default is not None else key

    if kwargs and isinstance(res, str):
        try:
            res = res.format(**kwargs)
        except Exception:
            pass
    return res


def t(key: str, lang: str = "en") -> str:
    """Shorthand alias for get_translation."""
    return get_translation(key, lang)
