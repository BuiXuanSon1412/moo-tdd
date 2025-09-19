from data import load_data
from decode import decode
from population import Individual

if __name__ == "__main__":
    problem = load_data(r"data/100customers/c101.txt", 8, 2, 3)

    #  0   1  2  3  4  5  6  7   8  9 10
    chromosome = [
        [1, 10, 3, 7, 4, 9, 5, 6, 11, 8, 2],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    ]

    truck_sols, drone_sols = decode(Individual(chromosome=chromosome), problem)
