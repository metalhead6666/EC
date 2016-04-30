#! /usr/bin/env python3

from file_parser import fileParser
from random import randint, sample, choice, random
from jb_int import *
from sea_int_2016 import *
from time import strftime
from fitness import fitness
from CycleCross import cycle_cross
from mutation import mutationItem
import numpy as np
import matplotlib.pyplot as plt

def main(filename, filesave, filesave2, probMutation, probCrossover, numRuns, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations):
	numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems = fileParser(filename)
	
	with open(filesave, 'a+') as f_out, open(filesave2, 'a+') as f_out2:
		f_out.write(strftime("%c") + '\n')
		f_out2.write(strftime("%c") + '\n')
		for i in range(numRuns):
			print(i+1)
			best, fitnessBest, fitnessAverage = run(probMutation, probCrossover, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations, numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems)			
			f_out.write(str(best) + '\n')
			f_out2.write(str(fitnessBest) + ',' + str(fitnessAverage) + '\n')
		f_out.write('\n')
		f_out2.write('\n')

def run(probMutation, probCrossover, popSize, tour_selection, crossoverOperator, mutationOperators, selection_survivors_elite, fitnessFunction, generations, numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems):
	# item list in which position is item_i and the value is the city where it was picked
	itemsPop = initializationItems(numItems, numCities, popSize, availabilityItems)
	citiesPop = initializationCities(numCities, popSize)

	fitnessBest = []
	fitnessAverage = []

	for i in range(len(citiesPop)):
		pos = citiesPop[i][0].index(1)
		temp = citiesPop[i][0][pos]
		citiesPop[i][0][pos] = citiesPop[i][0][0]
		citiesPop[i][0][0] = temp

	# evaluate pop here
	fitnessList = [fitness(numCities, numItems, i[0], j[0], distanceMatrix, weightValueItems, availabilityItems, vMax, vMin, knapsackWeight, coefficient, dropRate) for i, j in zip(citiesPop, itemsPop)]
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
			crossover = choice(crossoverOperator)
			sonsItems = crossover(indivItem1, indivItem2, probCrossover)
			progenitoresItems.extend(sonsItems)

			indivCities1 = matePoolCities[j]
			indivCities2 = matePoolCities[j + 1]
			sonsCities = cycle_cross(indivCities1, indivCities2, probCrossover)
			progenitoresCities.extend(sonsCities)

		#print(len(progenitoresItems), len(progenitoresCities))
		descendentesItems = []
		descendentesCities = []
		for i in range(len(progenitoresItems)):
			newCromoItem = mutationOperators[1](progenitoresItems[i][0], availabilityItems)
			newCromoCity = mutationOperators[0](progenitoresCities[i][0], numCities)
			#print(newCromoItem, newCromoCity)
			value = fitness(numCities, numItems, newCromoCity, newCromoItem, distanceMatrix, weightValueItems, availabilityItems, vMax, vMin, knapsackWeight, coefficient, dropRate)

			descendentesItems.append((newCromoItem, value)) # ALTERAR 0 POR FITNESS FUNCTION			
			descendentesCities.append((newCromoCity, value)) # ALTERAR 0 POR FITNESS FUNCTION

		itemsPop = selection_survivors_elite(itemsPop, descendentesItems)
		citiesPop = selection_survivors_elite(citiesPop, descendentesCities)
		#print(len(citiesPop[0][0]))
		#popSize = len(itemsPop)

		# evaluate the new population
		fitnessList = [fitness(numCities, numItems, i[0], j[0], distanceMatrix, weightValueItems, availabilityItems, vMax, vMin, knapsackWeight, coefficient, dropRate) for i, j in zip(citiesPop, itemsPop)]		
		itemsPop = [(itemsPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]
		citiesPop = [(citiesPop[i][0], fitnessList[i]) for i in range(len(fitnessList))]
		
		fitnessAverage.append(np.mean(fitnessList))
		fitnessBest.append(np.max(fitnessList))

	best_pops = [best_pop(itemsPop), best_pop(citiesPop)]
	
	return best_pops, fitnessBest, fitnessAverage
	
def initializationItems(numItems, numCities, popSize, availabilityItems):
	return [([valid_value(availabilityItems,i) for i in range(numItems)], 0) for i in range(popSize)]

def valid_value(availabilityItems,index):
    choices = [i+1 for i, x in enumerate(availabilityItems[index]) if x == 1]
    choices.append(0)
    return choice(choices)

def initializationCities(numCities, popSize):	
	return [(sample(list(range(1, numCities + 1)), numCities), 0) for i in range(popSize)]

def mutationStuff(probMutation):
	def mutationIndiv(cromo, dimension):
		for i in range(len(cromo)):
			if random() < probMutation:
				cromo[i] = randint(1, dimension)

		return cromo
	return mutationIndiv

def crossover(indiv1, indiv2, probCrossover):
	if random() < probCrossover:
		value = randint(1, len(indiv1[0]) - 1)
		newIndiv1 = indiv1[0][:value] + indiv2[0][value:]
		newIndiv2 = indiv2[0][:value] + indiv1[0][value:]
		#print(newIndiv1, newIndiv2)
		return ((newIndiv1, 0), (newIndiv2, 0))
	return indiv1, indiv2


if __name__ == '__main__':
	probMutation = 0.1
	probCrossover = 0.5
	numRuns = 30
	popSize = 1000
	elitePercent = 0.05
	tourSize = int(popSize*0.01)
	generations = 400
	mutationOperators = [mutation(1, probMutation), mutationItem(probMutation)]
	crossoverOperator = [crossover]
	fitnessFunction = fitness
	testsFolder = 'Tests/'
	resultsFolder = 'Results/Run/'
	resultsFolderGen = 'Results/Generation/'
	numberCities = ['100']
	numberItems = ['5']
	instanceNum = [1]
	tightness = ['75']

	
	for z in numberCities:
		for k in numberItems:
			for i in instanceNum:
				for j in tightness:
					filename = z + '/' + z + '_' + k + '_' + str(i) + '_' + j + '.txt'
					main(testsFolder + filename, resultsFolder + filename, resultsFolderGen + filename, probMutation, probCrossover, numRuns, popSize, tour_sel(tourSize), crossoverOperator, mutationOperators, sel_survivors_elite(elitePercent), fitnessFunction, generations)
	
	

	#filename = '10/10_15_10_25.txt'
	#filename = 'test.txt'
	#main(testsFolder + filename, resultsFolder + filename, resultsFolderGen + filename, probMutation, probCrossover, numRuns, popSize, tour_sel(tourSize), crossoverOperator, mutationOperators, sel_survivors_elite(elitePercent), fitnessFunction, generations)


	#20 cities
	#pop 1000
	#gen 500

	#50 cities
	#pop 1500
	#gen 750
