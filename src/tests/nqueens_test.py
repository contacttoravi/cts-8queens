import unittest
import sys
sys.path.insert(0, "../../src")

from nqueens.core import NQueens


class TestCore(unittest.TestCase):
    def setUp(self):
        pass

    def test01_get_initial_population(self):
        obj = NQueens(4, 10)
        data = obj.get_initial_population()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 10, "Expecting 10 rows")
        self.assertEqual(len(data[0]), 4, "Expecting solution length 4")

    def test02_evaluate(self):
        obj = NQueens(4, 6)
        data = [2,0,1,3]
        score = obj.evaluate(data)
        self.assertEqual(score, 5)
        data = [0,1,2,3]
        score = obj.evaluate(data)
        self.assertEqual(score, 0)
        data = [0,2,3,1]
        score = obj.evaluate(data)
        self.assertEqual(score, 5)

    def test03_get_target_score(self):
        obj = NQueens(4, 6)
        self.assertEqual(6, obj.get_target_score())
        obj = NQueens(5, 6)
        self.assertEqual(10, obj.get_target_score())
        obj = NQueens(8, 6)
        self.assertEqual(28, obj.get_target_score())

    def test04_final_solution(self):
        obj = NQueens(8, 10)
        solution = [2, 5, 3, 0, 7, 4, 6, 1]
        score = obj.evaluate(solution)
        self.assertEqual(obj.target_score, 28)
        self.assertEqual(score, obj.target_score)

    def test05_generate_8x8_solution(self):
        obj = NQueens(8, 40, 0.05, False)
        solution = obj()
        self.assertIsNotNone(solution)
        score = obj.evaluate(solution)
        self.assertEqual(score, obj.target_score)

    def test06_generate_10x10_solution(self):
        obj = NQueens(10, 100, 0.025, False)
        solution = obj()
        self.assertIsNotNone(solution)
        score = obj.evaluate(solution)
        self.assertEqual(score, obj.target_score)
