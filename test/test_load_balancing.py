import unittest
import json
from LoadBalancing.MC_Solver import MC_Solver

class Test_Load_Balancing_Solver(unittest.TestCase):
    def setUp(self):
        with open('/Users/yifeiwang/Desktop/test214/pce/test/data/Test_LB_data.json', 'r') as f:
            file = json.load(f)
        with open('/Users/yifeiwang/Desktop/test214/pce/test/data/Test_solution.json', 'r') as s:
            solution = json.load(s)
        self.data = file
        self.solution = solution

    def test_Computation(self):

        result = MC_Solver(self.data)[0]

        self.assertEqual(self.solution, result)


if __name__ == '__main__':
    unittest.main()




