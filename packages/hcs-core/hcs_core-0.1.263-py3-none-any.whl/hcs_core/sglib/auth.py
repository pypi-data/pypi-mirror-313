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
import jwt
import json
import hashlib
import logging
from hcs_core.ctxp import profile, panic, jsondot
from .csp import CspClient
from .login_support import create_oauth_client, refresh_oauth_token

log = logging.getLogger(__name__)


def _get_profile_auth_hash():
    csp = profile.current().csp
    text = json.dumps(csp, default=vars)
    return profile.name() + "#" + hashlib.md5(text.encode("ascii"), usedforsecurity=False).hexdigest()


def _is_auth_valid(auth_data):
    if not auth_data:
        return
    if not auth_data.token:
        return
    if auth_data.hash != _get_profile_auth_hash():
        return
    if time.time() + 0 * 5 * 60 > auth_data.token.expires_at:
        return
    return True


def login(force_refresh: bool = False):
    """Ensure login state, using credentials from the current profile. Return oauth token."""

    # _validate_profile_readiness()

    auth_data = profile.auth.get()
    if force_refresh or not _is_auth_valid(auth_data):
        oauth_token = _get_new_oauth_token(auth_data.token)
        if oauth_token:
            use_oauth_token(oauth_token)
    else:
        oauth_token = auth_data.token
    return oauth_token


def _get_new_oauth_token(old_oauth_token=None):
    csp_config = profile.current().csp

    csp_client = CspClient(url=csp_config.url)

    if csp_config.apiToken:
        oauth_token = csp_client.login_with_api_token(csp_config.apiToken)
    elif csp_config.clientId:
        oauth_token = csp_client.login_with_client_id_and_secret(
            csp_config.clientId, csp_config.clientSecret, csp_config.orgId
        )
    else:
        # This should be a config from interactive login.
        # Use existing oauth_token to refresh.
        if old_oauth_token:
            try:
                oauth_token = refresh_oauth_token(old_oauth_token, csp_config.url)
            except Exception as e:
                oauth_token = None
                log.warning(e)
        else:
            oauth_token = None
    return oauth_token


# _oauth_client_instance = None
# import threading
# _lock = threading.RLock()


def oauth_client():
    return _oauth_client_impl()
    # global _oauth_client_instance, _lock
    # if not _oauth_client_instance:
    #     with _lock:
    #         if not _oauth_client_instance:
    #             _oauth_client_instance = _oauth_client_impl()
    # return _oauth_client_instance


def _oauth_client_impl():
    oauth_token = login(False)

    if not oauth_token:
        panic(
            "Login failed. If this is configured API key or client credential, refresh the credential from CSP and update profile config. If this is browser based interactive login, login again."
        )

    csp_url = profile.current().csp.url

    def fn_on_new_oauth_token(token, refresh_token=None, access_token=None):
        use_oauth_token(token)

    if profile.current().csp.apiToken:
        # for api-token login, due to no client ID, it will fail with 400 during refresh.
        # So instead of doing standard OAuth refresh, just use the API token to acquire a new one.
        return create_oauth_client(oauth_token, csp_url, fn_on_new_oauth_token, _get_new_oauth_token)
    else:
        # return create_oauth_client(oauth_token, csp_url, fn_on_new_oauth_token)

        # With the updated CSP (Omnissa), the default refresh mechanism from oauth client does not work, it might be the service
        # side issue.
        # To make it compatible, use the custom refresh mechanism (get new token).
        return create_oauth_client(oauth_token, csp_url, fn_on_new_oauth_token, _get_new_oauth_token)


def details(get_org_details: bool = False) -> jsondot.dotdict:
    """Get the auth details, for the current profile"""
    oauth_token = login()
    if not oauth_token:
        return
    return details_from_token(oauth_token, get_org_details)


def details_from_token(oauth_token, get_org_details: bool = False):
    decoded = jwt.decode(oauth_token["access_token"], options={"verify_signature": False})
    org_id = decoded["context_name"]
    ret = {"token": oauth_token, "jwt": decoded, "org": {"id": org_id}}

    if get_org_details:
        csp_client = CspClient(url=profile.current().csp.url, oauth_token=oauth_token)
        try:
            org_details = csp_client.get_org_details(org_id)
        except Exception as e:
            org_details = {"error": f"Fail retrieving org details: {e}"}
        ret["org"].update(org_details)
    return jsondot.dotify(ret)


def get_org_id_from_token(oauth_token: str) -> str:
    decoded = jwt.decode(oauth_token["access_token"], options={"verify_signature": False})
    return decoded["context_name"]


def use_oauth_token(oauth_token):
    if "expires_at" not in oauth_token:
        oauth_token["expires_at"] = int(time.time()) + oauth_token["expires_in"]
    profile.auth.set({"token": oauth_token, "hash": _get_profile_auth_hash()})
