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

from typing import Any
from .profile_store import profile_store, fstore
import re
import json
from . import jsondot


def _store() -> fstore:
    return profile_store("context")


def list() -> list:
    return _store().keys()


def get(name: str, reload: bool = False, default=None) -> jsondot.dotdict:
    return _store().get(key=name, reload=reload, default=default)


def set(name: str, data: dict):
    return _store().save(name, data)


def delete(name: str):
    return _store().delete(name)


def file(name: str):
    return _store()._get_path(name)


def clear():
    return _store().clear()


class Context:
    def __init__(self, name):
        self.name = name
        self._store = _store()
        self._data = None
        self._changed = False

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        existing = self._data.get(key)
        if existing != value:
            self._changed = True
            self._data[key] = value
        return self

    def remove(self, key: str):
        if key in self._data:
            self._changed = True
            del self._data[key]

    def __enter__(self):
        self._data = self._store.get(key=self.name, reload=False, default={})

    def __exit__(self, exc_type, exc_value, traceback):
        if self._changed:
            self._store.save(key=self.name, data=self.data)
        return False

    def apply_variables(self, object: any, additional_vars: dict = None):

        mapping = self._data.copy()
        if additional_vars:
            mapping.update(additional_vars)

        # The Python default Template.substitute has too many limitations...
        def substitute(text: str):
            pattern = re.compile(".*\${(.+?)}.*")
            while True:
                m = pattern.match(text)
                if not m:
                    break
                name = m.group(1)
                text = text.replace("${" + name + "}", self.get(name))
            return text

        t = type(object)
        try:
            if t is str:
                return substitute(object)

            if t is dict:
                text = json.dumps(object)
                text = substitute(text)
                return json.loads(text)

            if t is jsondot.dotdict:
                text = json.dumps(object)
                text = substitute(text)
                return jsondot.parse(text)
        except KeyError as e:
            raise Exception("Variable not defined in context") from e

    def load_template(self, name: str):
        # with open(name) as f:
        #     text = f.read()
        # return apply_variables(text)

        tmpl = jsondot.load(name)
        return self.apply_variables(tmpl)
