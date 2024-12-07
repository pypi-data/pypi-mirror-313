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
import subprocess
from importlib import reload, import_module
import pkg_resources
from .util import CtxpException


def ensure_extension(required: str, parent_module_name: str = None):
    installed = {pkg.key for pkg in pkg_resources.working_set}  # pylint: disable=not-an-iterable
    if required in installed:
        return

    msg = f"This command requires an extension: {required}. Install now?"
    click.confirm(click.style(msg, fg="yellow"), default=True, abort=True)

    cmd = f"pip install {required}"
    try:
        msg = f"Executing: '{cmd}'"
        click.echo(click.style(msg, fg="yellow"))
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, text=True, shell=True, check=True)
    except Exception as e:
        error_message = f"Fail installing extensions. Error details: {e}"
        raise CtxpException(error_message)

    if parent_module_name:
        m = import_module(parent_module_name)
        reload(m)
    else:
        import_module(required.replace("-", "_"))
    reload(pkg_resources)
