#!/usr/bin/env python

import os
import sys
import click
from subprocess import check_call
from collections import namedtuple

RepoData = namedtuple('RepoData', 'name url')
ProjData = namedtuple('ProjData', 'name path repos')

def cfg2dat(filename):
    filename = os.path.expanduser(os.path.expandvars(filename))

    from ConfigParser import SafeConfigParser
    cfg = SafeConfigParser()
    cfg.read(filename)

    repos = dict()
    projs = dict()

    for secname in cfg.sections():
        sectype, name = secname.split(' ',1)
        if sectype == 'repo':
            repos[name] = RepoData(name, cfg.get(secname, 'url'))
        if sectype == 'project':
            projs[name] = ProjData(name, os.path.expanduser(os.path.expandvars(cfg.get(secname, 'path'))),
                                   cfg.get(secname, 'repos'))
    return repos, projs
        


@click.group()
@click.option('-c', '--config', default='~/.otto/config',
              help = 'Set configuration file.')
@click.pass_context
def cli(ctx, config):
    ctx.obj['repo'], ctx.obj['proj'] = cfg2dat(config)
    return


@cli.command()
@click.option('-s','--subdir', default='venv', help='Sub-directory in project to hold virtual environment')
@click.argument('project')
@click.pass_context
def venvinit(ctx, subdir, project):
    p = ctx.obj['proj'][project]
    click.echo("Initializing virtualenv in %s" % p.path)
    if not os.path.exists(p.path):
        os.makedirs(p.path)
    vpath = os.path.join(p.path, subdir)
    if os.path.exists(vpath):
        click.echo('Project "%s" already has virtual environment at %s' % (project, vpath))
        sys.exit(1)
    check_call("virtualenv %s" % subdir, cwd=p.path, shell=True)
    apath = os.path.join(vpath,'bin/activate')
    if os.path.exists(vpath):
        click.echo('Initialized virtualenv in %s' % vpath)
        return
    click.echo('Failed to create virtualenv at %s' % vpath)
    sys.exit(1)


@cli.command()
@click.argument('project')
@click.pass_context
def clone(ctx, project):
    


def main():
    cli(obj=dict())

if '__main__' == __name__:
    main()
