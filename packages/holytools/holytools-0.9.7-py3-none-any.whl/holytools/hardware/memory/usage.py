import psutil
import inspect
from psutil import Process, NoSuchProcess
from pympler import asizeof

# -------------------------------------------

class ProcessStatistics:
    def __init__(self, pid : int):
        self.pid : int = pid

        init_successful = False
        try:
            self.process : Process = psutil.Process(self.pid)
            init_successful = True
        except NoSuchProcess:
            pass
        if not init_successful:
            raise IOError(f"Process with PID {self.pid} does not exist.")

    def get_subprocesses(self) -> list[Process]:
        return self.process.children(recursive=True)

    def get_memory_usage_in_mb(self) -> float:
        memory_info = self.process.memory_info()
        return memory_info.rss / (1024 ** 2)

    def get_cpu_usage(self) -> float:
        process = psutil.Process(self.pid)
        return process.cpu_percent(interval=0.1)

    def get_subprocess_mem_usage(self) -> dict[str, int]:
        mem_usage = {}
        for child in self.get_subprocesses():
            try:
                mem_info = child.memory_info()
                mem_usage[child.name()] = mem_info.rss
            except psutil.NoSuchProcess:
                continue
        return mem_usage


class FunctionStatistics:
    @staticmethod
    def get_mem_usage() -> int:
        caller_frame = inspect.currentframe().f_back
        try:
            current_locals_size = asizeof.asizeof(caller_frame.f_locals)
            return current_locals_size
        finally:
            del caller_frame

    @staticmethod
    def get_variable_mem_usage() -> dict[str, int]:
        caller_frame = inspect.currentframe().f_back
        try:
            variables_memory_usage = {}
            for var_name, var_value in caller_frame.f_locals.items():
                variables_memory_usage[var_name] = asizeof.asizeof(var_value)
            return variables_memory_usage
        finally:
            del caller_frame


if __name__ == "__main__":
    process_stats = ProcessStatistics(4028)
    print(f"Memory usage: {process_stats.get_memory_usage_in_mb()} MB")
    print(f"CPU usage: {process_stats.get_cpu_usage()} %")
    print(process_stats.get_subprocesses())
    print(process_stats.get_subprocess_mem_usage())