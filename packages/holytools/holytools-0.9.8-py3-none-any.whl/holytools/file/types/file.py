from abc import abstractmethod
from typing import Optional
import os
from enum import Enum
from pathlib import Path
from base64 import b64encode
from abc import ABC

class Access(Enum):
    READABLE = os.R_OK
    WRITABLE = os.W_OK
    EXECUTABLE = os.X_OK

class File(ABC):
    def __init__(self, fpath : str, require_writable : bool = True, require_executable : bool = False):
        self.fpath : str = str(Path(fpath).absolute())
        required_permissions : set[Access] = {Access.READABLE}
        if require_writable:
            required_permissions.add(Access.WRITABLE)
        if require_executable:
            required_permissions.add(Access.EXECUTABLE)

        actual_permissions = {access for access in required_permissions if self.has_permission(access=access)}
        missing_permissions = required_permissions - actual_permissions
        if missing_permissions:
            raise PermissionError(f'File {fpath} does not have required permissions: {missing_permissions}')

        self.check_format_ok()

    def has_permission(self, access : Access) -> bool:
        if os.path.isdir(self.fpath):
            return False
        if os.path.isfile(self.fpath):
            return os.access(self.fpath, access.value)
        else:
            parent_directory = os.path.dirname(self.fpath)
            return os.access(parent_directory, access.value) if parent_directory else False

    def check_format_ok(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, content):
        pass

    @abstractmethod
    def view(self):
        print(f'Displaying content of file \"{self.fpath}\":')
        print('-'*20)

    def get_suffix(self) -> Optional[str]:
        parts = self.fpath.split('.')
        suffix = parts[-1] if len(parts) > 1 else None
        return suffix

    def as_bytes(self):
        with open(self.fpath, 'rb') as file:
            content = file.read()
        return content

    def as_base64(self) -> str:
        data = self.as_bytes()
        return b64encode(data).decode(encoding='utf-8')

    def exists_on_disk(self) -> bool:
        return os.path.isfile(self.fpath)
