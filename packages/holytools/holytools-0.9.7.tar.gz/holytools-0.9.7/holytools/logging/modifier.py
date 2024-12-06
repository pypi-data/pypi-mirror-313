import linecache
import os
import traceback
import types
from typing import Literal

Color = Literal['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']

# ---------------------------------------------------------


class LoggingModifier:
    @staticmethod
    def add_color(msg : str, color : Color) -> str:
        color_code_map = {
            'BLACK': '\033[30m',
            'RED': '\033[31m',
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'WHITE': '\033[37m'
        }

        color_code = color_code_map[color]
        return f"{color_code}{msg}\033[0m"


    @staticmethod
    def get_limited_stacktrace(err: Exception, excluded_modules : list[types.ModuleType]) -> str:
        err_class, err_instance, err_traceback = err.__class__, err, err.__traceback__
        tb_list = traceback.extract_tb(err_traceback)
        def is_relevant(tb):
            in_exclued_module = any([os.path.dirname(module.__file__) in tb.filename for module in excluded_modules])
            return not in_exclued_module

        err_msg = ''
        relevant_tb = [tb for tb in tb_list if is_relevant(tb)]
        if relevant_tb:
            err_msg = "\nEncountered error during training routine. Relevant stacktrace:"
            for frame in relevant_tb:
                file_path = frame.filename
                line_number = frame.lineno
                tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                          f'    {linecache.getline(file_path, line_number).strip()}')
                err_msg += f'\n{err_class.__name__}: {err_instance}\n{tb_str}'

        return err_msg
