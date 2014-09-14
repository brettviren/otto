#!/usr/bin/env python
'''
test otto.util
'''
from otto.util import format, format_get


def test_format():
    kwds = dict(a='one', b='two{c}two', c=" see ")
    
    trials_get = [
        ('{a}_{b}', 'one_two{c}two'),
    ]

    trials = [
        ('{a}_{b}', 'one_two see two'),
    ]
    

    for give, want in trials_get:
        got = format_get(give, kwds.get)
        assert want == got, 'Want: "%s", got: "%s"' % (want, got)
        print got

    for give, want in trials:
        got = format(give, **kwds)
        assert want == got, 'Want: "%s", got: "%s"' % (want, got)
        print got
