import threading
from copy import deepcopy
from dataclasses import dataclass

from time import sleep, time

import schedule
import logging
from . import duration

log = logging.getLogger(__name__)


class TaskRef:
    def __init__(self, ref1, ref2=None):
        self.ref1 = ref1
        self.ref2 = ref2

    def cancel(self):
        if self.ref1:
            fn = list(self.ref1.job_func.args)[0]
            log.debug("Cancel job %s: %s" % (fn.__name__, self.ref1))
            schedule.cancel_job(self.ref1)
            self.ref1 = None
        if self.ref2:
            fn2 = list(self.ref2.job_func.args)[0]
            log.debug("Cancel job %s: %s" % (fn2.__name__, self.ref2))
            schedule.cancel_job(self.ref2)
            self.ref2 = None


@dataclass
class JobStatistics:
    last_start: int = 0
    last_end: int = 0
    history_total: int = 0
    last_cycle_total: int = 0

    def start(self):
        self.last_start = int(time())
        self.last_cycle_total += 1
        self.history_total += 1

    def end(self):
        self.last_end = int(time())

    def reset_cycle(self):
        self.last_cycle_total = 0


@dataclass
class Statistics:
    run_once_job: JobStatistics = JobStatistics()
    recurring_job: JobStatistics = JobStatistics()
    size: int = 0

    def reset_cycle(self):
        self.run_once_job.reset_cycle()
        self.recurring_job.reset_cycle()


_g_worker_thread: threading.Event = None
_g_flag_stop_daemon: threading.Thread = None
_g_flag_running: bool = True
_g_statistics = Statistics()


def _task_wrapper_repeat(fn_impl, kwargs):
    _g_statistics.recurring_job.start()
    fn_impl(**kwargs)
    _g_statistics.recurring_job.end()


def _task_wrapper_once(fn_impl, kwargs):
    _g_statistics.run_once_job.start()
    fn_impl(**kwargs)
    _g_statistics.run_once_job.end()
    return schedule.CancelJob


def submit(fn_task: callable, initial_delay: str = None, repeat_interval: str = None, **kwargs):
    if initial_delay:
        initial_delay_seconds = duration.to_seconds(initial_delay)
    else:
        initial_delay_seconds = 1

    if repeat_interval:
        # Have an initial run
        # TODO: this is not correct, but better than no lib-provided initial delay.
        job1 = schedule.every(initial_delay_seconds).seconds.do(_task_wrapper_once, fn_task, kwargs)
        log.debug(f"Register initial run {fn_task.__name__} {job1}")

        # TODO: identify a way to use the scheduler with initial delay, with cancellation in mind.
        seconds = duration.to_seconds(repeat_interval)
        job2 = schedule.every(seconds).seconds.do(_task_wrapper_repeat, fn_task, kwargs)
        log.debug(f"Register scheduled job {fn_task.__name__} at interval {repeat_interval} {job2}")
    else:
        job1 = schedule.every(initial_delay_seconds).seconds.do(_task_wrapper_once, fn_task, kwargs)
        log.debug(f"Register one-shot job {fn_task.__name__} {job1}")
        job2 = None
    return TaskRef(job1, job2)


def statistics(reset_cycle: bool = False):
    _g_statistics.size = len(schedule.get_jobs())
    ret = deepcopy(_g_statistics)
    if reset_cycle:
        _g_statistics.reset_cycle()
    return ret


def _daemon_worker():
    log.info("task scheduler daemon thread start")
    global _g_flag_stop_daemon
    while not _g_flag_stop_daemon.is_set():
        if _g_flag_running:
            schedule.run_pending()
        sleep(1)
    log.info("task scheduler daemon thread exit")


def start_daemon(paused: bool = False):
    global _g_flag_stop_daemon
    global _g_worker_thread
    if _g_worker_thread:
        raise Exception("Already started")

    if paused:
        global _g_flag_running
        _g_flag_running = False

    _g_flag_stop_daemon = threading.Event()
    _g_worker_thread = threading.Thread(target=_daemon_worker, daemon=True, name="task-schd")
    _g_worker_thread.start()


def pause():
    global _g_flag_running
    if _g_flag_running:
        _g_flag_running = False
        log.info("task scheduler daemon paused")


def resume():
    global _g_flag_running
    if not _g_flag_running:
        _g_flag_running = True
        log.info("task scheduler daemon resumed")


def stop_daemon():
    global _g_flag_stop_daemon
    global _g_worker_thread
    if _g_worker_thread:
        _g_flag_stop_daemon.set()
        _g_worker_thread.join()
        _g_worker_thread = None


if __name__ == "__main__":

    def job1(a, b):
        log.info(f"job1 {a} {b}")

    # logutil.setup()
    start_daemon()
    j1 = submit(fn_task=job1, initial_delay="PT3S", repeat_interval="PT5S", a="aa", b="bb")
    sleep(10)
    stop_daemon()
    log.info("exit")
