import os
import data_functions as data_functions 

spark = data_functions.start_session()

root_directory = os.getcwd()
data_directory = root_directory + '/data/'
raw_data_directory = data_directory + 'raw/'
processed_data_directory = data_directory + 'processed/'

processed_files = os.listdir(processed_data_directory)

if 'experiment_1.csv' not in processed_files:
	file_path = raw_data_directory + 'experiment_1.json'
	save_path = processed_data_directory + 'experiment_1/'
	df = data_functions.process(spark, file_path)
	df = df.drop('input_intra_group_influences', 'input_number_of_agents', \
	             'input_stakeholders', 'input_initial_routines')
	# df.show(truncate=True, vertical=True)
	# df.dtypes.show()
	data_functions.save(df, save_path)
spark.stop()
exit()

if 'modelling_data.csv' not in processed_files or 'additional_data' not in processed_files:
	file_path = raw_data_directory
	df = data_functions.process(spark, file_path)
	save_path = processed_data_directory + 'modelling_data.csv'
	
	