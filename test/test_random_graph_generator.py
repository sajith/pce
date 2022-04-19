import unittest
from LoadBalancing.Multi_Input_LoadBalancer import lbnxgraphgenerator

class Test_random_graph_generator(unittest.TestCase):

    def test_Computation(self):

        result = lbnxgraphgenerator(40, 0.1, 999999)
        print(result)
        return True


if __name__ == '__main__':
    unittest.main()
