#!/usr/bin/env python
'''
Otto's state machinery
'''

class StateMachine(object):
    '''Otto's state machine operates on a workflow which should look like a networkx graph.

    The state None is reserved to indicate that the machine requires external resetting.

    Machine parameters may be given and will be treated as opaque.

    Special edge attributes will be interpreted by the machine.  They
    may be a callable object or a sequence of callable objects:

    - before(source, **kwds) :: called just before leaving the current state

    - transition(source, target, **kwds) :: called to affect the
      transition, return values saved

    - after(target, values, **kwds) :: called just after entering the
      target transition, any return value which is a dictionary will
      be used to update the state machine parameters.

    The kwds argument holds any node attributes belonging to the source node.

    '''

    def __init__(self, workflow, state=None, before=None, after=None, **params):
        '''Create a state machine with the given workflow and initial state.

        If before or after are given they are considered globally
        applicable edge callable.

        '''
        self.workflow = workflow
        self._state = None
        self.params = params
        self.state = state
        self.before = before
        self.after = after
        return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self.jump(value)

    def jump(self, state):
        '''
        Jump directly to given state without transition.
        '''
        self._state = state


    def call_callables(self, corcc, *args, **kwds):
        '''
        Call a callable object or a collection of callable objects
        '''
        if corcc is None:
            return
        if callable(corcc):
            corcc = [corcc]

        ret = list()
        for i,c in enumerate(corcc):
            print 'Calling[%d]: %s' % (i,c)
            res = c(*args, **kwds)
            ret.append(res)
        return ret

    def goto(self, state, **kwds):
        '''Attempt to transition to the given state.

        Any kwds given will update any associated with the current
        node attributes before being passed to any edge callables.

        '''
        old_state = self.state
        new_state = state

        print 'Attempt to go from "%s" to "%s"' % (old_state, new_state)

        # if this fails, the SM keeps state
        edge = self.workflow[old_state][new_state]
        self.state = None       # at this point state is indeterminate
            
        print 'EDGE:', edge
        print 'EDGES:', self.workflow.edge

        params = dict(self.workflow.node[old_state])
        params.update(edge.get('params',dict()))
        params.update(self.params)
        params.update(kwds)

        print 'Calling global before'
        self.call_callables(self.before, old_state, **params)
        print 'Calling edge before'
        self.call_callables(edge.get('before',None), old_state, **params)

        trans = edge.get('transition', None)
        print 'Calling edge transition: %s' % str(trans)

        value = self.call_callables(trans, old_state, new_state, **params)
        print '\tgot: %s' % str(value)
        print 'Calling edge after'
        new_params = self.call_callables(edge.get('after',None), new_state, value, **params)
        if isinstance(new_params, dict):
            self.params.update(new_params)
        print 'Calling global after'
        new_params = self.call_callables(self.after, new_state, value, **params)
        if isinstance(new_params, dict):
            self.params.update(new_params)

        self.state = new_state
        return

import shelve

class PersistentStateMachine(StateMachine):
    
    def __init__(self, state_store_filename, workflow=None, state=None, before=None, after=None, **params):

        self._shelf = shelve.open(state_store_filename)

        #if workflow is None:
        #    workflow = self._shelf.get('workflow', None)
        #    print ('Using nodes from shelf: "%s"' % ', '.join([str(n) for n in workflow.node.keys()]))
        #else:
        #    print ('Using passed in nodes: "%s"' % ', '.join([str(n) for n in workflow.node.keys()]))

        if state is None:
            state = self._shelf.get('state', None)
            print ('No state given, using from shelf: "%s"' % state)
        else:
            print ('Using passed in state: "%s"' % state)

        if not params:
            params = self._shelf.get('params', dict())
            print ('No params given, using from shelf: "%s"' % str(params))
        else:
            print ('Using passed in parameters: "%s"' % str(params))

        super(PersistentStateMachine, self).__init__(workflow, state, before, after, **params)
        self.sync()

    def jump(self, state):
        '''
        Jump directly to given state without transition.
        '''
        self._state = state
        self.sync()

    def sync(self):
        '''
        Sync the to the persistent file.  This is needed if, eg, self.params are modified in place.
        '''
        self._shelf['state'] = self._state
        self._shelf['params'] = self.params
        #self._shelf['workflow'] = self.workflow
        self._shelf.sync()

        #print ('PersistentStateMachine: syncing with %d params, nodes="%s"' % (len(self.params), ', '.join([str(n) for n in self.workflow.node.keys()])))
