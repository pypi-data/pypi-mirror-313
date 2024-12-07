import os
import pandas as pd
from ..visualization import *
from ..path import *
from ..utils import *

DEFAULT_OUTPUT_FILE_NAME = 'sample'

def custom_sample(df, sample_filter, sample_count=None, breakdown_column=None, sample_columns=None, random_state=None, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Custom sample the dataframe
	:param df: input dataframe
	:param sample_filter: sample filter
	:param sample_count: sample size
	:param breakdown_column: breakdown column
	:param sample_columns: sample columns
	:param random_state: random state
	:param drop_na: drop the rows with missing values in the sample_columns
	:param save_to_file: save the result to a csv file
	:param output_file_name: the name of the file to save the result
	:return: a dataframe with sampled data
	"""
	print(f">>>> sample_filter : {sample_filter}")
	
	if sample_columns is None or len(sample_columns) == 0:
		sample_columns = df.columns.tolist()
	if sample_count is None:
		sample_count = 20
		print(f">>>> Sample size is not specified, use default value {sample_count}")
	
	# dedup according to sample_columns
	print(f">>>> Original dataframe size: {df.shape}")
	df = df.drop_duplicates(subset=sample_columns)
	print(f">>>> Deduped dataframe size: {df.shape}")

	if drop_na:
		df = drop_na_raw(df, sample_columns)
		print(f">>>> Drop na dataframe size: {df.shape}")

	# sample based on breakdown_column 
	if breakdown_column is not None and len(breakdown_column) > 0:
		sample_df = df[sample_columns].groupby(breakdown_column).apply(lambda x: x.query(sample_filter)).reset_index(drop=True)
		sample_df = sample_df.groupby(breakdown_column).apply(lambda x: simple_sample(x, sample_count, random_state=random_state)).reset_index(drop=True)
		print(f">>>> Sampled dataframe size for each group: {sample_df.groupby(breakdown_column).size()}")
	else:
		sample_df = df[sample_columns].query(sample_filter)
		sample_df = simple_sample(sample_df, sample_count, random_state=random_state)
	print(f">>>> Sampled dataframe size: {sample_df.shape}")
	save_df_to_csv(sample_df, save_to_file, default_output_file_name=DEFAULT_OUTPUT_FILE_NAME, custom_output_file_name=output_file_name)
	return sample_df


def simple_sample(df, sample_count, random_state=None):
	"""
	Sample the dataframe
	:param df: input dataframe
	:param sample_count: sample size
	:param random_state: random state
	return: sample dataframe
	"""
	if sample_count > df.shape[0]:
		print(f">>>> Sample size is larger than the dataframe size, use the dataframe size {df.shape[0]}")
		sample_count = df.shape[0]
	df = df.sample(sample_count, random_state=random_state)
	return df

