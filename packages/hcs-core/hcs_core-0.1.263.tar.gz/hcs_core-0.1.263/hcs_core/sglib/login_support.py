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

# nanw @ 2023
# PKCE with authlib: https://docs.authlib.org/en/latest/specs/rfc7636.html

import threading
import time
from typing import Callable
import webbrowser
import secrets
import logging
from hcs_core.util.scheduler import ThreadPoolScheduler
from authlib.integrations.httpx_client import OAuth2Client
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

log = logging.getLogger(__name__)

_server_address = ("127.0.0.1", 10762)
_callback_url = "/hcs-cli/oauth/callback"

_public_client_ids = {
    "production": "ldjmWbBAUcSB1w3HSbzoYcdKoloYFqT2dWK",
    "staging": "BbwHlgWt0vFwPUZMJTb5IKltynXjDmb46IO",
}

_auth_code_event = threading.Event()
_state = None

_auth_success_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Login successfully</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        code {
            font-family: Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            display: inline-block;
            background-color: rgb(242, 242, 242);
            padding: 12px 16px;
            margin: 8px 0px;
        }
    </style>
</head>
<body>
    <h3>You have successfully logged into VMware Horizon Cloud Service.</h3>
    <p>You can close this window, and return to the terminal.</p>
    <br/>
    <p><a href="https://github.com/euc-eng/hcs-cli">HCS CLI</a> is in beta phase. <a href="https://github.com/euc-eng/hcs-cli/blob/main/doc/hcs-cli-cheatsheet.md">Cheatsheet</a>:</p>
    <code>
    # To get the login details: <br/>
    hcs login -d <br/><br/>
    # To login programmatically: <br/>
    hcs login --api-token &lt;my-CSP-user-API-token&gt; <br/><br/>
    # Switch to a different profile:<br/>
    hcs profile use <br/><br/>
    </code>
</body>
</html>
"""


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        def _respond(code: int, reason: str, content_type: str = "text/plain"):
            self.send_response(code)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(reason.encode())
            self.wfile.flush()

        try:
            # Parse the query parameters from the callback URL
            parsed_url = urlparse(self.path)
            log.debug(parsed_url)
            if parsed_url.path == _callback_url or parsed_url.path == "/hcsadmin/index.html":
                query_components = parse_qs(parsed_url.query)
                codes = query_components.get("code", None)
                states = query_components.get("state", None)

                # Check if the 'code' parameter is present in the callback URL
                if not codes:
                    _respond(400, "Missing authorization code")
                    return
                if not states:
                    _respond(400, "Missing state in server response")
                    return
                state = states[0]
                if _state != state:
                    _respond(401, "Response state mismatch")
                    return

                code = codes[0]
                # Process the authorization code
                log.debug(f"auth code {code}")
                _auth_code_event.value = code

                # Send a response back to the client
                _respond(200, _auth_success_html, "text/html")
            else:
                _respond(404, "Not found")
        finally:
            # Terminate the server
            _auth_code_event.set()
            threading.Thread(target=lambda: self.server.shutdown()).start()

    def log_message(self, *args):
        log.debug(*args)


def run_server_async():
    def run_server():
        log.debug("oauth callback httpd - start")
        httpd = HTTPServer(_server_address, OAuthCallbackHandler)
        httpd.serve_forever()
        log.debug("oauth callback httpd - exit")

    threading.Thread(target=run_server, daemon=True).start()


def do_oauth2_pkce(csp_url: str, client_id: str, org_id: str):
    # OAuth2 server details
    # authorization_endpoint = csp_url + '/csp/gateway/am/api/auth/api-tokens/authorize'
    discovery_endpoint = csp_url + "/csp/gateway/discovery"
    token_endpoint = csp_url + "/csp/gateway/am/api/auth/token"

    redirect_uri = f"http://{_server_address[0]}:{_server_address[1]}{_callback_url}"

    # Create an OAuth2Session instance
    session = OAuth2Client(client_id, redirect_uri=redirect_uri)

    # Generate a code verifier and code challenge

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = create_s256_code_challenge(code_verifier)
    # code_challenge = CodeChallenge().from_code_verifier(code_verifier)

    # Create authorization URL
    # https://console-stg.cloud.vmware.com/csp/gateway/authn/api/swagger-ui.html#/Discovery/getDiscoveryUsingGET
    global _state
    authorization_url, _state = session.create_authorization_url(
        discovery_endpoint, orgId=org_id, code_challenge=code_challenge, code_challenge_method="S256"
    )

    log.debug(authorization_url)

    # Redirect the user to the authorization URL
    webbrowser.open(authorization_url, new=0, autoraise=True)

    try:
        _auth_code_event.wait()
    except:
        log.info("Aborted")
        return
    # Once the user is redirected back to your app with an authorization code, exchange it for an access token
    authorization_code = _auth_code_event.value
    log.debug("authorization_code: %s", authorization_code)
    if not authorization_code:
        log.debug("Login failed")
        return

    token = session.fetch_token(
        token_endpoint,
        auth=(client_id, ""),  # auth method required by CSP API for PKCE flow
        authorization_response=redirect_uri + "?code=" + authorization_code,
        code_verifier=code_verifier,
    )

    log.debug("token: %s", token)
    return token


def identify_client_id(csp_url: str) -> str:
    if csp_url.find("console.cloud") >= 0:
        return _public_client_ids["production"]
    if csp_url.find("https://connect.omnissa.com") >= 0:
        return _public_client_ids["production"]

    if csp_url.find("console-stg.cloud") >= 0:
        return _public_client_ids["staging"]
    raise Exception("Unknonw CSP url: " + csp_url)


def login_via_browser(csp_url: str, org_id: str):
    client_id = identify_client_id(csp_url)
    run_server_async()
    return do_oauth2_pkce(csp_url, client_id, org_id)


def create_oauth_client(
    oauth_token: dict, csp_url: str, fn_on_new_oauth_token: Callable = None, fn_custom_refresh: Callable = None
):
    client_id = identify_client_id(csp_url)

    if not fn_custom_refresh and client_id:
        client = OAuth2Client(
            client_id=client_id,
            client_secret="",  # Required by CSP auth
            token=oauth_token,
            token_endpoint=csp_url + "/csp/gateway/am/api/auth/token",
            token_endpoint_auth_method="client_secret_basic",
            update_token=fn_on_new_oauth_token,
        )
        log.debug("create_oauth_client - no custom refresher")
    else:
        # This is the case for production today, no csp-oauth-app yet,
        # and auth with API token case.
        client = OAuth2Client(
            # client_id=client_id,
            # client_secret="",  # Required by CSP auth
            token=oauth_token,
            # token_endpoint=csp_url + "/csp/gateway/am/api/auth/token",
            # token_endpoint_auth_method="client_secret_basic",
            # update_token=fn_on_new_oauth_token,
        )
        # start our own token refresh timer. Refresh using provided method
        if oauth_token and fn_on_new_oauth_token:
            _register_custom_refresher(client, oauth_token, fn_on_new_oauth_token, fn_custom_refresh)
        else:
            # not even initialized.
            pass
    return client


_scheduler: ThreadPoolScheduler = None


def _register_custom_refresher(
    client: OAuth2Client, oauth_token, fn_on_new_oauth_token: Callable, fn_custom_refresh: Callable
):
    log.debug("_register_custom_refresher")
    global _scheduler
    if not _scheduler:
        _scheduler = ThreadPoolScheduler()

    def get_refresh_delay(token):
        delay_seconds = token["expires_at"] - time.time() - 30
        log.debug(f"delay_seconds {delay_seconds}")

        # The expiry normally is 4 hrs but effectively it expires every 30 minutes.
        safe_delay_seconds = 25 * 60
        if delay_seconds > safe_delay_seconds:
            delay_seconds = safe_delay_seconds
        return delay_seconds

    def refresh_impl():
        if client.is_closed:
            return
        log.debug("_register_custom_refresher#refesh_impl")
        new_token = fn_custom_refresh()
        log.debug(f"_register_custom_refresher#refesh_impl: token={new_token}")
        client.token = new_token
        fn_on_new_oauth_token(new_token)
        delay = get_refresh_delay(new_token)
        _scheduler.submit(refresh_impl, delay)

    delay = get_refresh_delay(oauth_token)
    _scheduler.submit(refresh_impl, delay)


def refresh_oauth_token(old_oauth_token: dict, csp_url: str):
    with create_oauth_client(old_oauth_token, csp_url) as client:
        token_endpoint = csp_url + "/csp/gateway/am/api/auth/token"
        log.debug("Refresh auth token...")
        new_token = client.refresh_token(token_endpoint)
        log.debug(f"New auth token: {new_token}")
        if not new_token:
            raise Exception("CSP auth refresh failed.")
        if "cspErrorCode" in new_token:
            raise Exception(f"CSP auth failed: {new_token.get('message')}")
    return new_token


# def _test():
#     import jwt
#     import json
#     csp_url = 'https://console-stg.cloud.vmware.com'
#     org_id = '06e09ab5-dc8d-413c-bd57-2c1e929a412c' #stg horizonv2-syntest
#     token = interactive_login_via_browser(csp_url, org_id)
#     decoded = jwt.decode(token['access_token'], options={"verify_signature": False})
#     print(json.dumps(decoded, indent=4))

# if __name__ == '__main__':
#     _test()
