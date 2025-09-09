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
        customer_list,
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
    pass


# the individual can be decoded only when it is feasible
def decode(individual: Individual, problem: Problem):
    chromosome = individual.chromosome
    truck_routes, drone_routes = extract_routes(chromosome, problem)

    truck_custs = [cust for route in truck_routes for cust in route]
    depot = 0
    truck_custs.append(depot)
    # split sequence of drone customers into trips
    # and determine launching node and landing node
    drone_trips = [[]]

    for drone_id, drone_route in enumerate(drone_routes):
        trip = []
        for drone_cust in drone_route:
            if not trip:
                lch_cust = min(
                    truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[truck_cust][
                        drone_cust
                    ],
                )

                rem_truck_custs = [cust for cust in truck_custs if cust != lch_cust]
                pred_ld_cust = min(
                    rem_truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[drone_cust][
                        truck_cust
                    ],
                )

                if problem.check_drone_capacity(
                    [drone_cust]
                ) and problem.check_drone_energy_constraint(
                    [lch_cust, drone_cust, pred_ld_cust]
                ):
                    trip.append(lch_cust)
                    trip.append(drone_cust)

            else:
                pred_ld_cust = min(
                    truck_custs,
                    key=lambda truck_cust: problem.distance_matrix_drone[drone_cust][
                        truck_cust
                    ],
                )
                if problem.check_drone_capacity(
                    trip[1:] + [drone_cust]
                ) and problem.check_drone_energy_constraint(
                    trip + [drone_cust, pred_ld_cust]
                ):
                    trip.append(drone_cust)
                else:
                    rem_truck_custs = [cust for cust in truck_custs if cust != trip[0]]
                    ld_cust = min(
                        rem_truck_custs,
                        key=lambda truck_cust: problem.distance_matrix_drone[trip[-1]][
                            truck_cust
                        ],
                    )

                    trip.append(ld_cust)
                    drone_trips[drone_id].append(trip)
                    trip.clear()

    return truck_routes, drone_trips
