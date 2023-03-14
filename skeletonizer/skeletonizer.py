import json
import time

import networkx as nx
import statistics as stats
import mog.graph_io as GraphIO
import layout.initial_layout as layout



def _get_communities(graph: nx.classes.graph.Graph, community_method, resolution=1):
    if graph.number_of_edges() == 0:
        return nx.connected_components(graph)
    elif community_method == 'modularity':
        return nx.algorithms.community.greedy_modularity_communities(graph, resolution=resolution)
    elif community_method == 'async_label_prop':
        return nx.algorithms.community.asyn_lpa_communities(graph)
    elif community_method == 'label_prop':
        return nx.algorithms.community.label_propagation_communities(graph)
    elif community_method == 'centrality':
        return nx.algorithms.community.girvan_newman(graph)
    elif community_method == 'louvain':
        return nx.algorithms.community.louvain_communities(graph, resolution=resolution)
    else:
        return nx.connected_components(graph)


def _get_nodes(communities):
    nodes = []
    for community in communities:
        nodes.append({'id': 'mn' + str(len(nodes)),
                      'comp_len': len(community),
                      'comp': list(community)
                      })
    return nodes


def _get_links_by_graph_cut(input_graph: nx.classes.graph.Graph, skeleton_nodes):
    node_map = {}
    for n in input_graph.nodes:
        node_map[n] = []
    for m in skeleton_nodes:
        for n in m['comp']:
            node_map[n].append(m)

    edge_map = {}
    for e in input_graph.edges:
        for l in node_map[e[0]]:
            for r in node_map[e[1]]:
                if l == r: continue
                id = (l['id'], r['id']) if l['id'] < r['id'] else (r['id'], l['id'])
                if id in edge_map:
                    edge_map[id] += 1
                else:
                    edge_map[id] = 1

    links = []
    for e in edge_map:
        links.append({"source": e[0], "target": e[1], 'value': edge_map[e]})

    return links


class Skeltonizer:
    def __init__(self):
        self.info = {}
        self.skelton_graph = None

    def load_skeleton(self, input_file):
        data, graph = GraphIO.read_json_graph(input_file)
        self.info = data['info']
        self.skelton_graph = graph

    def build_skeleton(self, input_graph: nx.classes.graph.Graph, community_method='connected_components', community_resolution=1, verbose=False):

        self.info = {
            'community_method': community_method,
        }

        start_time = time.time()

        if verbose:
            print("Skeltonizer: Step 1 of 4")

        communities = _get_communities(input_graph, community_method, resolution=community_resolution)

        if verbose:
            print("Skeltonizer: Step 2 of 4")

        nodes = _get_nodes(communities)

        if verbose:
            print("Skeltonizer: Step 3 of 4")

        links = _get_links_by_graph_cut(input_graph, nodes)

        if verbose:
            print("Skeltonizer: Step 4 of 4")

        self.skelton_graph = nx.readwrite.node_link_graph({'nodes': nodes, 'links': links}, directed=False, multigraph=False)

        self.info['compute_time'] = time.time() - start_time

    def compute_time(self):
        # return self.end_time-self.start_time
        return self.info['compute_time']

    def number_of_nodes(self):
        return self.skelton_graph.number_of_nodes()

    def number_of_edges(self):
        return self.skelton_graph.number_of_edges()

    def extract_greatest_connect_component(self):
        gcc = max(nx.connected_components(self.skelton_graph), key=len)
        self.skelton_graph = self.skelton_graph.subgraph(gcc)

    def strip_components_from_nodes(self):
        for (n, data) in self.skelton_graph.nodes.items():
            del data['comp']

    def filter_node_size(self, minimum_node_size):
        component_sizes = {}

        for (n, data) in self.skelton_graph.nodes.items():
            component_sizes[n] = data['component_count']

        ns = list(filter((lambda node: component_sizes[node] > minimum_node_size), self.skelton_graph.nodes()))
        self.skelton_graph = self.skelton_graph.subgraph(ns)

    def to_json(self):
        if self.skelton_graph.number_of_nodes() < 2500:
            layout.initialize_radial_layout(self.skelton_graph)
        # layout.initialize_vertical_layout(self.mapper_graph)
        json_data = nx.node_link_data(self.skelton_graph)
        json_data['info'] = self.info
        del json_data['directed']
        del json_data['multigraph']
        del json_data['graph']
        return json.dumps(GraphIO.round_floats(json_data), separators=(',', ':'))

    def save_json(self, out_file_path):
        if self.skelton_graph.number_of_nodes() < 2500:
            layout.initialize_radial_layout(self.skelton_graph)
        json_data = nx.node_link_data(self.skelton_graph)
        json_data['info'] = self.info
        del json_data['directed']
        del json_data['multigraph']
        del json_data['graph']
        with open(out_file_path, 'w') as outfile:
            json.dump(GraphIO.round_floats(json_data), outfile, separators=(',', ':'))
