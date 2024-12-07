import pandas as pd
from ..utils import *
from ..path import *

GroundTruth = 'GroundTruth'
Predict = 'Predict'
DEFAULT_OUTPUT_FILE_NAME = 'prf'


def calculate_prf(df, ground_truth_colunms, predict_columns, breakdown_column=None, weight_column=None, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Calculate the precision, recall, F1 of the prediction
	:param df: input dataframe
	:param ground_truth_colunms: ground truth columns
	:param predict_columns: predict columns
	:param breakdown_column: breakdown column
	:param weight_column: weight for the calculation
	:param drop_na: drop the rows with missing values in the ground_truth_colunms and predict_columns
	:param save_to_file: save the result to a csv file
	:param output_file_name: the name of the file to save the result
	:return: a dataframe with precision, recall, F1 of the prediction
	"""
	merged_prf = []
	# check the type of ground_truth_colunms and predict_columns if they are not list, convert them to list
	if not isinstance(ground_truth_colunms, list):
		ground_truth_colunms = [ground_truth_colunms]
	if not isinstance(predict_columns, list):
		predict_columns = [predict_columns]

	# check the length of ground_truth_colunms and predict_columns are the same
	assert len(ground_truth_colunms) == len(predict_columns), "The length of ground_truth_colunms and predict_columns should be the same"
	for i in range(len(ground_truth_colunms)):
		prf_df = calculate_single_pair_prf(df, ground_truth_colunms[i], predict_columns[i], breakdown_column=breakdown_column, weight_column=weight_column, drop_na=drop_na)
		merged_prf.append(prf_df)
	merged_prf = pd.concat(merged_prf)
	save_df_to_csv(merged_prf, save_to_file, default_output_file_name=DEFAULT_OUTPUT_FILE_NAME, custom_output_file_name=output_file_name)
	return merged_prf

def calculate_single_pair_prf(df, ground_truth_colunm, predict_column, breakdown_column=None, weight_column=None, drop_na=True):
	"""
	Calculate the precision, recall, F1 of the prediction
	:param df: input dataframe
	:param ground_truth_colunm: ground truth column
	:param predict_column: predict column
	:param breakdown_column: breakdown column
	:param weight_column: weight for the calculation
	:param drop_na: drop the rows with missing values in the ground_truth_colunm and predict_column
	:return: a dataframe with precision, recall, F1 of the prediction
	"""
	# # check df is a pandas dataframe, ground_truth_colunm and predict_column, breakdown_column are in the df
	# assert isinstance(df, pd.DataFrame), "df should be a pandas dataframe"
	# assert ground_truth_colunm in df.columns, f"{ground_truth_colunm} should be in the dataframe"
	# assert predict_column in df.columns, f"{predict_column} should be in the dataframe"
	# if breakdown_column is not None:
	# 	assert breakdown_column in df.columns, f"{breakdown_column} should be in the dataframe"
	
	# remove rows with missing values in the two columns
	if drop_na:
		df = drop_na_raw(df, [ground_truth_colunm, predict_column])

	# check the value of ground_truth_colunm and predict_column are in [0, 1]
	assert df[ground_truth_colunm].isin([0, 1]).all(), f"{ground_truth_colunm} should only contain 0 or 1"
	assert df[predict_column].isin([0, 1]).all(), f"{predict_column} should only contain 0 or 1"
	
	if breakdown_column is None:
		prf_df = calculate_prf_single(df, ground_truth_colunm, predict_column, weight_column)
		prf_df = prf_df.to_frame().T
	else:
		prf_df = df.groupby(breakdown_column).apply(lambda x: calculate_prf_single(x, ground_truth_colunm, predict_column, weight_column)).reset_index()
		# put the GroundTruth and Predict columns to the front
		cols = prf_df.columns.tolist()
		cols.remove(GroundTruth)
		cols.remove(Predict)
		prf_df = prf_df[[GroundTruth, Predict] + cols]
	return prf_df


def calculate_prf_single(df, ground_truth_colunm, predict_column, weight_column):
	"""
	Calculate the precision, recall, F1 of the prediction for a single group
	:param df: input dataframe
	:param ground_truth_colunm: ground truth column
	:param predict_column: predict column
	:param weight_column: weight for the calculation
	"""
	ground_truth = df[ground_truth_colunm].values.tolist()
	predict = df[predict_column].values.tolist()
	if weight_column is not None:
		weights = df[weight_column].values.tolist()
	TP = 0
	FP = 0
	TN = 0
	FN = 0
	for i in range(len(ground_truth)):
		weight = 1
		if weight_column is not None:
			weight = weights[i]
		if ground_truth[i] == 1 and predict[i] == 1:
			TP += weight
		elif ground_truth[i] == 0 and predict[i] == 1:
			FP += weight
		elif ground_truth[i] == 1 and predict[i] == 0:
			FN += weight
		elif ground_truth[i] == 0 and predict[i] == 0:
			TN += weight
		else:
			print("ground_truth and predict should be 0 or 1")
			raise ValueError(f"ground_truth: {ground_truth[i]}, predict: {predict[i]}")
	if TP + FP == 0:
		precision = 0
	else:
		precision = TP / (TP + FP)
	if TP + FN == 0:
		recall = 0
	else:
		recall = TP / (TP + FN)
	if precision + recall == 0:
		f1 = 0
	else:
		f1 = 2 * precision * recall / (precision + recall)
	ground_truth_positive = TP + FN
	ground_truth_positive_ratio = ground_truth_positive / len(ground_truth)
	predict_positive = TP + FP
	predict_positive_ratio = predict_positive / len(predict)
	ACC = (TP + TN) / (TP + FP + TN + FN)
	FPR = FP / (FP + TN)
	return pd.Series({GroundTruth: ground_truth_colunm, Predict: predict_column, 'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN, 'Precision': precision, 'Recall': recall, 'F1': f1, 'ACC': ACC, 'FPR': FPR,
				   'ground_truth_positive': ground_truth_positive, 'ground_truth_positive_ratio': ground_truth_positive_ratio, 
				   'predict_positive': predict_positive, 'predict_positive_ratio': predict_positive_ratio
				   })


