import numpy as np
import random
from pprint import pprint as pp


class NQueens(object):
    def __init__(self, board_length=4, population_count=10):
        self.board_length = board_length
        self.population_count = population_count
        self.population = None
        self.solution = None
        self.target_score = self.get_target_score()

    def get_initial_population(self):
        first_list = np.array(range(0, self.board_length))
        population = []
        for count in range(0, self.population_count):
            np.random.shuffle(first_list)
            population.append(np.copy(first_list))
        return population

    def evaluate(self, solution):
        score = 0
        y=0
        while y < self.board_length:
            x = solution[y]
            y1 = y+1
            while y1 < self.board_length:
                x1 = solution[y1]
                if x == x1:
                    # same row
                    pass
                elif y == y1:
                    # same column
                    pass
                elif (x+y1) == (y+x1):
                    # diagonally opposite
                    pass
                elif (x + y) == (x1 + y1):
                    # reverse diagonally opposite
                    pass
                else:
                    score = score + 1
                y1 = y1+1
            y = y+1
        return score

    def get_target_score(self):
        n = self.board_length - 1
        target_score = n * (n+1) / 2
        return target_score

    def evaluate_population(self):
        scores = []
        for individual in self.population:
            scores.append(self.evaluate(individual))
        return scores

    def __call__(self):
        print("Target Score is: {}".format(self.target_score))

        self.population = self.get_initial_population()
        print("Initial Population:")
        pp(self.population)

        scores = self.evaluate_population()
        print("Scores:")
        pp(scores)

        for (score, solution) in zip(scores, self.population):
            if score == self.target_score:
                print("Found Solution: {}".format(solution))
                self.print_board(solution)

    def print_board(self, solution):
        board = np.zeros((self.board_length, self.board_length))
        rows = solution
        cols = range(0, self.board_length)
        for (row, col) in zip(rows, cols):
            board[row, col] = 1
        print("\n")
        pp(board)


if __name__ == "__main__":
    four_queens = NQueens(8, 10)
    four_queens()




