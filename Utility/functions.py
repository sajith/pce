# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 16:40:56 2021

@author: Michael
"""

def create_unvisited_list(link_list):
    unvisited_list=[]
    for keys in link_list:
        unvisited_list.append(keys)
    return unvisited_list

def create_unvisited_node(my_list):
    unvisited_node={}
    for keys in my_list:
         unvisited_node[keys]=0
    return  unvisited_node
        
def get_graph_info(link_list):
    key_list=[]
    for keys in link_list:
        key_list.append()
    print(key_list)
