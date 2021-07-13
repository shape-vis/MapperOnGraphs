import networkx as nx
import numpy as np
import functools
import math
import time
import graph_io as GraphIO


def average_geodesic_distance(g, _weight, _out_path=None):
    start = time.time()
    data = {}

    for x in nx.shortest_path_length(g, weight=_weight):
        data[x[0]] = functools.reduce(lambda a, b: a + b, x[1].values()) / (g.number_of_nodes() - 1)

    ret = {'name': 'agd', 'num_of_nodes': g.number_of_nodes(), 'num_of_edges': g.number_of_edges(), 'weight': _weight,
           'process_time': (time.time() - start), 'data': data}

    if _out_path is not None:
        GraphIO.write_json_data(_out_path, ret)

    return ret


def eccentricity(g, _out_path=None):
    start = time.time()
    data = nx.eccentricity(g)

    ret = {'name': 'eccentricity', 'num_of_nodes': g.number_of_nodes(), 'num_of_edges': g.number_of_edges(),
           'process_time': (time.time() - start), 'data': data}

    if _out_path is not None:
        GraphIO.write_json_data(_out_path, ret)

    return ret


def density(g, _weight, _eps=0.5, _out_path=None):
    start = time.time()
    data = {}

    for x in nx.shortest_path_length(g, weight=_weight):
        scaled = map(lambda a: math.exp(-a * a / _eps), x[1].values())
        data[x[0]] = functools.reduce(lambda a, b: a + b, scaled)

    ret = {'name': 'density', 'eps': _eps, 'weight': _weight, 'num_of_nodes': g.number_of_nodes(),
           'num_of_edges': g.number_of_edges(), 'process_time': (time.time() - start), 'data': data}

    if _out_path is not None:
        GraphIO.write_json_data(_out_path, ret)

    return ret


def eigen_function(g, _weight, _normalized=False, _which_eig=None, _out_path=None):
    start = time.time()
    order = list(g.nodes())
    if _normalized:
        lap = nx.normalized_laplacian_matrix(g, nodelist=order, weight=_weight)
    else:
        lap = nx.laplacian_matrix(g, nodelist=order, weight=_weight)

    w, v = np.linalg.eigh(lap.A)

    data = []
    for i in range(len(w)):
        eval = w[i]
        evec = v[:,i]
        out_evec = {}
        for j in range(len(order)):
            out_evec[order[j]] = evec[j]
        data.append([eval, out_evec])

    data.sort(key=(lambda e: e[0]))
    end = time.time()

    if _which_eig is not None and _out_path is not None:
        for ev in _which_eig:
            if g.number_of_nodes() > ev:
                ev_path = _out_path.format(str(ev))
                res = {'name': 'eigen', 'eigen': ev, 'normalized': _normalized, 'num_of_nodes': g.number_of_nodes(),
                       'num_of_edges': g.number_of_edges(), 'process_time': (end - start), 'data': data[ev][1]}
                GraphIO.write_json_data(ev_path, res)

    ret = {'name': 'eigen', 'normalized': _normalized, 'process_time': (end - start), 'data': data}

    return ret




def fiedler_vector(g, _weight, _normalized=False, _out_path=None):
    try:
        start = time.time()

        fv = nx.fiedler_vector(g, weight=_weight, normalized=_normalized)
        node_list = list(g.nodes)
        data = {}
        for i in range(len(node_list)):
            data[node_list[i]] = fv[i]

        ret = {'name': 'fiedler', 'normalized': _normalized, 'weight': _weight, 'num_of_nodes': g.number_of_nodes(),
               'num_of_edges': g.number_of_edges(), 'process_time': (time.time() - start), 'data': data}

        if _out_path is not None:
            GraphIO.write_json_data(_out_path, ret)

        return ret

    except nx.exception.NetworkXError:
        print(">>> FAILED (fiedler_vector): processing error. maybe graph not connected?")

    return None


def pagerank(g, _weight, _alpha=0.85, _out_path=None):
    start = time.time()
    data = nx.pagerank(g, weight=_weight, alpha=_alpha)

    ret = {'name': 'pagerank', 'alpha': _alpha, 'weight': _weight, 'num_of_nodes': g.number_of_nodes(),
           'num_of_edges': g.number_of_edges(), 'process_time': (time.time() - start), 'data': data}

    if _out_path is not None:
        GraphIO.write_json_data(_out_path, ret)

    return ret

