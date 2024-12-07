from threading import Event
from typing import Callable
from .task_scheduler import TaskScheduler


class Countdown:
    def __init__(self, duration: float, on_expiration: Callable = lambda *args, **kwargs: None):
        self.duration : float = duration
        self.on_expiration : Callable = on_expiration
        self.scheduler : TaskScheduler = TaskScheduler()
        self.one_time_lock = Lock()

    def start(self):
        self.scheduler.submit_once(task=self._release, delay=self.duration)

    def restart(self):
        self.scheduler.cancel_all()
        self.start()

    def is_active(self):
        return self.scheduler.is_active()

    def wait(self):
        self.one_time_lock.wait()

    # -------------------------------------------

    def _release(self):
        self.one_time_lock.unlock()
        self.on_expiration()


class Lock:
    def __init__(self):
        self._event = Event()
        self._event.clear()

    def wait(self):
        self._event.wait()

    def unlock(self):
        self._event.set()



