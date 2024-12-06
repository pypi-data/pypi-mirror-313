from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import *
from j5basic import ObjTracker

def test_objtracker():
    ot = ObjTracker.ObjTracker()
    new_objects = []
    for i in range(10):
        new_objects.append({})

    ot.print_changes()