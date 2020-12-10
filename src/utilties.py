import numpy as np

def calculate_tvd(probability_set_0, probability_set_1):
	return sum(abs(np.array(probability_set_0) - np.array(probability_set_1)))/2