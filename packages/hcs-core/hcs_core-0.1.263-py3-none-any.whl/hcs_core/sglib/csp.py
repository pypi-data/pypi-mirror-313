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

import httpx
import json
import logging

log = logging.getLogger(__name__)

log_http_details = False


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
    except Exception:
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


class CspClient:
    def __init__(self, url: str, oauth_token: dict = None, org_id: str = None) -> None:
        self._base_url = url
        self._oauth_token = oauth_token
        self._org_id = org_id

        self._client = httpx.Client(
            base_url=url,
            timeout=20,
            event_hooks={
                "request": [_log_request],
                "response": [_log_response, _raise_on_4xx_5xx],
            },
        )

    def login_with_api_token(self, api_token: str) -> dict:
        # https://console-stg.cloud.vmware.com/csp/gateway/authn/api/swagger-ui.html#/Authentication/getAccessTokenByApiRefreshTokenUsingPOST

        # curl -X 'POST' \
        # 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize' \
        # -H 'accept: application/json' \
        # -H 'Content-Type: application/x-www-form-urlencoded' \
        # -d 'refresh_token=<the-refresh-token>'

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        # <no org id for this API>
        resp = self._client.post(
            "/csp/gateway/am/api/auth/api-tokens/authorize", headers=headers, data=f"api_token={api_token}"
        )
        self._oauth_token = resp.json()
        return self._oauth_token

    def login_with_client_id_and_secret(self, client_id: str, client_secret: str, org_id: str) -> dict:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        params = {
            "grant_type": "client_credentials",
        }
        if org_id:
            params["orgId"] = org_id
        resp = self._client.post(
            "/csp/gateway/am/api/auth/authorize",
            auth=(client_id, client_secret),
            headers=headers,
            params=params,
        )
        self._oauth_token = resp.json()
        return self._oauth_token

    # def get_oauth_token(self, force=False):
    #     if self._oauth_token and not force:
    #         return self._oauth_token

    #     if self._api_token:
    #         resp = self._login_by_api_token()
    #     elif self._refresh_token:
    #         if self._grant_type == 'refresh_token':
    #             resp = self._login_by_refresh_token_from_user_login()
    #         else:
    #             resp = self._login_by_refresh_token_from_api_token()
    #     elif self._refresh_token_from_api_token:
    #         resp = self._login_by_refresh_token_from_api_token()
    #     else:
    #         resp = self._login_by_client_id()
    #     try:
    #         oauth_token = resp.json()
    #     except:
    #         log.error(resp.content)
    #         raise
    #     self.use_oauth_token(oauth_token)
    #     return oauth_token

    # def use_oauth_token(self, oauth_token):
    #     access_token = oauth_token["access_token"]
    #     self._client.headers["authorization"] = "Bearer " + access_token

    #     token_ttl_seconds = int(oauth_token["expires_in"])
    #     self._token_expires_at = int(time.time() + token_ttl_seconds)

    #     decoded = jwt.decode(access_token, options={"verify_signature": False})
    #     log.debug(decoded)

    #     self._org_id = decoded["context_name"]
    #     self._decoded_jwt = decoded
    #     self._oauth_token = oauth_token

    # def _login_by_client_id(self):
    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     params = {
    #         "grant_type": "client_credentials",
    #     }
    #     if self._org_id:
    #         params['orgId'] = self._org_id
    #     return self._client.post(
    #         "/csp/gateway/am/api/auth/authorize",
    #         auth=(self._client_id, self._client_key),
    #         headers=headers,
    #         params=params,
    #     )

    # def _login_by_refresh_token_from_api_token(self):
    #     #https://console-stg.cloud.vmware.com/csp/gateway/authn/api/swagger-ui.html#/Authentication/getAccessTokenByApiRefreshTokenUsingPOST

    #     # curl -X 'POST' \
    #     # 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize' \
    #     # -H 'accept: application/json' \
    #     # -H 'Content-Type: application/x-www-form-urlencoded' \
    #     # -d 'refresh_token=<the-refresh-token>'

    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     # <no org id for this API>
    #     return self._client.post(
    #         "/csp/gateway/am/api/auth/api-tokens/authorize",
    #         headers=headers,
    #         data=f"api_token={self._refresh_token}"
    #     )
    # def _login_by_refresh_token_from_user_login(self):
    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     # <no org id for this API>
    #     return self._client.post(
    #         "/csp/gateway/am/api/auth/tokens",
    #         headers=headers,
    #         data=f"grant_type=refresh_token&refresh_token={self._refresh_token}"
    #     )
    # def _login_by_api_token(self):
    #     # curl -X 'POST' \\n  'https://console-stg.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize' \\n  -H 'accept: application/json' \\n  -H 'Content-Type: application/x-www-form-urlencoded' \\n  -d 'api_token=vA24tXLuWUlDmu-84ar5nl2zItvctRBKPOUyuBnxxPfOiRjEef1jJmDSW_IxRDMP'
    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     params = {
    #         "grant_type": "client_credentials",
    #     }
    #     if self._org_id:
    #         params['orgId'] = self._org_id
    #     return self._client.post(
    #         "/csp/gateway/am/api/auth/api-tokens/authorize",
    #         headers=headers,
    #         params=params,
    #         data=f"api_token={self._api_token}",
    #     )

    def get_org_details(self, org_id: str):
        resp = self._client.get(f"/csp/gateway/am/api/orgs/{org_id}")
        return resp.json()
