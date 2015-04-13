"""

Python 2/3 Compatibility
========================

Not sure we need to support anything but Python 2.7 at this point , but copied
this module over from flask-peewee for the time being.

"""

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr
    reduce = reduce
else:
    text_type = str
    string_types = (str, )
    unichr = chr
    from functools import reduce
