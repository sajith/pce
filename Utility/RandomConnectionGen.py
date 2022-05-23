import numpy as np
import json


def RandomConnectionGenerator(nodes, querynum, bw, latencylimit):
    np.random.seed(2022)
    connection = []
    for i in range(querynum):
        query = []
        query.append(np.random.randint(1,(nodes+1)/2))
        query.append(np.random.randint((nodes+1)/2, nodes + 1))
        query.append(np.random.randint(1, bw+1))
        query.append(np.random.randint(latencylimit, latencylimit+latencylimit/2))
        connection.append(query)

    with open('../test/data/connection.json', 'w') as json_file:
        data = connection
        json.dump(data, json_file, indent=4)



RandomConnectionGenerator(20,3,100,1000)