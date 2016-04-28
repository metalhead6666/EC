import matplotlib.pyplot as plt
import matplotlib.pylab as lab
import numpy as np
from os import listdir
from os.path import isfile, join


def dataFromFile(filename, nRuns, city, showPlot):
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
			mean = np.mean(fitness)
			props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
			plt.text(0.5, fitness[best_index]*0.95, 'BEST\nTour: ' + str(best_tour) + '\nItems: ' + str(best_item) + '\nFitness: ' + str(best_fitness) + '\nAverage Best of all runs: ' + str(mean), bbox=props)

		plt.xticks([i for i in range(1, nRuns+1)])
		plt.ylabel('Fitness')
		plt.xlabel('Runs')
		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()

		
		if showPlot == 0:			
			name = 'Graphs/' + filename[8:-3] + 'png'
			lab.savefig(name)
		else:
			plt.show()
		
		plt.clf()


if __name__ == '__main__':
	resultsFolder = 'Results/'
	graphsFolder = 'Graphs/'
	numberCities = ['10', '20', '50', '100']
	nRuns = 30
	showPlot = 1

	"""
	for k in numberCities:
		mypath = resultsFolder + k + '/'
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		for i in onlyfiles:
			filename = mypath + i
			dataFromFile(filename, nRuns, k, showPlot)
		#print(onlyfiles)
	"""
	


	filename = 'Results/50/50_15_1_75.txt'
	
	dataFromFile(filename, nRuns, '50', showPlot)