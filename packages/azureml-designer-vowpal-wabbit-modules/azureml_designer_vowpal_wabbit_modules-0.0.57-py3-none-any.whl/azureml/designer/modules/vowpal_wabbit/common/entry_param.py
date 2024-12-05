import types
from abc import ABCMeta
from functools import partial


class EntryParam(ABCMeta):
    _LOADER = 'load'
    _ENTRY_PARAM_LOADER = "_ENTRY_PARAM_LOADER"
    param_loaders = {}

    def __new__(mcs, name, bases, class_dict):
        cls = ABCMeta.__new__(mcs, name, bases, class_dict)
        loader_name = class_dict.get(EntryParam._ENTRY_PARAM_LOADER, EntryParam._LOADER)
        EntryParam.param_loaders[cls] = getattr(cls, loader_name)
        return cls

    @staticmethod
    def load(p_type, p_value):
        """Try to load p_value to the specified p_type type.

        If p_value is None or has already been of p_type, just return, or try to find loaders in params_loader.
        """
        if p_value is None or isinstance(p_value, p_type):
            return p_value
        loader = EntryParam.param_loaders.get(p_type, p_type)
        return loader(p_value)


class Boolean(metaclass=EntryParam):
    @staticmethod
    def load(bool_str: str):
        if isinstance(bool_str, bool):
            return bool_str
        if bool_str not in ["True", "False"]:
            raise TypeError(f"Cannot convert {bool_str} to bool type")
        return bool_str == "True"


class MultiTypeParam:
    def __new__(cls, exp_types):
        multi_type = types.new_class(name=f"MultiTypeParam({','.join([str(exp_type) for exp_type in exp_types])})",
                                     kwds={'metaclass': EntryParam},
                                     exec_body=lambda ns: ns.update({'load': partial(cls.load, exp_types=exp_types)}))
        return multi_type

    @staticmethod
    def load(p_value, exp_types):
        exp_value = None
        for exp_type in exp_types:
            if isinstance(p_value, exp_type):
                exp_value = p_value
                break
        return exp_value if exp_value else EntryParam.load(next((exp_type for exp_type in exp_types)), p_value)
