import fnmatch
import json
import multiprocessing
import ntpath
import os
import sys
import time
import networkx as nx

import mog.graph_io as GraphIO
import mog.filter_functions as ff
import layout.initial_layout as layout

import cache

data_sets = {}

filter_function_names = {'agd': 'Average Geodesic Distance',
                         'ecc': 'Eccentricity',
                         'pr_0_85': 'PageRank (alpha=0.85)',
                         'fv': 'Fiedler Vector',
                         'fv_norm': 'Fiedler Vector Normalized',
                         'den_0_5': 'Density 0.5'}


def process_graph(in_filename):
    print("Found: " + in_filename)
    basename, ext = os.path.splitext(ntpath.basename(in_filename).lower())

    # Check if the graph already exists
    # if os.path.exists('docs/data/very_small/' + basename + '.json'): return 'docs/data/very_small/' + basename + '.json'
    if os.path.exists('docs/data/small/' + basename + '.json'): return 'docs/data/small/' + basename + '.json'
    if os.path.exists('docs/data/medium/' + basename + '.json'): return 'docs/data/medium/' + basename + '.json'
    if os.path.exists('docs/data/large/' + basename + '.json'): return 'docs/data/large/' + basename + '.json'

    # Load the graph, if possible
    if ext == ".json": data, graph = GraphIO.read_json_graph(in_filename)
    elif ext == ".graph": data, graph = GraphIO.read_graph_file(in_filename)
    elif ext == ".tsv": data, graph = GraphIO.read_tsv_graph_file(in_filename)
    else: return None

    # set outfile name
    # if graph.number_of_nodes() < 100: out_filename = 'docs/data/very_small/' + basename + '.json'
    if graph.number_of_nodes() < 100: return None
    elif graph.number_of_nodes() < 1000: out_filename = 'docs/data/small/' + basename + '.json'
    elif graph.number_of_nodes() < 5000: out_filename = 'docs/data/medium/' + basename + '.json'
    else: out_filename = 'docs/data/large/' + basename + '.json'

    print("   >> Converting " + in_filename + " to " + out_filename)

    # Extract the largest connected component
    gcc = max(nx.connected_components(graph), key=len)
    graph = graph.subgraph(gcc)

    # Provide a good quality initial layout for small and medium sized graphs
    if graph.number_of_nodes() < 5000:
        layout.initialize_radial_layout(graph)

    # Write the graph to file
    GraphIO.write_json_graph(out_filename, graph)

    return out_filename


# Generate AGD
def generate_agd(out_path, graph, weight):
    if not os.path.exists(out_path):
        print("   >> Generating AGD")
        data = ff.average_geodesic_distance(graph, _weight=weight, _out_path=out_path)


# Generate eccentricity
def generate_ecc(out_path, graph):
    if not os.path.exists(out_path):
        print("   >> Generating Eccentricity")
        data = ff.eccentricity(graph, _out_path=out_path)


# Generate pagerank
def generate_pr(out_path, graph, weight, alpha):
    if not os.path.exists(out_path):
        print("   >> Generating Pagerank")
        data = ff.pagerank(graph, weight, alpha, _out_path=out_path)


# Generate fiedler vector
def generate_fv(out_path, graph, weight, normalized):
    if not os.path.exists(out_path):
        print("   >> Generating Fiedler Vector")
        data = ff.fiedler_vector(graph, _weight=weight, _normalized=normalized, _out_path=out_path)


# Generate density
def generate_den(out_path, graph, weight, eps):
    if not os.path.exists(out_path):
        print("   >> Generating Density")
        data = ff.density(graph, weight, eps, _out_path=out_path)


# Function that controls the creating of filter functions
def process_filter_functions(in_filename, max_time_per_file=1, scalableOnly=False):
    print("Processing Graph: " + in_filename)

    ff_file_list = ["/agd.json", "/ecc.json", "/pr_0_85.json", "/fv.json", "/fv_norm.json", "/den_0_5.json"]

    need_processing = False
    for f in ff_file_list:
        need_processing = need_processing or not os.path.exists(f)

    if not need_processing: return

    data, graph = GraphIO.read_json_graph(in_filename)

    out_dir = os.path.splitext(in_filename)[0]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    if scalableOnly:
        mprocs = [multiprocessing.Process(target=generate_pr, args=(out_dir + "/pr_0_85.json", graph, 'value', 0.85)),
                 multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv.json", graph, 'value', False)),
                 multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv_norm.json", graph, 'value', True))]
    else:
        mprocs = [multiprocessing.Process(target=generate_agd, args=(out_dir + "/agd.json", graph, 'value')),
                 multiprocessing.Process(target=generate_ecc, args=(out_dir + "/ecc.json", graph)),
                 multiprocessing.Process(target=generate_pr, args=(out_dir + "/pr_0_85.json", graph, 'value', 0.85)),
                 multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv.json", graph, 'value', False)),
                 multiprocessing.Process(target=generate_fv, args=(out_dir + "/fv_norm.json", graph, 'value', True)),
                 multiprocessing.Process(target=generate_den, args=(out_dir + "/den_0_5.json", graph, 'value', 0.5))]

    # process the functions in parallel for max_time_per_file
    end_time = time.time() + max_time_per_file
    for p in mprocs: p.start()
    for p in mprocs:
        p.join(max(1, int(end_time - time.time())))
        if p.is_alive():
            p.terminate()
            p.join()


def generate_data(max_time_per_file=1):

    # Find graphs and convert them into usable json format
    data_gen = []
    for d0 in os.listdir("data"):
        if os.path.isdir("data/" + d0):
            for d1 in os.listdir("data/" + d0):
                try:
                    if fnmatch.fnmatch(d1.lower(), "*.json") \
                            or fnmatch.fnmatch(d1.lower(), "*.graph") \
                            or fnmatch.fnmatch(d1.lower(), "*.tsv"):
                        data_gen.append(process_graph("data/" + d0 + "/" + d1))
                except:
                    print("data/" + d0 + "/" + d1 + " failed with " + str(sys.exc_info()[0]))

    for file in data_gen:
        if file is None: continue
        try:
            process_filter_functions(file, max_time_per_file)
        except json.decoder.JSONDecodeError:
            print(">>> FAILED: json parse " + file)
        except TypeError:
            print(">>> FAILED: type error " + file)
        except nx.exception.NetworkXError:
            print(">>> FAILED: graph not connected error " + file)
        except:
            print(file + " failed with " + str(sys.exc_info()[0]))


def scan_datasets():
    # for d0 in ['very_small', 'small', 'medium', 'large']:
    for d0 in ['small', 'medium', 'large']:
        if os.path.isdir("docs/data/" + d0):
            data_sets[d0] = {}
            for d1 in os.listdir("docs/data/" + d0):
                if fnmatch.fnmatch(d1.lower(), "*.json"):
                    ff_dir = os.path.splitext("docs/data/" + d0 + '/' + d1)[0]
                    data_sets[d0][d1] = {}
                    for ff in filter_function_names.keys():
                        if os.path.exists(ff_dir + "/" + ff + ".json"):
                            data_sets[d0][d1][ff] = filter_function_names[ff]
                    if len(data_sets[d0][d1]) == 0:
                        del data_sets[d0][d1]
    GraphIO.write_json_data('docs/data/datasets.json',data_sets)


def __pre_generate_mog( params, opts, opts_keys ):
    if len(opts_keys) == 0:
        cache.generate_mog(params['dataset'], params['datafile'],
                           params['filter_func'],
                           params['coverN'], params['coverOverlap'],
                           params['component_method'],
                           params['link_method'], params['rank_filter'])
    else:
        key = opts_keys[0]
        for o in opts[key]:
            params[key] = o
            __pre_generate_mog(params, opts, opts_keys[1:])


def pre_generate_mog(dataset,datafile,ff):
    opts = {
        'dataset': [dataset],
        'datafile': [datafile],
        'filter_func': ff,
        'coverN': [2,3,4,6,8,10,20],
        'coverOverlap': [0],
        'component_method': ['connected_components','modularity','async_label_prop'],
        'link_method': ['connectivity'],
        'mapper_node_size_filter': [0],
        'rank_filter': ['true','false'],
        'gcc_only': ['false']
    }
    __pre_generate_mog( {}, opts, list(opts.keys()) )


# if not os.path.exists("docs/data/very_small"): os.mkdir("docs/data/very_small")
if not os.path.exists("docs/data/small"): os.mkdir("docs/data/small")
if not os.path.exists("docs/data/medium"): os.mkdir("docs/data/medium")
if not os.path.exists("docs/data/large"): os.mkdir("docs/data/large")


if __name__ == '__main__':

    timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if timeout > 0:
        generate_data(timeout)

    # process_graph('data/snap/com-youtube.ungraph.graph')
    # process_filter_functions('docs/data/large/amazon0302.json', 18000, True)
    # process_filter_functions('docs/data/large/com-amazon.ungraph.json', 18000, True)
    # process_filter_functions('docs/data/large/com-youtube.ungraph.json', 18000, True)
    #
    scan_datasets()

    # with multiprocessing.Pool(processes=6) as pool:
    #     procs = []
    #     for d0 in data_sets:
    #         for d1 in data_sets[d0]:
    #             procs.append( pool.apply_async(pre_generate_mog, (d0,d1,data_sets[d0][d1]) ) )
    #     print([res.get(timeout=900) for res in procs])
