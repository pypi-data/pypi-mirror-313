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

from .jsondot import dotdict
from .fstore import fstore

_store_impl: fstore = None


def init(config_path: str) -> None:
    global _store_impl
    _store_impl = fstore(config_path)


def get(name: str, reload: bool = False) -> dotdict:
    return _store_impl.get(name, reload)


def list() -> list:
    return _store_impl.keys()
