
import data
import os
import json
import mog.graph_io as GraphIO
import cache


def csv_header( modal ):
    ret = ''
    for m in modal:
        ret += str(m) + ','
    return ret[:-1]


def csv_add_row( modal, data ):
    ret = '\n'
    for m in modal:
        if m in data:
            s = str(data[m])
            if s.find(",") >= 0: s = '"' + s + '"'
            ret += s
        ret += ','
    return ret[:-1]


def generate_filter_summary(force_overwrite=False):
    if not force_overwrite and os.path.exists("analysis/filter_summary.csv") : return

    ffs = list(data.filter_function_names.keys())
    ffs.sort()

    modal = ['dataset','datafile','nodes','edges'] + ffs

    ret = csv_header(modal)

    record = {}
    for ds0 in data.data_sets:
        record['dataset'] = ds0
        for ds1 in data.data_sets[ds0]:
            record['datafile'] = ds1
            record['nodes'] = 0
            record['edges'] = 0

            for ff in ffs:
                record[ff] = ''
                if ff in data.data_sets[ds0][ds1]:
                    with open('docs/data/' + ds0 + "/" + os.path.splitext(ds1)[0] + "/" + ff + ".json") as json_file:
                        ff_data = json.load(json_file)
                        if 'num_of_nodes' in ff_data: record['nodes'] = ff_data['num_of_nodes']
                        if 'num_of_edges' in ff_data : record['edges'] = ff_data['num_of_edges']
                        record[ff] = ff_data['process_time']

            ret += csv_add_row(modal, record)

    with open("analysis/filter_summary.csv", 'w') as outfile:
        outfile.write(ret)


def generate_graph_summary(force_overwrite=False):
    if not force_overwrite and os.path.exists("analysis/graph_summary.csv") : return
    ret = 'dataset,datafile,node_count,edge_count\n'
    for ds0 in data.data_sets:
        for ds1 in data.data_sets[ds0]:
            graph_data, graph = GraphIO.read_json_graph('docs/data/' + ds0 + "/" + ds1)
            ret += ds0 + ',"' + ds1 + '",' + str(graph.number_of_nodes()) + ',' + str(graph.number_of_edges()) + '\n'
    with open("analysis/graph_summary.csv", 'w') as outfile:
        outfile.write(ret)


def generate_mog_profile(dataset,datafile):
    ret = 'filter_func,cover_elem_count,component_method,connectivity_method,ranked,nodes,edges,compute_time\n'
    graph_data, graph = GraphIO.read_json_graph('docs/data/' + dataset + "/" + datafile)
    for ff in data.data_sets[dataset][datafile]:
        levels = [2,3,4,6,8,10,20]
        #for coverN in range(2,20):
        for coverN in levels:
            mog, mog_cf = cache.generate_mog( dataset, datafile, ff, coverN, 0, 'connected_components', 'connectivity', 'false' )
            ret += ff + ',' + str(coverN) + ',' + 'connected_components,connectivity,false' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
            mog, mog_cf = cache.generate_mog(dataset, datafile, ff, coverN, 0, 'connected_components', 'connectivity', 'true')
            ret += ff + ',' + str(coverN) + ',' + 'connected_components,connectivity,true' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
            if graph.number_of_nodes() < 100000:
                mog, mog_cf = cache.generate_mog( dataset, datafile, ff, coverN, 0, 'modularity', 'connectivity', 'false' )
                ret += ff + ',' + str(coverN) + ',' + 'modularity,connectivity,false' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
                mog, mog_cf = cache.generate_mog(dataset, datafile, ff, coverN, 0, 'modularity', 'connectivity', 'true')
                ret += ff + ',' + str(coverN) + ',' + 'modularity,connectivity,true' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
                mog, mog_cf = cache.generate_mog( dataset, datafile, ff, coverN, 0, 'async_label_prop', 'connectivity', 'false' )
                ret += ff + ',' + str(coverN) + ',' + 'async_label_prop,connectivity,false' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
                mog, mog_cf = cache.generate_mog(dataset, datafile, ff, coverN, 0, 'async_label_prop', 'connectivity', 'true')
                ret += ff + ',' + str(coverN) + ',' + 'async_label_prop,connectivity,true' + ',' + str(mog.number_of_nodes()) + ',' + str(mog.number_of_edges()) + ',' + str(mog.info['compute_time']) + '\n'
    with open("analysis/mog/"+datafile[:-5]+".csv",'w') as outfile:
        outfile.write(ret)


if __name__ == '__main__':
    if not os.path.exists("analysis"): os.mkdir("analysis")
    if not os.path.exists("analysis/mog"): os.mkdir("analysis/mog")
    data.scan_datasets()
    generate_filter_summary(False)
    generate_graph_summary(False)
    for ds in ['small','medium','large']:
        for df in data.data_sets[ds]:
            generate_mog_profile(ds,df)
