from src import agent
import numpy as np

class Environment:

	def __init__(self, routine, ideal_routine, influences_between_groups, choice_frequency):
		self.routine = routine
		self.ideal_routine = ideal_routine
		self.time = 0
		self.agents = {}
		self.influences = influences_between_groups
		self.choice_frequency = choice_frequency
		self.data = {'Organizational Routine': [[routine]],
					'Influence Between Groups': [[influences_between_groups]],
					'Choice Frequency': [[choice_frequency]],
					'Group Decisions': [],
					'Group Means': [],
					'Group SDs': [],
					'Time': [[0]]} 

	def add_agents(self, agents_dictionary):
		''' Agent dictionary should be in such a form such that the key relates to the type, with values
		in the form of a list such as: [number_of_agents, choice_frequency, group_influence, 
	             change_capacity, feedback_proximity] '''
		for key in agents_dictionary.keys():
			self.agents[key] = [agent.Agent(key, i + 1, self, 
			                    agents_dictionary[key][1], agents_dictionary[key][2], 
			                    agents_dictionary[key][3], agents_dictionary[key][4],
			                    agents_dictionary[key][5], agents_dictionary[key][6],
			                    agents_dictionary[key][7], agents_dictionary[key][8])
								for i in range(agents_dictionary[key][0])]

	def give_feedback(self, ideal_routine):
		if ideal_routine - 2 <= self.routine <= ideal_routine + 2:
		 	feedback = 1.0
		elif ideal_routine - 10 <= self.routine <= ideal_routine + 10:
			feedback = 0.5
		elif ideal_routine - 20 <= self.routine <= ideal_routine + 20:
			feedback = 0.25
		elif ideal_routine - 30 <= self.routine <= ideal_routine + 30:
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
		self.data['Group Decisions'] += [group_decisions]

	# def negotiate_pre(self):
	# 	group_decisions = []
	# 	students = self.agents['Students']
	# 	faculty = self.agents['Faculty']
	# 	students_decision = sum([x.routine * x.group_influence for x in students])
	# 	faculty_decision = 	sum([x.routine * x.group_influence for x in faculty])
	# 	overall_decision = students_decision

	def get_data(self):
		means = {}
		sds = {}
		for key in self.agents.keys():
			routines = [x.routine for x in self.agents[key]]
			means[key] = np.mean(routines)
			sds[key] = np.std(routines)
		self.data['Group Means'] += [means]
		self.data['Group SDs'] += [sds]
		self.data['Time'] += [self.time]

	def step(self):
		[[x.variation(self) for x in self.agents[key]] for key in self.agents.keys()]
		self.get_data()
		if self.time % self.choice_frequency == 0:
			self.negotiate()
		self.time += 1

	def simulate(self, num_steps):
		for step in range(num_steps):
			self.step()
