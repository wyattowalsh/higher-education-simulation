import numpy as np

def calculate_tvd(probability_set_0, probability_set_1):
	return sum(abs(np.array(probability_set_0) - np.array(probability_set_1)))/2

def normalize(input_list):
	array = np.array(input_list)
	normal = np.divide(array, np.sum(array))
	return normal.tolist()

