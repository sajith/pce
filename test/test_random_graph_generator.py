import unittest
from LoadBalancing.Multi_Input_LoadBalancer import lbnxgraphgenerator

class Test_random_graph_generator(unittest.TestCase):
    def setUp(self):
        self.request = [[1,15,5], [2,19,3],[0,13,1]]



    def test_Computation(self):

        result = lbnxgraphgenerator(40, 0.1,self.request, 999999, 5)
        print(result)
        return True


if __name__ == '__main__':
    unittest.main()
