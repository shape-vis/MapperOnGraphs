
import data
import os
import json
import mog.graph_io as GraphIO
import cache


def generate_filter_summary(force_overwrite=False):
    if not force_overwrite and os.path.exists("analysis/filter_summary.csv") : return
    ret = 'dataset,datafile,filter_function,nodes,processing time\n'
    for ds0 in data.data_sets:
        for ds1 in data.data_sets[ds0]:
            for ff in data.data_sets[ds0][ds1]:
                with open('data/' + ds0 + "/" + os.path.splitext(ds1)[0] + "/" + ff + ".json") as json_file:
                    ff_data = json.load(json_file)
                    ret += ds0 + ',"' + ds1 + '",' + ff + ',' + str(len(ff_data['data'])) + ',' + str(ff_data['process_time']) + '\n'
    with open("analysis/filter_summary.csv", 'w') as outfile:
        outfile.write(ret)


def generate_graph_summary(force_overwrite=False):
    if not force_overwrite and os.path.exists("analysis/graph_summary.csv") : return
    ret = 'dataset,datafile,node_count,edge_count\n'
    for ds0 in data.data_sets:
        for ds1 in data.data_sets[ds0]:
            graph_data, graph = GraphIO.read_json_graph('data/' + ds0 + "/" + ds1)
            ret += ds0 + ',"' + ds1 + '",' + str(graph.number_of_nodes()) + ',' + str(graph.number_of_edges()) + '\n'
    with open("analysis/graph_summary.csv", 'w') as outfile:
        outfile.write(ret)


def generate_mog_profile(dataset,datafile):
    ret = 'filter_func,cover_elem_count,component_method,connectivity_method,ranked,nodes,edges,compute_time\n'
    for ff in data.data_sets[dataset][datafile]:
        for coverN in range(2,20):
            mog, mog_cf = cache.generate_mog( dataset, datafile, ff, coverN, 0, 'connected_components', 'connectivity', 'false' )
            ret += ff + ',' + str(coverN) + ',' + 'connected_components,connectivity,false' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
            mog, mog_cf = cache.generate_mog( dataset, datafile, ff, coverN, 0, 'modularity', 'connectivity', 'false' )
            ret += ff + ',' + str(coverN) + ',' + 'modularity,connectivity,false' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
            mog, mog_cf = cache.generate_mog(dataset, datafile, ff, coverN, 0, 'connected_components', 'connectivity', 'true')
            ret += ff + ',' + str(coverN) + ',' + 'connected_components,connectivity,true' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
            mog, mog_cf = cache.generate_mog(dataset, datafile, ff, coverN, 0, 'modularity', 'connectivity', 'true')
            ret += ff + ',' + str(coverN) + ',' + 'modularity,connectivity,true' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
    with open("analysis/"+datafile[:-5]+".csv",'w') as outfile:
        outfile.write(ret)


if __name__ == '__main__':
    data.scan_datasets()
    generate_filter_summary()
    generate_graph_summary()
    for ds in ['small','medium']:
        for df in data.data_sets[ds]:
            generate_mog_profile(ds,df)
            