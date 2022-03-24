import unittest
import json
from LoadBalancing.Multi_Input_Solver import LB_Solver

class Test_Load_Balancing_Solver(unittest.TestCase):
    def setUp(self):
        with open('/Users/yifeiwang/Desktop/test214/pce/test/data/LB_data.json', 'r') as f:
            file = json.load(f)
        with open('/Users/yifeiwang/Desktop/test214/pce/test/data/Test_solution.json', 'r') as s:
            solution = json.load(s)
        self.data = file
        self.solution = solution

    def test_Computation(self):

        result = LB_Solver(self.data)

        self.assertEqual(self.solution, result)


if __name__ == '__main__':
    unittest.main()




