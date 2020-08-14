
import networkx as nx
import os

import glob
import numpy as np
import time

def load_weighted_graph_from_hd(path):
    
    
    if not os.path.exists(path):
        print('the graph file does not exist')
        return
    print('loading the file : ' +path )     
    G=nx.Graph() 
    edges=[]
    nodes=[]
    
    with open(path) as f:
        for line in f:
            numbers_str = line.split()

            if len(numbers_str)==0:
                continue
            if numbers_str[0]=='n' or numbers_str[0]=='e' or numbers_str[0]=='v':
                numbers_str1=numbers_str[1:]
  
            numbers_float = [float(x) for x in numbers_str1]  #map(float,numbers_str) works too

            if numbers_str[0]=='n' or numbers_str[0]=='v':
                nodes.append(numbers_float)

            elif numbers_str[0]=='e':

                edges.append(numbers_float)
            else:
                continue
            
    for node in nodes:
        G.add_node( int(node[0]) )
    if len(edges)==0:
        return G
    
    if len(edges[0])==2:
        for row in edges:
            G.add_edge(int(row[0]),int(row[1]))
    else:
        
        for row in edges:
            
            G.add_edge(int(row[0]),int(row[1]),color='k', weight=row[2] )


    return G        


folder=os.getcwd()

print(folder)

number_of_tests=5

graphs_files =glob.glob(folder+"/*.graph")


print("the total # of graphs found = "+str(len(graphs_files)) )



for file in graphs_files:
    print("calculating graph "+str(file))    
	
    G=load_weighted_graph_from_hd(file)
    
    runningtimes=[]
    
    for i in range(0,number_of_tests):
            
        
        starttime=time.time()
        
        f=nx.pagerank(G)
        
        endtime=time.time()-starttime
        
        runningtimes.append(endtime)
        
    
    print("the Avg Runtime for the graph " + file + " is : ")
    print(np.mean(np.array(runningtimes)))

    print("the Stdev of the Runtime for the graph " + file + " is : ")
    print(np.std(np.array(runningtimes)))
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++++")
