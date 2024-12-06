import time
import threading
import inspect
import uuid
from typing import Callable
from dataclasses import dataclass

@dataclass
class Task:
    func : Callable
    is_canceled : bool = False

    def __post_init__(self):
        self.id: str = str(uuid.uuid4())

    def run(self):
        if not self.is_canceled:
            self.func()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class TaskScheduler:
    def __init__(self):
        self.scheduled_tasks: dict[str, Task] = {}
    
    def submit_once(self, task: Callable, delay: float) -> Task:
        return self._schedule_task(task=task, delay=delay)

    def submit_periodic(self, task: Callable, interval: float):
        def periodic():
            threading.Thread(target=task).start()
            self.submit_periodic(task, interval)
        self._schedule_task(task=periodic, delay=interval)

    def submit_at_rate(self, tasks : list[Callable], rate_per_second : float):
        for task in tasks:
            time.sleep(1/rate_per_second)
            self._schedule_task(task, delay=0)

    def cancel_all(self):
        for task in self.scheduled_tasks.values():
            task.is_canceled = True

    def is_active(self):
        return len(self.scheduled_tasks) != 0

    # ---------------------------------------------------------

    def _schedule_task(self, task : Callable, delay : float) -> Task:
        parameters = inspect.signature(task).parameters.values()
        for param in parameters:
            not_args_or_kwargs = (param.kind not in [param.VAR_POSITIONAL, param.VAR_KEYWORD])
            has_no_defaults = (param.default is param.empty)
            if has_no_defaults and not_args_or_kwargs:
                raise InvalidCallableException("Cannot schedule task that requires arguments")

        task = Task(func=task)
        def do_delayed():
            self.scheduled_tasks[task.id] = task
            time.sleep(delay)
            task.run()
            print(f'Scheduled tasks is {self.scheduled_tasks}')
            print(f'Task id is {task.id}')
            del self.scheduled_tasks[task.id]
        
        threading.Thread(target=do_delayed).start()
        return task


class InvalidCallableException(Exception):
    """Exception raised when a callable with arguments is passed where none are expected."""
    pass


# Example usage
if __name__ == "__main__":
    def my_task():
        print(f"Task executed at {time.ctime()}. Now sleeping for 2 seconds")
        time.sleep(2)
        print(f'I work up at {time.ctime()}')

    def get_print_function(num : int):
        def print_num():
            print(num)
        return print_num


    def invalid_task(num : int):
        print(num)


    scheduler = TaskScheduler()
    # scheduler.submit_once(my_task, delay=2)
    # scheduler.submit_periodic(my_task, interval=1)
    scheduler.submit_once(task=invalid_task, delay=0)

    # scheduler.submit_at_rate(tasks=[get_print_function(i) for i in range(10)], rate_per_second=5)
    #
    # print(f'Sleepting at {time.ctime()}')
    # time.sleep(15)
