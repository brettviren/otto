#!/usr/bin/env python
'''
Otto's state machinery
'''

class StateStore(object):
    def __init__(self, value = None):
        self._state = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        print 'BI: Setting state: was="%s" now="%s"' % (self.state, value)
        self._state = value
    

class StateMachine(object):
    '''Otto's state machine expects a networkx graph as a workflow.

    The state None is reserved to indicate that the machine requires external resetting.

    Special edge attributes will be interpreted by the machine.  They
    may be a callable object or a sequence of callable objects:

    - before(source, **kwds) :: called just before leaving the current state

    - transition(source, target, **kwds) :: called to affect the transition, return values saved

    - after(target, values) :: called just after entering the target transition

    The kwds argument holds any node attributes belonging to the source node.

    '''

    def __init__(self, workflow, state=None, before=None, after=None, store = None):
        '''Create a state machine with the given workflow and initial state.

        If before or after are given they are considered globally
        applicable edge callable.

        '''
        self.workflow = workflow
        self._store = store or StateStore()
        self.state = state
        self.before = before
        self.after = after
        return

    @property
    def state(self):
        return self._store.state

    @state.setter
    def state(self, value):
        self._store.state = value

    def call_callables(self, corcc, *args, **kwds):
        '''
        Call a callable object or a collection of callable objects
        '''
        if corcc is None:
            return
        if callable(corcc):
            corcc = [corcc]
        return [c(*args, **kwds) for c in corcc]

    def goto(self, state, **kwds):
        '''Attempt to transition to the given state.

        Any kwds given will update any associated with the current
        node attributes before being passed to any edge callables.

        '''
        old_state = self.state
        new_state = state

        # if this fails, the SM keeps state
        edge = self.workflow[old_state][new_state]
        self.state = None       # at this point state is indeterminate
            
        params = dict(self.workflow.node[old_state])
        params.update(kwds)

        
        self.call_callables(self.before, old_state, **params)
        self.call_callables(edge.get('before',None), old_state, **params)
        value = self.call_callables(edge.get('transition', None), old_state, new_state, **params)
        self.call_callables(edge.get('after',None), new_state, value)
        self.call_callables(self.after, new_state, value)
        self.state = new_state
        return
