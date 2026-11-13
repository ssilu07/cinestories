"""
Local development & preview server for CineStories with intelligent Geo-Routing.
Serves dist/ and dist/hi/ on http://localhost:8080 (or next available port).

Supports:
- 4-Tier Geo-Detection simulation:
  * Query parameters: ?simulate_geo=IN/US or ?lang=hi/en
  * Cookies: cinestories_lang=hi/en, cinestories_lang_manual=true
  * Edge headers: CF-IPCountry, x-vercel-ip-country, CloudFront-Viewer-Country
- Automatic 302 redirection to /hi/ for Indian visitors and / for US/Tier-1
- Persistent cookie management for manual language toggles
- Instant live preview across mobile & desktop viewports
"""

import http.server
import socketserver
import socket
import sys
import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http import cookies

from geo_routing import resolve_geo_language, COOKIE_MAX_AGE

DEFAULT_PORT = 8080
DIST_DIR = Path(__file__).resolve().parent / "dist"
DIST_HI_DIR = DIST_DIR / "hi"


class CineStoriesGeoRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Intelligent development server handler simulating Edge CDN & Client Geo-Routing.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        raw_query = parse_qs(parsed.query)

        # Flatten query parameters
        query_params = {k: v[0] for k, v in raw_query.items() if v}

        # Extract Cookies
        cookie_header = self.headers.get("Cookie", "")
        cookie_jar = cookies.SimpleCookie()
        if cookie_header:
            try:
                cookie_jar.load(cookie_header)
            except Exception:
                pass
        cookie_dict = {k: morsel.value for k, morsel in cookie_jar.items()}

        # Extract Edge Headers
        edge_headers = {}
        for h in ["CF-IPCountry", "x-vercel-ip-country", "CloudFront-Viewer-Country"]:
            val = self.headers.get(h)
            if val:
                edge_headers[h] = val

        # Ignore static assets (.css, .js, .png, .jpg, .svg, .json, .xml, .webp)
        is_asset = re.search(r"\.(css|js|png|jpe?g|svg|json|xml|webp|ico|woff2?|map)$", path, re.I)

        if not is_asset:
            decision = resolve_geo_language(
                query_params=query_params,
                cookies=cookie_dict,
                edge_headers=edge_headers,
                current_path=path
            )

            # Check if redirection needed
            if decision["should_redirect"]:
                target = decision["target_path"]
                # Append original query string if any
                if parsed.query:
                    target += f"?{parsed.query}"

                self.send_response(302)
                self.send_header("Location", target)

                # Set cookies if manual or query override
                if query_params.get("lang") or query_params.get("simulate_geo"):
                    target_lang = decision["lang"]
                    self.send_header(
                        "Set-Cookie",
                        f"cinestories_lang={target_lang}; Path=/; Max-Age={COOKIE_MAX_AGE}; SameSite=Lax"
                    )

                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                return

        # Serve static file normally
        super().do_GET()


def find_free_port(start_port=DEFAULT_PORT, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return start_port


def main():
    if not DIST_DIR.exists():
        print(f"[Error] Directory {DIST_DIR} does not exist. Run 'python build_slate.py' first.", flush=True)
        sys.exit(1)

    port = find_free_port(DEFAULT_PORT)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CineStoriesGeoRequestHandler) as httpd:
        print("\n" + "=" * 65, flush=True)
        print(f"   CineStories Bilingual Geo-Routing Preview Server Running! ", flush=True)
        print("=" * 65, flush=True)
        print(f"English Edition : http://localhost:{port}/", flush=True)
        print(f"Hindi Edition   : http://localhost:{port}/hi/", flush=True)
        print(f"Discover (EN)   : http://localhost:{port}/discover/", flush=True)
        print(f"Discover (HI)   : http://localhost:{port}/hi/discover/", flush=True)
        print(f"Simulate India  : http://localhost:{port}/?simulate_geo=IN", flush=True)
        print(f"Simulate US     : http://localhost:{port}/?simulate_geo=US", flush=True)
        print(f"XML Sitemap     : http://localhost:{port}/sitemap.xml", flush=True)
        print("=" * 65, flush=True)
        print("Press Ctrl+C to stop the server.\n", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down preview server.", flush=True)


if __name__ == "__main__":
    main()
