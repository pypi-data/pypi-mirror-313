import os
from os import environ, listdir
from os.path import join

import pandas as pd


def load_file(file_path, sep=None):
	"""
	Load the file
	:param file_path: the file path
	:param sep: the separator of the file
	:return: the dataframe
	"""
	if sep is None:
		with open(file_path, 'r', encoding="utf8") as f:
			first_line = f.readline()
			if '\t' in first_line:
				sep = '\t'
			elif ',' in first_line:
				sep = ','
			else:
				raise ValueError('The file does not contain the valid separator')
	df = pd.read_csv(file_path, sep=sep)
	return df


def load_dir(dir_path, target_str=None, sep=None):
	"""
	Load all files in the directory with the target string in the file name
	:param dir_path: the directory path
	:param target_str: the target string in the file name
	:param sep: the separator of the file
	:return: the concatenated dataframe
	"""
	if target_str is not None:
		file_paths = [join(dir_path, f) for f in listdir(dir_path) if target_str in f]
	else:
		file_paths = [join(dir_path, f) for f in listdir(dir_path)]
	dfs = []
	for file_path in file_paths:
		dfs.append(load_file(file_path, sep))
	df = pd.concat(dfs)
	df = df.reset_index(drop=True)
	return df

