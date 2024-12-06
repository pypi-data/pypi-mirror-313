import inspect
from typing import Any, Callable, get_type_hints
from dataclasses import dataclass
from typing import Union

class BoundFunction:
    __self__: object


@dataclass
class Argument:
    name: str
    dtype: type

    def set_default_val(self, val: object):
        setattr(self, 'default_val', val)

    def has_default_val(self):
        return hasattr(self, 'default_val')

    def get_default_val(self) -> Any:
        if not self.has_default_val():
            raise AttributeError(f"Argument '{self.name}' has no default value.")
        return getattr(self, 'default_val')



class ModuleInspector:
    @staticmethod
    def get_methods(obj : Union[object, type], public_only= False, include_operators : bool = False, include_inherited : bool = True) -> list[Callable]:
        def attr_filter(attr_name : str) -> bool:
            is_ok = True
            if public_only and attr_name.startswith('_'):
                is_ok = False
            if not include_operators and attr_name.startswith('__') and attr_name.endswith('__'):
                is_ok = False
            attr_value = getattr(obj, attr_name)
            is_callable = callable(attr_value)
            return is_ok and is_callable
        attrs = dir(obj) if include_inherited else list(obj.__dict__.keys())
        methods = [getattr(obj, name) for name in attrs if attr_filter(name)]
        return methods


    @staticmethod
    def get_args(func: Union[Callable, BoundFunction], exclude_self : bool = True) -> list[Argument]:
        spec = inspect.getfullargspec(func)
        type_hints = get_type_hints(func)
        if not spec.args:
            return []
        start_index = 1 if exclude_self and spec.args[0] in ['self', 'cls'] else 0
        relevant_arg_names = spec.args[start_index:]
        defaults_mapping = ModuleInspector._get_defaults_mapping(spec=spec)

        def create_arg(name : str):
            dtype = type_hints.get(name)
            is_bound = inspect.ismethod(func)
            if name == 'self' and is_bound:
                dtype = func.__self__.__class__
            if name == 'cls' and is_bound:
                dtype = func.__self__
            if not dtype:
                raise ValueError(f"Type hint for argument '{name}' is missing.")
            argument = Argument(name=name, dtype=dtype)
            if name in defaults_mapping:
                argument.set_default_val(defaults_mapping[name])
            return argument

        return [create_arg(name=name) for name in relevant_arg_names]

    @staticmethod
    def _get_defaults_mapping(spec):
        defaults = spec.defaults or ()
        reversed_args = spec.args[::-1]
        reversed_defaults = defaults[::-1]

        zipped = zip(reversed_args, reversed_defaults)
        return dict(zipped)
