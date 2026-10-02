"""
Simple local development server for CineStories.
Serves the dist/ directory on http://localhost:8000.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8000
DIST_DIR = Path(__file__).resolve().parent / "dist"

class DualStackServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    if not DIST_DIR.exists():
        print(f"[Error] Directory {DIST_DIR} does not exist. Run 'python fetch_and_generate.py' first.")
        sys.exit(1)

    with socketserver.TCPServer(("", PORT), DualStackServer) as httpd:
        print("\n" + "="*55)
        print(f"   CineStories Local Preview Server Running!        ")
        print("="*55)
        print(f"Portal Homepage : http://localhost:{PORT}/")
        print(f"Stories Feed    : http://localhost:{PORT}/stories.json")
        print(f"XML Sitemap     : http://localhost:{PORT}/sitemap.xml")
        print("="*55)
        print("Press Ctrl+C to stop the server.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down preview server.")

if __name__ == "__main__":
    main()
