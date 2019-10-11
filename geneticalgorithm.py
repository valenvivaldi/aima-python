import random

from deap import base
from deap import creator
from deap import tools

n=8
populationsize =100

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, n-1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def heuristic2(individual):
    max = len(individual)

    result = 0
    i = 0

    while (i < max - 1):
        # print("me paro en {}".format(i))
        j = i + 1
        while (j < max):
            #    print("miro {}".format(j))
            if (individual[j] == individual[i]):
                result -= 1
            a = (individual[j] - individual[i]) / (j - i)
            #   print(" pendiente {}".format(a))
            if (a == -1 or a == 1):
                result -= 1

            j += 1
        i += 1
    return result


def evaluateNQueen(individual):
    return heuristic2(individual),


# region Description
toolbox.register("evaluate", evaluateNQueen)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt,low=0,up=7, indpb=0.3)
toolbox.register("select", tools.selRoulette, k=populationsize//4)

# print(evaluateNQueen([2,4,6,8,3,1,7,5]))

# creating population

population = toolbox.population(n=populationsize)

# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit
# CXPB  is the probability with which two individuals
#       are crossed
#
# MUTPB is the probability for mutating an individual
CXPB, MUTPB = 0.5, 0.2

# Extracting all the fitnesses of
fits = [ind.fitness.values[0] for ind in population]

# Variable keeping track of the number of generations
g = 0

# Begin the evolution

while max(fits) < 0 and g < 100000:
   # print("poblacion inicial: {}".format(population))
    # A new generation
    g = g + 1
    if (g % 1000 == 0):
        print("-- Generation %i --" % g)
    # Select the next generation individuals
    offspring = toolbox.select(population)
    #print("SELECIONO!             {}".format(len(offspring)))
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))
    # Apply crossover and mutation on the offspring

    # Next, we will perform both the crossover (mating) and the mutation of the produced children
    # with a certain probability of CXPB and MUTPB.

    # The del statement will invalidate the fitness of the modified offspring.
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    # And last but not least, we replace the old population by the offspring.

    population.extend(offspring) #agregamosssssssss los nuevos descendientes a  la poblacion
    population.sort(key = lambda x:x.fitness.values[0],reverse=True) #se vuelve a ordenar la poblacion
    population = population[0:populationsize]
  #  print("el mejor hasta ahora es {} de la poblacion de {} ".format(population[0:5],len(population)))

    # Gather all the fitnesses in one list and print the stats
    if (g % 1000 == 0):
        fits = [ind.fitness.values[0] for ind in population]

        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

maxvalue = -100
for ind in population:
    if ind.fitness.values[0] > maxvalue:
        best=ind
        maxvalue = ind.fitness.values[0]

print("una solucion es {} con  {}".format(best, heuristic2(best)))
# endregion
