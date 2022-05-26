import unittest
import json
from LoadBalancing.LB_Utilization_Solver import runLB_UT_Solver
from LoadBalancing.RandomTopologyGenerator import GetNetworkToplogy
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator

class Test_Load_Balancing_Solver(unittest.TestCase):
    def setUp(self):
        with open('data/test_connection.json', 'r') as f:
            connection = json.load(f)
        with open('data/test_LB_solution.json', 'r') as s:
            solution = json.load(s)
        self.connection = connection
        self.topology = GetNetworkToplogy(25,0.4)
        self.solution = solution

    def test_Computation(self):
        lbnxgraphgenerator(25, 0.4, self.connection, self.topology)
        result = runLB_UT_Solver()

        self.assertEqual(self.solution, result)


if __name__ == '__main__':
    unittest.main()




