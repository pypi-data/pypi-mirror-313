# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""Test the VCE functionality."""

import os
from collections.abc import Generator
from contextlib import contextmanager
from copy import deepcopy

from typer.testing import CliRunner

from tm352_app.__main__ import app

runner = CliRunner()


@contextmanager
def switch_home_directory(path: str) -> Generator[str, None, None]:
    """Temporarily switch the HOME location in the OS environment."""
    old_environ = deepcopy(os.environ)
    try:
        temp_home_path = os.path.abspath(path)
        os.environ["HOME"] = temp_home_path
        yield temp_home_path
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_check_postcss_config_js_not_present() -> None:
    """Test that the vce check correctly passes when no postcss.config.js is set in the home directory."""
    with switch_home_directory("tests/fixtures/vce/root_postcss_config_js/empty") as home_path:  # noqa: F841
        result = runner.invoke(app, ["vce", "check"])
        assert result.exit_code == 0
        assert "All checks passed successfully" in result.stdout


def test_check_postcss_config_js_present() -> None:
    """Test that the vce check correctly notifies when a postcss.config.js is set in the home directory."""
    with switch_home_directory("tests/fixtures/vce/root_postcss_config_js/existing") as home_path:  # noqa: F841
        result = runner.invoke(app, ["vce", "check"])
        assert result.exit_code == 0
        assert "Errors have been founded" in result.stdout
        assert "postcss.config.js found in the home directory. Please delete this file." in result.stdout


def test_check_postcss_config_js_cleaned() -> None:
    """Test that the vce check correctly fixes a postcss.config.js that is set in the home directory."""
    with switch_home_directory("tests/fixtures/vce/root_postcss_config_js/empty") as home_path:
        try:
            with open(os.path.join(home_path, "postcss.config.js"), "w") as out_f:  # noqa: F841
                pass
            assert os.path.isfile(os.path.join(home_path, "postcss.config.js"))

            result = runner.invoke(app, ["vce", "check", "--fix"])
            assert result.exit_code == 0
            assert "All checks passed successfully" in result.stdout
        finally:
            if os.path.isfile(os.path.join(home_path, "postcss.config.js")):
                os.unlink(os.path.join(home_path, "postcss.config.js"))
