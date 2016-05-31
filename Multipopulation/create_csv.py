def create_csv(bests_a, bests_b, filename):
	with open(filename, 'w') as f:
		f.write("Best,Algorithm\n")

		for i in range(len(bests_a)):
			f.write(str(bests_a[i]) + ",A\n")
		for i in range(len(bests_b)):
			f.write(str(bests_b[i]) + ",B\n")
