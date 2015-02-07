# -*- coding: utf-8 *-*
from nicepy.decorators import default_args

class TestDefaultArgsFromAttrs:

    def test_without_args(self):
        class A(object):
            def __init__(self):
                self.x = 0
                self.y = 1
                self.z = 2

            @default_args
            def m(self, x, y, z):
                print 'm1', x, y, z
                return x, y, z

        a = A()

        assert (3, 4, 5) == a.m(3, 4, 5)
        assert (0, 1, 2) == a.m()
        assert (3, 1, 2) == a.m(3)
        assert (3, 4, 2) == a.m(3, 4)

    def test_with_attr_kwarg(self):
        class A(object):
            def __init__(self):
                self.x = 0
                self.y = 1
                self.z = 2

            @default_args(attrs='x y z')
            def m1(self, a, b, c):
                print 'm1', a, b, c
                return a, b, c

            @default_args(attrs='z x y')
            def m2(self, x, y, z):
                print 'm2', x, y, z
                return x, y, z

            @default_args(attrs='x y')
            def m3(self, x, y, z):
                print 'm3', x, y, z
                return x, y, z

            @default_args(attrs='x y')
            def m4(self, a, b, c):
                print 'm4', a, b, c
                return a, b, c

        a = A()

        assert (0, 1, 2) == a.m1()
        assert (3, 1, 2) == a.m1(3)
        assert (3, 4, 2) == a.m1(3, 4)
        assert (3, 4, 5) == a.m1(3, 4, 5)

        assert (2, 0, 1) == a.m2()
        assert (3, 0, 1) == a.m2(3)
        assert (3, 4, 1) == a.m2(3, 4)
        assert (3, 4, 5) == a.m2(3, 4, 5)

        assert (0, 0, 1) == a.m3()
        assert (3, 0, 1) == a.m3(3)
        assert (3, 4, 1) == a.m3(3, 4)
        assert (3, 4, 5) == a.m3(3, 4, 5)

        assert (3, 0, 1) == a.m4(3)
        assert (3, 4, 1) == a.m4(3, 4)
        assert (3, 4, 5) == a.m4(3, 4, 5)

    def test_with_default_and_attr_kwarg(self):
        class A(object):
            def __init__(self):
                self.x = 0
                self.z = 2

            @default_args(y=1, attrs='z')
            def m1(self, x, y, v):
                print 'm1', x, y, v
                return x, y, v

        a = A()

        assert (0, 1, 2) == a.m1()
        assert (3, 1, 2) == a.m1(3)
        assert (3, 4, 2) == a.m1(3, 4)
        assert (3, 4, 5) == a.m1(3, 4, 5)

    def test_with_default_and_attr_kwarg_and_set_attrs(self):
        class A(object):
            def __init__(self):
                self.x = 0
                self.z = 2

            @default_args(y=1, attrs='z', set_attrs=True)
            def m1(self, x, y, v):
                print 'm1', x, y, v
                return x, y, v

            @default_args(y=1, attrs='z', set_attrs='y')
            def m2(self, x, y, v):
                print 'm1', x, y, v
                return x, y, v

        a = A()
        assert (0, 1, 2) == a.m1()
        assert 0 == a.x
        assert 1 == a.y

        a = A()
        assert (3, 1, 2) == a.m1(3)
        assert 3 == a.x
        assert 1 == a.y

        a = A()
        assert (3, 4, 2) == a.m1(3, 4)
        assert 3 == a.x
        assert 4 == a.y

        a = A()
        assert (3, 4, 5) == a.m1(3, 4, 5)
        assert 3 == a.x
        assert 4 == a.y

        a = A()
        assert (0, 1, 2) == a.m2()
        assert 0 == a.x
        assert 1 == a.y

        a = A()
        assert (3, 1, 2) == a.m2(3)
        assert 0 == a.x
        assert 1 == a.y

        a = A()
        assert (3, 4, 2) == a.m2(3, 4)
        assert 0 == a.x
        assert 4 == a.y

        a = A()
        assert (3, 4, 5) == a.m2(3, 4, 5)
        assert 0 == a.x
        assert 4 == a.y
