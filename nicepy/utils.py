from __future__ import absolute_import
import inspect
from collections import OrderedDict
from datetime import datetime

__all__ = ['ljust_all', 'showme', 'permuteflat', 'pretty_repr', 'rjust_all']

def showme():
    frame = inspect.stack()[1][0]
    print('%s()' % inspect.getframeinfo(frame).function)
    arginfo = inspect.getargvalues(frame)

    local_vars = arginfo.locals
    if 'self' in local_vars:
        local_vars = OrderedDict()
        self_var = local_vars['self'] = arginfo.locals['self']
        for k, v in self_var.__dict__.items():
            local_vars['self.' + k] = v
        for k, v in arginfo.locals.items():
            if not k == 'self':
                local_vars[k] = v

    format_str = '\t{0[0]:<%d} = {0[1]}' % max(map(len, local_vars.keys()))
    print('\n'.join(map(format_str.format, local_vars.items())))


def permuteflat(*args):
    """
    Returns a list with all combinations of elements between all sequences.

    Example:
        seq_a = [1, 2, 3]
        seq_b = [4, 5]
        seq_c = [6, 7]
        permuted = sorted(util.permuteflat(seq_a,seq_b,seq_c))
        permuted == [(1, 4, 6), (1, 4, 7), (1, 5, 6), (1, 5, 7),
                     (2, 4, 6), (2, 4, 7), (2, 5, 6), (2, 5, 7),
                     (3, 4, 6), (3, 4, 7), (3, 5, 6), (3, 5, 7)]

    from: http://code.activestate.com/recipes/65285-looping-through-multiple-lists/

    """
    # make shure iterators and sets are converted in lists
    args = map(list, args)
    outs = []
    olen = 1
    tlen = len(args)
    for seq in args:
        olen = olen * len(seq)
    for i in range(olen):
        outs.append([None] * tlen)
    plq = olen
    for i in range(len(args)):
        seq = args[i]
        plq = plq / len(seq)
        for j in range(olen):
            si = (j / plq) % len(seq)
            outs[j][i] = seq[si]
    for i in range(olen):
        outs[i] = tuple(outs[i])
    return outs


def pretty_repr(value, ignore_own_repr=False):
    """
    Wrapper for repr to prettify some types for easy copy paste.

    For classes use:
        def __repr__(self):
            return pretty_repr(self, ignore_own_repr=True)

    """
    if not ignore_own_repr and hasattr(value, '__repr__'):
        return value.__repr__()
    if isinstance(value, unicode):
        try:
            # try to avoid u char if a non unicode string is all we need
            return repr(str(value))
        except UnicodeEncodeError:
            return repr(value)
    if isinstance(value, long):
        # don't output L char
        return '%d' % value
    if isinstance(value, datetime):
        # strip the datetime module, because we mostly use from imports
        return repr(value).split('.')[1]
    if hasattr(value, '__dict__'):
        kwargs_str = ', '.join(map(lambda i: '%s=%s' % (i[0], pretty_repr(i[1])),
                                   sorted(value.__dict__.iteritems())))

        return '%s(%s)' % (value.__class__.__name__, kwargs_str)
    return repr(value)


def rjust_all(strings, fillchar=' '):
    """
    Determine max length of all *strings* and apply rjust to all of them.

    Example: rjust_all(('a','bb',''))
    [' a', 'bb', '  ']

    """
    width = max(map(len, strings))
    return [s.rjust(width, fillchar) for s in strings]


def ljust_all(strings, fillchar=' '):
    """
    Determine max length of all *strings* and apply ljust to all of them.

    Example: ljust_all(('a','bb',''))
    ['a ', 'bb', '  ']

    """
    width = max(map(len, strings))
    return [s.ljust(width, fillchar) for s in strings]
