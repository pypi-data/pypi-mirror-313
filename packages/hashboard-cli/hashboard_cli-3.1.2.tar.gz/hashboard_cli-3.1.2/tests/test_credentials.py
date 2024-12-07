import pytest

from hashboard.credentials import get_credentials
from tests.helpers import get_fixture_path


def test_get_valid_credentials():
    credentials = get_credentials(get_fixture_path("credentials_files/valid.json"))
    assert credentials.project_id == "test-project"
    assert credentials.access_key_id == "test-access-key-id"
    assert credentials.access_key_token == "test-access-key-token"


def test_get_invalid_credentials():
    with pytest.raises(RuntimeError):
        get_credentials(get_fixture_path("credentials_files/invalid.json"))


def test_get_valid_credentials_using_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("HASHBOARD_PROJECT_ID", "test-project-from-env")
    monkeypatch.setenv("HASHBOARD_ACCESS_KEY_ID", "test-access-key-id-from-env")
    monkeypatch.setenv("HASHBOARD_SECRET_ACCESS_KEY_TOKEN", "test-access-key-token-from-env")

    credentials = get_credentials(
        get_fixture_path("credentials_files/valid.json")
    )
    assert credentials.project_id == "test-project-from-env"
    assert credentials.access_key_id == "test-access-key-id-from-env"
    assert credentials.access_key_token == "test-access-key-token-from-env"


def test_get_invalid_credentials_using_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("HASHBOARD_PROJECT_ID","test-project-from-env")
    monkeypatch.setenv("HASHBOARD_ACCESS_KEY_ID", "test-access-key-id-from-env")

    with pytest.raises(RuntimeError):
        get_credentials(get_fixture_path("credentials_files/valid.json"))
