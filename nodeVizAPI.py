from flask import Flask
from flask_restful import Resource, Api, request
import os
import json

import nodeLib
import nodeViz

app = Flask(__name__)
api = Api(app)

path = os.path.join(os.getcwd(), 'data')

viz_instance1 = nodeViz.nodeViz()


class commons:
    database_name = "viz_api_database"
    @staticmethod
    def write_clusters(clusters_):
        for cluster in clusters_:
            nodeLib.files.write_cluster(
                cluster, path, commons.database_name)


@app.route('/')
def index():
    # return({'msg': 'Welcome to nodeAPI for nodeViz.<br>For documentation refer <a href="WIP">nodeAPI repo</a>'})
    return('Welcome to nodeAPI for nodeViz.<br>For documentation refer <a href="WIP">nodeAPI repo</a>')


class create_node(Resource):
    def post(self, name):
        viz_instance1.create_node(name)
        return ({'msg': "node '%s' is created" % (name)})


api.add_resource(create_node, '/create/node/<name>')


class save_state(Resource):
    def post(self):
        commons.write_clusters(
            [viz_instance1.source_cluster, viz_instance1.viz_cluster])
        return ({'msg': "done"})


api.add_resource(save_state, '/save')


class load_state(Resource):
    # doing:
    def get(self):
        viz_instance1.load_database(path, commons.database_name)
        return ({'msg': "done"})


api.add_resource(load_state, '/load')


class archive(Resource):
    def post(self, mode):
        nodeLib.files.archive_database(
            path, commons.database_name, mode=mode, remove=False)
        return ({'msg': "done"})


api.add_resource(archive, '/archive/<mode>')


class describe1:
    def __init__(self):
        self.msgs = []

    def _describer(self, msg):
        self.msgs.append(msg)

    def out(self):
        out_msg = ''
        for msg in self.msgs:
            out_msg = out_msg+str(msg)+'<br>'
        return out_msg


class describe(Resource):
    def get(self):
        d1 = describe1()
        nodeLib.cluster.describe(
            viz_instance1.source_cluster, describer_=d1._describer)
        print(d1.msgs)
        d2 = describe1()
        print(d2.msgs)
        nodeLib.cluster.describe(
            viz_instance1.viz_cluster, describer_=d2._describer)
        return ("%s <br><br> %s" % (d1.out(), d2.out()))


api.add_resource(describe, '/describe')


class update_prop(Resource):
    def post(self, ID):
        args = request.args
        print(args)
        for prop in args.keys():
            values = args[prop]
            # context: its better to convert this string to list at the receiving end
            if prop in ['location', 'color']:
                values = values.strip(')(').split(',')
                values = [int(value) for value in values]
            viz_instance1.change_property(ID, prop, values)
        return ({'msg': ''})


api.add_resource(update_prop, '/updateProps/<ID>')


class clear_database(Resource):
    def post(self):
        viz_instance1.clear_database()
        return ({"msg": ''})


api.add_resource(clear_database, '/clear')

if __name__ == "__main__":
    app.run(debug=True)
