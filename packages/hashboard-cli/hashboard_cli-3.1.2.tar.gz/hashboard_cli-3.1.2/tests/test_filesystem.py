import pytest
from click.exceptions import ClickException

from hashboard.filesystem import (
    build_spec_from_local,
    local_resources,
    process_filepaths,
)
from hashboard.utils.grn import GRNComponents
from hashboard.utils.resource import Resource
from tests.helpers import get_fixture_path


@pytest.fixture
def clear_env(monkeypatch: pytest.MonkeyPatch):
    """Don't let actual env vars affect these tests"""
    monkeypatch.delenv("A_NAME", raising=False)


def test_environment_variable_substitution(clear_env, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("A_NAME", "substitution")

    PATH = "model_config_files/with_env_vars"

    build_spec = build_spec_from_local([get_fixture_path(PATH)], "")
    assert len(build_spec["inlineConfigFiles"]) == 1

    env_vars = build_spec["clientEnvVars"]

    # check that the file contents have the substituted value for name
    assert env_vars == [{"name": "A_NAME", "value": "substitution"}]


def test_file_validation():
    with pytest.raises(ClickException) as exception_info:
        build_spec_from_local(
            [get_fixture_path("model_config_files/with_invalid_files")], ""
        )
    assert "Could not parse file" in exception_info.value.args[0]


def test_local_resources():
    PATH = "model_config_files/with_env_vars"

    # cast paths to strings to make snapshots platform-independent
    display = lambda d: dict((str(k), v) for k, v in d.items())

    assert (
        display(local_resources(get_fixture_path("model_config_files/with_env_vars")))
    ) == {
        "file1.yml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "name": "$A_NAME", "grn": "m:RNuzTq-85qzAFKJ8"},
            grn=GRNComponents(resource_type="m", gluid="RNuzTq-85qzAFKJ8", alias=None),
        )
    }

    assert display(
        local_resources(get_fixture_path("model_config_files/with_invalid_files"))
    ) == {
        "alt_extension.yaml": Resource(
            hb_version="0.1",
            raw={"glean": "0.1", "note": ".yaml is okay too"},
            grn=None,
        ),
        "glean_file.json": Resource(
            hb_version="0.1",
            raw={"glean": "0.1", "key": "value"},
            grn=None,
        ),
        "has_grn.yml": Resource(
            hb_version="1.0",
            raw={
                "glean": "1.0",
                "grn": "m:RNuzTq-85qzAFKJ8",
                "preventUpdatesFromUI": True,
            },
            grn=GRNComponents(resource_type="m", gluid="RNuzTq-85qzAFKJ8", alias=None),
        ),
        "glean_file.yml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "key": "value"},
            grn=None,
        ),
    }

    # regression test that we are able to resolve GRNs for models in nested directories

    assert display(
        local_resources(get_fixture_path("model_config_files/with_nested_folders"))
    ) == {
        "inner_folder/model.yaml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "type": "model"},
            type="model",
            grn=None,
        ),
        "inner_folder/saved_view.yaml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "type": "saved_view", "model": "./model.yaml"},
            type="saved_view",
            grn=None,
        ),
    }

    assert display(
        local_resources(get_fixture_path("model_config_files/symlinks"))
    ) == {
        "models/model.yaml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "type": "model"},
            type="model",
            grn=None,
        ),
        "views/saved_view.yaml": Resource(
            hb_version="1.0",
            raw={
                "glean": "1.0",
                "type": "saved_view",
                "model": "../models/model.yaml",
            },
            type="saved_view",
            grn=None,
        ),
    }

    # Test to ensure files in hidden folders aren't being read
    assert display(
        local_resources(get_fixture_path("model_config_files/with_hidden_folders"))
    ) == {
        "model.yml": Resource(
            hb_version="1.0",
            raw={"glean": "1.0", "type": "model"},
            type="model",
            grn=None,
        ),
    }


def _get_test_processed_files(relative_path, root_dir=None):
    files, env_vars = process_filepaths(
        [get_fixture_path(relative_path)],
        "test-id",
        get_fixture_path(root_dir) if root_dir else None,
    )

    files.sort(key=lambda x: x["filename"])
    return files, env_vars


def test_file_matching():
    assert _get_test_processed_files("model_config_files/with_nested_folders") == (
        [
            {
                "parentDirectory": f"/tmp/repos/test-id/{get_fixture_path('model_config_files/with_nested_folders')}/inner_folder",
                "filename": "model.yaml",
                "fileContents": 'glean: "1.0"\ntype: model\n',
            },
            {
                "parentDirectory": f"/tmp/repos/test-id/{get_fixture_path('model_config_files/with_nested_folders')}/inner_folder",
                "filename": "saved_view.yaml",
                "fileContents": 'glean: "1.0"\ntype: saved_view\nmodel: ./model.yaml\n',
            },
        ],
        set(),
    )

    # Test glob result
    assert _get_test_processed_files(
        "model_config_files/with_nested_folders"
    ) == _get_test_processed_files("model_config_files/with_nested_folders/**/*.yaml")

    assert _get_test_processed_files(
        "model_config_files/with_nested_folders"
    ) == _get_test_processed_files("model_config_files/with_nested_folders/**/*")

    assert _get_test_processed_files("model_config_files/symlinks") == (
        [
            {
                "parentDirectory": f"/tmp/repos/test-id/{get_fixture_path('model_config_files/symlinks')}/models",
                "filename": "model.yaml",
                "fileContents": 'glean: "1.0"\ntype: model\n',
            },
            {
                "parentDirectory": f"/tmp/repos/test-id/{get_fixture_path('model_config_files/symlinks')}/views",
                "filename": "saved_view.yaml",
                "fileContents": 'glean: "1.0"\ntype: saved_view\nmodel: ../models/model.yaml\n',
            },
        ],
        set(),
    )

    # Test glob result
    assert _get_test_processed_files(
        "model_config_files/symlinks/**/*view.yaml"
    ) == _get_test_processed_files("model_config_files/symlinks/views")

    # Test single path result
    assert _get_test_processed_files(
        "model_config_files/symlinks/views/saved_view.yaml"
    ) == _get_test_processed_files("model_config_files/symlinks/views")

    # Test paths with .hbproject file root defined
    assert _get_test_processed_files(
        "model_config_files/with_nested_folders",
        "model_config_files/with_nested_folders",
    ) == (
        [
            {
                "parentDirectory": f"/tmp/repos/test-id/inner_folder",
                "filename": "model.yaml",
                "fileContents": 'glean: "1.0"\ntype: model\n',
            },
            {
                "parentDirectory": f"/tmp/repos/test-id/inner_folder",
                "filename": "saved_view.yaml",
                "fileContents": 'glean: "1.0"\ntype: saved_view\nmodel: ./model.yaml\n',
            },
        ],
        set(),
    )

    assert _get_test_processed_files(
        "model_config_files/with_nested_folders",
        "model_config_files/with_nested_folders",
    ) == _get_test_processed_files(
        "model_config_files/with_nested_folders/inner_folder",
        "model_config_files/with_nested_folders",
    )
