from datetime import datetime 
from sklearn.model_selection import ParameterGrid as grid
import environment as env
import utilities as utils

import json
import multiprocessing
import numpy as np
import pandas as pd

class Model():

	def __init__(self):
		self.stakeholders = []
		self.number_of_agents = []
		self.negotiation_frequency = 0
		self.intra_group_influences = {}
		self.inter_group_influences = []
		self.renewal_frequency = []
		self.opinion_flexibilities = []
		self.initial_routines  = {}
		self.external_influences = {}
		self.relative_impacts = []
		self.experiment_parameters = []

	def set_environment(self, experiment_parameters):
		self.environment = env.Environment(experiment_parameters)


	def set_intra_group_influences(self, stakeholders, number_of_agents):
		for i, stakeholder in enumerate(stakeholders[0]):
			rvs = np.random.default_rng().exponential(scale = 1, size = number_of_agents[i])
			rvs_normal = np.round(utils.normalize(rvs),8).tolist()
			self.intra_group_influences[stakeholder] = [rvs_normal]

	def generate_experiment_parameter_set(self, stakeholders, number_of_agents, negotiation_frequency):
		self.set_intra_group_influences(stakeholders, number_of_agents)
		inter_group_influences = [
						[0.2, 0.2, 0.4, 0.2],
						[0.813, 0.067, 0.013, 0.107],
						[0.25, 0.25, 0.4, 0.1]
						]
		# inter_group_influences = [
		# 				[0.1, 0.1, 0.7, 0.1],
		# 				[0.2, 0.2, 0.4, 0.2],
		# 				[0.813, 0.067, 0.013, 0.107]
		# 				]
		renewal_frequencies = [[1,1,1,1],
							[3,3,3,3],
							[5,5,5,5]]				
		# renewal_frequencies = [
		# 					[1, 1, 1, 1],
		# 					[5, 5, 5, 5],
		# 					]

		initial_routines = {}
		initial_routines_other = {}
		external_influences = []
		for i, stakeholder in enumerate(stakeholders[0]):
			initial_list = [0.2]*len(stakeholders[0]) 
			initial_list[i] = 0.4
			external_influences += [initial_list] 
			# initial_routines[stakeholder] = [[initial_list] * number_of_agents[i]]
			rvs = np.random.default_rng().uniform(low = 0.25, high = 1, size = number_of_agents[i])
			routine_proportion_other = np.round((1 - rvs)/3,3)
			routines = [[b, b, b] for a,b in zip(rvs, routine_proportion_other)]
			routines = [np.insert(x, i, rvs[j]) for j, x in enumerate(routines)]
			rvs_normal = [[utils.normalize(x)] for x in routines]
			initial_routines_other[stakeholder] = rvs_normal
		
		initial_routines_all =  [initial_routines_other]
		# initial_routines_all = [initial_routines] + [initial_routines_other]

		# flexi_grid =   [0.1, 0.9]
		# flexi_grid_dict = dict(zip(['1', *stakeholders[0]], [flexi_grid] * 5))
		# combinations = list(grid(flexi_grid_dict))

		# relative_influences = [list(x.values()) for x in combinations]
		relative_influences = [
							[0.25, 0.1875, 0.1875, 0.1875, 0.1875],
							[0.5, 0.125, 0.125, 0.125, 0.125],
							[0.75, 0.0625, 0.0625, 0.0625, 0.0625],
							[0.25, 0.61, 0.05, 0.01, 0.08],
							[0.5, 0.41, 0.03, 0.007, 0.053],
							[0.75, 0.203, 0.017, 0.003, 0.027]
							]

		flexi_grid =  [0.2, 0.4, 0.6, 0.8]
		flexi_grid_dict = dict(zip(stakeholders[0], [flexi_grid] * 4))
		combinations = list(grid(flexi_grid_dict))
		opinion_flexibilities = [list(x.values()) for x in combinations]
		# opinion_flexibilities = [[0.2, 0.2, 0.2, 0.2],
		# 						[0.5, 0.5, 0.5, 0.5],
		#                         [0.8, 0.8, 0.8, 0.8],
		#                         *opinion_flexibilities]          # (1 - np.array(combo['inter_group_influences'])).tolist()
		                                 #        ]
		param_grid = {
			'stakeholders': [stakeholders],
			'number_of_agents': [number_of_agents],
			'negotiation_frequency': [negotiation_frequency],
		    'inter_group_influences': inter_group_influences,
		    'intra_group_influences': [self.intra_group_influences],
		    'renewal_frequencies': renewal_frequencies,
		    'initial_routines': initial_routines_all,
		    'relative_influences': relative_influences,
		    'external_influences': [external_influences],
		    'opinion_flexibilities': opinion_flexibilities
		}

		
		params = list(grid(param_grid))
		self.experiment_parameters = params

	def run_experiment(self, experiment_number, time_steps):
		self.environment.simulate(time_steps)
		self.environment.data = pd.DataFrame.from_dict(self.environment.data)
		self.environment.data.to_json('data/raw/experiment_{}.json'.format(experiment_number), 'columns')
		# print('Experiment {} successfully completed at {} and saved to data/raw/experiment_{}.json'.\
		#       format(experiment_number,datetime.now().strftime("%H:%M:%S"), experiment_number))

	def run_experiments(self):
		pool = multiprocessing.Pool()
		pool.map(self.single_iter, list(range(len(self.experiment_parameters))))
		# for i in range(len(self.experiment_parameters)):
		# 	self.set_environment(self.experiment_parameters[i])
		# 	self.run_experiment(i+1, time_steps)

	def single_iter(self, i, time_steps=100):
			model = Model()
			model.set_environment(self.experiment_parameters[i])
			model.run_experiment(i+1, time_steps)
			del model
