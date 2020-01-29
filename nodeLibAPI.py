from flask import Flask
from flask_restful import Resource, Api
import os

import nodeLib
clusters = dict()

app = Flask(__name__)
api = Api(app)

path = os.path.join(os.getcwd(), 'data')
def pathinator(cluster_obj):
    return os.path.join(path, '{}.node_cluster'.format(cluster_obj.cluster_name))

class commons:
    @staticmethod
    def write_clusters(clusters_, name):
        print(name)
        if name=='__all__':
            for cluster in clusters.values():
                nodeLib.files.write_cluster(cluster, pathinator(cluster))
        else:
            cluster = clusters.get(name)
            nodeLib.files.write_cluster(cluster, pathinator(cluster))

class welcome(Resource):
    def get(self):
        return({'msg': 'Welcome to nodeAPI.<br>For documentation refer <a href="WIP">nodeAPI repo</a>'})

    def post(self):
        return({'msg': ''})


api.add_resource(welcome, '/')


class create_cluster(Resource):
    def get(self, name):
        cluster = nodeLib.cluster.create_cluster(name)
        clusters[name] = cluster
        return ({'msg': "cluster '%s' is created" % (name)})


api.add_resource(create_cluster, '/create/cluster/<name>')


class load_cluster(Resource):
    def get(self, name):
        if name not in clusters.keys():
            # doing: look in 'data' folder
            for file in os.listdir(path):
                if file.split('.')[0] == name:
                    # todo read cluster from file
                    cluster_ = nodeLib.files.load_cluster(os.path.join(path, name+'.node_cluster'))
                    clusters[cluster_.cluster_name] = cluster_
                    return ({'msg': "cluster '%s' is loaded" % (name)})
        return ({'msg': "cluster '%s' is already loaded" % (name)})


api.add_resource(load_cluster, '/load/cluster/<name>')

class write_clusters(Resource):
    def get(self, name):
        """print(name)
        if name=='__all__':
            for cluster in clusters.values():
                nodeLib.files.write_cluster(cluster, pathinator(cluster))
        else:
            cluster = clusters.get(name)
            nodeLib.files.write_cluster(cluster, pathinator(cluster))"""
        commons.write_clusters(clusters, name)
        return ({'msg': "done"})

api.add_resource(write_clusters, '/write/<name>')

if __name__ == "__main__":
    app.run(debug=True)
