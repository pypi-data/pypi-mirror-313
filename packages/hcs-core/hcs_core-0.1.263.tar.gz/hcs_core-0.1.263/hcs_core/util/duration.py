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

import re
from datetime import timedelta, datetime, timezone

PATTERN = re.compile("^(([0-9]+)D)?(([0-9]+)H)?(([0-9]+)M)?(([0-9]+)S)?$")


# Examples

# 11D12H13M14S
# 2H33S


def to_seconds(duration_string: str) -> int:
    if not duration_string:
        return 0
    duration_string = duration_string.upper()

    future = duration_string[0] == "-"
    if future:
        duration_string = duration_string[1:]

    matcher = PATTERN.fullmatch(duration_string)
    if matcher is None:
        raise Exception("Unsupported duration format: %s" % duration_string)

    d = matcher.group(2)
    h = matcher.group(4)
    m = matcher.group(6)
    s = matcher.group(8)

    total_seconds = 0
    if d:
        total_seconds += int(d) * 24 * 3600
    if h:
        total_seconds += int(h) * 3600
    if m:
        total_seconds += int(m) * 60
    if s:
        total_seconds += int(s)

    if future:
        total_seconds = -total_seconds
    return total_seconds


def to_duration(seconds: int, simple: bool = False) -> str:

    future = seconds < 0
    if future:
        seconds = -seconds

    ONE_MINUTE = 60
    ONE_HOUR = ONE_MINUTE * 60
    ONE_DAY = ONE_HOUR * 24
    days = int(seconds / ONE_DAY)
    seconds %= ONE_DAY
    hours = int(seconds / ONE_HOUR)
    seconds %= ONE_HOUR
    minutes = int(seconds / ONE_MINUTE)
    seconds %= ONE_MINUTE

    ret = ""
    v = 0
    while True:
        if days > 0:
            ret += f"{days}D"
            v += 1
        if hours > 0:
            ret += f"{hours}H"
            v += 1
            if simple and v >= 2:
                break
        if minutes > 0:
            ret += f"{minutes}M"
            v += 1
            if simple and v >= 2:
                break
        if seconds > 0:
            ret += f"{seconds}S"
        break
    if future:
        ret = "-" + ret
    return ret


def format_timedelta(d: timedelta, simple: bool = True):
    seconds = d.days * 86400 + d.seconds  # + d.microseconds / 1e6
    return to_duration(seconds, simple)


def to_utc(dt):
    if isinstance(dt, int) or isinstance(dt, float):
        dt = datetime.fromtimestamp(dt)
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    if dt.tzinfo is None:
        # Naive datetime: Assume it is in the local timezone and convert to UTC
        dt = dt.replace(tzinfo=timezone.utc)  # Assuming naive datetime is in UTC for this example
    return dt.astimezone(timezone.utc)


def stale(when) -> str:
    return format_timedelta(from_now(when), True)


def from_now(when) -> timedelta:
    when_utc = to_utc(when)
    now_utc = datetime.now().astimezone(timezone.utc)
    return now_utc - when_utc


def _test():
    data = {
        "14S": 14,
        "13M": 13 * 60,
        "12H": 12 * 3600,
        "11D": 11 * 24 * 3600,
        "13M14S": 13 * 60 + 14,
        "12H14S": 12 * 3600 + 14,
        "11D14S": 11 * 24 * 3600 + 14,
        "12H13M": 12 * 3600 + 13 * 60,
        "11D13M": 11 * 24 * 3600 + 13 * 60,
        "11D12H": 11 * 24 * 3600 + 12 * 3600,
        "11D12H13M": 11 * 24 * 3600 + 12 * 3600 + 13 * 60,
        "11D12H14S": 11 * 24 * 3600 + 12 * 3600 + 14,
        "11D13M14S": 11 * 24 * 3600 + 13 * 60 + 14,
        "12H13M14S": 12 * 3600 + 13 * 60 + 14,
        "11D12H13M14S": 11 * 24 * 3600 + 12 * 3600 + 13 * 60 + 14,
    }
    for k in data.keys():
        v = data[k]
        assert to_seconds(k) == v, f"to_seconds failed: k={k},v={v},got={to_seconds(k)}"
        assert to_duration(v) == k, f"to_duration failed: k={k},v={v},got={to_duration(v)}"
    print("PASS")


if __name__ == "__main__":
    _test()
