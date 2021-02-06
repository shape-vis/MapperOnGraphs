import layout.disjointset as disjointset
import networkx as nx


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
