# -*- coding: utf-8 -*-

"""Provides a generator which takes a list and repeats teh list endlessly"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
def EndlessIterator(baselist):
    while True:
        for item in baselist:
            yield item


