#!/usr/bin/env python
'''
Ottomate repositories
'''

import os
import sys
import click
from subprocess import check_call
from collections import namedtuple
from . import git

from ConfigParser import SafeConfigParser


default_config_file = '~/.otto/repos.cfg'

def path_to_name(path):
    path = os.path.basename(path)
    if path.startswith('.'):
        path = path[1:]
    return path

def expandpath(path):
    return os.path.expanduser(os.path.expandvars(path))

def objectify(name, **data):
    name = name.replace('.','_').replace('-','_')
    return namedtuple(name, sorted(data.keys()))(**data)

class RepoConfg(object):
    '''
    Read/write access to the repository configuration file.

    Each repository is a named section with these expected items:

    - path :: absolute filesystem path

    '''
    def __init__(self, filename):
        self._filename = expandpath(filename)
        self._dirty = False

    # context manager
    def __enter__(self):
        self.cfg = SafeConfigParser()
        self.cfg.read(self._filename)
        return self
    def __exit__(self, typ, val, tb):
        if typ:
            raise
        if not self._dirty:
            return
        with open(self._filename, 'w') as fp:
            self.cfg.write(fp)

    # accessors
    @property
    def repos(self):
        return self.cfg.sections()

    def repo(self, name):
        items = self.cfg.items(name)
        return objectify(name, **dict(items))

    def __getitem__(self, name):
        return self.repo(name)

    def add(self, name, **data):
        if name in self.repos:
            raise ValueError, 'Repository "%s" already exists' % name
        self.cfg.add_section(name)
        for k,v in data.items():
            self.cfg.set(name, k,v)
        self._dirty = True

    def remove(self, name):
        ret = self.cfg.remove_section(name)
        if ret:
            self._dirty = True
        return ret
            
    def find(self, **kwds):
        want = set(kwds.items())
        ret = list()
        for name in self.repos:
            dat = set(self.cfg.items(name))
            if not dat.issuperset(want):
                continue
            ret.append(name)
        return ret


@click.group()
@click.option('-c', '--config', default=default_config_file,
              help = 'Set global configuration file.')
@click.pass_context
def cli(ctx, config):
    ctx.obj['config'] = config
    return


@cli.command()
@click.option('-p', '--path', default=None,
              help = 'Set path to top of repository')
@click.option('-n', '--name', default=None,
              help = 'Set name for this repository')
@click.pass_context
def register(ctx, path, name):
    'Remember a repository.'
    path = expandpath(path or os.getcwd())

    if not os.path.exists(os.path.join(path,'.git/config')):
        click.echo('Not a git repository: %s' % path)
        sys.exit(1)

    if not name:
        name = path_to_name(path)

    with RepoConfg(ctx.obj['config']) as rc:
        try:
            rc.add(name, path=path)
        except ValueError,e:
            click.echo(str(e))
            sys.exit(1)

@cli.command()
@click.option('-p', '--path', default=None,
              help = 'Set path to top of repository')
@click.option('-n', '--name', default=None,
              help = 'Set name for this repository')
@click.pass_context
def forget(ctx, path, name):
    'Forget a repository registration.'
    with RepoConfg(ctx.obj['config']) as rc:

        if name:
            if rc.remove(name):
                return

        path = expandpath(path or os.getcwd())
        todie = rc.find(path=path)
        if not todie:
            click.echo('Current repo not registered')
            sys.exit(1)
        if len(todie) > 1:
            msg = '''Multiple registrations for this repository use "-n name", 
have: %s''' % ', '.join(todie)
            click.echo(msg)
            sys.exit(1)
        if rc.remove(todie[0]):
            return
        click.echo('Failed to remove repo "%s"' % todie[0])
        sys.exit(1)

@cli.command()
@click.argument('repo', default='')
@click.option('-f','--format',default='{name:>10}: {desc:<25} [{summary:10}] {path}',
              help='Set format for description')
@click.pass_context
def status(ctx, repo, format):
    'Show the global status of known repositories'
    with RepoConfg(ctx.obj['config']) as rc:
        repos = rc.repos
        if repo: repos = [repo]
        for name in repos:
            path = rc[name].path
            desc = git.describe(path=path)
            summary = 'mod:{modified} new:{untracked}'.format(**git.file_summary(path))
            string = format.format(**locals())

            click.echo(string)


def main():
    cli(obj=dict())

