import os
import data_functions as data_functions 
import pandas as pd
import numpy as np


root_directory = os.getcwd()
data_directory = root_directory + '/data/'
raw_data_directory = data_directory + 'raw/'
if __name__ == '__main__':
	data_functions.edit_json_time(raw_data_directory)