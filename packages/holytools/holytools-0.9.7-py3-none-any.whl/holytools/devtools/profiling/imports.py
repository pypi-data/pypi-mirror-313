import builtins

from .profiler import Profiler



class ProfiledImportScope:
    def __init__(self):
        self._original_importer = builtins.__import__
        self.profiler : Profiler = Profiler()
        self.is_in_stack : bool = False

    # noinspection PyShadowingBuiltins
    def _profiled_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        if level == 0 and not self.is_in_stack:
            self.is_in_stack = True
            with self.profiler.timed_scope(name=name):
                result = self._original_importer(name, globals, locals, fromlist, level=level)
            self.is_in_stack = False
        else:
            result = self._original_importer(name, globals, locals, fromlist, level=level)
        return result

    def __enter__(self):
        builtins.__import__ = self._profiled_import

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.profiler.make_report(section_name=f'Library', print_average_times=False, print_num_calls=False))
        builtins.__import__ = self._original_importer

