import json
import os

import cache
import data as data_mod
from flask import Flask
from flask import request
from flask import send_file
from flask import send_from_directory

app = Flask(__name__, static_url_path="/docs", static_folder='docs')


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


@app.route('/')
def send_main():
    return send_file('docs/index.html')


@app.route('/<path:path>')
def send_static(path):
    try:
        return send_from_directory('docs', path)
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
        return send_file(cache.get_graph_path(request.args.to_dict()))


@app.route('/update_graph', methods=['GET', 'POST'])
def update_graph():
    # Check that the request is valid
    if request.args.get('type') == 'graph_layout':
        if request_valid(True, True, False):
            cache.save_graph_layout(request.args.to_dict(), request.json)
            return "{'result':'ok'}"

    return "{'result':'failed'}"


@app.route('/update_mog', methods=['GET', 'POST'])
def update_mog():
    # Check that the request is valid
    if request_valid(True, True, True):
        filename = cache.get_mog_path(request.args.get('dataset'),
                                      request.args.get('datafile'),
                                      request.args.get('filter_func'),
                                      {
                                          'component_method' : request.args.get('component_method'),
                                          'link_method': request.args.get('link_method'),
                                          'coverN': request.args.get('coverN'),
                                          'rank_filter': request.args.get('rank_filter'),
                                          'coverOverlap': request.args.get('coverOverlap')
                                      })
        with open(filename, 'w') as outfile:
            json.dump(request.json, outfile)
        return "{'result':'ok'}"

    return "{'result':'failed'}"


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
        return "{'result':'failed'}"
    else:
        return cache.get_mog(request.args.to_dict())


if __name__ == '__main__':
    if not os.path.exists("cache"):
        os.mkdir("cache")
    data_mod.scan_datasets()
    app.run(host='0.0.0.0', port=5000)
