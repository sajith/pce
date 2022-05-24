from LoadBalancing.MC_Solver import runMC_Solver
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator
import json

def ConnectionSplit():
    with open('../test/data/connection.json') as f:
          connection= json.load(f)
    with open('../test/data/splittedconnection.json', 'w') as json_file:
        data = connection
        json.dump(data, json_file, indent=4)


def Heuristic_CSP():
    ConnectionSplit()
    pathlist = {}
    cost = 0
    c = 1
    with open('../test/data/splittedconnection.json') as f:
          connection= json.load(f)
    for query in connection:
        singleconnection = [query]
        with open('../test/data/connection.json', 'w') as json_file:
            data = singleconnection
            json.dump(data, json_file, indent=4)

        lbnxgraphgenerator(25, 0.4)

        solution = runMC_Solver()
        pathlist[c]=solution[0][1]
        cost += solution[1]
        c+=1

    print(pathlist,cost)

Heuristic_CSP()



