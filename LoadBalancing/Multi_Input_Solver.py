

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 13:42:31 2022

@author: yifeiwang
"""

from ortools.linear_solver import pywraplp
import json


def create_data_model(graph):
    # with open('Test_LB_data.json') as f:
    #       graph = json.load(f)
  
  
    data = {}
    data['constraint_coeffs'] = graph['constraint_coeffs']
    # max_latency = graph["max_latency"]

    data['bounds'] = graph['bounds']
    # data['bounds'].append(int(max_latency)) # append the user input min_latency to the RHS of the last constraint



    data['obj_coeffs'] = graph['obj_coeffs']
    data['num_vars'] = graph["num_vars"]
    data['num_constraints'] = graph['num_constraints']
    num_inequality = graph['num_inequality']
    
    return (data, num_inequality)

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]


def pathlookup(solution, linknum,linklist):
    with open(linklist) as f:
        linklist = json.load(f)
    
    linkindex = []
    for i in range(len(solution)):
        if abs(solution[int(i)] - 1) < 0.01:
            linkindex.append(i)
    linkselection = []

    for i in linkindex:
        linkselection.append(linklist[int(i)])
    return (linkselection,linkindex)

def solutiontranslator(solution):
    output = []
    c = 0
    for i in solution:
        if abs(i - 1) <= 0.001:
            output.append(c)
        c+=1
    return output

def solution_translator(solution,linklistname):
    with open(linklistname) as f:
        linklist = json.load(f)
    link_num = len(linklist)
    print("num"+str(link_num))
    solution_list = list(split(solution, link_num))
    path_list = {}
    c = 1
    for request in solution_list:
        individual_solution = []
        i = 0
        
        for solution in request:
            if abs(solution - 1) < 0.01:
                print(i)
                individual_solution.append(linklist[i])
            i += 1
                                
        path_list[c] = individual_solution
        c+=1
    ordered_path_list = pathordering(path_list)
    return ordered_path_list




def pathordering(path_list):
    ordered_path_list = {}
    source_list = []
    c = 0
    with open('/Users/yifeiwang/Desktop/test214/pce/test/data/query.json') as f:
          query_list = json.load(f)
    for query in query_list:
        source_list.append(query[0])

    for query in path_list:
        source_node = source_list[c]
        ordered_path_list[query] = []
        while len(path_list[query]) != 0:
            for path in path_list[query]:
                if path[0] == source_node:
                    ordered_path_list[query].append(path)
                    source_node = path[1]
                    path_list[query].remove(path)
        c+=1
    return ordered_path_list


#
# path_list = {1: [[1, 27], [7, 15], [27, 7]], 2: [[2, 20], [20, 19]], 3: [[0, 32], [27, 30], [32, 27]]}
# print(pathordering(path_list))


def LB_Solver(data):
    graph = create_data_model(data)
    data = graph[0]
    num_inequality = graph[1]
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')


    x = {}
    for j in range(data['num_vars']):
        x[j] = solver.IntVar(0, 1, 'x[%i]' % j)
    print('Number of variables =', solver.NumVariables())


    for i in range(data['num_constraints']-num_inequality):
      constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
      solver.Add(sum(constraint_expr) == data['bounds'][i])
    for i in range(data['num_constraints']-num_inequality, data['num_constraints']):
      constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
      solver.Add(sum(constraint_expr) <= data['bounds'][i])     
    print('Number of constraints =', solver.NumConstraints())

    objective = solver.Objective()
    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])
    objective.SetMinimization()


    status = solver.Solve()
    solution = []

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for j in range(data['num_vars']):
            print(x[j].name(), ' = ', x[j].solution_value())
            solution.append(x[j].solution_value())
        print()
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    else:
        print('The problem does not have an optimal solution.')
    
    return solution
    # print(solution)
    # linkselection = pathlookup(solution, num_inequality)
    # solutionnum = solutiontranslator(solution)
    # print(linkselection)
    # print(solutionnum)
    
    
with open('/Users/yifeiwang/Desktop/test214/pce/test/data/LB_data.json') as f:
      data = json.load(f)
# file = "Test_LB_data.json"
solution = LB_Solver(data)
print(solution)

print(solution_translator(solution,'/Users/yifeiwang/Desktop/test214/pce/test/data/LB_linklist.json'))


