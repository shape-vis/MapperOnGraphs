import json
import mog.filter_functions as ff
from networkx.readwrite import json_graph



def read_json_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return [js_graph, json_graph.node_link_graph(js_graph,directed=False,multigraph=False)]

def process_datafile(in_filename,out_filename):
    data, graph = read_json_graph(in_filename)

    data['filter_functions'] = {}

    # Generate AGD
    data['filter_functions']['Average Geodesic Distance'] = 'agd'
    agd = ff.average_geodesic_distance(graph)
    for n in data['nodes']:
        n['agd'] = agd[n['id']]

    # Generate eccentricity
    data['filter_functions']['Eccentricity'] = 'ecc'
    ecc = ff.eccentricity(graph)
    for n in data['nodes']:
        n['ecc'] = ecc[n['id']]

    # Generate pagerank @ 0.85
    data['filter_functions']['PageRank (alpha=0.85)'] = 'pr_0.85'
    pr = ff.pagerank(graph,0.85)
    for n in data['nodes']:
        n['pr_0.85'] = pr[n['id']]

    # Generate fiedler vector
    data['filter_functions']['Fiedler Vector'] = 'fv'
    data['filter_functions']['Fiedler Vector Normalized'] = 'fv_norm'
    fv = ff.fiedler_vector(graph,_normalized=False)
    fv_norm = ff.fiedler_vector(graph,_normalized=True)
    for n in data['nodes']:
        n['fv'] = fv[n['id']]
        n['fv_norm'] = fv_norm[n['id']]

    # Generate density
    data['filter_functions']['Density 0.5'] = 'den_0.5'
    den = ff.density(graph, 0.5)
    for n in data['nodes']:
        n['den_0.5'] = den[n['id']]


    # Generate eigen functions
    eig = ff.eigen_function(graph,_normalized=False)
    eig_norm = ff.eigen_function(graph,_normalized=True)
    data['filter_functions']['Eigen Function (2nd)'] = 'ev_2'
    data['filter_functions']['Eigen Function (3rd)'] = 'ev_3'
    data['filter_functions']['Eigen Function (4th)'] = 'ev_4'
    data['filter_functions']['Eigen Function (5th)'] = 'ev_5'
    data['filter_functions']['Eigen Function Normalized (2nd)'] = 'ev_norm_2'
    data['filter_functions']['Eigen Function Normalized (3rd)'] = 'ev_norm_3'
    data['filter_functions']['Eigen Function Normalized (4th)'] = 'ev_norm_4'
    data['filter_functions']['Eigen Function Normalized (5th)'] = 'ev_norm_5'
    for i in range(len(data['nodes'])):
        n = data['nodes'][i]
        n['ev_2'] = eig[1][1][i]
        n['ev_3'] = eig[2][1][i]
        n['ev_4'] = eig[3][1][i]
        n['ev_5'] = eig[4][1][i]
        n['ev_norm_2'] = eig_norm[1][1][i]
        n['ev_norm_3'] = eig_norm[2][1][i]
        n['ev_norm_4'] = eig_norm[3][1][i]
        n['ev_norm_5'] = eig_norm[4][1][i]

    with open(out_filename, 'w') as outfile:
        json.dump(data, outfile)

    return data

