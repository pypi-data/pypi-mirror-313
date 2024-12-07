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

from copy import deepcopy
import pathlib
import shutil
import os
from typing import Any
from .util import panic, CtxpException
from .jsondot import dotdict, dotify
from . import state
from .data_util import load_data_file, save_data_file

_repo_path: str = None
_active_profile_name: str = None
_data: dotdict = None
_auth_cache: dict = None


def _set_active_profile_name(name):
    global _active_profile_name
    _active_profile_name = name
    state.set("active_profile", name)


def init(repo_path: str, active_profile_name: str = None) -> None:
    if active_profile_name:
        _set_active_profile_name(active_profile_name)

    global _repo_path
    _repo_path = repo_path


def path(profile_name: str = None) -> str:
    """Get directory name of a profile"""
    if not profile_name:
        profile_name = name()
    return os.path.join(_repo_path, profile_name)


def create(name: str, data: dict, auto_use: bool = True, overwrite: bool = False):
    if not overwrite and exists(name):
        if auto_use:
            use(name)
        raise CtxpException("Profile already exists: " + name)
    file_path = file(name)
    pathlib.Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
    save_data_file(data, file(name), "yaml", 0o600)
    if auto_use:
        use(name)
    return get(name)


def copy(from_name: str, to_name: str, overwrite: bool = True):
    if exists(to_name) and not overwrite:
        raise CtxpException("Profile already exists: " + to_name)
    data = get(from_name)
    if not data:
        raise CtxpException("Profile does not exist: " + from_name)
    create(to_name, deepcopy(data), auto_use=False)


def current(reload: bool = False, exit_on_failure=True, exclude_secret: bool = False) -> dict:
    """Get content of the current active profile"""
    profile_name = name()
    data = get(profile_name, reload)

    if data is None and exit_on_failure:
        panic(
            "Profile not set. Use 'hcs profile use [profile-name]' to choose one, or use 'hcs profile init' to create default profiles."
        )

    if exclude_secret:
        data = dotdict(dict(data))
        csp_config = dict(data.get("csp", {}))
        if csp_config:
            csp_config["apiToken"] = None
            csp_config["clientSecret"] = None
            data["csp"] = csp_config
    return data


def save():
    """Save the current profile"""
    global _data
    if _data is None:
        return
    write(name(), _data)


def write(profile_name: str, data: dict):
    """Save profile by name"""
    save_data_file(data, file(profile_name), "yaml", 0o600)


def name() -> str:
    """Get the current active profile name"""
    global _active_profile_name
    if not _active_profile_name:
        _active_profile_name = state.get("active_profile", default="default")
        if not exists(_active_profile_name):
            _set_active_profile_name("default")
    return _active_profile_name


def use(name: str) -> str:
    """Use to the specified profile"""

    profile_exists = name in names()
    if not profile_exists:
        return

    _set_active_profile_name(name)
    return name


def names() -> list[str]:
    """List profile names"""
    ret = [f for f in os.listdir(_repo_path) if os.path.isdir(os.path.join(_repo_path, f))]
    ret.sort()
    return ret


def delete(profile_name: str = None) -> None:
    """Delete a profile"""

    if profile_name is None:
        profile_name = name()
    global _active_profile_name, _data
    if _active_profile_name == profile_name:
        _active_profile_name = "default"
        _data = None

    shutil.rmtree(os.path.join(_repo_path, profile_name), ignore_errors=True)


def get(profile_name: str, reload: bool = False, default=None) -> dotdict:
    """Get profile data by name"""
    if profile_name == name():
        global _data
        if _data is not None and not reload:
            return _data
        data = load_data_file(file(profile_name), default=default)
        if data is not None:
            data = dotify(data)
            _data = data
    else:
        data = load_data_file(file(profile_name), default=default)
        if data is not None:
            data = dotify(data)
    return data


def file(profile_name: str) -> str:
    """Get the file path of a profile"""
    return os.path.join(_repo_path, profile_name, "profile.yml")


def exists(profile_name: str) -> bool:
    if profile_name not in names():
        return False
    return os.path.isfile(file(profile_name))


class auth:
    @staticmethod
    def _file_name() -> str:
        return os.path.join(_repo_path, name(), ".auth")

    @staticmethod
    def get() -> dict:
        global _auth_cache
        if _auth_cache is None:
            _auth_cache = load_data_file(auth._file_name(), {}, "yaml")
        return dotify(deepcopy(_auth_cache))

    @staticmethod
    def set(data: dict) -> None:
        global _auth_cache
        import json

        if json.dumps(data) == json.dumps(_auth_cache):
            return
        _auth_cache = deepcopy(data)
        file_name = auth._file_name()
        save_data_file(data, file_name, "yaml", 0o600)

    @staticmethod
    def delete() -> None:
        file_name = auth._file_name()
        if os.path.exists(file_name):
            os.unlink(file_name)
        global _auth_cache
        _auth_cache = None


# --------------------------------------------------


def _nested_obj_to_plain_dict(obj: Any, path: str, result: dotdict) -> None:
    t = type(obj)
    if t is str or t is int or t is float or t is bool:
        result[path] = obj
    elif t is dict or t is dotdict:
        for k in obj:
            v = obj[k]
            _nested_obj_to_plain_dict(v, path + "." + k, result)
    elif t is list:
        for i in range(len(obj)):
            v = obj[i]
            _nested_obj_to_plain_dict(v, path + "[" + i + "]", result)
    else:
        raise Exception(f"TODO: type={t}")


def plain() -> dotdict:
    _plain = dotdict()
    data = current()
    for k in data:
        _nested_obj_to_plain_dict(data[k], k, _plain)

    return _plain


# --------------------------------------------------
