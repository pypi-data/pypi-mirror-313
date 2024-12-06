"""Test the basic main CLI functionality."""

from typer.testing import CliRunner

from tm352_app.__about__ import __version__
from tm352_app.__main__ import app

runner = CliRunner()


def test_version() -> None:
    """Test that the version output is correct."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__version__}\n"
