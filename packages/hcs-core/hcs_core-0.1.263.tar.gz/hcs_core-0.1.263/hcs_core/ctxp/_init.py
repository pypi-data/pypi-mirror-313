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
from os import path
from pathlib import Path
from . import profile
from . import state
from . import config
from . import cli_processor

user_home = str(Path.home())


def init(
    cli_name: str,
    main_cli: click.Group,
    commands_dir: str = "./cmds",
    store_path: str = user_home,
    config_path="./config",
):
    try:
        real_store_path = path.join(store_path, "." + cli_name)
        state.init(real_store_path, ".state")
        profile.init(real_store_path)
        config.init(config_path)

        return cli_processor.init(main_cli, commands_dir)
    except Exception as e:
        # critical errors, must print stack trace.
        if _need_stack_trace(e):
            raise e
        else:
            # Other errors, no stack.
            from .util import panic

            panic(e)


def _need_stack_trace(e) -> bool:
    program_errors = [
        LookupError,
        TypeError,
        ValueError,
        ArithmeticError,
        NameError,
        SyntaxError,
        KeyError,
        AttributeError,
    ]
    for t in program_errors:
        if isinstance(e, t):
            return True
    return False
