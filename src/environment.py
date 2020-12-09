from src import agent
import numpy as np

class Environment:

	def __init__(self, initial_routine, influences_between_groups, negotiation_frequency,
				 initial_group_decisions):
		self.routine = initial_routine
		self.time = 0
		self.agents = {}
		self.influences = influences_between_groups
		self.negotiation_frequency = negotiation_frequency
		self.group_decisions = initial_group_decisions
		self.data = {'Input Parameters': []
					'Organizational Routine': [[initial_routine]],
					'Influence Between Groups': [[influences_between_groups]],
					'Negotiation Frequency': [[negotiation_frequency]],
					'Group Decisions': [[initial_group_decisions]],
					'Group Means': [],
					'Group SDs': [],
					'Time': [[0]]} 

	def add_agents(self, agents_dictionary):
		''' Agent dictionary should be in such a form such that the key relates to the type, with values
		in the form of a list such as: [number_of_agents, choice_frequency, group_influence, 
	             change_capacity, feedback_proximity] '''
	    self.data['Input Parameters'] += agents_dictionary
		for key in agents_dictionary.keys():
			num_agents = agents_dictionary[key][0]
			agent_parameters = agents_dictionary[key][1:]
			self.agents[key] = [agent.Agent(key, i + 1, self, *agent_parameters)
								for i in range(num_agents)]

	def negotiate(self):
		group_decisions = []
		for key in self.agents.keys():
			agents = self.agents[key]
			group_decision = sum([x.routine * x.group_influence for x in agents])
			group_decisions += [group_decision]
		self.real_routine = sum([a*b for a,b in zip(group_decisions, self.influences_between_groups)])
		self.data['Organizational Routine'] += [self.real_routine]
		self.data['Group Decisions'] += [group_decisions]
		self.group_decisions = group_decisions

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
