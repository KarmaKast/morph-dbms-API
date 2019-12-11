import argparse
import nodeAPI

"""
> Aimed Interface:
    nodeLib create node --name fooNode
    nodeLib create cluster --name fooCluster
    nodeLib create server --name fooServer
    nodeLib activate cluster --name fooCluster
    nodeLib add node --path fooNodePath
    nodeLib add cluster --path fooClusterPath
"""

#parser = argparse.ArgumentParser(description='what?')
parser = argparse.ArgumentParser(
    prog='nodeCli', description='NodeLib Cli interface')
# parser.add_argument('option1', help="create activate or add") # help=" create node, cluster, or server"
subparsers = parser.add_subparsers()

# parser for the create command
parser_create = subparsers.add_parser(
    'create', help="create node, cluster, or server")
parser_activate = subparsers.add_parser(
    'activate', help="activate cluster or server")


subparsers1 = parser_create.add_subparsers()
parser_CreateNode = subparsers1.add_parser('node')
parser_CreateNode.add_argument('--name')
parser_CreateCluster = subparsers1.add_parser('cluster')
parser_CreateCluster.add_argument('--name')

subparsers2 = parser_activate.add_subparsers()
parser_ActivateNode = subparsers2.add_parser('cluster')
parser_ActivateNode.add_argument('--name')

args = parser.parse_args()

# print(args.sum(args.integers))
#print(args.create)
