import utilities as utils 
import numpy as np

class Agent():

	def __init__(self, id, environment, type, intra_group_influence, renewal_frequency, opinion_flexibility, \
	             initial_routine, external_influence, relative_influences):
		self.environment = environment
		self.type = type
		self.id = id
		self.intra_group_influence = intra_group_influence
		self.renewal_frequency = renewal_frequency
		self.opinion_flexibility = opinion_flexibility
		self.routine = initial_routine
		self.external_influence = external_influence
		self.relative_influences = relative_influences
		self.inertial_clock = 0
		self.convergence = 0



	def change_opinion(self, compiled_influence, inertial_constant, eq_tolerance, change_tolerance):
		def binary_search(level, guess, lower_bound, upper_bound, tolerance=0.04):
			level = level + 1
			TVD_guess = utils.calculate_tvd(self.routine[0], guess)
			error = scaled_by_intertia - TVD_guess
			if level == 900:
				# print('type: {}, {} did not converge w/ error: {}'.format(self.type, self.id, error))
				self.convergence = 0
				return guess
			if abs(error) < tolerance:
				# print('type: {}, {} converged'.format(self.type, self.id))
				self.convergence = 1
				return guess
			else:
				routines = np.array(np.vstack([lower_bound, upper_bound]))
				new_guess = utils.normalize(np.mean(routines, 0))

				if utils.calculate_tvd(new_guess, guess) < 1e-6:
					# print(self.type, self,id, 'stable guesses')
					self.convergence = 0
					return guess 
				if error < 0:
					return binary_search(level, new_guess, lower_bound, guess)
				else:
					return binary_search(level, new_guess, guess, upper_bound)

		total_tvd = utils.calculate_tvd(self.routine[0], compiled_influence)
		scaled_by_flexibility = self.opinion_flexibility * total_tvd
		if self.inertial_clock == 0 or self.inertial_clock == 1:
			inertial_factor = 1
		else:
			inertial_factor = 1/(self.inertial_clock/(self.inertial_clock - inertial_constant))	
		scaled_by_intertia = scaled_by_flexibility * inertial_factor
		routines = np.array(np.vstack([self.routine, compiled_influence]))
		guess = np.mean(routines, 0)
		guess = utils.normalize(guess)
		lower_bound = self.routine
		upper_bound = compiled_influence
		new_routine = binary_search(0, guess, lower_bound, upper_bound)
		# for i in range(num_iters):
		# 	routines = np.array(np.vstack([lower_bound, upper_bound]))
		# 	guess = np.mean(routines, 0)
		# 	TVD_guess = utils.calculate_tvd(self.routine[0], guess)
		# 	error = scaled_by_intertia - TVD_guess
		# 	if abs(error) < eq_tolerance:
		# 		print('converged')
		# 		break
		# 	else:
		# 		if error < 0:
		# 			lower_bound = lower_bound
		# 			upper_bound = guess
		# 		else:
		# 			lower_bound = guess
		# 			upper_bound = upper_bound
		# if i == num_iters - 1:
		# 	print('failed to converge')
		# new_routine = guess
		TVD_new = utils.calculate_tvd(self.routine[0], new_routine)
		# error = scaled_by_intertia - TVD_guess
		# iteration_count = 0
		# while abs(error) > eq_tolerance: 
		# 	iteration_count = iteration_count + 1
		# 	if iteration_count >= num_iters:
		# 		print('Maximum iterations reached for {}, {} with error: {}'.format(self.type, self.id, error))
		# 		print('Associated inertial clock value is: {}'.format(self.inertial_clock))
		# 		break
		# 	if error < 0:
		# 		routines = np.array(np.vstack([guess, self.routine]))
		# 	else:
		# 		routines = np.array(np.vstack([guess, compiled_influence]))
		# 	guess = np.mean(routines, 0)
		# 	# guess = utils.normalize(np.mean(routines, 0))
		# 	TVD_guess = utils.calculate_tvd(self.routine[0], guess)
		# 	error = scaled_by_intertia - TVD_guess
		if TVD_new > change_tolerance:
			self.inertial_clock == 0
		self.routine = new_routine
		'''consider instead of individual guessing conducting hypothesis test'''

	def variation(self, inertial_constant=1, eq_tolerance=0.05, change_tolerance=0.25):
		sources_of_influence = np.vstack([self.external_influence, \
		                                 np.reshape(np.concatenate(self.environment.group_decisions, axis =0), (4,4))])
		relative_impacts = self.relative_influences
		compiled_influence = np.transpose(np.array(sources_of_influence)).dot(relative_impacts)
		compiled_influence = utils.normalize(compiled_influence)
		self.change_opinion(compiled_influence, inertial_constant, eq_tolerance, change_tolerance)