"""Authorize Strava API access and persist the resulting dlt credentials."""

import urllib.parse
import webbrowser

import requests  # pylint: disable=import-error

from strava_credentials import (
    StravaTokens,
    load_strava_credentials,
    persist_strava_tokens,
    prime_runtime_strava_tokens,
    reload_dlt_credentials,
)

REDIRECT_URI = "http://localhost/exchange_token"
SCOPES = "activity:read_all"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"


def build_auth_url(client_id: str) -> str:
    """Build the Strava authorization URL with the required parameters."""

    params = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "approval_prompt": "force",
            "scope": SCOPES,
        }
    )
    return f"https://www.strava.com/oauth/authorize?{params}"


def exchange_code(code: str, client_id: str, client_secret: str) -> StravaTokens:
    """Exchange the one-time Strava code for an access and refresh token."""

    response = requests.post(
        STRAVA_TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    response.raise_for_status()
    token_data = response.json()
    return StravaTokens(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
    )


if __name__ == "__main__":
    credentials = load_strava_credentials(require_tokens=False)
    auth_url = build_auth_url(credentials.client_id)
    print("Opening browser for Strava authorization...")
    webbrowser.open(auth_url)

    code = input("Paste the code from the redirected URL: ").strip()
    tokens = exchange_code(code, credentials.client_id, credentials.client_secret)

    updated_target = persist_strava_tokens(tokens)
    prime_runtime_strava_tokens(tokens)
    reload_dlt_credentials()
    print(f"Updated {updated_target} with new credentials.")
