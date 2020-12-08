from src import agent

class Environment:

	def __init__(self, ideal_routine, real_routine, influences_between_groups):
		self.ideal_routine = ideal_routine
		self.real_routine = real_routine
		self.time = 0
		self.agents = {}
		self.influences = influences_between_groups
		self.data = {'Target Customer Value': [ideal_routine],
					'Organizational Routine': [real_routine],
					'Influence Between Groups': influences_between_groups,
					'Time': [0]} 

	def add_agents(self, agents_dictionary):
		''' Agent dictionary should be in such a form such that the key relates to the type, with values
		in the form of a list such as: [number_of_agents, choice_frequency, group_influence, 
	             change_capacity, feedback_proximity] '''
		for key in agents_dictionary.keys():
			self.agents[key] = [agent.Agent(key, i + 1, self, 
			                    agents_dictionary[key][1], agents_dictionary[key][2], 
			                    agents_dictionary[key][3], agents_dictionary[key][4])
								for i in range(agents_dictionary[key][0])]

	def set_ideal_routine(self, new_ideal):
		self.ideal_routine = new_ideal

	def set_real_routine(self, new_real):
		self.real_routine = new_real

	def give_feedback(self):
		if self.ideal_routine - 2 <= self.real_routine <= self.ideal_routine + 2:
		 	feedback = 1.0
		elif self.ideal_routine - 10 <= self.real_routine <= self.ideal_routine + 10:
			feedback = 0.5
		elif self.ideal_routine - 20 <= self.real_routine <= self.ideal_routine + 20:
			feedback = 0.25
		elif self.ideal_routine - 30 <= self.real_routine <= self.ideal_routine + 30:
			feedback = 0.1
		else:
			feedback = 0.05
		return feedback

	def negotiate(self):
		group_decisions = []
		for key in self.agents.keys():
			agents = self.agents[key]
			group_decision = sum([x.routine * x.group_influence for x in agents])
			group_decisions += [group_decision]
		self.real_routine = sum([a*b for a,b in zip(group_decisions, self.influences)])
		self.data['Organizational Routine'] += [self.real_routine]

	def step(self):
		self.time += 1
		self.negotiate()
		self.find_data()

	def simulate(self, num_steps):
		for step in range(num_steps):
			self.step()
