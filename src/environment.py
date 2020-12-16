import agent
import utilities as utils
import numpy as np

class Environment:

	def __init__(self, parameters):
		self.routine = [[0,0,0,0]]
		self.group_decisions = [[0,0,0,0]] * 4
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
		'time': [],
		'organizational_routine': [],
			'organizational_routine_change': []}
		
		for key in parameters.keys():
			self.data["input_{}".format(key)] = [parameters[key]] * 101

		for stakeholder in parameters['stakeholders'][0]:
			self.data['decisions_{}'.format(stakeholder)] = []
			self.data['decisions_change_{}'.format(stakeholder)] = []
			self.data['means_{}'.format(stakeholder)] = []
			self.data['means_change_{}'.format(stakeholder)] = []
			self.data['sd_{}'.format(stakeholder)] = []
			self.data['sd_change_{}'.format(stakeholder)] = []
			self.data['convergence_proportion_{}'.format(stakeholder)] = []
			self.data['convergence_proportion_change_{}'.format(stakeholder)] = []

		self.negotiate()
		self.get_data()
		
	def negotiate(self):
		group_decisions = []
		for i, key in enumerate(self.agents.keys()):
			agents = self.agents[key]
			routines = np.transpose(np.array([x.routine  for x in agents]))
			group_influences = np.array([x.intra_group_influence for x in agents])
			group_decision = routines.dot(group_influences)
			group_decision = utils.normalize(group_decision)
			self.data['decisions_{}'.format(key)] += [np.array(group_decision).ravel()]

			change = utils.calculate_tvd(np.array(self.group_decisions[i]).ravel(), \
			                             np.array(group_decision).ravel())
			self.data['decisions_change_{}'.format(key)] += [change]
			group_decisions += [[group_decision]]
		routine = np.transpose(np.array(group_decisions)).dot(self.inter_group_influences)
		change_routine = utils.calculate_tvd(np.array(self.routine).ravel(), np.array(routine).ravel())
		self.routine = utils.normalize(routine)
		self.data['organizational_routine'] += [np.array(self.routine).ravel()]
		self.data['organizational_routine_change'] += [change_routine]
		self.group_decisions = group_decisions

	def data_getter(self):
		return self.data

	def get_data(self):
		for key in self.agents.keys():
			routines = [x.routine for x in self.agents[key]]
			convergences = [x.convergence for x in self.agents[key]]
			convergence_proportion = np.mean(convergences)
			
			means = utils.normalize(np.mean(routines, 0))
			
			sds = np.std(routines, 0)
			
			try:
				change_convergence_proportion = convergence_proportion - \
									self.data['convergence_proportion_{}'.format(key)][-1] 
				change_means = utils.calculate_tvd(np.array(self.data['means_{}'.format(key)][-1]).ravel(),\
											np.array(means).ravel()) 
				change_sds = sds - self.data['sd_{}'.format(key)][-1]
			except:
				change_convergence_proportion = convergence_proportion
				change_means = utils.calculate_tvd(np.array([0,0,0,0]),\
											np.array(means).ravel()) 
				change_sds = sds
			self.data['means_{}'.format(key)] += [np.array(means).ravel()]
			self.data['means_change_{}'.format(key)] += [change_means]
			self.data['sd_{}'.format(key)] += [np.array(sds).ravel()]
			self.data['sd_change_{}'.format(key)] += [np.array(change_sds).ravel()]
			self.data['convergence_proportion_{}'.format(key)] += [convergence_proportion]
			self.data['convergence_proportion_change_{}'.format(key)] += [change_convergence_proportion]
		
		self.data['time'] += [self.time + 1]
		

	def step(self):
		[[[x.variation()] for x in self.agents[key]] for key in self.agents.keys()]
		self.get_data()
		if self.time % self.negotiation_frequency == 0:
			self.negotiate()
		else:
			for key in self.agents.keys():	
				self.data['decisions_{}'.format(key)] += [self.data['decisions_{}'.format(key)][-1]]
				self.data['decisions_change_{}'.format(key)] += [0]
			self.data['organizational_routine'] += [self.data['organizational_routine'][-1]]
			self.data['organizational_routine_change'] += [0]
		self.time += 1
		# if self.time % 50 == 0:
		# 	print('Simulation of time step {} successfully completed'.format(self.time))
	
	def simulate(self, num_steps):
		[self.step() for i in range(num_steps)]
		# self.data['inputs'] = [self.data['inputs']] * len(self.data['time'])