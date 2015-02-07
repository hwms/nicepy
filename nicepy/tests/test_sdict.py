# -*- coding: utf-8 *-*
from nicepy.collections import sdict


def test_init_dict():
    class sdict_(sdict):
        call_times = 0
        call_args_list = []
        call_kwargs_list = []
        def update(self, *args, **kwargs):
            self.__class__.call_times += 1
            self.__class__.call_args_list.append(args)
            self.__class__.call_kwargs_list.append(kwargs)

    sdict_()
    assert sdict_.call_times == 0

    a, b = object(), object()

    sdict_(a)
    sdict_(b=b)
    sdict_(a, b=b)
    assert sdict_.call_times == 3
    assert sdict_.call_args_list == [(a,), (), (a,)]
    assert sdict_.call_kwargs_list == [{}, {'b': b}, {'b': b}]


def test_update():
    a = sdict()
    a.update(dict(a=[1, 2], b=[3, 4], c=[1, 4]))
    assert a == {'a': set([1, 2]), 'b': set([3, 4]), 'c': set([1, 4])}

    a = sdict()
    a.update([('a', [1, 2]), ('b', [3, 4]), ('c', [1, 4])])
    assert a == {'a': set([1, 2]), 'b': set([3, 4]), 'c': set([1, 4])}

    a = sdict()
    a.update([('a', [1, 2])], b=[3, 4], c=[1, 4])
    assert a == {'a': set([1, 2]), 'b': set([3, 4]), 'c': set([1, 4])}

    a = sdict()
    a.update(a=[1, 2], b=[3, 4], c=[1, 4])
    assert a == {'a': set([1, 2]), 'b': set([3, 4]), 'c': set([1, 4])}


def test_switched():
    a = sdict(a=[1, 2], b=[3, 4], c=[1, 4])
    b = a.switched()
    assert b == {1: set(['a', 'c']), 2: set(['a']), 3: set(['b']),
                 4: set(['c', 'b'])}


def test_setitem():
    b = sdict({1: ['a', 'c'], 2: ['a'], 3: ['b'], 4: ['c', 'b']})
    b[1] = ['a', 'd']
    assert b == {1: set(['a', 'd']), 2: set(['a']), 3: set(['b']),
                 4: set(['c', 'b'])}


def test_delete():
    b = sdict({1: ['a', 'd'], 2: ['a'], 3: ['b'], 4: ['c', 'b']})
    removed_from, deleted = b.delete('a')
    assert removed_from == set([1, 2])
    assert deleted == set([2])
    assert b == {1: set(['d']), 3: set(['b']), 4: set(['c', 'b'])}


def test_union():
    b = sdict({1: ['d'], 3: ['b'], 4: ['c', 'b']})
    c = b.union()
    assert c == set(['d', 'b', 'c'])
