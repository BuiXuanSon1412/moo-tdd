from utils import *
from data import load_data
from moo_algorithm.nsga_ii import run_nsga_ii
from moo_algorithm.pfg_moea import run_pfgmoea
from moo_algorithm.nsga_iii import run_nsga_iii
from moo_algorithm.moead import run_moead, init_weight_vectors_3d
if __name__ == "__main__":
    number_customer = 100
    number_truck = 10
    number_drone = 15
    problem = load_data(r"data\100customers\r110.txt", number_customer, number_truck, number_drone)
    for customer in problem.customer_list:
        print(customer)

    processing_number = 8
    # from utils import crossover_PMX, mutation_flip, init_random
    pro_drone = 0.7
    pop_size = 10
    max_gen = 10
    crossover_rate = 0.8
    mutation_rate = 0.7
    indi_list = []
    for i in range(pop_size):
        indi = init_random(problem, pro_drone)
        indi_list.append(indi)
    result_nsga_ii = run_nsga_ii(processing_number, problem, indi_list, pop_size, max_gen, crossover_PMX, mutation_flip, crossover_rate, mutation_rate, cal_fitness)
    
    GK = 3
    sigma = 0.1

    result_pfgmoea = run_pfgmoea(processing_number, problem, indi_list, pop_size, max_gen, GK, sigma, crossover_PMX, mutation_flip, 
                crossover_rate, mutation_rate, cal_fitness)
    
    result_nsga_iii = run_nsga_iii(processing_number, problem, indi_list, pop_size, max_gen, 
                                   crossover_PMX, mutation_flip, crossover_rate, mutation_rate, cal_fitness)
    neighborhood_size = 5
    result_moead = run_moead(processing_number, problem, indi_list, pop_size, max_gen, neighborhood_size, init_weight_vectors_3d, crossover_PMX,
                             mutation_flip, cal_fitness)
