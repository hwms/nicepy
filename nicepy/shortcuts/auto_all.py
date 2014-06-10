# -*- coding: utf-8 *-*
import inspect
import logging
import sys

log = logging.getLogger(__name__)

def auto_all(module_name):
    module = sys.modules[module_name]
    all_list = sys.modules[module_name].__dict__.setdefault('__all__', [])
    for name, value in sys.modules[module_name].__dict__.items():
        if name not in all_list and not name.startswith('_') and inspect.getmodule(value) == module:
            all_list.append(name)

auto_all(__name__)
