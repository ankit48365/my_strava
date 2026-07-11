"""Refresh the Strava access token using the current refresh token."""

import requests

from strava_credentials import (
    StravaTokens,
    load_strava_credentials,
    persist_strava_tokens,
    prime_runtime_strava_tokens,
    reload_dlt_credentials,
)

STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"


def refresh_access_token() -> StravaTokens | None:
    """Refresh the Strava access token and return the new token pair."""

    try:
        credentials = load_strava_credentials()
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return None

    try:
        response = requests.post(
            STRAVA_TOKEN_URL,
            data={
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "refresh_token": credentials.refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"ERROR Failed to refresh token: {exc}")
        if exc.response is not None:
            print(f"Response: {exc.response.text}")
        return None

    token_data = response.json()
    return StravaTokens(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
    )


def main() -> int:
    """Refresh tokens and persist them for the current environment."""

    print("Refreshing Strava access token...")
    tokens = refresh_access_token()
    if tokens is None:
        print("ERROR Token refresh failed. You may need to re-authorize.")
        return 1

    print("OK Token refreshed")
    updated_target = persist_strava_tokens(tokens)
    print(f"OK Updated {updated_target}")
    prime_runtime_strava_tokens(tokens)
    reload_dlt_credentials()
    print("OK Reloaded DLT credentials")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
