# -*- coding: utf-8 *-*
import pytest
from nicepy import deep

class Foo(object):
    """
    Our test objects come from here and are extendable.

    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


a = Foo('a')
a.b = Foo('a.b')
c = Foo('c')
c.b = Foo('c.b')

a.b.a = a
a.l = [a.b, c.b]
a.d = {'a': a.b, 'c': c.b}

def test_namepaths():
    assert a is deep.get(a)
    assert a is deep.get(a, '')

    # attributes
    assert a is deep.get(a.b, 'a')
    assert a is deep.get(a, 'b.a')

    # list indices
    assert a.l == deep.get(a, 'l')
    assert a.b is deep.get(a.l, '0')
    assert c.b is deep.get(a.l, '1')
    assert a.b is deep.get(a, 'l.0')
    assert c.b is deep.get(a, 'l.1')

    # dict values
    assert a.d == deep.get(a, 'd')
    assert a.b is deep.get(a.d, 'a')
    assert c.b is deep.get(a.d, 'c')
    assert a.b is deep.get(a, 'd.a')
    assert c.b is deep.get(a, 'd.c')

    # all together
    assert c.b is deep.get(a, 'l.0.a.d.c')

    # multiple at once
    assert (a.b, c.b) == deep.get(a, ('l.0', 'l.1'))
    assert (a.b, c.b) == deep.get(a, ('l.0 l.1'))


def test_failing():
    with pytest.raises(AttributeError):
        deep.get(a, 'x')
    with pytest.raises(IndexError):
        deep.get(a, 'l.2')
    with pytest.raises(KeyError):
        deep.get(a, 'd.x')


def test_not_failing_with_safe_variant():
    default = object()
    assert default is deep.get(a, 'x', default=default)
    assert default is deep.get(a, 'l.2', default=default)
    assert default is deep.get(a, 'd.x', default=default)
    assert (default, default) == deep.get(a, 'l.2 d.x', default=default)

    assert None is deep.get.safe(a, 'x')
    assert None is deep.get.safe(a, 'l.2')
    assert None is deep.get.safe(a, 'd.x')
    assert (None, None) == deep.get.safe(a, 'l.2 d.x')
