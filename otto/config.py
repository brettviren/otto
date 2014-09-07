#!/usr/bin/env python

import os
import re
try: from ConfigParser import SafeConfigParser
except ImportError: from configparser import SafeConfigParser

from collections import OrderedDict, defaultdict

def to_list(lst, delims = ', '):
    'Split a string into to a list according to delimiters.'
    ret = []
    for x in re.compile('[%s]' % delims).split(lst):
        x = x.strip()
        if x is '': continue
        ret.append(x)
    return ret

def load(filename = "~/.otto/config"):
    path = os.path.expanduser(os.path.expandvars(filename))
    cfgdir = os.path.dirname(path)

    ret = defaultdict(OrderedDict)
    if not os.path.exists(cfgdir):
        os.makedirs(cfgdir)
        return ret

    cfg = SafeConfigParser()
    cfg.read(path)
    for secname in cfg.sections():
        sec = OrderedDict()
        ret[secname] = sec
        for key in cfg.options(secname):
            sec[key] = cfg.get(secname, key, raw=True)
    return ret


def dump(cfg, filename = "~/.otto/config"):
    path = os.path.expanduser(os.path.expandvars(filename))
    with open(path, 'w') as fp:
        for secname, sec in cfg.items():
            fp.write('[%s]\n' % secname)
            for key, val in sec.items():
                val = val.replace('\n','\n\t')
                fp.write('%s = %s\n' % (key, val))
            fp.write('\n')

def register(cfg, name, path, **kwds):
    secname = 'repo %s' % name
    sec = cfg[secname]
    if sec:
        return
    sec['path'] = path
    for k,v in kwds.items():
        sec[k] = v
    return sec
