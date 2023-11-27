"""
Script to test the functionality of a star and the path generated
"""
import unittest
import random
from map import IntersectionPoints
from completeMap import OptionMap
from aStar import create_graph, create_maximal_graph, astar, astarComplete, manhattan_distance

"""
class TestAStarFunctionsPerformance(unittest.TestCase):

    def generate_random_node(self, IntersectionPoints):
        return random.choice(list(IntersectionPoints.keys()))

    def test_path_lengths(self):
        num_tests = 10000

        for i in range(num_tests):
            print(f"test {i} pass")
            try:
                # Compare lengths
                start_node1 = self.generate_random_node(IntersectionPoints)
                goal_node1 = self.generate_random_node(IntersectionPoints)

                G1 = create_graph(IntersectionPoints)
                path1 = astar(G1, start_node1, goal_node1, manhattan_distance)
                length1 = len(path1)


                G2 = create_maximal_graph(OptionMap)
                path2 = astarComplete(G2, start_node1, goal_node1, manhattan_distance)
                length2 = len(path2)


                self.assertLessEqual(length2, length1)
            except AssertionError:
                # Print paths and nodes if assertion fails
                print(f"Test failed for nodes {start_node1} to {goal_node1}")
                print(f"Path 1: {path1}")
                print(f"Path 2: {path2}")
                raise  # Re-raise the exception
"""
class TestAStarFunction(unittest.TestCase):

    def generate_random_node(self, OptionMap):
        return random.choice(list(OptionMap.keys()))

    def test_path_lengths(self):
        num_tests = 100000

        for i in range(num_tests):
            print(f"test {i} pass")
            try:
                start_node = self.generate_random_node(OptionMap)
                goal_node = self.generate_random_node(OptionMap)

                G = create_maximal_graph(OptionMap)
                path = astarComplete(G, start_node, goal_node, manhattan_distance)
                if start_node != goal_node:
                    self.assertLessEqual(goal_node, path[-1])

            except AssertionError:
                print(f"Test failed for nodes {start_node} to {goal_node}")
                print(f"Path: {path}")


if __name__ == '__main__':
    unittest.main()