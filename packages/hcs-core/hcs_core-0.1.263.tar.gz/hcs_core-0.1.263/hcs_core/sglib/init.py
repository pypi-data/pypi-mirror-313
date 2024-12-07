import atexit
import logging

log = logging.getLogger(__name__)
_sg_client = None


# Work around issue:
# http11.py, line 211, in close: AttributeError: 'NoneType' object has no attribute 'CLOSED'
def _on_exit():
    if _sg_client:
        _sg_client.close()

    log.info("Exit")


atexit.register(_on_exit)
