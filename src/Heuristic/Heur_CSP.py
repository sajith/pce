from LoadBalancing.MC_Solver import runMC_Solver
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator
from LoadBalancing.RandomTopologyGenerator import GetNetworkToplogy
import json


def ConnectionSplit(connection):
    with open('./tests/data/splittedconnection.json', 'w') as json_file:
        data = connection
        json.dump(data, json_file, indent=4)


def Heuristic_CSP(connection,g):
    ConnectionSplit(connection)
    pathlist = {}
    cost = 0
    c = 1
    with open('./tests/data/splittedconnection.json') as f:
          connection= json.load(f)
    for query in connection:
        singleconnection = [query]
        with open('./tests/data/connection.json', 'w') as json_file:
            data = singleconnection
            json.dump(data, json_file, indent=4)

        lbnxgraphgenerator(25, 0.4,data, g)

        solution = runMC_Solver()
        pathlist[str(c)]=solution[0]["1"]
        cost += solution[1]
        c+=1

    return[pathlist,cost]

# with open('../test/data/connection.json') as f:
#       connection= json.load(f)
#
# g = GetNetworkToplogy(25,0.4)
# print(Heuristic_CSP(connection,g))



