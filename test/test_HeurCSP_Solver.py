import unittest
import json
from CSP.Heur_CSP import Heuristic_CSP
from LoadBalancing.RandomTopologyGenerator import GetConnection
from LoadBalancing.RandomTopologyGenerator import GetNetworkToplogy
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator

Topology = GetNetworkToplogy(25,0.4)
Connection = GetConnection('./test/data/test_connection.json')
Solution = './test/data/test_HeurCSP_solution.json'

class Test_HeurCSP_Solver(unittest.TestCase):
    def setUp(self):
        with open(Solution, 'r') as s:
            solution = json.load(s)
        self.connection = Connection
        self.topology = Topology
        self.solution = solution

        with open('./test/data/connection.json', 'w') as json_file:
            json.dump(self.connection, json_file, indent=4)

    def test_Computation(self):
        lbnxgraphgenerator(25, 0.4, self.connection, self.topology)
        result = Heuristic_CSP(self.connection,self.topology)

        self.assertEqual(self.solution, result)


if __name__ == '__main__':
    unittest.main()




