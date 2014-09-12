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

@cli.command()
@click.argument("setting")
@click.pass_context
def set(ctx, setting):
    k,v = setting.split('=')
    sm = ctx.obj['machine']
    p = dict(sm.params)
    p[k] = v
    sm.params = p
    print sm.params
    sm.sync()

@cli.command()
@click.pass_context
def status(ctx):
    sm = ctx.obj['machine']
    click.echo('In state: "%s"' % sm.state)
    click.echo('Parameters:\n\t%s' % '\n\t'.join(["%s:%s" % kv for kv in sm.params.items()]))


@cli.command()
@click.argument('state')
@click.pass_context
def goto(ctx, state):
    sm = ctx.obj['machine']
    sm.goto(state)

@cli.command()
@click.argument('state', default = '')
@click.pass_context
def jump(ctx, state):
    sm = ctx.obj['machine']
    sm.jump(state or None)


def main():
    cli(obj=dict())

