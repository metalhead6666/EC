def fitness(numCities, numItems, x, z, distanceMatrix, weightValueItems, availabilityItems, vMax, vMin, knapsackWeight, coefficient, dropRate):
	
	#If the first city in the tour is not 1, return 0
	if x[0] != 1:
		return 0

	for i in range(1, numCities + 1):
		if x.count(i) > 1:
			return 0

	times_item = [-1]*numItems
	Wc = 0
	vc = 0
	time_total = 0

	#Calculate TIME of the tour
	for i in range(0, numCities):
		#print(i, numCities, x)
		next_city = x[(i+1)%numCities]
		array_items = []
		current_city = x[i]
		#Check which items were picked it the current city
		if z.count(current_city)>0:
			for j in range(z.index(current_city), numItems):
				#Check if item j was taken from city i, and also if it exists there
				#print(j, len(availabilityItems), current_city-1)
				if z[j] == current_city and availabilityItems[j][current_city-1]==1:					
					array_items.append(j)

				#If item doesn't exist in city, return 0
				elif z[j] == current_city and availabilityItems[j][current_city-1]==0:
					return 0

		#Calculate weight on knapsack
		if len(array_items) > 0:
			for j in array_items:
				#print(j, len(weightValueItems[0]), len(array_items))
				Wc = Wc + weightValueItems[0][j]

				#If current weight is bigger than the capacity of the knapsack, return 0
				if Wc > knapsackWeight:
					return 0
				#Insert time in which the item was added to the bag
				times_item[j] = time_total

		#Increases time
		vc = vMax - Wc*(vMax - vMin)/knapsackWeight
		distance_next_city = distanceMatrix[current_city-1][next_city-1]
		time_total = time_total + distance_next_city/vc


	#print(time_total)
	#Calculate PROFIT of the tour

	profit_total = 0

	for i in range(numItems):
		if times_item[i] != -1:
			time_bag = time_total - times_item[i]
			profit_total = profit_total + weightValueItems[1][i]*dropRate**(time_bag/coefficient)

	#print(profit_total)
	#print(profit_total, time_total)
	return profit_total/time_total
