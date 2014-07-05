# -*- coding: utf-8 *-*
from __future__ import absolute_import
from .wrap import wrap_decorator

__all__ = ['default_args']

class default_args(wrap_decorator):
    """
    Decorator to remove boilerplate defaults duplication for examples like this:
    class A(object):
        def __init__(self):
            self.x = 0
            self.y = 1
            self.z = 2

        def method_with_values_where_defaults_are_same_as_instance_attrs(x=None, y=None, z=None):
            x = x or self.x
            y = y or self.y
            z = z or self.z
            return x, y, z

        @default_args
        def no_boilerplate_method(x, y, z):
            return x, y, z

    both methods return the same stuff.

    Just works for instance methods right now. See tests for further examples.
    """
    def __init__(self, *args, **kwargs):
        super(default_args, self).__init__(*args, **kwargs)
        self.defaults = {}

    def get_attrs(self):
        attrs = []
        if 'attrs' in self.kwargs:
            attrs = self.kwargs.pop('attrs')
        if isinstance(attrs, str):
            attrs = attrs.split(' ')
        for attr in self.func_attrs:
            if attr in self.kwargs:
                self.defaults[attr] = self.kwargs.pop(attr)
        attrs = self.func_attrs[:len(self.func_attrs) - len(attrs)] + attrs
        return attrs

    def wrap(self, *args, **kwargs):
        args = list(args)
        attrs = self.attrs[len(args):]
        for attr in attrs:
            args.append(getattr(self.instance, attr, self.defaults.get(attr, None)))
        return self.func(self.instance, *args, **kwargs)
