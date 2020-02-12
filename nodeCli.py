#import argparse
import os
import click
import json

import nodeLib

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

# active cluster


@click.group()
def nodeCli():
    pass
# --------------------------------------------------------------------------------------------------------------


@click.group()
def config():
    pass

# ---------------------------------------------------------------------------------
@click.command(name="add")
@click.option('--database', default=[os.path.join(cwd, 'data')], nargs=1, help="")
def config_add(**options):
    # set the 'env'
    # TODO check whether user given env path is valid full path or not
    global config_data
    if config_data == None:
        config_data = {}
    config_data['database'].append(options['database'])
    click.echo(config_data)
    update_config()


config.add_command(config_add)


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


config.add_command(config_list)
# ---------------------------------------------------------------------------------
nodeCli.add_command(config)
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
    
    if 'database' in config_data.keys():
        click.echo(config_data['database'][0])
        if not os.path.exists(config_data['database'][0]):
            # create path
            os.mkdir(config_data['database'][0])
    else:
        #update
        pass
    # create a node with give name
    #nodeLib
    # node_ID : ID -1 indicates orphan node. i.e not related to any other node
    node_ = nodeLib.node.Node_Manager.create_node( node_ID={'ID':-1 , 'node_name':name})
    nodeLib.files.write(node_, os.path.join(config_data['database'][0], '{}.node.yaml'.format(node_._hash)))
    


@click.command(name='cluster')
@click.argument('name', nargs=1)
def create_cluster(name):
    click.echo('TODO create cluster with name: {}'.format(name))
    
    if 'database' in config_data.keys():
        click.echo(config_data['database'][0])
        if not os.path.exists(config_data['database'][0]):
            # create path
            os.mkdir(config_data['database'][0])
    else:
        #update
        pass
    # create a cluster with give name
    #nodeLib


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
