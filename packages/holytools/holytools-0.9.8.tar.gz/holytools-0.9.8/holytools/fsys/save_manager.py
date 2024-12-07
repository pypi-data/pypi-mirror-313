import os
from typing import Optional

from pathvalidate import sanitize_filename


class SaveManager:
    @staticmethod
    def to_valid_filename(name : str) -> str:
        name = name.strip()
        name = name.replace(' ', '_')
        name = sanitize_filename(name)
    
        return name

    @staticmethod
    def prune_suffix(fpath : str) -> str:
        parts = fpath.split('.')
        if len(parts) > 1:
            return '.'.join(parts[:-1])
        else:
            return fpath

    @staticmethod
    def ensure_suffix(fpath: str, suffix : str) -> str:
        parts = fpath.split('.')
        if len(parts) < 2:
            fpath = f'{fpath}.{suffix}'
        elif parts[-1] != f'.{suffix}':
            fpath = f'{parts[0]}.{suffix}'
        return fpath

    @staticmethod
    def get_suffix(fpath: str) -> Optional[str]:
        parts = fpath.split('.')
        if len(parts) > 1:
            return parts[-1]
        else:
            return None

    @staticmethod
    def get_free_path(save_dirpath: str, name: str, suffix: Optional[str] = None, start_index: int = 1) -> str:
        if suffix:
            if not suffix.startswith('.'):
                suffix = f'.{suffix}'

        def get_path(index: int = start_index):
            conditional_suffix = '' if suffix is None else f'{suffix}'
            conditional_index = f'_{index}' if not index is None else ''
            return os.path.join(save_dirpath, f'{name}{conditional_index}{conditional_suffix}')

        fpath = get_path()
        current_index = 0
        while os.path.isfile(path=fpath) or os.path.isdir(fpath):
            current_index += 1
            fpath = get_path(index=current_index)
        return fpath