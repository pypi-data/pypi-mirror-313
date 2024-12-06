#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 16:51
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .var_main import MortalVarMain


class MortalVar(MortalVarMain):
    def __init__(self, reprint=False, inherit=False, **kwargs):
        self._set_class(MortalVar, reprint, inherit)
        self._mv_add(kwargs)

    def add(self, **kwargs):
        self._mv_add(kwargs)

    def add_list(self, *args):
        self._mv_add_list(args)

    def pop(self, name):
        self._mv_pop(name)

    def pops(self, *args):
        self._mv_pops(args)

    def set(self, name, value, inherit=False):
        self._mv_set(name, value, inherit)

    def set_kwargs(self, **kwargs):
        self._mv_set_kwargs(kwargs)

    def clear(self):
        self._mv_clear()

    def get(self, *args):
        return self._mv_get(args)

    def keys(self):
        return self._mv_keys()

    def items(self):
        return self._mv_items()

    def todict(self, sort=False):
        return self._mv_to_dict(sort)

    def to_params(self):
        return self._mv_to_params()

    def to_string(self):
        return self._mv_to_string()
