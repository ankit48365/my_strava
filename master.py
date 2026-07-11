"""Orchestrate the Strava token refresh and BigQuery load in one run."""

import dlt_strava_bigquery
import refresh_strava_token
from strava_credentials import (
    persist_strava_tokens,
    prime_runtime_strava_tokens,
    reload_dlt_credentials,
)


def run_all() -> int:
    """Run the end-to-end Strava refresh and pipeline workflow."""

    print("Starting Strava pipeline...\n")

    print("Refreshing Strava access token...")
    tokens = refresh_strava_token.refresh_access_token()
    if tokens is None:
        print("ERROR Token refresh failed. You may need to re-authorize.")
        return 1

    print("OK Token refreshed")
    updated_target = persist_strava_tokens(tokens)
    print(f"OK Updated {updated_target}")
    prime_runtime_strava_tokens(tokens)
    reload_dlt_credentials()
    print("OK Reloaded DLT credentials")

    print("\nRunning Strava pipeline...")
    dlt_strava_bigquery.load_strava(access_token=tokens.access_token)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
