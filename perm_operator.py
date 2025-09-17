import random
from population import Individual
def pmx_crossover(parent1, parent2):
    # Extract layers
    p1_layer1, p1_layer2 = parent1.chromosome[0], parent1.chromosome[1]
    p2_layer1, p2_layer2 = parent2.chromosome[0], parent2.chromosome[1]

    size = len(p1_layer1)
    # choose two crossover points
    cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

    def pmx_one_layer(l1, l2):
        offspring = [None]*size
        # copy the segment
        offspring[cx_point1:cx_point2] = l1[cx_point1:cx_point2]
        # mapping for duplicates
        for i in range(cx_point1, cx_point2):
            if l2[i] not in offspring:
                pos = i
                val = l2[i]
                while offspring[pos] is not None:
                    pos = l2.index(l1[pos])
                offspring[pos] = val
        # fill remaining with l2
        for i in range(size):
            if offspring[i] is None:
                offspring[i] = l2[i]
        return offspring

    child1_layer1 = pmx_one_layer(p1_layer1, p2_layer1)
    child2_layer1 = pmx_one_layer(p2_layer1, p1_layer1)

    # second layer: simple one-point crossover for flags
    cut = random.randint(1, size-1)
    child1_layer2 = p1_layer2[:cut] + p2_layer2[cut:]
    child2_layer2 = p2_layer2[:cut] + p1_layer2[cut:]

    return (Individual([child1_layer1, child1_layer2]),
            Individual([child2_layer1, child2_layer2]))

def ox_crossover(parent1, parent2):
    p1_layer1, p1_layer2 = parent1.chromosome[0], parent1.chromosome[1] 
    p2_layer1, p2_layer2 = parent2.chromosome[0], parent2.chromosome[1]

    size = len(p1_layer1)
    cx_point1, cx_point2 = sorted(random.sample(range(size), 2))

    def ox_one_layer(l1, l2):
        offspring = [None]*size
        offspring[cx_point1:cx_point2] = l1[cx_point1:cx_point2]
        fill_values = [x for x in l2 if x not in offspring]
        pos = cx_point2
        for val in fill_values:
            if pos >= size:
                pos = 0
            while offspring[pos] is not None:
                pos += 1
                if pos >= size:
                    pos = 0
            offspring[pos] = val
        return offspring

    child1_layer1 = ox_one_layer(p1_layer1, p2_layer1)
    child2_layer1 = ox_one_layer(p2_layer1, p1_layer1)

    # second layer: simple one-point crossover
    cut = random.randint(1, size-1)
    child1_layer2 = p1_layer2[:cut] + p2_layer2[cut:]
    child2_layer2 = p2_layer2[:cut] + p1_layer2[cut:]

    return (Individual([child1_layer1, child1_layer2]),
            Individual([child2_layer1, child2_layer2]))

def cx_crossover(parent1, parent2):
    p1_layer1, p1_layer2 = parent1.chromosome[0], parent1.chromosome[1]
    p2_layer1, p2_layer2 = parent2.chromosome[0], parent2.chromosome[1]    

    size = len(p1_layer1)

    def cx_one_layer(l1, l2):
        offspring = [None]*size
        visited = [False]*size
        index = 0
        while not all(visited):
            if visited[index]:
                index = visited.index(False)
            start = index
            while not visited[index]:
                offspring[index] = l1[index]
                visited[index] = True
                index = l1.index(l2[index])
            index = visited.index(False) if not all(visited) else 0
            # swap cycle to second parent
            for i in range(size):
                if offspring[i] is None:
                    offspring[i] = l2[i]
        return offspring

    child1_layer1 = cx_one_layer(p1_layer1, p2_layer1)
    child2_layer1 = cx_one_layer(p2_layer1, p1_layer1)

    # second layer: simple one-point crossover
    cut = random.randint(1, size-1)
    child1_layer2 = p1_layer2[:cut] + p2_layer2[cut:]
    child2_layer2 = p2_layer2[:cut] + p1_layer2[cut:]

    return (Individual([child1_layer1, child1_layer2]),
            Individual([child2_layer1, child2_layer2]))
