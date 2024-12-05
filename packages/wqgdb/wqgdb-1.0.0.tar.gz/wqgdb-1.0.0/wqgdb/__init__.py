import os
import sys
import gdb
import importlib

sys.path.append(os.path.dirname(__file__))
from common import *

# foreach register module
modules = []
for f in os.listdir(os.path.dirname(__file__)):
    if os.path.isfile(os.path.join(os.path.dirname(__file__), f)) and f not in [
        "__init__.py",
        "common.py",
    ]:
        # print(f)
        module_name = f[:-3]
        modules.append(importlib.import_module("wq." + module_name))

# foreach register command
instances = []
for class_name, cls in GdbCommandRegistry.classes.items():
    instance = cls()
    instances.append(instance)
    # print(f"Created an instance of {class_name}: {instance}")
