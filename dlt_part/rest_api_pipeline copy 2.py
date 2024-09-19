from typing import Any, Optional

import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)

def load_strava_athlete() -> None:
    client_id = dlt.secrets.get("strava.client_id")
    client_secret = dlt.secrets.get("strava.client_secret")
    access_token = dlt.secrets.get("strava.access_token")

    pipeline = dlt.pipeline(
        pipeline_name="rest_api_strava_athlete",
        destination="postgres",
        dataset_name="rest_api_data",
    )

    strava_athlete_source = rest_api_source(
        {
            "client": {
                "base_url": "https://www.strava.com/api/v3/",
                "headers": {
                    "Authorization": f"Bearer {access_token}"
                }
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "per_page": 200,
                    },
                },
            },
            "resources": [
                "athlete",
                "athlete/activities",
                "athlete/clubs",
            ],
        }
    )


    load_info = pipeline.run(strava_athlete_source)
    print(load_info)



if __name__ == "__main__":
    # load_pokemon()
    load_strava_athlete()




# def load_pokemon() -> None:
#     pipeline = dlt.pipeline(
#         pipeline_name="rest_api_pokemon",
#         destination='postgres',
#         dataset_name="rest_api_data",
#     )

#     pokemon_source = rest_api_source(
#         {
#             "client": {
#                 "base_url": "https://pokeapi.co/api/v2/",
#                 # If you leave out the paginator, it will be inferred from the API:
#                 # "paginator": "json_link",
#             },
#             "resource_defaults": {
#                 "endpoint": {
#                     "params": {
#                         "limit": 1000,
#                     },
#                 },
#             },
#             "resources": [
#                 "pokemon",
#                 "berry",
#                 "location",
#             ],
#         }
#     )

#     def check_network_and_authentication() -> None:
#         (can_connect, error_msg) = check_connection(
#             pokemon_source,
#             "not_existing_endpoint",
#         )
#         if not can_connect:
#             pass  # do something with the error message

#     check_network_and_authentication()

#     load_info = pipeline.run(pokemon_source)
#     print(load_info)  # noqa: T201