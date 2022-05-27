import unittest
import json
from LoadBalancing.RandomTopologyGenerator import GetConnection
from LoadBalancing.LB_Utilization_Solver import runLB_UT_Solver
from LoadBalancing.RandomTopologyGenerator import GetNetworkToplogy
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator

class Test_Load_Balancing_Solver(unittest.TestCase):
    def setUp(self):
        with open('data/test_LB_solution.json', 'r') as s:
            solution = json.load(s)
        self.connection = GetConnection('data/test_connection.json')
        self.topology = GetNetworkToplogy(25,0.4)
        self.solution = solution
        with open('data/connection.json', 'w') as json_file:
            json.dump(self.connection, json_file, indent=4)

    def test_Computation(self):
        lbnxgraphgenerator(25, 0.4, self.connection, self.topology)
        result = runLB_UT_Solver()

        self.assertEqual(self.solution, result)


if __name__ == '__main__':
    unittest.main()




