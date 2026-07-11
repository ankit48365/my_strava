"""Shared helpers for resolving, persisting, and activating Strava credentials."""

from dataclasses import dataclass
import os
from pathlib import Path

import dlt
from dlt.common.configuration.container import Container
from dlt.common.configuration.providers.toml import SecretsTomlProvider
from dlt.common.configuration.specs.pluggable_run_context import PluggableRunContext
from google.cloud import secretmanager

DEFAULT_GCP_PROJECT_ID = "mystrava-464501"
STRAVA_SECTION = ("sources", "strava")

CLIENT_ID_ENV = "SOURCES__STRAVA__CLIENT_ID"
CLIENT_SECRET_ENV = "SOURCES__STRAVA__CLIENT_SECRET"
ACCESS_TOKEN_ENV = "SOURCES__STRAVA__ACCESS_TOKEN"
REFRESH_TOKEN_ENV = "SOURCES__STRAVA__REFRESH_TOKEN"


@dataclass(frozen=True)
class StravaTokens:
    """The token pair returned by Strava refresh and authorization flows."""

    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class StravaCredentials:
    """The full credential set required to refresh Strava tokens."""

    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str


def is_running_in_cloud() -> bool:
    """Return True when the process is executing on Cloud Run."""

    return os.getenv("K_SERVICE") is not None


def load_strava_credentials(require_tokens: bool = True) -> StravaCredentials:
    """Load Strava credentials from env vars first, then from dlt secrets."""

    secret_values = dlt.secrets.get("sources.strava") or {}

    client_id = os.getenv(CLIENT_ID_ENV) or secret_values.get("client_id")
    client_secret = os.getenv(CLIENT_SECRET_ENV) or secret_values.get("client_secret")
    access_token = os.getenv(ACCESS_TOKEN_ENV) or secret_values.get("access_token")
    refresh_token = os.getenv(REFRESH_TOKEN_ENV) or secret_values.get("refresh_token")

    required_values = [
        ("client_id", client_id),
        ("client_secret", client_secret),
    ]
    if require_tokens:
        required_values.extend(
            [
                ("access_token", access_token),
                ("refresh_token", refresh_token),
            ]
        )

    missing = [name for name, value in required_values if not value]
    if missing:
        missing_csv = ", ".join(missing)
        raise RuntimeError(f"Missing Strava credentials: {missing_csv}")

    return StravaCredentials(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
    )


def persist_strava_tokens(tokens: StravaTokens) -> str:
    """Persist refreshed Strava tokens to the correct backing store."""

    if is_running_in_cloud():
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or DEFAULT_GCP_PROJECT_ID
        update_cloud_secret("strava_access_token", tokens.access_token, project_id)
        update_cloud_secret("strava_refresh_token", tokens.refresh_token, project_id)
        return "Google Secret Manager"

    secrets_path = update_local_secrets_file(tokens)
    return _display_path(secrets_path)


def update_local_secrets_file(
    tokens: StravaTokens, settings_dir: Path | str | None = None
) -> Path:
    """Update only the Strava tokens inside the local .dlt/secrets.toml file."""

    local_settings_dir = Path(settings_dir) if settings_dir else _get_settings_dir()
    local_settings_dir.mkdir(parents=True, exist_ok=True)

    provider = SecretsTomlProvider(str(local_settings_dir))
    provider.set_value("access_token", tokens.access_token, None, *STRAVA_SECTION)
    provider.set_value("refresh_token", tokens.refresh_token, None, *STRAVA_SECTION)
    provider.write_toml()

    return Path(provider.locations[0])


def prime_runtime_strava_tokens(tokens: StravaTokens) -> None:
    """Seed the current process with the fresh tokens for same-run dlt usage."""

    os.environ[ACCESS_TOKEN_ENV] = tokens.access_token
    os.environ[REFRESH_TOKEN_ENV] = tokens.refresh_token


def reload_dlt_credentials() -> None:
    """Reload dlt providers so secrets.toml and env-backed values are refreshed."""

    Container()[PluggableRunContext].reload_providers()


def update_cloud_secret(secret_name: str, new_value: str, project_id: str) -> None:
    """Write a new version for a Strava token in Google Secret Manager."""

    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_name}"
    client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": new_value.encode("utf-8")},
        }
    )


def _get_settings_dir() -> Path:
    """Resolve the local dlt settings directory for the active run context."""

    run_context = Container()[PluggableRunContext].context
    return Path(run_context.settings_dir)


def _display_path(path: Path) -> str:
    """Prefer a project-relative display path when possible."""

    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)
