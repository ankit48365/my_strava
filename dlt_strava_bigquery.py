"""A DLT source that loads Strava data into BigQuery."""

from typing import Any

import dlt  # pylint: disable=import-error
from dlt.sources.rest_api import (  # pylint: disable=import-error
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
)


def _get_access_token(access_token: str | None = None) -> str:
    """Resolve the access token from the explicit runtime value or dlt secrets."""

    if access_token:
        return access_token

    sec = dlt.secrets.get("sources.strava")
    return sec["access_token"]


@dlt.source(name="strava")
def strava_source(access_token: str | None = None) -> Any:
    """Define the Strava source using dlt's REST API helpers."""

    token = _get_access_token(access_token)
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://www.strava.com/api/v3/",
            "auth": {"type": "bearer", "token": token} if token else None,
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": {"disposition": "merge", "strategy": "upsert"},
            "endpoint": {
                "params": {
                    "per_page": 200,  # Strava API supports max 200 per page.
                },
            },
        },
        "resources": [
            {
                "name": "activities",
                "endpoint": {
                    "path": "athlete/activities",
                    "params": {
                        "per_page": 200,  # Strava API supports max 200 per page.
                    },
                },
            }
        ],
    }

    yield from rest_api_resources(config)


def load_strava(access_token: str | None = None) -> Any:
    """Run the Strava pipeline and return the dlt load result."""

    pipeline = dlt.pipeline(
        pipeline_name="strava_pipeline",
        destination="bigquery",
        dataset_name="landing",
    )

    strava = strava_source(access_token=access_token)
    can_connect, error = check_connection(strava, "activities")
    if not can_connect:
        raise RuntimeError(f"Cannot connect to Strava API: {error}")

    print("OK Connected to Strava API")
    load_info = pipeline.run(strava)
    print("OK Activities loaded into BigQuery")
    return load_info


if __name__ == "__main__":
    load_strava()
