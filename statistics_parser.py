import matplotlib.pyplot as plt
import matplotlib.pylab as lab
import numpy as np
from os import listdir, makedirs, path
from os.path import isfile, join
from matplotlib.legend_handler import HandlerLine2D


def dataFromFile(filename, nRuns, city, showPlot):
	aux = filename.split('/')
	aux = aux[3].split('.')
	#print(aux)
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

		#print(filename[8:-3])
		if showPlot == 0:			
			name = 'Graphs/Run/' + filename[12:-3] + 'png'
			lab.savefig(name)
		else:
			plt.show()
		
		plt.clf()

def dataFromFileGen(filename, nRuns, city, showPlot):
	aux = filename.split('/')
	#print(aux)
	nCities,nItems, dummy1, dummy2 = aux[3].split('_')
	nCities = int(nCities)
	nItems = int(nItems)
	#print(nCities, nItems)
	#print(filename[19:-3])

	with open(filename) as f:
		aux = f.readline()
		for i in range(nRuns):
			aux = f.readline()
			fitnessBest = []
			fitnessAverage = []
			
			aux = aux.replace(', ', ' ')
			aux = aux.replace('[', ' ')
			aux = aux.replace(']', ' ')
			aux = aux.split()

			

			#print(len(aux), i+1)
			for j in range(len(aux)):
				#print(aux[j])
				if j<(len(aux)-1)/2:
					fitnessBest.append(float(aux[j]))

				elif j>(len(aux)-1)/2:
					fitnessAverage.append(float(aux[j]))

			#print(len(fitnessBest), len(fitnessAverage))

			length = int((len(aux)-1)/2)
			plt.plot([j for j in range(0, length)], fitnessBest, label='Best Fitness')
			plt.plot([j for j in range(0, length)], fitnessAverage, label='Average Fitness')
			plt.ylabel('Fitness')
			plt.xlabel('Generations')
			plt.legend(loc=4)
			mng = plt.get_current_fig_manager()
			mng.window.showMaximized()

			#if i==0:
			#	plt.show()
			
			

			
			if showPlot == 0:
				newpath = 'Graphs/Generation/' + filename[19:-4] + '/'
				if not path.exists(newpath):
					makedirs(newpath)
				name = newpath + filename[22:-4] + '_Run' + str(i+1) + '.png'
				lab.savefig(name)
			else:
				plt.show()
			

			plt.clf()




	pass


if __name__ == '__main__':
	resultsFolder = 'Results/Run/'
	resultsFolderGen = 'Results/Generation/'
	graphsFolder = 'Graphs/Run/'
	graphsFolderGen = 'Graphs/Generation/'
	numberCities = ['10', '20', '50', '100']
	nRuns = 30
	showPlot = 0

	
	#Read data from runs
	for k in numberCities:
		mypath1 = resultsFolder + k + '/'
		mypath2 = resultsFolderGen + k + '/'
		onlyfiles = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]
		for i in onlyfiles:
			if i != 'dummy':
				dataFromFile(mypath1 + i, nRuns, k, showPlot)
				dataFromFileGen(mypath2 + i, nRuns, k, showPlot)
	
	#Read data from generations

		
	
	


	#filename = resultsFolderGen + '20/20_5_1_25.txt'
	
	#dataFromFile(filename, nRuns, '50', showPlot)
	#dataFromFileGen(filename, nRuns, '20', showPlot)