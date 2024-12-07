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

from typing import Optional
import threading
from time import sleep, monotonic
import sys
import os
from rich.live import Live
from rich.progress import Progress, Task, ProgressBar, SpinnerColumn, TextColumn, TimeRemainingColumn, ProgressColumn
from rich.table import Column
from rich.text import Text
from rich.console import RenderableType
import hcs_core.util.duration as duration


def _shorten_package_name(package_name, max_length):
    if len(package_name) <= max_length:
        return package_name

    parts = package_name.split(".")
    shortened_parts = []

    for i, part in enumerate(parts):
        shortened_parts.append(part[0])

        if i == len(parts) - 1:
            # Last package name
            remaining_length = max_length - len(".".join(shortened_parts))
            if len(part) > remaining_length:
                shortened_parts[-1] = "..." + part[-remaining_length + 3 :]
            else:
                shortened_parts[-1] = part
        else:
            new_package_name = ".".join(shortened_parts)

            if len(new_package_name) + len(parts) - i - 1 > max_length:
                break

    return ".".join(shortened_parts)


class _MyPlainBarColumn(ProgressColumn):
    def __init__(self) -> None:
        super().__init__(table_column=Column(min_width=10))

    def render(self, task: Task) -> ProgressBar:
        """Gets a progress bar widget for a task."""
        return ProgressBar(
            total=max(0, task.total) if task.total is not None else None,
            completed=max(0, task.completed),
            width=10,
            pulse=False,
            animation_time=task.get_time(),
            style="bar.back",
            complete_style="bar.complete",
            finished_style="bar.finished",
            pulse_style="bar.pulse",
        )


class _MyTimeRemainingColumn(ProgressColumn):
    """Renders estimated time remaining."""

    # Only refresh twice a second to prevent jitter
    max_refresh = 0.5

    def __init__(
        self,
        compact: bool = False,
        elapsed_when_finished: bool = False,
        table_column: Optional[Column] = None,
    ):
        self.compact = compact
        self.elapsed_when_finished = elapsed_when_finished
        super().__init__(table_column=table_column)

    def render(self, task: "Task") -> Text:
        """Show time remaining."""
        if self.elapsed_when_finished and task.finished:
            task_time = task.finished_time
            style = "progress.download"
        else:
            task_time = task.time_remaining
            style = "progress.remaining"

        if task.total is None:
            return Text("", style=style)

        if task_time is None:
            return Text("--:--" if self.compact else "-:--:--", style=style)

        # Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py
        minutes, seconds = divmod(int(task_time), 60)
        hours, minutes = divmod(minutes, 60)

        if self.compact and not hours:
            formatted = f"{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{hours:d}:{minutes:02d}:{seconds:02d}"

        return Text(formatted, style=style)


class _MySpinnerColumn(SpinnerColumn):
    def render(self, task: "Task") -> RenderableType:
        if task.finished:
            text = self.finished_text
        elif task.stop_time:
            text = " "  # stopped. E.g. error.
        else:
            text = self.spinner.render(task.get_time())
        return text


def _timeout_to_seconds(timeout: str, default: int = 60) -> int:
    t = duration.to_seconds(timeout)
    if t == 0 and default:
        t = default
    return t


class JobView:
    def __init__(self, auto_close: bool = True):
        self._map = {}
        self._todo = set()
        self._auto_close = auto_close
        self._closed = False
        self._view_started = threading.Event()
        self._view_exited = threading.Event()

        w, h = os.get_terminal_size()
        msg_width = w - 40 - 1 - 1 - 1 - 10 - 1 - 5 - 1 - 1
        self._job_ctl = Progress(
            TextColumn("{task.description}", table_column=Column(max_width=40, min_width=10)),
            # SpinnerColumn(table_column=Column(min_width=1)),
            _MySpinnerColumn(table_column=Column(min_width=1)),
            # BarColumn(pulse_style='white'),
            _MyPlainBarColumn(),
            # TextColumn("[white][progress.percentage][white]{task.percentage:>3.0f}%"),
            # TaskProgressColumn(show_speed=True),
            TimeRemainingColumn(
                compact=True, elapsed_when_finished=True, table_column=Column(style="white", min_width=5)
            ),
            TextColumn("{task.fields[details]}", table_column=Column(max_width=msg_width, no_wrap=True)),
            get_time=monotonic,
        )

    def add(self, id: str, name: str):
        name = _shorten_package_name(name, 30)
        self._map[id] = self._job_ctl.add_task(name, start=False, details="")
        self._todo.add(id)

    def remove(self, id: str):
        task_id = self._map[id]
        self._job_ctl.remove_task(task_id)
        del self._map[id]
        self._todo.discard(id)

    def refresh(self):
        for task_id in self._map.values():
            task = self._job_ctl._tasks[task_id]

            if task.started and not task.finished and not task.stop_time:
                completed = monotonic() - task.start_time
                if completed >= task.total:
                    completed = task.total - 1
                self._job_ctl.update(task_id, completed=completed)

    def update(self, id: str, details: str):
        task_id = self._map[id]
        if not details:
            details = ""
        self._job_ctl.update(task_id, details=details)

    def start(self, id: str, timeout: str) -> None:
        task_id = self._map[id]
        if timeout:
            total = _timeout_to_seconds(timeout)
            self._job_ctl.update(task_id, total=total)
        self._job_ctl.start_task(task_id)

    def _ensure_started(self, id: str) -> None:
        self.start(id, None)

    def success(self, id: str) -> None:
        self._ensure_started(id)
        task_id = self._map[id]
        self._job_ctl.update(task_id, completed=sys.float_info.max)
        self._todo.discard(id)

    def skip(self, id: str, reason: str) -> None:
        self._ensure_started(id)
        task_id = self._map[id]
        details = "skipped"
        if reason:
            details += f": {reason}"
        self._job_ctl.update(task_id, completed=sys.float_info.max, details=details)
        self._todo.discard(id)

    def error(self, id: str, details: str):
        self._ensure_started(id)
        task_id = self._map[id]
        if not details:
            details = ""
        self._job_ctl.update(task_id, details=details)
        self._job_ctl.stop_task(task_id)
        # self._job_ctl._tasks[task_id].finished = True
        self._todo.discard(id)
        self._job_ctl.stop

    def close(self) -> None:
        self._todo.clear()
        self._closed = True
        self._view_exited.wait()

    def show(self) -> None:
        try:
            with Live(self._job_ctl, refresh_per_second=10):
                self._view_started.set()
                while True:
                    self.refresh()
                    if self._closed:
                        break
                    if self._auto_close and not self._todo:
                        break
                    sleep(0.2)
        finally:
            self._view_exited.set()

    @staticmethod
    def create_async(auto_close: bool = False) -> "JobView":
        inst = JobView(auto_close)
        t = threading.Thread(target=inst.show, daemon=False)
        t.start()
        inst._view_started.wait()
        return inst
