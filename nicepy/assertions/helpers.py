# -*- coding: utf-8 *-*
from collections import OrderedDict
from nicepy.utils import ljust_all, pretty_repr


def get_failed_msg(compare_method, values, expected_values, names=None, expected_names=None):
    failed_list = []
    names = names or map(str, range(len(values)))
    expected_names = expected_names or [''] * len(names)
    for value, expected_value, name, expected_name in zip(values, expected_values,
                                                          names, expected_names):
        #print value, expected_value, name, expected_name
        if not compare_method(expected_value, value):
            failed_list.append((pretty_repr(value), pretty_repr(expected_value),
                                name, expected_name))

    return _get_failed_msg(failed_list)

def _get_failed_msg(failed_list):
    if not failed_list:
        return None
    msg = 'actual values != expected values:'
    failed_list = zip(*map(ljust_all, zip(*failed_list)))
    for value_repr, expected_value_repr, name, expected_name in sorted(failed_list):
        msg += '\n\t%s' % name
        if expected_name:
            msg += ' != %s' % expected_name
        msg += ': %s != %s' % (value_repr, expected_value_repr)
    return msg

def get_multi_failed_msg(assert_method, *lists):
    failed_msgs = OrderedDict()
    for index, args in enumerate(zip(*lists)):
        try:
            assert_method(*args)
        except AssertionError as e:
            failed_msgs[index] = e.message
    msg = None
    if failed_msgs:
        msg = 'Multi-assert failed:'
        for index, error_msg in sorted(failed_msgs.iteritems()):
            msg += '\nIndex %d: %s' % (index, error_msg)
    return msg
