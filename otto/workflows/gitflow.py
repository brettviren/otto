#!/usr/bin/env python
'''
An Otto workflow using gitflow
'''
from otto.workflow import make_workflow

params = dict(cwd='{path}')

edge_data = [
    (     None,  "master", "git clone {url} {path}"),

    (     "master", "gitflowinit", "git flow init -d", params),
    ("gitflowinit",     "develop", None)

    ( "master", "develop", "git checkout -b develop master", params),
    ("develop", "feature", "git flow feature start {feature}", params),
    ("feature", "develop", "git flow feature finish {feature}", params),
    ("develop", "release", "git flow release start {release}", params),
    ("release", "develop", "git flow release finish {release}", params),
]


def workflow():
    return make_workflow(*edge_data)
