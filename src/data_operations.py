import os
import data_functions as data_functions 
import pandas as pd
import numpy as np
import datetime

root_directory = os.getcwd()
data_directory = root_directory + '/data/'
raw_data_directory = data_directory + 'raw/'
spark = data_functions.start_session()

processed_data_directory = data_directory + 'processed/'

processed_files = os.listdir(processed_data_directory)
# print(processed_files)
stakeholders = ['students', 'faculty', 'managers','other']
to_expand = ['input_inter_group_influences', 'input_opinion_flexibilities', \
				'input_relative_influences', 'input_renewal_frequencies', 'organizational_routine', \
				'sd_change_faculty', 'sd_change_managers','sd_change_other', 'sd_change_students', \
				'sd_faculty', 'sd_managers', 'sd_other', 'sd_students','decisions_faculty', \
				'decisions_managers', 'decisions_other', 'decisions_students', \
				'means_faculty', 'means_managers', 'means_other', 'means_students'] 

if 'experiment_1' not in processed_files:
	print('converting experiment_1')
	file_path = raw_data_directory + 'experiment_1.json'
	save_path = processed_data_directory + 'experiment_1'
	# df = pd.read_json(file_path)

	# df['experiment']=df['experiment'].str.replace('(.*?)_','').str.replace(r'\.(.*)', '')

	# df['input_external_influences'].apply(pd.Series).rename(columns = lambda x: )
	# df = df.join(df.select([df.input_external_influences]  + \
	#             [df.input_external_influences[i][j].alias('input_external_influences_' + \
	#             stakeholders[j] + '_' + stakeholders[i]) for i in range(4) for j in range(4)]).\
	#         	drop(df.input_external_influences)).drop(df.input_external_influences)
	
	df = data_functions.process(spark, file_path)
	print('processed')
	print(df.count(), len(df.columns))
	df = df.repartition(1)
	# print('repartitioned')
	# print(df.rdd.getNumPartitions())
	# df.show(5, truncate=True, vertical=True)
	# df = df.toPandas()
	df.write.json(save_path)
	# print('processed')
	# print(df.dtypes)
	# print(df.rdd.getNumPartitions())
	# df.printSchema()
	# df = df.toPandas()
	# print(df)

	# print('topandas')
	# df.to_csv(save_path, header=True)

if 'all_data' not in processed_files:
	print('processing all data')
	file_path = raw_data_directory
	save_path = processed_data_directory + 'all_data'

	df = data_functions.process(spark, file_path)
	print('processed')
	# print(df.count(), len(df.columns))
	df = df.drop('input_intra_group_influences', 'input_number_of_agents', \
	             'input_stakeholders', 'input_initial_routines')
	# print(len(df.columns))
	print('dropped', datetime.datetime.now().time())
	df = df.coalesce(1)
	print('coalesced', datetime.datetime.now().time())
	df.write.csv(save_path, mode='overwrite', header='true') 
# if 'modelling_data' not in processed_files or 'additional_data' not in processed_files:
# 	file_path = raw_data_directory
# 	df = data_functions.process(spark, file_path)
# 	save_path = processed_data_directory + 'modelling_data.csv'
	
	