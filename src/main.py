import Environment
import random
random.seed(18)
import numpy as np

#  choice_frequency, group_influence, change_capacity, feedback_proximity
agent_dictionary = {'Student - Undergraduate': [100, 0.1, 0.1, 1, 1],
					'Student - Graduate': [],
					'Faculty - Instructor': [],
					'Faculty - Assistant Professor': [],
					'Faculty - Associate Professor': [],
					'Faculty - Professor': [],
					'Administration - Dean': [], 
					'Administration - Trustee': [],
					'Administration - Provost': [],
					'Administration - President/Chancellor': [],
					'Staff': [],
					'Alumni': []}

influences_between_groups = {'Students': [],
							'Faculty': [],
							'Administration': [],
							'Staff': [],
							'Alumni': []}