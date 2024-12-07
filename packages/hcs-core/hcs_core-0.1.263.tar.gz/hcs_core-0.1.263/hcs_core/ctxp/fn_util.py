import inspect
import os
import threading


def debounce(graceful_seconds):
    """
    Delay a function call by graceful_seconds. If an additional call happens during this time,
    the delay will be reset.
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            def call_impl():
                wrapper._timer = None
                return function(*args, **kwargs)

            # Cancel existing timer, if any
            if wrapper._timer is not None:
                wrapper._timer.cancel()

            # Schedule debounced run
            wrapper._timer = threading.Timer(graceful_seconds, call_impl)
            wrapper._timer.start()

        wrapper._timer = None
        return wrapper

    return decorator


def once(fn):
    """
    Raise exception if the function called more than once.
    """

    def wrapper(*args, **kwargs):
        if wrapper._invoked:
            raise Exception("Duplicated invocation: %s, %s" % (_get_caller_file(), fn.__name__))
        wrapper._invoked = True
        return fn(*args, **kwargs)

    wrapper._invoked = False
    return wrapper


def _get_caller_file():
    # first get the full filename (including path and file extension)
    caller_frame = inspect.stack()[2]
    caller_filename_full = caller_frame.filename

    # now get rid of the directory (via basename)
    # then split filename and extension (via splitext)
    caller_filename_only = os.path.splitext(os.path.basename(caller_filename_full))[0]

    # return both filename versions as tuple
    return caller_filename_only
