import flask
import nodeLib

app = flask.Flask(__name__)
app.config["DEBUG"] = True

clusters = {}


@app.route('/', methods=['GET'])
def home():
    return "<h1>NodeLib Web API</h1><p>This is a prototype API for nodeLib graph database.</p>"

@app.route('/nodeLib/create/cluster/<name>')
def create_cluster(name):
    clusters[name] = nodeLib.node.Node_Cluster.create_cluster(clusterName=name)
    return "TODO create a cluster {}".format(name)
#nodeLib.node.Node_Cluster.create_cluster(clusterName='family')

@app.route('/nodeLib/get/cluster/<name>')
def get_cluster(name):
    if name in clusters.keys():
        return str(clusters[name])
    else:
        return 'cluster with name {} not found'.format(name)

app.run()