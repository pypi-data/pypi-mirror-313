import pytest
from click.testing import CliRunner

from hashboard.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner: CliRunner):
    """Very basic smoke test for cli."""
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "hb" in result.output
