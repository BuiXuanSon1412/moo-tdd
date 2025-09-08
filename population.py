import math
import random
import copy
import heapq


'''
Individual chromosome structure:

'''

class Individual:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome
        self.objectives = None  # Objectives vector

        self.domination_count = None  # be dominated
        self.dominated_solutions = None  # dominate
        self.crowding_distance = None
        self.rank = None

    def gen_random(self, problem, create_solution):
        self.chromosome = create_solution(problem)

    # Dominate operator
    def dominates(self, other_individual):
        tolerance = 0
        and_condition = True
        or_condition = False
        # for first, second in zip(self.objectives, other_individual.objectives):
        #    and_condition = and_condition and (first <= second + tolerance)
        #    or_condition = or_condition or (first < second - tolerance)
        return and_condition and or_condition

    def repair(self):
        # for i in range(len(self.chromosome)):
        pass
