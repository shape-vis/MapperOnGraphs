import json
import os

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import send_file

import mog.mapper as mapper
import data as data_mod
import mog.graph_io as GraphIO
import layout.initial_layout as layout
import networkx as nx
import cache

app = Flask(__name__)


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


def get_arg_params():
    return {
        'filter_func': request.args.get('filter_func'),
        'coverN': request.args.get('coverN'),
        'coverOverlap': request.args.get('coverOverlap'),
        'component_method': request.args.get('component_method'),
        'link_method': request.args.get('link_method'),
        'mapper_node_size_filter': request.args.get('mapper_node_size_filter'),
        'rank_filter': 'false' if request.args.get('rank_filter') is None else request.args.get('rank_filter'),
        'gcc_only': 'false' if request.args.get('gcc_only') is None else request.args.get('gcc_only')
    }

# def load_graph():
#     ds0 = request.args.get('dataset')
#     ds1 = request.args.get('datafile')
#     return GraphIO.read_json_graph('data/' + ds0 + "/" + ds1)


# def get_cache_filename():
#     rank_filter = 'false' if request.args.get('rank_filter') is None else request.args.get('rank_filter')
#     gcc_only = 'false' if request.args.get('gcc_only') is None else request.args.get('gcc_only')
#
#     dir = 'cache/' + request.args.get('dataset')
#     if not os.path.exists(dir): os.mkdir(dir)
#
#     dir += '/' + request.args.get('datafile')
#     if not os.path.exists(dir): os.mkdir(dir)
#
#     return dir + '/mog_' + request.args.get('filter_func') + '_' + rank_filter + '_' \
#            + request.args.get('coverN') + '_' + request.args.get('coverOverlap') + '_' \
#            + request.args.get('component_method') + '_' + request.args.get('link_method') + '_' \
#            + request.args.get('mapper_node_size_filter') + '_' + gcc_only + '.json'


@app.route('/')
def send_main():
    return send_file('static/index.html')


@app.route('/<path:path>')
def send_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        return str(e)


@app.route('/datasets', methods=['GET', 'POST'])
def get_datasets():
    return json.dumps(data_mod.data_sets)


@app.route('/graph', methods=['GET', 'POST'])
def get_graph():
    # Check that the request is valid
    if not request_valid(True, True, False):
        return "{'result':'failed'}"
    else:
        return send_file(cache.get_graph_filename(request.args.to_dict()))


@app.route('/graph_layout', methods=['GET', 'POST'])
def save_graph():
    # Check that the request is valid
    if not request_valid(True, True, False):
        return "{'result':'failed'}"
    else:
        cache.save_graph_layout(request.args.to_dict(), request.json)
        return "{'result':'ok'}"


@app.route('/filter_function', methods=['GET', 'POST'])
def get_filter_function():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{'result':'failed'}"
    else:
        return json.dumps(cache.get_filter_function(request.args.to_dict()))


@app.route('/mog', methods=['GET', 'POST'])
def get_mog():
    # Check that the request is valid
    if not request_valid(True, True, True):
        return "{}"
    else:
        mog_layout_cf = cache.get_cache_fn("mog_layout", request.args.get('dataset'), request.args.get('datafile'),
                                           get_arg_params())

        if os.path.exists(mog_layout_cf):
            print("  >> " + request.args.get('datafile') + " found in mog layout cache")
            return send_file(mog_layout_cf)

        return cache.get_mog(request.args.to_dict())


@app.route('/mog_layout', methods=['GET', 'POST'])
def cache_mog():
    filename = cache.get_cache_fn("mog_layout", request.args.get('dataset'), request.args.get('datafile'), get_arg_params())
    with open(filename, 'w') as outfile:
        json.dump(request.json, outfile)

    return "{}"


if __name__ == '__main__':
    if not os.path.exists("cache"):
        os.mkdir("cache")
    data_mod.scan_datasets()
    app.run(host='0.0.0.0', port=5000)
