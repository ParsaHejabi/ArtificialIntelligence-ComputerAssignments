import numpy
import matplotlib.pyplot
import random

xTrain = numpy.genfromtxt('x_train.csv', delimiter=',')
yTrain = numpy.genfromtxt('y_train.csv', delimiter=',')
coefficient_lower_bound = -50
coefficient_upper_bound = 50
individual_size = 3
population_size = 1000


# matplotlib.pyplot.scatter(xTrain, yTrain)
# matplotlib.pyplot.show()


def check_termination_condition(best_individual):
    # if error of best_individual is lower than 1% OR generation_count == max_generation

    return True


def create_initial_individual():
    return [random.uniform(coefficient_lower_bound, coefficient_upper_bound) for _ in range(individual_size)]


def create_initial_population():
    return [create_initial_individual() for _ in range(population_size)]


def calculate_fitness(individual):
    return numpy.array(
        [abs(((i ** 2) * individual[0] + i * individual[1] + individual[2]) - j) for i, j in zip(xTrain, yTrain)]).sum()


initial_individual = create_initial_individual()
print(initial_individual)
print(calculate_fitness(initial_individual))
