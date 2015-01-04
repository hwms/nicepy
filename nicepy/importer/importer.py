# -*- coding: utf-8 -*-
import contextlib
import os
import sys, imp

from .compile_flags import COMPLETE_FUTURE
from six.moves import filter, intern, input, map, range, reduce, xrange, zip  # @UnresolvedImport

default_config = dict(
    file_encoding='utf8',
    compile_flags=COMPLETE_FUTURE,
    filter=filter,
    intern=intern,
    input=input,
    map=map,
    range=range,
    reduce=reduce,
    xrange=xrange,
    zip=zip
    )


class NiceFutureImporter(object):
    def __init__(self, name, path, config=default_config, **kwargs):
        self.name = name
        # only deal with a single path for low complexity and for just py files this might be ok
        self.path = path[0]
        self.config = config.copy()
        self.config.update(kwargs)

    def find_module(self, fullname, path=None):
        if not path:
            return
        path = path[0]
        if not path.startswith(self.path):
            return
        name = fullname.split('.')[-1]
        fqname = os.path.join(path, '%s.py' % name)
        if os.path.isfile(fqname):
            path = fqname
        # TODO: loading packages would be needed when there is a need to write code in __init__.py
        # else:
        #    path = os.path.join(path, name)
        #    fqname = os.path.join(path, '__init__.py')
        if not os.path.isfile(fqname):
            return
        return NiceFutureLoader(self.config, fullname, [path], name, fqname)


class NiceFutureLoader(object):
    def __init__(self, config, fullname, path, name, fqname):
        self.config = config.copy()
        self.file_encoding = config.pop('file_encoding', 'utf8')
        self.compile_flags = config.pop('compile_flags', COMPLETE_FUTURE)
        self.fullname = fullname
        self.path = path
        self.name = name
        self.fqname = fqname

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            pass
        module = sys.modules.setdefault(self.fullname, self.new_module())
        with open(self.fqname, 'rb') as fh:
            source = fh.read().encode(self.file_encoding)
        code = compile(source, self.fqname, 'exec', flags=self.compile_flags, dont_inherit=True)
        exec(code, module.__dict__)
        return module

    def new_module(self):
        module = imp.new_module(self.fullname)
        module.__dict__.update(self.config,
            __file__=self.fqname,
            __loader__=self,
            __path__=self.path,
            __package__='.'.join(self.fullname.split('.')[:-1]),
        )
        return module


@contextlib.contextmanager
def future_imports(name, path, config=default_config, **kwargs):
    """
    Handle the import of all *.py files (except __init__.py) under a package path and allows keeping
    boilerplate header lines on all files to a minimum.

    With the following in packages __init__.py:

        from nicedjango.importer import future_imports
        with future_imports(__name__, __path__):
            from .submodule import *

    all submodules get treated as they would have this header:

        # -*- coding: utf-8 -*-
        from __future__ import with_statement, unicode_literals, division, print_function
        from six.moves import filter, intern, input, map, range, reduce, xrange, zip

    This can be changed by providing a config as dict containing import mappings and overwrites for
    file_encoding and compile_flags and/or kwargs for extending the default one.

    Example1:

        from nicedjango.importer import future_imports
        with future_imports(__name__, __path__, dict(file_encoding='latin1', compile_flags=None)):
            from .submodule import *

    all submodules get treated as they would have this header:

        # -*- coding: latin1 -*-

    Example2:

        from six.moves import filterfalse
        from itertools import chain
        from nicedjango.importer import future_imports
        with future_imports(__name__, __path__, exclude=filterfalse, chain=chain):
            from .submodule import *

    all submodules get treated as they would have this header:

        # -*- coding: utf-8 -*-
        from __future__ import with_statement, unicode_literals, division, print_function
        from six.moves import filter, intern, input, map, range, reduce, xrange, zip
        from six.moves import filterfalse as exclude
        from itertools import chain

    """
    old_meta_path = sys.meta_path
    sys.meta_path = [NiceFutureImporter(name, path, config, **kwargs)] + sys.meta_path
    try:
        yield None
    finally:
        sys.meta_path = old_meta_path
