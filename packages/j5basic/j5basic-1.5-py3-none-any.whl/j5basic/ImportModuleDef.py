from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
__author__ = 'matth'

def import_def_from(other_module_name, myvars):
    for key, val in vars(__import__(other_module_name)).items():
        if key.startswith('__') and key.endswith('__'):
            continue
        myvars[key] = val