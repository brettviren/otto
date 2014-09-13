#!/usr/bin/env python

from subprocess import Popen, PIPE

def cmd(cmdstr, path = "."):
    proc = Popen(cmdstr, shell=True, cwd=path, stdout=PIPE, stderr=PIPE)
    out,err = proc.communicate()
    ret = (out,err,proc.returncode)
    #print 'CMD: %s -> %s' % (cmdstr, ret)
    return ret

def describe(path = '.'):
    o,e,c = cmd("git symbolic-ref HEAD", path=path)
    branch = o.strip().split('/')[-1]

    o,e,c = cmd("git describe --dirty", path=path)
    if not c:
        commit = o.strip()
    else:
        o,e,c = cmd("git rev-parse --verify HEAD --short", path=path)
        commit = o.strip()
    return "%s:%s" % (branch,commit)

# http://stackoverflow.com/questions/2657935/checking-for-a-dirty-index-or-untracked-files-with-git
def shortstat(path = '.'):
    o,e,c = cmd("git diff --shortstat", path=path)
    if not c:
        return o.strip()
    return ""

def file_summary(path = '.'):
    o,e,c = cmd("git status --porcelain", path=path)
    if c:
        return
    #  M path
    # ?? path
    fs = [s.split()[0].strip() for s in o.split('\n') if s]
    return dict(
        modified = fs.count('M'),
        untracked = fs.count('??'),
    )

