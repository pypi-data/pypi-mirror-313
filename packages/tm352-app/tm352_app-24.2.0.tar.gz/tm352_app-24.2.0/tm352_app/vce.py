# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""VCE-level checks."""

import os

from rich import print  # noqa: A004
from typer import Typer

app = Typer()


def post_css_in_home_directory(fix: bool) -> bool:
    """Check that there is no `postcss.config.js` in the home directory."""
    if "HOME" in os.environ:
        if os.path.isfile(os.path.join(os.environ["HOME"], "postcss.config.js")):
            if fix:
                try:
                    os.unlink(os.path.join(os.environ["HOME"], "postcss.config.js"))
                    print(
                        "[bold green]:wastebasket:  postcss.config.js found in the home directory and removed.\n",
                        "  Details: http://docs.ocl.open.ac.uk/tm352/24j/faq/issues/postcss-config-js.html\n",
                    )
                except Exception:
                    print(
                        "[bold red]:x: postcss.config.js found in the home directory could not be removed. Please delete this file.\n"  # noqa: E501
                        "  [bold red]Details: http://docs.ocl.open.ac.uk/tm352/24j/faq/issues/postcss-config-js.html\n",
                    )
                    return False
            else:
                print(
                    "[bold red]:x: postcss.config.js found in the home directory. Please delete this file.\n",
                    "  [bold red]Details: http://docs.ocl.open.ac.uk/tm352/24j/faq/issues/postcss-config-js.html\n",
                )
                return False
    return True


@app.command()
def check(fix: bool = False) -> None:
    """Run all VCE checks."""
    success = True
    success = success and post_css_in_home_directory(fix)
    if success:
        print("[bold green]:+1: All checks passed successfully")
    else:
        print(
            "\n:x: Errors have been founded. Please check the output above and address these.\n",
            "  Some errors can be fixed automatically by running:\n\n     tm352 vce check --fix\n",
        )
