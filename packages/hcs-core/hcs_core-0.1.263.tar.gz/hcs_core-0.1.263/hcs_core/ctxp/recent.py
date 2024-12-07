from . import context
from .util import CtxpException

_recent = dict(context.get(".recent", default={}))


def set(k: str, v):
    _recent[k] = v
    context.set(".recent", _recent)
    return v


def unset(k: str):
    ret = None
    if k in _recent:
        ret = _recent.pop(k)
    context.set(".recent", _recent)
    return ret


def unset_all():
    _recent.clear()
    context.set(".recent", _recent)


def get(k: str):
    return _recent.get(k)


def all():
    return _recent


def require(provided, k: str):
    if not k:
        raise Exception("Missing 'key' in recent.require(current, key).")

    last = _recent.get(k)
    if provided:
        if last != provided:
            _recent[k] = provided
            context.set(".recent", _recent)
        return provided
    if not last:
        raise CtxpException("Missing parameter: " + k)
    return last


class Bag:
    def __init__(self, name: str):
        self._name = name
        self._changed = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self._changed:
            context.set(".recent", _recent)

    def get(self):
        return _recent.get(self._name)

    def set(self, v):
        if v != _recent.get(self._name):
            _recent[self._name] = v
            self._changed = True
        return v

    def unset(self):
        if self._name in _recent:
            self._changed = True
            return _recent.pop(self._name)


def of(k: str):
    return Bag(k)


class helper:
    @staticmethod
    def default_list(array: list, name: str):
        with of(name) as r:
            if len(array) == 1:
                r.set(array[0]["id"])
            else:
                r.unset()
