from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from j5basic import OrderedSet

def test_ordered_set():
    os = OrderedSet.OrderedSet()
    os.extend([1,2,3])
    os.update([4,5,6])
    os.append(7)
    os.add(8)
    os.remove(2)
    del os[4]
    assert list(os) == [1,3,4,5,7,8]