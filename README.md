# pce

## Google OR-Tools
Solver in this OR-Tools is used to solve for the optimal solution. It takes in the formulation matrix with defined obejective functions and relationships with RHS. 

In this project, links are set to be binary variables which means if a link is selected, the corresponding variable is 1, if a link is not selected, the variable is 0.

The object function will be the sum of cost of all selected links.


## Constrained Shortest Path (CSP)

Randomgraph is used to generate the topology of a network. Each link in the network will have three attributes: cost, latency and bandwidth.

Topology will be generated in .json file. Other link info files will aslo be generated for later use.

- nodes: Number of nodes in the graph
- p: Probability of link creation
- max_latency: Used for testing the heuristic sorting method. Can be set to 99999 for regular toplogy.
- bwlimit: Remove any link that is lower than this bwlimit. There is connectivity check before the final creation of the topology, new topology will be created if the current one is not connected.
