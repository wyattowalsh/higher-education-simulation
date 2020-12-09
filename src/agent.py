import random

random.seed(18)

import numpy as np

class Agent():

	def __init__(self, type, id, environment, choice_frequency, group_influence, 
	             change_capacity, feedback_proximity, routine_mean, routine_sd, ideal_routine_mean, 
	             ideal_routine_sd):
		self.type = type
		self.id = id
		self.environment = environment
		self.choice_frequency = choice_frequency
		self.group_influence = group_influence
		self.change_capacity = change_capacity
		self.feedback_proximity = feedback_proximity
		self.routine = np.random.normal(routine_mean, routine_sd)
		self.ideal_routine = np.random.normal(ideal_routine_mean, ideal_routine_sd)
		self.intertial_clock = 1

	def variation(self, environment):
		for i in range(self.choice_frequency):
			feedback = environment.give_feedback(self.ideal_routine)
			interpreted = 1 + (self.feedback_proximity *(feedback - 1))
			capacity = self.change_capacity * (1 - interpreted)
			if capacity == 0:
				self.intertial_clock += 1
			else:
			 	self.intertial_clock = 1
			capacity_inertia = capacity / (self.intertial_clock * (1))
			if self.environment.routine - self.ideal_routine > 0:
				self.routine = self.routine - capacity_inertia
			else:
				self.routine = self.routine + capacity_inertia

