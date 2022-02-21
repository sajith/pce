# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:25:20 2021

@author: Michael
"""

from ortools.linear_solver import pywraplp
import numpy as np
import json

import time



def create_data_model():
    with open('data.json') as f:
          graph = json.load(f)
  
  
    data = {}
    data['constraint_coeffs'] = graph['constraint_coeffs']
    max_latency = graph["max_latency"]

    data['bounds'] = graph['bounds']
    data['bounds'].append(int(max_latency)) # append the user input min_latency to the RHS of the last constraint



    data['obj_coeffs'] = graph['obj_coeffs']
    data['num_vars'] = len(data['constraint_coeffs'][0])
    data['num_constraints'] = graph['num_constraints']
    
    return data

def pathlookup(solution):
    with open('linklist.json') as f:
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




def solvermethod():
    data = create_data_model()
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = {}

    # set the variables to be binary
    for j in range(data['num_vars']):
        x[j] = solver.IntVar(0, 1, 'x[%i]' % j)
    print('Number of variables =', solver.NumVariables())

    # setup the equality of the constraints and RHS
    for i in range(data['num_constraints'] - 1):
        constraint = solver.RowConstraint(data['bounds'][i], data['bounds'][i], '')
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])


    # set the limit of latency to be the last constraint
    constraint = solver.RowConstraint(0, data['bounds'][-1], '')


    for j in range(data['num_vars']):
        constraint.SetCoefficient(x[j], data['constraint_coeffs'][-1][j])
    print('Number of constraints =', solver.NumConstraints())

    # setup the objective function
    objective = solver.Objective()
    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])
    objective.SetMinimization()

    status = solver.Solve()

    solution = []
    if status == pywraplp.Solver.OPTIMAL:
        value = solver.Objective().Value()
        # print('Objective value =', solver.Objective().Value())
        for j in range(data['num_vars']):
            print(x[j].name(), ' = ', x[j].solution_value())
            solution.append(x[j].solution_value())
        total_latency = sum(np.multiply(np.array(solution), np.array(data['constraint_coeffs'][-1])))

    else:
        print('The problem does not have an optimal solution.')

    linkselection = pathlookup(solution)
    solutionnum = solutiontranslator(solution)
    return linkselection




print(solvermethod()[0])

