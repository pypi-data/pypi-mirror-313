from __future__ import annotations

import os


# -------------------------------------------

class LocationManager:
    def __init__(self, root_dirpath : str):
        if not os.path.isdir(root_dirpath):
            raise ValueError(f'Failed to initialize {self.__class__.__name__}: Root directory {root_dirpath} does not exist')
        self._root_dirpath : str = root_dirpath
        self._subdir_paths: list[str] = []
        self._fpaths : list[str] = []

    def add_dir(self, relative_path: str) -> str:
        dirpath = self._get_relative_path(relative_path=relative_path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        self._subdir_paths.append(dirpath)
        return dirpath

    def add_file(self, relative_path: str) -> str:
        fpath = self._get_relative_path(relative_path=relative_path)
        self._fpaths.append(fpath)
        return fpath

    # -------------------------------------------

    def _get_relative_path(self, relative_path: str) -> str:
        root_dirpath = self.get_root_dirpath()
        return os.path.join(root_dirpath, relative_path)

    def get_root_dirpath(self) -> str:
        if self._root_dirpath is None:
            raise ValueError(f'Root directory not set for {self.__class__.__name__}')
        return self._root_dirpath
