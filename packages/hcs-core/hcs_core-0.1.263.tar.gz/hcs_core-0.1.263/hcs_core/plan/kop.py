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

import time
import traceback
import logging
from hcs_core.ctxp.util import error_details

log = logging.getLogger(__name__)


class KopException(Exception):
    pass


class KopMode:
    create = "create"
    delete = "delete"
    update = "update"


class KopAction:
    start = "start"
    success = "success"
    error = "error"
    skip = "skip"


class _DummyJobView:
    @staticmethod
    def add(id, name):
        pass

    @staticmethod
    def update(id, text: str):
        pass

    @staticmethod
    def start(id, eta: str):
        pass

    @staticmethod
    def success(id):
        pass

    @staticmethod
    def skip(id, reason):
        pass

    @staticmethod
    def error(id, err):
        pass


_job_view = _DummyJobView


def attach_job_view(view):
    global _job_view
    _job_view = view


class KOP:
    MODE = KopMode

    def __init__(self, state: dict, kind: str, name: str, mode: str = KopMode.create) -> "KOP":
        self._state = state
        self._kind = kind
        self._name = name
        self._id = None
        self._mode = mode
        self._started = False
        self._closed = False
        job_id = kind + "/" + name
        _job_view.add(job_id, job_id)

    def _job_id(self):
        return self._kind + "/" + self._name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            self.error(exc_value)
        else:
            # default closing upon leaving scope
            if not self._closed:
                self._success()

    def id(self, res_id: str):
        self._id = res_id
        _job_view.update(self._job_id(), res_id)

    def start(self, mode: str = None, eta: str = None):
        if self._started:
            raise KopException("Kop already started. This is a framework logging issue.")
        if self._closed:
            raise KopException("Kop already closed. This is a framework logging issue.")
        if mode:
            self._mode = mode
        self._started = True
        self._add_log(KopAction.start)
        _job_view.start(self._job_id(), eta)

    def _success(self):
        if not self._started:
            raise KopException(
                "Kop not started. This is a framework logging issue. Call kop.start() before starting the resource operation."
            )
        if self._closed:
            raise KopException("Kop already closed. This is a framework logging issue.")
        self._add_log(KopAction.success)
        self._closed = True
        _job_view.success(self._job_id())

    def error(self, err):
        if isinstance(err, Exception):
            if _need_stack_trace(err):
                traceback.print_exception(type(err), err, err.__traceback__)
            details = error_details(err)
        else:
            details = str(err)
        self._add_log(KopAction.error, details)
        self._closed = True
        _job_view.error(self._job_id(), details)

    def skip(self, reason):
        self._add_log(KopAction.skip, reason)
        self._closed = True
        _job_view.skip(self._job_id(), reason)

    def _add_log(self, action: str, details: str = None):
        labels = {
            KopMode.create: {
                KopAction.start: "[creating]",
                KopAction.success: "[created ]",
                KopAction.skip: "[skipped ]",
                KopAction.error: "[error   ]",
            },
            KopMode.delete: {
                KopAction.start: "[deleting]",
                KopAction.success: "[deleted ]",
                KopAction.skip: "[skipped ]",
                KopAction.error: "[error   ]",
            },
            KopMode.update: {
                KopAction.start: "[updating]",
                KopAction.success: "[updated ]",
                KopAction.skip: "[skipped ]",
                KopAction.error: "[error   ]",
            },
        }
        label_map = labels.get(self._mode)
        if not label_map:
            raise KopException(f"Invalid mode: {self._mode}")
        label = label_map[action]
        msg = f"{label} {self._kind}:{self._name}"
        if self._id:
            msg += " " + self._id

        if _job_view == _DummyJobView:
            log.info(msg)
        entry = {"name": self._name, "time": int(time.time()), "action": action, "id": self._id}
        if details:
            entry["details"] = details
        self._state["log"][self._mode].append(entry)
        if action == "error":
            if self._id:
                log.warning('Plugin "%s:%s" failed: %s. Id=%s', self._kind, self._name, details, self._id)
            else:
                log.warning('Plugin "%s:%s" failed: %s.', self._kind, self._name, details)


def _need_stack_trace(e):
    if isinstance(e, KeyError):
        return True
    if isinstance(e, TypeError):
        return True
