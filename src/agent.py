from src import utilties as utils 
import numpy as np

class Agent():
	def __init__(self, environment, type, id, group_influence, renewal_frequency, opinion_flexibility, \
	             initial_routine, external_influence, influence_proportions):
		self.environment = environment
		self.type = type
		self.id = id
		self.group_influence = group_influence
		self.renewal_frequency = renewal_frequency
		self.opinion_flexibility = opinion_flexibility
		self.routine = initial_routine
		self.external_influence = external_influence
		self.influence_proportions = influence_proportions
		self.inertial_clock = 0


	def change_opinion(self, compiled_influence, inertial_constant, eq_tolerance, change_tolerance, num_iters):
		total_tvd = utils.calculate_tvd(self.routine, compiled_influence)
		scaled_by_flexibility = self.opinion_flexibility * total_tvd
		if self.inertial_clock == 0:
			inertial_factor = 1
		else:
			inertial_factor = 1/(self.intertial_clock * inertial_constant)	
		scaled_by_intertia = scaled_by_flexibility * inertial_factor
		routines = [[self.routine]] + [[compiled_influence]]
		guess = [np.mean(x) for x in np.transpose(np.array(routines))]
		for i in range(num_iters):
			current_guess_error = utils.calculate_tvd(guess, self.routine) - scaled_by_intertia
			if abs(current_guess_error) <= 0 + eq_tolerance:
				break
			else:
				if current_guess_error > 0:
					routines = [[guess]] + [[self.routine]]
				else: 
					routines = [[guess]] + [[compiled_influence]]
				guess = [np.mean(x) for x in np.transpose(np.array(routines))]
		if utils.calculate_tvd(self.routine, guess) > change_tolerance:
			self.inertial_clock == 0
		self.routine = guess

	def variation(self, inertial_constant=5, eq_tolerance=0.025, change_tolerance=0.5, num_iters = 2500):
		sources_of_influence = np.vstack([self.external_influence, \
		                                 np.concatenate(self.environment.group_decisions, axis =0)])
		relative_impacts = self.influence_proportions
		compiled_influence = np.transpose(np.array(sources_of_influence)).dot(relative_impacts)
		self.change_opinion(compiled_influence, inertial_constant, eq_tolerance, change_tolerance, num_iters)