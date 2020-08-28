import fnmatch
import json
import multiprocessing
import ntpath
import os
import networkx as nx

import mog.filter_functions as ff

data_sets = {}

filter_function_names = {'agd': 'Average Geodesic Distance',
                         'ecc': 'Eccentricity',
                         'pr_0_85': 'PageRank (alpha=0.85)',
                         'fv': 'Fiedler Vector',
                         'fv_norm': 'Fiedler Vector Normalized',
                         'den_0_5': 'Density 0.5',
                         'ev_2': 'Eigen Function (2nd)',
                         'ev_3': 'Eigen Function (3rd)',
                         'ev_4': 'Eigen Function (4th)',
                         'ev_5': 'Eigen Function (5th)',
                         'ev_6': 'Eigen Function (6th)',
                         'ev_norm_2': 'Eigen Function Normalized (2nd)',
                         'ev_norm_3': 'Eigen Function Normalized (3rd)',
                         'ev_norm_4': 'Eigen Function Normalized (4th)',
                         'ev_norm_5': 'Eigen Function Normalized (5th)',
                         'ev_norm_6': 'Eigen Function Normalized (6th)'}


def read_json_graph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return [js_graph, nx.readwrite.node_link_graph(js_graph, directed=False, multigraph=False)]


def write_json_data(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def process_datafile(in_filename):
    print("Processing: " + in_filename)
    data, graph = read_json_graph(in_filename)

    '''
    cc = list(nx.connected_components(graph))
    if len(cc) > 1:
        for _cc in cc:
            print( len(_cc) )
    '''

    out_filename = "data/"
    if graph.number_of_nodes() < 100:
        out_filename += "small/"
    elif graph.number_of_nodes() < 1000:
        out_filename += "medium/"
    else:
        out_filename += "large/"
    out_filename += ntpath.basename(in_filename)

    print("                     => " + out_filename)

    out_dir = os.path.splitext(out_filename)[0]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Generate AGD
    if not os.path.exists(out_dir + "/agd.json"):
        write_json_data(out_dir + "/agd.json", ff.average_geodesic_distance(graph))

    # Generate eccentricity
    if not os.path.exists(out_dir + "/ecc.json"):
        write_json_data(out_dir + "/ecc.json", ff.eccentricity(graph))

    # Generate pagerank @ 0.85
    if not os.path.exists(out_dir + "/pr_0_85.json"):
        write_json_data(out_dir + "/pr_0_85.json", ff.pagerank(graph, 0.85))

    # Generate fiedler vector
    if not os.path.exists(out_dir + "/fv.json"):
        write_json_data(out_dir + "/fv.json", ff.fiedler_vector(graph, _weight='value', _normalized=False))

    # Generate fiedler vector normalized
    if not os.path.exists(out_dir + "/fv_norm.json"):
        write_json_data(out_dir + "/fv_norm.json", ff.fiedler_vector(graph, _weight='value', _normalized=True))

    # Generate density
    if not os.path.exists(out_dir + "/den_0_5.json"):
        write_json_data(out_dir + "/den_0_5.json", ff.density(graph, 0.5))

    # Generate eigen functions
    if not os.path.exists(out_dir + "/ev_2.json"):
        eig = ff.eigen_function(graph, _weight='value', _normalized=False)
        eig_norm = ff.eigen_function(graph, _weight='value', _normalized=True)
        for ev in range(2, 6):
            write_json_data(out_dir + "/ev_" + str(ev) + ".json", eig[ev][1])
            write_json_data(out_dir + "/ev_norm_" + str(ev) + ".json", eig_norm[ev][1])

    write_json_data(out_filename, data)

    return data


data_gen = ["data/source/not_in_paper/football_out.JSON", "data/source/not_in_paper/airport6632_gcc.JSON",
            "data/source/not_in_paper/barabasi_albert_graph(10,5).json",
            "data/source/not_in_paper/barabasi_albert_graph(20,10).json",
            "data/source/not_in_paper/barabasi_albert_graph(20,3).json",
            "data/source/not_in_paper/barabasi_albert_graph(50,40).json",
            "data/source/not_in_paper/bcsstk20.json", "data/source/not_in_paper/bcsstk22.json",
            "data/source/not_in_paper/beach.json", "data/source/not_in_paper/caveman_graph[3,5].json",
            "data/source/not_in_paper/caveman_graph[7,4].json", "data/source/not_in_paper/chvatal_graph.json",
            "data/source/not_in_paper/corr1.json", "data/source/not_in_paper/davis_southern_women_graph.json",
            "data/source/realworld/circle_of_science.json", "data/source/realworld/USair97.json"]

for file in data_gen:
    p = multiprocessing.Process(target=process_datafile, args=[file])
    p.start()

    # Wait for 20 seconds or until process finishes
    p.join(1)

    # If thread is still active
    if p.is_alive():
        print("   Taking too long, skipping remaining calculations")

        # Terminate
        p.terminate()
        p.join()


for d0 in os.listdir("data/"):
    if os.path.isdir("data/" + d0):
        data_sets[d0] = {}
        for d1 in os.listdir("data/" + d0):
            if fnmatch.fnmatch(d1.lower(), "*.json"):
                ff_dir = os.path.splitext("data/" + d0 + '/' + d1)[0]
                data_sets[d0][d1] = {}
                for ff in filter_function_names.keys():
                    if os.path.exists(ff_dir + "/" + ff + ".json"):
                        data_sets[d0][d1][ff] = filter_function_names[ff]
