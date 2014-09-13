#!/usr/bin/env python

import os
import sys
import click

import otto.state
import otto.workflows.gitflow

@click.group()
@click.option('-s','--store',default="otto.state", help="The Otto database to use")
@click.pass_context
def cli(ctx, store):
    g = otto.workflows.gitflow.workflow()
    sm = otto.state.PersistentStateMachine(store, g)
    ctx.obj['machine'] = sm
    pass


def kev2dict(setting):
    d = dict()
    for s in setting:
        k,v = s.split('=')
        d[k] = v
    return d

@cli.command()
@click.argument("setting", nargs=-1)
@click.pass_context
def set(ctx, setting):
    'Set database parameters.'
    sm = ctx.obj['machine']
    p = dict(sm.params)
    p.update(kev2dict(setting))
    sm.params = p
    sm.sync()

@cli.command()
@click.pass_context
def status(ctx):
    sm = ctx.obj['machine']
    click.echo('In state: "%s"' % sm.state)
    click.echo('Parameters:\n\t%s' % '\n\t'.join(["%s:%s" % kv for kv in sm.params.items()]))


@cli.command()
@click.argument('state')
@click.argument("setting", nargs=-1)
@click.pass_context
def goto(ctx, state, setting):
    sm = ctx.obj['machine']
    sm.goto(state, **kev2dict(setting))

@cli.command()
@click.argument('state', default = '')
@click.pass_context
def jump(ctx, state):
    sm = ctx.obj['machine']
    sm.jump(state or None)

@cli.command()
@click.argument('arg', nargs=-1)
@click.pass_context
def dummy(ctx, arg):
    click.echo(str(arg))
    pass

def main():
    cli(obj=dict())

