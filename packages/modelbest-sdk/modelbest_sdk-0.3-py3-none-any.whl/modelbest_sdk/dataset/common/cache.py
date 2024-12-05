
import itertools
import queue
import threading
from typing import List

from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk


class CacheNotFilled(Exception):
    pass


class CacheFull(Exception):
    pass


class AllCached(Exception):
    pass


class PrefetchCache(object):
    """
    Primitive for concurrently performing tasks and block when cache is full.
    Manage shared states to avoid racing, ensuring at most self.size tasks are cached
    Typical use case
    1. submit tasks to be cached
    cache.submit(tasks)
    2. within producer threads: get task, do some process, and put the results back
    while True:
        try:
            task = cache.pull_task()
            result = do_something(task)  # heavy work
            cache.put_result(result)
        except CacheFull:
            time.sleep(0.2)
        except AllCached:
            break
    3. get results within the consumer thread
    # CacheNotFilled: tasks not exhausted but no task are currently pulled, supressed by block=True
    # StopIteration: tasks are exhausted and all results are consumed
    result = cache.get(block=False)
    do_something(result)
    """

    def __init__(self, size):
        self.size = size
        self._lock = threading.RLock()
        self._count = self._finished = self._queue = self._tasks = None

    def submit(self, tasks):
        with self._lock:
            self._queue = queue.Queue()  # cache for the task results
            self._tasks = tasks  # iterator of tasks to be performed
            self._count = 0  # counting the expected results, manually maintaining count to avoid racing
            self._finished = False

    def pull_task(self) -> Chunk:
        with self._lock:
            if self._count + 1 > self.size:
                raise CacheFull
            try:
                task = next(self._tasks)
                self._count += 1
                return task
            except StopIteration:
                self._finished = True
                raise AllCached
    
    def push_task(self, task: Chunk):
        with self._lock:
            self._tasks = itertools.chain([task], self._tasks)

    @property
    def finished(self):
        with self._lock:
            return self._finished

    @property
    def count(self):
        with self._lock:
            return self._count

    def put_result(self, result):
        self._queue.put(result)

    def get(self, block=False):
        with self._lock:
            if self._count <= 0:
                if self._finished:
                    raise StopIteration
                elif not block:
                    raise CacheNotFilled
            self._count -= 1
        data = self._queue.get(block=True)
        return data

