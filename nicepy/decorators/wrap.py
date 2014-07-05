# -*- coding: utf-8 *-*
import inspect

__all__ = ['wrap_decorator']

class wrap_decorator(object):
    """
    Writing wrappers for instance methods can be a pain in the ass, so maybe this will grow into
    some helper which can deal with all kinds functions, methods, classmethods some day.

    For now it's the base for the default_args decorator.
    """
    def __init__(self, *args, **kwargs):
        self.func = None
        self.args = list(args)
        self.kwargs = kwargs
        self.func_attrs = []
        self.attrs = []

    def __call__(self, *args, **kwargs):
        if not self.func:
            self.set_func_and_func_attrs(args[0])
        return self

    def __get__(self, instance, owner):
        self.instance = instance
        self.owner = owner
        if not self.func:
            self.set_func_and_func_attrs(self.args[0])
            self.args = self.args[1:]
        if not self.attrs:
            self.attrs = self.get_attrs()
        return self.wrap

    def set_func_and_func_attrs(self, func):
        self.func = func
        self.func_attrs = inspect.getargspec(self.func)[0][1:]

    def get_attrs(self):
        return self.func_attrs[:]

    def wrap(self, *args, **kwargs):
        return self.func(self.instance, *args, **kwargs)
