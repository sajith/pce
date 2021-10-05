#
import ast
import functions as functions


def connectedgraph(filename):
    file = open(filename,"r")
    contents = file.read()
    link_list = ast.literal_eval(contents)
    file.close()

    unvisited_list=functions.create_unvisited_list(link_list)

    stack={}

    stack[list(link_list.keys())[0]]=0 #assign the first node in stack the 0 value

    c=-1
    null_value=0
    while True:
        if null_value in stack.values():
            if stack[list(stack)[c]]==0:    #if the last element has a null_value
                stack[list(stack)[c]]=1
                for ele in link_list[list(stack)[c]]:
                    if ele in unvisited_list:
                        unvisited_list.remove(ele)
                        stack[ele]=0
                print("unvisited node list: "+ str(unvisited_list))
                print("stack_new "+str(stack))
            else:
                c=c-1
        else:
            if len(unvisited_list):
                print("The graph is not connected.")
            else:
                print("The graph is connected.")
            break



connectedgraph("connected_graph.txt")
