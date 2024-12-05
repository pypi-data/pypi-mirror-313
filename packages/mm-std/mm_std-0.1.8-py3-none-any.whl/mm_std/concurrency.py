import concurrent.futures
import functools
import time
from collections import defaultdict
from collections.abc import Callable
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from logging import Logger
from threading import Lock, Thread
from typing import ParamSpec, TypeVar

from .date import is_too_old, utc_now

type Func = Callable[..., object]
type Args = tuple[object, ...]
type Kwargs = dict[str, object]


class ConcurrentTasks:
    def __init__(self, max_workers: int = 5, timeout: int | None = None, thread_name_prefix: str = "concurrent_tasks") -> None:
        self.max_workers = max_workers
        self.timeout = timeout
        self.thread_name_prefix = thread_name_prefix
        self.tasks: list[ConcurrentTasks.Task] = []
        self.exceptions: dict[str, Exception] = {}
        self.error = False
        self.timeout_error = False
        self.result: dict[str, object] = {}

    @dataclass
    class Task:
        key: str
        func: Func
        args: Args
        kwargs: Kwargs

    def add_task(self, key: str, func: Func, args: Args = (), kwargs: Kwargs | None = None) -> None:
        if kwargs is None:
            kwargs = {}
        self.tasks.append(ConcurrentTasks.Task(key, func, args, kwargs))

    def execute(self) -> None:
        with ThreadPoolExecutor(self.max_workers, thread_name_prefix=self.thread_name_prefix) as executor:
            future_to_key = {executor.submit(task.func, *task.args, **task.kwargs): task.key for task in self.tasks}
            try:
                result_map = concurrent.futures.as_completed(future_to_key, timeout=self.timeout)
                for future in result_map:
                    key = future_to_key[future]
                    try:
                        self.result[key] = future.result()
                    except Exception as err:
                        self.error = True
                        self.exceptions[key] = err
            except concurrent.futures.TimeoutError:
                self.error = True
                self.timeout_error = True


T = TypeVar("T")
P = ParamSpec("P")


def synchronized_parameter(arg_index: int = 0, skip_if_locked: bool = False) -> Callable[..., Callable[P, T | None]]:
    locks: dict[object, Lock] = defaultdict(Lock)

    def outer(func: Callable[P, T]) -> Callable[P, T | None]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            if skip_if_locked and locks[args[arg_index]].locked():
                return None
            try:
                with locks[args[arg_index]]:
                    return func(*args, **kwargs)
            finally:
                locks.pop(args[arg_index], None)

        wrapper.locks = locks  # type: ignore[attr-defined]
        return wrapper

    return outer


def synchronized(fn: Callable[P, T]) -> Callable[P, T]:
    lock = Lock()

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        with lock:
            return fn(*args, **kwargs)

    return wrapper


class Scheduler:
    def __init__(self, log: Logger, loop_delay: float = 0.5, debug: bool = False):
        self.log = log
        self.debug = debug
        self.loop_delay = loop_delay
        self.stopped = False
        self.jobs: list[Scheduler.Job] = []
        self.run_immediately_jobs: list[Scheduler.Job] = []
        self._debug("init")

    @dataclass
    class Job:
        func: Func
        args: tuple[object, ...]
        interval: int
        is_running: bool = False
        last_at: datetime = field(default_factory=utc_now)

        def __str__(self) -> str:
            return str(self.func)

    def add_job(self, func: Func, interval: int, args: tuple[object, ...] = (), run_immediately: bool = False) -> None:
        job = Scheduler.Job(func, args, interval)
        self.jobs.append(job)
        if run_immediately:
            self.run_immediately_jobs.append(job)

    def _run_job(self, job: Job) -> None:
        self._debug(f"_run_job: {job}")
        if self.stopped:
            return
        try:
            job.func(*job.args)
            self._debug(f"_run_job: {job} done")
        except Exception as e:
            self.log.exception("scheduler error: %s", str(e))
            self._debug(f"_run_job: {job} error")
        finally:
            job.is_running = False

    def _start(self) -> None:
        self._debug(f"_start: jobs={len(self.jobs)}, run_immediately_jobs={len(self.run_immediately_jobs)}")
        for j in self.run_immediately_jobs:
            j.is_running = True
            j.last_at = utc_now()
            Thread(target=self._run_job, args=(j,)).start()
        while not self.stopped:
            for j in self.jobs:
                if not j.is_running and is_too_old(j.last_at, j.interval):
                    j.is_running = True
                    j.last_at = utc_now()
                    Thread(target=self._run_job, args=(j,)).start()
            time.sleep(self.loop_delay)

    def _debug(self, message: str) -> None:
        if self.debug:
            self.log.debug("Scheduler: %s", message)

    def start(self) -> None:
        Thread(target=self._start).start()

    def stop(self) -> None:
        self.stopped = True
