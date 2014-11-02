__author__ = 'pzdeb'

import re


def remove_xdc(text):
    def replacer(c):
        cr = eval("b'\\x%s\\x%s'" % c.groups()).decode('utf8')
        return cr
    fixed_text = re.sub(r'\\udc([a-f0-9]{2})\\udc([a-f0-9]{2})', replacer, repr(text))
    return fixed_text[1:-1]

