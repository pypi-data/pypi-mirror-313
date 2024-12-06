from types import NoneType
from typing import get_origin, get_args, Union


class TypeInspector:
    @staticmethod
    def get_type_list(dtype : type) -> list[type]:
        """
        :return: If dtype is of form Union[<dtype>] returns [<dtype1>, <dtype2>,...] ; Else returns [<dtype>]
        """
        if get_origin(dtype) is Union:
            return list(get_args(dtype))
        else:
            return [dtype]

    # noinspection DuplicatedCode
    @staticmethod
    def get_core_type(dtype : type) -> type:
        """
        :return: If dtype is of form Optional[<dtype>] returns <dtype>; Else returns <dtype>
        """
        if get_origin(dtype) is Union:
            types = get_args(dtype)

            core_types = [t for t in types if not t is NoneType]
            if len(core_types) == 1:
                return core_types[0]
            else:
                raise ValueError(f'Union dtype {dtype} has more than one core dtype')
        else:
            return dtype

    @staticmethod
    def is_optional_type(dtype : type) -> bool:
        """
        :return: Returns true if <dtype> is of form Optional[<dtype>] or Union[None, (...)]; Else returns false
        """
        if get_origin(dtype) is Union:
            types = get_args(dtype)
            return any([t for t in types if t is NoneType])

        return False

    @staticmethod
    def check_dtype_confirmity(obj : object, dtype : type) -> bool:
        if get_origin(dtype) is list:
            if not isinstance(obj, list):
                return False
            if not get_args(dtype):
                return False
            element_type = get_args(dtype)[0]
            return all([isinstance(x, element_type) for x in obj])
        else:
            obj_conforms = isinstance(obj, dtype)
        return obj_conforms
