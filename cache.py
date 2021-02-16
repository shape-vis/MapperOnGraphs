import json
import os

import mog.mapper as mapper
import data as data_mod
import mog.graph_io as GraphIO
import layout.initial_layout as layout
import networkx as nx


def get_filter_function(params):
    rank_filter = False if 'rank_filter' not in params else params['rank_filter'].lower() == 'true'
    filename = 'data/' + params['dataset'] + "/" + os.path.splitext(params['datafile'])[0] + "/" + params['filter_func'] + ".json"
    return GraphIO.read_filter_function(filename, rank_filter)


def get_cache_fn(cache_type, dataset, datafile, params=None):
    path = 'cache/' + dataset
    if not os.path.exists(path): os.mkdir(path)

    path += '/' + datafile
    if not os.path.exists(path): os.mkdir(path)

    path += '/' + cache_type

    if params is not None:
        pKeys = list(params.keys())
        pKeys.sort()
        for k in params.keys():
            path += "_" + str(params[k])
    return path + ".json"


def generate_mog(dataset, datafile, filter_func, cover_elem_count, cover_overlap, component_method, link_method,
                 rank_filter):
    mog = mapper.MapperOnGraphs()

    mog_cf = get_cache_fn("mog", dataset, datafile, {
        'filter_func': filter_func,
        'coverN': cover_elem_count,
        'coverOverlap': cover_overlap,
        'component_method': component_method,
        'link_method': link_method,
        'rank_filter': 'false' if rank_filter is None else rank_filter
    })

    if os.path.exists(mog_cf):
        print("  >> " + datafile + " found in mog graph cache")
        mog.load_mog(mog_cf)
    else:
        # Load the graph and filter function
        graph_data, graph = GraphIO.read_json_graph('data/' + dataset + "/" + datafile)
        print(" >> Input Node Count: " + str(graph.number_of_nodes()))
        print(" >> Input Edge Count: " + str(graph.number_of_nodes()))

        values = get_filter_function({'dataset': dataset, 'datafile': datafile, 'filter_func': filter_func,
                                      'rank_filter': rank_filter})

        # Construct the cover
        intervals = int(cover_elem_count)
        overlap = float(cover_overlap)
        cover = mapper.Cover(values, intervals, overlap)

        # Construct MOG
        mog.build_mog(graph, values, cover, component_method, link_method, verbose=graph.number_of_nodes() > 1000)

        if graph.number_of_nodes() > 5000:
            mog.strip_components_from_nodes()

        with open(mog_cf, 'w') as outfile:
            outfile.write(mog.to_json())

    return mog, mog_cf


def get_graph_filename(params):
    filename = get_cache_fn("graph_layout", params['dataset'], params['datafile'])
    if os.path.exists(filename):
        print("  >> " + params['datafile'] + " found in graph layout cache")
    else:
        graph_data, graph = GraphIO.read_json_graph('data/' + params['dataset'] + "/" + params['datafile'])
        layout.initialize_radial_layout(graph)

        with open(filename, 'w') as outfile:
            json.dump(nx.node_link_data(graph), outfile)
    return filename


def save_graph_layout(params, data):
    filename = get_cache_fn("graph_layout", params['dataset'], params['datafile'])
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def get_mog(params):
    tmp = dict(
        filter(lambda x: x[0] in ['dataset', 'datafile', 'filter_func', 'coverN', 'coverOverlap', 'component_method',
                                  'link_method', 'rank_filter'], params.items()))
    print(tmp)

    mog, mog_cf = generate_mog(params['dataset'], params['datafile'],
                               params['filter_func'],
                               params['coverN'], params['coverOverlap'],
                               params['component_method'],
                               params['link_method'], params['rank_filter'])

    print(" >> MOG Node Count: " + str(mog.number_of_nodes()))
    print(" >> MOG Edge Count: " + str(mog.number_of_nodes()))
    print(" >> MOG Compute Time: " + str(mog.compute_time()) + " seconds")

    node_size_filter = int(params['mapper_node_size_filter'])
    if node_size_filter > 0:
        mog.filter_node_size(node_size_filter)

    if params['gcc_only'] == 'true':
        mog.extract_greatest_connect_component()

    return mog.to_json()
