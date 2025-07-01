"""docstring for strava_authorize.py
   A script to authorize Strava API access and update DLT secrets.
   It opens a browser for user authorization, retrieves access and refresh tokens,
   and updates the DLT secrets file."""
import webbrowser
import requests # pylint: disable=import-error
import urllib.parse
import os
import dlt # pylint: disable=import-error


sec = dlt.secrets.get("sources.strava")
CLIENT_ID = sec["client_id"]
CLIENT_SECRET = sec["client_secret"]
REDIRECT_URI = "http://localhost/exchange_token"
SCOPES = "activity:read_all"
TEMP_SECRET_PATH = ".dlt/temp_secret.toml"

def build_auth_url():
    """Builds the Strava authorization URL with required parameters."""
    params = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "approval_prompt": "force",
        "scope": SCOPES
    })
    return f"https://www.strava.com/oauth/authorize?{params}"

def exchange_code(code):
    """Exchanges the authorization code for access and refresh tokens."""
    res = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })
    res.raise_for_status()
    return res.json()["access_token"], res.json()["refresh_token"]

def update_secrets_file(access_token, refresh_token):
    """Updates the DLT secrets file with the new access and refresh tokens."""
    lines = [
        "[sources.strava]",
        f'access_token  = "{access_token}"',
        f'refresh_token = "{refresh_token}"',
        f'client_id     = "{CLIENT_ID}"',
        f'client_secret = "{CLIENT_SECRET}"',
        ""
    ]
    os.makedirs(os.path.dirname(TEMP_SECRET_PATH), exist_ok=True)
    with open(TEMP_SECRET_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Updated {TEMP_SECRET_PATH} with new credentials.")

if __name__ == "__main__":
    """Main function to handle the authorization flow."""
    auth_url = build_auth_url()
    print("🌐 Opening browser for Strava authorization...")
    webbrowser.open(auth_url)

    code = input("📥 Paste the code from the redirected URL: ").strip()
    access_token, refresh_token = exchange_code(code)

    print(f"🔐 Access token: {access_token[:8]}..., Refresh token: {refresh_token[:8]}...")
    update_secrets_file(access_token, refresh_token)
