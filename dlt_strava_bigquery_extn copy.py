"""docstring for dlt_strava_bigquery_extn.py, 
   a DLT source for Strava data, 
   which can be loaded into BigQuery.
"""
from typing import Any ,Optional

import dlt # pylint: disable=import-error
# from dlt.sources.helpers.rest_client.paginators import PageNumberPaginatorConfig # pylint: disable=import-error
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator # pylint: disable=import-error
from dlt.common.pendulum import pendulum # pylint: disable=import-error
from dlt.sources.rest_api import ( # pylint: disable=import-error
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    # rest_api_source,
)
# below not part of DLT template
# from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator



@dlt.source(name="strava")
def strava_source() -> Any:
# def strava_source(access_token: Optional[str] = dlt.secrets.value) -> Any:
    """this function defines the Strava source for DLT.
    It uses the DLT REST API source functionality to connect to Strava's API."""
    # === manually fetch the secrets dict ===
    sec = dlt.secrets.get("sources.strava")
    access_token  = sec["access_token"]

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://www.strava.com/api/v3/",
            "auth": (
                {
                    "type": "bearer",
                    "token": access_token,
                } if access_token else None
            ),
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {
                    "per_page": 200 # Strava API supports max 200 per page
                }, 
            },
        },
        "resources": [
            {
                "name": "activities",
                "endpoint": {
                    "path": "athlete/activities",


                    "params": {
                        # "per_page": 100, # Strava API supports pagination with per_page
                        "sort": "start_date", #2025-06-29 12:19:47 UTC",
                        "direction": "desc", # Not needed for Strava
                        "since": "{incremental.start_value}", # This is a special parameter to incrementally load data from the API.
                        # "limit": 1000,
                        # "after": "{incremental.start_value}"
                    },
                    "incremental": {
                        "cursor_path": "start_date",
                        "initial_value": pendulum.today().subtract(days=30).to_iso8601_string()
                    },

                },
            }
        ],
    }
    print("Access token in use:", access_token)
    # print("DLT sees:", dlt.secrets.get("sources.strava"))

    yield from rest_api_resources(config)

def load_strava() -> None:
    """this function initializes the DLT pipeline 
    and runs it to load Strava data into BigQuery."""
    pipeline = dlt.pipeline(
        pipeline_name="strava_pipeline",
        destination="bigquery",
        dataset_name="landing",
    )

    strava = strava_source()
    can_connect, error = check_connection(strava, "activities")

    if not can_connect:
        raise RuntimeError(f"Cannot connect to Strava API: {error}")

    load_info = pipeline.run(strava)
    print(load_info)

if __name__ == "__main__":
    load_strava()
