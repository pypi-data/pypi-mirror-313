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

import os
import logging
from os import path, listdir
from typing import Any
from collections.abc import Generator
from . import jsondot
from .jsondot import dotdict
import yaml
import shutil


log = logging.getLogger(__name__)


def _validate_key(key: str):
    # if key.find(os.pathsep) >= 0:
    if key.find("/") >= 0 or key.find("\\") >= 0:
        raise Exception("Invalid profile name: " + key)


def _load_yaml(file_name: str):
    if not os.path.exists(file_name):
        return
    with open(file_name, "r") as file:
        ret = yaml.safe_load(file)
        return jsondot.dotify(ret)


def _load_text(file_name: str) -> str:
    if not os.path.exists(file_name):
        return
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def _load_file(file_path: str, format: str):
    try:
        _, ext = path.splitext(file_path)

        if ext == ".json" or (ext == "" and format == "json"):
            return jsondot.load(file_path, lock=True)
        if ext == ".yaml" or ext == ".yml" or (ext == "" and (format == "yaml" or format == "yml")):
            return _load_yaml(file_path)
        if ext == ".txt" or (ext == "" and format in ["text", "plain", "txt"]):
            return _load_text(file_path)

        if format != "auto":
            raise Exception(f"Invalid store format: {format}")

        # The specified path has no ext name, and format is auto.
        if os.path.exists(file_path):
            return jsondot.load(file_path, lock=True)

        tmp = file_path + ".json"
        if os.path.exists(tmp):
            return jsondot.load(file_path + ".json", lock=True)

        tmp = file_path + ".yaml"
        if os.path.exists(tmp):
            return _load_yaml(tmp)

        tmp = file_path + ".yml"
        if os.path.exists(tmp):
            return _load_yaml(tmp)

        # Not found
    except Exception as e:
        raise Exception(f"Fail with file {file_path}") from e


def _list_sub_dirs(directory, depth):
    def recursive_list(current_dir, current_depth, base_dir):
        if depth != -1 and current_depth > depth:
            return []
        subdirs = []
        with os.scandir(current_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    rel_path = os.path.relpath(entry.path, base_dir)
                    subdirs.append(rel_path)
                    subdirs.extend(recursive_list(entry.path, current_depth + 1, base_dir))
        return subdirs

    return recursive_list(directory, 0, directory)


class _ManagedDict(dict):
    def __init__(self, initial_data: dict, store: "fstore", name: str):
        super().__init__(initial_data)
        self._store = store
        self._name = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._store.save(self._name, self)


class fstore:
    """A key-value store, optionally backed by a file system directory and files in it."""

    def __init__(self, store_path: str = None, create: bool = True):
        """Initialize the store

        Args:
                store_path (str): The path to store state files. If None, state will not be stored.
        create (bool, optional): If store_path is specified, try creating it if not exist. Defaults to True.

        Raises:
                Exception: [description]
        """
        if store_path:
            store_path = path.realpath(store_path)
            if not path.exists(store_path):
                if create:
                    os.makedirs(store_path)
                else:
                    raise Exception(f"Store path does not exist: {store_path}")
            elif not os.path.isdir(store_path):
                raise Exception(f"Store path is not a directory: {store_path}")
            self._path = store_path
        else:
            self._path = None
        self._cache = {}

    def get(self, key: str, reload: bool = False, format: str = "auto", default=None) -> dotdict:
        _validate_key(key)
        if self._path and (reload or key not in self._cache):
            file_path = self._get_path(key)
            log.debug(f"Read {file_path}")
            data = _load_file(file_path, format)
            if data is not None:
                self._cache[key] = data
        else:
            data = self._cache.get(key)

        if data is None and default is not None:
            return jsondot.dotify(default)
        return data

    def exists(self, key: str) -> bool:
        _validate_key(key)
        if key in self._cache:
            return True
        return path.exists(path.join(self._path, key))

    def _get_path(self, key: str) -> str:
        if not self._path:
            return None
        return path.join(self._path, key)

    def save(self, key: str, data: Any, format: str = "auto") -> Any:
        _validate_key(key)

        if format == "auto":
            if isinstance(data, str):
                format = "text"
            else:
                format = "json"

        data = jsondot.dotify(data)

        self._cache[key] = data
        if self._path:
            file_path = self._get_path(key)
            log.debug(f"Write {file_path}")
            if format == "json":
                jsondot.save(data, file_path, lock=True)
            elif format == "text":
                with open(file_path, "w", encoding="utf-8") as outfile:
                    # TODO lock
                    outfile.write(str(data))
            elif format == "json-compact":
                jsondot.save(data, file_path, format=False, lock=True)
            elif format == "yaml":
                with open(file_path, "w", encoding="utf-8") as outfile:
                    # TODO lock
                    yaml.safe_dump(data, outfile)
            else:
                raise Exception(f"Invalid format. key={key}, format={format}")

        return data

    def delete(self, key: str) -> None:
        key = str(key)
        _validate_key(key)
        self._cache.pop(key, None)
        if self._path:
            file_path = self._get_path(key)
            if os.path.exists(file_path):
                os.remove(file_path)

    def keys(self) -> list[str]:
        if self._path:
            return [f for f in listdir(self._path) if path.isfile(path.join(self._path, f))]
        return list(self._cache.keys())

    def children(self, depth: int = 0) -> list[str]:
        """List child stores"""
        if self._path:
            if depth == 0:
                return [f for f in listdir(self._path) if path.isdir(path.join(self._path, f))]
            else:

                return _list_sub_dirs(self._path, depth)

        raise Exception("TODO: list children for RAM store")

    def child(self, name) -> "fstore":
        return fstore(self._path + "/" + name)

    def values(self) -> Generator[Any, None, None]:
        for k in self.keys():
            yield self.get(k)

    def items(self) -> Generator[tuple[str, dict], None, None]:
        for k in self.keys():
            yield (k, self.get(k))

    def clear(self) -> None:
        for k in self.keys():
            self.delete(k)

    def destroy(self) -> None:
        self._cache.clear()
        if self._path:
            shutil.rmtree(self._path)

    def size(self) -> int:
        return len(self.keys())

    def contains(self, key: str) -> bool:
        if key in self._cache:
            return True
        return key in self.keys()

    # ----------------- Helpers -----------------

    def patch(self, key: str, data: dict) -> dotdict:
        existing_data = self.get(key)
        if existing_data is None:
            existing_data = jsondot.dotify({})
        existing_data |= data
        self.save(key, existing_data)
        return existing_data

    def doc(self, key: str) -> dict:
        data = self.get(key, {})
        return _ManagedDict(data, self, key)
