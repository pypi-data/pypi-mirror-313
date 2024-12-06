from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from j5basic import CleanXHTML

DIRTY_XHTML = """
Testing fragment<br/>
<span id="this_is_a_great_id" class="MYCLASS" style="badstyle" lang="en-inve-us">TEXT</span>
<span/>
"""

def test_clean_html():
    cleaned_html = CleanXHTML.clean_html(DIRTY_XHTML)
    assert cleaned_html == "\nTesting fragment<br/>\nTEXT\n\n"
