import time
import pandas as pd
from ..path import *

def save_df_to_csv(df, save_to_file, default_output_file_name, custom_output_file_name=None):
	"""
	Save the dataframe to a csv file
	:param df: DataFrame
	:param save_to_file: if save path
	:param default_output_file_name: default output file name
	:param custom_output_file_name: custom output file name
	"""
	if not save_to_file:
		return
	
	path = get_output_dir()
	if custom_output_file_name is not None:
		path += f'/{custom_output_file_name}.csv'
	else:
		default_output_file_name += f'_{time.strftime("%Y%m%d%H%M%S")}'
		path += f'/{default_output_file_name}.csv'

	df.to_csv(path, index=False)
	print(f">>>> save dataframe result to {path}")

def drop_na_raw(df, columns):
	"""
	Drop the rows with na value in the columns
	:param df: DataFrame
	:param columns: list of column names
	:return: DataFrame
	"""
	all_rows = df.shape[0]
	df = df.dropna(subset=columns)
	drop_rows = all_rows - df.shape[0]
	print(f'>>>> all rows = {all_rows}, drop rows = {drop_rows} in {columns}')
	return df
