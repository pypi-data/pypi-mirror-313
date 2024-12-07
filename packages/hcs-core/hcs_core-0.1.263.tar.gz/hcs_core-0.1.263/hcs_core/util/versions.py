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

import logging
import httpx
import time
import hcs_core
import pkg_resources

from packaging.version import Version

log = logging.getLogger(__name__)


def check_upgrade():
    last_upgrade_check_at = "last_upgrade_check_at"
    checked_at = hcs_core.ctxp.state.get(last_upgrade_check_at, 0)

    now = time.time()
    if now - checked_at > 24 * 60 * 60:
        try:
            latest = get_latest_version()
            current = Version(get_version())
            if current < latest:
                log.warning(f"New version available: {latest}. Execute 'hcs upgrade' to upgrade.")
        except Exception as e:
            logging.debug(e)

    hcs_core.ctxp.state.set(last_upgrade_check_at, now)


def get_version():
    return pkg_resources.require("hcs-cli")[0].version


def get_latest_version() -> Version:
    res = httpx.get("https://pypi.org/pypi/hcs-cli/json")
    names = res.json().get("releases").keys()
    versions = [Version(n) for n in names]
    versions.sort(reverse=True)
    return versions[0]


def is_version(s: str):
    try:
        return Version(s)
    except ValueError:
        return False
