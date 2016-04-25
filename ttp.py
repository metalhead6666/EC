#! /usr/bin/env python3

from file_parser import fileParser
from random import randint, sample

def main(filename, probMutation, probCrossover, numRuns, popSize):
	numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems = fileParser(filename)
	
	# item list in which position is item_i and the value is the city where it was picked
	itemsPop = initialization_items(numItems, numCities, popSize)

	citiesPop = initialization_cities(numCities, popSize)
	#print(citiesPop)
	
def initialization_items(numItems, numCities, popSize):
	return [[randint(1, numCities) for i in range(numItems)] for i in range(popSize)]

def initialization_cities(numCities, popSize):	
	return [sample(list(range(1, numCities + 1)), numCities) for i in range(popSize)]


if __name__ == '__main__':
	probMutation = 0.1
	probCrossover = 0.9
	numRuns = 30
	popSize = 10	
	main('Tests/10/10_3_1_25.txt', probMutation, probCrossover, numRuns, popSize)
