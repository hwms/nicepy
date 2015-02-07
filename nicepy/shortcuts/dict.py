# -*- coding: utf-8 *-*
from __future__ import absolute_import
import itertools

__all__ = ['dict_items_map', 'items_map']

def dict_items_map(func, dct):
    return items_map(dct.iteritems())

def items_map(func, items):
    return list(itertools.starmap(func, items))
