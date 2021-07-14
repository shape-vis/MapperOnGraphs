import networkx as nx
import json


def read_json_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return [js_graph, nx.readwrite.node_link_graph(js_graph, directed=False, multigraph=False)]


def read_graph_file(filename):
    f = open(filename)
    graph = nx.Graph()
    for _x in f:
        x = _x.split()
        if x[0] == 'n':
            graph.add_node(x[1])
        if x[0] == 'e':
            graph.add_edge(x[1], x[2], value=1)
    return [None, graph]


def read_tsv_graph_file(filename):
    f = open(filename)
    graph = nx.Graph()
    for _x in f:
        if _x[0] == '#': continue
        x = _x.split()
        if not graph.has_node(x[0]):
            graph.add_node(x[0])
        if not graph.has_node(x[1]):
            graph.add_node(x[1])
        if graph.has_edge(x[0], x[1]):
            print("edge exists")
        if len(x) == 2:
            graph.add_edge(x[0], x[1], value=1)
        else:
            graph.add_edge(x[0], x[1], value=float(x[2]))
    return [None, graph]


def read_filter_function(filename, ranked=False):
    with open(filename) as json_file:
        ff = json.load(json_file)

    if ranked:
        return ff['ranked']
    return ff['data']


def round_floats(o):
    if isinstance(o, float): return round(o, 4)
    if isinstance(o, dict): return {k: round_floats(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [round_floats(x) for x in o]
    return o


def write_json_data(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(round_floats(data), outfile, separators=(',', ':'))


def write_json_graph(filename, graph):
    write_json_data(filename, nx.node_link_data(graph))
