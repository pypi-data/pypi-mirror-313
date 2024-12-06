#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for design pattern utilities"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Copyright 2006 St James Software

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import *
from builtins import object
from j5basic import DesignPatterns
import threading

class TestMultiton(object):
    def test_creation(self):
        class Foo(DesignPatterns.Multiton):
            pass

        o1 = Foo(1,2)
        o2 = Foo(3,4)
        o3 = Foo(1,2)

        assert id(o1) == id(o3)
        assert id(o1) != id(o2)

    def test_threaded_creation(self):
        OBJECTS = 40
        THREADS = 5

        class Foo(DesignPatterns.Multiton):
            pass

        results = {}
        def worker_process():
            for i in range(OBJECTS):
                o = Foo("a",i)
                objs = results.setdefault(i,[])
                objs.append(o)

        threads = []
        for i in range(THREADS):
            threads.append(threading.Thread(target=worker_process))

        for thrd in threads:
            thrd.start()

        for thrd in threads:
            thrd.join()

        for objs in list(results.values()):
            assert len(objs) == THREADS
            for i in range(len(objs) - 1):
                assert id(objs[i]) == id(objs[i+1])
