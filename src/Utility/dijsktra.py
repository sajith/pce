import copy

# use dijsktra to get the primary shortest path
def dijnew(graph, start_node, end_node):
    graph_new = graph_simplify(graph)
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph_new
    infinity = 9999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start_node] = 0

    while unseenNodes:  # loop all the nodes in the list
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node  # find the current node

        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)

    currentNode = end_node  # run path backwards to get the real path
    while currentNode != start_node:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0, start_node)
    if shortest_distance[end_node] != infinity:  # check if the end_node has been reached
        print('Shortest distance is ' + str(shortest_distance[end_node]))
        print('And the path is ' + str(path))
    return path


# make the non-simple graph to be the simple graph
def graph_simplify(graph):
    for node in graph:
        for endpoint in graph[node]:
            try:
                if len(graph[node][endpoint]) > 1:
                    shortest = min(graph[node][endpoint])
                    graph[node][endpoint] = shortest
            except TypeError:
                pass
    return graph


# remove the primary shortest path and redo the dijsktra to get the backup path
def backup_path(graph, start_node, end_node):
    backupstart_node = start_node
    backupend_node = end_node
    graphprimary = copy.deepcopy(graph)
    graph_original = copy.deepcopy(graph)
    graph_new = graph_simplify(graph)
    print("The primary path: ")
    path = dijnew(graphprimary, start_node, end_node)
    path_new = path.copy()
    path_new.pop()

    for ele in path_new:  # update the graph, delete the path that was used in primary path
        index = path.index(ele)
        try:
            graph_original[ele][path[index + 1]].remove(graph_new[ele][path[index + 1]])
        except AttributeError:
            del graph_original[ele][path[index + 1]]

    for start_node in graph_original:  # reformat the updated graph list
        for end_node in graph_original[start_node]:
            try:
                if len(graph_original[start_node][end_node]) == 1:
                    graph_original[start_node][end_node] = graph_original[start_node][end_node][0]
            except TypeError:
                continue

    print("The back up path: ")
    dijnew(graph_original, backupstart_node, backupend_node)
