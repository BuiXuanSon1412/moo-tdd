from problem import Problem
from population import Individual
from copy import deepcopy
from decode_time_greedy import *
import random
def random_permutation(n):
    numbers = list(range(1, n+1))
    random.shuffle(numbers)
    return numbers

def random_binary_vector(n, p):
    vec = []
    for _ in range(n):
        if random.random() < p:   # random() ~ U[0,1)
            vec.append(0)
        else:
            vec.append(1)
    return vec

def cal_fitness(indi: Individual, problem: Problem):
    temp_chromosome = deepcopy(indi.chromosome)
    temp_chromosome = repair_distance(temp_chromosome, problem)
    temp_chromosome = repair_capacity(temp_chromosome, problem)
    if temp_chromosome == False:
        return indi.chromosome, np.inf, np.inf, np.inf
    assigned_truck_customers, assigned_drone_customers = extract_routes(temp_chromosome, problem)
    truck_solutions, drone_solutions = find_solution(assigned_truck_customers, assigned_drone_customers, problem)
    i = 0
    while truck_solutions == False and i <= problem.number_customer:
        idx = temp_chromosome[0].index(drone_solutions)
        temp_chromosome[1][idx] = 0

        temp_chromosome = repair_distance(temp_chromosome, problem)
        temp_chromosome = repair_capacity(temp_chromosome, problem)
        if temp_chromosome == False:
            return indi.chromosome, np.inf, np.inf, np.inf
        assigned_truck_customers, assigned_drone_customers = extract_routes(temp_chromosome, problem)
        truck_solutions, drone_solutions = find_solution(assigned_truck_customers, assigned_drone_customers, problem)
        i = i + 1
    if truck_solutions == False:
        return indi.chromosome, np.inf, np.inf, np.inf
    total_cost = problem.cal_total_cost(truck_solutions, drone_solutions)
    wait_time = problem.customer_wait_max(truck_solutions, drone_solutions)
    fainess = problem.cal_truck_fairness(truck_solutions)
    return temp_chromosome, total_cost, wait_time, fainess


def init_random(problem: Problem, pro_drone):
    dimension = problem.number_customer + problem.number_of_trucks+ problem.number_of_drones-2
    per_customers = random_permutation(dimension)
    drone_truck_assign = random_binary_vector(dimension, pro_drone)
    chromosome = [per_customers, drone_truck_assign]
    print(chromosome)
    indi = Individual(chromosome)
    return indi




    


