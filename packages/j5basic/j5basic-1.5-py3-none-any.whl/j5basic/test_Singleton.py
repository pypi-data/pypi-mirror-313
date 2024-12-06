#!/usr/bin/env python

"""Tests the j5basic.Singleton implementation"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from . import Singleton
import gc
import types
from future.utils import with_metaclass

def test_basic():
    """Tests most basic singleton definition, that it works and constructing always produces the same result"""
    class Highlander(with_metaclass(Singleton.Singleton, object)):
        pass
    assert issubclass(Highlander, object)
    highlander = Highlander()
    assert isinstance(highlander, Highlander)
    highlander2 = Highlander()
    assert highlander2 is highlander

def test_non_oldstyle():
    """Tests that Singleton classes are implictly newstyle"""
    class Highlander(with_metaclass(Singleton.Singleton, object)):
        pass
    assert issubclass(Highlander, object)
    highlander = Highlander()
    assert isinstance(highlander, Highlander)
    highlander2 = Highlander()
    assert highlander2 is highlander

def test_subclass():
    """Tests that subclasses are distinct singletons"""
    class Highlander(with_metaclass(Singleton.Singleton, object)):
        pass
    class VeryHighlander(Highlander):
        pass
    assert issubclass(VeryHighlander, Highlander)
    assert issubclass(VeryHighlander, object)
    highlander = Highlander()
    assert isinstance(highlander, Highlander)
    veryhighlander = VeryHighlander()
    assert veryhighlander is not highlander
    veryhighlander2 = VeryHighlander()
    assert veryhighlander2 is veryhighlander

def test_deletion():
    """Tests that deletion and garbage collection don't destroy the singleton"""
    class Highlander(with_metaclass(Singleton.Singleton, object)):
        pass
    assert issubclass(Highlander, object)
    highlander = Highlander()
    highlander.value = 3
    assert isinstance(highlander, Highlander)
    highid = id(highlander)
    del highlander
    gc.collect()
    highlander2 = Highlander()
    assert id(highlander2) == highid
    assert highlander2.value == 3

def test_args_irrelevant():
    """Tests that arguments passed to the constructor don't have any effect after the initial construction"""
    class Highlander(with_metaclass(Singleton.Singleton, object)):
        def __init__(self, clan):
            self.clan = clan
    assert issubclass(Highlander, object)
    highlander = Highlander("McDonald")
    assert isinstance(highlander, Highlander)
    highlander2 = Highlander("BurgerKing")
    assert highlander2.clan == "McDonald"
    assert highlander2 is highlander

