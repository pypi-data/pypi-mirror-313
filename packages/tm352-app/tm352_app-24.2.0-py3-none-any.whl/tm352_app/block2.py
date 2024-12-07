# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""Block 2 commands."""

import os
import subprocess
from enum import Enum

from typer import Typer

app = Typer()


class ExpoVersion(str, Enum):
    """Expo versions enumeration."""

    live = "live"
    sdk51 = "sdk51"
    sdk51dev = "sdk51dev"


@app.command()
def build(part: str, activity: str, expo_version: ExpoVersion = ExpoVersion.live) -> None:
    """Run a Block 2 activity."""
    subprocess.run(  # noqa: S603
        [
            os.path.join(os.environ["HOME"], "block_2", "resources", "build.sh"),
            part,
            activity,
            expo_version.value,
            "build",
        ],
        shell=False,
        check=False,
    )


@app.command()
def doc(part: str, activity: str, expo_version: ExpoVersion = ExpoVersion.live) -> None:
    """Run a Block 2 documentation."""
    subprocess.run(  # noqa: S603
        [
            os.path.join(os.environ["HOME"], "block_2", "resources", "build.sh"),
            part,
            activity,
            expo_version.value,
            "doc",
        ],
        shell=False,
        check=False,
    )
