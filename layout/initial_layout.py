import layout.disjointset as disjointset
import networkx as nx
import math


def get_mst(g):
    mst = nx.empty_graph()
    mst.add_nodes_from(g)

    djs = disjointset.DisjointSet(g.nodes(), lambda x: x)

    links = list(g.edges(data=True))
    links.sort(reverse=True, key=(lambda x: x[2]['value'] if 'value' in x[2] else 1))
    for link in links:
        if not djs.findKey(link[0]) == djs.findKey(link[1]):
            mst.add_edge(link[0], link[1], value=link[2]['value'] if 'value' in link[2] else 1)
            djs.unionKey(link[0], link[1])

    return mst


def abstract_layout(g, mst):
    proc_list = [{'id': list(g.nodes())[0], 'level': 0, 'range': [0, 1]}]
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
    return visited


def initialize_vertical_layout(g):
    mst = get_mst(g)
    abs_layout = abstract_layout(g, mst)

    positions = {}
    for node in abs_layout.values():
        positions[node['id']] = {'x': (node['range'][0] + node['range'][1]) / 2 * 600, 'y': 50 * node['level']}

    nx.set_node_attributes(g, positions)
    return g


def initialize_radial_layout(g):
    mst = get_mst(g)
    abs_layout = abstract_layout(g, mst)

    positions = {}
    for node in abs_layout.values():
        pos = (node['range'][0] + node['range'][1]) / 2
        x = node['level'] * 50 * math.cos(pos * math.pi * 2)
        y = node['level'] * 50 * math.sin(pos * math.pi * 2)
        positions[node['id']] = {'x': x + 300, 'y': y + 300}

    nx.set_node_attributes(g, positions)
    return g
