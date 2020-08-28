import json
import os

from flask import Flask, request, send_from_directory
from flask import send_file

import mog.mapper as mapper
import data as data_mod

app = Flask(__name__)


def error(err):
    print(err)


def request_valid(dataset_req, datafile_req, filter_func_req):
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')
    ff = request.args.get('filter_func')

    if dataset_req and ds0 not in data_mod.data_sets:
        return False

    if datafile_req and ds1 not in data_mod.data_sets[ds0]:
        return False

    if filter_func_req and ff not in data_mod.data_sets[ds0][ds1]:
        return False

    return True


def load_graph(ds0, ds1):
    return data_mod.read_json_graph('data/' + ds0 + "/" + ds1)


def load_filter_function(ds0, ds1, ff, ranked=False):
    if ff not in data_mod.data_sets[ds0][ds1]:
        return None

    with open('data/' + ds0 + "/" + os.path.splitext(ds1)[0] + "/" + ff + ".json") as json_file:
        ff_data = json.load(json_file)

    if ranked:
        tmp = list(ff_data.keys())
        tmp.sort(key=(lambda e: ff_data[e]))
        for i in range(len(tmp)):
            ff_data[tmp[i]] = i

    return ff_data


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
def get_datasets():
    return json.dumps(data_mod.data_sets)


@app.route('/graph', methods=['GET', 'POST'])
def get_graph():
    # Check that the request is valid
    if not request_valid(True, True, False):
        return "{}"

    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')

    return send_file('data/' + ds0 + "/" + ds1)


@app.route('/filter_function', methods=['GET', 'POST'])
def get_filter_function():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{}"

    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')
    ff = request.args.get('filter_func')

    return json.dumps(load_filter_function(ds0, ds1, ff, request.args.get('rank_filter') == 'true'))


@app.route('/mog', methods=['GET', 'POST'])
def get_mog():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{}"

    # Load the graph and filter function
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')
    ff = request.args.get('filter_func')

    graph_data, graph = load_graph(ds0, ds1)
    values = load_filter_function(ds0, ds1, ff, request.args.get('rank_filter') == 'true')

    # Construct the cover
    intervals = int(request.args.get('coverN'))
    overlap = float(request.args.get('coverOverlap'))

    cover = mapper.form_cover(values, intervals, overlap)

    # Construct MOG
    mog = mapper.MapperOnGraphs(graph, values, cover)

    node_size_filter = int(request.args.get('mapper_node_size_filter'))
    if node_size_filter > 0:
        mog.filter_node_size(node_size_filter)

    gcc_only = request.args.get('gcc_only') == 'true'
    if gcc_only:
        mog.extract_greatest_connect_component()

    return mog.to_json()
