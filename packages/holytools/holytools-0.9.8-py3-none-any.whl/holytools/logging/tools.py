import os
import sys
import time
from datetime import datetime
from typing import Callable

def get_timestamp(time_only : bool = False):
    if time_only:
        return datetime.now().strftime("%H:%M:%S")
    else:
        return datetime.now().strftime("%Y-%m-%d_%H%M")


def mute(func : Callable) -> Callable:
    def muted_func(*args, **kwargs):
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        result = func(*args, **kwargs)
        sys.stdout, sys.stderr = stdout, stderr
        return result
    return muted_func


def log_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        timestamp_start = get_timestamp(time_only=True)
        print(f"-[{timestamp_start}]: Launched \"{func.__name__}\" ")

        result = func(*args, **kwargs)

        end_time = time.time()
        timestamp_end = get_timestamp(time_only=True)
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f"-[{timestamp_end}]: Finished \"{func.__name__}\" (Time taken: {elapsed_time_ms:.2f} ms)\n")

        return result

    return wrapper



def to_sci_notation(val : str | float | int) -> str:
    try:
        val = float(val)
        display_val = f'{val:.1e}'
    except:
        display_val = val
    return  display_val



if __name__ == "__main__":
    @log_execution
    def some_nonsense():
        print('Hello world')

    some_nonsense()