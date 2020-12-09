def calculate_tvd(probability_set_0, probability_set_1):
	return sum(abs(probability_set_0 - probability_set_1))/2

def calculate_raw_feedback(routine, comparison):
	tvd = calculate_tvd(routine, comparison)
	if tvd < 0.01:
		feedback = 1.0
	elif tvd < 0.05:
		feedback = 0.8
	elif tvd < 0.1:
		feedback = 0.6
	elif tvd < 0.25:
		feedback = 0.4
	elif tvd < 0.5:
		feedback = 0.2
	else:
		feedback = 0.05
	return feedback