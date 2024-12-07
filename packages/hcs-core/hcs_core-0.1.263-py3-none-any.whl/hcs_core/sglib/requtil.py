import httpx
import logging

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


def on404ReturnNone(func):
    try:
        resp = func()
        return parse(resp)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise
