# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:18:25 2021

@author: Michael
"""
import time
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import random
import operator
import json
from solver import solvermethod

def sorting_allpath_bylatency(allpath_list, g):
    allpath_dict = {}
    output = []
    for path in allpath_list:
        total_length = 0
        total_latency = 0
        for i in range(len(path)-1):
            source, target = path[i], path[i+1]
            edge = g[source][target]
            length = edge['weight']
            lat = edge['latency']
            total_length += length
            total_latency += lat
        allpath_dict[(total_latency,total_length)] = path
        
    items = allpath_dict.items()
    output = sorted(items)
    return output

def sorting_allpath_byweight(allpath_list, g):
    allpath_dict = {}
    output = []
    for path in allpath_list:
        total_length = 0
        total_latency = 0
        for i in range(len(path)-1):
            source, target = path[i], path[i+1]
            edge = g[source][target]
            length = edge['weight']
            lat = edge['latency']
            total_length += length
            total_latency += lat
        allpath_dict[(total_length,total_latency)] = path

    items = allpath_dict.items()
    output = sorted(items)

    return output

def heur_bylatency(g, nodes, max_latency):
    global solution
        #### creating the heuristic model
    time_start=time.time()
    allpath_list=[]

    for path in nx.all_simple_paths(g, source=0, target=nodes-1):
        allpath_list.append(path)

    sortedlist = sorting_allpath_bylatency(allpath_list, g)
    solution = "Null"
    for pair in sortedlist:
        if pair[0][0] <= max_latency:
            solution = pair
            break
            
    time_end = time.time()
    time_used = (time_end-time_start)*1000
    # print("sortedlist"+str(sortedlist))
    
    return [solution,time_used]


def heur_byweight(g, nodes, max_latency):
    global solution
    #### creating the heuristic model
    time_start = time.time()
    allpath_list = []

    for path in nx.all_simple_paths(g, source=0, target=nodes - 1):
        allpath_list.append(path)

    sortedlist = sorting_allpath_byweight(allpath_list, g)
    solution = "Null"
    for pair in sortedlist:
        if pair[0][1] <= max_latency:
            solution = pair
            break

    time_end = time.time()
    time_used = (time_end - time_start) * 1000

    return [solution, time_used]
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def bwassign(g): ## pass in the bw name
    for (u,v,w) in g.edges(data=True):
        w['bandwidth'] = random.randint(1,150)


 ## also for latency filter
def bwfilter(g,bwlimit): ## remove paths that does not satisfy the bw requirement and display paths that has been removed
    path_remove = []
    path_remove_withbw = []
    for (u,v,w) in g.edges(data=True):
        if w['bandwidth'] < bwlimit:
            path_remove.append((u,v))
            path_remove_withbw.append((u,v,w))
    g.remove_edges_from(path_remove)
    print("remove path:" + str(path_remove_withbw))
    return g
    
        
def weightassign(g):
    distance_list = []
    latency_list = []
    for (u,v,w) in g.edges(data=True):
        w['weight'] = random.randint(1,2**24) #10-10^9
        
        latency = random.randint(10,100) #10,100 1/100 msec
        w['latency'] =latency
        distance_list.append(w['weight']) 
        latency_list.append(latency) 
    return[distance_list,latency_list]

def nodes_connected(g, u, v):
    return u in g.neighbors(v)

def jsonfilemaker(nodes, inputmatrix, inputdistance, link_list, max_latency, sortedanswer):
    rhs = zerolistmaker(nodes)
    rhs[0] = -1
    rhs[-1] = 1    
    jsonoutput = {}
    jsonoutput['constraint_coeffs'] = inputmatrix
    jsonoutput['bounds'] = rhs
    jsonoutput['obj_coeffs'] = inputdistance
    jsonoutput['num_vars'] = len(link_list)
    jsonoutput['num_constraints'] = len(inputmatrix)
    jsonoutput['max_latency'] = max_latency
    with open('data.json', 'w') as json_file:
        json.dump(jsonoutput, json_file,indent=4)
  
    try:
        output = sortedanswer[0][1]
    except IndexError:
        output = "Null"
    return [output,time]

def bwlinklist(g,link_list):
    bwlinklist = {}
    for u,v,w in g.edges(data=True):
        bwlinklist[u,v] = w["bandwidth"]

    print(bwlinklist)

    bwlinkdict = []
    for pair in link_list:
        if (pair[0], pair[1]) in bwlinklist:
            # print("pair"+str((pair[0], pair[1])))
            bw = bwlinklist[(pair[0], pair[1])]
            bwlinkdict.append(bw)
        else:
            bw = bwlinklist[(pair[1], pair[0])]
            bwlinkdict.append(bw)
    #
    with open('bwlinklist.json', 'w') as json_file:
        data = bwlinkdict
        json.dump(data, json_file, indent=4)
    print(bwlinkdict)



def nxgraphgenerator(nodes,p,max_latency,bwlimit):
    # random.seed(1)
    g = erdos_renyi_graph(nodes,p)
    
    while True:
        if nx.is_connected(g):
            break
        else:
            g = erdos_renyi_graph(nodes,p)
    bwassign(g)
    bwfilter(g, bwlimit)



        
    link_dict = {}
    weightassignment = weightassign(g)
    edgelist = list(g.edges)
    
    ## generate each node's parent node
    for pair in g.edges:
        if pair[0] in link_dict:
            link_dict[pair[0]].append(pair[1])
        else:
            link_dict[pair[0]]=[pair[1]]
        
        if pair[1] in link_dict:
            link_dict[pair[1]].append(pair[0])
        else:
            link_dict[pair[1]]=[pair[0]]
    linknum = 2*len(g.edges)
         
    sorted_dict = dict(sorted(link_dict.items(), key=operator.itemgetter(0)))  

    
    
    ## show every link (bidirectional link means 2 different link)
    link_list = []
    for startnode in sorted_dict:
        for endnode in sorted_dict[startnode]:
            link_list.append([startnode, endnode])
            
    
    ## generte a link name list for future look up and reference
    linktitle_dict={}
    for n in range(len(link_list)):
        linktitle_dict[n] = link_list[n]

    
    ## create the  contraint matrix of 0s
    nodenum = len(g.nodes)    
    inputmatrix = []
    for n in range(nodenum):
        inputmatrix.append(zerolistmaker(linknum))

    
    ## input values based on the linklist into the matrix, 1 means flow into the nodes, -1 meanse flow out of the node
    c = 0
    for line in inputmatrix:
        n = 0
        for link in link_list:
            if link[0] == c:
                inputmatrix[c][n] = -1
                n= n+1
            elif link[1] == c:
                inputmatrix[c][n] = 1
                n=n+1
            else:
                n=n+1
        c = c+1
    
    
    inputdistance = zerolistmaker(len(link_list))
    inputlatency = zerolistmaker(len(link_list))
    distance_list = weightassignment[0]
    latency_list = weightassignment[1]

    
    ## look up and form the distance and latency array for each link
    count = 0
    for link in link_list:
        try:
            inputdistance[count] = distance_list[edgelist.index((link[0],link[1]))]
            count = count+1
        except ValueError:
            inputdistance[count] = distance_list[edgelist.index((link[1],link[0]))]
            count = count+1
            
    count = 0        
    for link in link_list:
        try:
            inputlatency[count] = latency_list[edgelist.index((link[0],link[1]))]
            count = count+1
        except ValueError:
            inputlatency[count] = latency_list[edgelist.index((link[1],link[0]))]

    pos = nx.spring_layout(g)
    
    print()
    

    # Draw the graph according to node positions
    labels = nx.get_edge_attributes(g,'bandwidth')
    # print("labels" + str(labels))

    latencyheurresult = heur_bylatency(g,nodes,max_latency)
    # print("latencyheurresult: "+str(latencyheurresult))
    latencysortedanswer = latencyheurresult[0]
    latencytime = latencyheurresult[1]
    
    weightheurresult = heur_byweight(g, nodes, max_latency)
    # print()
    # print("weight: "+str(weightheurresult))
    # print()
    weightsortedanswer = weightheurresult[0]
    weighttime = weightheurresult[1]
    
    # print("sorted answer: "+str(latencysortedanswer))
    
 
    
    rhs = zerolistmaker(nodes)
    rhs[0] = -1
    rhs[-1] = 1    
    jsonoutput = {}
    jsonoutput['constraint_coeffs'] = inputmatrix
    jsonoutput['bounds'] = rhs
    jsonoutput['obj_coeffs'] = inputdistance
    jsonoutput['num_vars'] = len(link_list)
    jsonoutput['num_constraints'] = len(inputmatrix)
    jsonoutput['max_latency'] = max_latency
    with open('data.json', 'w') as json_file:
        json.dump(jsonoutput, json_file,indent=4)
  
    try:
        latencyoutput = latencysortedanswer[0][1]
        weightoutput = weightsortedanswer[0][0]
    except IndexError:
        latencyoutput = "Null"
        weightoutput = "Null"


    with open('linklist.json', 'w') as json_file:
        data = link_list
        json.dump(data, json_file,indent=4)
    
    
    result = [latencyoutput,latencytime,weightoutput,weighttime]


    bwlinklist(g,link_list)
    return result
    # return [latencyoutput,latencytime,weightoutput,weighttime]







# try:
#     heur = nxgraphgenerator(8,0.6,1000,20)
#     print(heur)
# except UnboundLocalError:
#     print("The source and destination nodes are no longer connected. ")
    


