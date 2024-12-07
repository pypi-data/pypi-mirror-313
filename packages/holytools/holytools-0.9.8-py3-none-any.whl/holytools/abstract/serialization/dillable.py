import dill
from pickle import dumps, loads
from .serializable import Serializable

class Dillable(Serializable):
    def to_str(self) -> str:
        return dill.dumps(self).hex()

    @classmethod
    def from_str(cls, s: str):
        return dill.loads(bytes.fromhex(s))


class Picklable(Serializable):
    def to_str(self) -> str:
        return dumps(self).hex()

    @classmethod
    def from_str(cls, s: str):
        return loads(bytes.fromhex(s))


# Example usage:
if __name__ == "__main__":
    class Example(Dillable):
        def __init__(self, data):
            self.data = data

    original = Example(data="Sample data")
    test_dill_str = original.to_str()
    restored = Example.from_str(test_dill_str)

    print(f"Original: {original.data}")
    # print(f"Restored: {restored._execution_profiles}")
