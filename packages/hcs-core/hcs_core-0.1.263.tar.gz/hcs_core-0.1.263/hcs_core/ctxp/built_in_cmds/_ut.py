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
import hcs_core.ctxp as ctxp
import hcs_core.ctxp.cli_options as cli
import hcs_core.ctxp.util as util


@click.group(hidden=True)
def cli_test():
    """Commands for context. Each profile has its own context. The commands work for the current profile."""


@cli_test.command()
def echo_none():
    return


def _format_custom_table(data: list) -> str:
    fields_mapping = {"id": "Id", "opt": "Opt"}
    return util.format_table(data, fields_mapping)


@cli_test.command()
@click.option("--opt")
@click.argument("id")
def echo_obj(opt: str, id: str):
    return {"id": id, "opt": opt}


@cli_test.command()
@click.option("--opt")
@click.argument("ids", nargs=-1)
@cli.formatter(_format_custom_table)
def echo_obj_list(opt: str, ids: tuple[str]):
    ret = []
    for i in ids:
        ret.append({"id": i, "opt": opt})
    return ret


@cli_test.command()
@click.argument("arg1", type=int)
def echo_int(arg1: int):
    return arg1


@cli_test.command()
@click.argument("arg1", type=int, nargs=-1)
def echo_int_list(arg1: tuple[int]):
    return list(arg1)


@cli_test.command()
@click.argument("arg1", type=str)
def echo_str(arg1: str):
    return arg1


@cli_test.command()
@click.argument("arg1", type=str, nargs=-1)
def echo_str_list(arg1: tuple[str]):
    return list(arg1)


@cli_test.command()
@click.argument("arg1", type=bool)
def echo_bool(arg1: bool):
    return arg1


@cli_test.command()
@click.argument("arg1", type=bool, nargs=-1)
def echo_bool_list(arg1: tuple[bool]):
    return list(arg1)


@cli_test.command()
@click.argument("arg1", type=float)
def echo_float(arg1: bool):
    return arg1


@cli_test.command()
@click.argument("arg1", type=float, nargs=-1)
def echo_float_list(arg1: tuple[bool]):
    return list(arg1)


@cli_test.command()
@click.option("--reason", type=str)
@click.option("--code", type=int)
@click.option("--ctxp-error/--tuple", type=bool)
def echo_error(reason: str, code: int, ctxp_error: bool):
    if ctxp_error:
        return ctxp.error(reason, code)
    return reason, code


@cli_test.command()
@click.option("--reason", type=str)
@click.option("--type", type=str)
def echo_exception(reason: str, type: str):
    root_cause = KeyError(reason)
    if type == "CtxpException":
        raise ctxp.CtxpException("pseudo-error") from root_cause
    if type == "TypeError":
        raise TypeError("pseudo-error") from root_cause
    if type == "httpx.HTTPStatusError":
        import httpx

        req = httpx.Request("GET", "http://ut")
        httpx.Response(400, text=reason, request=req).raise_for_status()
    if type == "Exception":
        raise Exception("pseudo-error") from root_cause
    raise Exception("Invalid exception type. This is an issue of the test case (caller).")
