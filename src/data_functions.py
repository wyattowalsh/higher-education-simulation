import pyspark as ps
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import input_file_name,  split, to_date, collect_list, col, udf, pandas_udf
import os
import datetime
from pyspark.sql.functions import input_file_name
import os
from pyspark.sql.functions import lit
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.tuning import ParamGridBuilder
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
from pyspark.sql.functions import *
import numpy as np
import json
import multiprocessing

def start_session():
	# Initializing and configuring PySpark with session variable 'spark'
	sc = ps.SparkContext(appName="HEI Simulation")
	sc.setLogLevel('WARN')
	spark = SparkSession(sc)
	# spark = SparkSession.builder \
	# 		    .master('local[1]') \
	# 		    .config("spark.driver.memory", "2g") \
	# 		    .config("spark.executor.memory", '10g')\
	# 		    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
	# 		    .config("spark.executor.extrajavaoptions", '-Xmx1024m')\
	# 		    .config("spark.pyspark.virtualenv.enabled", 'true')\
	# 		    .config("spark.pyspark.virtualenv.type", 'conda')\
	# 		    .config("spark.pyspark.virtualenv.bin.path", \
	# 		            ' /Users/wyattowalsh/miniconda3/envs/ieor-174/bin')\
	# 		    .config("spark.driver.extraJavaOptions", "-verbose:gc -XX:+PrintGCDetails")\
	# 		    .config("spark.executor.extraJavaOptions", '-verbose:gc -XX:+PrintGCDetails')\
	# 		    .getOrCreate()
			    # conf.setAppName('App Name') \
    # .setMaster('spark://hostname-of-master:7077')
	# spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
	# spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")
	# spark.conf.set(, "org.apache.spark.serializer.KryoSerializer")
	# spark.conf.set("spark.driver.memory", '5g')
	# spark.conf.set("spark.sql.debug.maxToStringFields" , 500)
	# spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
	return spark

def save(df, path):
	df.repartition(90).write.csv(path, mode='overwrite', header='true') #compression='gzip',

def process(spark, path):

	stakeholders = ['students', 'faculty', 'managers','other']
	to_expand = ['input_inter_group_influences', 'input_opinion_flexibilities', \
				'input_renewal_frequencies', 'organizational_routine', \
				'sd_change_faculty', 'sd_change_managers','sd_change_other', 'sd_change_students', \
				'sd_faculty', 'sd_managers', 'sd_other', 'sd_students','decisions_faculty', \
				'decisions_managers', 'decisions_other', 'decisions_students', \
				'means_faculty', 'means_managers', 'means_other', 'means_students']
	# time_df = spark.range(0,101).toDF('id')
	df = spark.read.load(path, format="json").withColumn("experiment", input_file_name())
	# print(df.rdd.getNumPartitions())
	# print('onload:',df.count(), len(df.columns))# .repartition(1) #.repartition(32)
	df = df.withColumn('experiment', regexp_replace('experiment', r'(.*?)_', ''))
	df = df.withColumn('experiment', regexp_replace('experiment', r'\.(.*)', ''))
	# df.show(5, truncate=True, vertical=True)
	# print(df.show(2), df.count(), len(df.columns))
	# df = df.withColumn('experiment', regexp_replace('experiment', '.json', ''))\
	# print(len(df.columns))
	# print(df.rdd.getNumPartitions())
	labels = [["input_external_influences_{}_{}".format(j,i) for i in stakeholders] for j in stakeholders]
	to_add = df.select('time', 'experiment',
	          df.input_external_influences[0][0].alias(labels[0][0]), df.input_external_influences[0][1].alias(labels[0][1]),
	          df.input_external_influences[0][2].alias(labels[0][2]), df.input_external_influences[0][3].alias(labels[0][3]),
	          df.input_external_influences[1][0].alias(labels[1][0]), df.input_external_influences[1][1].alias(labels[1][1]),
	          df.input_external_influences[1][2].alias(labels[1][2]), df.input_external_influences[1][3].alias(labels[1][3]),
	          df.input_external_influences[2][0].alias(labels[2][0]), df.input_external_influences[2][1].alias(labels[2][1]),
	          df.input_external_influences[2][2].alias(labels[2][2]), df.input_external_influences[2][3].alias(labels[2][3]),
	          df.input_external_influences[3][0].alias(labels[3][0]), df.input_external_influences[3][1].alias(labels[3][1]),
	          df.input_external_influences[3][2].alias(labels[3][2]), df.input_external_influences[3][3].alias(labels[3][3]))
	# to_add.show()
	# df.time.show()
	# to_add.time.show()
	df = df.join(to_add, ['time', 'experiment']).drop('input_external_influences')

	column = 'input_relative_influences'
	to_add = df.select('time', 'experiment', col(column)[0].alias(column + '_external'),\
	                   	col(column)[0].alias(column + '_student'), col(column)[1].alias(column + '_faculty'),\
	                   	 col(column)[2].alias(column + '_managers'), col(column)[3].alias(column + '_other'))
	df = df.join(to_add, ['time', 'experiment']).drop('input_relative_influences')
	# print(len(df.columns))
	# print(df.rdd.getNumPartitions())
	column = to_expand[0]
	to_add = df.select('time', 'experiment', col(column)[0].alias(column + '_student'), \
		                   col(column)[1].alias(column + '_faculty'), col(column)[2].alias(column + '_managers'), \
		                   col(column)[3].alias(column + '_other'))
	for i, column in enumerate(to_expand[1:]):
		to_add = to_add.join(df.select('time', 'experiment', col(column)[0].alias(column + '_student'), \
		                   col(column)[1].alias(column + '_faculty'), col(column)[2].alias(column + '_managers'), \
		                   col(column)[3].alias(column + '_other')), ['time', 'experiment'])
		# print(len(to_add.columns))
		# print('completed join ', i, ' out of ', len(to_expand))
		# print('size: ', to_add.count(), " ", len(to_add.columns))

	df = df.drop(*to_expand)

	df = df.join(to_add, ['time', 'experiment'])
	# print(len(df.columns))
	# print(df.show(2), df.count(), len(df.columns))
	

	return df #.repartition(1)
	# df = df.join(df.select([df.input_inter_group_influences	]  + \
	#                [df.input_inter_group_influences[i] for i in range(4)]).\
	#         drop(df.input_inter_group_influences)).drop(df.input_inter_group_influences)

	# df = df.join(df.select([df.input_opinion_flexibilities]  + \
	#                [df.input_opinion_flexibilities[i] for i in range(4)]).\
	#         drop(df.input_opinion_flexibilities)).drop(df.input_opinion_flexibilities)

	# df = df.join(df.select([df.input_relative_influences]  + \
	#                [df.input_relative_influences[i] for i in range(4)]).\
	#         drop(df.input_relative_influences)).drop(df.input_relative_influences)

	# df = df.join(df.select([df.input_renewal_frequencies]  + \
	#                [df.input_renewal_frequencies[0]]).\
	#         drop(df.input_renewal_frequencies)).drop(df.input_renewal_frequencies)

	# df = df.join(df.select([df.organizational_routine]  + \
	#                [df.organizational_routine[i] for i in range(4)]).\
	#             drop(df.organizational_routine)).drop(df.organizational_routine)

	# df = df.join(df.select([df.sd_change_faculty]  + \
	#                [df.sd_change_faculty[i] for i in range(4)]).\
	#             drop(df.sd_change_faculty)).drop(df.sd_change_faculty)
	# df = df.join(df.select([df.sd_change_managers]  + \
	#                [df.sd_change_managers[i] for i in range(4)]).\
	#             drop(df.sd_change_managers)).drop(df.sd_change_managers)
	# df = df.join(df.select([df.sd_change_other]  + \
	#                [df.sd_change_other[i] for i in range(4)]).\
	#             drop(df.sd_change_other)).drop(df.sd_change_other)
	# df = df.join(df.select([df.sd_change_students]  + \
	#                [df.sd_change_students[i] for i in range(4)]).\
	#             drop(df.sd_change_students)).drop(df.sd_change_students)

	# df = df.join(df.select([df.sd_faculty]  + \
	#                [df.sd_faculty[i] for i in range(4)]).\
	#             drop(df.sd_faculty)).drop(df.sd_faculty)
	# df = df.join(df.select([df.sd_managers]  + \
	#                [df.sd_managers[i] for i in range(4)]).\
	#             drop(df.sd_managers)).drop(df.sd_managers)
	# df = df.join(df.select([df.sd_other]  + \
	#                [df.sd_other[i] for i in range(4)]).\
	#             drop(df.sd_other)).drop(df.sd_other)
	# df = df.join(df.select([df.sd_students]  + \
	#                [df.sd_students[i] for i in range(4)]).\
	#             drop(df.sd_students)).drop(df.sd_students)

	# df = df.join(df.select([df.decisions_faculty]  + \
	#                [df.decisions_faculty[i] for i in range(4)]).\
	#             drop(df.decisions_faculty)).drop(df.decisions_faculty)
	# df = df.join(df.select([df.decisions_managers]  + \
	#                [df.decisions_managers[i] for i in range(4)]).\
	#             drop(df.decisions_managers)).drop(df.decisions_managers)
	# df = df.join(df.select([df.decisions_other]  + \
	#                [df.decisions_other[i] for i in range(4)]).\
	#             drop(df.decisions_other)).drop(df.decisions_other)
	# df = df.join(df.select([df.decisions_students]  + \
	#                [df.decisions_students[i] for i in range(4)]).\
	#             drop(df.decisions_students)).drop(df.decisions_students)

	# df = df.join(df.select([df.means_faculty]  + \
	#                [df.means_faculty[i] for i in range(4)]).\
	#             drop(df.means_faculty)).drop(df.means_faculty)
	# df = df.join(df.select([df.means_managers]  + \
	#                [df.means_managers[i] for i in range(4)]).\
	#             drop(df.means_managers)).drop(df.means_managers)
	# df = df.join(df.select([df.means_other]  + \
	#                [df.means_other[i] for i in range(4)]).\
	#             drop(df.means_other)).drop(df.means_other)
	# df = df.join(df.select([df.means_students]  + \
	#                [df.means_students[i] for i in range(4)]).\
	#             drop(df.means_students)).drop(df.means_students)
	# print(df.columns)
	 #.repartition(32)

def variable_selection_model(df):
	pass

def edit_json_time(directory_path):
	files = os.listdir(directory_path)
	files = [directory_path + file for file in files]
	pool = multiprocessing.Pool()
	pool.map(edit_json_time_helper, files)

def edit_json_time_helper(path):
		a = open(path)
		b = json.load(a)
		df = pd.DataFrame(b)
		df.at[0, 'time'] = 0
		df.to_json(path, 'records')	
		print(path, "successfully modified")	