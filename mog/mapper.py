import networkx as nx
from functools import reduce
import statistics as stats


def fill_missing_diffuse_avg(G, values, missing_vals):
    for n in missing_vals:
        sum = 0
        cnt = 0
        for x in G.neighbors(n):
            if x in values:
                sum += values[x]
                cnt += 1

        if cnt > 0:
            values[n] = sum / cnt


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
        ret.append( [start,end] )

    return ret


def get_components(G, values, cover):
    ret = []
    for ce in cover:
        filtered = list(filter(lambda v: ce[0] <= values[v] <= ce[1], values))
        subg = G.subgraph(filtered)
        ret += nx.connected_components(subg)
    return ret


def get_nodes(values, components):
    nodes = []
    for x in components:
        comp_vals = list(map((lambda _x: values[_x]), x))
        minV = min(comp_vals)
        maxV = max(comp_vals)
        avg = stats.mean(comp_vals)
        nodes.append({'id': 'mapper_node_' + str(len(nodes)), 'min_value': minV, 'max_value': maxV,
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
