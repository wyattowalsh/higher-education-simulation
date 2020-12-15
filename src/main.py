import model as model 
import random
random.seed(18)

model = model.Model()
stakeholders = [['students', 'faculty', 'managers', 'other']]
number_of_agents = [305, 25, 5, 40] # 61, 5, 1, 8
negotiation_frequency = [1, 5]
model.generate_experiment_parameter_set(stakeholders, number_of_agents, negotiation_frequency)
# model.set_environment(model.experiment_parameters[0])
# model.run_experiment(1, 100)
# print(len(model.experiment_parameters)) # 13824
# print(model.experiment_parameters[0])
# # # time_steps_per_experiment = 100
if __name__ == '__main__':
	model.run_experiments()
# model.run_experiments()



