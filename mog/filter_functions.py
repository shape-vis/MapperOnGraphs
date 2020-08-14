import networkx as nx
import numpy as np
import functools
import math


def density(G, _eps=0.5):
    ret = {}
    for x in nx.shortest_path_length(G):
        scaled = map( lambda a: math.exp( -a * a / _eps ), x[1].values() )
        ret[x[0]] = functools.reduce(lambda a, b: a + b, scaled)
    return ret


def eigen_function(G,_normalized=False):
    if _normalized:
        L = nx.normalized_laplacian_matrix(G)
    else:
        L = nx.laplacian_matrix(G)

    w, v = np.linalg.eigh(L.A)

    eigVal = list(enumerate(w))
    eigVal.sort(key=(lambda e: e[1]))

    ret = []
    for i in range(len(eigVal)):
        ev = eigVal[i]
        ret.append( [ev[1], v[ev[0] ] ] )
    return ret


def pagerank(G, _alpha=0.85):
    return nx.pagerank(G, alpha=_alpha)


def average_geodesic_distance(G):
    ret = {}
    for x in nx.shortest_path_length(G):
        ret[x[0]] = functools.reduce(lambda a, b: a + b, x[1].values()) / (G.number_of_nodes()-1)
    return ret


def eccentricity(G):
    return nx.eccentricity(G)


def fiedler_vector(G,_normalized=False):
    fv = nx.fiedler_vector(G,normalized=_normalized)
    node_list = list(G.nodes)
    ret = {}
    for i in range(len(node_list)):
        ret[ node_list[i]] =fv[i]
    return ret
