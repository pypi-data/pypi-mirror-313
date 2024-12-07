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

import pathlib
from typing import Any
import os
from . import jsondot


class _StateFile:
    def __init__(self, file_path: str):
        self._path = file_path
        self._cache = None
        pathlib.Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

    def _data(self, reload: bool = False):
        if self._cache is None or reload:
            self._cache = jsondot.load(self._path, {}, lock=True)
        return self._cache

    def get(self, key: str, default: Any, reload: bool = False):
        return self._data(reload).get(key, default)

    def set(self, key: str, value: Any):
        self._data()[key] = value
        jsondot.save(self._cache, self._path, lock=True)


_file: _StateFile = None


def init(store_path: str, name: str):
    global _file
    _file = _StateFile(os.path.join(store_path, name))


def get(key: str, default: Any, reload: bool = False):
    return _file.get(key=key, default=default, reload=reload)


def set(key: str, value: Any):
    _file.set(key, value)
