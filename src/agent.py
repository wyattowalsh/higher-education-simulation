from src import utilties as utils 

class Agent():
	def __init__(self, environment, type, id, renewal_frequency, group_influence, opinion_flexibility, 
	             initial_routine, external_influence, influence_proportions, change_capacities):
		self.environment = environment
		self.type = type
		self.id = id
		self.renewal_frequency = renewal_frequency
		self.group_influence = group_influence
		self.opinion_flexibility = opinion_flexibility
		self.initial_routine = initial_routine
		self.external_influence = external_influence
		self.influence_proportions = influence_proportions
		self.change_capacities = change_capacities
		self.intertial_clock = 1

	def variation(self, environment):
		feedback_routines = [self.external_influence] + [self.environment.group_decisions]
		raw_feedback = [utils.calculate_raw_feedback(self.routine, x) for x in feedback_routines]
		interpreted_feedback = [a*b for a, b in zip(raw_feedback, self.influence_proportions)]
		integrated_feedback = [x * self.opinion_flexibility for x in interpreted_feedback]

	def variation(self, environment):
		for i in range(self.choice_frequency):
			external_feedback = environment.give_feedback(self.ideal_routine)
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

