from dataclasses import dataclass
import json
import os.path
from typing import Optional

from hashboard.utils.env import env_with_fallback


@dataclass
class CliCredentials:
    access_key_id: str
    access_key_token: str
    project_id: str


def get_credentials(credentials_filepath: str) -> CliCredentials:
    """Returns the credentials to use, as specified by the user via environment variables or credentials filepath."""
    project_id_from_env = env_with_fallback("HASHBOARD_PROJECT_ID", "GLEAN_PROJECT_ID")
    access_key_id_from_env = env_with_fallback("HASHBOARD_ACCESS_KEY_ID", "GLEAN_ACCESS_KEY_ID")
    access_key_token_from_env = env_with_fallback("HASHBOARD_SECRET_ACCESS_KEY_TOKEN", "GLEAN_SECRET_ACCESS_KEY_TOKEN")
    if project_id_from_env and access_key_id_from_env and access_key_token_from_env:
        return CliCredentials(
            project_id=project_id_from_env,
            access_key_id=access_key_id_from_env,
            access_key_token=access_key_token_from_env,
        )
    elif [project_id_from_env, access_key_id_from_env, access_key_token_from_env].count(
        None
    ) < 3:
        raise RuntimeError(
            'Either all or none of these environment variables must be set: "HASHBOARD_PROJECT_ID", "HASHBOARD_ACCESS_KEY_ID", "HASHBOARD_SECRET_ACCESS_KEY_TOKEN"'
        )

    if not os.path.isfile(credentials_filepath):
        raise RuntimeError(f"Credentials file does not exist ({credentials_filepath})")

    with open(credentials_filepath, "r") as f:
        credentials_json = f.read()

    try:
        credentials = json.loads(credentials_json)
        return CliCredentials(**credentials)
    except Exception as e:
        raise RuntimeError("Invalid credentials file.") from e
