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

from typing import Callable
import time
from hcs_core.ctxp import profile, panic, CtxpException
from hcs_core.sglib import hcs_client
from hcs_core.util.query_util import with_query, PageRequest
from hcs_core.util import duration
from hcs_core.util import exit

_caches = {}


def hdc_service_client(service_name: str):
    instance = _caches.get(service_name)
    if not instance:
        url = profile.current().hcs.url
        if not url.endswith("/"):
            url += "/"
        url += service_name
        instance = hcs_client(url)
        _caches[service_name] = instance
    return instance


def _get_region_url(region_name: str):
    regions = profile.current().hcs.regions
    if not region_name:
        return regions[0].url
    for r in regions:
        if r.name.lower() == region_name.lower():
            return r.url
    names = []
    for r in regions:
        names.append(r.name)
    panic(f"Region not found: {region_name}. Available regions: {names}")


def regional_service_client(region_name: str, service_name: str):
    # 'https://dev1b-westus2-cp103a.azcp.horizon.vmware.com/vmhub'
    url = _get_region_url(region_name)
    if not url:
        panic("Missing profile property: hcs.regions")
    if not url.endswith("/"):
        url += "/"
    url += service_name
    return hcs_client(url)


def _with_org_id(url: str, org_id: str):
    if org_id:
        if url.find("?") < 0:
            url += "?"
        url += "org_id=" + org_id
    return url


class default_crud:
    def __init__(self, client, base_context: str, resource_type_name: str):
        self._client = client
        self._base_context = base_context
        self._resource_type_name = resource_type_name

    def get(self, id: str, org_id: str, **kwargs):
        if org_id:
            kwargs["org_id"] = org_id
        url = with_query(f"{self._base_context}/{id}", **kwargs)
        # print(url)
        return self._client.get(url)

    def list(self, org_id: str, fn_filter: Callable = None, **kwargs):
        if org_id:
            kwargs["org_id"] = org_id

        def _get_page(query_string):
            url = self._base_context + "?" + query_string
            # print(url)
            return self._client.get(url)

        return PageRequest(_get_page, fn_filter, **kwargs).get()

    def create(self, payload: dict, headers: dict = None, **kwargs):
        url = with_query(f"{self._base_context}", **kwargs)
        # print(url)
        # import json
        # print(json.dumps(payload, indent=4))
        if isinstance(payload, str):
            return self._client.post(url, text=payload, headers=headers)
        if isinstance(payload, dict):
            return self._client.post(url, json=payload, headers=headers)
        return self._client.post(url, json=payload, headers=headers)

    def upload(self, files, **kwargs):
        url = with_query(f"{self._base_context}", **kwargs)
        return self._client.post(url, files=files)

    def delete(self, id: str, org_id: str, **kwargs):
        if org_id:
            kwargs["org_id"] = org_id
        url = with_query(f"{self._base_context}/{id}", **kwargs)
        # print(url)
        return self._client.delete(url)

    def wait_for_deleted(self, id: str, org_id: str, timeout: str, fn_is_error: Callable = None):
        name = self._resource_type_name + "/" + id
        fn_get = lambda: self.get(id, org_id)
        return wait_for_res_deleted(name, fn_get, timeout=timeout, fn_is_error=fn_is_error)

    def update(self, id: str, org_id: str, data: dict, **kwargs):
        if org_id:
            kwargs["org_id"] = org_id
        url = with_query(f"{self._base_context}/{id}")
        return self._client.patch(url, data)


def _parse_timeout(timeout: str):
    if isinstance(timeout, int):
        return timeout
    if isinstance(timeout, str):
        return duration.to_seconds(timeout)

    raise CtxpException(f"Invalid timout. Type={type(timeout).__name__}, value={timeout}")


def wait_for_res_deleted(
    resource_name: str,
    fn_get: Callable,
    timeout: str,
    polling_interval_seconds: int = 10,
    fn_is_error: Callable = None,
):
    timeout_seconds = _parse_timeout(timeout)
    start = time.time()
    while True:
        t = fn_get()
        if t is None:
            return
        if fn_is_error:
            if fn_is_error(t):
                msg = f"Failed deleting resource '{resource_name}', resource in Error state."
                raise CtxpException(msg)

        now = time.time()
        remaining_seconds = timeout_seconds - (now - start)
        if remaining_seconds < 1:
            msg = f"Timeout waiting for resource '{resource_name}' to be deleted."
            raise TimeoutError(msg)
        sleep_seconds = remaining_seconds
        if sleep_seconds > polling_interval_seconds:
            sleep_seconds = polling_interval_seconds
        exit.sleep(sleep_seconds)


def wait_for_res_status(
    resource_name: str,
    fn_get: Callable,
    get_status: Callable,
    status_map: dict = None,
    is_ready: Callable = None,
    is_error: Callable = None,
    is_transition: Callable = None,
    timeout: str = "10m",
    polling_interval: str = "20s",
    not_found_as_success: bool = False,
):
    timeout_seconds = _parse_timeout(timeout)
    polling_interval_seconds = _parse_timeout(polling_interval)
    if polling_interval_seconds < 3:
        polling_interval_seconds = 3
    start = time.time()
    prefix = f"Error waiting for resource {resource_name}: "

    if isinstance(get_status, str):
        field_name = get_status
        get_status = lambda t: t[field_name]
    if status_map:
        if isinstance(status_map["ready"], str):
            status_map["ready"] = [status_map["ready"]]
        if isinstance(status_map["transition"], str):
            status_map["transition"] = [status_map["transition"]]
        if isinstance(status_map["error"], str):
            status_map["error"] = [status_map["error"]]
        if is_ready:
            raise CtxpException("Can not specify is_ready when status_map is provided.")
        if is_error:
            raise CtxpException("Can not specify is_error when status_map is provided.")
        if is_transition:
            raise CtxpException("Can not specify is_transition when status_map is provided.")
        is_ready = lambda s: s in status_map["ready"]
        is_error = lambda s: s in status_map["error"]
        is_transition = lambda s: s in status_map["transition"]
    else:
        if not is_ready:
            raise CtxpException("Either status_map or is_ready must be specified.")
        if not is_error:
            raise CtxpException("Either status_map or is_error must be specified.")
        if not is_transition:
            raise CtxpException("Either status_map or is_transition must be specified.")

    while True:
        t = fn_get()
        if t is None:
            if not_found_as_success:
                return
            raise CtxpException(prefix + "Not found.")
        status = get_status(t)
        # print(f"DDD - status {status}")
        if is_error(status):
            msg = prefix + f"Status error. Actual={status}"
            if status_map:
                msg += f", expected={status_map['ready']}"
            raise CtxpException(msg)
        if is_ready(status):
            return t
        if not is_transition(status):
            raise CtxpException(
                prefix + f"Unexpected status: {status}. If this is a transition, add it to status_map['transition']."
            )

        now = time.time()
        remaining_seconds = timeout_seconds - (now - start)
        if remaining_seconds < 1:
            raise TimeoutError(prefix + "Timeout.")
        sleep_seconds = remaining_seconds
        if sleep_seconds > polling_interval_seconds:
            sleep_seconds = polling_interval_seconds

        # print(f"DDD sleeping {sleep_seconds}")
        exit.sleep(sleep_seconds)
