# -*- coding: utf-8 *-*
import inspect
from collections import OrderedDict

__all__ = ['showme']

def showme():
    frame = inspect.stack()[1][0]
    print '%s()' % inspect.getframeinfo(frame).function
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
    print '\n'.join(map(format_str.format, local_vars.items()))
