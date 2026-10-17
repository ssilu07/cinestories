"""
Tumblr OAuth 1.0a Helper Script for CineStories.
Quickly generates TUMBLR_OAUTH_TOKEN and TUMBLR_OAUTH_SECRET for sumits7196.

Usage:
    python tumblr_auth.py
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"

REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"
CALLBACK_HOST = "localhost"
CALLBACK_PORT = 8080
CALLBACK_URI = f"http://{CALLBACK_HOST}:{CALLBACK_PORT}/callback"

captured_callback_query = {}

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_callback_query
        parsed_url = urlparse(self.path)
        captured_callback_query = parse_qs(parsed_url.query)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
        <html>
        <body style="font-family: system-ui, sans-serif; text-align: center; padding: 50px; background: #0b0f19; color: #fff;">
            <h1 style="color: #4ade80;">Authorization Successful!</h1>
            <p>Tumblr authentication has been completed. You can close this tab and return to your terminal.</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress standard logging to keep terminal output clean
        return

def get_env_variable(key: str, default: str = "") -> str:
    """Read value from current environment or .env file."""
    val = os.getenv(key, "").strip()
    if val:
        return val
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip()
    return default

def update_env_file(tokens: dict):
    """Save or update Tumblr credentials in .env file."""
    existing_lines = []
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()

    keys_to_update = set(tokens.keys())
    new_lines = []
    updated_keys = set()

    for line in existing_lines:
        matched = False
        for k, v in tokens.items():
            if line.strip().startswith(f"{k}=") or line.strip().startswith(f"# {k}="):
                new_lines.append(f"{k}={v}\n")
                updated_keys.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    # Append any remaining keys that were not present in .env
    for k, v in tokens.items():
        if k not in updated_keys:
            new_lines.append(f"{k}={v}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"\n[OK] Successfully updated credentials in {ENV_PATH}")

def main():
    print("=" * 60)
    print("  CineStories - Tumblr OAuth 1.0a Token Generator")
    print("=" * 60)

    try:
        from requests_oauthlib import OAuth1Session
    except ImportError:
        print("[ERROR] 'requests-oauthlib' is required. Run: pip install requests-oauthlib pytumblr")
        sys.exit(1)

    consumer_key = get_env_variable("TUMBLR_CONSUMER_KEY")
    consumer_secret = get_env_variable("TUMBLR_CONSUMER_SECRET")
    blog_name = get_env_variable("TUMBLR_BLOG_NAME", "sumits7196")

    if not consumer_key:
        consumer_key = input("Enter your Tumblr OAuth Consumer Key: ").strip()
    else:
        print(f"Using Consumer Key from config: {consumer_key[:8]}...")

    if not consumer_secret:
        consumer_secret = input("Enter your Tumblr OAuth Consumer Secret: ").strip()
    else:
        print(f"Using Consumer Secret from config: {consumer_secret[:8]}...")

    if not consumer_key or not consumer_secret:
        print("[ERROR] Both Consumer Key and Consumer Secret are required!")
        sys.exit(1)

    callback_choice = input(
        "\nWhich Callback URL did you register in Tumblr?\n"
        "  1) https://cinematicbites.com  (Recommended if you put your site)\n"
        "  2) http://localhost:8080/callback\n"
        "Select [1 or 2, default: 1]: "
    ).strip()

    callback_uri = "https://cinematicbites.com" if callback_choice in ("", "1") else "http://localhost:8080/callback"
    is_localhost = "localhost" in callback_uri

    print(f"\n[Step 1/3] Requesting temporary OAuth token from Tumblr (using callback: {callback_uri})...")
    try:
        oauth_session = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            callback_uri=callback_uri
        )
        fetch_response = oauth_session.fetch_request_token(REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
    except Exception as e:
        print(f"[ERROR] Failed to obtain request token: {e}")
        print("Please verify your Consumer Key and Consumer Secret, and ensure Callback URL in Tumblr matches the selected URL.")
        sys.exit(1)

    auth_url = oauth_session.authorization_url(AUTHORIZE_URL)
    print("\n[Step 2/3] Authorizing Application...")
    print(f"Opening browser to authorize CineStories:\n{auth_url}\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    verifier = None
    if is_localhost:
        # Try starting local server to catch callback automatically
        try:
            print(f"Waiting for authorization callback on {callback_uri}...")
            server = HTTPServer((CALLBACK_HOST, CALLBACK_PORT), OAuthCallbackHandler)
            server.timeout = 120
            server.handle_request()
            if "oauth_verifier" in captured_callback_query:
                verifier = captured_callback_query["oauth_verifier"][0]
                print(f"[OK] Callback captured automatically! Verifier: {verifier[:6]}...")
        except Exception as e:
            print(f"Local server listening skipped: {e}")
    else:
        print("Tumblr will redirect you to cinematicbites.com after you click 'Allow'.")
        print("Look at your browser's address bar: it will have '?oauth_token=...&oauth_verifier=...' at the end.")


    # Fallback to manual prompt if callback was not captured
    if not verifier:
        print("\nIf browser did not redirect automatically, copy the full redirect URL from your browser bar.")
        redirect_input = input("Paste the redirected URL (or verifier code): ").strip()
        if "oauth_verifier=" in redirect_input:
            parsed = parse_qs(urlparse(redirect_input).query)
            verifier = parsed.get("oauth_verifier", [redirect_input])[0]
        else:
            verifier = redirect_input

    if not verifier:
        print("[ERROR] No OAuth verifier received.")
        sys.exit(1)

    print("\n[Step 3/3] Exchanging verifier for permanent Access Token...")
    try:
        oauth_session = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier
        )
        tokens = oauth_session.fetch_access_token(ACCESS_TOKEN_URL)
        oauth_token = tokens.get("oauth_token")
        oauth_token_secret = tokens.get("oauth_token_secret")

        print("\n" + "=" * 60)
        print("  🎉 AUTHORIZATION SUCCESSFUL!")
        print("=" * 60)
        print(f"TUMBLR_BLOG_NAME={blog_name}")
        print(f"TUMBLR_CONSUMER_KEY={consumer_key}")
        print(f"TUMBLR_CONSUMER_SECRET={consumer_secret}")
        print(f"TUMBLR_OAUTH_TOKEN={oauth_token}")
        print(f"TUMBLR_OAUTH_SECRET={oauth_token_secret}")
        print("=" * 60)

        # Save to .env
        update_env_file({
            "TUMBLR_BLOG_NAME": blog_name,
            "TUMBLR_CONSUMER_KEY": consumer_key,
            "TUMBLR_CONSUMER_SECRET": consumer_secret,
            "TUMBLR_OAUTH_TOKEN": oauth_token,
            "TUMBLR_OAUTH_SECRET": oauth_token_secret,
            "TUMBLR_POST_STATE": "published",
            "TUMBLR_DAILY_POST_LIMIT": "2"
        })

    except Exception as e:
        print(f"[ERROR] Failed to obtain access token: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
