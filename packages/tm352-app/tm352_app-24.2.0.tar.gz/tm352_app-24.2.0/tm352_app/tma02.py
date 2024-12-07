# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""TMA02 commands."""

import os
import re
import shutil
import signal
import subprocess
import sys
from time import sleep
from urllib.parse import urlparse

import psutil
from rich import print  # noqa: A004
from typer import Typer

app = Typer()


@app.command()
def submit(student_pi: str) -> None:
    """Prepare a TMA02 submission."""
    if not os.path.isdir("tma02"):
        print(
            "[red bold]Error:[/red bold] No [cyan]tma02[/cyan] folder in the current folder. Check that you are in the folder that contains the tma02 folder"  # noqa: E501
        )
        return
    if os.path.isfile(f"tma02-{student_pi}-q1.zip"):
        print(":litter_in_bin_sign: Removing old submission file")
        os.unlink(f"tma02-{student_pi}-q1.zip")
    print(":hammer: Create the submission file")
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "zip",
            "-r",
            f"tma02-{student_pi}-q1.zip",
            "tma02",
            "-x",
            "**/node_modules/",
            "**/node_modules/**",
            "**/dist/",
            "**/dist/**",
        ],
        check=True,
    )
    if result.returncode == 0:
        print(f":white_check_mark: Submission file tma02-{student_pi}-q1.zip created")
    else:
        print("[red bold]Error:[/red bold]: Failed to correctly create the submission file")


@app.command()
def test(filename: str) -> None:
    """Test the submission for marking."""
    print(f":hammer: Extracting submission from {filename}")
    if os.path.isdir("test"):
        print(":litter_in_bin_sign: Removing old files")
        shutil.rmtree("test")
    os.mkdir("test")
    result = subprocess.run(  # noqa: S603
        ["unzip", os.path.join("..", filename)],  # noqa: S607
        cwd="test",
        check=False,
    )
    if result.returncode == 0:
        print(":white_check_mark: Submission file extracted")
    else:
        print("[red bold]Error:[/red bold] Failed to correctly extract the submission file")
        return
    if not os.path.isdir(os.path.join("test", "tma02", "tma02-service")):
        print(
            "[red bold]Error:[/red bold] No [cyan]test/tma02/tma02-service[/cyan] folder in the current folder. Required service not included in the submission"  # noqa: E501
        )
        return
    if not os.path.isdir(os.path.join("test", "tma02", "tma02-app")):
        print(
            "[red bold]Error:[/red bold] No [cyan]test/tma02/tma02-app[/cyan] folder in the current folder. Required application not included in the submission"  # noqa: E501
        )
        return
    if not os.path.isdir(os.path.join("test", "tma02", "tma02-app", "web")):
        print(
            "[red bold]Error:[/red bold] No [cyan]test/tma02/tma02-app/web[/cyan] folder in the current folder. Required web application not included in the submission"  # noqa: E501
        )
        return
    print(":hammer: Installing service dependencies")
    result = subprocess.run(  # noqa: S603
        ["npm", "ci"],  # noqa: S607
        cwd=os.path.join("test", "tma02", "tma02-service"),
        check=False,
    )
    if result.returncode != 0:
        print("\n\n[red bold]Error:[/red bold] Failed to install service dependencies\n")
        return
    print(":hammer: Installing application dependencies")
    result = subprocess.run(  # noqa: S603
        ["npm", "ci"],  # noqa: S607
        cwd=os.path.join("test", "tma02", "tma02-app"),
        check=False,
    )
    if result.returncode != 0:
        print("\n\n[red bold]Error:[/red bold] Failed to install application dependencies\n")
        return
    print(":hammer: Installing web application dependencies")
    result = subprocess.run(  # noqa: S603
        ["npm", "ci"],  # noqa: S607
        cwd=os.path.join("test", "tma02", "tma02-app", "web"),
        check=False,
    )
    if result.returncode != 0:
        print("\n\n[red bold]Error:[/red bold] Failed to install web application dependencies\n")
        return

    api_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
    app_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
    api_path = "http://localhost:3000"
    app_path = "http://localhost:5173"
    if "VSCODE_PROXY_URI" in os.environ:
        url = urlparse(os.environ["VSCODE_PROXY_URI"])
        api_path = f"{url.scheme}://{url.netloc}"
        app_path = f"{url.scheme}://{url.netloc}"
        api_base = api_base + "proxy/3000"
        app_base = app_base + "proxy/absolute/5173"
    api_path = api_path + api_base
    app_path = app_path + app_base
    if not api_path.endswith("/"):
        api_path = api_path + "/"
    api_path = api_path + "photo/"

    print("\n:hammer: Fixing paths\n")
    apibase_fixed = False
    if os.path.exists(os.path.join("test", "tma02", "tma02-app", "libraries", "PhotoService.ts")):
        with open(os.path.join("test", "tma02", "tma02-app", "libraries", "PhotoService.ts")) as in_f:
            lines = in_f.readlines()
        with open(os.path.join("test", "tma02", "tma02-app", "libraries", "PhotoService.ts"), "w") as out_f:
            for line in lines:
                if re.search(r"apibase\s*=\s*", line) and not re.search(r"^\s*//", line):
                    out_f.write(f'const apibase = "{api_path}";')
                    apibase_fixed = True
                else:
                    out_f.write(line)

    if not apibase_fixed:
        print("""\n
[red bold]============================[/red bold]
[red bold]No apibase found / corrected[/red bold]
[red bold]============================[/red bold]

No [cyan]apibase[/cyan] was found in the [cyan]test/tma02/tma02-app/libraries/PhotoService.ts[/cyan] file. The application may still work, but this cannot be guaranteed.

Press [green]Enter[/green] to continue
""")  # noqa: E501
        input()

    print("\n:hammer: Starting the TMA02 service\n")
    tma02_service = subprocess.Popen(  # noqa: S603
        ["npm", "run", "dev"],  # noqa: S607
        cwd=os.path.join("test", "tma02", "tma02-service"),
        start_new_session=True,
    )
    while True:
        found = False
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr.port == 3000:  # noqa: PLR2004
                found = True
        if found:
            break
        sleep(1)
    print("\n:white_check_mark: TMA02 service ready\n")
    print("\n:hammer: Starting the TMA02 App\n")
    frontend_server = subprocess.Popen(  # noqa: S603
        ["npm", "run", "dev"],  # noqa: S607
        cwd=os.path.join("test", "tma02", "tma02-app", "web"),
        start_new_session=True,
        stdin=subprocess.DEVNULL,
    )
    while True:
        found = False
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr.port == 5173:  # noqa: PLR2004
                found = True
        if found:
            break
        sleep(1)
    print("\n:white_check_mark: Web application server ready\n")

    def shutdown_processes(sig, frame) -> None:  # noqa: ARG001, ANN001
        print(":hammer: Shutting down the TMA02 service")
        os.killpg(os.getpgid(tma02_service.pid), signal.SIGTERM)
        print(":hammer: Shutting down the TMA02 web application server")
        os.killpg(os.getpgid(frontend_server.pid), signal.SIGTERM)
        print(":white_check_mark: All servers shut down\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_processes)

    sleep(2)

    print(
        f"\n\n:white_check_mark: Ready for testing at [cyan bold]{app_path}[/cyan bold]. Press [green]Enter[/green] to shut down\n\n"  # noqa: E501
    )
    input()
    shutdown_processes(None, None)
