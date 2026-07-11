"""Tests for Strava credential persistence helpers."""

import os
from pathlib import Path
import tempfile
import tomllib
import unittest

from strava_credentials import (
    ACCESS_TOKEN_ENV,
    REFRESH_TOKEN_ENV,
    StravaTokens,
    prime_runtime_strava_tokens,
    update_local_secrets_file,
)

SAMPLE_SECRETS = """[sources.strava]
# Strava API credentials
client_id = "133027"
client_secret = "existing-secret"
access_token = "old-access-token"
refresh_token = "old-refresh-token"

[destination.bigquery.credentials]
project_id = "demo-project"
client_email = "runner@example.com"
"""


class StravaCredentialsTests(unittest.TestCase):
    """Regression tests for the credential update helpers."""

    def test_update_local_secrets_file_preserves_other_sections(self) -> None:
        """Only the Strava tokens should change when the secrets file is updated."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            settings_dir = Path(tmp_dir) / ".dlt"
            settings_dir.mkdir()
            secrets_path = settings_dir / "secrets.toml"
            secrets_path.write_text(SAMPLE_SECRETS, encoding="utf-8")

            written_path = update_local_secrets_file(
                StravaTokens(
                    access_token="new-access-token",
                    refresh_token="new-refresh-token",
                ),
                settings_dir=settings_dir,
            )

            self.assertEqual(written_path, secrets_path)

            updated_text = secrets_path.read_text(encoding="utf-8")
            updated_data = tomllib.loads(updated_text)

            self.assertEqual(
                updated_data["sources"]["strava"]["access_token"],
                "new-access-token",
            )
            self.assertEqual(
                updated_data["sources"]["strava"]["refresh_token"],
                "new-refresh-token",
            )
            self.assertEqual(updated_data["sources"]["strava"]["client_id"], "133027")
            self.assertEqual(
                updated_data["sources"]["strava"]["client_secret"],
                "existing-secret",
            )
            self.assertEqual(
                updated_data["destination"]["bigquery"]["credentials"]["project_id"],
                "demo-project",
            )
            self.assertEqual(
                updated_data["destination"]["bigquery"]["credentials"]["client_email"],
                "runner@example.com",
            )

            self.assertIn("# Strava API credentials", updated_text)
            self.assertIn("[destination.bigquery.credentials]", updated_text)

    def test_prime_runtime_strava_tokens_updates_process_environment(self) -> None:
        """Fresh tokens should be immediately available to the current process."""

        original_access = os.environ.get(ACCESS_TOKEN_ENV)
        original_refresh = os.environ.get(REFRESH_TOKEN_ENV)

        try:
            os.environ.pop(ACCESS_TOKEN_ENV, None)
            os.environ.pop(REFRESH_TOKEN_ENV, None)

            prime_runtime_strava_tokens(
                StravaTokens(
                    access_token="runtime-access",
                    refresh_token="runtime-refresh",
                )
            )

            self.assertEqual(os.environ[ACCESS_TOKEN_ENV], "runtime-access")
            self.assertEqual(os.environ[REFRESH_TOKEN_ENV], "runtime-refresh")
        finally:
            if original_access is None:
                os.environ.pop(ACCESS_TOKEN_ENV, None)
            else:
                os.environ[ACCESS_TOKEN_ENV] = original_access

            if original_refresh is None:
                os.environ.pop(REFRESH_TOKEN_ENV, None)
            else:
                os.environ[REFRESH_TOKEN_ENV] = original_refresh


if __name__ == "__main__":
    unittest.main()
