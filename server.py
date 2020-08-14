import fnmatch
import json
import os

from flask import Flask, request, send_from_directory
from flask import send_file

import mog.mapper as mapper
import data
from networkx.readwrite import json_graph


app = Flask(__name__)

data_gen = [ {"in": "data/source/not_in_paper/football_out.JSON", "out": "data/small/football_out.json"},
             {"in": "data/source/not_in_paper/airport6632_gcc.JSON", "out": "data/medium/airport6632_gcc.json"} ]

for file in data_gen:
    if not os.path.exists(file["out"]):
        data.process_datafile( file["in"], file["out"] )

data_sets = {}
for d0 in os.listdir("data/"):
    if os.path.isdir( "data/" + d0 ):
        data_sets[d0] = {}
        for d1 in os.listdir("data/" + d0 ):
            if fnmatch.fnmatch(d1.lower(), "*.json") or fnmatch.fnmatch(d1.lower(), "*.graph"):
                data_sets[d0][d1] = ["average_geodesic_distance", "density", "eccentricity", "eigen_function", "pagerank"]
# print(data_sets)


def error(err):
    print(err)


@app.route('/')
def send_main():
    try:
        return send_file('static/main.html')
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
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')

    if ds0 not in data_sets or ds1 not in data_sets[ds0]:
        return "{}"

    return send_file('data/' + ds0 + "/" + ds1)


@app.route('/mog', methods=['GET', 'POST'])
def get_mog():
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')

    if ds0 not in data_sets or ds1 not in data_sets[ds0]:
        return "{}"

    intervals = int( request.args.get('coverN') )
    overlap = float( request.args.get('coverOverlap') )
    attribute = request.args.get('filter_func')

    if ds0 not in data_sets or ds1 not in data_sets[ds0]:
        return "{}"


    with open('data/' + ds0 + "/" + ds1) as json_file:
        data = json.load(json_file)

        nodes = {}
        for n in data['nodes']:
            nodes[n['id']] = n

        G = json_graph.node_link_graph(data)

        values = {}
        for n in G.nodes:
            values[n] = float( nodes[n][attribute] )
        # missing_vals = list(filter(lambda n: attribute not in nodes[n], G.nodes ))
        #
        # for loop_iter in range(0, 3):
        #     mapper.fill_missing_diffuse_avg(G, values, missing_vals)

        cover = mapper.form_cover(values, intervals, overlap)
        components = mapper.get_components(G, values, cover)
        nodes = mapper.get_nodes( values, components )
        links = mapper.get_links( nodes )

        return json.dumps( {'nodes': nodes, 'links': links} )


file_list = []

