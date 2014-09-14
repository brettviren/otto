#!/usr/bin/env python

import networkx as nx
from otto import proc
from otto.util import is_sequence

def noop(src, tgt, **kwds):
    return

def intern_task(task):
    if is_sequence(task):
        return [intern_task(t) for t in task]

    if callable(task):
        return task

    if isinstance(task, type("")):
        return proc.shell_task(task)

    if task is None:
        return noop

    raise TypeError, 'Unknown task type: %s' % repr(task)

def make_workflow(*edge_data):
    '''Return a workflow as a graph 

    The graph is made of the edge_data which must be of the form of a
    list of tuples:

      (tail, head, task, [params])

    The tail and head are state labels.

    The task is one of:

    - a string to be interpreted as a shell command

    - a callable to be interpreted as a workflow task function

    - a sequence composed of these

    - None interpreted to be a no-op

    The params element is optional and if given is a dictionary stored
    in the "params" element of the edge and will be added into the
    parameters passed to the task when it is executed.

    '''
    graph = nx.Graph()
    
    for ed in edge_data:
        src, tgt, task = ed[:3]
        edge_params = ed[3:] or dict()
        graph.add_edge(src, tgt, 
                       transition=intern_task(task), 
                       params = edge_params)
            
    return graph
