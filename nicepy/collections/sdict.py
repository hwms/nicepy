# -*- coding: utf-8 -*-
import logging
from collections import Mapping, MutableMapping
log = logging.getLogger(__name__)

class sdict(dict):
    """
    A dict which has sets as values containing the real values.
    Opens the possibility to switch values against keys.

    sdict([[E, ]**F]) -> D
    Create D, either empty or from mapping/iterable E and F.
    If E present and has a .keys() method, does equivalent of:
        D = sdict(); for k in E: D[k] = D.get(k, set()).update(E[k])
    If E present and lacks .keys() method, does equivalent of:
        D = sdict(); for (k, v) in E: D[k] = D.get(k, set()).update(v)
    In either case, this is followed by equivalent of:
        for k, v in F.items(): D[k] = D.get(k, set()).update(v)

    Example usages:
        a = sdict(a=[1,2],b=[3,4],c=[1,4])
        a == {'a': set([1, 2]),
              'b': set([3, 4]),
              'c': set([1, 4])}

        b = a.switched()
        b == sdict({1: set(['a', 'c']),
                    2: set(['a']),
                    3: set(['b']),
                    4: set(['c', 'b'])}

        b[1] = ['a', 'd']
        b == sdict({1: set(['a', 'd']),
                    2: set(['a']),
                    3: set(['b']),
                    4: set(['c', 'b'])}

        c = b.delete('a')
        c == set([1, 2])
        b == sdict({1: set(['d']),
                    3: set(['b']),
                    4: set(['c', 'b'])}

        c = b.union()
        c == set(['d', 'b', 'c'])

    """
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self.update(*args, **kwargs)

    def __repr__(self):
        return 'sdict(%r)' % super(sdict, self).__repr__()

    __marker = object()

    def update(self, *args, **kwds):
        """
        D.update([E, ]**F) -> D.
        Update D from mapping/iterable E and F and return D for chaining again.
        If E present and has a .keys() method, does equivalent of:
            for k in E: D[k] = D.get(k, set()).update(E[k])
        If E present and lacks .keys() method, does equivalent of:
            for (k, v) in E: D[k] = D.get(k, set()).update(v)
        In either case, this is followed by equivalent of:
            for k, v in F.items(): D[k] = D.get(k, set()).update(v)
        """
        if len(args) > 1:
            raise TypeError("update() takes at most 1 positional "
                            "argument ({} given)".format(len(args)))
        other = args[0] if len(args) >= 1 else ()

        if isinstance(other, Mapping):
            self._update_with_keys(other, other)
        elif hasattr(other, 'keys'):
            self._update_with_keys(other, other.keys())
        else:
            self._update_with_items(other)
        self._update_with_items(kwds.items())

        return self

    def _update_with_keys(self, other, keys):
        for key in keys:
            self._get_or_create(key).update(other[key])

    def _update_with_items(self, items):
        for key, value in items:
            self._get_or_create(key).update(value)

    def _get_or_create(self, key):
        value_set = self.get(key, None)
        if value_set is None:
            self[key] = value_set = set()
        return value_set

    def __setitem__(self, key, value):
        if not type(value) == set or value:
            value = set(value)
        super(sdict, self).__setitem__(key, value)

    def switched(self):
        result = sdict()
        for key, value_set in self.iteritems():
            for value in value_set:
                result._get_or_create(value).add(key)
        return result

    def delete(self, value):
        """
        Delete a value in all value sets and delete resulting empty items.

        Returns removed_from and deleted sets of keys.
        """
        removed_from = set()
        deleted = set()
        for key, value_set in self.iteritems():
            try:
                value_set.remove(value)
            except KeyError:
                continue
            removed_from.add(key)
            if not value_set:
                deleted.add(key)
        for key in deleted:
            self.pop(key)
        return removed_from, deleted

    def union(self):
        return set.union(*self.values())

MutableMapping.register(sdict)
