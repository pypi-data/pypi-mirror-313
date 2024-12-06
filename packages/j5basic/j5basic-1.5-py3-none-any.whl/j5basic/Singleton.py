#!/usr/bin/env python

"""Singleton metaclass implementation from http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
class Singleton(type):
    """Singleton metaclass; classes of this type will only ever create a single instance"""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

