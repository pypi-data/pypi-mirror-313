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
import logging
from http.client import HTTPResponse
from typing import Callable

import httpx
from authlib.integrations.httpx_client import OAuth2Client
from hcs_core.ctxp import jsondot

log = logging.getLogger(__name__)


def parse(resp: httpx.Response):
    if not resp.content:
        return None
    content_type = resp.headers["Content-Type"]
    if content_type.startswith("text"):
        return resp.text
    if len(resp.content) > 3:
        try:
            data = resp.json()
            if isinstance(data, list):
                return [jsondot.dotify(obj) for obj in data]
            elif isinstance(data, dict):
                return jsondot.dotify(data)
        except:
            log.info("--- Fail parsing json. Dump content ---")
            log.info(resp.content)
            raise
    else:
        return None


def _raise_on_4xx_5xx(response: httpx.Response):
    if not response.is_success:
        response.read()
        if len(response.text) > 0:
            text = _try_formatting_json(response.text)
            log.debug(text)

    response.raise_for_status()


def _try_formatting_json(text: str):
    try:
        return json.dumps(json.loads(text), indent=4)
    except:
        return text


def _log_request(request):
    if not log.isEnabledFor(logging.DEBUG):
        return
    log.debug("\n")
    log.debug(f"--> {request.method} {request.url}")
    log.debug(f"--> {request.headers}")

    if len(request.content) > 0:
        text = _try_formatting_json(request.content)
        log.debug(text)


def _log_response(response: httpx.Response):
    if not log.isEnabledFor(logging.DEBUG):
        return
    request = response.request
    log.debug(f"<-- {request.method} {request.url} - {response.status_code}")
    log.debug(f"<-- {request.headers}")
    response.read()
    if len(response.text) > 0:
        text = _try_formatting_json(response.text)
        log.debug(text)
    log.debug("\n")


def _parse_resp(resp: httpx.Response):
    if not resp.content:
        return
    content_type = resp.headers["Content-Type"]
    if content_type.startswith("text"):
        return resp.text
    if content_type == "application/json" and resp.content:
        try:
            data = resp.json()
            return jsondot.dotify(data)
        except:
            log.info("--- Fail parsing json. Dump content ---")
            log.info(resp.content)
            raise
    return resp.text


def _is_404(e: httpx.HTTPStatusError) -> bool:
    return e.response.status_code == 404


def on404ReturnNone(func):
    try:
        resp = func()
        return _parse_resp(resp)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise


class EzClient:
    def __init__(self, base_url: str, oauth_client: OAuth2Client = None, lazy_oauth_client: Callable = None) -> None:
        # self._client = httpx.Client(base_url=base_url, timeout=30, event_hooks=event_hooks)
        self._base_url = base_url
        self._client_impl = oauth_client
        self._lazy_oauth_client = lazy_oauth_client

    def _client(self):
        if not self._client_impl:
            client = self._lazy_oauth_client()
            client.base_url = self._base_url
            client.timeout = 30
            request_hooks = client.event_hooks["request"]
            response_hooks = client.event_hooks["response"]
            if _log_request not in request_hooks:
                request_hooks.append(_log_request)
            if _log_response not in response_hooks:
                response_hooks.append(_log_response)
            if _raise_on_4xx_5xx not in response_hooks:
                response_hooks.append(_raise_on_4xx_5xx)
            self._client_impl = client
        return self._client_impl

    def post(self, url: str, json: dict = None, text: str = None, files=None, headers: dict = None):
        # import json as jsonlib
        # print(url, jsonlib.dumps(json, indent=4))
        resp = self._client().post(url, json=json, content=text, files=files, headers=headers)
        return _parse_resp(resp)

    def get(self, url: str, raise_on_404: bool = False):
        try:
            # print("->", url)
            resp = self._client().get(url)
            return _parse_resp(resp)
        except httpx.HTTPStatusError as e:
            if _is_404(e):
                if raise_on_404:
                    raise e
                else:
                    pass
            else:
                raise

    def patch(self, url: str, json: dict):
        resp = self._client().patch(url, json=json)
        return _parse_resp(resp)

    def delete(self, url: str, raise_on_404: bool = False):
        try:
            resp = self._client().delete(url)
            return _parse_resp(resp)
        except httpx.HTTPStatusError as e:
            if _is_404(e):
                if raise_on_404:
                    raise
                else:
                    pass
            else:
                raise

    def put(self, url: str, json: dict):
        resp = self._client().put(url, json=json)
        return _parse_resp(resp)

    def close(self):
        self._client().close()

    def dump_response(self, response: HTTPResponse):
        log.info("response text: " + response.text())
