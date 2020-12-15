import agent
import utilities as utils
import numpy as np

class Environment:

	def __init__(self, parameters):
		self.time = 0
		self.agents = {}
		self.inter_group_influences = parameters['inter_group_influences']
		self.negotiation_frequency = parameters['negotiation_frequency']

		for j, key in enumerate(parameters['stakeholders'][0]):
			num_agents = parameters['number_of_agents'][j]
			self.agents[key] = [agent.Agent(id = i + 1, environment = self,
									type=key, 
			                        intra_group_influence = parameters['intra_group_influences'][key][0][i], 
			                        renewal_frequency = parameters['renewal_frequencies'][j],
			                        opinion_flexibility= parameters['opinion_flexibilities'][j],
	             					initial_routine= parameters['initial_routines'][key][i], 
	             					external_influence = parameters['external_influences'][j],
	             					relative_influences = parameters['relative_influences'])
								for i in range(num_agents)]
		self.data = {
		'inputs': parameters,
		'organizational_routine': [],
			'decisions_group': [],
			'means_group': [],
			'sd_group': [],
			'convergence_proportions_group': [],
			'time': []}

		self.negotiate()
		self.get_data()
		
	def negotiate(self):
		group_decisions = []
		for key in self.agents.keys():
			agents = self.agents[key]
			routines = np.transpose(np.array([x.routine  for x in agents]))
			group_influences = np.array([x.intra_group_influence for x in agents])
			group_decision = routines.dot(group_influences)
			group_decision = utils.normalize(group_decision)
			group_decisions += [[group_decision]]
		routine = np.transpose(np.array(group_decisions)).dot(self.inter_group_influences)
		self.routine = utils.normalize(routine)
		self.data['organizational_routine'] += [[self.routine]]
		self.data['decisions_group'] += [[group_decisions]]
		self.group_decisions = group_decisions

	def data_getter(self):
		return self.data

	def get_data(self):
		means = {}
		sds = {}
		convergence_proportion = {}
		for key in self.agents.keys():
			routines = [x.routine for x in self.agents[key]]
			convergences = [x.convergence for x in self.agents[key]]
			convergence_proportion[key] = np.mean(convergences)
			means[key] = np.mean(routines, 0)
			sds[key] = np.std(routines, 0)
		self.data['means_group'] += [means]
		self.data['sd_group'] += [sds]
		self.data['time'] += [self.time + 1]
		self.data['convergence_proportions_group'] += [convergence_proportion]

	def step(self):
		[[[x.variation()] for x in self.agents[key]] for key in self.agents.keys()]
		self.get_data()
		if self.time % self.negotiation_frequency[0] == 0:
			self.negotiate()
		self.time += 1
		# if self.time % 50 == 0:
		# 	print('Simulation of time step {} successfully completed'.format(self.time))
	
	def simulate(self, num_steps):
		[self.step() for i in range(num_steps)]
		self.data['inputs'] = [self.data['inputs']] * len(self.data['time'])