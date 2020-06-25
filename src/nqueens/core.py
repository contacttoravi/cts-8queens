import numpy as np
import random
from pprint import pprint as pp


class NQueens(object):
    def __init__(self, board_length=4, population_count=10, mutation_probability=0.025, verbose=True):
        self.board_length = board_length
        self.population_count = population_count
        self.population = None
        self.solution = None
        self.scores = None
        self.target_score = self.get_target_score()
        self.progress = []
        self.mutation_probability = mutation_probability
        self.verbose = verbose

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

    def evaluate_population(self, population=None):
        scores = []
        if not population:
            population = self.population

        for individual in population:
            scores.append(self.evaluate(individual))
        return scores

    def print_board(self, solution, format_display=True):
        board = np.zeros((self.board_length, self.board_length))
        rows = solution
        cols = range(0, self.board_length)
        for (row, col) in zip(rows, cols):
            board[row, col] = 1
        print("\n")
        if format_display:
            for row in board:
                line = ""
                for col in row:
                    if col:
                        line = line + "Q "
                    else:
                        line = line + "- "
                print(line)
        else:
            pp(board)

    def select_individual_by_tournament(self):
        # Select 2 random individuals and return best of them
        fighter1 = random.randint(0, self.population_count - 1)
        fighter2 = random.randint(0, self.population_count - 1)
        while fighter2 == fighter1:
            fighter2 = random.randint(0, self.board_length - 1)

        if self.scores[fighter1] >= self.scores[fighter2]:
            winner = fighter1
        else:
            winner = fighter2
        return np.copy(self.population[winner])

    def breed_by_crossover(self, parent1, parent2):
        # Pick crossover point, avoding ends
        crossover_point = random.randint(1, self.board_length - 2)

        # Create children
        child1 = np.hstack((parent1[0: crossover_point], parent2[crossover_point:]))
        child2 = np.hstack((parent2[0: crossover_point], parent1[crossover_point:]))

        return child1, child2

    def mutate_population(self, population, mutation_probability=0.025):
        # mutation_probability is % population need to be mutated
        if mutation_probability > 100:
            raise Exception("mutation_probability should be between 0 and 100")

        mutation_count = int(self.population_count * mutation_probability)
        for count in range(0, mutation_count):
            start_position = random.randint(0, self.population_count - 1)
            random_swap_index1 = random.randint(0, self.board_length - 1)
            random_swap_index2 = random.randint(0, self.board_length - 1)
            val0 = population[start_position][random_swap_index1]
            population[start_position][random_swap_index1] = population[start_position][random_swap_index2]
            population[start_position][random_swap_index2] = val0

    def __call__(self):
        if self.verbose:
            print("Target Score is: {}".format(self.target_score))

        # Set execution limits. If target solution not found in max generations then start from scratch again
        # Do this till max attempts exceed and then give up with best solution.
        max_generations = 100
        max_attempts = 20
        best_solution = None

        for attempt in range(1, max_attempts):
            # Start from randomness
            self.population = self.get_initial_population()

            if self.verbose:
                print("\nStarting attempt #{}".format(attempt))
                print("Initial Population:")
                pp(self.population)

            for generation_index in range(0, max_generations):
                self.scores = self.evaluate_population()
                self.progress.append(sum(self.scores))
                if self.verbose:
                    print("Generation {} score: {}, Scores: {}".format(generation_index, sum(self.scores), self.scores))

                # sort population based on scores
                sorted_population = sorted(zip(self.scores, self.population), key=lambda x: x[0], reverse=True)

                # check for target reached
                if sorted_population[0][0] >= self.target_score:
                    target_solution = sorted_population[0][1]
                    if self.verbose:
                        print("\nFound Final Solution:")
                        self.print_board(target_solution)
                        print("\nFinal Solution: {}".format(target_solution))
                    return target_solution

                # update best solution so far
                if not best_solution or best_solution[0] < sorted_population[0][0]:
                    best_solution = sorted_population[0]

                # produce children
                new_population = []
                while len(new_population) < self.population_count:
                    parent1 = self.select_individual_by_tournament()
                    parent2 = self.select_individual_by_tournament()
                    child1, child2 = self.breed_by_crossover(parent1, parent2)
                    new_population.append(child1)
                    new_population.append(child2)

                # mutation
                self.mutate_population(population=new_population, mutation_probability=self.mutation_probability)

                # Get scores of new population
                new_scores = self.evaluate_population(population=new_population)
                min_new_pop_score = min(new_scores)

                # if there are any better scores in old population, then keep those individuals in new population
                for score, individual in sorted_population:
                    if score > min_new_pop_score:
                        if (new_population == individual).all(1).any():
                            # This individual is already present
                            pass
                        else:
                            new_population.append(individual)
                            new_scores.append(score)

                # select top scores from new population for gen next keeping same population count
                sorted_new_population = sorted(zip(new_scores, new_population), key=lambda x: x[0], reverse=True)
                next_gen_population = []
                for i in range(0, self.population_count):
                    next_gen_population.append(sorted_new_population[i][1])

                # now we have got our next generation which is better than previous generation
                self.population = next_gen_population

        # Could not reach final solution, but lets see what is the best solution we hav got
        if self.verbose:
            print("\nFound best (but not target) Solution:")
            self.print_board(best_solution[1])
            print("\nBest Solution: {}".format(best_solution[1]))
        return None


if __name__ == "__main__":
    n_queens = NQueens(8, 40, 0.05)
    solution = n_queens()
