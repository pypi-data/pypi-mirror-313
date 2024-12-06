#!/usr/bin/env python

"""this is an iterator wrapper that allows things to be pushed back"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import *
from builtins import object
class PushBack(object):
    def __init__(self, iterator):
        self.iterator = iterator
        self.pushedback = []

    def __iter__(self):
        return self

    def pushback(self, item):
        self.pushedback.append(item)

    def __next__(self):
        if self.pushedback:
            return self.pushedback.pop(0)
        else:
            return next(self.iterator)

class PushToBack(object):
    def __init__(self, iterator):
        self.iterator = iterator
        self.pushedtoback = []
        self.iterator_done = False

    def __iter__(self):
        return self

    def pushback(self, item):
        self.pushedtoback.append(item)

    def __next__(self):
        if not self.iterator_done:
            try:
                return next(self.iterator)
            except StopIteration:
                self.iterator_done = True
        if len(self.pushedtoback):
            return self.pushedtoback.pop(0)
        raise StopIteration()

