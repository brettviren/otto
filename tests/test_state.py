#!/usr/bin/env python
'''
test otto.state
'''

import os
import otto.state
import networkx as nx

def chirp(*args, **kwds):
    print ('\targs: %s' % ', '.join(['%s'%a for a in args]))
    print ('\tkwds: %s' % ', '.join(['%s:%s' % kv for kv in kwds.items()]))


def before(*args, **kwds):
    print ('before:')
    chirp(*args, **kwds)

def after(*args, **kwds):
    print ('after:')
    chirp(*args, **kwds)

def move(s, t, **kwds):
    print ('move: %s --> %s with %s' % (s,t,', '.join(['%s:%s' % kv for kv in kwds.items()])))
    return 42

def barf(s, t, **kwds):
    if 'barf' in kwds:
        raise RuntimeError, kwds['barf']
    return 9

def test_nominal():
    g = nx.Graph()
    g.add_edge(1, 2, transition=move, before=before, after=after)
    g.add_edge(1, 3, transition=move, before=before, after=after)
    g.add_edge(2, 3, transition=move, before=before, after=after)
    g.add_edge(2, 4, transition=move, before=before, after=after)
    g.add_edge(3, 4, transition=move, before=before, after=after)
    g.add_node(1, a=10,b=20)

    sm = otto.state.StateMachine(g)
    sm.state = 1
    print 'state:', sm.state
    sm.goto(2)
    print 'state:', sm.state
    sm.goto(3)
    print 'state:', sm.state
    sm.goto(4)
    
def test_failure():    
    g = nx.Graph()
    g.add_edge(1, 2, transition=barf, before=before, after=after)
    g.add_edge(1, 3, transition=barf, before=before, after=after)
    g.add_edge(2, 3, transition=barf, before=before, after=after)
    g.add_edge(2, 4, transition=barf, before=before, after=after)
    g.add_edge(3, 4, transition=barf, before=before, after=after)
    g.add_node(1, a=10,b=20)
    g.add_node(3, barf='Force a failure')

    sm = otto.state.StateMachine(g)
    sm.state = 1
    print 'state:', sm.state
    sm.goto(2)
    print 'state:', sm.state
    sm.goto(3)
    print 'state:', sm.state
    try:
        sm.goto(4)
    except RuntimeError,msg:
        print ('Caught expected exception, state is: %s' % sm.state)
    else:
        raise RuntimeError, 'We should have got a RuntimeError'

def test_smart_state():
    class SmartStateStore(object):
        def __init__(self, value = None):
            self._state = value

        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value):
            self._state = value
        
    g = nx.Graph()
    g.add_edge(1, 2, transition=move, before=before, after=after)
    g.add_edge(1, 3, transition=move, before=before, after=after)
    g.add_edge(2, 3, transition=move, before=before, after=after)
    g.add_edge(2, 4, transition=move, before=before, after=after)
    g.add_edge(3, 4, transition=move, before=before, after=after)
    g.add_node(1, a=10,b=20)

    ss = SmartStateStore(42)
    sm = otto.state.StateMachine(g, store = ss)

    sm.state = 1
    print 'state:', sm.state, ss.state
    assert sm.state is ss.state

    sm.goto(2)
    print 'state:', sm.state, ss.state
    assert sm.state is ss.state

    sm.goto(3)
    print 'state:', sm.state, ss.state
    assert sm.state is ss.state


