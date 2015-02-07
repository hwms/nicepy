# -*- coding: utf-8 *-*

__all__ = ['NOT_SET']

class NotSet(object):
    """
    Object to be used for optional arguments, where None or False can be correct values.
    """
    def __str__(self):
        return 'NOT_SET'
NOT_SET = NotSet()

_DEBUG = False

def _get(obj, name, default=NOT_SET):
    if _DEBUG: print('_get(%s, "%s", default=%s)' % (obj, name, default))
    if name == '':
        if _DEBUG: print('direct')
        return obj
    try:
        if isinstance(obj, dict):
            if _DEBUG: print('dict', obj[name])
            return obj[name]
        if name.isdigit():
            if _DEBUG: print('list', obj[int(name)])
            return obj[int(name)]
        if _DEBUG: print('getattr', getattr(obj, name))
        return getattr(obj, name)
    except (AttributeError, IndexError, KeyError) as e:
        if default == NOT_SET:
            raise e
        if _DEBUG: print('default', default)
        return default

def deep_names_get(obj, names, index=0, default=NOT_SET):
    name = names[index]
    val = _get(obj, name, default)

    if index + 1 == len(names):
        return val

    sub_call = lambda v: deep_names_get(v, names, index + 1, default=default)

    # TODO: explore posibility for using maybe * as cascadingly return all from iterables
    #    if handle_iterables and isinstance(val, collections.Iterable):
    #        return list(itertools.chain(map(sub_call, val)))

    return sub_call(val)

def deep_path_get(obj, path, default=NOT_SET):
    return deep_names_get(obj, path.split('.'), default=default)

def deep_get(obj, paths='', default=NOT_SET, one_as_tuple=False):
    """
    Return result of getattr with same call syntax.

    paths can either be a single path string or multiple ones as tuple/ whitespace seperated.

    If *path* contains multiple names separated by dots '.' the result should be the same as if
    python tries to solve the attributes.

    If default is set, any exception will be handled.

    If a name apears to be an integer, assume this is the index of an indexable type of object.

    """
    if isinstance(paths, str):
        paths = paths.split(' ')
    values = [deep_path_get(obj, p, default=default) for p in paths]
    if len(paths) == 1 and not one_as_tuple:
        return values[0]
    return tuple(values)

class GetBase(object):
    def __init__(self, negate=False):
        self.negate = negate

    def _get(self, obj, paths='', default=NOT_SET, one_as_tuple=False):
        return deep_get(obj, paths, default, one_as_tuple)

    def _optional_negated(self, value):
        if self.negate:
            return not value
        return value
