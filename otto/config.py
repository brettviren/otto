#!/usr/bin/env python

import os
import re
try: from ConfigParser import SafeConfigParser
except ImportError: from configparser import SafeConfigParser


from collections import OrderedDict, defaultdict

def to_list(lst, delims = ', '):
    'Split a string into to a list according to delimiters.'
    if isinstance(lst, list) or isinstance(lst, tuple):
        return lst
    ret = []
    for x in re.compile('[%s]' % delims).split(lst):
        x = x.strip()
        if x is '': continue
        ret.append(x)
    return ret


class Configuration(object):
    '''
    An Otto configuration object.

    It consists of a collection of repositories and projects (groups of repositories).
    '''
    pass


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


class ConfigFile(object):
    def __init__(self, filename):
        self.filename = filename
    def __enter__(self):
        self.cfg = load(self.filename)
        return self.cfg
    def __exit__(self):
        dump(self.cfg, self.filename)
        




def register(cfg, name, path, **kwds):
    secname = 'repo %s' % name
    sec = cfg[secname]
    if sec:
        return
    sec['path'] = path
    for k,v in kwds.items():
        sec[k] = v
    return sec


def get_thing(cfg, name, what='group'):
    ret = OrderedDict()
    for secname, sec in cfg.items():
        thing_type, thing_name = secname.split(' ',1)
        if not thing_type != what:
            continue
        if not name or thing_name == name:
            ret[thing_name] = sec
    return ret

def get_repos(cfg, name = None):
    '''
    Return an OrderedDict of (repo name, repo dict) for given name or all if None.
    '''
    return get_thing(cfg, name, 'repo')

def get_groups(cfg, name = None):
    '''
    Return an OrderedDict of (group name, group dict) for given name or all if None.
    '''
    return get_thing(cfg, name, 'group')

def get_group(cfg, name):
    return get_groups(cfg, name)[name]


def add_group(cfg, name, repos):
    grp = cfg['group %s' % name]
    have = to_list(grp.get('repos', ''))
    repos = to_list(repos)
    for r in repos:
        if not r in have:
            have.append(r)
    grp['repos'] = ', '.join(have)

    
