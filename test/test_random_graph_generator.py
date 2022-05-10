import unittest
from LoadBalancing.RandomTopologyGenerator import lbnxgraphgenerator

class Test_random_graph_generator(unittest.TestCase):

    def test_Computation(self):

        result = lbnxgraphgenerator(40, 0.1)
        print(result)
        return True


if __name__ == '__main__':
    unittest.main()
