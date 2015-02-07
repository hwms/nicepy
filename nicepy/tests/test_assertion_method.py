# -*- coding: utf-8 *-*
import logging
from unittest import TestCase

from nicepy import assert_equal_struct, multi_assert_equal_struct, pretty_repr, permuteflat

log = logging.getLogger(__name__)


class Foo(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            self[k] = v

    def __setitem__(self, name, value):
        # helper to add attributes per self[attr] = value -> self.attr == value
        setattr(self, name, value)

    def __repr__(self):
        return pretty_repr(self, ignore_own_repr=True)


class TestAssertEqualStruct(TestCase):

    def run_assert(self, args, expected_msg=None):
        log.debug('args: %s' % str(args))

        msg = None
        try:
            assert_equal_struct(*args)
        except AssertionError as e:
            msg = e.message

        log.debug('msg: %s' % msg)
        self.assertEqual(msg, expected_msg)

    def check(self, actual_classes=(list,),
                    expected_classes=(list,),
                    expected_obj=None, expected_kwargs={},
                    working_obj=None, working_kwargs={},
                    failing_obj=None, failing_kwargs={},
                    failure_msg=None,
                    namepaths=None,
                    expected_namepaths=None):

        for actual_cls, expected_cls in permuteflat(actual_classes, expected_classes):
            expected_obj = expected_obj or expected_cls(**expected_kwargs)

            working_obj = working_obj or actual_cls(**working_kwargs)

            self.run_assert((working_obj, expected_obj, namepaths, expected_namepaths))

            failing_obj = failing_obj or actual_cls(**failing_kwargs)

            self.run_assert((failing_obj, expected_obj, namepaths, expected_namepaths),
                            failure_msg)

    def test_directly(self):
        """
        *assert_equal_struct* can compare similar flat structures directly.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs=dict(x=1),
                   working_kwargs=dict(x=1, y=2),
                   failing_kwargs=dict(x=3, y=2),
                   failure_msg='actual values != expected values:\n\tx: 3 != 1')

        self.check(expected_obj=[1],
                   working_obj=[1, 2],
                   failing_obj=[3, 2],
                   failure_msg='actual values != expected values:\n\t0: 3 != 1')

    def test_with_namepaths(self):
        """
        With namepaths *assert_equal_struct* can compare similar structures and structures with
        lists of values in full depth.

        This ignores all additional paths at the expected object.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs=dict(x=1, y=4),
                   namepaths=['x'],
                   working_kwargs=dict(x=1, y=2),
                   failing_kwargs=dict(x=3, y=2),
                   failure_msg='actual values != expected values:\n\tx: 3 != 1')

        self.check(actual_classes=(dict, Foo),
                   expected_obj=[1, 4],
                   namepaths=['x'],
                   working_kwargs=dict(x=1, y=2),
                   failing_kwargs=dict(x=3, y=2),
                   failure_msg='actual values != expected values:\n\tx: 3 != 1')

        self.check(expected_obj=[1, 4],
                   namepaths=['0'],
                   working_obj=[1, 2],
                   failing_obj=[3, 2],
                   failure_msg='actual values != expected values:\n\t0: 3 != 1')

    def test_with_namepaths_and_expected_namepaths(self):
        """
        Like just with namepaths, the values are sometimes at other paths at the expected object and
        will be compared using expected_namepaths in same order as namepaths.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs=dict(a=1, b=4),
                   namepaths=['x'],
                   expected_namepaths=['a'],
                   working_kwargs=dict(x=1, y=2),
                   failing_kwargs=dict(x=3, y=2),
                   failure_msg='actual values != expected values:\n\tx != a: 3 != 1')

        self.check(actual_classes=(dict, Foo),
                   expected_obj=[4, 1],
                   namepaths=['x'],
                   expected_namepaths=['1'],
                   working_kwargs=dict(x=1, y=2),
                   failing_kwargs=dict(x=3, y=2),
                   failure_msg='actual values != expected values:\n\tx != 1: 3 != 1')

        self.check(expected_obj=[4, 1],
                   namepaths=['0'],
                   expected_namepaths=['1'],
                   working_obj=[1, 2],
                   failing_obj=[3, 2],
                   failure_msg='actual values != expected values:\n\t0 != 1: 3 != 1')

class TestMultiAssertEqualStruct(TestCase):

    def run_assert(self, args, expected_msg=None):
        log.debug('args: %s' % str(args))

        msg = None
        try:
            multi_assert_equal_struct(*args)
        except AssertionError as e:
            msg = e.message

        log.debug('msg: %s' % msg)
        self.assertEqual(msg, expected_msg)

    def check(self, actual_classes=(list,),
                    expected_classes=(list,),
                    expected_objs=None, expected_kwargs_list=[],
                    working_objs=None, working_kwargs_list=[],
                    failing_objs=None, failing_kwargs_list=[],
                    failure_msg=None,
                    namepaths=None,
                    expected_namepaths=None):

        for actual_cls1, actual_cls2, expected_cls1, expected_cls2 in \
                permuteflat(*([actual_classes] * 2 + [expected_classes] * 2)):
            if not expected_objs:
                expected_objs = (expected_cls1(**expected_kwargs_list[0]),
                                  expected_cls2(**expected_kwargs_list[1]))

            if not working_objs:
                working_objs = (actual_cls1(**working_kwargs_list[0]),
                                 actual_cls2(**working_kwargs_list[1]))

            self.run_assert((working_objs, expected_objs, namepaths, expected_namepaths))

            if not failing_objs:
                failing_objs = (actual_cls1(**failing_kwargs_list[0]),
                                actual_cls2(**failing_kwargs_list[1]))

            self.run_assert((failing_objs, expected_objs, namepaths, expected_namepaths),
                            failure_msg)

    def test_directly(self):
        """
        *multi_assert_equal_struct* can compare multiple similar flat structures directly.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs_list=[dict(x=1), dict(x=2, y=3)],
                   working_kwargs_list=[dict(x=1, y=0), dict(x=2, y=3)],
                   failing_kwargs_list=[dict(x=4, y=0), dict(x=2, y=5)],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\tx: 4 != 1\n'\
                               'Index 1: actual values != expected values:\n\ty: 5 != 3')

        self.check(expected_objs=[[1], [2, 3]],
                   working_objs=[[1, 0], [2, 3]],
                   failing_objs=[[4, 0], [2, 5]],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\t0: 4 != 1\n'\
                               'Index 1: actual values != expected values:\n\t1: 5 != 3')

    def test_with_namepaths(self):
        """
        With namepaths *multi_assert_equal_struct* can compare multiple similar structures and
        structures with lists of values in full depth.

        This ignores all additional paths at the expected objects.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs_list=[dict(x=1), dict(x=2, y=3)],
                   working_kwargs_list=[dict(x=1, y=0), dict(x=2)],
                   failing_kwargs_list=[dict(x=4, y=0), dict(x=5)],
                   namepaths=['x'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\tx: 4 != 1\n'\
                               'Index 1: actual values != expected values:\n\tx: 5 != 2')

        self.check(actual_classes=(dict, Foo),
                   expected_objs=[[1], [2, 0]],
                   working_kwargs_list=[dict(x=1, y=5), dict(x=2)],
                   failing_kwargs_list=[dict(x=3, y=5), dict(x=4)],
                   namepaths=['x'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\tx: 3 != 1\n'\
                               'Index 1: actual values != expected values:\n\tx: 4 != 2')

        self.check(expected_objs=[[1], [2, 3]],
                   working_objs=[[1, 0], [2, 0]],
                   failing_objs=[[4, 0], [5, 0]],
                   namepaths=['0'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\t0: 4 != 1\n'\
                               'Index 1: actual values != expected values:\n\t0: 5 != 2')

    def test_with_namepaths_and_expected_namepaths(self):
        """
        Like just with namepaths, the values are sometimes at other paths at the expected object and
        will be compared using expected_namepaths in same order as namepaths.

        """
        self.check(actual_classes=(dict, Foo),
                   expected_classes=(dict, Foo),
                   expected_kwargs_list=[dict(y=1), dict(y=2, x=3)],
                   working_kwargs_list=[dict(x=1, y=0), dict(x=2)],
                   failing_kwargs_list=[dict(x=4, y=0), dict(x=5)],
                   namepaths=['x'],
                   expected_namepaths=['y'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\tx != y: 4 != 1\n'\
                               'Index 1: actual values != expected values:\n\tx != y: 5 != 2')

        self.check(actual_classes=(dict, Foo),
                   expected_objs=[[0, 1], [0, 2]],
                   working_kwargs_list=[dict(x=1, y=5), dict(x=2)],
                   failing_kwargs_list=[dict(x=3, y=5), dict(x=4)],
                   namepaths=['x'],
                   expected_namepaths=['1'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\tx != 1: 3 != 1\n'\
                               'Index 1: actual values != expected values:\n\tx != 1: 4 != 2')

        self.check(expected_objs=[[1, 2], [3, 4]],
                   working_objs=[[2, 1], [4, 3]],
                   failing_objs=[[2, 5], [6, 3]],
                   namepaths=['0', '1'],
                   expected_namepaths=['1', '0'],
                   failure_msg='Multi-assert failed:\n' \
                               'Index 0: actual values != expected values:\n\t1 != 0: 5 != 1\n'\
                               'Index 1: actual values != expected values:\n\t0 != 1: 6 != 4')
