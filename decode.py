from population import Individual
from copy import deepcopy
from problem import Drone_Trip, Problem, Truck_Solution
from itertools import combinations

"""
Example: 2 trucks, 3 drones, 8 customers

[1, 10, 3, 7, 4, 9, 5, 6, 11, 8, 2]
[0,  0, 0, 1, 0, 0, 1, 0,  0, 1, 0]

0: truck
1: drone


[1, 8]: customer annotation
9: truck partition
10, 11: drone partition


truck route: [1, 3, 4], [6, 2]
drone route: [], [7, 5], [8]

"""

"""
relaxed version of repair without full solution
"""


def relaxed_repair(chromosome, problem: Problem):
    # compute matrix of travelling time between 2 specific customers of truck and drone
    time_by_truck = [
        [dist / problem.speed_of_truck for dist in row]
        for row in problem.distance_matrix_truck
    ]
    time_by_drone = [
        [
            (problem.launch_time + problem.land_time + dist) / problem.speed_of_drone
            for dist in row
        ]
        for row in problem.distance_matrix_drone
    ]

    truck_routes = []
    drone_routes = []
    drone_triplists = []
    while True:
        truck_routes.clear()
        drone_routes.clear()

        tmp_truck_route = []
        tmp_drone_route = []

        k = len(problem.customer_list)
        d = len(problem.customer_list) + problem.number_of_trucks - 1

        def nearest_truck_partition(lst):
            for idx, e in enumerate(lst):
                if e in range(k, d):
                    return idx
            return None

        for i in range(len(chromosome[0])):
            # partition numbers in 1st layer of chromosome
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

            # save indices of chromosome's elements
            # append customer into current route
            if chromosome[1][i] == 0:  # truck customer
                if problem.check_capacity_truck_constraint(
                    tmp_truck_route + [chromosome[0][i]]
                ):  # if not violate truck capacity
                    tmp_truck_route.append(chromosome[0][i])
                else:
                    # if violate truck capacity, insert current partition into this position
                    idx = nearest_truck_partition(chromosome[0][i:])
                    chromosome[0].pop(idx)
                    chromosome[1].pop(idx)
                    chromosome[0].insert(i, chromosome[0][idx])
                    chromosome[1].insert(i, 0)
            elif chromosome[1][i] == 1:  # drone customer
                if (
                    problem.customer_list[chromosome[0][i]].quantity
                    <= problem.drone_capacity
                ):  # if not violate drone capacity
                    tmp_drone_route.append(chromosome[0][i])
                else:  # if violate drone capacity, change it to truck customer
                    chromosome[1][i] = 0
                    if problem.check_capacity_truck_constraint(
                        tmp_truck_route + [chromosome[0][i]]
                    ):
                        tmp_truck_route.append(chromosome[0][i])
                    else:
                        idx = nearest_truck_partition(chromosome[0][i:])
                        chromosome[0].pop(idx)
                        chromosome[1].pop(idx)
                        chromosome[0].insert(i, chromosome[0][idx])
                        chromosome[1].insert(i, 0)

        truck_routes.append(tmp_truck_route)
        drone_routes.append(tmp_drone_route)

        # route-trip extraction from chromosome will be ended when all customers will be delivered by trucks
        # also all these customers are well distributed to do not violated capacity constraint of truck
        if all(
            chromosome[0][i] >= k or chromosome[1][i] == 0
            for i in range(len(chromosome[1]))
        ):
            drone_triplists = [[] for _ in range(problem.number_of_drones)]

            return truck_routes, drone_triplists

        # mapping customers to their indices in chromosome
        mp_cust_chro = [-1 for _ in range(len(problem.customer_list) + 1)]
        for i in range(len(chromosome[0])):
            if chromosome[0][i] <= len(problem.customer_list):
                mp_cust_chro[chromosome[0][i]] = i
        """
        split drone routes into list of trips for each drone
        """

        # set of truck customers
        truck_custs = [cust for route in truck_routes for cust in route]
        depot = 0
        truck_custs.append(depot)

        # estimate timeline of truck schedule
        truck_schedule = [[0, 0] for _ in range(len(problem.customer_list) + 1)]
        for truck_idx, truck_route in enumerate(truck_routes):
            for cust_idx in range(len(truck_route)):
                cust = truck_route[cust_idx]
                if cust_idx == 0:
                    truck_schedule[cust] = (
                        max(
                            time_by_truck[0][cust],
                            problem.customer_list[cust].arrive_time,
                        ),
                        time_by_truck[0][cust]
                        + problem.customer_list[cust].service_time,
                    )
                else:
                    prev_cust = truck_route[cust_idx - 1]
                    truck_schedule[cust][0] = max(
                        truck_schedule[prev_cust][1] + time_by_truck[prev_cust][cust],
                        problem.customer_list[cust].arrive_time,
                    )
                    truck_schedule[cust][1] = (
                        truck_schedule[cust][0]
                        + problem.customer_list[cust].service_time
                    )

        truck_direction = []

        for truck_route in truck_routes:
            direction = [-1 for _ in range(len(problem.customer_list) + 1)]
            for idx in range(len(truck_route) - 1):
                direction[truck_route[idx]] = truck_route[idx + 1]
            truck_direction.append(direction)

        pairs = list(combinations(truck_custs, 2))
        pairs = pairs + [(cust, cust) for cust in truck_custs]

        def opt_pair_cust(trip):
            opt_lch_cust = None
            opt_ld_cust = None
            opt_lch_wait = None
            opt_ld_wait = None
            if (
                sum([problem.customer_list[cust].quantity for cust in trip])
                > problem.drone_capacity
            ):
                return opt_lch_cust, opt_ld_cust

            for pair in pairs:
                # determine which is launching customer and landing customer
                lch_cust = pair[0]
                ld_cust = pair[1]
                if (
                    problem.customer_list[lch_cust].arrive_time
                    > problem.customer_list[ld_cust].arrive_time
                ):
                    lch_cust, ld_cust = ld_cust, lch_cust

                trip = [lch_cust] + trip + [ld_cust]
                received = (
                    [0] + [problem.customer_list[cust].quantity for cust in trip] + [0]
                )

                lch_wait = 0
                ld_wait = 0

                arrive = [0 for _ in range(len(trip))]
                leave = [0 for _ in range(len(trip))]

                arrive[0] = truck_schedule[lch_cust][0]
                if (
                    truck_schedule[lch_cust][0]
                    <= problem.customer_list[trip[1]].arrive_time
                    - time_by_drone[lch_cust][trip[1]]
                    <= truck_schedule[lch_cust][1]
                ):
                    leave[0] = (
                        problem.customer_list[lch_cust].arrive_time
                        - time_by_drone[lch_cust][trip[1]]
                    )
                    lch_wait = 0
                elif (
                    problem.customer_list[trip[1]].arrive_time
                    - time_by_drone[lch_cust][trip[1]]
                    > truck_schedule[lch_cust][1]
                ):
                    leave[0] = (
                        problem.customer_list[lch_cust].arrive_time
                        - time_by_drone[lch_cust][trip[1]]
                    )
                    lch_wait = leave[0] - truck_schedule[lch_cust][1]
                else:
                    leave[0] = truck_schedule[lch_cust][0]
                    lch_wait = 0

                total_energy = 0
                total_goods = 0

                for i in range(len(trip) - 1):
                    u, u_next = trip[i], trip[i + 1]
                    total_energy = total_energy + problem.energy_consumption_rate * (
                        problem.weight_of_drone + total_goods
                    ) * (
                        problem.distance_matrix_drone[u][u_next]
                        / problem.speed_of_drone
                        + problem.launch_time
                    )
                    if received[i + 1] != 0:
                        arrive[i + 1] = max(
                            problem.customer_list[u_next].arrive_time,
                            leave[i] + time_by_drone[u][u_next],
                        )
                        wait_time = max(
                            problem.customer_list[u_next].arrive_time - arrive[i + 1], 0
                        )
                        leave[i + 1] = (
                            arrive[i + 1]
                            + problem.customer_list[u_next].service_time
                            + wait_time
                        )
                        total_goods = total_goods + received[i]
                        total_energy = (
                            total_energy
                            + problem.energy_consumption_rate
                            * (problem.weight_of_drone + total_goods)
                            * problem.customer_list[u_next].service_time
                        )
                    else:
                        arrive[i + 1] = max(
                            problem.customer_list[u_next].arrive_time,
                            leave[i] + time_by_drone[u][u_next],
                        )
                        wait_time = max(0, truck_schedule[u_next][1] - arrive[i + 1])
                        ld_wait = wait_time
                        total_energy = (
                            total_energy
                            + problem.energy_consumption_rate
                            * (problem.weight_of_drone + total_goods)
                            * wait_time
                        )
                if total_energy <= problem.drone_energy:
                    if (opt_lch_wait is None or opt_ld_wait is None) or (
                        lch_wait + ld_wait < opt_lch_wait + opt_ld_wait
                    ):
                        opt_lch_cust = lch_cust
                        opt_ld_cust = ld_cust
                        opt_lch_wait = lch_wait
                        opt_ld_wait = ld_wait

            return opt_lch_cust, opt_ld_cust

        # split drone routes into the list of trips for each drone
        drone_schedule = [
            [[0, 0] for _ in range(problem.number_of_drones)]
            for _ in range(len(problem.customer_list) + 1)
        ]
        drone_triplists = []
        violated = False
        for drone_idx, drone_route in enumerate(drone_routes):
            drone_route.sort(key=lambda cust: problem.customer_list[cust].arrive_time)
            triplist = []

            while drone_route:
                trip = []
                opt_lch_cust, opt_ld_cust = None, None

                while drone_route:
                    tmp_lch_cust, tmp_ld_cust = opt_pair_cust(trip + [drone_route[0]])
                    if tmp_lch_cust is None:
                        if opt_lch_cust is None:
                            chro_idx = mp_cust_chro[drone_route[0]]
                            chromosome[chro_idx][1] = 0
                            violated = True
                        break

                    opt_lch_cust, opt_ld_cust = tmp_lch_cust, tmp_ld_cust
                    trip.append(drone_route[0])
                    drone_route.pop(0)

                if violated:
                    break

                trip = [opt_lch_cust] + trip + [opt_ld_cust]
                triplist.append(trip)

            if violated:
                break
            drone_triplists.append(triplist)

        if not violated:
            return truck_routes, drone_triplists


"""
to decode complete solution, compute the schedule
"""


# rebuild truck routes by adding depot
def schedule(chromosome, truck_routes, drone_triplists, problem: Problem):
    # mapping customers to their indices in chromosome
    mp_cust_chro = [-1 for _ in range(len(problem.customer_list) + 1)]
    for i in range(len(chromosome[0])):
        if chromosome[0][i] <= len(problem.customer_list):
            mp_cust_chro[chromosome[0][i]] = i

    depart_depot = 0
    return_depot = len(problem.customer_list)
    truck_routes = [
        [depart_depot] + truck_route + [return_depot] for truck_route in truck_routes
    ]

    # rebuild drone trips by adjusting return depot annotation to 'return depot'
    for trips in drone_triplists:
        for i in range(len(trips)):
            if trips[i][-1] == 0 and len(trips[i]) > 0:
                trips[i][-1] = return_depot

    # compute matrix of travelling time between 2 specific customers of truck and drone
    time_by_truck = [
        [dist / problem.speed_of_truck for dist in row]
        for row in problem.distance_matrix_truck
    ]
    time_by_drone = [
        [
            (problem.launch_time + problem.land_time + dist) / problem.speed_of_drone
            for dist in row
        ]
        for row in problem.distance_matrix_drone
    ]

    # set of launching customers and landing customers
    ld_custs = [
        trip[-1]
        for trips in drone_triplists
        for trip in trips
        if trip[-1] != return_depot
    ]

    # current identifier of current truck and drone in the specified route
    truck_route_idx = [0 for _ in range(problem.number_of_trucks)]  # (route_idx)
    # update these lists for solution
    truck_arrival = [[0] * len(truck_route) for truck_route in truck_routes]
    truck_depart = deepcopy(truck_arrival)

    drone_arrival = [[[0] * len(trip) for trip in trips] for trips in drone_triplists]
    drone_depart = deepcopy(drone_arrival)

    # the arrival time from each customer
    assemble = [0 for _ in range(len(problem.customer_list) + 1)]

    # count of landing drones on each customer
    pickup_count = [0 for _ in range(len(problem.customer_list) + 1)]
    for trips in drone_triplists:
        for trip in trips:
            if trip[-1] != return_depot:
                pickup_count[trip[-1]] = pickup_count[trip[-1]] + 1

    # whether the customer has been departed
    departed = [False for _ in range(len(problem.customer_list) + 2)]
    # whether the customer has been arrived
    arrived = [False for _ in range(len(problem.customer_list) + 2)]
    arrived[0] = True

    # the iteration will be ended when all the trucks return to depot
    while all(
        [
            truck_route_idx[truck_id] < len(truck_route)
            for truck_id, truck_route in enumerate(truck_routes)
        ]
    ) and not all(
        [
            truck_route[truck_route_idx[truck_id]] == return_depot
            for truck_id, truck_route in enumerate(truck_routes)
        ]
    ):
        # let each truck reaches the nearest landing customer on its route
        for truck_id in range(problem.number_of_trucks):
            truck_route = truck_routes[truck_id]  # route of current truck
            route_idx = truck_route_idx[
                truck_id
            ]  # current index in the current truck route
            # terminated when the current index is the last index of the current truck route
            while route_idx < len(truck_route) - 1:
                # current customer and next customer in the current truck route
                cur_cust = truck_route[route_idx]
                next_cust = truck_route[route_idx + 1]
                # truck arrival time of the next customer based on the departture time of the current customer
                truck_arrival[truck_id][route_idx + 1] = (
                    truck_depart[truck_id][
                        route_idx
                    ]  # maybe departure time from 'depot' must be initially calculated
                    + time_by_truck[cur_cust][next_cust % return_depot]
                )

                # update the assembling time of all vehicle(s) at the next customer
                assemble[next_cust] = truck_arrival[truck_id][route_idx + 1]

                arrived[next_cust] = True

                # terminated when the next customer is a landing customer or return depot
                # can not calculate the departure time of the next customer without arrival time of landing drones
                if next_cust in ld_custs or next_cust == return_depot:
                    break

                # truck departure time of the next customer based on its arrival time and service time
                truck_depart[truck_id][route_idx + 1] = (
                    max(
                        truck_arrival[truck_id][route_idx + 1],
                        problem.customer_list[next_cust].arrive_time,
                    )
                    + problem.customer_list[next_cust].service_time
                )

                departed[next_cust] = True
                route_idx = route_idx + 1

            # remain the current departure-unscpecified customer index
            # could be return depot or a landing customer
            truck_route_idx[truck_id] = (
                route_idx + 1 if route_idx < len(truck_route) - 1 else route_idx
            )

        # let drones move that depart from arrived customers to arrived customer but departed yet
        for drone_id in range(problem.number_of_drones):
            trips = drone_triplists[drone_id]

            for trip_idx in range(len(trips)):
                cur_trip = trips[trip_idx]
                # condition to let the drone trip depart
                if arrived[cur_trip[0]] and (
                    (not departed[cur_trip[-1]] and arrived[cur_trip[-1]])
                    or cur_trip[-1] == return_depot
                ):
                    for i in range(len(cur_trip)):
                        if i == 0:
                            drone_arrival[drone_id][trip_idx][i] = assemble[cur_trip[i]]
                            drone_depart[drone_id][trip_idx][i] = drone_arrival[
                                drone_id
                            ][trip_idx][i]
                        else:
                            # drone arrival time of the current customer based on the departure time of the previous customer
                            drone_arrival[drone_id][trip_idx][i] = (
                                drone_depart[drone_id][trip_idx][i - 1]
                                + time_by_drone[cur_trip[i - 1]][cur_trip[i]]
                            )
                            arrived[cur_trip[i]] = True

                            if i == len(cur_trip) - 1:
                                break

                            # drone departure time of the current customer based on max(its arrival time, customer's arrival time) and service time
                            drone_depart[drone_id][trip_idx][i] = (
                                max(
                                    drone_arrival[drone_id][trip_idx][i],
                                    problem.customer_list[cur_trip[i]].arrive_time,
                                )
                                + problem.customer_list[cur_trip[i]].service_time
                            )
                            departed[cur_trip[i]] = True
                    if not problem.check_energy_drone(
                        Drone_Trip(
                            cur_trip,
                            [problem.customer_list[cust].quantity for cust in cur_trip],
                            drone_arrival[drone_id][trip_idx],
                            drone_depart[drone_id][trip_idx],
                        )
                    ):
                        for cust in cur_trip:
                            chromosome[1][mp_cust_chro[cust]] = 0
                        return None, None, None, None, None, None
                    # reduce the number of drones assembled at the landing customer by 1
                    pickup_count[cur_trip[-1]] = pickup_count[cur_trip[-1]] - 1
                    # update the assembling time of the landing customer

                    assemble[cur_trip[-1]] = max(
                        assemble[cur_trip[-1]], drone_arrival[drone_id][trip_idx][-1]
                    )
        # specify the departure time of trucks at their current landing customers when all drones landing on this customer have arrived
        for truck_id in range(problem.number_of_trucks):
            truck_route = truck_routes[truck_id]
            cur_cust = truck_route[truck_route_idx[truck_id]]
            if pickup_count[cur_cust] == 0 and cur_cust != return_depot:
                truck_depart[truck_id][truck_route_idx[truck_id]] = max(
                    assemble[cur_cust],
                    problem.customer_list[cur_cust].arrive_time
                    + truck_arrival[truck_id][truck_route_idx[truck_id]],
                )
                truck_route_idx[truck_id] = truck_route_idx[truck_id] + 1
                departed[cur_cust] = True

    return (
        truck_routes,
        drone_triplists,
        truck_arrival,
        truck_depart,
        drone_arrival,
        drone_depart,
    )


def build_solution(
    truck_routes,
    drone_triplists,
    truck_arrival,
    truck_depart,
    drone_arrival,
    drone_depart,
    problem,
):
    return_depot = len(problem.customer_list)
    ld_custs = [
        trip[-1]
        for trips in drone_triplists
        for trip in trips
        if trip[-1] != return_depot
    ]

    # build the solution in required format
    truck_sols = []
    for truck_id in range(problem.number_of_trucks):
        assigned_customers = truck_routes[truck_id][1:-1]
        recived_truck = [
            problem.customer_list[cust % return_depot].quantity
            for cust in assigned_customers
        ]
        recived_drone = []
        for cust in assigned_customers:
            if cust in ld_custs:
                recived_drone.append(problem.customer_list[cust].quantity)
            else:
                recived_drone.append(0)

        arrive_time = truck_arrival[truck_id][1:-1]
        depart_time = truck_depart[truck_id][1:-1]
        truck_sols.append(
            Truck_Solution(
                assigned_customers,
                recived_truck,
                recived_drone,
                arrive_time,
                depart_time,
            )
        )

    drone_sols = []
    for drone_id in range(problem.number_of_drones):
        trips = drone_triplists[drone_id]
        drone_sol = []
        for trip_idx in range(len(trips)):
            cur_trip = trips[trip_idx]
            assigned_customers = deepcopy(cur_trip)
            if len(assigned_customers) == 0:
                continue
            recived_drone = [0 for _ in range(len(assigned_customers))]
            recived_drone[1:-1] = [
                problem.customer_list[cust].quantity
                for cust in assigned_customers[1:-1]
            ]
            arrive_time = deepcopy(drone_arrival[drone_id][trip_idx])
            depart_time = deepcopy(drone_depart[drone_id][trip_idx])
            drone_trip = Drone_Trip(
                assigned_customers, recived_drone, arrive_time, depart_time
            )
            drone_sol.append(drone_trip)
        drone_sols.append(drone_sol)

    return truck_sols, drone_sols


# the individual can be decoded only when it is feasible
def decode(individual: Individual, problem: Problem):
    chromosome = individual.chromosome

    while True:
        if chromosome is None:
            return None
        truck_routes, drone_triplists = relaxed_repair(chromosome, problem)

        # debug: view truck routes and drone trips after a relaxed version of repair
        print("Truck route")
        for truck_id, truck_route in enumerate(truck_routes):
            print(truck_id, ":", truck_route)

        print("Drone trips")
        for drone_id, trip_list in enumerate(drone_triplists):
            print(drone_id, ":", trip_list)
        print()

        (
            truck_routes,
            drone_triplists,
            truck_arrival,
            truck_depart,
            drone_arrival,
            drone_depart,
        ) = schedule(chromosome, truck_routes, drone_triplists, problem)

        if truck_routes:
            if not drone_triplists:
                truck_routes, drone_triplists = relaxed_repair(chromosome, problem)

            (
                truck_routes,
                drone_triplists,
                truck_arrival,
                truck_depart,
                drone_arrival,
                drone_depart,
            ) = schedule(chromosome, truck_routes, drone_triplists, problem)

            return build_solution(
                truck_routes,
                drone_triplists,
                truck_arrival,
                truck_depart,
                drone_arrival,
                drone_depart,
                problem,
            )
