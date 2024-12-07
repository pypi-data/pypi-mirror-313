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

# Profile_store provides a utility method to create profile-scoped fstore

import os
from . import profile
from .fstore import fstore
from .util import CtxpException

_store_map: dict[str, fstore] = {}
_active_profile_name: str = None


def profile_store(store_name: str) -> fstore:
    global _store_map, _active_profile_name

    profile_name = profile.name()
    if not profile_name:
        raise CtxpException("Profile not specified")

    if profile_name != _active_profile_name:
        # profile changed
        _active_profile_name = profile_name
        _store_map = {}

    ret = _store_map.get(store_name)
    if ret is None:
        ret = _store_from_profile_name(profile_name, store_name)
        _store_map[store_name] = ret
    return ret


def _store_from_profile_name(profile_name: str, store_name: str) -> fstore:
    profile_path = profile.path(profile_name)
    store_path = os.path.join(profile_path, store_name)
    return fstore(store_path)
