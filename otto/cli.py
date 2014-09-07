#!/usr/bin/env python

import os
import sys
import click
import otto.config

@click.group()
@click.option('-c', '--config', default='~/.otto/config',
              help = 'Set configuration file.')
@click.pass_context
def cli(ctx, config):
    cfg = otto.config.load(config)
    ctx.obj['config'] = cfg
    ctx.obj['config_filename'] = config
    return

@cli.command()
@click.argument('name', default="")
@click.option('-p','--path', default=os.getcwd(),
              help = 'Path to repository area (def=cwd)')
@click.option('-k','--keywords', 
              help = 'Any extra key/value pairs like key1=val1;key2=val2')
@click.option('-k','--keywords', 
              help = 'Any extra key/value pairs like key1=val1;key2=val2')
@click.option('--force', is_flag=True,
              help = 'Force a registration even if it exists')
@click.pass_context
def register(ctx, name, path, keywords, force):
    assert os.path.exists('.git')
    if not name:
        name = os.path.basename(os.getcwd())

    kwds = dict()
    if keywords:
        for kv in keywords.split(';'):
            k,v = kv.split('=')
            kwds[k] = v

    cfg = ctx.obj['config']
    repokey = 'repo ' + name
    if cfg.has_key(repokey):
        if force:
            cfg.pop(repokey)
        else:
            click.echo('Repository "%s" already registered' % name)
            sys.exit(1)

    sec = otto.config.register(cfg, name, path, **kwds)
    if not sec:
        click.echo('Failed to register "%s"' % name)
        sys.exit(1)
    otto.config.dump(cfg, ctx.obj['config_filename'])
    return

def main():
    cli(obj=dict())

if '__main__' == __name__:
    main()
