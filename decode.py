from population import Individual
from copy import deepcopy


class Customer:
    def __init__(self, arrive_time, quantity, service_time, x, y):
        self.arrive_time = arrive_time
        self.quantity = quantity
        self.service = service_time
        self.x = x
        self.y = y


class Truck_Solution:
    def __init__(
        self, assigned_customers, recived_truck, recived_drone, arrive_time, leave_time
    ):
        self.assigned_customers = assigned_customers
        self.recived_truck = recived_truck
        self.recived_drone = recived_drone
        self.arrive_time = arrive_time
        self.leave_time = leave_time


class Drone_Trip:
    def __init__(self, assigned_customers, recived_drone, arrive_time, leave_time):
        self.assigned_customers = assigned_customers
        self.recived_drone = recived_drone
        self.arrive_time = arrive_time
        self.leave_time = leave_time


class Drone_Solution:
    def __init__(self, num_of_trips, trip_list):
        self.num_of_trips = num_of_trips
        self.trip_list = trip_list


class Problem:
    def __init__(
        self,
        customer_list: list[Customer],
        number_of_trucks,
        number_of_drones,
        distance_matrix_truck,
        distance_matrix_drone,
        truck_capacity,
        drone_capacity,
        drone_energy,
        speed_of_truck,
        speed_of_drone,
        launch_time,
        land_time,
        energy_consumption_rate,
        weight_of_drone,
    ):
        self.customer_list = customer_list
        self.number_of_trucks = number_of_trucks
        self.number_of_drones = number_of_drones
        self.distance_matrix_truck = distance_matrix_truck
        self.distance_matrix_drone = distance_matrix_drone
        self.truck_capacity = truck_capacity
        self.drone_capacity = drone_capacity
        self.drone_energy = drone_energy
        self.speed_of_truck = speed_of_truck
        self.speed_of_drone = speed_of_drone
        self.launch_time = launch_time
        self.land_time = land_time
        self.energy_consumption_rate = energy_consumption_rate
        self.weight_of_drone = weight_of_drone

    def check_truck_capacity(self, route):
        total = 0
        for customer in route:
            total = total + customer[1]
        if total <= self.truck_capacity:
            return True
        else:
            return False

    def check_drone_capacity(self, route):
        total = 0
        for customer in route:
            total = total + customer[1]
        if total <= self.drone_capacity:
            return True
        else:
            return False

    def cal_truck_route_time(self, route):
        total_time = 0
        if len(route) == 0:
            return 0
        total_time = (
            total_time
            + self.distance_matrix_truck[0][route[0][0]] / self.speed_of_truck
            + self.customer_list[route[0][0]].service
        )
        for i in range(len(route) - 1):
            total_time = (
                total_time
                + self.distance_matrix_truck[route[i][0]][route[i + 1][0]]
                / self.speed_of_truck
                + self.customer_list[route[i + 1][0]].service
            )
        total_time = (
            total_time
            + self.distance_matrix_truck[route[-1][0]][0] / self.speed_of_truck
        )
        return total_time

    def check_drone_energy_constraint(self, route):
        pass

    def check_truck_time_constraint(self, route):
        pass

    def cal_drone_route_time(self, route):
        pass

    """
    def check_truck_time_constraint(self, route):
        total_time = self.cal_truck_route_time(route)
        if total_time <= self.:
            return True
        else:
            return False

    def cal_drone_route_time(self, route):
        total_time = 0
        if len(route) == 0:
            return 0
        total_time = (
            total_time
            + self.tau_l
            + self.tilde_d[0][route[0][0]] / self.tilde_v
            + self.tau_r
            + self.customer_list[route[0][0]].t
        )
        for i in range(len(route) - 1):
            total_time = (
                total_time
                + self.tau_l
                + self.tilde_d[route[i][0]][route[i + 1][0]] / self.tilde_v
                + self.tau_r
                + self.customer_list[route[i + 1][0]].t
            )
        total_time = (
            total_time
            + self.tau_l
            + self.tilde_d[route[-1][0]][0] / self.tilde_v
            + self.tau_r
        )
        return total_time

    def check_drone_time_constraint(self, multi_route):
        total_time = 0
        for route in multi_route:
            total_time = total_time + self.cal_drone_route_time(route)
        if total_time <= self.T:
            return True
        else:
            return False

    def cal_drone_route_energy(self, route):
        total_energy = 0
        if len(route) == 0:
            return 0
        total_demand = 0
        for customer in route:
            total_demand = total_demand + customer[1]

        total_energy = (
            total_energy
            + self.lbda
            * (self.tilde_qo + total_demand)
            * self.tilde_d[0][route[0][0]]
            / self.tilde_v
        )
        total_demand = total_demand - route[0][1]
        total_energy = (
            total_energy + self.lbda * total_demand * self.customer_list[route[0][0]].t
        )
        for i in range(len(route) - 1):
            total_energy = (
                total_energy
                + self.lbda
                * (self.tilde_qo + total_demand)
                * self.tilde_d[route[i][0]][route[i + 1][0]]
                / self.tilde_v
            )
            total_demand = total_demand - route[i + 1][1]
            total_energy = (
                total_energy
                + self.lbda * total_demand * self.customer_list[route[i + 1][0]].t
            )

        total_energy = (
            total_energy
            + self.lbda
            * (self.tilde_qo + total_demand)
            * self.tilde_d[route[-1][0]][0]
            / self.tilde_v
        )
        return total_energy

    def check_drone_energy_constraint(self, route):
        total_energy = self.cal_drone_route_energy(route)
        if total_energy <= self.E:
            return True
        else:
            return False

    """


"""
Example: 2 trucks, 3 drones, 8 customers

[1, 10, 3, 7, 4, 9, 5, 6, 11, 8, 2]
[0,  0, 0, 1, 0, 0, 1, 0,  0, 1, 0]

0: truck
1: drone

0: truck split
-1: drone split

[1, 8]: customer annotation
9: truck partition
10, 11: drone partition


truck route: [1, 3, 4], [6, 2]
drone route: [], [7, 5], [8]

"""


def extract_routes(chromosome, problem: Problem):
    truck_routes = []
    drone_routes = []
    tmp_truck_route = []
    tmp_drone_route = []

    k = len(problem.customer_list) + 1
    d = len(problem.customer_list) + problem.number_of_trucks

    for i in range(len(chromosome[0])):
        if chromosome[0][i] >= k and chromosome[0][i] < d:
            truck_routes.append(tmp_truck_route)
            tmp_truck_route = []
            continue
        elif (
            chromosome[0][i] >= d
            and chromosome[0][i] < d + problem.number_of_drones - 1
        ):
            drone_routes.append(tmp_drone_route)
            tmp_drone_route = []
            continue

        if chromosome[1][i] == 0:
            tmp_truck_route.append(chromosome[0][i])
        elif chromosome[1][i] == 1:
            tmp_drone_route.append(chromosome[0][i])

    truck_routes.append(tmp_truck_route)
    drone_routes.append(tmp_drone_route)
    print("Truck routes:", truck_routes)
    print("Drone routes:", drone_routes)

    return truck_routes, drone_routes


def repair(individual: Individual, problem: Problem):
    chromosome = individual.chromosome

    if chromosome is None:
        return None

    truck_routes = []
    drone_routes = []
    tmp_truck_route = []
    tmp_drone_route = []

    k = len(problem.customer_list) + 1
    d = len(problem.customer_list) + problem.number_of_trucks

    # decode individual into a general solution which possibly get population
    # extract gene and its index of chromosome to fix later on
    for i in range(len(chromosome[0])):
        if chromosome[0][i] >= k and chromosome[0][i] < d:
            truck_routes.append(tmp_truck_route)
            tmp_truck_route = []
            continue
        elif (
            chromosome[0][i] >= d
            and chromosome[0][i] < d + problem.number_of_drones - 1
        ):
            drone_routes.append(tmp_drone_route)
            tmp_drone_route = []
            continue

        if chromosome[1][i] == 0:
            tmp_truck_route.append((i, chromosome[0][i]))
        elif chromosome[1][i] == 1:
            tmp_drone_route.append((i, chromosome[0][i]))

    truck_custs = [cust for route in truck_routes for cust in route]
    depot = 0
    truck_custs.append(depot)
    # repair drone_routes:
    #   ensure all customers are feasible for drone capacity
    #   ensure all customers are feasible for drone energy
    for drone_route in drone_routes:
        for chro_id, cust in drone_route:
            # violate capacity constraints
            if not problem.check_drone_capacity([cust]):
                chromosome[1][chro_id] = 0  # 0 for truck   1 for drone

            # violate energy constraints
            lch_cust = min(
                truck_custs,
                key=lambda truck_cust: problem.distance_matrix_drone[truck_cust][cust],
            )
            rem_truck_custs = [cust for cust in truck_custs if cust != lch_cust]
            ld_cust = min(
                rem_truck_custs,
                key=lambda truck_cust: problem.distance_matrix_drone[truck_cust][cust],
            )
            if not problem.check_drone_energy_constraint([lch_cust, cust, ld_cust]):
                chromosome[1][chro_id] = 0

    # repair truck_routes:
    #   ensure all routes are feasible for truck capacity


def split_drone_routes(truck_routes, drone_routes, problem):
    """
    split sequence of drone customers into trips
    and determine launching node and landing node
    """
    # list of customers who are departed up by trucks
    truck_custs = [cust for route in truck_routes for cust in route]
    depot = 0
    truck_custs.append(depot)

    drone_tripsets = [[]]

    for drone_id, drone_route in enumerate(drone_routes):
        # split current drone's customers sequence into feasible trips
        trip = []
        rem_truck_custs = deepcopy(truck_custs)
        # iterate through sequence of customers
        for drone_cust in drone_route:
            # when the trips is by far intitialized
            if not trip:
                # get the closest customer to launch
                lch_cust = min(
                    truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[truck_cust][
                        drone_cust
                    ],
                )

                # get the closest customer apart from launching customer to land
                rem_truck_custs = [cust for cust in rem_truck_custs if cust != lch_cust]
                pred_ld_cust = min(
                    rem_truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[drone_cust][
                        truck_cust
                    ],
                )

                # check energy and capacity feasibility
                if problem.check_drone_capacity(
                    [drone_cust]
                ) and problem.check_drone_energy_constraint(
                    [lch_cust, drone_cust, pred_ld_cust]
                ):
                    trip.append(lch_cust)
                    trip.append(drone_cust)

            # when the current drone is on a certain trip but still lands yet
            else:
                # get the closest customer as the landing customer apart from the launching customer
                pred_ld_cust = min(
                    rem_truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[drone_cust][
                        truck_cust
                    ],
                )
                # check capacity and energy feasibility of insertion of current 'drone_cust' into the current trip
                if problem.check_drone_capacity(
                    trip[1:] + [drone_cust]
                ) and problem.check_drone_energy_constraint(
                    trip + [drone_cust, pred_ld_cust]
                ):
                    trip.append(drone_cust)
                else:
                    # close the current trip by specifying the landing customer
                    ld_cust = min(
                        rem_truck_custs,
                        key=lambda truck_cust: problem.distance_matrix_drone[trip[-1]][
                            truck_cust
                        ],
                    )
                    trip.append(ld_cust)  # append landing customer into current trip
                    drone_tripsets[drone_id].append(
                        trip
                    )  # append current trip into list of the current drone's trips
                    rem_truck_custs = deepcopy(truck_custs)
                    trip.clear()  # empty the temporary trip to continue retrieval

    return drone_tripsets


# the individual can be decoded only when it is feasible
def decode(individual: Individual, problem: Problem):
    chromosome = individual.chromosome
    # extract sequences of customers for truck and drone
    truck_routes, drone_routes = extract_routes(chromosome, problem)
    drone_tripsets = split_drone_routes(truck_routes, drone_routes, problem)

    """
    to decode complete solution, compute the schedule
    """
    # rebuild truck routes by adding depot
    depart_depot = 0
    return_depot = len(problem.customer_list) + 1
    truck_routes = [
        [depart_depot] + truck_route + [return_depot] for truck_route in truck_routes
    ]

    # rebuild drone trips by adjusting return depot annotation to 'return depot'
    for trips in drone_tripsets:
        for i in range(len(trips)):
            if trips[i][-1] == 0 and len(trips[i]) > 0:
                trips[i][-1] = return_depot

    # compute matrix of travelling time between 2 specific customers of truck and drone
    time_by_truck = [
        problem.distance_matrix_truck[i][j] / problem.speed_of_truck
        for i in range(len(problem.distance_matrix_truck))
        for j in range(len(problem.distance_matrix_truck[0]))
    ]
    time_by_drone = [
        problem.distance_matrix_drone[i][j] / problem.speed_of_drone
        for i in range(len(problem.distance_matrix_drone))
        for j in range(len(problem.distance_matrix_drone[0]))
    ]

    # set of launching customers and landing customers
    ld_custs = [
        trip[-1]
        for trips in drone_tripsets
        for trip in trips
        if trip[-1] != return_depot
    ]

    # current identifier of current truck and drone in the specified route
    truck_route_idx = [0 for _ in range(len(problem.number_of_trucks))]  # (route_idx)

    # update these lists
    truck_arrival = [[0] * len(truck_route) for truck_route in truck_routes]
    truck_depart = deepcopy(truck_arrival)

    drone_arrival = [[[0] * len(trip) for trip in trips] for trips in drone_tripsets]
    drone_depart = deepcopy(drone_arrival)

    assemble = [0 for _ in range(len(problem.customer_list) + 1)]

    pickup_count = [0 for _ in range(len(problem.customer_list) + 1)]
    for trips in drone_tripsets:
        for trip in trips:
            if trip[-1] != return_depot:
                pickup_count[trip[-1]] = pickup_count[trip[-1]] + 1

    departed = [False for _ in range(len(problem.customer_list) + 2)]
    arrived = [False for _ in range(len(problem.customer_list) + 2)]
    arrived[0] = True

    while not all(
        [
            truck_route[truck_route_idx[truck_id]] == return_depot
            for truck_id, truck_route in enumerate(truck_routes)
        ]
    ):
        # let each truck reaches the nearest landing customer on its route
        for truck_id in range(problem.number_of_trucks):
            truck_route = truck_routes[truck_id]  # route of current truck
            route_idx = truck_route_idx[truck_id]
            while route_idx < len(truck_route) - 1:
                cur_cust = truck_route[route_idx]
                next_cust = truck_route[route_idx + 1]

                truck_arrival[truck_id][route_idx + 1] = (
                    truck_depart[truck_id][route_idx]
                    + time_by_truck[cur_cust][next_cust]
                )
                arrived[next_cust] = True

                if next_cust in ld_custs or next_cust == return_depot:
                    break

                truck_depart[truck_id][route_idx + 1] = (
                    truck_arrival[truck_id][route_idx + 1]
                    + problem.customer_list[next_cust].service
                    if truck_arrival[truck_id][route_idx + 1]
                    >= problem.customer_list[next_cust].arrive_time
                    else problem.customer_list[next_cust].arrive_time
                    + problem.customer_list[next_cust].service
                )
                assemble[next_cust] = (
                    truck_arrival[truck_id][route_idx + 1],
                    truck_depart[truck_id][route_idx],
                )
                departed[next_cust] = True
                route_idx = route_idx + 1

            truck_route_idx[truck_id] = route_idx + 1

        for drone_id in range(problem.number_of_drones):
            trips = drone_tripsets[drone_id]

            for trip_idx in range(len(trips)):
                cur_trip = trips[trip_idx]
                if arrived[cur_trip[0]] and (
                    not departed[cur_trip[-1]] or cur_trip[-1] == return_depot
                ):
                    for i in range(len(cur_trip)):
                        if i == 0:
                            drone_arrival[drone_id][trip_idx][i] = assemble[cur_trip[i]]
                            drone_depart[drone_id][trip_idx][i] = drone_arrival[
                                drone_id
                            ][trip_idx][i]
                        else:
                            drone_arrival[drone_id][trip_idx][i] = (
                                drone_depart[drone_id][trip_idx][i - 1]
                                + time_by_drone[cur_trip[i - 1]][cur_trip[i]]
                            )
                            arrived[cur_trip[i]] = True

                            if i == len(cur_trip) - 1:
                                break

                            drone_depart[drone_id][trip_idx][i] = (
                                max(
                                    drone_arrival[drone_id][trip_idx][i],
                                    problem.customer_list[cur_trip[i]].arrive_time,
                                )
                                + problem.customer_list[cur_trip[i]].service
                            )
                            departed[cur_trip[i]] = True
                    pickup_count[cur_trip[-1]] = pickup_count[cur_trip[-1]] - 1
                    assemble[cur_trip[-1]] = max(
                        assemble[cur_trip[-1]], drone_arrival[drone_id][trip_idx][-1]
                    )

        for truck_id in range(len(problem.number_of_trucks)):
            truck_route = truck_routes[truck_id]
            cur_cust = truck_route[truck_route_idx]
            if pickup_count[cur_cust] == 0:
                truck_depart[truck_id][truck_route_idx[truck_id]] = max(
                    assemble[cur_cust],
                    problem.customer_list[cur_cust].arrive_time
                    + truck_arrival[truck_id][truck_route_idx[truck_id]],
                )
                truck_route_idx[truck_id] = truck_route_idx[truck_id] + 1
                departed[cur_cust] = True

    return (
        truck_routes,
        drone_tripsets,
        truck_arrival,
        truck_depart,
        drone_arrival,
        drone_depart,
    )
