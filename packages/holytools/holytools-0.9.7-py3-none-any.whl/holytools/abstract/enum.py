from enum import Enum
from typing import TypeVar

EnumType = TypeVar('EnumType', bound=Enum)

class SelectableEnum(Enum):
    @classmethod
    def from_manual_query(cls) -> EnumType:
        options = [e.name for e in cls]
        while True:
            val = input(f"Creating {cls.__name__} manually, choose one of options {options}, type 'exit' to quit): ")
            if val.lower() == 'exit':
                raise ValueError("User exited")
            try:
                return cls[val]
            except KeyError:
                print("Invalid input. Please try again.")


class NEW(SelectableEnum):
    UP = 'up'
    DOWN = 'downn'

if __name__ == "__main__":
    a = NEW.from_manual_query()