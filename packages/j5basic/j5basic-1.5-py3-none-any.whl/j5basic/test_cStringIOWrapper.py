from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from j5basic import cStringIOWrapper

def test_wrapper():
    myio = cStringIOWrapper.StringIO()
    myio.write('Testing\n')
    myio.writelines(['This\n', 'Class\n'])
    myio.flush()
    myio.close()