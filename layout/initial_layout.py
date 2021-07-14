import layout.graph_mst as graph_mst
import networkx as nx
import math
import sys


def __map(val, in_min, in_max, out_min, out_max):
    t = (val - in_min) / (in_max - in_min)
    return out_min + (out_max - out_min) * t


def __abstract_layout(g: nx.graph.Graph, use_best_root=True):
    mst = graph_mst.get_mst(g)

    if not use_best_root:
        # this method just selects the first node of mst, whatever it is
        central_node = list(mst.nodes())[0]
    else:
        # this (confusing) method finds the node with the shortest path to all other nodes
        central_node = min(nx.shortest_path_length(mst), key=lambda n: n[1][max(n[1], key=n[1].get)])[0]

    proc_list = [{'id': central_node, 'level': 0, 'range': [0, 1]}]
    visited = {}
    while len(proc_list) > 0:
        node = proc_list.pop()
        visited[node['id']] = node
        neighbors = list(mst.neighbors(node['id']))
        for i, neighbor in enumerate(neighbors):
            if neighbor not in visited:
                b = node['range'][0] + (node['range'][1] - node['range'][0]) * (i / len(neighbors))
                e = node['range'][0] + (node['range'][1] - node['range'][0]) * ((i + 1) / len(neighbors))
                proc_list.append({'id': neighbor, 'level': node['level'] + 1, 'range': [b, e]})
    tree_depth = 1 + visited[max(visited, key=lambda n: visited[n]['level'])]['level']
    return visited, tree_depth


def initialize_vertical_layout(g, x_range=[0, 500], y_range=[0, 500]):
    abs_layout, tree_depth = __abstract_layout(g)

    positions = {}
    for node in abs_layout.values():
        x = __map( (node['range'][0] + node['range'][1]) / 2, 0, 1, x_range[0], x_range[1])
        y = __map(node['level'], 0, tree_depth-1, y_range[0], y_range[1])
        positions[node['id']] = {'x': x, 'y': y}

    nx.set_node_attributes(g, positions)
    return g


def initialize_radial_layout(g, x_range=[0, 500], y_range=[0, 500]):
    abs_layout, tree_depth = __abstract_layout(g)

    if tree_depth == 1: tree_depth = 2

    cen = [(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2]
    rad = min(x_range[1] - x_range[0], y_range[1] - y_range[0]) / 2

    positions = {}
    for node in abs_layout.values():
        a = (node['range'][0] + node['range'][1]) / 2 * math.pi * 2
        r = __map(node['level'], 0, tree_depth - 1, 0, rad)
        positions[node['id']] = {'x': cen[0] + r * math.cos(a), 'y': cen[1] + r * math.sin(a)}

    nx.set_node_attributes(g, positions)
    return g
