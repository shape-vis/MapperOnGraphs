import fnmatch
import json
import os

from flask import Flask, request, send_from_directory
from flask import send_file
from networkx.readwrite import json_graph

import mog.mapper as mapper
import mog.filter_functions as ff

app = Flask(__name__)


data_sets = {}
for d0 in os.listdir("../data/"):
    if os.path.isdir( "../data/" + d0 ):
        data_sets[d0] = {}
        for d1 in os.listdir("../data/" + d0 ):
            if fnmatch.fnmatch(d1.lower(), "*.json") or fnmatch.fnmatch(d1.lower(), "*.graph"):
                data_sets[d0][d1] = ["average_geodesic_distance", "density", "eccentricity", "eigen_function", "pagerank"]
print(data_sets)


def error(err):
    print(err)


@app.route('/')
def send_main():
    try:
        return send_file('pages/main.html')
    except Exception as e:
        return str(e)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/datasets', methods=['GET', 'POST'])
def get_datasets( ):
    return json.dumps(data_sets)


@app.route('/graph', methods=['GET', 'POST'])
def get_graph():
    ds0 = request.args.get('ds0')
    ds1 = request.args.get('ds1')

    if ds0 not in data_sets or ds1 not in data_sets[ds0]:
        return "{}"

    return send_file('../data/' + ds0 + "/" + ds1)


@app.route('/mog', methods=['GET', 'POST'])
def get_mog():
    ds0 = request.args.get('ds0')
    ds1 = request.args.get('ds1')

    if ds0 not in data_sets or ds1 not in data_sets[ds0]:
        return "{}"

    intervals = int( request.args.get('intervals') )
    overlap = float( request.args.get('overlap') )
    attribute = request.args.get('attribute')

    with open(data_dir + data_file) as json_file:
        data = json.load(json_file)

        nodes = {}
        for n in data['nodes']:
            nodes[n['id']] = n

        G = json_graph.node_link_graph(data)

        values = {}
        for n in filter(lambda n: attribute in nodes[n], G.nodes):
            values[n] = float( nodes[n][attribute] )
        missing_vals = list(filter(lambda n: attribute not in nodes[n], G.nodes ))

        for loop_iter in range(0, 3):
            mapper.fill_missing_diffuse_avg(G, values, missing_vals)

        components = mapper.get_mapper_components(G, values, intervals, overlap)

        nodes = mapper.get_nodes( values, components )
        links = mapper.get_links( nodes )

        return json.dumps( {'nodes':nodes, 'links':links} )


file_list = []


def read_json_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


def search_directory( dir ):
    for data_file in os.listdir(dir + "/"):
        if fnmatch.fnmatch(data_file.lower(), "*.json") or fnmatch.fnmatch(data_file.lower(), "*.graph"):
            # print( "df: " + dir + "/" + data_file)
            file_list.append(dir + "/" + data_file)
        elif os.path.isdir( dir + "/" + data_file):
            search_directory( dir + "/" + data_file )
        else:
            print( "other: " + dir + "/" + data_file )

search_directory( "../data" )

graph = read_json_graph("../data/not_in_paper/miserables.json")
print( graph.nodes)
print()
print( graph.edges)
print()
print("AGD")
print( ff.average_geodesic_distance(graph) )
print()
print("Density")
print( ff.density(graph) )
print()
print("eccentricity")
print( ff.eccentricity(graph) )
print()
print("eigen_function")
print( ff.eigen_function(graph) )
print()
print("pagerank")
print( ff.pagerank(graph) )