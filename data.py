import fnmatch
import json
import multiprocessing
import ntpath
import os
import sys
import time


import networkx as nx

import mog.filter_functions as ff

data_sets = {}

filter_function_names = {'agd': 'Average Geodesic Distance',
                         'ecc': 'Eccentricity',
                         'pr_0_85': 'PageRank (alpha=0.85)',
                         'fv': 'Fiedler Vector',
                         'fv_norm': 'Fiedler Vector Normalized',
                         'den_0_5': 'Density 0.5',
                         'ev_1': 'Eigen Function (2nd)',
                         'ev_2': 'Eigen Function (3rd)',
                         'ev_3': 'Eigen Function (4th)',
                         'ev_4': 'Eigen Function (5th)',
                         'ev_5': 'Eigen Function (6th)',
                         'ev_norm_1': 'Eigen Function Normalized (2nd)',
                         'ev_norm_2': 'Eigen Function Normalized (3rd)',
                         'ev_norm_3': 'Eigen Function Normalized (4th)',
                         'ev_norm_4': 'Eigen Function Normalized (5th)',
                         'ev_norm_5': 'Eigen Function Normalized (6th)'}


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


def read_tsv_file(filename):
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


def write_json_data(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# Generate AGD
def generate_agd(out_path, graph, weight):
    if not os.path.exists(out_path):
        write_json_data(out_path, ff.average_geodesic_distance(graph, _weight=weight))


# Generate eccentricity
def generate_ecc(out_path, graph):
    if not os.path.exists(out_path):
        write_json_data(out_path, ff.eccentricity(graph))


# Generate pagerank
def generate_pr(out_path, graph, weight, alpha):
    if not os.path.exists(out_path):
        write_json_data(out_path, ff.pagerank(graph, weight, alpha))


# Generate fiedler vector
def generate_fv(out_path, graph, weight, normalized):
    try:
        if not os.path.exists(out_path):
            write_json_data(out_path, ff.fiedler_vector(graph, _weight=weight, _normalized=normalized))
    except nx.exception.NetworkXError:
        print(">>> FAILED (fiedler vector): graph not connected error")


# Generate density
def generate_den(out_path, graph, weight, eps):
    if not os.path.exists(out_path):
        write_json_data(out_path, ff.density(graph, weight, eps))


# Generate eigen functions
def generate_eig(out_path, graph, weight, which_eig, normalized):
    try:
        compute = False
        for ev in which_eig:
            ev_path = out_path.format(str(ev))
            if graph.number_of_nodes() > ev and not os.path.exists(ev_path): compute = True

        if compute:
            eig = ff.eigen_function(graph, _weight=weight, _normalized=normalized)
            for ev in which_eig:
                if graph.number_of_nodes() > ev:
                    ev_path = out_path.format(str(ev))
                    write_json_data(ev_path, eig[ev][1])
    except TypeError:
        print(">>> FAILED (eigen): type error")


def process_datafile(in_filename, max_time_per_file=1):
    print("Processing: " + in_filename)

    if fnmatch.fnmatch(in_filename.lower(), "*.json"):
        data, graph = read_json_graph(in_filename)
    elif fnmatch.fnmatch(in_filename.lower(), "*.graph"):
        data, graph = read_graph_file(in_filename)
    elif fnmatch.fnmatch(in_filename.lower(), "*.tsv"):
        data, graph = read_tsv_file(in_filename)
    else:
        return

    gcc = max(nx.connected_components(graph), key=len)
    graph = graph.subgraph(gcc)

    out_filename = "data/"
    if graph.number_of_nodes() < 100:
        out_filename += "small/"
    elif graph.number_of_nodes() < 1000:
        out_filename += "medium/"
    elif graph.number_of_nodes() < 5000:
        out_filename += "large/"
    else:
        out_filename += "very_large/"

    out_filename += os.path.splitext(ntpath.basename(in_filename).lower())[0] + ".json"

    print("                     => " + out_filename)

    out_dir = os.path.splitext(out_filename)[0]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    procs = [multiprocessing.Process(target=generate_agd, args=(out_dir + "/agd.json", graph, 'value')),
             multiprocessing.Process(target=generate_ecc, args=(out_dir + "/ecc.json", graph)),
             multiprocessing.Process(target=generate_pr, args=(out_dir + "/pr_0_85.json", graph, 'value', 0.85)),
             multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv.json", graph, 'value', False)),
             multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv_norm.json", graph, 'value', True)),
             multiprocessing.Process(target=generate_den, args=(out_dir + "/den_0_5.json", graph, 'value', 0.5)),
             multiprocessing.Process(target=generate_eig, args=(out_dir + "/ev_{}.json", graph, 'value', range(1, 6), False)),
             multiprocessing.Process(target=generate_eig, args=(out_dir + "/ev_norm_{}.json", graph, 'value', range(1, 6), True))]

    # process the functions in parallel for max_time_per_file
    end_time = time.time() + max_time_per_file
    for p in procs: p.start()
    for p in procs:
        p.join(max(1, int(end_time - time.time())))
        if p.is_alive():
            p.terminate()
            p.join()

    write_json_data(out_filename, nx.node_link_data(graph))

    return data


if not os.path.exists("data/small"): os.mkdir("data/small")
if not os.path.exists("data/medium"): os.mkdir("data/medium")
if not os.path.exists("data/large"): os.mkdir("data/large")
if not os.path.exists("data/very_large"): os.mkdir("data/very_large")


def generate_data(max_time_per_file=1):
    data_gen = []
    for d0 in os.listdir("data/source"):
        if os.path.isdir("data/source/" + d0):
            for d1 in os.listdir("data/source/" + d0):
                if fnmatch.fnmatch(d1.lower(), "*.json"):
                    data_gen.append("data/source/" + d0 + "/" + d1)
                if fnmatch.fnmatch(d1.lower(), "*.graph"):
                    data_gen.append("data/source/" + d0 + "/" + d1)
                if fnmatch.fnmatch(d1.lower(), "*.tsv"):
                    data_gen.append("data/source/" + d0 + "/" + d1)

    for file in data_gen:
        try:
            process_datafile(file, max_time_per_file)
        except json.decoder.JSONDecodeError:
            print(">>> FAILED: json parse " + file)
        except TypeError:
            print(">>> FAILED: type error " + file)
        except nx.exception.NetworkXError:
            print(">>> FAILED: graph not connected error " + file)
        except:
            print(file + " failed with " + str(sys.exc_info()[0]))


def scan_datasets():
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


if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_data(int(sys.argv[1]))
    else:
        generate_data(1)
