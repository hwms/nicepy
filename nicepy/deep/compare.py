# -*- coding: utf-8 *-*
from .base import GetBase, NOT_SET

class Compare(GetBase):
    def __init__(self, compare_method=None, negate=False):
        super(Compare, self).__init__(negate=negate)
        self.compare_method = compare_method

    def get(self, obj, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        value = self._get(obj, paths, default, one_as_tuple)
        value = self.compare_method(value, comparable)
        return self._optional_negated(value)

    __call__ = get

    def safe(self, obj, comparable, paths='', one_as_tuple=False):
        return self.get(obj, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cget(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def getter(obj):
            return self.get(obj, comparable, paths, default, one_as_tuple)
        return getter

    def csafe(self, comparable, paths='', one_as_tuple=False):
        return self.cget(comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def getg(self, single_object_generator, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        return self.get(single_object_generator(), comparable, paths, default, one_as_tuple)

    def safeg(self, single_object_generator, comparable, paths='', one_as_tuple=False):
        return self.getg(single_object_generator, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cgetg(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cgetg(single_object_generator):
            return self.get(single_object_generator, comparable, paths, default, one_as_tuple)
        return cgetg

    def csafeg(self, comparable, paths='', one_as_tuple=False):
        return self.cgetg(comparable, paths, default=None, one_as_tuple=one_as_tuple)


    def map(self, objects, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        cget = self.cget(comparable, paths, default, one_as_tuple)
        return map(cget, objects)

    def safe_map(self, objects, comparable, paths='', one_as_tuple=False):
        return self.map(objects, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cmap(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cmap(objects):
            return self.map(objects, comparable, paths, default, one_as_tuple)
        return cmap

    def safe_cmap(self, comparable, paths='', one_as_tuple=False):
        return self.cmap(comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def mapg(self, objects_generator, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        return self.map(objects_generator(), paths, default, one_as_tuple)

    def safe_mapg(self, objects_generator, comparable, paths='', one_as_tuple=False):
        return self.mapg(objects_generator, paths, default=None, one_as_tuple=one_as_tuple)

    def cmapg(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cmapg(objects_generator):
            return self.mapg(objects_generator, comparable, paths, default, one_as_tuple)
        return cmapg

    def safe_cmapg(self, comparable, paths='', one_as_tuple=False):
        return self.cmapg(comparable, paths, default=None, one_as_tuple=one_as_tuple)


    def dict(self, objects, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        objects = list(objects)
        return dict(zip(self.map(objects, comparable, paths, default, one_as_tuple), objects))

    def safe_dict(self, objects, comparable, paths='', one_as_tuple=False):
        objects = list(objects)
        return self.dict(objects, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cdict(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cdict(objects):
            return self.dict(objects, comparable, paths, default, one_as_tuple)
        return cdict

    def safe_cdict(self, comparable, paths='', one_as_tuple=False):
        return self.cdict(comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def dictg(self, objects_generator, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        return self.dict(objects_generator(), comparable, paths, default, one_as_tuple)

    def safe_dictg(self, objects_generator, comparable, paths='', one_as_tuple=False):
        return self.dictg(objects_generator, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cdictg(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cdictg(objects_generator):
            return self.dictg(objects_generator, comparable, paths, default, one_as_tuple)
        return cdictg

    def safe_cdictg(self, comparable, paths='', one_as_tuple=False):
        return self.cdictg(comparable, paths, default=None, one_as_tuple=one_as_tuple)


    def filter(self, objects, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        cget = self.cget(comparable, paths, default, one_as_tuple)
        return filter(cget, objects)

    def safe_filter(self, objects, comparable, paths='', one_as_tuple=False):
        cget = self.cget(comparable, paths, default=None, one_as_tuple=one_as_tuple)
        return filter(cget, objects)

    def cfilter(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cfilter(objects):
            return self.dict(objects, comparable, paths, default, one_as_tuple)
        return cfilter

    def safe_cfilter(self, comparable, paths='', one_as_tuple=False):
        return self.cfilter(comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def filterg(self, objects_generator, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        return self.filter(objects_generator(), comparable, paths, default, one_as_tuple)

    def safe_filterg(self, objects_generator, comparable, paths='', one_as_tuple=False):
        return self.filterg(objects_generator, comparable, paths, default=None, one_as_tuple=one_as_tuple)

    def cfilterg(self, comparable, paths='', default=NOT_SET, one_as_tuple=False):
        def cfilterg(objects_generator):
            return self.filterg(objects_generator, comparable, paths, default, one_as_tuple)
        return cfilterg

    def safe_cfilterg(self, comparable, paths='', one_as_tuple=False):
        return self.cfilterg(comparable, paths, default=None, one_as_tuple=one_as_tuple)
