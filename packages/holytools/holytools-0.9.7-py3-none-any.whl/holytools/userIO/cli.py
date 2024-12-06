from typing import Callable
import inspect
from holytools.logging import Loggable, LogLevel
# ---------------------------------------------------------


class InteractiveCLI(Loggable):
    _exit_str = 'q'

    def __init__(self, cls : type, description : str = ''):
        super().__init__()
        self.cls : type = cls
        self.desc : str = description

        self._log_header()
        self.obj : object = self._create_object()
        self.methods_dict : dict[int, Callable] = self._get_methods_dict(obj=self.obj)


    def _log_header(self):
        header_size = 40
        cls_name = self.cls.__name__
        hash_count = int(max(header_size-len(cls_name), 0)/2)
        hashes = '-' * hash_count
        self.log(f'{hashes} {cls_name.upper()} CLI {hashes}')
        desc_str = self.desc if self.desc else 'No description found'
        self.log(f"Description: {desc_str} \n")


    def _create_object(self):
        self.log(f'Initializing object {self.cls.__name__}:')
        try:
            init_method = self.__init__
            init_kwargs = self._get_args_dict(mthd=init_method)
            return self.cls(**init_kwargs)
        except Exception as e:
            self.log(f"Error initializing {self.cls.__name__}: {e}. Please try again\n")
            return self._create_object()



    def _get_methods_dict(self, obj) -> dict[int, Callable]:
        public_methods_names = self._get_public_method_names()
        return {i + 1: getattr(obj,name) for i, name in enumerate(public_methods_names)}


    def _get_public_method_names(self) -> list[str]:
        is_public_callable = lambda attr: callable(getattr(self.obj, attr)) and not attr.startswith("_")
        public_method_names = [method for method in dir(self.obj) if is_public_callable(method)]
        return public_method_names

    # ---------------------------------------------------------
    # loop

    def loop(self):
        while True:
            self.print_info()
            user_input = input()
            if user_input == self._exit_str:
                break

            if not user_input.isdigit() or int(user_input) not in self.methods_dict:
                self.log("Please enter a valid number.")
                continue

            try:
                result = self._handle_mthd_call(int(user_input))
                msg = f"Result : {result}"
                level = LogLevel.INFO
            except Exception as e:
                msg = f"Error: {e}"
                level = LogLevel.WARNING
            self.log(msg=msg, level=level)


    def print_info(self):
        text = f"\nChoose a method by entering its number or '{self._exit_str}' to quit): "
        for index, method in self.methods_dict.items():
            text += f"\n{index}: {method.__name__}"
        self.log(msg=text)


    def _handle_mthd_call(self, index : int):
        mthd = self.methods_dict[index]
        args_dict = self._get_args_dict(mthd=mthd)
        result = mthd(**args_dict)
        return result


    def _get_args_dict(self, mthd: callable) -> dict:
        args_dict = {}
        spec = inspect.getfullargspec(mthd)
        annotations = spec.annotations
        for arg_name in spec.args[1:]:
            arg_type = annotations.get(arg_name, str)
            self.log(f"Enter value for \"{mthd.__name__}\" argument \"{arg_name}\" ({arg_type.__name__}): ")
            user_input = input()
            args_dict[arg_name] = self.get_value(user_input=user_input, arg_type=arg_type, arg_name=arg_name)
        return args_dict


    @staticmethod
    def get_value(user_input : str, arg_type : type, arg_name : str):
        if arg_type == bool:
            if user_input not in ['0', '1']:
                raise ValueError(f"For argument '{arg_name}', please enter '0' for False or '1' for True.")
            val = bool(int(user_input))
        else:
            try:
                val = arg_type(user_input)
            except ValueError:
                raise ValueError(f"Invalid input type for '{arg_name}'. Expected a value of type {arg_type.__name__}.")
        return val
