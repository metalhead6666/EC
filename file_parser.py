def file_parser(filename):
	with open(filename) as f:
		numCities = int(f.readline())
		numItems = int(f.readline())
		knapsackWeight = int(f.readline())
		vMax = float(f.readline())
		vMin = float(f.readline())
		coefficient = float(f.readline())
		dropRate = float(f.readline())

		distanceMatrix = saveMatrix(numCities, f, float)
		weightValueItems = saveMatrix(2, f, float)		
		availabilityItems = saveMatrix(numItems, f, int)

	return numCities, numItems, knapsackWeight, vMax, vMin, coefficient, dropRate, distanceMatrix, weightValueItems, availabilityItems


def saveMatrix(num, f, type):
	distanceMatrix = []

	for i in range(num):
		line = f.readline().split(" ")
		del(line[-1])
		line = list(map(type, line))
		distanceMatrix.append(line)

	return distanceMatrix

if __name__ == '__main__':
	file_parser('Tests/10/10_3_1_25.txt')
