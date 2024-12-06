import os
import importlib
from inspect import isclass, getmembers

__all__ = []

# Dynamically import all modules and collect classes
for module in os.listdir(os.path.dirname(__file__)):
    if module.endswith(".py") and module != "__init__.py":
        module_name = module[:-3]
        module_obj = importlib.import_module(f".{module_name}", package=__name__)
        for name, obj in getmembers(module_obj):
            if isclass(obj):
                globals()[name] = obj
                __all__.append(name)