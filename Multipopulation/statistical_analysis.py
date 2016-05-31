from pandas import read_csv
from scipy.stats import ttest_ind

def statistical_analysis(filename):
	experimentDF = read_csv(filename)

	alg_a = experimentDF[experimentDF["Algorithm"] == "A"]
	alg_b = experimentDF[experimentDF["Algorithm"] == "B"]

	print(ttest_ind(alg_a["Best"], alg_b["Best"]))
