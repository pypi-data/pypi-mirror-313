from typing import Any, Optional
from queue import Queue


class InputWaiter:
    def __init__(self, target_value : Optional[Any] = None):
        self.q = Queue()
        self.target_value : Optional[Any] = target_value
        self.is_done : bool = False

    def clear(self):
        self.q = Queue()

    def write(self, value : Optional[Any] = None):
        self.q.put(value)

    def get(self) -> Any:
        while True:
            value = self.q.get()
            if self.target_value == value:
                self.is_done = True
                return value

if __name__ == "__main__":
    waiter = InputWaiter(target_value=None)