import time
from typing import Callable

from tabulate import tabulate


class ExecutionProfile:
    def __init__(self):
        self.execution_times = []

    def register_time(self, time_in_sec : float):
        self.execution_times.append(time_in_sec)

    @property
    def num_calls(self):
        return len(self.execution_times)

    @property
    def total_time(self):
        return sum(self.execution_times)

    @property
    def average_time(self):
        return self.total_time / self.num_calls

class TimedScope:
    def __init__(self, name: str, storage : dict[str, ExecutionProfile], on_exit : Callable):
        self.name : str = name
        self.storage : dict[str, ExecutionProfile] = storage
        self.on_exit : Callable = on_exit

    def __enter__(self):
        self.start_time = time.time()
        if not self.name in self.storage:
            self.storage[self.name] = ExecutionProfile()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed = end_time - self.start_time
        if self.name in self.storage:
            self.storage[self.name].register_time(elapsed)
        else:
            raise KeyError(f"Execution profile {self.name} not found in storage")
        self.on_exit()

class Profiler:
    def __init__(self):
        self._execution_profiles : dict[str, ExecutionProfile] = {}

    def make_report(self, section_name : str = f'Routine', print_average_times=True, print_num_calls=True):
        headers = [section_name, "Total Time (s)"]
        if print_average_times:
            headers.append("Average Time (s)")
        if print_num_calls:
            headers.append("Calls")

        table = []
        for section, profile in self._execution_profiles.items():
            row = [section, f"{profile.total_time:.6f}"]
            if print_average_times:
                row.append(f"{profile.average_time:.6f}")
            if print_num_calls:
                row.append(profile.num_calls)
            table.append(row)

        return tabulate(table, headers=headers, tablefmt="psql")

    def timed_scope(self, name : str, print_on_exit : bool = False) -> TimedScope:
        def print_report():
            print(self.make_report())
        on_exit = print_report if print_on_exit else lambda *args, **kwargs : None
        return TimedScope(name=name,storage=self._execution_profiles,on_exit=on_exit)


    @staticmethod
    def measure(self, func):
        def wrapper(*args, **kwargs):
            with self.timed_scope(name=func.__name__):
                result = func(*args, **kwargs)
            return result

        return wrapper


if __name__ == "__main__":
    class ExampleClass(Profiler):
        def some_method(self):
            with self.timed_scope(name='being_work'):
                time.sleep(0.1)

            with self.timed_scope(name='phase2'):
                time.sleep(0.1)
                self.subroutine()
            with self.timed_scope(name='phase3'):
                time.sleep(0.1)

        def subroutine(self):
            with self.timed_scope(name='subroutine'):
                time.sleep(0.2)

    instance = ExampleClass()
    instance.some_method()  # Execute the profiled method multiple times to see accumulation
    instance.some_method()
    print(instance.make_report())  # Output the profiling report


