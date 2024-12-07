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

import json
import os.path
import copy
import time
import random
import portalocker
from typing import Any


"""
jsondot is utility to make json/dict object accessible in the "." way.

##########
#Example 1: load, update, and save JSON file
##########

data = jsondot.load('path/to/my.json')
print(data.hello.message)
data.hello.message = 'Hello, mortal.'
jsondot.save(data, 'path/to/my.json')


##########
#Example 2: decorate an existing python dict
##########

my_dict = jsondot.dotify(my_dict)
print(my_dict.key1.key2)
"""


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __lt__(self, other):
        # to support tuple-based sort. (dotdict_a < dotdict_b)
        return True

    def __deepcopy__(self, memo=None):
        # To workaround deepcopy with some python version
        new = {}
        for key in self.keys():
            new[key] = copy.deepcopy(self[key], memo=memo)
        return new


# TODO: how to remove the lib-specific dependency from this utility class?
# Register the represent_dict function with SafeDumper
def _represent_dict(dumper, data):
    return dumper.represent_dict(data.items())


import yaml

yaml.SafeDumper.add_representer(dotdict, _represent_dict)


def dotify(target: Any) -> Any:
    """Deeply convert an object from dict to dotdict"""

    # If already dotified, skip
    if isinstance(target, dotdict):
        return target
    if isinstance(target, list):
        for i in range(len(target)):
            target[i] = dotify(target[i])
        return target
    if isinstance(target, dict):
        for k in target:
            target[k] = dotify(target[k])
        return dotdict(target)

    # Return unchanged
    return target


def undot(target: Any) -> Any:
    """Deeply convert an object from dotdict to plain dictd"""
    if isinstance(target, list):
        for i in range(len(target)):
            target[i] = undot(target[i])
        return target
    if isinstance(target, dict):
        ret = {}
        for k in target:
            ret[k] = undot(target[k])
        return ret
    return target


def _is_primitive(obj):
    return isinstance(obj, str) or isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float)


def plain(target: Any) -> Any:
    """Deeply convert a dotdict from dict"""
    if _is_primitive(target):
        return target

    if isinstance(target, list):
        for i in range(len(target)):
            target[i] = plain(target[i])
        return target
    if isinstance(target, dict):
        for k in target:
            target[k] = plain(target[k])
        return dict(target)


def parse(text: str) -> dotdict:
    dict = json.loads(text)
    return dotify(dict)


def _lock_with_retry(file, for_read: bool):
    if for_read:
        flags = portalocker.LockFlags.SHARED
    else:
        flags = portalocker.LockFlags.EXCLUSIVE  # | portalocker.LockFlags.NON_BLOCKING

    max_retry = 6
    retry = 0
    backoff_seconds = 0.05
    while True:
        try:
            portalocker.lock(file, flags)
            return
        except Exception as e:
            retry += 1
            if retry > max_retry:
                raise Exception(f"Fail locking file {file}") from e
            random_delay = backoff_seconds + random.uniform(0, 0.1)
            time.sleep(random_delay)
            backoff_seconds += backoff_seconds


def load(file: str, default: Any = None, lock: bool = False) -> Any:
    try:
        if not os.path.exists(file):
            return dotify(default)
        with open(file) as json_file:
            if lock:
                _lock_with_retry(json_file, True)
            dict = json.load(json_file)
        return dotify(dict)
    except Exception as e:
        raise Exception(f"Error loading file {file}") from e


def save(data: dict, file, format=True, lock: bool = False) -> None:
    with open(file, "w") as outfile:
        if lock:
            _lock_with_retry(outfile, False)
        if format:
            json.dump(data, outfile, indent="\t", default=vars)
        else:
            json.dump(data, outfile)
