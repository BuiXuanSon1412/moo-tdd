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
    


# if __name__ == '__main__':
#     N_list = [32, 64, 128, 256, 512]
#     M = 100
#     K = 10
#     for N in N_list:
        
#         channel_path = r'Channel\channel_' + str(N) + 'users_surveyRIS.json'
#         H, u, g = read_channel(channel_path)
#         Eb = 0.25
#         Es = 1
#         m_qam = 16
#         pop_size = 100
#         max_gen = 5
#         CR_init = 0.9
#         F_init = 0.1
#         num_pro = 10
#         SINR_SER = []
#         Sum_RATE = []
#         Direct_SER = []
#         CR = 0.9
#         F = 0.1
#         Es_No = np.arange(0, 21, 4)
#         for es_no in Es_No:
#             No = Es * 10**(-es_no/10)
#             channel = Channel(H, u, g, M, N, Eb, Es, No, K, m_qam)
#             initilize_indi_path = r"Initialize_pop_RIS\Individual_" + str(N) +"RIS.json"
#             indi_list = initialize_indi_from_file(initilize_indi_path)

#             ##### NSGA-II ############
#             nsgaii_start = time.time()
#             nsgaii_history = run_nsga_ii(num_pro, channel, indi_list, pop_size, max_gen, crossover_operator, mutation_operator,
#                             CR_init, F_init, cal_fitness)
#             nsgaii_end = time.time()
#             nsgaii_result = {}
#             nsgaii_result['time'] = nsgaii_end - nsgaii_start
#             nsgaii_result['history'] = nsgaii_history
#             nsgaii_path = r"Result_grid\nsgaii_" +  str(N) +"RIS.json"
#             with open(nsgaii_path, 'w') as f:
#                 json.dump(nsgaii_result, f)

#             # ##### NSGA-III ############
#             # nsgaiii_start = time.time()
#             # nsgaiii_history = run_nsga_iii(num_pro, channel, indi_list, pop_size, max_gen, crossover_operator, mutation_operator,
#             #                 CR_init, F_init, cal_fitness)
#             # nsgaiii_end = time.time()
#             # nsgaiii_result = {}
#             # nsgaiii_result['time'] = nsgaiii_end - nsgaiii_start
#             # nsgaiii_result['history'] = nsgaiii_history
#             # nsgaiii_path = r"Result_MOO\NSGAIII\result_" + str(K) +"users_" + str(es_no)+ "Es_No_" + str(N) +"RIS.json"
#             # with open(nsgaiii_path, 'w') as f:
#             #     json.dump(nsgaiii_result, f)

#             ##### MOEAD ############
#             moead_start = time.time()
#             moead_history = run_moead(num_pro, channel, indi_list, pop_size, max_gen, 5, init_weight_vectors_4d, crossover_operator, mutation_operator, cal_fitness)
#             moead_end = time.time()
#             moead_result = {}
#             moead_result['time'] = moead_end - moead_start
#             moead_result['history'] = moead_history
#             moead_path = r"Result_grid\moead_" +  str(N) +"RIS.json"
#             with open(moead_path, 'w') as f:
#                 json.dump(moead_result, f)

            
#             ##### PFG_MOEA ############
#             pfg_start = time.time()
#             pfg_history = run_pfgmoea_rand_1(num_pro, channel, indi_list, pop_size, max_gen, 5, 0.01, F, CR, cal_fitness)
#             pfg_end = time.time()
#             pfg_result = {}
#             pfg_result['time'] = pfg_end - pfg_start
#             pfg_result['history'] = pfg_history
#             pfg_path = r"Result_grid\pfg_" +  str(N) +"RIS.json"
#             with open(pfg_path, 'w') as f:
#                 json.dump(pfg_result, f)

#             #### MODE ############
#             mode_start = time.time()
#             mode_history = run_mode(num_pro, channel, indi_list, pop_size, max_gen, F, CR, cal_fitness)
#             mode_end = time.time()
#             mode_result = {}
#             mode_result['time'] = mode_end - mode_start
#             mode_result['history'] = mode_history
#             mode_path = r"Result_grid\mode_" +  str(N) +"RIS.json"
#             with open(mode_path, 'w') as f:
#                 json.dump(mode_result, f)

#             ##### MOPSO ############
#             mopso_start = time.time()
#             mopso_history = run_mopso(num_pro, channel, indi_list, pop_size, max_gen, 0.9, 0.1, 0.1, cal_fitness)
#             mopso_end = time.time()
#             mopso_result = {}
#             mopso_result['time'] = mopso_end - mopso_start
#             mopso_result['history'] = mopso_history
#             mopso_path = r"Result_grid\mopso_" +  str(N) +"RIS.json"
#             with open(mopso_path, 'w') as f:
#                 json.dump(mopso_result, f)

#             ##### Proposed ############
#             proposed_start = time.time()
#             proposed_history = run_pfgmoea_best_1_pareto(num_pro, channel, indi_list, pop_size, max_gen, 5, 0.01, F, CR, cal_fitness)
#             proposed_end = time.time()
#             proposed_result = {}
#             proposed_result['time'] = proposed_end - proposed_start
#             proposed_result['history'] = proposed_history
#             proposed_path = r"Result_grid\proposed_" +  str(N) +"RIS.json"
#             with open(proposed_path, 'w') as f:
#                 json.dump(proposed_result, f)
            


            
            
