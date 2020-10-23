import json
import time

import networkx as nx
import statistics as stats


# def fill_missing_diffuse_avg(graph, values, missing_vals):
#     for n in missing_vals:
#         tot = 0
#         cnt = 0
#         for x in graph.neighbors(n):
#             if x in values:
#                 tot += values[x]
#                 cnt += 1
#
#         if cnt > 0:
#             values[n] = tot / cnt
#
#
# def get_min_max(values):
#     minkey = min(values, key=(lambda k: values[k]))
#     maxkey = max(values, key=(lambda k: values[k]))
#     return [values[minkey], values[maxkey]]


def form_cover(values, intervals, overlap):

    minv = values[ min(values, key=(lambda k: values[k])) ]
    maxv = values[ max(values, key=(lambda k: values[k])) ]

    # minmax = get_min_max(values)
    per_interval = (maxv - minv) / intervals
    overlap_amnt = per_interval * overlap

    ret = []
    for x in range(0, intervals):
        start = minv + per_interval * x - overlap_amnt
        end = minv + per_interval * (x + 1) + overlap_amnt
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
        nodes.append({'id': 'mapper_node_' + str(len(nodes)),
                      'min_value': min(comp_vals),
                      'max_value': max(comp_vals),
                      'avg_value': stats.mean(comp_vals),
                      'component_count': len(x),
                      'components': list(x)
                    })
    return nodes


def get_links_by_node_overlap(nodes):
    links = []
    for i in range(0, len(nodes)):
        node_set_i = set(nodes[i]['components'])
        for j in range(i + 1, len(nodes)):
            w = len(node_set_i & set(nodes[j]['components']))
            if w > 0:
                if nodes[i]['min_value'] < nodes[j]['min_value']:
                    links.append({"source": nodes[i]['id'], "target": nodes[j]['id'], 'value': w})
                else:
                    links.append({"target": nodes[i]['id'], "source": nodes[j]['id'], 'value': w})
    return links


def get_links_by_edges(input_graph: nx.classes.graph.Graph, mapper_nodes):
    node_map = {}
    for n in input_graph.nodes:
        node_map[n] = []
    for m in mapper_nodes:
        for n in m['components']:
            node_map[n].append(m)

    edge_map = {}
    for e in input_graph.edges:
        for l in node_map[e[0]]:
            for r in node_map[e[1]]:
                if l == r: continue
                id = (l['id'],r['id']) if l['id']<r['id'] else (r['id'],l['id'])
                if id in edge_map:
                    edge_map[id] += 1
                else:
                    edge_map[id] = 1

    links = []
    for e in edge_map:
        links.append({"source": e[0], "target": e[1], 'value': edge_map[e]})
    #     print(str(e) + " " + str(edge_map[e]))
    # #print(node_map)
    # for i in range(0, len(mapper_nodes)):
    #     set_i = set(mapper_nodes[i]['components'])
    #     for j in range(i + 1, len(mapper_nodes)):
    #         set_j = set(mapper_nodes[j]['components'])
    #         w = nx.cut_size( input_graph, set_i, set_j )
    #         if w > 0:
    #             if mapper_nodes[i]['min_value'] < mapper_nodes[j]['min_value']:
    #                 links.append({"source": mapper_nodes[i]['id'], "target": mapper_nodes[j]['id'], 'value': w})
    #             else:
    #                 links.append({"target": mapper_nodes[i]['id'], "source": mapper_nodes[j]['id'], 'value': w})
    #
    # for l in links:
    #     print(l)
    return links


class MapperOnGraphs:
    def __init__(self, input_graph: nx.classes.graph.Graph, values, cover, component_method='connected_components', link_method='overlap'):
        self.start_time = time.time()

        print("A")
        if component_method == 'modularity':
            self.components = get_modularity_components(input_graph, values, cover)
        elif component_method == 'async_label_prop':
            self.components = get_async_label_prop_components(input_graph, values, cover)
        elif component_method == 'label_prop':
            self.components = get_label_prop_components(input_graph, values, cover)
        elif component_method == 'centrality':
            self.components = get_centrality_components(input_graph, values, cover)
        else:
            self.components = get_connected_components(input_graph, values, cover)

        print("B")
        self.nodes = get_nodes(values, self.components)

        print("C")
        if link_method == 'connectivity':
            self.links = get_links_by_edges(input_graph, self.nodes)
        else:
            self.links = get_links_by_node_overlap(self.nodes)
        print("D")

        self.mapper_graph = nx.readwrite.node_link_graph({'nodes': self.nodes, 'links': self.links})
        print("E")

        self.end_time = time.time()

    def compute_time(self):
        return self.end_time-self.start_time

    def number_of_nodes(self):
        return self.mapper_graph.number_of_nodes()

    def number_of_edges(self):
        return self.mapper_graph.number_of_edges()

    def extract_greatest_connect_component(self):
        gcc = max(nx.connected_components(self.mapper_graph), key=len)
        self.mapper_graph = self.mapper_graph.subgraph(gcc)

    def strip_components_from_nodes(self):
        for (n,data) in self.mapper_graph.nodes.items():
            del data['components']

    def filter_node_size(self, minimum_node_size):
        node_dict = {}
        for n in self.nodes:
            node_dict[n['id']] = n

        ns = list(filter((lambda node: len(node_dict[node]['components']) > minimum_node_size), self.mapper_graph.nodes()))
        self.mapper_graph = self.mapper_graph.subgraph(ns)

    def to_json(self):
        return json.dumps(nx.node_link_data(self.mapper_graph))
