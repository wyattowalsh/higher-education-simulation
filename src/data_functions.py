import pyspark as ps
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

def start_session():
	# Initializing and configuring PySpark with session variable 'spark'
	sc = ps.SparkContext(appName="HEI Simulation")
	# sc.setLogLevel('ALL')
	spark = SparkSession(sc)
	spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
	return spark

def save(df, path):
	df.write.csv(path= path, mode="append", header="true")

def process(spark, path):
	df = spark.read.load(path, format="json").withColumn("experiment", input_file_name())
	df = df.withColumn('experiment', regexp_replace('experiment', 'file://' + path + 'experiment_', ''))
	df = df.withColumn('experiment', regexp_replace('experiment', '.json', ''))
	df = df.join(df.select([df.input_external_influences]  + \
	               [df.input_external_influences[i][j] for i in range(4) for j in range(4)]).\
	        drop(df.input_external_influences)).drop(df.input_external_influences)

	to_expand = ['input_inter_group_influences', 'input_opinion_flexibilities', \
				'input_relative_influences', 'input_renewal_frequencies', 'organizational_routine', \
				'sd_change_faculty', 'sd_change_managers','sd_change_other', 'sd_change_students', \
				'sd_faculty', 'sd_managers', 'sd_other', 'sd_students','decisions_faculty', \
				'decisions_managers', 'decisions_other', 'decisions_students', \
				'means_faculty', 'means_managers', 'means_other', 'means_students']

	new_cols = [df.select([df[x]] + \
	               [df[x][i] for i in range(4)]).\
	        drop(df[x]) for x in to_expand]

	for i, column in enumerate(to_expand):
		df = df.join(new_cols[i]).drop(column)

	


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
	return df

def variable_selection_model(df):
	pass
