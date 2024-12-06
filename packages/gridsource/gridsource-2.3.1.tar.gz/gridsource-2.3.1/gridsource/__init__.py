# -*- coding: utf-8 -*-

"""Top-level package for GridSource."""

from gridsource.io import IOMixin
from gridsource.validation import ValidatorMixin

__author__ = """Nicolas Cordier"""
__email__ = "nicolas.cordier@numeric-gmbh.ch"
__version__ = "2.3.1"


class _Base:
    def __init__(self):
        self._data = {}
        possible_mixins_init = ("validator_mixin_init", "io_mixin_init")
        for f in possible_mixins_init:
            if hasattr(self, f):
                getattr(self, f)()

    def get(self, tabname=None, attr="_data", remove_hidden_cols=True):
        if not attr.startswith("_"):
            attr = "_" + attr
        if not tabname:
            raise AttributeError(f"`tabname` should be one of {set(self._data.keys())}")
        if tabname not in self.tabs():
            return None
        data = getattr(self, attr)[tabname]
        if attr == "_data" and remove_hidden_cols:
            # early remove __<col>
            data = data.loc[:, ~data.columns.str.startswith("__")]
        return data

    def tabs(self, ordered=False):
        """return contained tabs"""
        if not ordered:
            return set(getattr(self, "_data").keys())
        return list(getattr(self, "_data").keys())

    def keys(self, ordered=False):
        """alias for self.tabs()"""
        return self.tabs(ordered=ordered)


class Data(_Base, IOMixin, ValidatorMixin):
    pass


class ValidData(_Base, ValidatorMixin):
    pass


class IOData(_Base, IOMixin):
    pass
