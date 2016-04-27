import matplotlib.pyplot as plt

def dataFromFile(filename, nRuns):
	aux = filename.split('/')

	aux = aux[2].split('.')
	nCities,nItems, dummy1, dummy2 = aux[0].split('_')
	nCities = int(nCities)
	nItems = int(nItems)
	#print(nCities, nItems)

	with open(filename) as f:
		aux = f.readline()

		best_index = -1
		best_fitness = 0
		best_tour = []
		best_item = []

		fitness = [0]*nRuns
		max_fitness = 0
		for i in range(nRuns):
			aux = f.readline()
			aux = aux[2:-2]
			aux = aux.replace(', ', ' ')
			aux = aux.replace('[', ' ')
			aux = aux.replace('(', ' ')
			aux = aux.replace(']', ' ')
			aux = aux.replace(')', ' ')		
			aux = aux.split()

			items = [0]*nItems
			for index in range(nItems):
				items[index] = int(aux[index])

			#print(items)

			fitness[i] = float(aux[nItems])
			#print(fitness)

			j=0
			tour = [0]*nCities
			for index in range(nItems+1,nItems+1+nCities):
				tour[j] = aux[index]
				j += 1

			#print(tour)

			if fitness[i] > best_fitness:
				best_tour = tour
				best_item = items
				best_fitness = fitness[i]
				best_index = i


		plt.plot([i for i in range(1, nRuns+1)], fitness, '-o')
		if best_index >= 0:
			props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
			plt.text(best_index+1.25, fitness[best_index], 'Tour: ' + str(best_tour) + '\nItems: ' + str(best_item) + '\nFitness: ' + str(best_fitness), bbox=props)

		plt.ylabel('Fitness')
		plt.xlabel('Runs')

		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()
		plt.show()


if __name__ == '__main__':
	filename = 'Results/20/20_5_6_75.txt'
	nRuns = 30
	dataFromFile(filename, nRuns)