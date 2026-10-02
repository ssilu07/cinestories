"""
Local development server for CineStories.
Serves the dist/ directory on http://localhost:8080 (or next available port).
"""

import http.server
import socketserver
import functools
import socket
import sys
from pathlib import Path

DEFAULT_PORT = 8080
DIST_DIR = Path(__file__).resolve().parent / "dist"

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
        print(f"[Error] Directory {DIST_DIR} does not exist. Run 'python fetch_and_generate.py' first.", flush=True)
        sys.exit(1)

    port = find_free_port(DEFAULT_PORT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST_DIR))

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("\n" + "="*55, flush=True)
        print(f"   CineStories Local Preview Server Running!        ", flush=True)
        print("="*55, flush=True)
        print(f"Portal Homepage : http://localhost:{port}/", flush=True)
        print(f"Discover Feed   : http://localhost:{port}/discover/", flush=True)
        print(f"Sample Article  : http://localhost:{port}/articles/money-heist/", flush=True)
        print(f"Sample Story    : http://localhost:{port}/stories/dune-part-two/", flush=True)
        print(f"Articles JSON   : http://localhost:{port}/articles.json", flush=True)
        print(f"Stories Feed    : http://localhost:{port}/stories.json", flush=True)
        print(f"XML Sitemap     : http://localhost:{port}/sitemap.xml", flush=True)
        print("="*55, flush=True)
        print("Press Ctrl+C to stop the server.\n", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down preview server.", flush=True)

if __name__ == "__main__":
    main()
