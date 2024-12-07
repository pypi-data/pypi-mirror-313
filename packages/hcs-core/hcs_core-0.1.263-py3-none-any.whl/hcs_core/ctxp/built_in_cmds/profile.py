"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
import sys
import json
import questionary
from hcs_core.ctxp import util, panic, profile, cli_processor


@click.group(name="profile", cls=cli_processor.LazyGroup)
def profile_cmd_group():
    """Commands for profile."""


@profile_cmd_group.command()
def list():
    """List all profile names."""
    return profile.names()


@profile_cmd_group.command()
@click.argument("name", required=False)
def use(name: str):
    """Switch to a specific profile. If no name specified, launch interactive list to choose profile."""

    if name:
        if profile.use(name) is None:
            panic("No such profile: " + name)
    else:
        current = profile.name()
        choices = profile.names()
        if not choices:
            panic("No profile available.")

        ret = questionary.select("Select profile", choices, default=current, show_selected=True).ask()
        if ret:
            if profile.use(ret) is None:
                panic("No such profile: " + name)
        else:
            # aborted
            return "", 1


@profile_cmd_group.command()
@click.option("--from-name", "-f", required=False)
@click.option("--to-name", "-t", required=True)
def copy(from_name: str, to_name: str):
    """Copy profile."""

    if not from_name:
        from_name = profile.name()

    data = profile.get(from_name)
    if not data:
        panic("No such profile: " + from_name)
    if profile.exists(to_name):
        panic("Profile already exists: " + to_name)
    profile.create(to_name, data, True)


@profile_cmd_group.command()
@click.argument("name", required=False)
def get(name: str):
    """Get content of a specific profile."""
    if name:
        data = profile.get(name)
        if data is None:
            panic(
                "Profile not found. Use 'hcs profile list' to show available profiles, or 'hcs profile init' to create one."
            )
    else:
        data = profile.current()
        if data is None:
            panic(
                "Default profile not set. Use 'hcs profile list' to show available profiles, 'hcs profile user <name>' to switch to a profile, or 'hcs profile init' to create one."
            )

    return data


@profile_cmd_group.command()
@click.argument("name")
def delete(name: str):
    """Delete a profile by name."""
    profile.delete(name)


@profile_cmd_group.command()
@click.argument("name", required=False)
def file(name: str):
    """Show file location of a profile by name."""
    if not name:
        name = profile.name()
    return profile.file(name)


@profile_cmd_group.command()
@click.argument("name", type=str)
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
def create(name: str, file):
    """Create a profile from file or STDIN."""
    with file:
        text = file.read()
    try:
        data = json.loads(text)
    except Exception as e:
        panic(f"Invalid json {e}")

    profile.create(name, data)


@profile_cmd_group.command()
def name():
    """Get current profile name."""
    return profile.name()


@profile_cmd_group.command()
@click.argument("name", type=str, required=False)
def edit(name: str):
    """Launch platform-specific editor to edit the profile file."""

    if not name:
        name = profile.name()
    file_name = profile.file(name)
    util.launch_text_editor(file_name)
