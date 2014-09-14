#!/usr/bin/env python
'''
Run sub-processes under otto
'''

from subprocess import Popen, PIPE
from .util import format


def shell(cmdline, cwd='.'):
    '''
    Run a shell command.  Return triple: (output,error, returncode)
    '''
    p = Popen(cmdline, shell=True, cwd=cwd, stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()
    ret = (out,err,p.returncode)
    #print 'CMD: %s -> %s' % (cmdstr, ret)
    return ret

def shell_task(cmdline, **code_kwds):
    '''
    Return a function callable as a workflow task.
    '''
    def task(srcnode, tgtnode, **run_kwds):
        params = dict(code_kwds)
        params.update(run_kwds)
        
        cwd = params.pop('cwd','.')
        cwd = format(cwd, **params)
        cmdstr = format(cmdline, cwd=cwd, **params)
        o,e,c = shell(cmdstr, cwd=cwd)
        if c:
            raise RuntimeError(e)
        return o
    task.cmdline = cmdline      # save it for reference
    return task
