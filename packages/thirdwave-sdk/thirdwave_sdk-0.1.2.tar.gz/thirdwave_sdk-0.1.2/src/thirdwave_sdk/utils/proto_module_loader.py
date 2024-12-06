import sys
import types


def load_module(module_name, target_module):
    module = types.ModuleType(module_name)
    sys.modules[module_name] = module
    for attr in dir(target_module):
        if not attr.startswith("__"):
            setattr(module, attr, getattr(target_module, attr))
