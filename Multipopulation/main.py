#! /usr/bin/env python3

from file_parser import file_parser
from random import sample
import numpy as np


def solutions_exchanged(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit):
	# last position of indiv is the fitness profit
	# previous last position of indiv is the fitness weight
	for i in range(num_runs):
		population = initialization_indiv(pop_size, number_objects)

		for i in range(len(population)):
			population[i] = fitness(population[i], knapsack_capacity, number_objects, objects_weight, objects_profit)

		for i in range(generations):
			mate_pool = tour_selection(tour_size, population, number_objects)

			offspring = []
			for j in range(0, pop_size - 1):
				indiv1 = mate_pool[j]
				indiv2 = mate_pool[j + 1]
				sons = crossover(indiv1, indiv2, prob_crossover)
				offspring.extend(sons)
			offspring = np.array(offspring)

			for j in range(len(offspring)):
				offspring[j] = mutation(offspring[j], prob_mutation)
				offspring[j] = fitness(offspring[j], knapsack_capacity, number_objects, objects_weight, objects_profit)				

			population = sel_survivors_elite(elite_percent, population, offspring)

		for i in range(len(population)):
			population[i] = fitness(population[i], knapsack_capacity, number_objects, objects_weight, objects_profit)

		print(best_individual(population))


def random_individuals(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit):
	pass

def initialization_indiv(pop_size, number_objects):
	population = np.random.randint(2, size = (pop_size, number_objects + 2), dtype = np.int)
	population[:, -1] = population[:, -2] = 0
	return population

def mutation(indiv, prob_mutation):
	for i in range(len(indiv) - 2):
		if np.random.random() < prob_mutation:
			indiv[i] ^= 1

	indiv[-1] = indiv[-2] = 0
	return indiv

def crossover(indiv1, indiv2, prob_crossover):
	if np.random.random() < prob_crossover:
		cut_index = np.random.randint(1, len(indiv1) - 2)
		newIndiv1 = np.append(indiv1[:cut_index], indiv2[cut_index:], axis = 0)
		newIndiv2 = np.append(indiv2[:cut_index], indiv1[cut_index:], axis = 0)
		newIndiv1[-1] = newIndiv1[-2] = 0
		newIndiv2[-1] = newIndiv2[-2] = 0
		return newIndiv1, newIndiv2
	return indiv1, indiv2

def tour_selection(tour_size, population, number_objects):
	size_pop = len(population)
	mate_pool = np.empty((size_pop, number_objects + 2), dtype = np.int)

	for i in range(size_pop):
		mate_pool[i] = one_tour(tour_size, population)

	return mate_pool

def one_tour(tour_size, population):
    pool = sample(list(population), tour_size)
    pool = np.array(pool)
    pool = pool[pool[:, 1].argsort()[::-1]]
    return pool[0]

def sel_survivors_elite(elite_percent, parents, offspring):
	size_parents = len(parents)
	comp_elite = int(size_parents * elite_percent)
	parents = parents[parents[:, 1].argsort()[::-1]]
	offspring = offspring[offspring[:, 1].argsort()[::-1]]
	new_population = np.append(parents[:comp_elite], offspring[:size_parents - comp_elite], axis = 0)
	return new_population

def fitness(indiv, knapsack_capacity, number_objects, objects_weight, objects_profit):
	fitness_weight = 0
	fitness_profit = 0

	for i in range(number_objects):
		fitness_weight += indiv[i] * objects_weight[i]
		fitness_profit += indiv[i] * objects_profit[i]

	if fitness_weight > knapsack_capacity:
		indiv[-1] = indiv[-2] = 0
	else:
		indiv[-1] = fitness_profit
		indiv[-2] = fitness_weight

	return indiv

def best_individual(population):
	population = population[population[:, 1].argsort()[::-1]]
	return population[0]

def change_individuals():
	pass

def introduce_random_indiv():
	pass


if __name__ == '__main__':
	prob_mutation = 0.01
	prob_crossover = 0.9
	num_runs = 30
	pop_size = 200
	elite_percent = 0.05
	tour_size = int(pop_size * 0.01)
	generations = 100

	file_number = 6
	knapsack_capacity, number_objects, objects_weight, objects_profit = file_parser(file_number)

	solutions_exchanged(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit)
	#random_individuals(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit)
