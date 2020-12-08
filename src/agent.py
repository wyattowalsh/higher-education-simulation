class Agent():

	def __init__(self, type, id, environment, choice_frequency, group_influence, 
	             change_capacity, feedback_proximity):
		self.type = type
		self.id = id
		self.environment = environment
		self.choice_frequency = choice_frequency
		self.group_influence = group_influence
		self.change_capacity = change_capacity
		self.feedback_proximity = feedback_proximity
		self.routine = self.environment.real_routine
		self.intertia = 0

	def variation(self):
		feedback = self.environment.give_feedback()
		interpreted = 1 + (self.feedback_proximity *(feedback - 1))
		capacity = self.change_capacity * (1 - interpreted)
		capacity_inertia = capacity / (self.intertia * (1/5))
		if self.environment.real_routine - self.environment.ideal_routine > 0:
			self.routine = self.routine - capacity_inertia
		else:
			self.routine = self.routine + capacity_inertia


	# class Student:
		

	# class Faculty:

	# class Student:

	# 	class Undergrad:
	# 		def __init__(self):
	# 			pass
	# 	class Graduate:
	# 		def __init__(self):
	# 			pass

	# class Faculty:

	# class Administration:

	# class Staff:
	