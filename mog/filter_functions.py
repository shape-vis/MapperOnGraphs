import networkx as nx
import numpy as np
import functools
import math


def density(g, _eps=0.5):
    ret = {}
    for x in nx.shortest_path_length(g):
        scaled = map(lambda a: math.exp(-a * a / _eps), x[1].values())
        ret[x[0]] = functools.reduce(lambda a, b: a + b, scaled)
    return ret


def eigen_function(g, _weight, _normalized=False):
    order = list(g.nodes())
    if _normalized:
        lap = nx.normalized_laplacian_matrix(g, nodelist=order, weight=_weight)
    else:
        lap = nx.laplacian_matrix(g, nodelist=order, weight=_weight)

    #print(lap.A)
    w, v = np.linalg.eigh(lap.A)

    eigval = list(enumerate(w))

    ret = []
    for i in range(len(w)):
        eval = w[i]
        evec = v[:,i]
        out_evec = {}
        for j in range(len(order)):
            out_evec[order[j]] = evec[j]
        ret.append([eval, out_evec])

    ret.sort(key=(lambda e: e[0]))

    return ret


def pagerank(g, _alpha=0.85):
    return nx.pagerank(g, alpha=_alpha)


def average_geodesic_distance(g):
    ret = {}
    for x in nx.shortest_path_length(g):
        ret[x[0]] = functools.reduce(lambda a, b: a + b, x[1].values()) / (g.number_of_nodes() - 1)
    return ret


def eccentricity(g):
    return nx.eccentricity(g)


def fiedler_vector(g, _weight, _normalized=False):
    fv = nx.fiedler_vector(g, weight=_weight, normalized=_normalized)
    node_list = list(g.nodes)
    ret = {}
    for i in range(len(node_list)):
        ret[node_list[i]] = fv[i]
    return ret
