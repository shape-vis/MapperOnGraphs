import networkx as nx
import numpy as np
import functools


def average_geodesic_distance(G):
    ret = {}
    for x in nx.shortest_path_length(G):
        ret[x[0]] = functools.reduce(lambda a, b: a + b, x[1].values()) / (G.number_of_nodes()-1)
    return ret


def density(G):
    sp_len = nx.shortest_path_length(G)
# double
# sum = 0;
# for (int i=0; i < getColumnCount(); i++) {
# float a = (float)get(row_ind, i);
# sum += (double)Math.exp(-a * a / eps);
# }
# return sum;

    return None


def eccentricity(G):
    return nx.eccentricity(G)


def eigen_function(G):
    L = nx.normalized_laplacian_matrix(G)
    e = np.linalg.eigvals(L.A)
    w, v = np.linalg.eig(L.A)
    print(e)
    print(w)
    print(v)


def pagerank(G, _alpha=0.85):
    # return nx.pagerank(G, alpha=_alpha)
    return None
