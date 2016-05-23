import numpy as np

def file_parser(file_number):
	folder = 'Tests/'
	file_capacity = 'p0' + str(file_number) + '_c.txt'
	file_weights = 'p0' + str(file_number) + '_w.txt'
	file_profits = 'p0' + str(file_number) + '_p.txt'

	with open(file_capacity, 'r') as f:
		knapsack_capacity = int(f.readline())

	with open(file_weights, 'r') as f:
		temp_list = []
		number_objects = 0

		for line in f:
			temp_list.append(int(line))
			number_objects += 1

		knapsack_weights = np.array(temp_list)

	with open(file_profits, 'r') as f:
		temp_list = []

		for line in f:
			temp_list.append(int(line))

		knapsack_profits = np.array(temp_list)

	return knapsack_capacity, number_objects, objects_weight, objects_profit
