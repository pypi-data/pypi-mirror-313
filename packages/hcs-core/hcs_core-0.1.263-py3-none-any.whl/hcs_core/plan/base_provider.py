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

from abc import ABC, abstractmethod
from typing import Callable
from .actions import actions


class BaseProvider(ABC):
    def __init__(self, data: dict, state: dict, fn_save_state: Callable):
        self.data = data
        self.state = state
        self._save_state = fn_save_state

    def save(self, data: dict):
        self._save_state(data)

    def decide(self) -> str:
        return actions.create

    @abstractmethod
    def refresh(self) -> dict:
        pass

    @abstractmethod
    def create(self) -> dict:
        pass

    @abstractmethod
    def delete(self) -> dict:
        pass

    def eta_create(self):
        return "1m"

    def eta_delete(self):
        return "1m"
