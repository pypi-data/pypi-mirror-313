import logging
import time
from datetime import datetime, timedelta
from threading import Semaphore, Thread
from typing import Optional, Callable, Dict, Any, List, TypedDict

OwnerLock = TypedDict("OwnerLock", {"acquiring_lock": List[int], "sema": Semaphore, "__created": datetime})

logger = logging.getLogger(__name__)


class ThreadController:
    def __init__(self, thread_size: int):
        self.sema = Semaphore(thread_size)
        self.thread_size = thread_size

        # a lock/queue for task that are acquiring semaphore
        self.acquiring_lock: List[int] = []
        self.owners: Dict[str | int, OwnerLock] = {}

    def create_thread(self, target: Callable, *, args: Optional[tuple] = None, kwargs: Optional[Dict[str, Any]] = None,
                      thread_owner: Optional[str | int] = None,
                      disable_sema: Optional[bool] = False, join: Optional[bool] = False):
        # prevent memory leak
        # clear outdated owners
        self.clear_outdated_owners()
        self.acquiring_lock.append(1)  # add to queue
        self.init_owner(thread_owner=thread_owner)  # init owner
        self._acquire_owner_lock(thread_owner)  # get owner lock
        if not disable_sema:
            # todo
            #   Check is this double acquire compare to below
            self.acquire(thread_owner=thread_owner)
            self._release_owner_lock(thread_owner)
            self.acquiring_lock.pop()  # release the acquire lock
        if args is None: args = tuple()
        if kwargs is None: kwargs = {}
        thread = Thread(target=target, args=args, kwargs=kwargs)
        thread.start()
        if join:
            # todo
            #   Check is this double acquire compare to above
            self.acquire(thread_owner=thread_owner)
            if not disable_sema:
                self.release(thread_owner=thread_owner)
        return thread

    def acquire(self, *, thread_owner: Optional[str | int] = None):
        self.sema.acquire()
        self._acquire_owner_sema(thread_owner)

    def release(self, *, thread_owner: Optional[str | int] = None):
        self.sema.release()
        self._release_owner_sema(thread_owner)

    def wait_all_to_finish(self):
        """Check is all the thread completely by acquire"""
        slept_secs = 0
        # wait until no task are asking for semaphore
        max_wait = 12 * 60 * 60  # 12 hours
        while len(self.acquiring_lock) > 0:
            time.sleep(1)
            slept_secs += 1
            if slept_secs % 300 == 0:
                if slept_secs >= max_wait:
                    raise ValueError("Max iteration reached")

        for i in range(self.thread_size):
            self.sema.acquire()
        self.sema.release(n=self.thread_size)

    def wait_owner_to_finish(self, thread_owner: str | int):
        """Check is all the thread of same owner completely by acquire"""
        assert thread_owner is not None, "[Helpers] You must provide a thread owner"
        slept_secs = 0
        # wait until no task are asking for semaphore
        max_wait = 1 * 60 * 60  # 1 hour
        while thread_owner in self.owners and len(self.owners[thread_owner]['acquiring_lock']) > 0:
            time.sleep(1)
            slept_secs += 1
            if slept_secs % 300 == 0:
                if slept_secs >= max_wait:
                    raise ValueError("Max iteration reached")

        for i in range(self.thread_size):
            if thread_owner not in self.owners: break
            self.owners[thread_owner]['sema'].acquire()
        if thread_owner in self.owners:
            self.owners[thread_owner]['sema'].release(n=self.thread_size)
            # delete owner
            del self.owners[thread_owner]

    def clear_outdated_owners(self):
        """remove outdated owners from hash map"""
        threshold = datetime.now() - timedelta(hours=2)
        keys_to_del = []
        for owner, owner_dict in self.owners.items():
            if owner_dict['__created'] < threshold:
                keys_to_del.append(owner)
        for key in keys_to_del:
            if key in self.owners:
                del self.owners[key]

    def init_owner(self, thread_owner: Optional[str | int] = None):
        if thread_owner is None: return
        self.owners.setdefault(thread_owner, {
            "acquiring_lock": [],
            "__created": datetime.now(),
            "sema": Semaphore(self.thread_size)
        })

    def _acquire_owner_lock(self, thread_owner: Optional[str | int] = None):
        if thread_owner is None or thread_owner not in self.owners:  return
        self.owners[thread_owner]['acquiring_lock'].append(1)

    def _release_owner_lock(self, thread_owner: Optional[str | int] = None):
        if thread_owner is None or thread_owner not in self.owners:  return
        self.owners[thread_owner]['acquiring_lock'].pop()

    def _acquire_owner_sema(self, thread_owner: Optional[str | int] = None):
        if thread_owner is None or thread_owner not in self.owners:  return
        self.owners[thread_owner]['sema'].acquire()

    def _release_owner_sema(self, thread_owner: Optional[str | int] = None):
        if thread_owner is None or thread_owner not in self.owners: return
        self.owners[thread_owner]['sema'].release()


def threaded(*, sema: Optional[Semaphore] = None, join: Optional[bool] = False):
    def threaded_func(func):
        """
        Decorator that multithreads the target function
        with the given parameters. Returns the thread
        created for the function
        """

        def wrapper(*args, **kwargs):
            # acquire sema if sema is provided
            if sema is not None:
                sema.acquire()
            try:
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.start()
                if join:
                    thread.join()  # join if sema is provided, and then release
                    if sema is not None:
                        sema.release()
            except Exception as e:
                logger.critical(f"[Helper] Failed to run thread due to exception {e}")
                raise e  # bubble up the exception
            return thread

        return wrapper

    return threaded_func
