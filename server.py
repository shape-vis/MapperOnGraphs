import json
import os

import sklearn.preprocessing

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


def load_graph():
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')
    return data_mod.read_json_graph('data/' + ds0 + "/" + ds1)


def load_filter_function(ranked=False):
    ds0 = request.args.get('dataset')
    ds1 = request.args.get('datafile')
    ff = request.args.get('filter_func')

    with open('data/' + ds0 + "/" + os.path.splitext(ds1)[0] + "/" + ff + ".json") as json_file:
        ff_data = json.load(json_file)

    if ranked:
        tmp = list(ff_data.keys())
        tmp.sort(key=(lambda e: ff_data[e]))
        for i in range(len(tmp)):
            ff_data[tmp[i]] = i / (len(tmp) - 1)
    else:
        val_max = ff_data[max(ff_data.keys(), key=(lambda k: ff_data[k]))]
        val_min = ff_data[min(ff_data.keys(), key=(lambda k: ff_data[k]))]
        if val_min == val_max: val_max += 1
        for (key, val) in ff_data.items():
            ff_data[key] = (float(val) - val_min) / (val_max - val_min)

    return ff_data


@app.route('/')
def send_main():
    try:
        return send_file('static/index.html')
    except Exception as e:
        return str(e)


@app.route('/<path:path>')
def send_very_large(path):
    try:
        return send_from_directory('static', path)
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

    return send_file('data/' + request.args.get('dataset') + "/" + request.args.get('datafile'))


@app.route('/filter_function', methods=['GET', 'POST'])
def get_filter_function():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{}"

    return json.dumps(load_filter_function(request.args.get('rank_filter') == 'true'))


def get_cache_filename():
    rank_filter = 'false' if request.args.get('rank_filter') is None else request.args.get('rank_filter')
    gcc_only = 'false' if request.args.get('gcc_only') is None else request.args.get('gcc_only')

    dir = 'cache/' + request.args.get('dataset')
    if not os.path.exists(dir): os.mkdir(dir)

    dir += '/' + request.args.get('datafile')
    if not os.path.exists(dir): os.mkdir(dir)

    return dir + '/mog_' + request.args.get('filter_func') + '_' + rank_filter + '_' \
           + request.args.get('coverN') + '_' + request.args.get('coverOverlap') + '_' \
           + request.args.get('component_method') + '_' + request.args.get('link_method') + '_' \
           + request.args.get('mapper_node_size_filter') + '_' + gcc_only + '.json'


@app.route('/mog_cache', methods=['GET', 'POST'])
def cache_mog():
    # print(file)

    with open(get_cache_filename(), 'w') as outfile:
        json.dump(request.json, outfile)

    # print(request.args);
    # print(request.json);
    return "{}"


@app.route('/mog', methods=['GET', 'POST'])
def get_mog():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{}"

    cf = get_cache_filename()
    if os.path.exists(cf):
        print("FOUND IN CACHE: " + cf)
        return send_file(cf)

    # Load the graph and filter function
    graph_data, graph = load_graph()
    values = load_filter_function(request.args.get('rank_filter') == 'true')

    # Construct the cover
    intervals = int(request.args.get('coverN'))
    overlap = float(request.args.get('coverOverlap'))

    cover = mapper.form_cover(values, intervals, overlap)

    # Construct MOG
    mog = mapper.MapperOnGraphs(graph, values, cover, request.args.get('component_method'),
                                request.args.get('link_method'))

    print("Input Node Count: " + str(graph.number_of_nodes()))
    print("Input Edge Count: " + str(graph.number_of_nodes()))
    print("MOG Node Count: " + str(mog.number_of_nodes()))
    print("MOG Edge Count: " + str(mog.number_of_nodes()))
    print("MOG Compute Time: " + str(mog.compute_time()) + " seconds")

    node_size_filter = int(request.args.get('mapper_node_size_filter'))
    if node_size_filter > 0:
        mog.filter_node_size(node_size_filter)

    gcc_only = request.args.get('gcc_only') == 'true'
    if gcc_only:
        mog.extract_greatest_connect_component()

    if graph.number_of_nodes() > 5000:
        mog.strip_components_from_nodes()

    json = mog.to_json()

    with open(get_cache_filename(), 'w') as outfile:
        outfile.write(json)

    return json


if __name__ == '__main__':
    if not os.path.exists("cache"):
        os.mkdir("cache")
    # data_mod.generate_data(1)
    data_mod.scan_datasets()
    app.run(host='0.0.0.0', port=5000)
