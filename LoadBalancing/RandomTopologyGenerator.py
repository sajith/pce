#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:34:06 2022

@author: yifeiwang
"""
import time
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import random
import operator
import json

import copy

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def bwassign(g): ## pass in the bw name
    for (u,v,w) in g.edges(data=True):
        w['bandwidth'] = random.randint(2000,3000)


 ## also for latency filter
# def bwfilter(g,bwlimit): ## remove paths that does not satisfy the bw requirement and display paths that has been removed
#     path_remove = []
#     path_remove_withbw = []
#     for (u,v,w) in g.edges(data=True):
#         if w['bandwidth'] < bwlimit:
#             path_remove.append((u,v))
#             path_remove_withbw.append((u,v,w))
#     g.remove_edges_from(path_remove)
#     print("remove path:" + str(path_remove_withbw))
#     return g
    
        
def weightassign(g):
    distance_list = []
    latency_list = []
    for (u,v,w) in g.edges(data=True):
        w['weight'] = random.randint(1,2**24) #10-10^9
        
        latency = random.randint(1,10) #10,100 1/100 msec
        w['latency'] =latency
        distance_list.append(w['weight']) 
        latency_list.append(latency)


    return[distance_list,latency_list]

def nodes_connected(g, u, v):
    return u in g.neighbors(v)

def bwlinklist(g,link_list):
    bwlinklist = {}
    for u,v,w in g.edges(data=True):
        bwlinklist[u,v] = w["bandwidth"]



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
    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/bwlinklist.json', 'w') as json_file:
        data = bwlinkdict
        json.dump(data, json_file, indent=4)

    
    return bwlinkdict
    

def duplicatematrixmaker(request_list,inputmatrix):
    print(len(inputmatrix))
    zeros = zerolistmaker(len(inputmatrix[0]))
    outputmatrix = []
    for i in range(len(request_list)):
        for line in inputmatrix:
            outputmatrix.append(zeros * i + line + zeros * (len(request_list)-i-1) )
    return outputmatrix

def lhsbw(request_list, inputmatrix):
    bwconstraints = []
    zeros = zerolistmaker(len(inputmatrix[0])*len(request_list))                
    for i in range(len(inputmatrix[0])):
        addzeros = copy.deepcopy(zeros)
        bwconstraints.append(addzeros)
        count = 0
        for request in request_list:
            bwconstraints[i][i+count * len(inputmatrix[0])] = request[2]
            count += 1
    return bwconstraints


def jsonfilemaker(nodes, inputmatrix, inputdistance,request_list,rhsbw, linknum):
    bounds = []
    for request in request_list:
        rhs = zerolistmaker(nodes)
        rhs[request[0]] = -1
        rhs[request[1]] = 1   
        bounds += rhs

    ## add the bwconstraint rhs
    bounds+=rhsbw

    jsonoutput = {}
    flowconstraints = duplicatematrixmaker(request_list,inputmatrix)
    bwconstraints = lhsbw(request_list, inputmatrix)
    # print()
    # print("bwcon"+str(bwconstraints))
    # print()
    lhs = flowconstraints + bwconstraints
    cost_list = copy.deepcopy(inputdistance)
    cost = []
    for i in range(len(request_list)):
        cost += cost_list

    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/latconstraint.json') as f:
        latconstraint = json.load(f)
    lhs+=latconstraint['lhs']
    bounds+=latconstraint['rhs']

    jsonoutput['constraint_coeffs'] = lhs
    jsonoutput['bounds'] = bounds
    jsonoutput['obj_coeffs'] = cost
    jsonoutput['num_vars'] = len(cost)
    jsonoutput['num_constraints'] = len(bounds)
    jsonoutput['num_inequality'] = linknum + int(len(request_list))

    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/LB_data.json', 'w') as json_file:
        json.dump(jsonoutput, json_file,indent=4)


def latconstraintmaker(request_list, latency_list):
    lhs = []
    rhs = []
    zerolist = zerolistmaker(len(latency_list))
    print(zerolist)
    requestnum = len(request_list)
    for i in range(requestnum):
        print(i)
        constraint = []
        constraint = i * zerolist + latency_list + (requestnum - 1 - i) * zerolist
        lhs.append(constraint)

        print()

    for request in request_list:
        rhs.append(request[3])

    latdata = {}
    latdata["lhs"] = lhs
    latdata["rhs"] = rhs

    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/latconstraint.json', 'w') as json_file:
        data = latdata
        json.dump(data, json_file, indent=4)
    
def lbnxgraphgenerator(nodes,p):
    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/connection.json') as f:
        source_destination_list = json.load(f)
    print("source_destination_list:"+str(source_destination_list))
    # random.seed(1)
    g = erdos_renyi_graph(nodes,p)
    
    while True:
        if nx.is_connected(g):
            break
        else:
            g = erdos_renyi_graph(nodes,p)
    bwassign(g)
    # bwfilter(g, bwlimit)



        
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
            count+=1

    pos = nx.spring_layout(g)
    
    print()
    print(inputdistance)
    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/latency_list.json', 'w') as json_file:
        data = inputlatency
        json.dump(data, json_file, indent=4)
    

    # Draw the graph according to node positions
    labels = nx.get_edge_attributes(g,'bandwidth')
    with open('/Users/yifeiwang/Desktop/5.3code/pce/test/data/LB_linklist.json', 'w') as json_file:
        data = link_list
        json.dump(data, json_file,indent=4)



    
    
    # result = [latencyoutput,latencytime,weightoutput,weighttime]


    rhsbw = bwlinklist(g,link_list)

    with open("/Users/yifeiwang/Desktop/5.3code/pce/test/data/latency_list.json") as f:
        latency_list = json.load(f)
    latconstraintmaker(source_destination_list, latency_list)
    linknum = len(link_list)
    jsonfilemaker(nodes, inputmatrix, inputdistance, source_destination_list,rhsbw, linknum)
    print("link##: "+str(len(link_list)))
    print(source_destination_list)


    return ("Random Graph is created with " + str(nodes) + " nodes, probability of link creation is " + str(p))

    
# request_list = [[1,15,5], [2,19,3],[0,13,1]]
print(lbnxgraphgenerator(25, 0.4))

