from src import agent
import numpy as np

class Environment:

	def __init__(self, intra_group_influence, inter_group_influence, negotiation_frequency, agents_dictionary):
		self.time = 0
		self.agents = {}
		self.influences = inter_group_influence
		self.negotiation_frequency = negotiation_frequency

		for j, key in enumerate(agents_dictionary.keys()):
			num_agents = agents_dictionary[key][0]
			agent_parameters = agents_dictionary[key][1:]
			self.agents[key] = [agent.Agent(self, key, i + 1, intra_group_influence[j][i], *agent_parameters)
								for i in range(num_agents)]
		self.data = {
		'Input Parameters': {
			'Agent': agents_dictionary,
			'Environment': {
				'Inter-Group Influences': inter_group_influence,
				'Intra-Group Influences': intra_group_influence,
				'Negotiation Frequency': negotiation_frequency}},
		'Time Evolving Parameters': {
			'Organizational Routine': [],
			'Group Decisions': [],
			'Group Means': [],
			'Group SDs': [],
			'Time': []}}

		self.negotiate()
		self.get_data()
		
	def negotiate(self):
		group_decisions = []
		for key in self.agents.keys():
			agents = self.agents[key]
			routines = np.transpose(np.array([x.routine  for x in agents]))
			group_influences = np.array([x.group_influence for x in agents])
			group_decision = routines.dot(group_influences)
			group_decisions += [[group_decision]]
		self.routine = np.transpose(np.array(group_decisions)).dot(self.influences)
		self.data['Time Evolving Parameters']['Organizational Routine'] += [[self.routine]]
		self.data['Time Evolving Parameters']['Group Decisions'] += [[group_decisions]]
		self.group_decisions = group_decisions

	def get_data(self):
		means = {}
		sds = {}
		for key in self.agents.keys():
			routines = [x.routine for x in self.agents[key]]
			means[key] = np.mean(routines)
			sds[key] = np.std(routines)
		self.data['Time Evolving Parameters']['Group Means'] += [means]
		self.data['Time Evolving Parameters']['Group SDs'] += [sds]
		self.data['Time Evolving Parameters']['Time'] += [self.time]

	def step(self):
		[[[x.variation()] for x in self.agents[key]] for key in self.agents.keys()]
		self.get_data()
		if self.time % self.negotiation_frequency == 0:
			self.negotiate()
		self.time += 1

	def simulate(self, num_steps):
		for step in range(num_steps):
			self.step()
