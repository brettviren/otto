#!/usr/bin/env python
'''
An Otto workflow using gitflow
'''
import os
import networkx as nx
from subprocess import check_call

states = ["master", "develop", "release", "feature", "hotfix"]

def cmd(cmdstr):
    def task(srcnode, tgtnode, **kwds):
        fcmdstr = cmdstr.format(**kwds)
        cwd = kwds.get('cwd',None)
        print 'Running command: "%s" in directory: %s' % (fcmdstr, cwd)
        check_call(fcmdstr, cwd=cwd, shell=True)
    task.cmdstr = cmdstr
    return task

def workflow(graph = None):
    if not graph:
        graph = nx.Graph()

    graph.add_edge(None, "master", transition = cmd("git clone {giturl} {repo}"))

    graph.add_edge("master", "develop", transition = cmd("git checkout -b develop master"))

    graph.add_edge("develop", "feature", transition = cmd("git flow feature start {feature}"))
    graph.add_edge("feature", "develop", transition = cmd("git flow feature finish {feature}"))

    graph.add_edge("develop", "release", transition = cmd("git flow release start {release}"))
    graph.add_edge("release", "develop", transition = cmd("git flow release finish {release}"))

    return graph


    
