import json
import time

import networkx as nx
import statistics as stats
import mog.graph_io as GraphIO
import layout.initial_layout as layout


class Cover:
    def __init__(self, values, intervals, overlap):
        self.intervals = intervals
        self.overlap = overlap

        minv = values[min(values, key=(lambda k: values[k]))]
        maxv = values[max(values, key=(lambda k: values[k]))]

        per_interval = (maxv - minv) / intervals
        overlap_amnt = per_interval * overlap

        self.cover = []
        for x in range(0, intervals):
            start = minv + per_interval * x - overlap_amnt
            end = minv + per_interval * (x + 1) + overlap_amnt
            self.cover.append({'level': x, 'range': [start, end]})

    def get_cover_elements(self):
        return self.cover

    def get_intervals(self):
        return self.intervals

    def get_overlap(self):
        return self.overlap


def _get_components(graph: nx.classes.graph.Graph, values, cover: Cover, component_method):
    ret = []
    for ce in cover.get_cover_elements():

        filtered = list(filter(lambda v: ce['range'][0] <= values[v] <= ce['range'][1], values))
        subg = graph.subgraph(filtered)

        if subg.number_of_edges() == 0:
            components = nx.connected_components(subg)
        elif component_method == 'modularity':
            components = nx.algorithms.community.greedy_modularity_communities(subg)
        elif component_method == 'async_label_prop':
            components = nx.algorithms.community.asyn_lpa_communities(subg)
        elif component_method == 'label_prop':
            components = nx.algorithms.community.label_propagation_communities(subg)
        # elif component_method == 'centrality':
        #     components = nx.algorithms.community.girvan_newman(subg)
        else:
            components = nx.connected_components(subg)

        for comp in components:
            ret.append({'cover':ce, 'components':comp})

    return ret


def _get_nodes(values, components):
    nodes = []
    for component in components:
        comp_vals = list(map((lambda _l: values[_l]), component['components']))
        nodes.append({'id': 'mn' + str(len(nodes)),
                      'cover': component['cover']['level'],
                      'min_v': min(comp_vals),
                      'max_v': max(comp_vals),
                      'avg_v': stats.mean(comp_vals),
                      'comp_len': len(component['components']),
                      'comp': list(component['components'])
                      })
    return nodes


def _get_links_by_node_overlap(nodes):
    links = []
    for i in range(0, len(nodes)):
        node_set_i = set(nodes[i]['comp'])
        for j in range(i + 1, len(nodes)):
            w = len(node_set_i & set(nodes[j]['comp']))
            if w > 0:
                if nodes[i]['min_v'] < nodes[j]['min_v']:
                    links.append({"source": nodes[i]['id'], "target": nodes[j]['id'], 'value': w})
                else:
                    links.append({"target": nodes[i]['id'], "source": nodes[j]['id'], 'value': w})
    return links


def _get_links_by_graph_cut(input_graph: nx.classes.graph.Graph, mapper_nodes):
    node_map = {}
    for n in input_graph.nodes:
        node_map[n] = []
    for m in mapper_nodes:
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


class MapperOnGraphs:
    def __init__(self):
        self.info = {}
        self.mapper_graph = None

    def load_mog(self, input_file):
        data, graph = GraphIO.read_json_graph(input_file)
        self.info = data['info']
        self.mapper_graph = graph

    def build_mog(self, input_graph: nx.classes.graph.Graph, values, cover: Cover,
                  component_method='connected_components', link_method='overlap', verbose=False):

        self.info = {
            'component_method': component_method,
            'link_method': link_method,
            'cover_overlap': cover.get_overlap(),
            'cover_intervals': cover.get_intervals(),
            'cover': cover.get_cover_elements()
        }

        start_time = time.time()

        if verbose:
            print("MapperOnGraphs: Step 1 of 4")

        components = _get_components(input_graph, values, cover, component_method)

        if verbose:
            print("MapperOnGraphs: Step 2 of 4")

        nodes = _get_nodes(values, components)

        if verbose:
            print("MapperOnGraphs: Step 3 of 4")

        if link_method == 'connectivity':
            links = _get_links_by_graph_cut(input_graph, nodes)
        else:
            links = _get_links_by_node_overlap(nodes)

        if verbose:
            print("MapperOnGraphs: Step 4 of 4")

        self.mapper_graph = nx.readwrite.node_link_graph({'nodes': nodes, 'links': links}, directed=False, multigraph=False)

        self.info['compute_time'] = time.time() - start_time

    def compute_time(self):
        # return self.end_time-self.start_time
        return self.info['compute_time']

    def number_of_nodes(self):
        return self.mapper_graph.number_of_nodes()

    def number_of_edges(self):
        return self.mapper_graph.number_of_edges()

    def extract_greatest_connect_component(self):
        gcc = max(nx.connected_components(self.mapper_graph), key=len)
        self.mapper_graph = self.mapper_graph.subgraph(gcc)

    def strip_components_from_nodes(self):
        for (n, data) in self.mapper_graph.nodes.items():
            del data['comp']

    def filter_node_size(self, minimum_node_size):
        component_sizes = {}

        for (n, data) in self.mapper_graph.nodes.items():
            component_sizes[n] = data['component_count']

        ns = list(filter((lambda node: component_sizes[node] > minimum_node_size), self.mapper_graph.nodes()))
        self.mapper_graph = self.mapper_graph.subgraph(ns)

    def to_json(self):
        if self.mapper_graph.number_of_nodes() < 2500:
            layout.initialize_radial_layout(self.mapper_graph)
        # layout.initialize_vertical_layout(self.mapper_graph)
        json_data = nx.node_link_data(self.mapper_graph)
        json_data['info'] = self.info
        del json_data['directed']
        del json_data['multigraph']
        del json_data['graph']
        return json.dumps(GraphIO.round_floats(json_data), separators=(',', ':'))

    def save_json(self, out_file_path):
        if self.mapper_graph.number_of_nodes() < 2500:
            layout.initialize_radial_layout(self.mapper_graph)
        json_data = nx.node_link_data(self.mapper_graph)
        json_data['info'] = self.info
        del json_data['directed']
        del json_data['multigraph']
        del json_data['graph']
        with open(out_file_path, 'w') as outfile:
            json.dump(GraphIO.round_floats(json_data), outfile, separators=(',', ':'))
