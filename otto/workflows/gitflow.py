#!/usr/bin/env python
'''
An Otto workflow using gitflow
'''
import os
import networkx as nx
from subprocess import check_call

def cmd(cmdstr):
    def task(srcnode, tgtnode, **kwds):
        cwd = kwds.pop('cwd','.')
        cwd = cwd.format(**kwds)
        fcmdstr = cmdstr.format(cwd=cwd, **kwds)
        print 'Running command: "%s" in directory: %s' % (fcmdstr, cwd)
        check_call(fcmdstr, cwd=cwd, shell=True)
    task.cmdstr = cmdstr
    return task

data = [
    (None, "master", "git clone {giturl} {repo}", {'cwd':'projectdir'}),
    ("master", "develop", "git checkout -b develop master", {'cwd':'repodir'}),
    ("develop", "feature", "git flow feature start {feature}", {'cwd':'repodir'}),
    ("feature", "develop", "git flow feature finish {feature}", {'cwd':'repodir'}),
    ("develop", "release", "git flow release start {release}", {'cwd':'repodir'}),
    ("release", "develop", "git flow release finish {release}", {'cwd':'repodir'}),
]


def workflow(graph = None):
    if not graph:
        graph = nx.Graph()
    for src, dst, cmdstr in data:
        graph.add_edge(src,dst, transition=cmd(cmdstr))

    return graph


    
