## same nodes now input request: [10,15]
from randomgraph import nxgraphgenerator
from randomgraph import jsonfilemaker
from solver import solvermethod
import json

input = {1:50, 2:20, 3:30}

def greedysort(bwinput):
    return dict(sorted(bwinput.items(), key=lambda item: item[1], reverse = True))

# def dataupdate(g, ):

def overloadcheck(bw, bwlinklist):
    index = 0
    congestion = []
    for link in bwlinklist:
        if link < bw:
            congestion.append(index)
        index+=1
    return congestion

def overloadlink_update(congestion):
    with open('/Users/yifeiwang/Desktop/test214/pce/test/data/data.json') as f:
        data = json.load(f)
    for link in congestion:
        data["obj_coeffs"][link] = 10**10
    with open("/Users/yifeiwang/Desktop/test214/pce/test/data/data.json", "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)




def multipleinputtest(bwinput):
    inputlist = greedysort(bwinput)
    maxbw = list(inputlist.values())[0]
    nxgraphgenerator(25, 0.1, 10000, maxbw-10)
    output = {}
    for input in inputlist:
        bw = inputlist[input]

        with open('/Users/yifeiwang/Desktop/test214/pce/test/data/bwlinklist.json') as f:
              bwlinklist = json.load(f)
        congestion = overloadcheck(bw, bwlinklist)
        print("congestion"+str(congestion))
        overloadlink_update(congestion)

        linkselection = solvermethod()[1]
        for link in linkselection:
            bwlinklist[link] = bwlinklist[link]-maxbw
        with open("/Users/yifeiwang/Desktop/test214/pce/test/data/bwlinklist.json", "w") as jsonFile:
            json.dump(bwlinklist, jsonFile)
        output[input] = linkselection
    return output










print(multipleinputtest(input))
# print(greedysort(input))





