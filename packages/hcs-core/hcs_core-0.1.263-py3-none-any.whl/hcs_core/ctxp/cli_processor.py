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
from click.core import Group
import os.path as path
import os
import re
import importlib
import importlib.util
from pathlib import Path
from .util import print_output, print_error, validate_error_return, avoid_trace_for_ctrl_c
from .extension import ensure_extension

_eager_loading = os.environ.get("_CTXP_EAGER_LOAD")
if _eager_loading:
    print("_CTXP_EAGER_LOAD:", _eager_loading, file=sys.stderr)


class LazyGroup(click.Group):
    def __init__(self, mod_path: Path = None, extension=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod_path = mod_path
        self._lazy_commands_loaded = False
        self._extension = extension
        if _eager_loading:
            self._ensure_subcommands()

    def list_commands(self, ctx):
        self._ensure_subcommands()
        return super().list_commands(ctx)

    def get_command(self, ctx, cmd_name):
        self._ensure_subcommands()
        return super().get_command(ctx, cmd_name)

    def _ensure_subcommands(self):
        self._ensure_extension()
        if not self._lazy_commands_loaded and self.mod_path:
            _add_subcommands(self.mod_path.absolute(), self)
            self._lazy_commands_loaded = True

    def invoke(self, ctx):
        self._ensure_extension()
        return super().invoke(ctx)

    def _ensure_extension(self):
        if self._extension:
            ensure_extension(self._extension)


def _add_built_in_commands(group: Group):
    script_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), "."))
    build_in_cmds_dir = path.join(script_dir, "built_in_cmds")
    _add_subcommands(build_in_cmds_dir, group)


def _ensure_sub_group(current: Group, mod_path: Path):
    name = mod_path.name.replace("_", "-")
    meta = _read_group_meta(mod_path)
    help = meta.get("help")
    extension = meta.get("extension")

    subgroup = current.commands.get(name)
    if subgroup and isinstance(subgroup, Group):
        if isinstance(subgroup, LazyGroup):
            subgroup.mod_path = mod_path
        return subgroup

    subgroup = LazyGroup(extension=extension, name=name, help=help, mod_path=mod_path)
    current.add_command(subgroup)
    return subgroup


_property_pattern = re.compile("(.*)\\s*=\\s*(.*)$")


def _read_group_meta(mod_path: Path) -> dict:
    meta_file = mod_path.absolute().joinpath("__init__.py")

    ret = {"help": None, "hidden": False, "extension": None}
    if meta_file.exists():
        with open(meta_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                m = _property_pattern.match(line)
                if m:
                    name = m.group(1).strip()
                    value = eval(m.group(2))
                    ret[name] = value
    return ret


_excluded_names = ["__pycache__", "__init__.py", ".DS_Store"]


def _add_subcommands(commands_dir: str, group: Group):
    for mod_path in Path(commands_dir).glob("*"):
        if mod_path.name in _excluded_names:
            continue
        if mod_path.is_dir():
            _ensure_sub_group(group, mod_path)
        elif mod_path.name.endswith(".py"):
            _import_cmd_file(mod_path, group)
        else:
            pass
            # print("Unrecognized sub cmd: " + mod_path.name)
    return


def _import_cmd_file(mod_path: Path, parent: click.core.Group):
    mod_name = f"{mod_path}"
    # print("Loading ---> ", mod_name)

    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # mod = importlib.import_module(mod_name)
    # filter out any things that aren't a click Command
    cli_methods = []
    for attr in dir(mod):
        foo = getattr(mod, attr)
        if callable(foo):
            cli_methods.append(foo)

    known_groups = []

    def is_in_known_group(c: click.core.Command):
        for g in known_groups:
            if g.get_command(None, c.name):
                return True

    # Find groups first
    for foo in cli_methods:
        if isinstance(foo, click.core.Group):
            parent.add_command(foo)
            known_groups.append(foo)

    for foo in cli_methods:
        if isinstance(foo, click.core.Group):
            continue

        if isinstance(foo, click.core.Command):
            foo = _default_io(foo)  # decorate with default parameters
            if is_in_known_group(foo):
                continue
            parent.add_command(foo)


# Create a new decorator that combines the individual decorators
def _default_io(cmd: click.Command):

    from .cli_options import output, field, id_only, first

    cmd = output(cmd)
    # cmd = cli_options.verbose(cmd)
    cmd = field(cmd)
    cmd = id_only(cmd)
    cmd = first(cmd)
    callback = cmd.callback

    def inner(*args, **kwargs):
        io_args = {
            "output": kwargs.pop("output"),
            #'verbose': kwargs.pop('verbose'),
            "field": kwargs.pop("field"),
            "id_only": kwargs.pop("id_only"),
            "first": kwargs.pop("first"),
        }
        if io_args["output"] == "table":

            def _format(data):
                if not hasattr(callback, "formatter"):
                    from .util import CtxpException

                    raise CtxpException("Table output is specified, but no custom formatter specified on the command.")
                formatter = callback.__getattribute__("formatter")
                return formatter(data)

            io_args["format"] = _format
        ret = callback(*args, **kwargs)
        return _process_result(ret, **io_args)

    cmd.callback = inner
    return cmd


def _process_result(result, **kwargs):
    if result is None:
        return
    if isinstance(result, tuple):
        data, return_code = result

        is_error = isinstance(data, Exception) or return_code is not None
        if is_error:
            if return_code is None:
                return_code = 1
            validate_error_return(data, return_code)
            if isinstance(data, Exception):
                print_error(data)
            else:
                print_output(data, kwargs, file=sys.stderr)
            ctx = click.get_current_context()
            ctx.exit(return_code)
        # else fall-through
    elif isinstance(result, Exception):
        print_error(result)
        ctx = click.get_current_context()
        ctx.exit(1)
    else:
        print_output(result, kwargs)


def init(main_cli: click.Group, commands_dir: str):
    avoid_trace_for_ctrl_c()
    _add_built_in_commands(main_cli)
    _add_subcommands(commands_dir, main_cli)
    # main_cli.result_callback()(_process_result)
    ret = main_cli(obj={})
    return ret
