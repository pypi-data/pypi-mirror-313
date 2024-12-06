# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@open.ac.uk>
#
# SPDX-License-Identifier: MIT
"""TMA01 commands."""

import os
import re
import shutil
import signal
import subprocess
import sys
from enum import Enum
from time import sleep
from urllib.parse import urlparse

import psutil
from rich import print  # noqa: A004
from typer import Typer

app = Typer()


@app.command()
def submit(student_pi: str) -> None:
    """Prepare a TMA01 submission."""
    warnings = False
    print(":magnifying_glass_tilted_left: Running a few checks prior to building your submission\n")
    if not os.path.isdir("tma01"):
        print(
            "[red bold]Error:[/red bold] No [cyan]tma01[/cyan] folder in the current folder. Check that you are in the folder that contains the tma01 folder"  # noqa: E501
        )
        return
    else:
        print(":white_check_mark: [cyan]tma01[/cyan] folder found")
    if os.path.isdir(os.path.join("tma01", "svelte-parking")):
        print(":white_check_mark: Svelte application found")
    else:
        print(":warning:  Svelte application not found (no [cyan]tma01/svelte-parking[/cyan] folder)")
        warnings = True
    if os.path.isfile(os.path.join("tma01", "svelte-parking", "src", "App.svelte")):
        with open(os.path.join("tma01", "svelte-parking", "src", "App.svelte")) as in_f:
            found = False
            for line in in_f.readlines():
                if re.match(r"\s*const\s+serverBaseUrl(?:\s*\:\s*string)?\s*=.*", line):
                    found = True
                    break
            if found:
                print(":white_check_mark: Svelte application's serverBaseUrl setting found")
            else:
                print(
                    ":warning:  May not be able to fix the API base URL in the Svelte application ([cyan]const serverBaseUrl = [/cyan] line not found)"  # noqa: E501
                )
                warnings = True
    else:
        print(
            ":warning:  May not be able to fix the API base URL in the Svelte application (no [cyan]tma01/svelte-parking/src/App.svelte[/cyan] file)"  # noqa: E501
        )
        warnings = True
    if os.path.isdir(os.path.join("tma01", "react-parking")):
        print(":white_check_mark: React application found")
    else:
        print(":warning:  React application not found (no [cyan]tma01/react-parking[/cyan] folder)")
        warnings = True
    if os.path.isfile(os.path.join("tma01", "react-parking", "src", "App.tsx")):
        with open(os.path.join("tma01", "react-parking", "src", "App.tsx")) as in_f:
            found = False
            for line in in_f.readlines():
                if re.match(r"\s*const\s+\[\s*serverBaseUrl\s*]\s*=\s*useState\s*\(.*", line):
                    found = True
            if found:
                print(":white_check_mark: React application's serverBaseUrl setting found")
            else:
                print(
                    ":warning:  May not be able to fix the API base URL in the React application ([cyan]const [serverBaseUrl] = useState [/cyan] line not found)"  # noqa: E501
                )
                warnings = True
    else:
        print(
            ":warning:  May not be able to fix the API base URL in the React application (no [cyan]tma01/react-parking/src/App.tsx[/cyan] file)"  # noqa: E501
        )
        warnings = True
    if os.path.isfile(f"tma01-{student_pi}-q1.zip"):
        print(":litter_in_bin_sign: Removing old submission file")
        os.unlink(f"tma01-{student_pi}-q1.zip")
    print(":hammer: Create the submission file")
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "zip",
            "-r",
            f"tma01-{student_pi}-q1.zip",
            "tma01",
            "-x",
            "**/node_modules/",
            "**/node_modules/**",
            "tma01/api-parking/",
            "tma01/api-parking/**",
            "**/dist/",
            "**/dist/**",
        ],
        check=True,
    )
    if result.returncode == 0:
        print(f":white_check_mark: Submission file tma01-{student_pi}-q1.zip created")
        if warnings:
            print(":warning: Warnings were raised during the build. Please check the logs above")
    else:
        print("[red bold]Error:[/red bold]: Failed to correctly create the submission file")


@app.command()
def extract(filename: str) -> None:
    """Extract the submission for marking."""
    print(f":hammer: Extracting submission from {filename}")
    if not os.path.isfile(filename):
        print(f"[red bold]Error:[/red bold] [cyan]{filename}[/cyan] not found")
        return
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
    print(":hammer: Adding backend API server")
    subprocess.run(  # noqa: S603
        ["chmod", "-R", "775", "tma01"],  # noqa: S607
        cwd="test",
        check=False,
    )
    print(":hammer: Adding backend API server")
    if os.path.isdir(os.path.join("test", "tma01", "api-parking")):
        print(":litter_in_bin_sign: Removing old backend API server")
        shutil.rmtree(os.path.join("test", "tma01", "api-parking"))
    if not os.path.isdir(os.path.join("skeletons", "tma01", "api-parking")):
        print(
            "[red bold]Error:[/red bold] Could not find backen API server at [cyan]skeletons/tma01/api-parking[/cyan]"
        )
        return
    print(":hammer: Copying the backend API server")
    shutil.copytree(
        os.path.join("skeletons", "tma01", "api-parking"),
        os.path.join("test", "tma01", "api-parking"),
    )
    print(":white_check_mark: Submission extracted and ready for testing")


class TestOptions(Enum):
    """Options for which application to test."""

    SVELTE = "svelte"
    REACT = "react"


@app.command()
def test(app: TestOptions) -> None:
    """Run the test server."""
    if not os.path.isdir(os.path.join("test", "tma01", "api-parking")):
        print(
            "\n\n[red bold]Error:[/red bold] Could not find backend API server at [cyan]test/tma01/api-parking[/cyan]\n"
            "Make sure that you are running the command from the [cyan]block_1[/cyan] folder\n"
        )
        return
    if os.path.exists(os.path.join("test", "tma01", f"{app.value}-parking")):
        print(f"\n:hammer: Installing {app.value} application dependencies\n")
        result = subprocess.run(  # noqa: S603
            ["npm", "ci"],  # noqa: S607
            cwd=os.path.join("test", "tma01", f"{app.value}-parking"),
            check=True,
        )
        if result.returncode != 0:
            print(f"\n\n[red bold]Error:[/red bold] Failed to install {app.value} application dependencies\n")
            return
        print(f":hammer: Running {app.value} application build")
        result = subprocess.run(  # noqa: S603
            ["npm", "run", "build"],  # noqa: S607
            cwd=os.path.join("test", "tma01", f"{app.value}-parking"),
            check=False,
        )
        if result.returncode == 0:
            print(f"\n:white_check_mark: Built the {app.value} application\n")
        else:
            print(
                f"\n\n:warning: Failed to build the {app.value} application. It may still run, but this cannot be guaranteed.\n"  # noqa: E501
            )
    else:
        print(
            f"\n[red bold]Error:[/red bold] Could not find Svelte application at [cyan]test/tma01/{app.value}-parking[/cyan]\n"  # noqa: E501
        )
        return
    api_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
    app_base = os.environ["JUPYTERHUB_SERVICE_PREFIX"] if "JUPYTERHUB_SERVICE_PREFIX" in os.environ else "/"
    api_path = "http://localhost:3000"
    app_path = "http://localhost:5173"
    if "VSCODE_PROXY_URI" in os.environ:
        url = urlparse(os.environ["VSCODE_PROXY_URI"])
        api_path = f"{url.scheme}://{url.netloc}"
        app_path = f"{url.scheme}://{url.netloc}"
        api_base = api_base + "proxy/absolute/3000"
        app_base = app_base + "proxy/absolute/5173"
    api_path = api_path + api_base
    app_path = app_path + app_base
    if not api_path.endswith("/"):
        api_path = api_path + "/"
    print(":hammer: Setting API base")
    api_base_found = False
    if app == TestOptions.SVELTE:
        app_component_path = os.path.join("test", "tma01", f"{app.value}-parking", "src", "App.svelte")
        if os.path.exists(app_component_path):
            for filename in os.listdir(os.path.join("test", "tma01", f"{app.value}-parking", "src")):
                if filename.endswith(".svelte"):
                    with open(os.path.join("test", "tma01", f"{app.value}-parking", "src", filename)) as in_f:
                        lines = in_f.readlines()
                    with open(os.path.join("test", "tma01", f"{app.value}-parking", "src", filename), "w") as out_f:
                        for line in lines:
                            if re.match(r"\s*const\s+serverBaseUrl(?:\s*\:\s*string)?\s*=.*", line):
                                out_f.write(f'const serverBaseUrl = "{api_path}";\n')
                                api_base_found = True
                            else:
                                out_f.write(line)
        else:
            print(
                f"\n[red bold]Error:[/red bold] Could not find Svelte App.svelte at [cyan]test/tma01/{app.value}-parking/src/App.svelte[/cyan]\n"  # noqa: E501
            )
            return
    elif app == TestOptions.REACT:
        app_component_path = os.path.join("test", "tma01", f"{app.value}-parking", "src", "App.tsx")
        if os.path.exists(app_component_path):
            for filename in os.listdir(os.path.join("test", "tma01", f"{app.value}-parking", "src")):
                if filename.endswith(".tsx") or filename.endswith(".jsx"):
                    with open(os.path.join("test", "tma01", f"{app.value}-parking", "src", filename)) as in_f:
                        lines = in_f.readlines()
                    with open(os.path.join("test", "tma01", f"{app.value}-parking", "src", filename), "w") as out_f:
                        skip = False
                        for line in lines:
                            if re.match(r"\s*const\s+\[\s*serverBaseUrl\s*]\s*=\s*useState\s*\(.*", line):
                                out_f.write(f'const [serverBaseUrl] = useState("{api_path}");\n')
                                api_base_found = True
                                skip = True
                            elif re.match(r"\s*const\s+serverBaseUrl(?:\s*\:\s*string)?\s*=.*", line):
                                out_f.write(f'const serverBaseUrl = "{api_path}";\n')
                                api_base_found = True
                            elif not skip:
                                out_f.write(line)
                            if ")" in line:
                                skip = False
        else:
            print(
                f"\n[red bold]Error:[/red bold] Could not find React App.tsx at [cyan]test/tma01/{app.value}-parking/src/App.tsx[/cyan]\n"  # noqa: E501
            )
            return
    if not api_base_found:
        print("""\n
[red bold]======================[/red bold]
[red bold]No serverBaseUrl found[/red bold]
[red bold]======================[/red bold]

No [cyan]serverBaseUrl[/cyan] could be found. The application may still work, but this cannot be guaranteed.

Press [green]Enter[/green] to continue
""")
        input()
    print("\n:hammer: Installing backend API server dependencies\n")
    result = subprocess.run(  # noqa: S603
        ["npm", "ci"],  # noqa: S607
        cwd=os.path.join("test", "tma01", "api-parking"),
        check=True,
    )
    if result.returncode != 0:
        print("\n[red bold]Error:[/red bold] Failed to install backend API server dependencies\n")
        return
    print("\n:hammer: Starting the backend API server\n")
    api_server = subprocess.Popen(  # noqa: S603
        ["npm", "run", "server"],  # noqa: S607
        cwd=os.path.join("test", "tma01", "api-parking"),
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
    print("\n:white_check_mark: Backend API server ready\n")
    frontend_server = subprocess.Popen(  # noqa: S603
        ["npm", "run", "dev"],  # noqa: S607
        cwd=os.path.join("test", "tma01", f"{app.value}-parking"),
        start_new_session=True,
    )
    while True:
        found = False
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr.port == 5173:  # noqa: PLR2004
                found = True
        if found:
            break
        sleep(1)
    print(f"\n:white_check_mark: {app.value} server ready\n")

    def shutdown_processes(sig, frame) -> None:  # noqa: ARG001, ANN001
        print(":hammer: Shutting down the API server")
        os.killpg(os.getpgid(api_server.pid), signal.SIGTERM)
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
