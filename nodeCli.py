#import argparse
import os
import click
import json

import nodeAPI

cwd = os.getcwd()
config_data = None
if 'cli_config.json' in os.listdir(cwd):
    path = os.path.join(cwd, 'cli_config.json')
    with open(path, 'r') as file:
        config_data = json.load(file)


def update_config():
    path = os.path.join(cwd, 'cli_config.json')
    with open(path, 'w') as file:
        json.dump(config_data, file)


@click.group()
def nodeCli():
    pass
# --------------------------------------------------------------------------------------------------------------


@click.group()
def config():
    pass

# ---------------------------------------------------------------------------------


@click.command(name="set")
@click.option('--env', default=os.path.join(cwd, 'data'), nargs=1)
def config_set(**options):
    # set the 'env'
    global config_data
    if config_data == None:
        config_data = {}
    config_data['env'] = options['env']
    click.echo(config_data)
    update_config()


@click.command(name="list")
@click.argument('mode', default='all', nargs=1)
def config_list(mode):
    if mode == 'all':
        if config_data != None:
            click.echo(config_data)
        else:
            click.echo('cli_config.json not found at {}/'.format(cwd))
    else:
        click.echo("{}".format({mode: config_data[mode]}))

# ---------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------


@click.group()
def create():
    pass

# ---------------------------------------------------------------------------------

# TODO name need to be able to automatically assigned incase its not given
@click.command(name='node')
@click.argument('name', nargs=1)
def create_node(name):
    click.echo('TODO create node with name: {}'.format(name))


@click.command(name='cluster')
@click.argument('name', nargs=1)
def create_cluster(name):
    click.echo('TODO create cluster with name: {}'.format(name))


@click.command(name='server')
@click.argument('name', nargs=1)
def create_server(name):
    click.echo('TODO create server with name: {}'.format(name))

# ---------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------


@click.group()
def activate():
    pass

# ---------------------------------------------------------------------------------

# TODO name need to be able to automatically assigned incase its not given
@click.command(name='cluster')
@click.argument('name', nargs=1)
def activate_cluster(name):
    click.echo('TODO activate cluster with name: {}'.format(name))


@click.command(name='server')
@click.argument('name', nargs=1)
def activate_server(name):
    click.echo('TODO activate server with name: {}'.format(name))

# ---------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------


@click.group()
def list():
    pass

# ---------------------------------------------------------------------------------

# TODO name need to be able to automatically assigned incase its not given
@click.command(name='node')
def list_node(name):
    click.echo('TODO list node with name: {}'.format(name))


@click.command(name='cluster')
def list_cluster(name):
    click.echo('TODO list cluster with name: {}'.format(name))


@click.command(name='server')
def list_server(name):
    click.echo('TODO list server with name: {}'.format(name))

# ---------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------


nodeCli.add_command(config)
config.add_command(config_set)
config.add_command(config_list)

nodeCli.add_command(create)
create.add_command(create_node)
create.add_command(create_cluster)
create.add_command(create_server)

nodeCli.add_command(activate)
activate.add_command(activate_cluster)
activate.add_command(activate_server)

nodeCli.add_command(list)
list.add_command(list_node)
list.add_command(list_cluster)
list.add_command(list_server)

if __name__ == '__main__':
    nodeCli()
