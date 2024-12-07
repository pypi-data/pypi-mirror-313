from weakref import WeakSet
import logging

log = logging.getLogger(__name__)


class Dispatcher:
    _registry: dict = {}

    def register(self, key: str, fn: callable):
        listeners = self._registry.get(key)
        if not listeners:
            listeners = WeakSet()
            self._registry[key] = listeners
        listeners.add(fn)
        return self

    def register_map(self, map: dict):
        for k, v in map.items():
            self.register(k, v)
        return self

    def unregister(self, key: str, fn: callable):
        listeners = self._registry.get(key)
        if listeners:
            listeners.remove(fn)
        return self

    def unregister_map(self, map: dict):
        for k, v in map.items():
            self.unregister(k, v)
        return self

    def emit(self, key: str, *args, **kwargs):
        listeners = self._registry.get(key)
        if listeners:
            copy = listeners.copy()
            for fn in copy:
                try:
                    fn(*args, **kwargs)
                except Exception as e:
                    log.error(f"Error handling event: {key}", e)
                    log.exception(e)
        return self

    def scope(self, events):
        return StrictDispatcher(self, events)


class StrictDispatcher:
    def __init__(self, impl: Dispatcher, events: set):
        self._impl = impl
        self._events = events

    def register(self, key: str, fn: callable):
        self._validate(key)
        self._impl.register(key, fn)
        return self

    def register_map(self, map: dict):
        for k, v in map.items():
            self.register(k, v)
        return self

    def unregister(self, key: str, fn: callable):
        self._validate(key)
        self._impl.unregister(key, fn)
        return self

    def unregister_map(self, map: dict):
        for k, v in map.items():
            self.unregister(k, v)
        return self

    def emit(self, key: str, *args, **kwargs):
        self._validate(key)
        self._impl.emit(key, *args, **kwargs)
        return self

    def _validate(self, key: str):
        if key not in self._events:
            raise Exception("Event is not in dispatcher scope: %s. The scoped events are: %s " % (key, self._events))
