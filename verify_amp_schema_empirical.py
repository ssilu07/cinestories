"""
Empirical Verification Test Suite for AMP & Schema.org Conformance
CineStories Milestone 1 - Challenger 2
"""

import os
import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

def test_amp_custom_css_size():
    print("\n--- Test 1: AMP Custom CSS Size & Disallowed Rules Check ---")
    stories_dir = Path("dist/stories")
    html_files = list(stories_dir.glob("*/index.html"))
    if not html_files:
        raise AssertionError("No stories found in dist/stories/")

    max_css_size = 0
    max_file = None
    has_important = []

    for f in html_files:
        content = f.read_text(encoding="utf-8")
        match = re.search(r"<style amp-custom>(.*?)</style>", content, re.DOTALL)
        if not match:
            raise AssertionError(f"Missing <style amp-custom> in {f}")
        css_text = match.group(1)
        css_size = len(css_text.encode("utf-8"))
        if css_size > max_css_size:
            max_css_size = css_size
            max_file = f
        
        # Check for disallowed !important in AMP custom CSS
        if "!important" in css_text:
            has_important.append(str(f))

    print(f"Total stories scanned: {len(html_files)}")
    print(f"Max CSS size: {max_css_size} bytes (File: {max_file})")
    print(f"AMP CSS limit: 75,000 bytes. Buffer remaining: {75000 - max_css_size} bytes")
    assert max_css_size < 75000, f"AMP CSS size limit exceeded: {max_css_size} >= 75000"
    assert len(has_important) == 0, f"Disallowed !important found in AMP custom CSS of: {has_important[:3]}"
    print(">>> PASS: AMP custom CSS is well within the 75,000 byte limit with zero '!important' rules.")

def test_story_builder_modifications():
    print("\n--- Test 2: story_builder.py Modification Verification ---")
    panchayat_story = Path("dist/stories/panchayat-season-3/index.html")
    assert panchayat_story.exists(), "Panchayat story does not exist!"
    content = panchayat_story.read_text(encoding="utf-8")

    # 1. .story-brand-badge link to /about/
    assert 'class="story-brand-badge"' in content, "Missing .story-brand-badge"
    assert '<a href="/about/" class="story-brand-badge"' in content, "Missing /about/ link on .story-brand-badge"
    print("  [x] .story-brand-badge links to /about/")

    # 2. .final-legal-row
    assert 'class="final-legal-row"' in content, "Missing .final-legal-row"
    for page in ["/about/", "/editorial/", "/privacy/", "/terms/", "/contact/"]:
        assert f'href="{page}"' in content, f"Missing {page} link in story final slide"
    print("  [x] .final-legal-row includes all 5 policy pages (/about/, /editorial/, /privacy/, /terms/, /contact/)")

    # 3. OpenGraph tags in story
    assert '<meta property="og:title"' in content, "Missing og:title"
    assert '<meta property="og:type" content="article"' in content, "Missing og:type article"
    assert '<meta property="article:published_time"' in content, "Missing article:published_time in story"
    assert '<meta property="article:modified_time"' in content, "Missing article:modified_time in story"
    print("  [x] OpenGraph article metadata present in story")

    # 4. JSON-LD BreadcrumbList in story
    soup = BeautifulSoup(content, "html.parser")
    json_ld_scripts = soup.find_all("script", type="application/ld+json")
    assert len(json_ld_scripts) > 0, "No JSON-LD script found in story"

    found_news_article = False
    found_breadcrumb = False
    in_language = None

    for script in json_ld_scripts:
        data = json.loads(script.string)
        graph = data.get("@graph", [data])
        for node in graph:
            if node.get("@type") == "NewsArticle":
                found_news_article = True
                in_language = node.get("inLanguage")
            if node.get("@type") == "BreadcrumbList":
                found_breadcrumb = True
                items = node.get("itemListElement", [])
                assert len(items) == 3, f"Expected 3 breadcrumb items, found {len(items)}"
                assert items[0]["name"] == "Home"
                assert items[1]["name"] == "Web Stories"

    assert found_news_article, "Missing NewsArticle in story JSON-LD"
    assert found_breadcrumb, "Missing BreadcrumbList in story JSON-LD"
    assert in_language == "en-US", f"Expected inLanguage 'en-US', got {in_language}"
    print(f"  [x] Story JSON-LD contains NewsArticle with inLanguage='{in_language}' and 3-tier BreadcrumbList")
    print(">>> PASS: story_builder.py modifications empirically verified.")

def test_homepage_schema():
    print("\n--- Test 3: Homepage dist/index.html Schema.org JSON-LD Verification ---")
    home = Path("dist/index.html")
    assert home.exists(), "dist/index.html does not exist!"
    content = home.read_text(encoding="utf-8")

    soup = BeautifulSoup(content, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    assert len(scripts) > 0, "No JSON-LD scripts found in dist/index.html"

    parsed_nodes = []
    for s in scripts:
        raw = s.string.strip()
        data = json.loads(raw)
        assert data.get("@context") == "https://schema.org", f"Invalid @context: {data.get('@context')}"
        if "@graph" in data:
            parsed_nodes.extend(data["@graph"])
        else:
            parsed_nodes.append(data)

    types = {n.get("@type"): n for n in parsed_nodes}
    assert "WebSite" in types, "Missing WebSite type in homepage JSON-LD"
    assert "Organization" in types, "Missing Organization type in homepage JSON-LD"

    website = types["WebSite"]
    potential_action = website.get("potentialAction", {})
    assert potential_action.get("@type") == "SearchAction", "Missing SearchAction in WebSite"
    target = potential_action.get("target")
    assert target is not None, "Missing Sitelinks Searchbox target"
    print(f"  [x] WebSite Sitelinks Searchbox target: {target}")
    assert "/discover/?q=" in target or "{search_term_string}" in str(target), f"Invalid Searchbox target: {target}"

    org = types["Organization"]
    assert org.get("name") == "CineStories", f"Unexpected Org name: {org.get('name')}"
    assert "CineStories Digital Media Network" in org.get("legalName", ""), f"Unexpected legalName: {org.get('legalName')}"
    assert org.get("publishingPrinciples"), "Missing publishingPrinciples in Organization"
    print(f"  [x] Organization publishingPrinciples: {org.get('publishingPrinciples')}")
    print(">>> PASS: dist/index.html Schema.org WebSite & Organization verified.")

def test_article_schema_and_og():
    print("\n--- Test 4: Article dist/articles/panchayat-season-3/index.html Schema.org & OG Verification ---")
    article = Path("dist/articles/panchayat-season-3/index.html")
    assert article.exists(), "Panchayat article does not exist!"
    content = article.read_text(encoding="utf-8")

    soup = BeautifulSoup(content, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    assert len(scripts) > 0, "No JSON-LD in article"

    article_node = None
    breadcrumb_node = None
    for s in scripts:
        data = json.loads(s.string.strip())
        graph = data.get("@graph", [data])
        for node in graph:
            if node.get("@type") == "NewsArticle":
                article_node = node
            elif node.get("@type") == "BreadcrumbList":
                breadcrumb_node = node

    assert article_node is not None, "Missing NewsArticle in article JSON-LD"
    assert breadcrumb_node is not None, "Missing BreadcrumbList in article JSON-LD"

    # Verify author is CineStories Editorial Board
    author = article_node.get("author", {})
    author_name = author.get("name") if isinstance(author, dict) else str(author)
    print(f"  [x] Author in JSON-LD: {author_name}")
    assert author_name == "CineStories Editorial Board", f"Expected 'CineStories Editorial Board', got '{author_name}'"
    assert author.get("url", "").endswith("/about/"), f"Author URL should point to /about/, got {author.get('url')}"

    # Verify inLanguage
    in_lang = article_node.get("inLanguage")
    print(f"  [x] inLanguage in JSON-LD: {in_lang}")
    assert in_lang == "en-US", f"Expected inLanguage 'en-US', got '{in_lang}'"

    # Verify BreadcrumbList
    items = breadcrumb_node.get("itemListElement", [])
    print(f"  [x] Breadcrumb items count: {len(items)}")
    assert len(items) == 3, f"Expected 3 breadcrumbs, got {len(items)}"
    assert items[0]["name"] == "Home"
    assert items[1]["name"] == "Discover Feed"

    # Verify OpenGraph date consistency
    og_pub = soup.find("meta", property="article:published_time")
    assert og_pub is not None, "Missing <meta property='article:published_time'>"
    og_pub_val = og_pub.get("content")

    json_ld_pub = article_node.get("datePublished")
    print(f"  [x] OpenGraph article:published_time: {og_pub_val}")
    print(f"  [x] JSON-LD datePublished:            {json_ld_pub}")
    assert og_pub_val == json_ld_pub, f"OG published_time ({og_pub_val}) does not match JSON-LD datePublished ({json_ld_pub})"

    og_mod = soup.find("meta", property="article:modified_time")
    if og_mod:
        og_mod_val = og_mod.get("content")
        json_ld_mod = article_node.get("dateModified")
        print(f"  [x] OpenGraph article:modified_time:  {og_mod_val}")
        print(f"  [x] JSON-LD dateModified:             {json_ld_mod}")
        assert og_mod_val == json_ld_mod, f"OG modified_time mismatch"

    print(">>> PASS: Article Schema.org and OG date consistency verified.")

def test_policy_pages_schema():
    print("\n--- Test 5: Policy Pages Schema.org JSON-LD Verification ---")
    pages = ["about", "contact", "privacy", "terms", "editorial"]
    expected_primary_types = {
        "about": "AboutPage",
        "contact": "ContactPage",
        "privacy": "WebPage",
        "terms": "WebPage",
        "editorial": ["WebPage", "ItemPage"],
    }

    for page in pages:
        file_path = Path(f"dist/{page}/index.html")
        assert file_path.exists(), f"Policy page dist/{page}/index.html does not exist!"
        content = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(content, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")
        assert len(scripts) > 0, f"No JSON-LD script found in dist/{page}/index.html"

        all_types = set()
        has_breadcrumb = False
        breadcrumb_items_count = 0

        for s in scripts:
            data = json.loads(s.string.strip())
            assert data.get("@context") == "https://schema.org", f"Invalid @context in {page}"
            graph = data.get("@graph", [data])
            for node in graph:
                t = node.get("@type")
                if t:
                    all_types.add(t)
                # Check for direct or nested BreadcrumbList
                if t == "BreadcrumbList":
                    has_breadcrumb = True
                    breadcrumb_items_count = len(node.get("itemListElement", []))
                bc = node.get("breadcrumb")
                if isinstance(bc, dict) and bc.get("@type") == "BreadcrumbList":
                    has_breadcrumb = True
                    all_types.add("BreadcrumbList")
                    breadcrumb_items_count = len(bc.get("itemListElement", []))

        print(f"  [x] dist/{page}/index.html detected Schema types: {all_types}")
        exp_primary = expected_primary_types[page]
        if isinstance(exp_primary, list):
            assert any(ep in all_types for ep in exp_primary), f"Missing one of {exp_primary} in {page}"
        else:
            assert exp_primary in all_types, f"dist/{page}/index.html missing expected primary type '{exp_primary}'"
        assert has_breadcrumb, f"dist/{page}/index.html missing BreadcrumbList (found: {all_types})"
        assert breadcrumb_items_count >= 2, f"dist/{page}/index.html has invalid breadcrumb items count ({breadcrumb_items_count})"
        print(f"      Verified {exp_primary} with valid BreadcrumbList ({breadcrumb_items_count} items)")

    print(">>> PASS: All 5 policy pages have valid Schema.org JSON-LD.")

def test_cross_article_date_consistency():
    print("\n--- Test 6: Cross-Article OG Date Consistency (Sample 20 Articles) ---")
    article_files = list(Path("dist/articles").glob("*/index.html"))
    print(f"Total articles found: {len(article_files)}")
    assert len(article_files) > 0, "No articles found"

    sample = article_files[:20]
    for af in sample:
        content = af.read_text(encoding="utf-8")
        soup = BeautifulSoup(content, "html.parser")
        og_pub = soup.find("meta", property="article:published_time")
        assert og_pub, f"Missing og:published_time in {af}"
        
        scripts = soup.find_all("script", type="application/ld+json")
        found_date = None
        for s in scripts:
            data = json.loads(s.string.strip())
            for node in data.get("@graph", [data]):
                if node.get("@type") == "NewsArticle":
                    found_date = node.get("datePublished")
        assert found_date, f"Missing datePublished in JSON-LD in {af}"
        assert og_pub.get("content") == found_date, f"Date mismatch in {af}: OG={og_pub.get('content')} != JSON-LD={found_date}"

    print(f">>> PASS: Verified date consistency across sample of {len(sample)} articles.")

if __name__ == "__main__":
    test_amp_custom_css_size()
    test_story_builder_modifications()
    test_homepage_schema()
    test_article_schema_and_og()
    test_policy_pages_schema()
    test_cross_article_date_consistency()
    print("\n======================================================================")
    print("ALL EMPIRICAL CHALLENGE TESTS PASSED SUCCESSFULLY WITH ZERO REGRESSIONS")
    print("======================================================================\n")
