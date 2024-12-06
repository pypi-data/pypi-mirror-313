# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from j5basic import Colours

def test_generate_colours():
    colours = Colours.get_colours(10)
    assert len(colours) == 10
    assert len(set([tuple(c) for c in colours])) == 10
    colours = Colours.get_colours(2)
    assert len(colours) == 2
    assert len(set([tuple(c) for c in colours])) == 2

