# -*- coding: utf-8 *-*
from .base import GetBase, NOT_SET

class Get(GetBase):
    def get(self, obj, paths='', default=NOT_SET, one_as_tuple=False):
        value = self._get(obj, paths, default, one_as_tuple)
        return self._optional_negated(value)

    __call__ = get

    def safe(self, obj, paths='', one_as_tuple=False):
        return self(obj, paths, default=None, one_as_tuple=one_as_tuple)

    def cget(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cget(obj):
            return self.get(obj, paths, default, one_as_tuple)
        return cget

    def csafe(self, paths='', one_as_tuple=False):
        return self.cget(paths, default=None, one_as_tuple=one_as_tuple)

    def getg(self, single_object_generator, paths='', default=NOT_SET, one_as_tuple=False):
        return self.get(single_object_generator(), paths, default, one_as_tuple)

    def safeg(self, single_object_generator, paths='', one_as_tuple=False):
        return self.getg(single_object_generator, paths, default=None, one_as_tuple=one_as_tuple)

    def cgetg(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cgetg(single_object_generator):
            return self.get(single_object_generator, paths, default, one_as_tuple)
        return cgetg

    def csafeg(self, paths='', one_as_tuple=False):
        return self.cgetg(paths, default=None, one_as_tuple=one_as_tuple)


    def map(self, objects, paths='', default=NOT_SET, one_as_tuple=False):
        cget = self.cget(paths, default, one_as_tuple)
        return map(cget, objects)

    def safe_map(self, objects, paths='', one_as_tuple=False):
        return self.map(objects, paths, default=None, one_as_tuple=one_as_tuple)

    def cmap(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cmap(objects):
            return self.map(objects, paths, default, one_as_tuple)
        return cmap

    def safe_cmap(self, paths='', one_as_tuple=False):
        return self.cmap(paths, default=None, one_as_tuple=one_as_tuple)

    def mapg(self, objects_generator, paths='', default=NOT_SET, one_as_tuple=False):
        return self.map(objects_generator(), paths, default, one_as_tuple)

    def safe_mapg(self, objects_generator, paths='', one_as_tuple=False):
        return self.mapg(objects_generator, paths, default=None, one_as_tuple=one_as_tuple)

    def cmapg(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cmapg(objects_generator):
            return self.mapg(objects_generator, paths, default, one_as_tuple)
        return cmapg

    def safe_cmapg(self, paths='', one_as_tuple=False):
        return self.cmapg(paths, default=None, one_as_tuple=one_as_tuple)


    def dict(self, objects, paths='', default=NOT_SET, one_as_tuple=False):
        objects = list(objects)
        return dict(zip(self.map(objects, paths, default, one_as_tuple), objects))

    def safe_dict(self, objects, paths='', one_as_tuple=False):
        return self.dict(objects, paths, default=None, one_as_tuple=one_as_tuple)

    def cdict(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cdict(objects):
            return self.dict(objects, paths, default, one_as_tuple)
        return cdict

    def safe_cdict(self, paths='', one_as_tuple=False):
        return self.cdict(paths, default=None, one_as_tuple=one_as_tuple)

    def dictg(self, objects_generator, paths='', default=NOT_SET, one_as_tuple=False):
        return self.dict(objects_generator(), paths, default, one_as_tuple)

    def safe_dictg(self, objects_generator, paths='', one_as_tuple=False):
        return self.dictg(objects_generator, paths, default=None, one_as_tuple=one_as_tuple)

    def cdictg(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cdictg(objects_generator):
            return self.dictg(objects_generator, paths, default, one_as_tuple)
        return cdictg

    def safe_cdictg(self, paths='', one_as_tuple=False):
        return self.cdictg(paths, default=None, one_as_tuple=one_as_tuple)


    def filter(self, objects, paths='', default=NOT_SET, one_as_tuple=False):
        cget = self.cget(paths, default, one_as_tuple)
        return filter(cget, objects)

    def safe_filter(self, objects, paths='', one_as_tuple=False):
        cget = self.cget(paths, default=None, one_as_tuple=one_as_tuple)
        return filter(cget, objects)

    def cfilter(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cfilter(objects):
            return self.dict(objects, paths, default, one_as_tuple)
        return cfilter

    def safe_cfilter(self, paths='', one_as_tuple=False):
        return self.cfilter(paths, default=None, one_as_tuple=one_as_tuple)

    def filterg(self, objects_generator, paths='', default=NOT_SET, one_as_tuple=False):
        return self.filter(objects_generator(), paths, default, one_as_tuple)

    def safe_filterg(self, objects_generator, paths='', one_as_tuple=False):
        return self.filterg(objects_generator, paths, default=None, one_as_tuple=one_as_tuple)

    def cfilterg(self, paths='', default=NOT_SET, one_as_tuple=False):
        def cfilterg(objects_generator):
            return self.filterg(objects_generator, paths, default, one_as_tuple)
        return cfilterg

    def safe_cfilterg(self, paths='', one_as_tuple=False):
        return self.cfilterg(paths, default=None, one_as_tuple=one_as_tuple)
