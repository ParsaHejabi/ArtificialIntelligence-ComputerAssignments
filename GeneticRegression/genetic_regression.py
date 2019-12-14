import numpy
import matplotlib.pyplot
import random
import math
import tqdm

xTrain = numpy.genfromtxt('x_train.csv', delimiter=',')
yTrain = numpy.genfromtxt('y_train.csv', delimiter=',')
coefficient_lower_bound = -50
coefficient_upper_bound = 50
mutation_lower_bound = -5
mutation_upper_bound = -5
individual_size = 3
population_size = 1000
selection_size = math.floor(0.4 * population_size)
probability_of_gene_mutating = 0.5
probability_of_individual_mutating = 0.1
generation_count = 0
max_generation_count = 50


def check_termination_condition(best_individual):
    # if error of best_individual is lower than 1% OR generation_count == max_generation
    if (generation_count == max_generation_count) or (best_individual['fitness'] < 10000):
        return True
    else:
        return False


def create_initial_individual():
    return [random.uniform(coefficient_lower_bound, coefficient_upper_bound) for _ in range(individual_size)]


def create_initial_population():
    return [create_initial_individual() for _ in range(population_size)]


def calculate_fitness(individual):
    return {'individual': individual,
            'fitness': numpy.array(
                [abs(((i ** 2) * individual[0] + i * individual[1] + individual[2]) - j) for i, j in
                 zip(xTrain, yTrain)]).sum()
            }


def selection(population):
    population_with_fitness = [calculate_fitness(individual) for individual in tqdm.tqdm(population)]
    selected_population = sorted(population_with_fitness, key=lambda i: i['fitness'])[: selection_size]
    return selected_population


def crossover(individual_1, individual_2):
    child = {}
    possible_indexes = [i for i in range(individual_size)]
    index_1 = random.sample(possible_indexes, math.floor(0.5 * individual_size))
    index_2 = [i for i in possible_indexes if i not in index_1]
    chromosome_1 = [[i, individual_1[i]] for i in index_1]
    chromosome_2 = [[i, (individual_2[i] + individual_1[i]) / 2] for i in index_2]
    child.update({key: value for (key, value) in chromosome_1})
    child.update({key: value for (key, value) in chromosome_2})
    return [child[i] for i in possible_indexes]


def mutation(individual):
    possible_indexes = [i for i in range(individual_size)]
    number_of_genes_mutated = math.floor(probability_of_gene_mutating * individual_size)
    indexes_to_mutate = random.sample(possible_indexes, number_of_genes_mutated)
    for i in indexes_to_mutate:
        gene_transform = random.choice([-1, 1])
        change = gene_transform * random.uniform(mutation_lower_bound, mutation_upper_bound)
        if individual[i] + change <= coefficient_lower_bound:
            individual[i] = coefficient_lower_bound
        else:
            if individual[i] + change >= coefficient_upper_bound:
                individual[i] = coefficient_upper_bound
            else:
                individual[i] = individual[i] + change
    return individual


def make_new_generation(selected_individuals):
    parent_pairs = [random.sample(selected_individuals, 2) for _ in range(population_size - selection_size)]
    offspring = [crossover(parent[0]['individual'], parent[1]['individual']) for parent in parent_pairs]
    selected_individuals_without_fitness = [individual['individual'] for individual in selected_individuals]
    new_generation = offspring + selected_individuals_without_fitness
    possible_indexes = [i for i in range(population_size)]
    individual_to_mutate = random.sample(possible_indexes,
                                         math.floor(probability_of_individual_mutating * population_size))
    individual_mutation = [[i, mutation(new_generation[i])] for i in individual_to_mutate]
    for mutated_offspring in individual_mutation:
        new_generation[mutated_offspring[0]] = mutated_offspring[1]
    return new_generation


""" Test for calculate_fitness """
# initial_individual = create_initial_individual()
# print(initial_individual)
# print(calculate_fitness(initial_individual))

""" Test for selection """
# initial_population = create_initial_population()
# print(initial_population)
# selection(initial_population)

""" Test for crossover """
# individua_1 = create_initial_individual()
# individua_2 = create_initial_individual()
# print(individua_1, individua_2)
# print(crossover(individua_1, individua_2))

""" Test for mutation """
# initial_individual = create_initial_individual()
# print(initial_individual)
# print(mutation(initial_individual))

initial_population = create_initial_population()
new_population = initial_population
initial_population_with_fitness = [calculate_fitness(individual) for individual in initial_population]
sorted_initial_population = sorted(initial_population_with_fitness, key=lambda i: i['fitness'])
should_terminate = check_termination_condition(sorted_initial_population[0])
while should_terminate is False:
    generation_count += 1
    new_population = make_new_generation(selection(new_population))
    new_population_with_fitness = [calculate_fitness(individual) for individual in new_population]
    sorted_new_population = sorted(new_population_with_fitness, key=lambda i: i['fitness'])
    best_new_individual = sorted_new_population[0]
    new_yTrain = numpy.array(
        [((i ** 2) * best_new_individual['individual'][0] + i * best_new_individual['individual'][1] +
          best_new_individual['individual'][2]) for i in
         xTrain])
    print('Generation: ', generation_count)
    print('Best individual:', best_new_individual)
    print('Average fitness: ', numpy.array(
        [[individual['fitness']] for individual in new_population_with_fitness]).sum() / population_size)
    matplotlib.pyplot.scatter(xTrain, new_yTrain)
    matplotlib.pyplot.show()
    should_terminate = check_termination_condition(best_new_individual)
