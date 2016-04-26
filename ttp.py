#! /usr/bin/env python3

from file_parser import fileParser
from random import randint, sample, choice
from jb_int import *
from sea_int_2016 import *
from time import strftime

def main(filename, filesave, probMutation, probCrossover, numRuns, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations):
	numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems = fileParser(filename)
	
	with open(filesave, 'a+') as f_out:
		f_out.write(strftime("%c") + '\n')
		for i in range(numRuns):
			best = run(probMutation, probCrossover, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations, numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems)			
			f_out.write(str(best) + '\n')
		f_out.write('\n')

def run(probMutation, probCrossover, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations, numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems):
	# item list in which position is item_i and the value is the city where it was picked
	itemsPop = initializationItems(numItems, numCities, popSize)
	citiesPop = initializationCities(numCities, popSize)

	# evaluate pop here
	fitnessList = [0 for i in range(popSize)]
	itemsPop = [(itemsPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]
	citiesPop = [(citiesPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]

	for i in range(generations):
		matePoolItems = tour_selection(itemsPop)
		matePoolCities = tour_selection(citiesPop)

		progenitoresItems = []
		progenitoresCities = []
		for j in range(0, popSize - 1, 2):
			indivItem1 = matePoolItems[j]
			indivItem2 = matePoolItems[j + 1]
			sonsItems = crossoverOperator(indivItem1, indivItem2, probCrossover)

			indivCities1 = matePoolCities[j]
			indivCities2 = matePoolCities[j + 1]
			sonsCities = crossoverOperator(indivCities1, indivCities2, probCrossover)

		descendentesItems = []
		for cromo, fit in progenitoresItems:
			mutation = choice(mutationOperators)
			newCromo = mutation(cromo, numItems)
			descendentesItems.append((newCromo, 0)) # ALTERAR 0 POR FITNESS FUNCTION

		descendentesCities = []
		for cromo, fit in progenitoresCities:
			mutation = choice(mutationOperators)
			newCromo = mutation(cromo, numCities)
			descendentesCities.append((newCromo, 0)) # ALTERAR 0 POR FITNESS FUNCTION

		itemsPop = selection_survivors_elite(itemsPop, descendentesItems)
		citiesPop = selection_survivors_elite(citiesPop, descendentesCities)

		# evaluate the new population
		fitnessList = [0 for i in range(popSize)]
		itemsPop = [(itemsPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]
		citiesPop = [(citiesPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]

	best_pops = [best_pop(itemsPop), best_pop(citiesPop)]
	return best_pops
	
def initializationItems(numItems, numCities, popSize):
	return [([randint(1, numCities) for i in range(numItems)], 0) for i in range(popSize)]

def initializationCities(numCities, popSize):	
	return [(sample(list(range(1, numCities + 1)), numCities), 0) for i in range(popSize)]


if __name__ == '__main__':
	probMutation = 0.1
	probCrossover = 0.9
	numRuns = 30
	popSize = 10
	elitePercent = 1
	tourSize = 3
	generations = 20
	mutationOperators = [mutation(1, 0.1)]
	crossoverOperator = sample_cross
	fitnessFunction = fitness
	main('Tests/10/10_3_1_25.txt', 'Results/10/10_3_1_25_result.txt', probMutation, probCrossover, numRuns, popSize, tour_sel(tourSize), crossoverOperator, mutationOperators, sel_survivors_elite(elitePercent), fitnessFunction, generations)
