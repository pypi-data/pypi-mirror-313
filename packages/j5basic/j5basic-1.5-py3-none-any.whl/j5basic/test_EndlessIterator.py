# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import range
from builtins import *
from j5basic import EndlessIterator

def test_endless_iterator():
    it = EndlessIterator.EndlessIterator([0,1,2,3,4,5])
    for i in range(18):
        n = next(it)
        assert n == i % 6
