from pathlib import Path as PathWrapper
import tempfile, shutil
import os, stat
from typing import Optional


class FsysResource:
    def __init__(self, path : str):
        self._path_wrapper : PathWrapper = PathWrapper(path)
        if not (self.is_dir() or self.is_file()):
            raise FileNotFoundError(f'Path {path} is not a file/folder')


    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_base_path = os.path.join(write_dir, 'zipfile')
            args_dir = {
                'base_name': zip_base_path,
                'format': 'zip',
            }
            if self.is_file():
                args_dir['root_dir'] = self.get_dirpath()
                args_dir['base_dir'] = self.get_name()

            if self.is_dir():
                args_dir['root_dir'] = self.get_path()

            shutil.make_archive(**args_dir)
            with open(f'{zip_base_path}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # path and naming

    def get_name(self) -> str:
        return self._path_wrapper.name

    def get_path(self) -> str:
        return str(self._path_wrapper.absolute())

    def get_suffix(self) -> Optional[str]:
        parts = self.get_name().split('.')
        if len(parts) == 1:
            return None
        else:
            return parts[-1]

    def get_dirpath(self) -> str:
        return str(self._path_wrapper.parent.absolute())

    # -------------------------------------------
    # type

    def is_file(self) -> bool:
        return self._path_wrapper.is_file()

    def is_dir(self) -> bool:
        return self._path_wrapper.is_dir()

    # -------------------------------------------
    # attributes

    def is_hidden(self) -> bool:
        return is_hidden(self.get_path())

    def get_epochtime_last_modified(self) -> float:
        return os.path.getmtime(self.get_path())

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.get_path()) / (1024 * 1024)


def is_hidden(filepath: str) -> bool:
    if os.name == 'posix':
        return os.path.basename(filepath).startswith('.')
    elif os.name == 'nt':
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    else:
        raise NotImplementedError(f'Unsupported OS: {os.name}, {FsysResource.is_hidden.__name__} is only supported '
                                  f'on Windows and Unix systems')

