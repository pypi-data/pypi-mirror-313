# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""TM352 CLI Application."""

from rich import print  # noqa: A004
from typer import Typer

from tm352_app.__about__ import __version__
from tm352_app.block2 import app as block2_app
from tm352_app.tma01 import app as tma01_app
from tm352_app.tma02 import app as tma02_app
from tm352_app.vce import app as vce_app

app = Typer()
app.add_typer(block2_app, name="block2", help="Commands for Block 2")
app.add_typer(tma01_app, name="tma01", help="Commands for TMA01")
app.add_typer(tma02_app, name="tma02", help="Commands for TMA02")
app.add_typer(vce_app, name="vce", help="Commands for checking the VCE")


@app.command()
def version() -> None:
    """Output the current application version."""
    print(__version__)
