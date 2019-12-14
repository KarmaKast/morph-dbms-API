#import argparse
import click
import nodeAPI


@click.group()
def nodeCli():
    pass

#--------------------------------------------------------------------------------------------------------------
@click.group()
def create():
    pass

#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------

@click.group()
def activate():
    pass

#---------------------------------------------------------------------------------

# TODO name need to be able to automatically assigned incase its not given
@click.command(name='cluster')
@click.argument('name', nargs=1)
def activate_cluster(name):
    click.echo('TODO activate cluster with name: {}'.format(name))
    
@click.command(name='server')
@click.argument('name', nargs=1)
def activate_server(name):
    click.echo('TODO activate server with name: {}'.format(name))

#---------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------

@click.group()
def list():
    pass

#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------

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
