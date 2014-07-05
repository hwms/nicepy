# -*- coding: utf-8 *-*
import operator
from .get import Get
from .compare import Compare

get = Get()
not_ = Get(negate=True)

lt = Compare(operator.lt)
nlt = Compare(operator.lt, negate=True)
le = Compare(operator.le)
nle = Compare(operator.le, negate=True)
gt = Compare(operator.gt)
ngt = Compare(operator.gt, negate=True)
ge = Compare(operator.ge)
nge = Compare(operator.ge, negate=True)
eq = Compare(operator.eq)
neq = Compare(operator.ne)
is_ = Compare(operator.is_)
nis = Compare(operator.is_not)
in_ = Compare(lambda a, b: a in b)
nin = Compare(lambda a, b: a not in b)
instance = Compare(lambda a, b: isinstance(a, b))
not_instance = Compare(lambda a, b: not isinstance(a, b))
