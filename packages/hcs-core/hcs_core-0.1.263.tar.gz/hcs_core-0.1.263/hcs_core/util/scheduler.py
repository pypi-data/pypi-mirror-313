import threading
import traceback
import time
import heapq
import atexit
from concurrent.futures import ThreadPoolExecutor

_g_lock = threading.RLock()
_schedulers = []


def _close_schedulers():
    with _g_lock:
        while _schedulers:
            try:
                s = _schedulers.pop()
                s.close()
            except:
                traceback.print_exc()


atexit.register(_close_schedulers)


class ThreadPoolScheduler:
    def __init__(self, max_threads=5):
        self._task_queue = []
        self._lock = threading.Lock()
        self._scheduler_event = threading.Event()
        self._counter = 0
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, name="thread-pool-sch", daemon=True)
        self._executor = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="thread-pool-exec")
        with _g_lock:
            _schedulers.append(self)
        self._scheduler_thread.start()

    def _scheduler_loop(self):
        while self._running:
            if self._task_queue:
                execute_at, _, task = self._task_queue[0]
                current_time = time.time()

                if execute_at > current_time:
                    # Head is still in future. Sleep
                    timeout = execute_at - current_time
                    self._scheduler_event.wait(timeout)
                    self._scheduler_event.clear()
                    continue

                # Ready to execute the head
                heapq.heappop(self._task_queue)
                self._executor.submit(task)
            else:
                # queue is empty.
                self._scheduler_event.wait()
                self._scheduler_event.clear()

    def submit(self, target_function, delay_seconds):
        with self._lock:
            execute_at = time.time() + delay_seconds
            # tuple subitems are compared after comparing the first one.
            # So make sure there's a differentiator with counter.
            self._counter += 1
            heapq.heappush(self._task_queue, (execute_at, self._counter, target_function))
            self._scheduler_event.set()

    def close(self):
        self._running = False
        self._scheduler_event.set()
        self._executor.shutdown(wait=False, cancel_futures=True)
        with _g_lock:
            try:
                _schedulers.remove(self)
            except:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


# Example usage
# def print_message(message):
#     print(message)
#     time.sleep(5)
#     print("done")

# scheduler = ThreadPoolScheduler(max_threads=5)
# _n = 0

# def rr(txt):
#     global _n
#     print("rr", txt, _n)
#     _n += 1
#     scheduler.submit(lambda: rr("a1"), 0)
# scheduler.submit(lambda: rr("a1"), 0)
# time.sleep(5)  # Give some time for tasks to execute
