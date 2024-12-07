# write a class to analyze data
# input is a file path, use pandas to read the file, and preprocess the data
# then wirte a function to calculate the precision and recall given two columns

import pandas as pd

class DataAnalysis:
	def __init__(self, file_path):
		self.file_path = file_path
		sep = ''
		with open(file_path, 'r', encoding="utf8") as f:
			first_line = f.readline()
			if '\t' in first_line:
				sep = '\t'
			elif ',' in first_line:
				sep = ','
			else:
				raise ValueError('The file does not contain the valid separator')
		self.df = pd.read_csv(file_path, sep=sep)
	

