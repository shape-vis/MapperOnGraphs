import json
import networkx as nx
import statistics as stats


def fill_missing_diffuse_avg(graph, values, missing_vals):
    for n in missing_vals:
        tot = 0
        cnt = 0
        for x in graph.neighbors(n):
            if x in values:
                tot += values[x]
                cnt += 1

        if cnt > 0:
            values[n] = tot / cnt


def get_min_max(values):
    minkey = min(values, key=(lambda k: values[k]))
    maxkey = max(values, key=(lambda k: values[k]))
    return [values[minkey], values[maxkey]]


def form_cover(values, intervals, overlap):
    minmax = get_min_max(values)
    per_interval = (minmax[1] - minmax[0]) / intervals
    overlap_amnt = per_interval * overlap

    ret = []
    for x in range(0, intervals):
        start = minmax[0] + per_interval * x - overlap_amnt
        end = minmax[0] + per_interval * (x + 1) + overlap_amnt
        ret.append([start, end])

    return ret


def get_connected_components(graph, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = graph.subgraph(filtered)
        ret += nx.connected_components(subg)
    return ret


def get_modularity_components(graph, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = graph.subgraph(filtered)
        if subg.number_of_edges() == 0:
            ret += nx.connected_components(subg)
        else:
            ret += list(nx.algorithms.community.greedy_modularity_communities(subg))
    return ret


def get_async_label_prop_components(graph, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = graph.subgraph(filtered)
        ret += list(nx.algorithms.community.asyn_lpa_communities(subg))
    return ret


def get_label_prop_components(graph, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = graph.subgraph(filtered)
        ret += list(nx.algorithms.community.label_propagation_communities(subg))
    return ret


def get_centrality_components(graph, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = graph.subgraph(filtered)
        ret += list(nx.algorithms.community.girvan_newman(subg))
    return ret


def get_nodes(values, components):
    nodes = []
    for x in components:
        comp_vals = list(map((lambda _x: values[_x]), x))
        min_val = min(comp_vals)
        max_val = max(comp_vals)
        avg = stats.mean(comp_vals)
        nodes.append({'id': 'mapper_node_' + str(len(nodes)), 'min_value': min_val, 'max_value': max_val,
                      'avg_value': avg, 'components': list(x)})
    return nodes


def get_links(nodes):
    links = []
    for i in range(0, len(nodes)):
        node_set_i = set(nodes[i]['components'])
        for j in range(i + 1, len(nodes)):
            w = len(node_set_i & set(nodes[j]['components']))
            if w > 0:
                links.append({"source": nodes[i]['id'], "target": nodes[j]['id'], 'value': w})
    return links


class MapperOnGraphs:
    def __init__(self, input_graph: nx.classes.graph.Graph, values, cover, component_method='connected_components'):

        if component_method == 'modularity':
            self.components = get_modularity_components(input_graph, values, cover)
        elif component_method == 'async_label_prop':
            self.components = get_async_label_prop_components(input_graph, values, cover)
        elif component_method == 'label_prop':
            self.components = get_label_prop_components(input_graph, values, cover)
        elif component_method == 'centrality':
            self.components = get_centrality_components(input_graph, values, cover)
        else:
            self.components = get_async_label_prop_components(input_graph, values, cover)

        self.nodes = get_nodes(values, self.components)
        self.links = get_links(self.nodes)
        self.mapper_graph = nx.readwrite.node_link_graph({'nodes': self.nodes, 'links': self.links})

    def extract_greatest_connect_component(self):
        gcc = max(nx.connected_components(self.mapper_graph), key=len)
        self.mapper_graph = self.mapper_graph.subgraph(gcc)

    def filter_node_size(self, minimum_node_size):
        node_dict = {}
        for n in self.nodes:
            node_dict[n['id']] = n

        ns = list(filter((lambda node: len(node_dict[node]['components']) > minimum_node_size), self.mapper_graph.nodes()))
        self.mapper_graph = self.mapper_graph.subgraph(ns)

    def to_json(self):
        return json.dumps(nx.node_link_data(self.mapper_graph))
