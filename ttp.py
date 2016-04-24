#! /usr/bin/env python3

from file_parser import fileParser

def main(filename, probMutation, probCrossover, numRuns):
	numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems = fileParser(filename)
	
	# item list in which position is item_i and the value is the city where it was picked
	items = initialization(numItems)

	# item time list which defines the time where item_i was picked -> necessary to g(x,z)
	itemsTime = initialization(numItems)

	# time passed since the start of the trip
	timePassed = 0

	# actual speed, which is between vMin and vMax
	vActual = vMax

	# actual knapsack weight, which is between 0 and knapsackWeight
	actualKnapsackWeight = 0
	
def initialization(num):
	return [0]*num

def mutation(items, probability):
	return items

def crossover(items, probability):
	return items

def fitness(items, dropRate, vMax, vMin):
	return 0

if __name__ == '__main__':
	probMutation = 0.01
	probCrossover = 0.9
	numRuns = 30	
	main('Tests/10/10_3_1_25.txt', probMutation, probCrossover, numRuns)
