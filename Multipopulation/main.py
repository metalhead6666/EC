#! /usr/bin/env python3

from file_parser import file_parser
from statistical_analysis import statistical_analysis
from create_csv import create_csv
from math import ceil
from random import sample
import numpy as np


def run(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit, change_solutions, percentage_change, type_algorithm):
	# last position of indiv is the fitness profit
	# previous last position of indiv is the fitness weight
	size = int(pop_size * percentage_change)
	best_runs = np.zeros(num_runs, dtype = np.int)

	for i in range(num_runs):
		population = initialization_indiv(pop_size, number_objects)
		population2 = initialization_indiv(pop_size, number_objects)

		for k in range(len(population)):
			population[k][-1], population[k][-2] = fitness(population[k], knapsack_capacity, number_objects, objects_weight, objects_profit)
			population2[k][-1], population2[k][-2] = fitness(population2[k], knapsack_capacity, number_objects, objects_weight, objects_profit)

		for k in range(generations):
			mate_pool = tour_selection(tour_size, population, number_objects)
			mate_pool2 = tour_selection(tour_size, population2, number_objects)

			offspring = []
			offspring2 = []
			for j in range(0, pop_size - 1):
				indiv1 = mate_pool[j]
				indiv2 = mate_pool[j + 1]
				sons = crossover(indiv1, indiv2, prob_crossover)
				offspring.extend(sons)

				indiv1 = mate_pool2[j]
				indiv2 = mate_pool2[j + 1]
				sons = crossover2(indiv1, indiv2, prob_crossover)
				offspring2.extend(sons)				
			offspring = np.array(offspring)
			offspring2 = np.array(offspring2)

			for j in range(len(offspring)):
				offspring[j] = mutation(offspring[j], prob_mutation)
				offspring[j][-1], offspring[j][-2] = fitness(offspring[j], knapsack_capacity, number_objects, objects_weight, objects_profit)

				offspring2[j] = mutation2(offspring2[j], prob_mutation)
				offspring2[j][-1], offspring2[j][-2] = fitness(offspring2[j], knapsack_capacity, number_objects, objects_weight, objects_profit)	

			population = sel_survivors_elite(elite_percent, population, offspring)
			population2 = sel_survivors_elite(elite_percent, population2, offspring2)

			if np.random.random() < change_solutions:
				if type_algorithm:
					exchange_solutions(population, population2, size)
				else:
					random_individuals(population, population2, size, number_objects)

		for k in range(len(population)):
			population[k][-1], population[k][-2] = fitness(population[k], knapsack_capacity, number_objects, objects_weight, objects_profit)
			population2[k][-1], population2[k][-2] = fitness(population2[k], knapsack_capacity, number_objects, objects_weight, objects_profit)

		indiv = best_individual(population, population2)
		best_runs[i] = indiv[-1]

	return best_runs

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

def mutation2(indiv, prob_mutation):
	if np.random.random() < prob_mutation:
		index = sample(range(len(indiv) - 2), 2)
		index1, index2 = index
		temp = indiv[index1]
		indiv[index1] = indiv[index2]
		indiv[index2] = temp
		indiv[-1] = indiv[-2] = 0	
	return indiv

def crossover2(indiv1, indiv2, prob_crossover):
	if np.random.random() < prob_crossover:
		cut_index = sample(range(len(indiv1) - 2), 2)
		cut_index.sort()
		cut_index1, cut_index2 = cut_index
		newIndiv1 = np.concatenate((indiv1[:cut_index1], indiv2[cut_index1:cut_index2], indiv1[cut_index2:]), axis = 0)
		newIndiv2 = np.concatenate((indiv2[:cut_index1], indiv1[cut_index1:cut_index2], indiv2[cut_index2:]), axis = 0)
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
    pool = pool[pool[:, -1].argsort()[::-1]]
    return pool[0]

def sel_survivors_elite(elite_percent, parents, offspring):
	size_parents = len(parents)
	comp_elite = int(size_parents * elite_percent)
	parents = parents[parents[:, -1].argsort()[::-1]]
	offspring = offspring[offspring[:, -1].argsort()[::-1]]
	new_population = np.append(parents[:comp_elite], offspring[:size_parents - comp_elite], axis = 0)
	return new_population

def fitness(indiv, knapsack_capacity, number_objects, objects_weight, objects_profit):
	fitness_weight = 0
	fitness_profit = 0

	for i in range(number_objects):
		fitness_weight += indiv[i] * objects_weight[i]
		fitness_profit += indiv[i] * objects_profit[i]

	if fitness_weight > knapsack_capacity:
		return 0, 0

	return fitness_profit, fitness_weight

def best_individual(population, population2):
	population = population[population[:, -1].argsort()[::-1]]
	population2 = population2[population2[:, -1].argsort()[::-1]]

	if population[0][-1] > population2[0][-1]:
		return population[0]

	return population2[0]

def exchange_solutions(population, population2, size):	
	temp = population[:size]
	population[:size] = population2[:size]
	population2[:size] = temp
	return population, population2

def random_individuals(population, population2, size, number_objects):
	population = population[population[:, -1].argsort()]
	population2 = population2[population2[:, -1].argsort()]
	
	population[:size] = initialization_indiv(size, number_objects)
	population2[:size] = initialization_indiv(size, number_objects)
	return population, population2


if __name__ == '__main__':
	prob_mutation = 0.1
	prob_crossover = 0.9
	num_runs = 30
	pop_size = 50
	elite_percent = 0.05
	tour_size = ceil(pop_size * 0.01)
	generations = 10
	change_solutions = [0.1, 0.25, 0.5, 0.75]
	percentage_change = [0.1, 0.25, 0.5, 0.75]

	file_number = [7, 8]
	folderstat = "Results/"

	for number_file in file_number:
		for solutions_change in change_solutions:
			for change_percentage in percentage_change:
				knapsack_capacity, number_objects, objects_weight, objects_profit = file_parser(number_file)

				bests1 = run(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit, solutions_change, change_percentage, True)
				bests2 = run(prob_mutation, prob_crossover, num_runs, pop_size, elite_percent, tour_size, generations, knapsack_capacity, number_objects, objects_weight, objects_profit, solutions_change, change_percentage, False)
								
				filestat = str(number_file) + "_" + str(solutions_change) + "_" + str(change_percentage) + ".csv"
				create_csv(bests1, bests2, folderstat + filestat)
				statistical_analysis(folderstat, filestat, False)
				print("Done: " + filestat)
