from pandas import read_csv
from scipy.stats import ttest_ind, normaltest
import matplotlib.pyplot as plt


def statistical_analysis(foldername, filename, verbose):
	experimentDF = read_csv(foldername + filename)

	alg_a = experimentDF[experimentDF["Algorithm"] == "A"]
	alg_b = experimentDF[experimentDF["Algorithm"] == "B"]

	if verbose:
		ax = alg_a.plot()
		ax2 = ax.twiny()
		alg_b.plot(ax = ax2,color="red")	
		plt.show()

	with open(foldername + "analysis_" + filename[:-4] + '.txt', 'w') as f:
		f.write(str(normaltest(experimentDF["Best"])) + "\n")
		f.write(str(ttest_ind(alg_a["Best"], alg_b["Best"])))

	fig, ax = plt.subplots()
	experimentDF.boxplot(ax = ax, by = 'Algorithm')

	if verbose:
		plt.show()
	
	fig.savefig("Images/boxplot_" + filename[:-4] + '.png')


if __name__ == '__main__':
	statistical_analysis("Results/", "8_0.5_0.75.csv", True)
