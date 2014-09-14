#!/usr/bin/env python
'''
Various utility functions.
'''

import re

def mgetter(callable):
    def f(match):
        key = match.group(1)
        val = callable(key,'{'+key+'}')
        return val
    return f

subn_reobj = re.compile(r'{(\w+)}')
def format_get(string, getter):
    '''Format <string> using the function <getter(key, default)> which
    returns the value for the <key> or <default> if not found.
    '''
    ret = re.subn(subn_reobj, mgetter(getter), string)
    return ret[0]

def format(string, **kwds):
    while True:
        new_string = format_get(string, kwds.get)
        if new_string == string:
            return new_string
        string = new_string

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))        
