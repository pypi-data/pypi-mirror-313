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
import os
from hcs_core.ctxp import CtxpException
from hcs_core.ctxp import recent
from hcs_core.ctxp.cli_options import *

org_id = click.option(
    "--org",
    type=str,
    default=None,
    required=False,
    help="Specify org ID. If not specified, org ID from the current auth token will be used.",
)


def get_org_id(org: str = None) -> str:
    # 1st priority: user explicitly specified org
    with recent.of("org") as r:
        try:
            if org:
                return org

            # 2nd priority: environment variable
            org = os.environ.get("HCS_ORG")
            if org:
                return org

            # 3rd priority: last used
            org = r.get()
            if org:
                return org

            # 4th priority: org from the current auth token
            from hcs_core.sglib import auth

            auth_info = auth.details(False)
            if not auth_info:
                raise CtxpException("Not authorized. See 'hcs login --help'.")
            org = auth_info["org"]["id"]
            return org
        finally:
            if org:
                r.set(org)


def ensure_login():
    return get_org_id(None)
