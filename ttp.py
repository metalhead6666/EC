#! /usr/bin/env python3

from file_parser import fileParser
from random import randint, sample, choice, random
from jb_int import *
from sea_int_2016 import *
from time import strftime
from fitness import fitness

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
			sonsCities = crossover(indivCities1, indivCities2, probCrossover)
			progenitoresCities.extend(sonsCities)

		#print(len(progenitoresItems), len(progenitoresCities))
		descendentesItems = []
		descendentesCities = []
		for i in range(len(progenitoresItems)):
			newCromoItem = mutationOperators(progenitoresItems[i][0], numCities)
			newCromoCity = mutationOperators(progenitoresCities[i][0], numCities)
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

	best_pops = [best_pop(itemsPop), best_pop(citiesPop)]
	return best_pops
	
def initializationItems(numItems, numCities, popSize):
	return [([randint(0, numCities) for i in range(numItems)], 0) for i in range(popSize)]

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
		return ((newIndiv1, 0), (newIndiv2, 0))
	return indiv1, indiv2


if __name__ == '__main__':
	probMutation = 0.1
	probCrossover = 0.5
	numRuns = 30
	popSize = 500
	elitePercent = 0.05
	tourSize = int(popSize*0.01)
	generations = 200
	mutationOperators = mutation(1, probMutation)
	crossoverOperator = [crossover]
	fitnessFunction = fitness
	testsFolder = 'Tests/'
	resultsFolder = 'Results/'
	numberCities = ['10', '20', '50', '100']
	numberItems = ['5']
	instanceNum = [i for i in range(1, 11)]
	tightness = ['25', '50', '75']

	for z in numberCities:
		for k in numberItems:
			for i in instanceNum:
				for j in tightness:
					filename = z + '/' + z + '_' + k + '_' + str(i) + '_' + j + '.txt'
					main(testsFolder + filename, resultsFolder + filename, probMutation, probCrossover, numRuns, popSize, tour_sel(tourSize), crossoverOperator, mutationOperators, sel_survivors_elite(elitePercent), fitnessFunction, generations)
