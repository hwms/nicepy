# -*- coding: utf-8 *-*
from collections import Sequence
from operator import eq
from .helpers import get_failed_msg, get_multi_failed_msg
from nicepy.deep import get

__all__ = ['assert_equal_struct', 'multi_assert_equal_struct']


def assert_equal_struct(obj, expected_obj, namepaths=None, expected_namepaths=None, msg=None):
    """
    The values on *expected_obj* are equal to those from *obj*

    If *namepaths* is given, only those attributes are compared.

    If *namepaths* isn't given, it is assumed as:
    * *expected_obj*.keys() if *expected_obj* is a dict or
    * range(len(*expected_obj*) if *expected_obj is a Sequence else
    * *expected_obj*.__dict__.keys(), filtered by all names that don't start with underscore.

    If *expected_namepaths* is given, *namepaths* at *obj* are compared with *expected_namepaths* on
    *expected_obj* in same order.

    Utilizes nicepy.deep.get, so *namepaths* and *expected_namepaths* can stand for attributes, or
    keys of a dict, or even indizes as strings for a list.

    """
    is_sequence = isinstance(expected_obj, Sequence)

    if not namepaths:
        if isinstance(expected_obj, dict):
            namepaths = expected_obj.keys()
        elif is_sequence:
            namepaths = map(str, range(len(expected_obj)))
        else:
            namepaths = filter(lambda a: not a.startswith('_'), expected_obj.__dict__)

    values = get(obj, namepaths, one_as_tuple=True)

    if is_sequence and not expected_namepaths:
        expected_values = expected_obj[:len(namepaths)]
    else:
        expected_values = get(expected_obj, expected_namepaths or namepaths, one_as_tuple=True)

    standard_msg = get_failed_msg(eq, values, expected_values, namepaths, expected_namepaths)

    if standard_msg:
        raise AssertionError(msg or standard_msg)

def multi_assert_equal_struct(obj_list, expected_obj_list, namepaths=None, expected_namepaths=None,
                              msg=None):
    """
    Compare *obj_list* against *expected_obj_list* with *assert_equal_struct* at once.

    """
    standard_msg = get_multi_failed_msg(assert_equal_struct, obj_list, expected_obj_list,
                                        [namepaths] * len(obj_list),
                                        [expected_namepaths] * len(obj_list))

    if standard_msg:
        raise AssertionError(msg or standard_msg)
