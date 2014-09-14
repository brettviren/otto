#!/usr/bin/env python

from .proc import shell

def describe(path = '.'):
    o,e,c = shell("git symbolic-ref HEAD", cwd=path)
    branch = o.strip().split('/')[-1]

    o,e,c = shell("git describe --dirty", cwd=path)
    if not c:
        commit = o.strip()
    else:
        o,e,c = shell("git rev-parse --verify HEAD --short", cwd=path)
        commit = o.strip()
    return "%s:%s" % (branch,commit)

# http://stackoverflow.com/questions/2657935/checking-for-a-dirty-index-or-untracked-files-with-git
def shortstat(path = '.'):
    o,e,c = shell("git diff --shortstat", cwd=path)
    if not c:
        return o.strip()
    return ""

def file_summary(path = '.'):
    o,e,c = shell("git status --porcelain", cwd=path)
    if c:
        return
    #  M path
    # ?? path
    fs = [s.split()[0].strip() for s in o.split('\n') if s]
    return dict(
        modified = fs.count('M'),
        untracked = fs.count('??'),
        added = fs.count('A')
    )

