from __future__ import annotations
import os
from abc import abstractmethod
from typing import TypeVar
from typing import Optional


class Serializable:
    @abstractmethod
    def to_str(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_str(cls, s: str):
        pass

    def save(self, fpath : str, force_overwrite : bool = False) -> str:
        fpath = os.path.abspath(path=fpath)
        dirpath = os.path.dirname(fpath)
        os.makedirs(dirpath, exist_ok=True)
        full_name = os.path.basename(fpath)
        non_suffixname = full_name.split('.')[0]
        suffix = get_suffix(fpath)

        if os.path.isfile(fpath) and not force_overwrite:
            fpath = get_free_path(save_dirpath=dirpath, name=non_suffixname, suffix=suffix, start_index=1)
            print(f'Warning: File already exists at specified filepath. Saving to {fpath} instead.')

        with open(fpath, 'w') as f:
            f.write(self.to_str())

        return fpath

    @classmethod
    def load(cls, fpath : str) -> SerializableType:
        with open(fpath, 'r') as f:
            str_data = f.read()
        return cls.from_str(str_data)


def get_suffix(fpath) -> Optional[str]:
    parts = fpath.split('.')
    if len(parts) == 1:
        return None
    else:
        return parts[-1]


def get_free_path(save_dirpath : str, name : str, suffix : Optional[str] = None, start_index : int = 0) -> str:
    if suffix:
        if not suffix.startswith('.'):
            suffix = f'.{suffix}'

    def get_path(index : int = start_index):
        conditional_suffix = '' if suffix is None else f'{suffix}'
        conditional_index = f'_{index}' if not index is None else ''
        return os.path.join(save_dirpath, f'{name}{conditional_index}{conditional_suffix}')

    fpath = get_path()
    current_index = 0
    while os.path.isfile(path=fpath) or os.path.isdir(fpath):
        current_index += 1
        fpath = get_path(index=current_index)
    return fpath


SerializableType = TypeVar(name='SerializableType', bound=Serializable)